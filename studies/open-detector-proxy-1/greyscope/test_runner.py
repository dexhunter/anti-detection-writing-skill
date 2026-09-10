"""Decoder math and no-truncation boundary checks; no model inference."""

import copy
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import runner

sys.path.insert(0, str(runner.SOURCE))
from greyscope.inference import decode_logits

CALIB = json.loads((runner.MODEL / "calibration.json").read_text())


def independent_math(values):
    cumulative = []
    product = 1.0
    for value in values:
        sigmoid = 1 / (1 + math.exp(-value)) if value >= 0 else math.exp(value) / (1 + math.exp(value))
        product *= sigmoid
        cumulative.append(product)
    buckets = [1 - cumulative[0], cumulative[0] - cumulative[1],
               cumulative[1] - cumulative[2], cumulative[2]]
    score = sum(cumulative) / 3
    scaled = min(max((score - CALIB["score_min"]) / (CALIB["score_max"] - CALIB["score_min"]), 0), 1)
    return cumulative, buckets, scaled


class FakeTokenizer:
    def __init__(self, length):
        self.length = length

    def encode(self, text, *, add_special_tokens, truncation):
        assert add_special_tokens is False and truncation is False
        return list(range(self.length))


class RunnerTests(unittest.TestCase):
    def test_author_corn_math_matches_independent_formula(self):
        for logits in ([0., 0., 0.], [-1000., -1000., -1000.], [1000., 1000., 1000.],
                       [-1., 2., -3.], [1.9140625, 1.2890625, 1.6640625]):
            with self.subTest(logits=logits):
                decoded = runner.decode_details(logits, CALIB)
                cumulative, buckets, scaled = independent_math(logits)
                self.assertEqual(decoded["native"], decode_logits(logits, CALIB))
                for actual, expected in zip(decoded["corn_cumulative_probs"], cumulative):
                    self.assertAlmostEqual(actual, expected, places=14)
                for actual, expected in zip(decoded["bucket_probs_full_precision"].values(), buckets):
                    self.assertAlmostEqual(actual, expected, places=14)
                self.assertAlmostEqual(decoded["ai_involvement_full_precision"], scaled, places=14)
                self.assertAlmostEqual(sum(buckets), 1.0, places=14)
        zero = runner.decode_details([0., 0., 0.], CALIB)
        self.assertEqual(list(zero["bucket_probs_full_precision"].values()), [0.5, 0.25, 0.125, 0.125])

    def test_threshold_boundary_labels_follow_author_strict_inequalities(self):
        calib = copy.deepcopy(CALIB)
        calib.update(score_min=0., score_max=1., h_thresh=7 / 24, ai_thresh=7 / 24,
                     binary_threshold=7 / 24)
        self.assertEqual(decode_logits([0., 0., 0.], calib)["label"], "AI-edited")
        self.assertEqual(decode_logits([0., 0., 0.], calib, "binary")["label"], "human")

    def test_empty_malformed_nonfinite_logits_rejected(self):
        for values in ([], [1., 2.], [1., 2., 3., 4.], [float("nan"), 0., 0.]):
            with self.assertRaises(ValueError):
                runner.decode_details(values, CALIB)

    def test_full_coverage_at_limit_and_overflow_never_calls_model(self):
        with tempfile.TemporaryDirectory(dir=runner.ROOT) as temporary:
            root = Path(temporary)
            raw = "Résumé\r\nAll UTF-8 bytes stay saved.\n".encode()
            (root / "input.txt").write_bytes(raw)
            record = {"id": "boundary", "path": "input.txt", "sha256": runner.sha256(raw)}
            with patch.object(runner, "ROOT", root):
                for length in (2048, 2049):
                    row, ids = runner.prepare_record(record, root, FakeTokenizer(length), CALIB)
                    self.assertEqual(row["token_counts"]["full_model_prompt"], length)
                    self.assertEqual(len(ids), length)
                    self.assertEqual(row["truncation"], False)
                    self.assertEqual(Path(row["artifacts"]["raw"]["path"]).read_bytes(), raw)
                    self.assertEqual(row["status"], "ready" if length == 2048 else "unavailable")
                    if length == 2049:
                        def fail_if_called(_):
                            raise AssertionError("Overlength input reached model")
                        runner.score_one(row, ids, fail_if_called, CALIB)
                        self.assertIsNone(row["ai_involvement"])
                        self.assertEqual(row["token_counts"]["submitted"], 0)
                record["sha256"] = "invalid"
                with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
                    runner.prepare_record(record, root, FakeTokenizer(1), CALIB)

    def test_author_content_removal_is_flagged(self):
        body, steps = runner.clean_with_audit("Sure, here is an introduction.\nThe substantive text.", CALIB)
        self.assertEqual(body, "the substantive text.")
        self.assertTrue(any(s["meaningful_removal_flag"] for s in steps))

    def test_real_tokenizer_does_not_implicitly_truncate(self):
        from mlx_lm.utils import load_tokenizer
        tokenizer = load_tokenizer(runner.MODEL, tokenizer_config_extra={"local_files_only": True})
        prompt = CALIB["prompt_template"].format(text=" word" * 2200)
        ids = runner.encode_full(tokenizer, prompt)
        self.assertGreater(len(ids), 2048)
        self.assertEqual(tokenizer.decode(ids), prompt)


if __name__ == "__main__":
    runner.disable_network()
    unittest.main(verbosity=2)
