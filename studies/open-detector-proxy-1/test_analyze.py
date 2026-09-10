"""Offline archive and failure-contract checks; never load or execute a detector."""

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

TRIAL = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("proxy_analysis_under_test", TRIAL / "analyze.py")
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        names = ["inference-manifest.json", "targets.json", "protocol.md",
                 "oculus/results.json", "greyscope/results.json"]
        manifest = json.loads((TRIAL / "inference-manifest.json").read_bytes())
        names.extend(row["path"] for row in manifest["records"])
        for name in names:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(TRIAL / name, destination)

    def load(self, name):
        return json.loads((self.root / name).read_bytes())

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def test_archived_arithmetic_and_human_controls_without_commercial_scores(self):
        result = analysis.analyze(self.root)
        self.assertEqual(result["unique_inputs"], 18)
        self.assertEqual(len(result["pairs"]), 10)
        self.assertEqual(result["commercial_scans_this_study"], 0)
        self.assertEqual(len(result["historical_human_controls"]), 2)
        self.assertTrue(all(row["gptzero"] is None for row in result["historical_human_controls"]))
        expected = {
            "oculus": (2, 4, 3, 4),
            "greyscope": (3, 2, 3, 3),
        }
        for model, counts in expected.items():
            with self.subTest(model=model):
                summary = result["summaries"][model]
                self.assertEqual(summary["available_pairs"], 10)
                self.assertEqual(summary["unavailable_pairs"], 0)
                self.assertEqual(summary["historical_reduction_pairs"], 3)
                self.assertEqual(summary["historical_tie_pairs"], 7)
                self.assertEqual(tuple(summary[key] for key in (
                    "recognized_reductions", "misleading_reductions_on_ties",
                    "recognized_reductions_any_drop", "misleading_reductions_on_ties_any_drop")), counts)

    def test_missing_and_duplicate_model_records_fail(self):
        for model in ("oculus", "greyscope"):
            name = f"{model}/results.json"
            original = self.load(name)
            for mutation in ("missing", "duplicate"):
                with self.subTest(model=model, mutation=mutation):
                    report = json.loads(json.dumps(original))
                    if mutation == "missing":
                        report["records"].pop()
                    else:
                        report["records"].append(dict(report["records"][0]))
                    self.write(name, report)
                    with self.assertRaisesRegex(ValueError, "Missing, duplicate or unexpected"):
                        analysis.analyze(self.root)
                    self.write(name, original)

    def test_changed_frozen_input_fails(self):
        record = self.load("inference-manifest.json")["records"][0]
        with (self.root / record["path"]).open("ab") as stream:
            stream.write(b" Changed bytes.")
        with self.assertRaisesRegex(ValueError, "Input hash mismatch"):
            analysis.analyze(self.root)

    def test_measured_input_hash_mismatch_fails(self):
        for model in ("oculus", "greyscope"):
            name = f"{model}/results.json"
            original = self.load(name)
            report = json.loads(json.dumps(original))
            report["records"][0]["input_sha256"] = "0" * 64
            self.write(name, report)
            with self.subTest(model=model), self.assertRaisesRegex(ValueError, "Measured input mismatch"):
                analysis.analyze(self.root)
            self.write(name, original)

    def test_report_manifest_hash_mismatch_fails(self):
        for model, field in (("oculus", "input_manifest_sha256"), ("greyscope", "corpus_sha256")):
            name = f"{model}/results.json"
            original = self.load(name)
            report = json.loads(json.dumps(original))
            report[field] = "0" * 64
            self.write(name, report)
            with self.subTest(model=model), self.assertRaisesRegex(ValueError, "Inference manifest mismatch"):
                analysis.analyze(self.root)
            self.write(name, original)

    def test_failed_null_input_keeps_pair_unavailable_and_other_model_unchanged(self):
        first_pair = self.load("targets.json")["pairs"][0]
        for model, field in (("oculus", "ai_probability"), ("greyscope", "ai_involvement_full_precision")):
            name = f"{model}/results.json"
            original = self.load(name)
            report = json.loads(json.dumps(original))
            record = next(row for row in report["records"] if row["id"] == first_pair["candidate"])
            record.update(status="failed", error="Synthetic offline failure")
            record[field] = None
            self.write(name, report)
            with self.subTest(model=model):
                result = analysis.analyze(self.root)
                self.assertEqual(len(result["pairs"]), 10)
                affected = next(pair for pair in result["pairs"] if pair["id"] == first_pair["id"])
                self.assertIsNone(affected[model]["candidate"])
                self.assertIsNone(affected[model]["drop"])
                self.assertIsNone(affected[model]["meaningful_drop"])
                self.assertIsNone(affected[model]["any_drop"])
                self.assertEqual(result["summaries"][model]["available_pairs"], 9)
                self.assertEqual(result["summaries"][model]["unavailable_pairs"], 1)
                other = "greyscope" if model == "oculus" else "oculus"
                self.assertEqual(result["summaries"][other]["available_pairs"], 10)
            self.write(name, original)

    def test_failure_cannot_keep_a_numeric_score(self):
        report = self.load("oculus/results.json")
        report["records"][0]["status"] = "failed"
        self.write("oculus/results.json", report)
        with self.assertRaisesRegex(ValueError, "Failed input must retain a null score"):
            analysis.analyze(self.root)

    def test_completed_score_must_be_finite_numeric_probability(self):
        original = self.load("oculus/results.json")
        for value in (None, True, "0.5", -0.1, 1.1, float("nan"), float("inf")):
            with self.subTest(value=value):
                report = json.loads(json.dumps(original))
                report["records"][0]["ai_probability"] = value
                self.write("oculus/results.json", report)
                with self.assertRaisesRegex(ValueError, "Invalid native score"):
                    analysis.analyze(self.root)

    def test_conflicting_repeated_commercial_observation_fails(self):
        targets = self.load("targets.json")
        conflict = dict(targets["observations"][0])
        conflict.update(ai=99, mixed=1, human=0, observation_id="synthetic-conflict")
        targets["observations"].append(conflict)
        self.write("targets.json", targets)
        with self.assertRaisesRegex(ValueError, "Repeated commercial outcomes disagree"):
            analysis.analyze(self.root)


if __name__ == "__main__":
    unittest.main()
