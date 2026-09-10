"""Freeze quality-only choices, then apply the predeclared local selection rule."""
import argparse
import hashlib
import json
import math
from decimal import Decimal
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def freeze_quality(root):
    manifest = json.loads((root / "inference-manifest.json").read_bytes())
    review = json.loads((root / "quality/review.json").read_bytes())
    if review.get("detector_scores_withheld") is not True:
        raise ValueError("Quality review must withhold detector scores")
    records = {r["id"]: r for r in manifest["records"]}
    if len(records) != 6 or len(manifest["records"]) != 6:
        raise ValueError("Expected six frozen outputs")
    case_ids = [case["id"] for case in review["cases"]]
    expected_cases = {record["case_id"] for record in records.values()}
    if len(case_ids) != 2 or len(set(case_ids)) != 2 or set(case_ids) != expected_cases:
        raise ValueError("Missing or duplicate quality cases")
    cases = []
    seen = set()
    for case in review["cases"]:
        expected = {k for k, r in records.items() if r["case_id"] == case["id"]}
        answers = {a["id"]: a for a in case["answers"]}
        if len(expected) != 3 or set(answers) != expected or len(answers) != len(case["answers"]):
            raise ValueError("Missing or duplicate quality findings")
        for key, answer in answers.items():
            if any(type(answer.get(field)) is not bool for field in
                   ("factual_pass", "acceptable", "qualifications_pass")):
                raise ValueError("Every quality verdict must be explicitly boolean")
            record = records[key]
            if answer["sha256"] != record["sha256"] or digest(root / record["path"]) != record["sha256"]:
                raise ValueError("Reviewed output hash mismatch")
        groups = case["preference_groups"]
        ranked = [key for group in groups for key in group]
        passed = {key for key, answer in answers.items()
                  if all(answer[field] is True for field in
                         ("factual_pass", "acceptable", "qualifications_pass"))}
        if set(ranked) != passed or len(ranked) != len(set(ranked)) or any(not group for group in groups):
            raise ValueError("Preference groups must rank every passing answer exactly once")
        top = sorted(groups[0]) if groups else []
        cases.append({"id": case["id"], "all_input_ids": sorted(expected), "eligible_ids": top,
                      "control_id": top[0] if top else None,
                      "state": "quality_ready" if top else "quality_rejected"})
        seen.update(expected)
    if seen != set(records):
        raise ValueError("Missing quality cases")
    return {"schema_version": 1, "review_sha256": digest(root / "quality/review.json"),
            "manifest_sha256": digest(root / "inference-manifest.json"), "cases": cases,
            "rule": "Best quality group only; quality control lexicographic ID; local minimum within same group; required decrease 0.01"}


def select_candidates(gate, rows):
    local = {row["id"]: row for row in rows}
    expected = {key for case in gate["cases"] for key in case["all_input_ids"]}
    if set(local) != expected or len(local) != len(rows):
        raise ValueError("Local results must retain exactly every frozen input")
    for row in rows:
        status = row.get("status")
        if status not in ("ok", "error", "unavailable"):
            raise ValueError("Unknown local result status")
        if "ai_involvement_full_precision" not in row:
            raise ValueError("Every local result must declare its score or null")
        score = row["ai_involvement_full_precision"]
        if status == "ok":
            if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError("Completed local score must be finite and within 0–1")
        elif score is not None:
            raise ValueError("Unavailable or failed local scores must be null")
    cases = []
    for case in gate["cases"]:
        result = {**case, "candidate_id": None, "local_drop": None, "dispatch": False}
        if case["state"] == "quality_rejected":
            cases.append(result)
            continue
        # Any unavailable row retains the whole planned case as unavailable.
        # Never improve selection by silently omitting a failed alternative.
        if any(local[key]["status"] != "ok" for key in case["all_input_ids"]):
            result["state"] = "local_unavailable"
            cases.append(result)
            continue
        candidate = min(case["eligible_ids"], key=lambda key: (local[key]["ai_involvement_full_precision"], key))
        control = case["control_id"]
        drop = (Decimal(str(local[control]["ai_involvement_full_precision"]))
                - Decimal(str(local[candidate]["ai_involvement_full_precision"])))
        state = "no_op" if candidate == control else "promising" if drop >= Decimal("0.01") else "below_local_threshold"
        result.update(candidate_id=candidate, control_score=local[control]["ai_involvement_full_precision"],
                      candidate_score=local[candidate]["ai_involvement_full_precision"],
                      local_drop=float(drop), state=state, dispatch=state == "promising")
        cases.append(result)
    return {"schema_version": 1, "scope": "prospective local-selection diagnostic", "cases": cases,
            "gptzero_results": None, "commercial_scans_so_far": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("freeze-quality", "select"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.root
    gate = freeze_quality(root)
    if args.phase == "freeze-quality":
        write_new(root / "quality-gate.json", gate)
        print(json.dumps(gate, indent=2))
    else:
        if gate != json.loads((root / "quality-gate.json").read_bytes()):
            raise ValueError("Quality gate changed after local scores")
        local = json.loads((root / "greyscope/results.json").read_bytes())
        if local["corpus_sha256"] != gate["manifest_sha256"]:
            raise ValueError("Local results use a different input manifest")
        frozen = json.loads((root / "inference-manifest.json").read_bytes())["records"]
        hashes = {r["id"]: r["sha256"] for r in frozen}
        if any(r["input_sha256"] != hashes[r["id"]] for r in local["records"]):
            raise ValueError("Local input hash mismatch")
        result = select_candidates(gate, local["records"])
        result.update(quality_gate_sha256=digest(root / "quality-gate.json"),
                      local_results_sha256=digest(root / "greyscope/results.json"))
        write_new(root / "selection.json", result)
        print(json.dumps(result, indent=2))
