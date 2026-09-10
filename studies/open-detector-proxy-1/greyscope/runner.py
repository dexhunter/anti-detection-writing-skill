"""Frozen-input, offline Greyscope MLX inference with no token truncation."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "model"
SOURCE = ROOT / "author-source"
SOURCE_REVISION = "e052f07b5e5bddacce41fe4d5fcc3250081385da"
MODEL_REVISION = "59b6ec7a24cae161c4cbc85e594c586541d8f710"
MODEL_ID = "yaoandy107/greyscope-v2-qwen3.5-4b-mlx-4bit"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def disable_network() -> None:
    os.environ.update(
        HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", HF_HUB_DISABLE_TELEMETRY="1",
        HF_HUB_DISABLE_IMPLICIT_TOKEN="1", DO_NOT_TRACK="1", TOKENIZERS_PARALLELISM="false",
    )

    def audit(event, _args):
        if event in {"socket.connect", "socket.connect_ex", "socket.sendto", "socket.getaddrinfo"}:
            raise RuntimeError(f"Network forbidden during local inference: {event}")

    sys.addaudithook(audit)


def freeze() -> None:
    tracked = [
        SOURCE / "greyscope" / name
        for name in ("__init__.py", "inference.py", "corn.py", "preprocess.py",
                     "mlx_inference.py", "mlx_model.py")
    ] + [SOURCE / "uv.lock", SOURCE / "pyproject.toml", ROOT / "runner.py"]
    tracked += sorted(p for p in MODEL.iterdir() if p.is_file())
    artifacts = {str(p.relative_to(ROOT)): {"sha256": file_hash(p), "bytes": p.stat().st_size}
                 for p in tracked}
    versions = {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()}
    manifest = {
        "schema_version": 1, "source_revision": SOURCE_REVISION,
        "source_url": "https://github.com/yaoandy107/greyscope",
        "model_id": MODEL_ID, "model_revision": MODEL_REVISION,
        "artifacts": artifacts, "versions": dict(sorted(versions.items())),
        "python": sys.version, "platform": platform.platform(), "machine": platform.machine(),
        "score_semantics": "calibrated AI involvement; not GPTZero confidence",
        "artifact_manifest_sha256": sha256(json.dumps(artifacts, sort_keys=True).encode()),
    }
    write_json(ROOT / "manifest.json", manifest)


def verify_manifest() -> dict:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for rel, metadata in manifest["artifacts"].items():
        if file_hash(ROOT / rel) != metadata["sha256"]:
            raise ValueError(f"Frozen artifact hash mismatch: {rel}")
    return manifest


def clean_with_audit(text: str, calib: dict) -> tuple[str, list[dict]]:
    from greyscope import preprocess as p

    if not calib["lowercase"]:
        return text, []
    body = text
    steps = []
    for name, function in [
        ("normalize_unicode", p.normalize_unicode), ("normalize_emoji", p.normalize_emoji),
        ("remove_think_tag", p.remove_think_tag), ("remove_ai_header", p.remove_ai_header),
        ("lowercase", str.lower), ("normalize_whitespace", p.normalize_whitespace),
    ]:
        changed = function(body)
        steps.append({
            "step": name, "changed": changed != body, "before_chars": len(body),
            "after_chars": len(changed), "before_sha256": sha256(body.encode()),
            "after_sha256": sha256(changed.encode()),
            "meaningful_removal_flag": changed != body and name in {
                "remove_think_tag", "remove_ai_header"},
        })
        body = changed
    assert body == p.clean_text(text), "Audited preprocessing must equal the author implementation"
    return body, steps


def encode_full(tokenizer, text: str) -> list[int]:
    return tokenizer.encode(text, add_special_tokens=False, truncation=False)


def prepare_record(record: dict, corpus_parent: Path, tokenizer, calib: dict) -> tuple[dict, list[int]]:
    source_path = (corpus_parent / record["path"]).resolve()
    raw = source_path.read_bytes()
    digest = sha256(raw)
    if digest != record["sha256"]:
        raise ValueError(f"Input SHA256 mismatch for {record['id']}")
    text = raw.decode("utf-8", errors="strict")
    body, steps = clean_with_audit(text, calib)
    prompt = calib["prompt_template"].format(text=body)
    token_ids = encode_full(tokenizer, prompt)
    output_dir = ROOT / "prepared"
    output_dir.mkdir(exist_ok=True)
    files = {"raw": raw, "cleaned": body.encode(), "prompt": prompt.encode()}
    artifacts = {}
    for kind, data in files.items():
        path = output_dir / f"{digest}.{kind}.txt"
        path.write_bytes(data)
        artifacts[kind] = {"path": str(path), "sha256": sha256(data), "bytes": len(data)}
    overflow = len(token_ids) > calib["max_length"]
    result = {
        "id": record["id"], "input_path": str(source_path), "input_sha256": digest,
        "status": "unavailable" if overflow else "ready",
        "error": {"type": "input_exceeds_calibrated_token_limit", "limit": calib["max_length"]}
        if overflow else None,
        "artifacts": artifacts, "preprocessing": steps,
        "meaningful_removed_content": any(s["meaningful_removal_flag"] for s in steps),
        "raw_equals_cleaned_bytes": raw == body.encode(),
        "token_counts": {
            "raw_text": len(encode_full(tokenizer, text)),
            "cleaned_text": len(encode_full(tokenizer, body)),
            "raw_text_with_prompt": len(encode_full(tokenizer, calib["prompt_template"].format(text=text))),
            "full_model_prompt": len(token_ids), "submitted": 0,
        },
        "token_ids_sha256": sha256(json.dumps(token_ids, separators=(",", ":")).encode()),
        "max_length": calib["max_length"], "length_gate": "full_model_prompt_after_author_cleaning",
        "truncation": False, "raw_logits": None, "bucket_probs": None,
        "label": None, "ai_involvement": None, "runtime_seconds": None,
        "native": None, "native_binary": None, "corn_cumulative_probs": None,
        "bucket_probs_full_precision": None, "corn_scalar_full_precision": None,
        "ai_involvement_full_precision": None,
    }
    return result, token_ids


def decode_details(raw_logits: list[float], calib: dict) -> dict:
    import numpy as np
    from greyscope.corn import corn_bucket_probs, corn_cumulative_probs, corn_scalar_score
    from greyscope.inference import decode_logits

    if len(raw_logits) != 3 or not all(math.isfinite(x) for x in raw_logits):
        raise ValueError("Expected exactly three finite CORN conditional logits")
    raw = np.asarray([raw_logits], dtype=float)
    native = decode_logits(raw_logits, calib, mode="ternary")
    scalar = float(corn_scalar_score(raw)[0])
    oriented = -scalar if calib["flip"] else scalar
    scaled = min(max((oriented - calib["score_min"]) /
                     (calib["score_max"] - calib["score_min"]), 0.0), 1.0)
    return {
        **native, "native": native, "native_binary": decode_logits(raw_logits, calib, mode="binary"),
        "raw_logits": raw_logits, "corn_cumulative_probs": corn_cumulative_probs(raw)[0].tolist(),
        "bucket_probs_full_precision": dict(zip(calib["bucket_descriptions"], corn_bucket_probs(raw)[0].tolist())),
        "corn_scalar_full_precision": scalar, "ai_involvement_full_precision": scaled,
    }


def score_one(row: dict, token_ids: list[int], model, calib: dict) -> dict:
    if row["status"] != "ready":
        return row
    if len(token_ids) > calib["max_length"]:
        raise ValueError("Overflow escaped preparation guard")
    import mlx.core as mx

    started = time.perf_counter()
    try:
        raw = model(mx.array([token_ids]))
        mx.eval(raw)
        values = raw[0].tolist()
        row.update(decode_details(values, calib), status="ok", error=None)
        row["token_counts"]["submitted"] = len(token_ids)
    except Exception as exc:
        row.update(status="error", error={"type": type(exc).__name__, "message": str(exc)})
    row["runtime_seconds"] = time.perf_counter() - started
    return row


def verify_author_parity(row, token_ids, model, tokenizer, calib):
    import mlx.core as mx
    from unittest.mock import patch
    from greyscope.mlx_inference import detect_mlx

    observed = {}

    def traced_model(inputs):
        observed["token_ids"] = inputs[0].tolist()
        raw = model(inputs)
        mx.eval(raw)
        observed["raw_logits"] = raw[0].tolist()
        return raw

    original = Path(row["artifacts"]["raw"]["path"]).read_bytes().decode()
    started = time.perf_counter()
    with patch("greyscope.mlx_inference._load_mlx", return_value=(traced_model, tokenizer, calib)):
        native = detect_mlx(original, model=str(MODEL))
    parity = {
        "id": row["id"], "native_outputs_equal": native == row["native"],
        "all_token_ids_equal": observed["token_ids"] == token_ids,
        "raw_logits_equal": observed["raw_logits"] == row["raw_logits"],
        "runtime_seconds": time.perf_counter() - started,
    }
    assert all(parity[k] for k in ("native_outputs_equal", "all_token_ids_equal", "raw_logits_equal"))
    return parity


def run(corpus_path: Path, prepare_only: bool) -> None:
    disable_network()
    sys.path.insert(0, str(SOURCE))
    manifest = verify_manifest()
    from mlx_lm.utils import load_tokenizer

    calib = json.loads((MODEL / "calibration.json").read_text())
    assert calib["head_type"] == "corn" and calib["n_buckets"] == 4 and calib["max_length"] == 2048
    corpus_bytes = corpus_path.read_bytes()
    corpus = json.loads(corpus_bytes)
    records = corpus["records"]
    ids = [r["id"] for r in records]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate input IDs")
    tokenizer = load_tokenizer(MODEL, tokenizer_config_extra={"local_files_only": True})
    started = time.perf_counter()
    prepared = [prepare_record(record, corpus_path.parent, tokenizer, calib) for record in records]
    report = {
        "schema_version": 1, "model_id": MODEL_ID, "model_revision": MODEL_REVISION,
        "source_revision": SOURCE_REVISION, "manifest_sha256": file_hash(ROOT / "manifest.json"),
        "artifact_manifest_sha256": manifest["artifact_manifest_sha256"],
        "model_weights_sha256": manifest["artifacts"]["model/model.safetensors"]["sha256"],
        "versions": manifest["versions"], "platform": manifest["platform"],
        "corpus_path": str(corpus_path), "corpus_sha256": sha256(corpus_bytes),
        "score_semantics": manifest["score_semantics"], "network_mode": "offline_with_python_socket_audit_guard",
        "input_count": len(records), "calibration": calib, "truncation": False,
        "records": [row for row, _ in prepared], "prepare_seconds": time.perf_counter() - started,
    }
    write_json(ROOT / "prepared.json", report)
    if prepare_only:
        print(json.dumps({"prepared": len(records), "unavailable": sum(r["status"] == "unavailable" for r, _ in prepared)}))
        return
    import mlx.core as mx
    from greyscope.mlx_inference import _load_mlx

    load_started = time.perf_counter()
    loaded_model, loaded_tokenizer, loaded_calib = _load_mlx(str(MODEL))
    report["model_load_seconds"] = time.perf_counter() - load_started
    assert loaded_calib == calib
    for row, token_ids in prepared:
        prompt = Path(row["artifacts"]["prompt"]["path"]).read_bytes().decode()
        assert encode_full(loaded_tokenizer, prompt) == token_ids
        row.update(model_weights_sha256=report["model_weights_sha256"], model_revision=MODEL_REVISION,
                   source_revision=SOURCE_REVISION, artifact_manifest_sha256=manifest["artifact_manifest_sha256"])
        score_one(row, token_ids, loaded_model, calib)
        if row["status"] == "ok" and "author_entrypoint_parity" not in report:
            report["author_entrypoint_parity"] = verify_author_parity(
                row, token_ids, loaded_model, loaded_tokenizer, calib)
        write_json(ROOT / "results.partial.json", report)
        print(json.dumps({"id": row["id"], "status": row["status"], "tokens": len(token_ids)}), flush=True)
    report.update(
        total_seconds=time.perf_counter() - started,
        peak_mlx_memory_bytes=mx.get_peak_memory(),
        peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        count_ok=sum(r["status"] == "ok" for r, _ in prepared),
        count_unavailable=sum(r["status"] == "unavailable" for r, _ in prepared),
        count_error=sum(r["status"] == "error" for r, _ in prepared),
    )
    assert [r["id"] for r in report["records"]] == ids
    assert file_hash(corpus_path) == report["corpus_sha256"]
    for row, _ in prepared:
        assert file_hash(Path(row["input_path"])) == row["input_sha256"]
    verify_manifest()
    write_json(ROOT / "results.json", report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--corpus", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    if args.freeze:
        freeze()
    else:
        if args.corpus is None:
            parser.error("--corpus is required")
        run(args.corpus.resolve(), args.prepare_only)
