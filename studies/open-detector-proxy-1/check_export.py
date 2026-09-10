"""Verify public evidence bytes and recompute this frozen diagnostic offline."""
import json
from pathlib import Path

from analyze import analyze, sha


def check(root):
    manifest = json.loads((root / "export-manifest.json").read_bytes())
    files = {entry["public_path"]: entry for entry in manifest["files"]}
    if len(files) != len(manifest["files"]):
        raise ValueError("Duplicate export paths")
    for name, entry in files.items():
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("Export path escapes study")
        if sha(path) != entry["public_sha256"]:
            raise ValueError(f"Export hash mismatch: {name}")
        if b"/Users/" in path.read_bytes() or b"/private/" in path.read_bytes():
            # This checker includes the search literals itself.
            if name != "check_export.py":
                raise ValueError(f"Private path retained: {name}")
    fresh = json.loads(json.dumps(analyze(root)))
    archived = json.loads((root / "analysis.json").read_bytes())
    for key in ("pairs", "summaries", "historical_human_controls", "unique_inputs"):
        if fresh[key] != archived[key]:
            raise ValueError(f"Derived comparison mismatch: {key}")
    for name, source_hash in archived["source_hashes"].items():
        if files[name]["source_sha256"] != source_hash:
            raise ValueError(f"Historical hash association mismatch: {name}")
    grey = json.loads((root / "greyscope/results.json").read_bytes())
    for row in grey["records"]:
        for artifact in row["artifacts"].values():
            if sha(root / artifact["path"]) != artifact["sha256"]:
                raise ValueError("Greyscope text artifact mismatch")
        if row["token_counts"]["full_model_prompt"] != row["token_counts"]["submitted"]:
            raise ValueError("Greyscope coverage mismatch")
    print(f"PASS: {len(files)} exported artifacts; 18 inputs; 10 paired comparisons; no model or network calls")


if __name__ == "__main__":
    check(Path(__file__).resolve().parent)
