"""Fact-preservation checks. The complaint below is synthetic."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/anti-ai-detection-writing-skill/scripts/check_facts.py"

SOURCE = (
    "The pot handle broke. The order number is NB-52044. "
    "It was bought on 18 October 2026 for £42.75, paid with Shop Pay. "
    "A refund was requested on 2 November 2026 and again on 9 November 2026. "
    "The seller rejected the request under the Consumer Rights Act. "
    "Photos can be supplied.\n"
)


def load():
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_facts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FactPreservation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = load()

    def test_identical_text_preserves_every_extracted_fact(self):
        report = self.facts.compare(SOURCE, SOURCE)
        self.assertEqual(report["result"], "facts_preserved")
        self.assertEqual(report["missing"], [])
        self.assertEqual(report["changed"], [])
        self.assertEqual(report["added"], [])
        self.assertEqual(report["source"]["order_ids"], ["NB-52044"])
        self.assertEqual(report["source"]["prices"], ["£42.75"])
        self.assertEqual(
            report["source"]["dates"],
            ["2026-10-18", "2026-11-02", "2026-11-09"],
        )
        self.assertEqual(report["source"]["names"], ["Consumer Rights Act", "Shop Pay"])
        self.assertEqual(report["source"]["numbers"], [])

    def test_folding_the_same_facts_into_another_sentence_is_preserved(self):
        candidate = (
            "The pot handle, bought on 18 October 2026 for £42.75 paid with "
            "Shop Pay under order number NB-52044, broke. A refund was "
            "requested on 2 November 2026 and again on 9 November 2026. The "
            "seller rejected the request under the Consumer Rights Act, of "
            "which photos can be supplied.\n"
        )
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(report["result"], "facts_preserved")

    def test_a_month_abbreviation_is_the_same_date(self):
        candidate = SOURCE.replace("18 October 2026", "18 Oct 2026")
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(report["result"], "facts_preserved")

    def test_a_uk_numeric_date_matches_the_written_date(self):
        candidate = SOURCE.replace("18 October 2026", "18/10/2026")
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(report["result"], "facts_preserved")

    def test_a_missing_date_is_reported(self):
        candidate = SOURCE.replace(" and again on 9 November 2026", "")
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(report["result"], "facts_differ")
        self.assertEqual(report["missing"], [{"kind": "date", "value": "2026-11-09"}])
        self.assertEqual(report["changed"], [])
        self.assertEqual(report["added"], [])

    def test_a_changed_price_is_not_reported_as_a_bare_number(self):
        candidate = SOURCE.replace("£42.75", "£42.76")
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(
            report["changed"],
            [{"kind": "price", "source": "£42.75", "candidate": "£42.76"}],
        )
        self.assertEqual(report["missing"], [])
        self.assertEqual(report["added"], [])
        self.assertEqual(report["candidate"]["numbers"], [])

    def test_a_changed_order_id_is_reported(self):
        candidate = SOURCE.replace("NB-52044", "NB-52045")
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(
            report["changed"],
            [{"kind": "order_id", "source": "NB-52044", "candidate": "NB-52045"}],
        )

    def test_a_removed_capitalised_name_is_missing(self):
        candidate = SOURCE.replace("Shop Pay", "the same checkout")
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(report["missing"], [{"kind": "name", "value": "Shop Pay"}])
        self.assertEqual(report["added"], [])

    def test_an_invented_price_is_added(self):
        candidate = SOURCE.replace("Photos can be supplied.", "A £5.00 fee applies.")
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(report["added"], [{"kind": "price", "value": "£5.00"}])
        self.assertEqual(report["missing"], [])

    def test_a_replaced_count_is_a_changed_number(self):
        source = SOURCE.replace("Photos can be supplied.", "Reply within 14 days.")
        candidate = source.replace("14 days", "21 days")
        report = self.facts.compare(source, candidate)
        self.assertEqual(
            report["changed"],
            [{"kind": "number", "source": "14", "candidate": "21"}],
        )

    def test_a_different_name_is_not_paired_with_the_old_one(self):
        candidate = SOURCE.replace("Shop Pay", "Store Credit")
        report = self.facts.compare(SOURCE, candidate)
        self.assertEqual(report["missing"], [{"kind": "name", "value": "Shop Pay"}])
        self.assertEqual(report["added"], [{"kind": "name", "value": "Store Credit"}])

    def test_a_mid_sentence_name_is_kept_and_a_different_name_is_not_a_change(self):
        source = "The pot was bought by Harper on 18 October 2026.\n"
        report = self.facts.compare(source, source)
        self.assertEqual(report["source"]["names"], ["Harper"])
        swapped = self.facts.compare(source, source.replace("Harper", "Jordan"))
        self.assertEqual(swapped["missing"], [{"kind": "name", "value": "Harper"}])
        self.assertEqual(swapped["added"], [{"kind": "name", "value": "Jordan"}])

    def test_sentence_initial_words_are_not_names(self):
        text = "Detachment of the handle took place later. Photos can be supplied.\n"
        report = self.facts.compare(text, text)
        self.assertEqual(report["source"]["names"], [])

    def test_a_price_with_commas_matches_the_same_amount(self):
        report = self.facts.compare("The total was £1,042.75.", "The total was £1042.75.")
        self.assertEqual(report["result"], "facts_preserved")
        self.assertEqual(report["source"]["prices"], ["£1042.75"])
        self.assertEqual(report["source"]["numbers"], [])

    def test_a_day_range_keeps_the_month_and_both_days(self):
        source = "Delivery is 1–2 November."
        same = self.facts.compare(source, "Delivery is 1-2 November.")
        self.assertEqual(same["result"], "facts_preserved")
        self.assertEqual(same["source"]["dates"], ["0000-11-01", "0000-11-02"])
        self.assertEqual(same["source"]["numbers"], [])
        moved = self.facts.compare(source, "Delivery is 1–2 December.")
        self.assertEqual(moved["result"], "facts_differ")
        self.assertEqual(moved["candidate"]["dates"], ["0000-12-01", "0000-12-02"])

    def test_a_dated_range_matches_the_two_written_dates(self):
        source = "Delivery is 1–2 November 2026, order #26672, £42.75."
        candidate = (
            "Delivery is 1 November 2026 and 2 November 2026, "
            "order number 26672, GBP 42.75."
        )
        report = self.facts.compare(source, candidate)
        self.assertEqual(report["result"], "facts_preserved")
        self.assertEqual(report["source"]["dates"], ["2026-11-01", "2026-11-02"])
        self.assertEqual(report["source"]["order_ids"], ["26672"])
        self.assertEqual(report["source"]["prices"], ["£42.75"])
        self.assertEqual(report["source"]["numbers"], [])

    def test_dropping_one_day_of_a_range_is_a_missing_date(self):
        report = self.facts.compare(
            "Delivery is 1 to 2 November 2026.",
            "Delivery is 2 November 2026.",
        )
        self.assertEqual(report["missing"], [{"kind": "date", "value": "2026-11-01"}])
        self.assertEqual(report["changed"], [])
        self.assertEqual(report["added"], [])

    def test_a_month_first_range_matches_the_day_first_range(self):
        report = self.facts.compare(
            "Delivery is November 1–2, 2026.",
            "Delivery is 1st–2nd November 2026.",
        )
        self.assertEqual(report["result"], "facts_preserved")
        self.assertEqual(report["source"]["dates"], ["2026-11-01", "2026-11-02"])

    def test_an_impossible_date_is_not_stored_as_a_date(self):
        report = self.facts.compare("Written on 31/02/2026.", "Written on 31/02/2026.")
        self.assertEqual(report["source"]["dates"], [])
        self.assertEqual(report["result"], "facts_preserved")
        leap = self.facts.compare("Written on 29/02/2024.", "Written on 29 February 2024.")
        self.assertEqual(leap["result"], "facts_preserved")
        self.assertEqual(leap["source"]["dates"], ["2024-02-29"])

    def test_order_hash_forms_are_the_same_order_id(self):
        report = self.facts.compare("The order #26672 arrived.", "The order#26672 arrived.")
        self.assertEqual(report["result"], "facts_preserved")
        self.assertEqual(report["source"]["order_ids"], ["26672"])
        self.assertEqual(report["source"]["numbers"], [])
        changed = self.facts.compare("The order #26672 arrived.", "The order #26673 arrived.")
        self.assertEqual(
            changed["changed"],
            [{"kind": "order_id", "source": "26672", "candidate": "26673"}],
        )

    def test_a_two_word_name_at_the_start_is_kept(self):
        report = self.facts.compare("Harper Quinn wrote on 18 October 2026.", "Harper Quinn wrote on 18 October 2026.")
        self.assertEqual(report["source"]["names"], ["Harper Quinn"])
        self.assertEqual(report["source"]["dates"], ["2026-10-18"])

    def test_an_apostrophe_in_a_mid_sentence_name_is_kept(self):
        report = self.facts.compare(
            "The pot was bought by O'Brien on 18 October 2026.",
            "The pot was bought by O'Brien on 18 October 2026.",
        )
        self.assertEqual(report["result"], "facts_preserved")
        self.assertEqual(report["source"]["names"], ["O'Brien"])

    def test_a_hyphenated_name_stays_one_name(self):
        report = self.facts.compare(
            "Mary-Jane bought the pot.",
            "Mary-Jane bought the pot.",
        )
        self.assertEqual(report["source"]["names"], ["Mary-Jane"])
        swapped = self.facts.compare(
            "Mary-Jane bought the pot.",
            "Mary Jane bought the pot.",
        )
        self.assertEqual(swapped["result"], "facts_differ")

    def test_cli_exits_zero_when_preserved_and_one_when_not(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.txt"
            same = root / "same.txt"
            changed = root / "changed.txt"
            source.write_text(SOURCE, encoding="utf-8")
            same.write_text(SOURCE, encoding="utf-8")
            changed.write_text(SOURCE.replace("£42.75", "£42.76"), encoding="utf-8")
            command = [sys.executable, str(SCRIPT)]
            ok = subprocess.run(
                command + [str(source), str(same)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertEqual(json.loads(ok.stdout)["result"], "facts_preserved")
            bad = subprocess.run(
                command + [str(source), str(changed)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(bad.returncode, 1)
            self.assertEqual(json.loads(bad.stdout)["result"], "facts_differ")
            self.assertIn("£42.76", bad.stdout)


if __name__ == "__main__":
    unittest.main()
