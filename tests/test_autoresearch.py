"""Synthetic local controller tests; fake receipts are never detector evidence."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/anti-detection-writing/scripts/autoresearch.py"
SPEC = importlib.util.spec_from_file_location("autoresearch", SCRIPT)
controller = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(controller)


def fake_validate(receipt_path, expected_answer):
    """A fixture adapter, deliberately independent of native receipt parsing."""
    result = json.loads(receipt_path.read_text())
    if result.pop("fixture_invalid", False):
        raise ValueError("Synthetic invalid receipt")
    result.setdefault("input_sha256", controller.digest(expected_answer.read_bytes()))
    return result


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.skill = self.root / "skill"
        self.skill.mkdir()
        self.original = "# Skill\n\n## Write and review\n\nPreserve facts.\n\n## Measure only when requested\n\nMeasure honestly.\n"
        (self.skill / "SKILL.md").write_text(self.original)
        (self.skill / "reference.txt").write_text("Frozen reference")
        self.run = self.root / "run"
        self.config = dict(controller.DEFAULTS)
        self.corpus = {"schema_version": 1, "cases": [
            dict(id=f"case-{i}", split="development" if i < 2 else "holdout",
                 question=f"Question {i}", original=f"Original case {i} KEEP.",
                 claims=["Preserve facts"], protected=["KEEP"], sources=["Public supplied context"])
            for i in range(4)]}
        self.fixture = types.ModuleType("detector_receipts")
        self.fixture.validate_scan = fake_validate
        self.addCleanup(patch.stopall)
        patch.dict(sys.modules, {"detector_receipts": self.fixture}).start()
        self.serial = 0
        self.generation = self.file(dict(model="synthetic-model", settings="synthetic settings", operator_sha256="a" * 64, context="fresh"))

    def file(self, data, suffix=".json"):
        self.serial += 1
        path = self.root / f"input-{self.serial}{suffix}"
        path.write_text(json.dumps(data) if not isinstance(data, str) else data)
        return path

    def call(self, command, ok=True, **options):
        if command == "output" and "generation" not in options:
            options["generation"] = self.generation
        args = [command, "--run", str(self.run)]
        for key, value in options.items():
            args += ["--" + key.replace("_", "-"), str(value)]
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = controller.main(args)
        self.assertEqual(code, 0 if ok else 1, err.getvalue() or out.getvalue())
        return json.loads(out.getvalue()) if code == 0 else err.getvalue()

    def initialize(self):
        return self.call("init", skill=self.skill, config=self.file(self.config), cases=self.file(self.corpus))

    def proposal(self, key="edit-1", writer="improver", text=None, ok=True):
        return self.call("propose", id=key, writer=writer, hypothesis="Make the causal connection explicit.",
                         skill_file=self.file(text or self.original.replace("Preserve facts.", "Preserve facts and causal connections."), ".md"), ok=ok)

    def selected(self):
        self.initialize()
        self.proposal()
        self.call("select", ranking=self.file(dict(ranker="ranker", ranked_ids=["edit-1"], reason="Most specific hypothesis.")))

    def outputs(self, key="case-0", same=False):
        for arm in ("baseline", "candidate"):
            text = f"{'Same' if same else arm} text for {key} KEEP."
            self.call("output", case=key, arm=arm, file=self.file(text, ".txt"), writer=arm + "-writer")

    def review(self, key="case-0", **overrides):
        state = self.state()
        outputs = state["outputs"][key]
        row = dict(reviewer="judge", detector_scores_withheld=True,
                   baseline_sha256=outputs["baseline"]["sha256"], candidate_sha256=outputs["candidate"]["sha256"],
                   baseline_pass=True, candidate_pass=True, preference="candidate", reason="Facts retained and clearer.")
        row.update(overrides)
        return self.file(row)

    def quality(self, key="case-0"):
        self.outputs(key)
        self.call("review", case=key, file=self.review(key))

    def state(self):
        return json.loads((self.run / "state.json").read_text())

    def reserve(self, key="case-0", arm="baseline", detector="gptzero", words=5, ok=True):
        return self.call("reserve", case=key, arm=arm, detector=detector, words=words, ok=ok)

    def receipt(self, attempt, ai=90, **overrides):
        row = dict(detector=attempt["detector"], mode="Basic Scan", model="test-model",
                   observed_at=datetime.now(timezone.utc).isoformat(), ai=ai, mixed=0, human=100-ai,
                   ai_assisted=None, warnings=[], input_sha256=attempt["output_sha256"])
        row.update(overrides)
        return self.file(row)

    def paired(self, key="case-0", baseline=90, candidate=70):
        self.quality(key)
        for arm, ai in (("baseline", baseline), ("candidate", candidate)):
            attempt = self.reserve(key, arm)
            self.call("record", attempt=attempt["id"], receipt=self.receipt(attempt, ai=ai))

    def development(self):
        self.paired("case-0")
        self.paired("case-1")

    def test_full_bounded_experiment_resume_and_denominator(self):
        self.selected()
        self.development()
        self.assertEqual(self.call("summarize")["status"], "development_promising")
        self.paired("case-2")
        self.assertEqual(self.call("status")["status"], "development_promising")
        self.paired("case-3")
        result = self.call("summarize")
        self.assertEqual(result["status"], "candidate_supported")
        self.assertEqual(result["budget"], dict(calls_charged=8, words_charged=40))
        self.assertEqual(len(result["holdout"]["rows"]), 2)
        self.assertEqual(self.call("status"), result)

    def test_invalid_config_numeric_types(self):
        for value in (True, -1, float("nan"), float("inf"), "8"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                controller.validate_inputs(dict(self.config, max_detector_calls=value), self.corpus)
        for key, value in (("max_rounds", 2), ("min_holdout_pairs", 1), ("primary_detector", "pangram")):
            with self.subTest(key=key), self.assertRaises(ValueError):
                controller.validate_inputs(dict(self.config, **{key: value}), self.corpus)

    def test_duplicate_ids_and_cross_split_text_rejected(self):
        for field in ("id", "original"):
            corpus = json.loads(json.dumps(self.corpus))
            corpus["cases"][2][field] = corpus["cases"][0][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                controller.validate_inputs(self.config, corpus)

    def test_freezes_entire_source_tree(self):
        self.initialize()
        (self.skill / "reference.txt").write_text("Later source change")
        self.assertEqual(self.call("status")["status"], "awaiting_proposals")
        self.assertEqual((self.run / "baseline/reference.txt").read_text(), "Frozen reference")
        (self.run / "baseline/reference.txt").write_text("Tampered")
        self.assertIn("Frozen artifact changed", self.call("status", ok=False))

    def test_added_frozen_tree_file_rejected(self):
        self.initialize()
        (self.run / "baseline/added.txt").write_text("Additional guidance")
        self.assertIn("tree changed", self.call("status", ok=False))

    def test_frozen_configuration_and_state_tamper(self):
        self.initialize()
        state = self.state()
        state["config"]["min_mean_ai_reduction"] = 0
        (self.run / "state.json").write_text(json.dumps(state))
        self.assertIn("Frozen config differs", self.call("status", ok=False))

    def test_frozen_config_file_tamper(self):
        self.initialize()
        (self.run / "frozen/config.json").write_text("{}")
        self.assertIn("Frozen artifact changed", self.call("status", ok=False))

    def test_proposal_boundary_noop_and_duplicate(self):
        self.initialize()
        self.assertIn("No-op", self.proposal(text=self.original, ok=False))
        self.assertIn("Only Write", self.proposal(text=self.original.replace("Measure honestly", "Hide failures"), ok=False))
        self.proposal()
        self.assertIn("Duplicate", self.proposal(key="edit-2", ok=False))
        self.assertEqual(len(self.state()["candidates"]), 1)

    def test_independent_ranking_and_frozen_selection(self):
        self.initialize()
        self.proposal()
        ranking = dict(ranker="improver", ranked_ids=["edit-1"], reason="Synthetic ranking")
        self.assertIn("independent", self.call("select", ranking=self.file(ranking), ok=False))
        ranking["ranker"] = "ranker"
        self.call("select", ranking=self.file(ranking))
        self.call("select", ranking=self.file(ranking), ok=False)
        self.proposal(key="edit-2", ok=False)

    def test_holdout_locked_until_all_development_pairs_pass(self):
        self.selected()
        options = dict(case="case-2", arm="baseline", file=self.file("Holdout KEEP", ".txt"), writer="writer")
        self.assertIn("Holdout is locked", self.call("output", **options, ok=False))
        self.paired("case-0")
        self.call("output", **options, ok=False)
        self.paired("case-1")
        self.call("output", **options)

    def test_quality_rejection_cannot_scan_or_win(self):
        self.selected()
        self.outputs()
        self.call("review", case="case-0", file=self.review(candidate_pass=False))
        self.assertIn("Quality review", self.reserve(ok=False))
        self.quality("case-1")
        result = self.call("summarize")
        self.assertEqual(result["status"], "development_rejected")
        self.assertEqual(result["budget"]["calls_charged"], 0)

    def test_quality_reviewer_must_be_independent_and_hash_bound(self):
        self.selected()
        self.outputs()
        for overrides in (dict(reviewer="baseline-writer"), dict(reviewer="improver"),
                          dict(detector_scores_withheld=False), dict(candidate_sha256="bad"), dict(baseline_pass=1)):
            self.call("review", case="case-0", file=self.review(**overrides), ok=False)
        self.assertFalse(self.state()["reviews"])

    def test_noop_is_retained_and_never_scanned(self):
        self.selected()
        self.outputs(same=True)
        self.call("review", case="case-0", file=self.review())
        self.assertIn("No-op", self.reserve(ok=False))
        self.paired("case-1")
        result = self.call("summarize")
        self.assertEqual(result["status"], "development_no_improvement")
        self.assertEqual(result["development"]["rows"][0]["status"], "no_op")

    def test_protected_spans_and_hidden_markers_rejected(self):
        self.selected()
        for text in ("Missing required detail", "A KEEP\u200b marker"):
            self.call("output", case="case-0", arm="baseline", writer="writer", file=self.file(text, ".txt"), ok=False)
        self.call("output", case="case-0", arm="baseline", writer="writer", file=self.file("Café KEEP — text.", ".txt"))

    def test_words_conservative_charge_and_uncertain_outcome(self):
        self.selected()
        self.quality()
        self.reserve(words=4, ok=False)
        attempt = self.reserve(words=9)
        self.call("record", attempt=attempt["id"], failure="uncertain: browser lost after submit")
        self.reserve(ok=False)
        self.call("record", attempt=attempt["id"], failure="refund", ok=False)
        self.assertEqual(self.call("status")["budget"], dict(calls_charged=1, words_charged=9))

    def test_confirmation_call_reserve_is_not_spendable_on_development(self):
        self.selected()
        self.development()
        self.assertIn("confirmation reserve", self.reserve(detector="pangram", ok=False))
        self.assertEqual(self.call("status")["budget"]["calls_charged"], 4)

    def test_first_scan_rejected_when_word_budget_cannot_cover_pair(self):
        self.config["max_detector_words"] = 8
        self.config["reserved_confirmation_words"] = 0
        self.selected()
        self.quality()
        self.assertIn("Word budget", self.reserve(ok=False))
        self.assertEqual(self.call("status")["budget"], dict(calls_charged=0, words_charged=0))

    def test_ui_cost_mismatch_cannot_dispatch_partial_pair(self):
        self.config["max_detector_words"] = 511
        self.selected()
        self.quality()
        first = self.reserve(words=6)
        self.assertFalse(first["dispatch_ready"])
        self.assertIn("confirmation word reserve", self.reserve(arm="candidate", words=6, ok=False))
        result = self.call("status")
        self.assertEqual(result["budget"], dict(calls_charged=1, words_charged=6))
        self.assertFalse(any(job["role"] == "detector_worker" for job in result["next"]))
        self.assertIn(dict(role="coordinator", action="reserve complete pair", case="case-0",
                           detector="gptzero", reserved_arms=["baseline"]), result["next"])

    def test_atomic_pair_rejects_actual_ui_cost_without_partial_charge(self):
        self.config["max_detector_words"] = 511
        self.selected()
        self.quality()
        error = self.call("reserve-pair", case="case-0", detector="gptzero",
                          baseline_words=6, candidate_words=6, ok=False)
        self.assertIn("confirmation word reserve", error)
        result = self.call("status")
        self.assertEqual(result["budget"], dict(calls_charged=0, words_charged=0))
        self.assertEqual(result["attempts"], {})
        self.assertFalse(any(job["role"] == "detector_worker" for job in result["next"]))
        self.assertFalse((self.run / "attempts").exists())

    def test_atomic_pair_dispatches_both_after_exact_cost_reservation(self):
        self.config["max_detector_words"] = 512
        self.selected()
        self.quality()
        result = self.call("reserve-pair", case="case-0", detector="gptzero",
                           baseline_words=6, candidate_words=6)
        self.assertEqual(len(result["attempts"]), 2)
        self.assertTrue(all(row["dispatch_ready"] for row in result["attempts"]))
        status = self.call("status")
        self.assertEqual(status["budget"], dict(calls_charged=2, words_charged=12))
        self.assertEqual({job["attempt"] for job in status["next"] if job["role"] == "detector_worker"},
                         {row["id"] for row in result["attempts"]})
        self.call("record", attempt=result["attempts"][0]["id"], failure="uncertain: synthetic timeout")
        self.assertEqual(self.call("status")["budget"], dict(calls_charged=2, words_charged=12))

    def test_atomic_pair_failure_leaves_only_outcome_reconciliation(self):
        self.selected()
        self.quality()
        pair = self.call("reserve-pair", case="case-0", detector="gptzero",
                         baseline_words=6, candidate_words=6)["attempts"]
        self.call("record", attempt=pair[0]["id"], failure="uncertain: synthetic timeout")
        status = self.call("status")
        self.assertEqual(status["next"], [dict(role="detector_worker", attempt=pair[1]["id"],
                                               action="record existing outcome only")])
        self.assertIn("Primary detector failure", self.call("reserve-pair", case="case-1", detector="gptzero",
                                                           baseline_words=6, candidate_words=6, ok=False))
        self.assertIn("Primary detector failure", self.call("output", case="case-1", arm="baseline",
                                                           writer="new-writer", file=self.file("New KEEP answer", ".txt"), ok=False))
        self.call("record", attempt=pair[1]["id"], failure="not submitted after first-arm failure")
        final = self.call("status")
        self.assertEqual(final["next"], [])
        self.assertEqual(final["budget"], dict(calls_charged=2, words_charged=12))
        self.assertIsNotNone(final["completed_at"])
        self.assertEqual(final["development"]["rows"][1]["status"], "awaiting_outputs_or_review")
        with patch.object(controller, "datetime") as mocked:
            mocked.now.return_value = datetime.now(timezone.utc) + timedelta(hours=1)
            mocked.fromisoformat.side_effect = datetime.fromisoformat
            self.assertEqual(self.call("status"), final)

    def test_failed_legacy_reservation_cannot_unlock_other_arm(self):
        self.selected()
        self.quality()
        first = self.reserve(words=6)
        self.call("record", attempt=first["id"], receipt=self.receipt(first, fixture_invalid=True))
        self.assertEqual(self.call("status")["next"], [])
        self.assertIn("Run completed", self.reserve(arm="candidate", words=6, ok=False))
        self.assertEqual(self.call("status")["budget"], dict(calls_charged=1, words_charged=6))

    def test_failed_pair_reconciles_after_deadline_without_losing_failure(self):
        self.selected()
        self.quality()
        pair = self.call("reserve-pair", case="case-0", detector="gptzero",
                         baseline_words=6, candidate_words=6)["attempts"]
        self.call("record", attempt=pair[0]["id"], failure="uncertain: synthetic timeout")
        with patch.object(controller, "expired", return_value=True):
            self.assertEqual(self.call("status")["status"], "development_rejected")
            self.call("record", attempt=pair[1]["id"], failure="not submitted after first-arm failure")
            final = self.call("status")
            self.assertEqual(final["status"], "development_rejected")
            self.assertIsNotNone(final["completed_at"])
            self.assertEqual(final["next"], [])
        self.assertEqual(self.call("status"), final)

    def test_invalid_receipt_charge_is_terminal(self):
        self.selected()
        self.quality()
        attempt = self.reserve()
        result = self.call("record", attempt=attempt["id"], receipt=self.receipt(attempt, fixture_invalid=True))
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(self.call("status")["budget"]["calls_charged"], 1)
        self.call("record", attempt=attempt["id"], receipt=self.receipt(attempt), ok=False)

    def test_wrong_output_hash_and_old_receipts_fail(self):
        self.selected()
        self.quality()
        attempts = {arm: self.reserve(arm=arm) for arm in ("baseline", "candidate")}
        for arm, override in (("baseline", dict(input_sha256="wrong")),
                              ("candidate", dict(observed_at=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat()))):
            attempt = attempts[arm]
            result = self.call("record", attempt=attempt["id"], receipt=self.receipt(attempt, **override))
            self.assertEqual(result["status"], "invalid")

    def test_mismatched_models_cannot_pair(self):
        self.selected()
        self.quality()
        first = self.reserve()
        self.call("record", attempt=first["id"], receipt=self.receipt(first))
        second = self.reserve(arm="candidate")
        result = self.call("record", attempt=second["id"], receipt=self.receipt(second, model="different"))
        self.assertEqual(result["status"], "invalid")
        self.assertIn("different mode or model", result["failure"])

    def test_pangram_metrics_remain_separate(self):
        self.config["max_detector_calls"] = 10
        self.selected()
        self.quality()
        attempt = self.reserve(detector="pangram")
        self.call("record", attempt=attempt["id"], receipt=self.receipt(attempt, ai=0, ai_assisted=20, model="4.0", mode="Pangram"))
        summary = self.call("summarize")
        self.assertEqual(summary["development"]["rows"][0]["status"], "awaiting_scans")
        self.assertEqual(summary["attempts"][attempt["id"]]["result"]["ai_assisted"], 20)

    def test_mean_improvement_does_not_hide_case_regression(self):
        self.selected()
        self.paired("case-0", baseline=90, candidate=10)
        self.paired("case-1", baseline=90, candidate=91)
        self.assertEqual(self.call("summarize")["status"], "development_no_improvement")

    def test_non_improvement_and_incomplete_never_promote(self):
        self.selected()
        self.paired("case-0", baseline=90, candidate=90)
        self.assertEqual(self.call("summarize")["status"], "development_incomplete")
        self.paired("case-1", baseline=90, candidate=90)
        self.assertEqual(self.call("summarize")["status"], "development_no_improvement")

    def test_unsafe_paths_and_symlinks(self):
        self.initialize()
        self.proposal(key="../escape", ok=False)
        link = self.root / "linked.md"
        link.symlink_to(self.skill / "SKILL.md")
        self.call("propose", id="safe", writer="writer", hypothesis="Test", skill_file=link, ok=False)
        with self.assertRaises(ValueError):
            controller.clean_path(self.root / "x/../run")

    def test_unsafe_receipt_artifact_cannot_escape(self):
        self.selected()
        self.quality()
        attempt = self.reserve()
        result = self.call("record", attempt=attempt["id"], receipt=self.receipt(attempt, answer=dict(path="../secret", sha256="x")))
        self.assertEqual(result["status"], "invalid")
        self.assertIn("Unsafe receipt", result["failure"])

    def test_terminal_outputs_and_reviews_cannot_be_overwritten(self):
        self.selected()
        self.quality()
        self.call("output", case="case-0", arm="baseline", writer="writer", file=self.file("New KEEP", ".txt"), ok=False)
        self.call("review", case="case-0", file=self.review(), ok=False)

    def test_committed_journal_recovers_after_interrupted_rename(self):
        self.selected()
        real_replace = controller.os.replace
        tripped = False

        def interrupted(source, destination):
            nonlocal tripped
            if "outputs" in Path(destination).parts and not tripped:
                tripped = True
                raise OSError("Synthetic interrupted commit")
            return real_replace(source, destination)

        with patch.object(controller.os, "replace", side_effect=interrupted):
            self.call("output", case="case-0", arm="baseline", writer="writer", file=self.file("Durable output KEEP", ".txt"), ok=False)
        self.call("status")
        self.assertIn("baseline", self.state()["outputs"]["case-0"])
        self.assertFalse((self.run / ".pending").exists())

    def test_uncommitted_staging_is_discarded_on_resume(self):
        self.selected()
        output = self.file("Retried KEEP output", ".txt")
        with patch.object(controller, "save_state", side_effect=OSError("Synthetic pre-journal interruption")):
            self.call("output", case="case-0", arm="baseline", writer="writer", file=output, ok=False)
        self.call("output", case="case-0", arm="baseline", writer="writer", file=output)
        self.assertFalse((self.run / ".pending").exists())

    def test_completed_decision_remains_stable_after_deadline(self):
        self.selected()
        self.development()
        self.paired("case-2")
        self.paired("case-3")
        before = self.call("status")
        self.assertEqual(before["status"], "candidate_supported")
        self.assertIsNotNone(before["completed_at"])
        completed = datetime.fromisoformat(before["completed_at"])
        start = datetime.fromisoformat(self.state()["started_at"])
        self.assertLess((completed - start).total_seconds(), self.config["max_elapsed_seconds"])
        with patch.object(controller, "datetime") as mocked:
            mocked.now.return_value = start + timedelta(hours=1)
            mocked.fromisoformat.side_effect = datetime.fromisoformat
            after = self.call("status")
            self.assertEqual(after, before)
            self.assertIn("Run completed", self.reserve(detector="pangram", ok=False))
        self.assertEqual(json.loads((self.run / "completion.json").read_text())["completed_at"], before["completed_at"])

    def test_completed_negative_decision_stays_final_after_deadline(self):
        self.selected()
        self.paired("case-0", baseline=100, candidate=100)
        self.assertIsNone(self.call("status")["completed_at"])
        self.paired("case-1", baseline=100, candidate=100)
        before = self.call("status")
        self.assertEqual(before["status"], "development_no_improvement")
        self.assertIsNotNone(before["completed_at"])
        self.assertIn("Run completed", self.proposal(key="another", ok=False))
        with patch.object(controller, "datetime") as mocked:
            mocked.now.return_value = datetime.now(timezone.utc) + timedelta(hours=1)
            mocked.fromisoformat.side_effect = datetime.fromisoformat
            self.assertEqual(self.call("status"), before)

    def test_complete_quality_rejection_stops_before_any_scan(self):
        self.selected()
        self.quality("case-0")
        self.outputs("case-1")
        self.call("review", case="case-1", file=self.review("case-1", preference="baseline"))
        result = self.call("status")
        self.assertEqual(result["status"], "development_rejected")
        self.assertIsNotNone(result["completed_at"])
        self.assertEqual(result["budget"], dict(calls_charged=0, words_charged=0))
        self.assertEqual(result["next"], [])
        self.assertEqual([r["status"] for r in result["development"]["rows"]],
                         ["not_scanned_candidate_rejected", "quality_rejected"])
        self.assertIsNone(result["development"]["mean_ai_reduction"])
        self.assertIn("Run completed", self.reserve(ok=False))

    def test_rejection_waits_for_remaining_cases_and_reserved_attempts(self):
        self.selected()
        self.quality("case-1")
        first = self.reserve("case-1")
        second = self.reserve("case-1", arm="candidate")
        self.outputs()
        self.call("review", case="case-0", file=self.review(candidate_pass=False))
        pending = self.call("status")
        self.assertIsNone(pending["completed_at"])
        self.assertEqual({job["attempt"] for job in pending["next"]}, {first["id"], second["id"]})
        self.assertTrue(all(job.get("action") == "record existing outcome only" for job in pending["next"]))
        self.call("record", attempt=first["id"], failure="failed: synthetic detector error")
        self.assertIsNone(self.call("status")["completed_at"])
        self.call("record", attempt=second["id"], failure="uncertain: synthetic browser outcome")
        result = self.call("status")
        self.assertEqual(result["status"], "development_rejected")
        self.assertIsNotNone(result["completed_at"])
        self.assertIn("Run completed", self.reserve("case-1", detector="pangram", ok=False))

    def test_quality_rejection_preserves_partial_reservation_reconciliation(self):
        self.selected()
        self.quality("case-1")
        first = self.reserve("case-1")
        self.outputs()
        self.call("review", case="case-0", file=self.review(candidate_pass=False))
        pending = self.call("status")["next"]
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["attempt"], first["id"])
        self.assertEqual(pending[0]["action"], "record existing outcome only")
        self.call("record", attempt=first["id"], failure="not submitted after quality rejection")
        self.assertIsNotNone(self.call("status")["completed_at"])
        self.assertEqual(self.call("status")["next"], [])

    def test_first_scan_preflight_preserves_confirmation_word_reserve(self):
        self.config["max_detector_words"] = 508
        self.selected()
        self.quality()
        self.assertIn("confirmation word reserve", self.reserve(ok=False))
        self.assertEqual(self.call("status")["budget"]["calls_charged"], 0)

    def test_first_scan_preflight_preserves_confirmation_call_reserve(self):
        self.config["max_detector_calls"] = 9
        self.selected()
        self.development()
        self.assertIn("confirmation reserve", self.reserve(detector="pangram", ok=False))
        self.assertEqual(self.call("status")["budget"]["calls_charged"], 4)

    def test_native_receipt_import_preserves_evidence_and_exact_text(self):
        self.selected()
        self.quality()
        attempt = self.reserve()
        text = (self.run / self.state()["outputs"]["case-0"]["baseline"]["path"]).read_bytes()
        ui = ("  - paragraph: " + text.decode() + '\n- heading "Basic Scan" [level=1]\n'
              '- generic: Text up-to-date\n- generic: Model test-model\n'
              '- button "AI 80%"\n- button "Mixed 10%"\n- button "Human 10%"\n')
        receipt = dict(schema_version=1, detector="gptzero", mode="Basic Scan", model="test-model",
                       status="complete", observed_at=datetime.now(timezone.utc).isoformat(),
                       entry_transform="verbatim_v1", short_text_warning=False, warnings=[])
        for key, data in dict(answer=text, submitted=text, editor_before=text, editor_after=text,
                              visible_result=ui.encode(), screenshot=b"\xff\xd8\xffsynthetic fixture").items():
            path = self.root / ("native-" + key)
            path.write_bytes(data)
            receipt[key] = dict(path=path.name, sha256=controller.digest(data))
        spec = importlib.util.spec_from_file_location("detector_receipts", SCRIPT.with_name("detector_receipts.py"))
        native = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(native)
        with patch.dict(sys.modules, {"detector_receipts": native}):
            result = self.call("record", attempt=attempt["id"], receipt=self.file(receipt))
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["result"]["ai"], 80)
        evidence = self.run / "attempts" / attempt["id"] / "evidence" / "native-answer"
        self.assertEqual(evidence.read_bytes(), text)
        evidence.write_bytes(b"Changed after import")
        self.assertIn("Frozen artifact changed", self.call("status", ok=False))

    def test_generation_provenance_must_match(self):
        self.selected()
        self.call("output", case="case-0", arm="baseline", writer="writer-1", file=self.file("Original KEEP text", ".txt"))
        metadata = json.loads(self.generation.read_text())
        for override in (dict(model="other-model"), dict(settings="changed"), dict(context="reused")):
            self.call("output", case="case-0", arm="candidate", writer="writer-2", file=self.file("Improved KEEP text", ".txt"),
                      generation=self.file(dict(metadata, **override)), ok=False)
        self.call("output", case="case-0", arm="candidate", writer="writer-1", file=self.file("Improved KEEP text", ".txt"), ok=False)

    def test_confirmation_word_reserve_is_not_spendable(self):
        self.config["max_detector_words"] = 504
        self.selected()
        self.quality()
        self.assertIn("confirmation word reserve", self.reserve(ok=False))
        self.assertEqual(self.call("status")["budget"]["calls_charged"], 0)

    def test_deadline_blocks_new_work_but_records_existing_outcome(self):
        self.selected()
        self.quality()
        attempt = self.reserve()
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        with patch.object(controller, "datetime") as mocked:
            mocked.now.return_value = future
            mocked.fromisoformat.side_effect = datetime.fromisoformat
            self.assertIn("elapsed-time", self.reserve(arm="candidate", ok=False))
            self.call("record", attempt=attempt["id"], failure="uncertain: timeout")
            summary = self.call("status")
            self.assertEqual(summary["status"], "development_rejected")
            self.assertIsNotNone(summary["completed_at"])
            self.assertEqual(summary["budget"]["calls_charged"], 1)

    def test_mutable_quality_metadata_cannot_override_frozen_review(self):
        self.selected()
        self.outputs()
        self.call("review", case="case-0", file=self.review(candidate_pass=False))
        state = self.state()
        state["reviews"]["case-0"]["candidate_pass"] = True
        (self.run / "state.json").write_text(json.dumps(state))
        self.assertIn("Frozen review metadata", self.call("status", ok=False))

    def test_concurrent_reservations_charge_once(self):
        self.selected()
        self.quality()
        args = [sys.executable, str(SCRIPT), "reserve", "--run", str(self.run),
                "--case", "case-0", "--arm", "baseline", "--detector", "gptzero", "--words", "5"]
        workers = [subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for worker in workers:
            worker.communicate(timeout=15)
        self.assertEqual(sorted(w.returncode for w in workers), [0, 1])
        self.assertEqual(self.call("status")["budget"]["calls_charged"], 1)

    def test_concurrent_pair_reservations_commit_once(self):
        self.selected()
        self.quality()
        args = [sys.executable, str(SCRIPT), "reserve-pair", "--run", str(self.run),
                "--case", "case-0", "--detector", "gptzero", "--baseline-words", "6", "--candidate-words", "6"]
        workers = [subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for worker in workers:
            worker.communicate(timeout=15)
        self.assertEqual(sorted(w.returncode for w in workers), [0, 1])
        status = self.call("status")
        self.assertEqual(status["budget"], dict(calls_charged=2, words_charged=12))
        self.assertEqual(len([job for job in status["next"] if job["role"] == "detector_worker"]), 2)


if __name__ == "__main__":
    unittest.main()
