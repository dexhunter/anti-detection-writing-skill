"""Synthetic invariant checks; no development or confirmation answers are read."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from crossover import InvalidInput, digest, prepare, run


class CrossoverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.a = self.root / "a.txt"
        self.b = self.root / "b.txt"
        self.review_path = self.root / "review.json"
        self.out = self.root / "out"
        self.set_parents("Café begins.\nAlpha closes.\n", "Tea starts.\nBeta ends.\n")

    def set_parents(self, a, b):
        self.a.write_bytes(a.encode())
        self.b.write_bytes(b.encode())
        self.review = {
            "parent_a_sha256": digest(self.a.read_bytes()),
            "parent_b_sha256": digest(self.b.read_bytes()),
            "required_claim_ids": ["c1", "c2"],
            "approved_seams": [
                {
                    "a_offset": len(a.splitlines(keepends=True)[0].encode()),
                    "b_offset": len(b.splitlines(keepends=True)[0].encode()),
                    "prefix_claim_ids": ["c1"],
                    "suffix_claim_ids": ["c2"],
                    "source_review_pass": True,
                    "reason": "Synthetic review fixture, not a factual judgment.",
                }
            ],
        }

    def execute(self, max_words=140):
        self.review_path.write_text(json.dumps(self.review), encoding="utf-8")
        return run(self.a, self.b, self.review_path, self.out, max_words)

    def rejects(self, message, max_words=140):
        with self.assertRaisesRegex(InvalidInput, message):
            self.execute(max_words)
        self.assertFalse(self.out.exists())

    def test_exact_success_and_reconstructable_manifest(self):
        manifest = self.execute()
        self.assertEqual((self.out / "child-a.txt").read_bytes(), "Café begins.\nBeta ends.\n".encode())
        self.assertEqual((self.out / "child-b.txt").read_bytes(), b"Tea starts.\nAlpha closes.\n")
        parents = {"A": self.a.read_bytes(), "B": self.b.read_bytes()}
        for record in manifest["children"].values():
            child = (self.out / record["file"]).read_bytes()
            self.assertEqual(record["sha256"], digest(child))
            reconstructed = b"".join(
                parents[s["parent"]][s["source_start"] : s["source_end"]]
                for s in record["spans"]
            )
            self.assertEqual(reconstructed, child)
            for span in record["spans"]:
                self.assertEqual(
                    child[span["child_start"] : span["child_end"]],
                    parents[span["parent"]][span["source_start"] : span["source_end"]],
                )
        self.assertEqual(manifest["review"]["sha256"], digest(self.review_path.read_bytes()))
        self.assertEqual(json.loads((self.out / "manifest.json").read_text()), manifest)

    def test_wrong_parent_hash(self):
        self.review["parent_a_sha256"] = "0" * 64
        self.rejects("hash")

    def test_utf8_split(self):
        self.review["approved_seams"][0]["a_offset"] = 4  # Inside é.
        self.rejects("UTF-8")

    def test_invalid_offsets(self):
        for value in [0, len(self.a.read_bytes()), True, 1.5, -1]:
            with self.subTest(offset=value):
                self.review["approved_seams"][0]["a_offset"] = value
                self.rejects("offset")

    def test_invalid_claim_partitions(self):
        for prefix, suffix in [(["c1"], ["c1", "c2"]), (["c1"], ["c3"]),
                               ([], ["c1", "c2"]), (["c1", "c1"], ["c2"])]:
            with self.subTest(prefix=prefix, suffix=suffix):
                seam = self.review["approved_seams"][0]
                seam["prefix_claim_ids"], seam["suffix_claim_ids"] = prefix, suffix
                self.rejects("partition|nonempty|duplicate")

    def test_deterministic_tie_independent_of_review_order(self):
        self.set_parents("A one.\nA two.\nA three.\n", "B one.\nB two.\nB three.\n")
        self.review["required_claim_ids"] = ["c1", "c2", "c3"]
        first = self.review["approved_seams"][0]
        first["suffix_claim_ids"] = ["c2", "c3"]
        second = dict(first, a_offset=14, b_offset=14,
                      prefix_claim_ids=["c1", "c2"], suffix_claim_ids=["c3"])
        for seams in [[second, first], [first, second]]:
            self.review["approved_seams"] = seams
            self.review_path.write_text(json.dumps(self.review))
            _, manifest = prepare(self.a, self.b, self.review_path)
            self.assertEqual(manifest["selection_key"], [1, 7, 7])

    def test_identical_parent_noop(self):
        self.set_parents("Same start.\nSame end.\n", "Same start.\nSame end.\n")
        self.rejects("no-op")

    def test_different_parents_can_still_make_parent_noop(self):
        self.set_parents("Same start.\nFirst end.\n", "Same start.\nSecond end.\n")
        self.rejects("no-op")

    def test_overlimit_rejects_both_before_saving(self):
        self.rejects("word limit", max_words=3)

    def test_missing_final_lf(self):
        self.set_parents("First begins.\nFirst ends.\n", "Second begins.\nSecond ends.")
        self.rejects("final LF")

    def test_no_approved_seams(self):
        self.review["approved_seams"] = []
        self.rejects("No approved seams")

    def test_review_pass_must_be_boolean_true(self):
        self.review["approved_seams"][0]["source_review_pass"] = 1
        self.rejects("passing source review")

    def test_duplicate_json_key_rejected(self):
        self.review_path.write_text('{"approved_seams": [], "approved_seams": []}')
        with self.assertRaisesRegex(InvalidInput, "Duplicate JSON key"):
            run(self.a, self.b, self.review_path, self.out)
        self.assertFalse(self.out.exists())

    def test_refuses_existing_output_without_changes(self):
        self.out.mkdir()
        sentinel = self.out / "keep.txt"
        sentinel.write_bytes(b"keep")
        with self.assertRaisesRegex(InvalidInput, "refusing overwrite"):
            self.execute()
        self.assertEqual(list(self.out.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_bytes(), b"keep")

    def test_cli_default_limit(self):
        self.review_path.write_text(json.dumps(self.review))
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("crossover.py")),
             "--parent-a", str(self.a), "--parent-b", str(self.b),
             "--review", str(self.review_path), "--out", str(self.out)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.out / "manifest.json").read_text())["max_words"], 140)


if __name__ == "__main__":
    unittest.main()
