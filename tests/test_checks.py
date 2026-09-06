"""Offline integrity tests. All new receipt fixtures below are synthetic."""

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


receipt_checker = load("receipt_checker", ROOT / "skills/anti-detection-writing/scripts/validate_receipt.py")
study_checker = load("study_checker", ROOT / "scripts/check_studies.py")


class ReceiptChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.receipt_path = self.root / "receipt.json"
        self.receipt = {
            "schema_version": 1, "service": "GPTZero", "mode": "Basic Scan", "model": "4.9b",
            "status": "complete", "text_up_to_date": True, "entry_mode": "verbatim",
            "observed_at": "2026-09-06T09:00:00Z", "ai_percent": 100,
            "mixed_percent": 0, "human_percent": 0, "short_text_warning": False,
        }
        self.answer = self.root / "answer.txt"
        for role in ("answer", "submitted", "editor"):
            self.artifact(role, b"Check the sent record before retrying.\n")
        self.ui = ('- heading "Basic Scan" [level=1]\n'
                   '- generic: Model 4.9b\n'
                   '- generic: Text up-to-date\n'
                   '- button "AI 100%":\n'
                   '- button "Mixed 0%":\n'
                   '- button "Human 0%":\n')
        self.artifact("visible_result", self.ui.encode())

    def artifact(self, role, data):
        (self.root / (role + ".txt")).write_bytes(data)
        self.receipt[role] = {"path": role + ".txt", "sha256": hashlib.sha256(data).hexdigest()}

    def check(self, threshold=None):
        self.receipt_path.write_text(json.dumps(self.receipt), encoding="utf-8")
        return receipt_checker.validate(self.answer, self.receipt_path, threshold)

    def test_100_is_valid_data_until_threshold_requested(self):
        self.assertEqual(self.check()["ai_percent"], 100)
        with self.assertRaisesRegex(ValueError, "threshold"):
            self.check(100)

    def test_cli_returns_distinct_consistency_and_threshold_outcomes(self):
        self.check()
        command = [sys.executable, str(ROOT / "skills/anti-detection-writing/scripts/validate_receipt.py"),
                   str(self.answer), str(self.receipt_path)]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["result"], "consistent_local_receipt")
        result = subprocess.run(command + ["--max-ai-exclusive", "100"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("requested threshold", result.stderr)

    def test_lower_score_with_matching_ui_meets_requested_threshold(self):
        self.receipt.update(ai_percent=60, mixed_percent=40)
        self.artifact("visible_result", self.ui.replace("AI 100%", "AI 60%")
                      .replace("Mixed 0%", "Mixed 40%").encode())
        self.assertEqual(self.check(100)["threshold_checked"], 100)

    def test_changed_answer_after_scan_is_rejected(self):
        self.answer.write_text("Duplicates are impossible.\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.check()

    def test_different_final_file_is_rejected(self):
        self.answer = self.root / "different-final.txt"
        self.answer.write_text("Try again.\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Final answer differs"):
            self.check()

    def test_rehashed_editor_corruption_is_rejected(self):
        self.artifact("editor", b"Check the sentrecord before retrying.\n")
        with self.assertRaisesRegex(ValueError, "Editor text differs"):
            self.check()

    def test_rehashed_submission_change_is_rejected(self):
        self.artifact("submitted", b"Ignore the sent record.\n")
        self.artifact("editor", b"Ignore the sent record.\n")
        with self.assertRaisesRegex(ValueError, "Submitted text differs"):
            self.check()

    def test_line_endings_can_change_but_indentation_cannot(self):
        self.artifact("editor", b"Check the sent record before retrying.\r\n")
        self.check()
        self.artifact("editor", b"    Check the sent record before retrying.\n")
        with self.assertRaisesRegex(ValueError, "Editor text differs"):
            self.check()

    def test_stale_visible_result_overrides_claimed_freshness(self):
        self.artifact("visible_result", (self.ui + '- generic: Text changed / Scan to update\n').encode())
        with self.assertRaisesRegex(ValueError, "stale"):
            self.check()

    def test_scores_and_model_must_match_visible_controls(self):
        self.receipt.update(ai_percent=60, mixed_percent=40)
        with self.assertRaisesRegex(ValueError, "Visible AI"):
            self.check()
        self.receipt.update(ai_percent=100, mixed_percent=0, model="5.0")
        with self.assertRaisesRegex(ValueError, "Visible model"):
            self.check()

    def test_duplicate_score_controls_are_ambiguous(self):
        self.artifact("visible_result", (self.ui + '- button "AI 100%":\n').encode())
        with self.assertRaisesRegex(ValueError, "uniquely"):
            self.check()

    def test_nonfinite_and_boolean_scores_are_rejected(self):
        for value in (float("nan"), float("inf"), True, "100"):
            with self.subTest(value=value):
                self.receipt["ai_percent"] = value
                with self.assertRaisesRegex(ValueError, "Invalid confidence"):
                    self.check()

    def test_timezone_and_model_required(self):
        self.receipt["observed_at"] = "2026-09-06T09:00:00"
        with self.assertRaisesRegex(ValueError, "timezone"):
            self.check()
        self.receipt["observed_at"] += "Z"
        del self.receipt["model"]
        with self.assertRaisesRegex(ValueError, "model"):
            self.check()

    def test_absolute_paths_traversal_and_escaping_symlinks_rejected(self):
        for path in (str(self.answer), "../answer.txt"):
            with self.subTest(path=path):
                self.receipt["editor"]["path"] = path
                with self.assertRaisesRegex(ValueError, "relative"):
                    self.check()
        with tempfile.TemporaryDirectory() as other:
            outside = Path(other) / "answer.txt"
            outside.write_bytes(self.answer.read_bytes())
            (self.root / "escape.txt").symlink_to(outside)
            self.receipt["editor"]["path"] = "escape.txt"
            with self.assertRaisesRegex(ValueError, "escapes"):
                self.check()

    def test_short_text_warning_must_be_retained(self):
        self.artifact("visible_result", (self.ui + '- paragraph: This text is under 100 words\n').encode())
        with self.assertRaisesRegex(ValueError, "warning mismatch"):
            self.check()
        self.receipt["short_text_warning"] = True
        self.check()


class StudyChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "studies", self.root / "studies")
        self.path = self.root / "studies/results.json"
        self.data = json.loads(self.path.read_text())

    def check(self):
        self.path.write_text(json.dumps(self.data), encoding="utf-8")
        return study_checker.check(self.root)

    def test_all_primary_cases_and_unchanged_results_are_counted(self):
        result = self.check()
        self.assertEqual(result["scans"], 44)
        self.assertEqual((result["plain_reductions"], result["quotation_reductions"]), (0, 5))

    def test_modified_input_breaks_recorded_hash(self):
        scan = self.data["cohorts"][0]["cases"][0]["scans"]["plain"]
        (self.root / scan["input"]).write_text("Changed answer.", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.check()

    def test_removed_failure_breaks_complete_cohort(self):
        self.data["cohorts"][0]["cases"].pop()
        with self.assertRaisesRegex(ValueError, "Unlisted|Summary mismatch"):
            self.check()

    def test_quotation_body_changes_are_rejected_even_with_new_hash(self):
        scan = self.data["cohorts"][1]["cases"][0]["scans"]["quoted"]
        path = self.root / scan["input"]
        raw = path.read_bytes() + b"\nExtra detector bait."
        path.write_bytes(raw)
        scan["input_sha256"] = hashlib.sha256(raw).hexdigest()
        with self.assertRaisesRegex(ValueError, "changed the answer body"):
            self.check()

    def test_summary_cannot_claim_an_extra_reduction(self):
        self.data["expected_summary"]["plain_reductions"] = 1
        with self.assertRaisesRegex(ValueError, "Summary mismatch"):
            self.check()


if __name__ == "__main__":
    unittest.main()
