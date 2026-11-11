"""Offline proxy checks. Fixtures are not detector results and do not load a model."""

import importlib.util
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/anti-ai-detection-writing-skill/scripts/proxy_detector.py"
SPEC = importlib.util.spec_from_file_location("proxy_detector", SCRIPT)
proxy = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(proxy)


class ProxyMathTests(unittest.TestCase):
    def test_spearman_direction_and_ties(self):
        self.assertAlmostEqual(proxy.spearman([1, 2, 3, 4], [1, 2, 3, 4]), 1.0)
        self.assertAlmostEqual(proxy.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertIsNone(proxy.spearman([1, 1, 1, 1], [1, 2, 3, 4]))
        self.assertIsNone(proxy.spearman([1, 2], [1, 2]))
        tied = proxy.spearman([1, 2, 2, 4], [1, 3, 3, 8])
        self.assertAlmostEqual(tied, 1.0)

    def test_binoculars_is_the_published_ratio(self):
        self.assertAlmostEqual(proxy.binoculars_score(2.0, 4.0), 0.5)
        for log_perplexity, cross in ((0.0, 1.0), (-1.0, 1.0), (1.0, 0.0), (float("nan"), 1.0)):
            with self.subTest(log_perplexity=log_perplexity, cross=cross), self.assertRaises(ValueError):
                proxy.binoculars_score(log_perplexity, cross)

    def test_curvature_matches_a_hand_calculation(self):
        probability = 0.8
        observed = math.log(probability)
        other = 0.2
        mean = probability * math.log(probability) + other * math.log(other)
        variance = (probability * (math.log(probability) - mean) ** 2
                    + other * (math.log(other) - mean) ** 2)
        expected = (observed - mean) / math.sqrt(variance)
        self.assertAlmostEqual(proxy.curvature_from_rows([(observed, [probability, other])]), expected)
        self.assertGreater(expected, 0)
        self.assertIsNone(proxy.curvature_from_rows([(0.0, [1.0])]))

    def test_cross_entropy_of_a_certain_observer(self):
        self.assertAlmostEqual(proxy.mean_cross_entropy([[1.0, 0.0]], [[0.5, 0.5]]), math.log(2))

    def test_pair_movement_uses_the_archived_five_point_bar(self):
        self.assertEqual(proxy.movement(100, 93, proxy.GPTZERO_REDUCTION_POINTS), "lower")
        self.assertEqual(proxy.movement(100, 96, proxy.GPTZERO_REDUCTION_POINTS), "flat")
        self.assertEqual(proxy.movement(100, 100, 0), "flat")
        self.assertEqual(proxy.movement(0, 100, 5), "higher")


class ProxyCorpusTests(unittest.TestCase):
    def test_archived_gptzero_corpus_is_hash_exact_and_saturated(self):
        corpus = proxy.load_gptzero_corpus(ROOT)
        records = corpus["records"]
        self.assertEqual(len(records), 108)
        self.assertEqual(corpus["conflicts"], [])
        self.assertEqual({record["model"] for record in records}, {"4.9b"})
        self.assertTrue(all(record["modes"] == ["Basic Scan"] for record in records))
        below = [record for record in records if record["ai"] < 100]
        self.assertEqual(len(below), 11)
        self.assertEqual(sum(record["whitespace_words"] < 100 and record["ai"] < 100 for record in records), 0)
        for record in records:
            raw = (ROOT / record["path"]).read_bytes()
            self.assertEqual(proxy.digest(raw), record["sha256"])
            self.assertEqual(proxy.digest(raw.decode("utf-8").rstrip().encode("utf-8")), record["stripped_sha256"])
            total = record["ai"] + record["mixed"] + record["human"]
            self.assertLessEqual(abs(total - 100), 1)
        pairs = proxy.load_archived_pairs(ROOT, records)
        self.assertEqual(len(pairs), 10)
        business = next(pair for pair in pairs if pair["id"] == "pair-07")
        self.assertEqual((business["baseline_ai"], business["candidate_ai"]), (100, 0))
        python_copies = [record for record in records if record["path"].endswith("python-baseline.txt")
                         or record["path"].endswith("python-baseline-effective.txt")]
        self.assertEqual(len(python_copies), 2)
        self.assertEqual({record["ai"] for record in python_copies}, {91})
        self.assertEqual(len({record["stripped_sha256"] for record in python_copies}), 1)
        self.assertEqual(len(proxy.human_control_records(ROOT)), 2)

    def test_summary_separates_a_useful_proxy_from_a_flat_one(self):
        records = [
            {"sha256": "a", "stripped_sha256": "a", "ai": 100, "whitespace_words": 120},
            {"sha256": "b", "stripped_sha256": "b", "ai": 100, "whitespace_words": 140},
            {"sha256": "c", "stripped_sha256": "c", "ai": 0, "whitespace_words": 150},
            {"sha256": "d", "stripped_sha256": "a", "ai": 100, "whitespace_words": 120},
        ]
        pairs = [{"id": "drop", "baseline_sha256": "a", "candidate_sha256": "c",
                  "baseline_ai": 100, "candidate_ai": 0},
                 {"id": "tie", "baseline_sha256": "a", "candidate_sha256": "b",
                  "baseline_ai": 100, "candidate_ai": 100}]
        useful = proxy.summarize_metric(records, {"a": 0.9, "b": 0.95, "c": 0.1, "d": 0.4}, pairs, True)
        self.assertEqual(useful["n"], 3)
        self.assertEqual(useful["archived_pairs_at_5_points"]["reductions_recognized"], 1)
        self.assertEqual(useful["archived_pairs_at_5_points"]["ties_with_a_proxy_decrease"], 0)
        self.assertEqual(useful["ceiling_median_separation"], 1.0)
        flat = proxy.summarize_metric(records, {"a": 0.2, "b": 0.05, "c": 0.8}, pairs, True)
        self.assertEqual(flat["archived_pairs_at_5_points"]["reductions_recognized"], 0)
        self.assertEqual(flat["archived_pairs_at_5_points"]["ties_with_a_proxy_decrease"], 1)


class ProxyCommandTests(unittest.TestCase):
    def test_corpus_command_writes_the_same_record_count(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "corpus.json"
            self.assertEqual(proxy.main(["corpus", "--root", str(ROOT), "--output", str(output)]), 0)
            payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(len(payload["records"]), 108)
        self.assertEqual(len(payload["pairs"]), 10)
        self.assertEqual(payload["service"], "GPTZero")


if __name__ == "__main__":
    unittest.main()
