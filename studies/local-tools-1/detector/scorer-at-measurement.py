#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#   "torch==2.8.0",
#   "transformers==4.57.6",
#   "safetensors==0.8.0",
#   "sentencepiece==0.2.1",
# ]
# ///
"""Score complete development texts with one pinned, already-local open detector."""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import re
import sys
import time

MODEL_ID = "desklib/ai-text-detector-v1.01"
REVISION = "5fdea974cd4287c61674951ec78803aa274e2fb7"
MAX_TOKENS = 768
MODEL_MANIFEST = Path(__file__).resolve().parents[1] / "references/local-detector-model.json"
SHA256 = re.compile(r"[a-f0-9]{64}")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def stamp():
    return datetime.now(timezone.utc).isoformat()


def relative_path(root, name, allow_external_symlink=False):
    require(isinstance(name, str) and name.strip(), "Missing relative file path")
    path = Path(name)
    require(not path.is_absolute() and ".." not in path.parts and name != ".",
            "File paths must be relative without parent traversal")
    target = root / path
    if not allow_external_symlink:
        require(target.resolve().is_relative_to(root.resolve()), "Input path escapes its directory")
    return target


def read_manifest(path):
    raw = path.read_bytes()
    manifest = json.loads(raw)
    require(isinstance(manifest, dict) and type(manifest.get("schema_version")) is int
            and manifest["schema_version"] == 1, "Expected input manifest schema_version 1")
    records = manifest.get("records")
    require(isinstance(records, list) and bool(records), "Manifest records must be a nonempty list")
    seen = set()
    for record in records:
        require(isinstance(record, dict), "Every input record must be an object")
        key = record.get("id")
        require(isinstance(key, str) and key.strip() and key not in seen,
                "Input IDs must be nonempty and unique")
        seen.add(key)
        require(isinstance(record.get("sha256"), str) and SHA256.fullmatch(record["sha256"]),
                "Every input needs a lowercase SHA-256")
        relative_path(path.parent, record.get("path"))
    return records, digest(raw)


def verify_model(model_dir, manifest_path=MODEL_MANIFEST):
    raw = manifest_path.read_bytes()
    spec = json.loads(raw)
    require(isinstance(spec, dict) and type(spec.get("schema_version")) is int
            and spec["schema_version"] == 1, "Unsupported model manifest")
    require(spec.get("model_id") == MODEL_ID and spec.get("revision") == REVISION,
            "Model manifest differs from the supported pinned model")
    files = spec.get("files")
    require(isinstance(files, dict) and {"config.json", "model.safetensors",
            "tokenizer_config.json", "spm.model"} <= set(files), "Model manifest lacks required files")
    require(model_dir.is_dir(), "Model directory does not exist")
    for name, expected in files.items():
        require(isinstance(expected, str) and SHA256.fullmatch(expected), "Invalid model file hash")
        # Standard Hugging Face snapshots point to sibling cached blobs. The
        # frozen byte hash, rather than symlink containment, verifies these files.
        path = relative_path(model_dir, name, allow_external_symlink=True)
        require(file_digest(path) == expected, f"Model file hash mismatch: {name}")
    # Prevent a tokenizer/config loader from preferring an unverified extra file.
    loader_suffixes = {".json", ".safetensors", ".bin", ".pt", ".pth", ".model", ".py"}
    for path in model_dir.iterdir():
        if path.is_file() and path.suffix in loader_suffixes:
            require(path.name in files, f"Unverified loader file: {path.name}")
    return {"model_id": MODEL_ID, "revision": REVISION,
            "manifest_sha256": digest(raw), "files": files}


def sigmoid(logit):
    require(type(logit) in (int, float) and math.isfinite(logit), "Nonfinite or invalid model logit")
    if logit >= 0:
        return 1.0 / (1.0 + math.exp(-logit))
    value = math.exp(logit)
    return value / (1.0 + value)


def score_record(record, root, backend):
    started = time.monotonic()
    result = {"id": record["id"], "path": record["path"],
              "expected_input_sha256": record["sha256"], "input_sha256": None,
              "input_bytes": None, "whitespace_words": None, "full_token_count": None,
              "token_ids_sha256": None, "status": "failed", "raw_logit": None,
              "ai_probability": None, "error": None}
    try:
        raw = relative_path(root, record["path"]).read_bytes()
        result.update(input_sha256=digest(raw), input_bytes=len(raw))
        require(result["input_sha256"] == record["sha256"], "Input hash mismatch")
        text = raw.decode("utf-8")
        require(bool(text.strip()), "Input text is empty")
        result["whitespace_words"] = len(text.split())
        ids = backend.encode(text)
        require(isinstance(ids, list) and ids and all(type(v) is int and v >= 0 for v in ids),
                "Tokenizer returned invalid token IDs")
        result.update(full_token_count=len(ids), token_ids_sha256=digest(
            json.dumps(ids, separators=(",", ":")).encode("utf-8")))
        require(len(ids) <= MAX_TOKENS,
                f"Input has {len(ids)} tokens including special tokens; limit is {MAX_TOKENS}; no truncation")
        logit = backend.score(ids)
        probability = sigmoid(logit)
        result.update(status="complete", raw_logit=logit, ai_probability=probability)
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
    result["elapsed_seconds"] = time.monotonic() - started
    return result


class DesklibBackend:
    """The published masked-mean/single-logit architecture; no remote loading."""

    def __init__(self, model_dir, device):
        import torch
        from safetensors.torch import load_file
        from transformers import AutoConfig, AutoModel, AutoTokenizer

        require(device in ("cpu", "mps"), "Device must be cpu or mps")
        if device == "mps":
            require(torch.backends.mps.is_available(), "Requested MPS device is unavailable")
        config = AutoConfig.from_pretrained(model_dir, local_files_only=True, trust_remote_code=False)
        require(config.model_type == "deberta-v2", "Unexpected detector backbone")

        class Detector(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.model = AutoModel.from_config(config, trust_remote_code=False)
                self.classifier = torch.nn.Linear(config.hidden_size, 1)

            def forward(self, input_ids, attention_mask):
                hidden = self.model(input_ids, attention_mask=attention_mask)[0]
                mask = attention_mask.unsqueeze(-1).expand(hidden.size()).float()
                pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)
                return self.classifier(pooled)

        self.torch = torch
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_dir, local_files_only=True, trust_remote_code=False)
        self.model = Detector()
        state = load_file(str(model_dir / "model.safetensors"), device="cpu")
        self.model.load_state_dict(state, strict=True)
        del state
        self.model.to(device=device, dtype=torch.float32)
        self.model.eval()
        self.runtime = {"python": sys.version.split()[0], "device": device, "dtype": "float32",
                        "packages": {name: importlib.metadata.version(name) for name in
                                     ("torch", "transformers", "safetensors", "sentencepiece")},
                        "inference_mode": True, "model_training": self.model.training,
                        "padding_tokens": MAX_TOKENS, "truncation": False,
                        "scoring": "attention-mask-weighted mean; single linear logit; sigmoid",
                        "higher_probability": "AI", "documents_per_forward": 1}

    def encode(self, text):
        return self.tokenizer(text, add_special_tokens=True, padding=False, truncation=False)["input_ids"]

    def score(self, ids):
        encoded = self.tokenizer.pad({"input_ids": [ids], "attention_mask": [[1] * len(ids)]},
                                     padding="max_length", max_length=MAX_TOKENS, return_tensors="pt")
        with self.torch.inference_mode():
            logits = self.model(input_ids=encoded["input_ids"].to(self.device),
                                attention_mask=encoded["attention_mask"].to(self.device))
        require(tuple(logits.shape) == (1, 1), "Unexpected classifier output shape")
        return float(logits.item())


def run(model_dir, manifest, output, device="cpu", backend_factory=DesklibBackend,
        model_manifest=MODEL_MANIFEST):
    require(not output.exists(), "Output already exists; choose a new path")
    records, input_manifest_hash = read_manifest(manifest)
    model = verify_model(model_dir, model_manifest)
    started = stamp()
    backend = backend_factory(model_dir, device)
    rows = [score_record(record, manifest.parent, backend) for record in records]
    report = {"schema_version": 1, "scope": "local_proxy", "unit": "sigmoid_probability_0_to_1",
              "commercial_detector_measurement": False,
              "limitations": "Uncalibrated local model output; not GPTZero/Pangram, authorship proof, quality review or skill promotion.",
              "started_at": started, "completed_at": stamp(), "model": model,
              "input_manifest_sha256": input_manifest_hash,
              "script_sha256": file_digest(Path(__file__).resolve()),
              "runtime": backend.runtime, "records": rows,
              "successful_records": sum(row["status"] == "complete" for row in rows),
              "failed_records": sum(row["status"] == "failed" for row in rows)}
    encoded = json.dumps(report, indent=2, allow_nan=False) + "\n"
    # Exclusive creation also handles another process winning the output path.
    with output.open("x", encoding="utf-8") as stream:
        stream.write(encoded)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("model-dir", "manifest", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "mps"), default="cpu")
    args = parser.parse_args(argv)
    try:
        report = run(args.model_dir, args.manifest, args.output, args.device)
    except (ValueError, OSError, KeyError, TypeError, ImportError, RuntimeError) as error:
        print(f"Local detector setup failed: {error}", file=sys.stderr)
        return 2
    print(json.dumps({"scope": report["scope"], "successful_records": report["successful_records"],
                      "failed_records": report["failed_records"], "output": str(args.output)}))
    return 1 if report["failed_records"] else 0


if __name__ == "__main__":
    sys.exit(main())
