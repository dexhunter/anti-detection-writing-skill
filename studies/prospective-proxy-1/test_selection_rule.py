"""Synthetic offline checks; no prospective drafts, reviews, or scores are read."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parent / "selection_rule.py"
SPEC = importlib.util.spec_from_file_location("selection_rule_under_test", SCRIPT)
rule = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rule)


class SelectionRuleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "quality").mkdir()
        (self.root / "greyscope").mkdir()
        self.manifest = {"schema_version": 1, "records": []}
        cases = []
        for case_id, prefix in (("case-a", "a"), ("case-b", "b")):
            answers = []
            for number in (1, 2, 3):
                key = f"{prefix}{number}"
                path = f"{key}.txt"
                raw = f"Synthetic fixture {key}; not a real answer.\n".encode()
                (self.root / path).write_bytes(raw)
                sha = hashlib.sha256(raw).hexdigest()
                self.manifest["records"].append({"id": key, "case_id": case_id, "path": path, "sha256": sha})
                answers.append({"id": key, "sha256": sha, "factual_pass": True, "acceptable": True, "qualifications_pass": True})
            cases.append({"id": case_id, "answers": answers,
                          "preference_groups": [[f"{prefix}2", f"{prefix}1"], [f"{prefix}3"]]})
        self.review = {"detector_scores_withheld": True, "cases": cases}
        self.write("inference-manifest.json", self.manifest)
        self.write("quality/review.json", self.review)
        self.scores = {"a1": 0.6, "a2": 0.5, "a3": 0.01,
                       "b1": 0.7, "b2": 0.8, "b3": 0.01}

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value, allow_nan=True), encoding="utf-8")

    def gate(self):
        self.write("inference-manifest.json", self.manifest)
        self.write("quality/review.json", self.review)
        return rule.freeze_quality(self.root)

    def rows(self):
        return [{"id": row["id"], "status": "ok", "input_sha256": row["sha256"],
                 "ai_involvement_full_precision": self.scores[row["id"]]}
                for row in self.manifest["records"]]

    def cli_fixture(self):
        gate = self.gate()
        rule.write_new(self.root / "quality-gate.json", gate)
        self.write("greyscope/results.json", {"corpus_sha256": gate["manifest_sha256"], "records": self.rows()})
        return gate

    def run_select(self):
        return subprocess.run([sys.executable, str(SCRIPT), "select", "--root", str(self.root)],
                              capture_output=True, text=True, check=False)

    def assert_select_rejected(self, message):
        result = self.run_select()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)
        self.assertFalse((self.root / "selection.json").exists())

    def test_quality_control_uses_lexicographic_tie_break_without_local_scores(self):
        gate = self.gate()
        self.assertEqual([case["control_id"] for case in gate["cases"]], ["a1", "b1"])
        self.assertEqual(gate["cases"][0]["eligible_ids"], ["a1", "a2"])
        # Reordering equally preferred answers cannot change the frozen control.
        self.review["cases"][0]["preference_groups"][0].reverse()
        reordered = self.gate()
        self.assertEqual(reordered["cases"], gate["cases"])

    def test_lower_score_on_inferior_quality_answer_cannot_win(self):
        result = rule.select_candidates(self.gate(), self.rows())
        self.assertEqual([case["candidate_id"] for case in result["cases"]], ["a2", "b1"])
        self.assertEqual([case["dispatch"] for case in result["cases"]], [True, False])

    def test_equal_local_score_preserves_control_as_no_op(self):
        self.scores["a2"] = self.scores["a1"]
        first = rule.select_candidates(self.gate(), self.rows())["cases"][0]
        self.assertEqual(first["candidate_id"], "a1")
        self.assertEqual(first["state"], "no_op")
        self.assertEqual(first["local_drop"], 0)
        self.assertFalse(first["dispatch"])

    def test_one_percent_boundary_and_below_threshold(self):
        gate = self.gate()
        for candidate, state in ((0.0200001, "below_local_threshold"),
                                 (0.02, "promising"), (0.019, "promising")):
            with self.subTest(candidate=candidate):
                self.scores.update(a1=0.03, a2=candidate)
                first = rule.select_candidates(gate, self.rows())["cases"][0]
                self.assertEqual(first["state"], state)
                self.assertEqual(first["dispatch"], state == "promising")

    def test_any_failed_alternative_makes_entire_case_unavailable(self):
        gate = self.gate()
        for failed_id in ("a1", "a2", "a3"):
            with self.subTest(failed_id=failed_id):
                rows = self.rows()
                next(row for row in rows if row["id"] == failed_id).update(
                    status="error", ai_involvement_full_precision=None)
                result = rule.select_candidates(gate, rows)
                self.assertEqual(len(result["cases"]), 2)
                first = result["cases"][0]
                self.assertEqual(first["state"], "local_unavailable")
                self.assertIsNone(first["candidate_id"])
                self.assertIsNone(first["local_drop"])
                self.assertFalse(first["dispatch"])
                self.assertEqual(result["cases"][1]["state"], "no_op")

    def test_all_quality_rejected_cases_still_remain_in_plan(self):
        for case in self.review["cases"]:
            case["preference_groups"] = []
            for answer in case["answers"]:
                answer["factual_pass"] = False
        result = rule.select_candidates(self.gate(), self.rows())
        self.assertEqual([case["id"] for case in result["cases"]], ["case-a", "case-b"])
        self.assertEqual([case["state"] for case in result["cases"]], ["quality_rejected"] * 2)
        self.assertTrue(all(case["candidate_id"] is None and not case["dispatch"] for case in result["cases"]))

    def test_missing_duplicate_and_unexpected_local_records_rejected(self):
        gate = self.gate()
        for mutation in ("missing", "duplicate", "unexpected"):
            with self.subTest(mutation=mutation):
                rows = self.rows()
                if mutation == "missing":
                    rows.pop()
                elif mutation == "duplicate":
                    rows.append(dict(rows[0]))
                else:
                    rows[-1]["id"] = "unplanned"
                with self.assertRaises(ValueError):
                    rule.select_candidates(gate, rows)

    def test_nonfinite_invalid_and_out_of_range_completed_scores_rejected(self):
        gate = self.gate()
        for value in (float("nan"), float("inf"), -float("inf"), None, True, "0.5", -0.01, 1.01):
            with self.subTest(value=value):
                rows = self.rows()
                rows[0]["ai_involvement_full_precision"] = value
                with self.assertRaises(ValueError):
                    rule.select_candidates(gate, rows)

    def test_nonfinite_successful_record_rejected_even_when_another_record_failed(self):
        rows = self.rows()
        rows[0]["ai_involvement_full_precision"] = float("nan")
        rows[2].update(status="error", ai_involvement_full_precision=None)
        with self.assertRaises(ValueError):
            rule.select_candidates(self.gate(), rows)

    def test_nonfinite_successful_record_rejected_in_quality_rejected_case(self):
        self.review["cases"][0]["preference_groups"] = []
        for answer in self.review["cases"][0]["answers"]:
            answer["factual_pass"] = False
        rows = self.rows()
        rows[0]["ai_involvement_full_precision"] = float("nan")
        with self.assertRaises(ValueError):
            rule.select_candidates(self.gate(), rows)

    def test_duplicate_input_manifest_rows_rejected(self):
        self.manifest["records"].append(dict(self.manifest["records"][0]))
        with self.assertRaises(ValueError):
            self.gate()

    def test_duplicate_quality_case_rejected(self):
        self.review["cases"].append(copy.deepcopy(self.review["cases"][0]))
        with self.assertRaises(ValueError):
            self.gate()

    def test_missing_quality_case_and_duplicate_quality_findings_rejected(self):
        original = copy.deepcopy(self.review)
        self.review["cases"].pop()
        with self.assertRaises(ValueError):
            self.gate()
        self.review = original
        self.review["cases"][0]["answers"].append(dict(self.review["cases"][0]["answers"][0]))
        with self.assertRaises(ValueError):
            self.gate()

    def test_all_quality_verdict_fields_must_pass_for_eligibility(self):
        original = copy.deepcopy(self.review)
        for field in ("factual_pass", "acceptable", "qualifications_pass"):
            with self.subTest(field=field):
                self.review = copy.deepcopy(original)
                self.review["cases"][0]["answers"][0][field] = False
                self.review["cases"][0]["preference_groups"] = [["a2"], ["a3"]]
                gate = self.gate()
                self.assertEqual(gate["cases"][0]["eligible_ids"], ["a2"])
                self.assertEqual(gate["cases"][0]["control_id"], "a2")
                self.scores["a1"] = 0.0
                selected = rule.select_candidates(gate, self.rows())["cases"][0]
                self.assertEqual(selected["candidate_id"], "a2")
                self.assertEqual(selected["state"], "no_op")

    def test_preference_group_cannot_include_unacceptable_or_unqualified_answer(self):
        original = copy.deepcopy(self.review)
        for field in ("acceptable", "qualifications_pass"):
            with self.subTest(field=field):
                self.review = copy.deepcopy(original)
                self.review["cases"][0]["answers"][0][field] = False
                with self.assertRaises(ValueError):
                    self.gate()

    def test_missing_quality_verdict_is_not_implicitly_passing(self):
        self.review["cases"][0]["answers"][0].pop("acceptable")
        with self.assertRaises(ValueError):
            self.gate()

    def test_failed_or_unavailable_record_requires_null_score(self):
        gate = self.gate()
        for status in ("error", "unavailable"):
            with self.subTest(status=status):
                rows = self.rows()
                rows[2]["status"] = status
                with self.assertRaises(ValueError):
                    rule.select_candidates(gate, rows)
                rows[2]["ai_involvement_full_precision"] = None
                selected = rule.select_candidates(gate, rows)
                self.assertEqual(selected["cases"][0]["state"], "local_unavailable")
                self.assertEqual(len(selected["cases"]), 2)

    def test_unknown_local_status_rejected(self):
        rows = self.rows()
        rows[0].update(status="unrecognized-status", ai_involvement_full_precision=None)
        with self.assertRaises(ValueError):
            rule.select_candidates(self.gate(), rows)

    def test_quality_review_requires_scores_withheld(self):
        self.review["detector_scores_withheld"] = False
        with self.assertRaisesRegex(ValueError, "withhold detector scores"):
            self.gate()

    def test_reviewed_content_hash_must_match_before_freeze(self):
        (self.root / "a1.txt").write_text("Changed synthetic text.")
        with self.assertRaisesRegex(ValueError, "Reviewed output hash mismatch"):
            self.gate()

    def test_select_cli_retains_all_cases_and_binds_gate_and_local_hashes(self):
        self.cli_fixture()
        result = self.run_select()
        self.assertEqual(result.returncode, 0, result.stderr)
        selected = json.loads((self.root / "selection.json").read_bytes())
        self.assertEqual(len(selected["cases"]), 2)
        self.assertEqual(selected["quality_gate_sha256"], rule.digest(self.root / "quality-gate.json"))
        self.assertEqual(selected["local_results_sha256"], rule.digest(self.root / "greyscope/results.json"))

    def test_review_bytes_frozen_between_phases_even_for_whitespace_change(self):
        self.cli_fixture()
        with (self.root / "quality/review.json").open("a") as stream:
            stream.write("\n")
        self.assert_select_rejected("Quality gate changed after local scores")

    def test_manifest_bytes_frozen_between_phases_even_for_whitespace_change(self):
        self.cli_fixture()
        with (self.root / "inference-manifest.json").open("a") as stream:
            stream.write("\n")
        self.assert_select_rejected("Quality gate changed after local scores")

    def test_actual_input_bytes_frozen_between_phases(self):
        self.cli_fixture()
        (self.root / "a1.txt").write_text("Changed synthetic input after freeze.")
        self.assert_select_rejected("Reviewed output hash mismatch")

    def test_local_manifest_hash_mismatch_rejected(self):
        self.cli_fixture()
        report = json.loads((self.root / "greyscope/results.json").read_bytes())
        report["corpus_sha256"] = "0" * 64
        self.write("greyscope/results.json", report)
        self.assert_select_rejected("Local results use a different input manifest")

    def test_local_input_hash_mismatch_rejected(self):
        self.cli_fixture()
        report = json.loads((self.root / "greyscope/results.json").read_bytes())
        report["records"][0]["input_sha256"] = "0" * 64
        self.write("greyscope/results.json", report)
        self.assert_select_rejected("Local input hash mismatch")


if __name__ == "__main__":
    unittest.main()
