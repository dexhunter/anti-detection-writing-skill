"""Synthetic UI fixtures test validation; they are never detector observations."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/anti-detection-writing/scripts/detector_receipts.py"
SPEC = importlib.util.spec_from_file_location("detector_receipts_tested", SCRIPT)
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


class DetectorReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.answer = self.root / "answer.txt"
        self.answer.write_text("Keep `api` and `ui` separate.\n\nUse the documented command.\n")
        self.receipt = {"schema_version": 1, "status": "complete", "detector": "gptzero",
                        "mode": "Basic Scan", "model": "4.9b",
                        "observed_at": datetime.now(timezone.utc).isoformat(),
                        "entry_transform": "gptzero_code_block_v1", "warnings": [],
                        "short_text_warning": False}
        self.put("answer", self.answer.read_bytes())
        self.put("submitted", self.answer.read_bytes()[:-1])
        self.put("editor_before", self.answer.read_bytes()[:-1] + b"\n\n\n")
        self.put("editor_after", self.answer.read_bytes()[:-1] + b"\n\n\n")
        self.ui = ('- heading "Basic Scan" [level=1]\n- generic: Model 4.9b\n'
                   '- generic: Text up-to-date\n- button "AI 100%":\n'
                   '- button "Mixed 0%":\n- button "Human 0%":\n')
        self.ui = '  - code: ' + json.dumps(adapter.display_text(self.answer.read_text())) + '\n' + self.ui
        self.put("visible_result", self.ui)
        # Only image format is checked here; this is explicitly a synthetic stub.
        self.put("screenshot", b"\xff\xd8\xffsynthetic-image-fixture")

    def put(self, key, value):
        raw = value.encode() if isinstance(value, str) else value
        path = self.root / (key + ".dat")
        path.write_bytes(raw)
        self.receipt[key] = {"path": path.name, "sha256": hashlib.sha256(raw).hexdigest()}

    def check(self):
        path = self.root / "receipt.json"
        path.write_text(json.dumps(self.receipt))
        return adapter.validate_scan(path, self.answer)

    def test_code_block_and_all_three_confidences(self):
        result = self.check()
        self.assertEqual((result["ai"], result["mixed"], result["human"]), (100, 0, 0))
        self.assertEqual(result["unit"], "document_confidence_percent")

    def test_changed_editor_is_not_hidden_by_rehashing(self):
        self.put("editor_before", b"Keep `apiui` separate.\n\n\n")
        with self.assertRaisesRegex(ValueError, "wrapper"):
            self.check()

    def test_changed_final_answer_invalidates_receipt(self):
        self.answer.write_text("A changed answer")
        with self.assertRaisesRegex(ValueError, "differs"):
            self.check()

    def test_stale_and_duplicate_score_controls_rejected(self):
        for suffix in ('- generic: Scan to update\n', '- button "AI 100%":\n'):
            with self.subTest(suffix=suffix):
                self.put("visible_result", self.ui + suffix)
                with self.assertRaises(ValueError):
                    self.check()

    def test_missing_human_confidence_is_not_zero(self):
        self.put("visible_result", self.ui.replace('- button "Human 0%":\n', ""))
        with self.assertRaisesRegex(ValueError, "Human confidence"):
            self.check()

    def test_other_answer_snapshot_rejected_even_with_valid_scores(self):
        self.put("visible_result", self.ui.replace("Keep `api` and `ui` separate.", "Use a different answer."))
        with self.assertRaisesRegex(ValueError, "different text"):
            self.check()

    def test_short_warning_and_declared_metrics_must_agree(self):
        self.put("visible_result", self.ui + '- paragraph: This text is under 100 words\n')
        with self.assertRaisesRegex(ValueError, "warning metadata"):
            self.check()
        self.receipt["short_text_warning"] = True
        self.receipt["metrics"] = {"ai": 0, "mixed": 0, "human": 100, "ai_assisted": None}
        with self.assertRaisesRegex(ValueError, "metrics disagree"):
            self.check()

    def test_unknown_mode_and_future_time_rejected(self):
        self.receipt["mode"] = "Advanced Scan"
        with self.assertRaises(ValueError):
            self.check()
        self.receipt["mode"] = "Basic Scan"
        self.receipt["observed_at"] = "2999-01-01T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "future"):
            self.check()

    def test_escaping_symlink_and_path_rejected(self):
        self.receipt["screenshot"]["path"] = "../outside.jpg"
        with self.assertRaisesRegex(ValueError, "inside receipt"):
            self.check()
        link = self.root / "escape"
        link.symlink_to(self.root.parent)
        self.receipt["screenshot"]["path"] = "escape/outside.jpg"
        with self.assertRaisesRegex(ValueError, "symlink escapes"):
            self.check()

    def pangram(self, assisted=False):
        self.receipt.update(detector="pangram", mode="Free text detection", model="4.0",
                            entry_transform="pangram_textarea_v1", short_text_warning=True)
        raw = self.answer.read_text()
        rendered = "\n".join(line.strip(" \t\r") for line in raw.split("\n") if line.strip(" \t\r"))
        self.put("submitted", raw)
        self.put("editor_before", raw)
        self.put("editor_after", rendered)
        self.put("rendered", rendered)
        label, native = ("AI Assisted", "AI Assisted") if assisted else ("AI Generated", "AI")
        doc = '  - generic: ' + json.dumps(adapter.display_text(rendered)) + '\n  - tablist:\n'
        ui = (f'- dialog "Text Query":\n{doc}  - tabpanel "Overview":\n'
              f'    - generic: {label}\n    - generic: 142 words scanned\n'
              '    - \'generic "Detection model: Pangram 4.0"\':\n'
              '    - generic: "100"\n    - generic: "%"\n'
              f'    - generic: of this text is {native}\n'
              '    - generic: Confidence limited — short text\n  - tabpanel "Notes"\n')
        self.put("visible_result", ui)
        self.put("details_ui", '- dialog "Text Query":\n' + doc
                 + '  - generic "Confidence level":\n    - text: medium\n')

    def test_pangram_native_metrics_are_not_gptzero_confidences(self):
        self.pangram(assisted=True)
        result = self.check()
        self.assertEqual(result["ai_assisted"], 100)
        self.assertIsNone(result["ai"])
        self.assertIsNone(result["human"])
        self.assertEqual(result["unit"], "displayed_text_proportion_percent")
        self.assertEqual(result["segment_confidence_labels"], ["medium"])

    def test_pangram_rendering_does_not_allow_token_merges(self):
        self.pangram()
        changed = "Keep `apiui` separate.\nUse the documented command."
        self.put("rendered", changed)
        self.put("editor_after", changed)
        with self.assertRaisesRegex(ValueError, "rendering changed"):
            self.check()

    def test_pangram_other_document_and_processing_rejected(self):
        self.pangram()
        path = self.root / self.receipt["visible_result"]["path"]
        ui = path.read_text()
        for changed in (ui.replace("Keep `api` and `ui` separate.", "Other answer."),
                        ui + '- generic: Processing detection\n'):
            self.put("visible_result", changed)
            with self.assertRaises(ValueError):
                self.check()


if __name__ == "__main__":
    unittest.main()
