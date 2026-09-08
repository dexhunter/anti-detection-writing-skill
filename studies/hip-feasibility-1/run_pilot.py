"""Bounded local HIP feasibility study; no detector calls or publication."""

import hashlib
import importlib.metadata
import json
import platform
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

ROOT = Path(__file__).resolve().parent
PLAN = json.loads((ROOT / "plan.json").read_text())


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def clean(text):
    text = text.strip()
    if text.startswith("<target_text>"):
        text = text[len("<target_text>") :].lstrip()
    return text.split("</target_text>", 1)[0].strip()


def protected(text):
    return {
        "code": re.findall(r"```[\s\S]*?```|`[^`\n]+`", text),
        "urls": re.findall(r"https?://[^\s)]+", text),
    }


def main():
    if (ROOT / "run.json").exists():
        raise RuntimeError("Existing run; do not overwrite or silently retry candidates")
    started = datetime.now(timezone.utc).isoformat()
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "mps" else torch.float32
    cache = str(ROOT / "weights")
    tok = AutoTokenizer.from_pretrained(
        PLAN["adapter"], revision=PLAN["adapter_revision"], cache_dir=cache,
        trust_remote_code=False, token=False,
    )
    tok.padding_side = "left"
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    inputs = []
    for case in PLAN["cases"]:
        source = (ROOT / "inputs" / (case + ".md")).read_text()
        prompt = f"<source_text>\n{source.strip()}\n</source_text>\n\n<target_text>\n"
        encoded = tok(prompt, return_tensors="pt", truncation=False)
        count = int(encoded["input_ids"].shape[1])
        if count > PLAN["max_input_tokens"]:
            raise RuntimeError(f"Input too long: {case}, {count}; no truncation")
        inputs.append((case, source, prompt, encoded))
    print(json.dumps({"device": device, "dtype": str(dtype), "input_tokens": {
        c: int(e["input_ids"].shape[1]) for c, _, _, e in inputs
    }}), flush=True)
    model = AutoModelForCausalLM.from_pretrained(
        PLAN["base"], revision=PLAN["base_revision"], cache_dir=cache,
        trust_remote_code=False, use_safetensors=True, token=False,
        torch_dtype=dtype, attn_implementation="sdpa",
    )
    model = PeftModel.from_pretrained(
        model, PLAN["adapter"], revision=PLAN["adapter_revision"],
        cache_dir=cache, token=False, autocast_adapter_dtype=False,
    ).to(device).eval()
    # Override unrelated inherited sampling settings explicitly.
    records = []
    for index, (case, source, prompt, encoded) in enumerate(inputs):
        set_seed(PLAN["seed"] + index)
        encoded = {k: v.to(device) for k, v in encoded.items()}
        t0 = time.monotonic()
        with torch.inference_mode():
            output = model.generate(
                **encoded, max_new_tokens=PLAN["max_new_tokens"], do_sample=True,
                temperature=1.0, top_p=0.95, top_k=0, repetition_penalty=1.0,
                pad_token_id=tok.pad_token_id, eos_token_id=tok.eos_token_id,
            )
        ids = output[0, encoded["input_ids"].shape[1] :].cpu().tolist()
        raw = tok.decode(ids, skip_special_tokens=True)
        candidate = clean(raw)
        (ROOT / "outputs" / (case + ".raw.txt")).write_text(raw)
        (ROOT / "outputs" / (case + ".md")).write_text(candidate)
        (ROOT / "outputs" / (case + ".prompt.txt")).write_text(prompt)
        record = {
            "case": case, "source_sha256": digest(source),
            "prompt_sha256": digest(prompt), "candidate_sha256": digest(candidate),
            "raw_sha256": digest(raw), "generated_tokens": len(ids),
            "ended_on_eos": bool(ids and ids[-1] == tok.eos_token_id),
            "target_closing_tag": "</target_text>" in raw,
            "hit_token_limit": len(ids) == PLAN["max_new_tokens"],
            "source_words": len(source.split()), "candidate_words": len(candidate.split()),
            "protected_before": protected(source), "protected_after": protected(candidate),
            "seed": PLAN["seed"] + index, "elapsed_seconds": time.monotonic() - t0,
            "detector": "not_measured_pending_independent_quality_review",
        }
        records.append(record)
        (ROOT / "outputs" / (case + ".json")).write_text(json.dumps(record, indent=2) + "\n")
        print(json.dumps(record), flush=True)
    result = {
        "started_at": started, "completed_at": datetime.now(timezone.utc).isoformat(),
        "plan_sha256": digest((ROOT / "plan.json").read_text()),
        "runner_sha256": digest(Path(__file__).read_text()),
        "device": device, "dtype": str(dtype), "platform": platform.platform(),
        "packages": {p: importlib.metadata.version(p) for p in [
            "torch", "transformers", "peft", "huggingface-hub", "safetensors"
        ]}, "records": records,
    }
    (ROOT / "run.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
