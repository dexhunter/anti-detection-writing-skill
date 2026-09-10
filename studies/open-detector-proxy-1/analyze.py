"""Compare frozen native local outputs with archived GPTZero observations."""
import argparse
import hashlib
import json
import math
from pathlib import Path

LOCAL_DROP = 0.01
GPTZERO_DROP = 5.0


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analyze(root):
    def load(name):
        return json.loads((root / name).read_bytes())
    manifest = load("inference-manifest.json")
    expected = {row["id"]: row for row in manifest["records"]}
    if len(expected) != len(manifest["records"]):
        raise ValueError("Duplicate input IDs")
    for row in expected.values():
        if sha(root / row["path"]) != row["sha256"]:
            raise ValueError("Input hash mismatch")
    targets = load("targets.json")
    commercial = {}
    for row in targets["observations"]:
        value = (row["ai"], row["mixed"], row["human"])
        if row["input_id"] in commercial and commercial[row["input_id"]] != value:
            raise ValueError("Repeated commercial outcomes disagree; define explicit pair observation mapping")
        commercial[row["input_id"]] = value
    reports = {name: load(f"{name}/results.json") for name in ("oculus", "greyscope")}
    manifest_sha = sha(root / "inference-manifest.json")
    if reports["oculus"]["input_manifest_sha256"] != manifest_sha or reports["greyscope"]["corpus_sha256"] != manifest_sha:
        raise ValueError("Inference manifest mismatch")
    local = {}
    for name, report in reports.items():
        rows = {row["id"]: row for row in report["records"]}
        if set(rows) != set(expected) or len(rows) != len(report["records"]):
            raise ValueError("Missing, duplicate or unexpected model records")
        for key, row in rows.items():
            if row["input_sha256"] != expected[key]["sha256"]:
                raise ValueError("Measured input mismatch")
            field = "ai_probability" if name == "oculus" else "ai_involvement_full_precision"
            value = row[field]
            if row["status"] in ("complete", "ok"):
                if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
                    raise ValueError("Invalid native score")
            elif value is not None:
                raise ValueError("Failed input must retain a null score")
        local[name] = {key: row["ai_probability" if name == "oculus" else "ai_involvement_full_precision"] for key, row in rows.items()}
    pairs = []
    for pair in targets["pairs"]:
        a, b = pair["baseline"], pair["candidate"]
        g_delta = commercial[a][0] - commercial[b][0]
        row = {**pair, "gptzero_baseline": commercial[a], "gptzero_candidate": commercial[b],
               "gptzero_ai_drop_percentage_points": g_delta, "gptzero_meaningful_drop": g_delta >= GPTZERO_DROP}
        for name, scores in local.items():
            before, after = scores[a], scores[b]
            delta = None if before is None or after is None else before - after
            row[name] = {"baseline": before, "candidate": after, "drop": delta,
                         "meaningful_drop": None if delta is None else delta >= LOCAL_DROP,
                         "any_drop": None if delta is None else delta > 0}
        pairs.append(row)
    summaries = {}
    for name in local:
        complete = [p for p in pairs if p[name]["drop"] is not None]
        reductions = [p for p in complete if p["gptzero_meaningful_drop"]]
        ties = [p for p in complete if p["gptzero_ai_drop_percentage_points"] == 0]
        summaries[name] = {
            "available_pairs": len(complete), "unavailable_pairs": len(pairs) - len(complete),
            "historical_reduction_pairs": len(reductions), "historical_tie_pairs": len(ties),
            "recognized_reductions": sum(p[name]["meaningful_drop"] for p in reductions),
            "misleading_reductions_on_ties": sum(p[name]["meaningful_drop"] for p in ties),
            "recognized_reductions_any_drop": sum(p[name]["any_drop"] for p in reductions),
            "misleading_reductions_on_ties_any_drop": sum(p[name]["any_drop"] for p in ties),
            "interpretation": "Counts describe dependent selected historical observations, not independent accuracy or future success rates"}
    controls = [{"id": key, **{name: scores[key] for name, scores in local.items()}, "gptzero": None}
                for key, row in expected.items() if row.get("origin") == "historical_human"]
    return {"schema_version": 1, "local_drop_threshold": LOCAL_DROP, "gptzero_drop_threshold_percentage_points": GPTZERO_DROP,
            "native_units": {"oculus": "sigmoid AI probability 0–1", "greyscope": "calibrated ordinal AI involvement 0–1", "gptzero": "document confidence percent"},
            "commercial_scans_this_study": 0, "unique_inputs": len(expected), "pairs": pairs,
            "summaries": summaries, "historical_human_controls": controls,
            "source_hashes": {name: sha(root / name) for name in ("inference-manifest.json", "targets.json", "protocol.md", "oculus/results.json", "greyscope/results.json")}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(args.root)
    if args.output:
        with args.output.open("x") as stream:
            json.dump(result, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
    print(json.dumps(result["summaries"], indent=2))
