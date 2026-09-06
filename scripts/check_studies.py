#!/usr/bin/env python3
"""Check the public study files and recompute counts; do not authenticate scores."""

import argparse
import hashlib
import json
import math
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(root):
    root = root.resolve()
    dataset = json.loads((root / "studies/results.json").read_text(encoding="utf-8"))
    require(dataset["schema_version"] == 1, "Unknown dataset schema")
    summary = Counter(dict.fromkeys(dataset["expected_summary"], 0))
    seen_cases, seen_inputs, seen_cohorts = set(), set(), set()
    roles_by_design = {
        "baseline_plain": {"baseline", "plain"},
        "baseline_plain_fixed_body_quotation": {"baseline", "plain", "quoted"},
        "unpaired_final_text": {"final"},
    }
    for cohort in dataset["cohorts"]:
        require(cohort["id"] not in seen_cohorts, "Duplicate cohort")
        seen_cohorts.add(cohort["id"])
        roles = roles_by_design[cohort["design"]]
        for case in cohort["cases"]:
            require(case["discussion_url"] not in seen_cases, "Duplicate question")
            seen_cases.add(case["discussion_url"])
            for url in (case["discussion_url"], case["owned_comment_url"]):
                if url is not None:
                    parsed = urlsplit(url)
                    require(parsed.scheme == "https" and parsed.netloc == "github.com"
                            and "/discussions/" in parsed.path, "Invalid public discussion URL")
            scans = case["scans"]
            require(set(scans) == roles, "Incomplete or unexpected comparison roles")
            summary["questions"] += 1
            inputs = {}
            for role, scan in scans.items():
                relative = Path(scan["input"])
                require(not relative.is_absolute() and ".." not in relative.parts,
                        "Invalid input path")
                path = (root / relative).resolve()
                require(path.is_relative_to(root / "studies/inputs"), "Input outside study directory")
                require(path not in seen_inputs, "Duplicate input file")
                seen_inputs.add(path)
                raw = path.read_bytes()
                require(hashlib.sha256(raw).hexdigest() == scan["input_sha256"],
                        f"Input hash mismatch: {relative}")
                inputs[role] = raw.decode("utf-8")
                scores = [scan[f"{label}_percent"] for label in ("ai", "mixed", "human")]
                require(all(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 100
                            for v in scores), "Invalid confidence")
                require(abs(sum(scores) - 100) <= 1, "Confidences do not sum to 100")
                require((scan["service"], scan["mode"], scan["model"])
                        == ("GPTZero", "Basic Scan", "4.9b"), "Unexpected historical service/mode/model")
                observed = datetime.fromisoformat(scan["observed_at"].replace("Z", "+00:00"))
                require(observed.utcoffset() is not None, "Missing timestamp timezone")
                require(type(scan["displayed_words"]) is int and scan["displayed_words"] > 0,
                        "Invalid word count")
                require(type(scan["short_text_warning"]) is bool, "Missing warning flag")
                require(scan["short_text_warning"] == (scan["displayed_words"] < 100),
                        "Historical short-text flag inconsistent with recorded word count")
                require(scan["added_asker_quotation"] == (role in ("quoted", "final")),
                        "Quotation metadata mismatch")
                if scan["added_asker_quotation"]:
                    require(inputs[role].startswith("> "), "Missing attributed excerpt")
                    require(len(inputs[role].splitlines()[0][2:].split()) <= 25,
                            "Asker excerpt exceeds the study's quotation limit")
                summary["scans"] += 1
                summary["short_text_warnings"] += scan["short_text_warning"]
            quality = case["quality"]
            require(quality["reviewer_type"] == "separate_llm_agent"
                    and quality["detector_scores_withheld"] is True, "Review provenance mismatch")
            if "plain" in scans:
                require(quality["plain_technical"] == "PASS", "Unexpected technical review outcome")
                require(quality["plain_prose"] in ("IMPROVED", "EQUIVALENT"), "Unknown prose outcome")
                summary["plain_comparisons"] += 1
                summary["plain_reductions"] += scans["plain"]["ai_percent"] < scans["baseline"]["ai_percent"]
                summary["plain_prose_" + quality["plain_prose"].lower()] += 1
            if "quoted" in scans:
                require(inputs["quoted"].partition("\n\n")[2] == inputs["plain"],
                        "Quotation comparison changed the answer body")
                require(quality["quoted_technical"] == "PASS"
                        and quality["quoted_prose"] == "EQUIVALENT", "Quotation review mismatch")
                summary["quotation_comparisons"] += 1
                summary["quotation_reductions"] += scans["quoted"]["ai_percent"] < scans["plain"]["ai_percent"]
            if "final" in scans:
                require(quality["final_technical"] == "PASS", "Unexpected new-answer review outcome")
                summary["unpaired_final_texts"] += 1
                summary["unpaired_below_100"] += scans["final"]["ai_percent"] < 100
    require(seen_inputs == {p.resolve() for p in (root / "studies/inputs").rglob("*.txt")},
            "Unlisted or missing study inputs")
    require(dict(summary) == dataset["expected_summary"],
            f"Summary mismatch: computed {dict(summary)}")
    return dict(summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = check(args.root)
    except (ValueError, KeyError, OSError, TypeError, AttributeError) as error:
        parser.exit(1, f"Study check failed: {error}\n")
    print(json.dumps({"result": "consistent_public_artifacts", "summary": result,
                      "limit": "Does not authenticate or rerun detector measurements."}, indent=2))


if __name__ == "__main__":
    main()
