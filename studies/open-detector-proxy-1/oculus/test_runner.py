"""Offline Oculus runner checks adapted from repository test_local_detector.py.

Synthetic fixtures only: no real tokenizer, weights or network are used.
"""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent / "runner.py"
SPEC = importlib.util.spec_from_file_location("local_detector", SCRIPT)
detector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(detector)


class FakeBackend:
    """Two synthetic special tokens; no tokenizer or model dependency."""

    def __init__(self, model_dir=None, device="cpu"):
        self.runtime = {"device": device, "synthetic": True}
        self.encoded = []
        self.scored = []

    def encode(self, text):
        self.encoded.append(text)
        return [0] + [2] * len(text.split()) + [1]

    def score(self, ids):
        self.scored.append(ids)
        return 2.0


class LocalDetectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.inputs = self.root / "inputs.json"
        self.output = self.root / "results.json"
        self.model_dir = self.root / "model"
        self.model_dir.mkdir()
        files = {}
        for name in ("config.json", "model.safetensors", "tokenizer_config.json", "tokenizer.json"):
            data = b"Synthetic model-file fixture, never loaded."
            (self.model_dir / name).write_bytes(data)
            files[name] = detector.digest(data)
        self.model_spec = {"schema_version": 1, "model_id": detector.MODEL_ID,
                           "revision": detector.REVISION, "files": files}
        self.model_manifest = self.root / "model-manifest.json"
        self.write_model_manifest()

    def write_model_manifest(self):
        self.model_manifest.write_text(json.dumps(self.model_spec))

    def text_record(self, text="One complete answer.\n", key="answer"):
        raw = text.encode("utf-8") if isinstance(text, str) else text
        path = self.root / f"{key}.txt"
        path.write_bytes(raw)
        return {"id": key, "path": path.name, "sha256": detector.digest(raw)}

    def manifest(self, records):
        self.inputs.write_text(json.dumps({"schema_version": 1, "records": records}))
        return self.inputs

    def run_fixture(self, records, factory=FakeBackend):
        return detector.run(self.model_dir, self.manifest(records), self.output,
                            backend_factory=factory, model_manifest=self.model_manifest)

    def test_published_model_pin_and_tokenizer_contract(self):
        self.assertEqual(detector.MODEL_ID, "danibor/oculus-v2.0-multilingual")
        self.assertEqual(detector.REVISION, "e6b41a2159c78d480738317c3ea6a680073a7b32")
        self.assertEqual(detector.MAX_TOKENS, 512)
        self.model_spec["files"].pop("tokenizer.json")
        self.write_model_manifest()
        with self.assertRaisesRegex(ValueError, "lacks required files"):
            detector.verify_model(self.model_dir, self.model_manifest)

    def test_hash_drift_stops_before_tokenization(self):
        record = self.text_record()
        (self.root / record["path"]).write_text("Changed after review.")
        backend = FakeBackend()
        result = detector.score_record(record, self.root, backend)
        self.assertEqual(result["status"], "failed")
        self.assertIn("hash mismatch", result["error"])
        self.assertIsNone(result["ai_probability"])
        self.assertEqual(backend.encoded, [])
        self.assertEqual(backend.scored, [])

    def test_empty_and_invalid_utf8_are_failed_rows(self):
        for text in (" \n\t", b"\xff\xfe"):
            with self.subTest(text=text):
                backend = FakeBackend()
                result = detector.score_record(self.text_record(text), self.root, backend)
                self.assertEqual(result["status"], "failed")
                self.assertIsNone(result["raw_logit"])
                self.assertIsNone(result["ai_probability"])
                self.assertEqual(backend.encoded, [])

    def test_capacity_includes_special_tokens_and_never_truncates(self):
        for words, expected in ((510, "complete"), (511, "failed")):
            with self.subTest(words=words):
                backend = FakeBackend()
                result = detector.score_record(self.text_record("word " * words), self.root, backend)
                self.assertEqual(result["full_token_count"], words + 2)
                self.assertEqual(result["status"], expected)
                self.assertEqual(len(backend.scored), 1 if expected == "complete" else 0)
                if expected == "failed":
                    self.assertIn("no truncation", result["error"])

    def test_text_is_passed_without_normalization(self):
        text = "  Résumé\r\n\nA\tB\u2014C.\n"
        backend = FakeBackend()
        result = detector.score_record(self.text_record(text), self.root, backend)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(backend.encoded, [text])

    def test_sigmoid_direction_extremes_and_nonfinite(self):
        self.assertAlmostEqual(detector.sigmoid(0.0), 0.5)
        self.assertAlmostEqual(detector.sigmoid(2.0), 0.8807970779778823)
        self.assertAlmostEqual(detector.sigmoid(-2.0), 0.11920292202211755)
        self.assertEqual(detector.sigmoid(1000.0), 1.0)
        self.assertEqual(detector.sigmoid(-1000.0), 0.0)
        for value in (float("nan"), float("inf"), -float("inf"), True, "2"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                detector.sigmoid(value)

    def test_nonfinite_model_output_has_no_score(self):
        backend = FakeBackend()
        backend.score = lambda ids: float("nan")
        result = detector.score_record(self.text_record(), self.root, backend)
        self.assertEqual(result["status"], "failed")
        self.assertIsNone(result["raw_logit"])
        self.assertIsNone(result["ai_probability"])

    def test_invalid_manifests_rejected(self):
        record = self.text_record()
        variants = [None, {}, {"schema_version": True, "records": [record]},
                    {"schema_version": 1, "records": []},
                    {"schema_version": 1, "records": [record, record]},
                    {"schema_version": 1, "records": [dict(record, id="")]},
                    {"schema_version": 1, "records": [dict(record, sha256="wrong")]},
                    {"schema_version": 1, "records": [dict(record, path="../outside.txt")]},
                    {"schema_version": 1, "records": [dict(record, path="/absolute.txt")]}]
        for value in variants:
            with self.subTest(value=value):
                self.inputs.write_text(json.dumps(value))
                with self.assertRaises(ValueError):
                    detector.read_manifest(self.inputs)

    def test_model_file_drift_and_unverified_extra_are_rejected(self):
        detector.verify_model(self.model_dir, self.model_manifest)
        (self.model_dir / "spm.model").write_text("Unverified alternative tokenizer")
        with self.assertRaisesRegex(ValueError, "Unverified loader"):
            detector.verify_model(self.model_dir, self.model_manifest)
        (self.model_dir / "spm.model").unlink()
        (self.model_dir / "model.safetensors").write_bytes(b"Changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            detector.verify_model(self.model_dir, self.model_manifest)

    def test_model_manifest_revision_drift_rejected(self):
        self.model_spec["revision"] = "main"
        self.write_model_manifest()
        with self.assertRaisesRegex(ValueError, "pinned model"):
            detector.verify_model(self.model_dir, self.model_manifest)

    def test_verified_huggingface_blob_symlinks_are_supported(self):
        model_path = self.model_dir / "model.safetensors"
        blob = self.root / "cached-blob"
        model_path.rename(blob)
        model_path.symlink_to(blob)
        detector.verify_model(self.model_dir, self.model_manifest)
        blob.write_bytes(b"Altered cached weights")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            detector.verify_model(self.model_dir, self.model_manifest)

    def test_failed_rows_are_retained_in_order_without_fake_score(self):
        first = self.text_record(key="first")
        missing = dict(self.text_record(key="missing"), path="absent.txt")
        last = self.text_record(key="last")
        report = self.run_fixture([first, missing, last])
        self.assertEqual([row["id"] for row in report["records"]], ["first", "missing", "last"])
        self.assertEqual(report["successful_records"], 2)
        self.assertEqual(report["failed_records"], 1)
        self.assertEqual(report["scope"], "local_proxy")
        self.assertFalse(report["commercial_detector_measurement"])
        self.assertIsNone(report["records"][1]["ai_probability"])
        self.assertEqual(json.loads(self.output.read_text()), report)

    def test_existing_output_is_preserved_before_loading_backend(self):
        self.output.write_text("Previous results\n")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.run_fixture([self.text_record()])
        self.assertEqual(self.output.read_text(), "Previous results\n")

    def test_serial_scoring_repeats_exact_input_value(self):
        backend = FakeBackend()
        record = self.text_record()
        first = detector.score_record(record, self.root, backend)
        second = detector.score_record(record, self.root, backend)
        self.assertEqual(first["raw_logit"], second["raw_logit"])
        self.assertEqual(first["token_ids_sha256"], second["token_ids_sha256"])
        self.assertEqual(len(backend.scored), 2)

    def test_cli_distinguishes_row_failure_from_setup_failure(self):
        args = ["--model-dir", str(self.model_dir), "--manifest", str(self.inputs),
                "--output", str(self.output)]
        report = {"scope": "local_proxy", "successful_records": 0, "failed_records": 1}
        with patch.object(detector, "run", return_value=report), redirect_stdout(io.StringIO()):
            self.assertEqual(detector.main(args), 1)
        with patch.object(detector, "run", side_effect=ValueError("bad model")), redirect_stderr(io.StringIO()):
            self.assertEqual(detector.main(args), 2)


if __name__ == "__main__":
    unittest.main()
