"""Packaged skill boundaries. These checks do not measure a detector."""

import csv
import hashlib
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/anti-ai-detection-writing-skill/SKILL.md"
YAML = ROOT / "skills/anti-ai-detection-writing-skill/agents/openai.yaml"
SCRIPT = ROOT / "skills/anti-ai-detection-writing-skill/scripts/autoresearch.py"


def load_controller():
    spec = importlib.util.spec_from_file_location("autoresearch_contract", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SkillContract(unittest.TestCase):
    def test_retailer_rules_stay_outside_the_editable_experiment_span(self):
        controller = load_controller()
        skill = SKILL.read_bytes()
        self.assertEqual(skill.count(controller.START), 1)
        self.assertEqual(skill.count(controller.END), 1)
        prefix, rest = skill.split(controller.START)
        editable, suffix = rest.split(controller.END)
        self.assertIn(b"## Private retailer and customer-service email\n", prefix)
        self.assertNotIn(b"retailer", editable.lower())
        self.assertNotIn(b"customer-service", editable.lower())
        email, _, _ = prefix.split(b"## Private retailer and customer-service email\n", 1)[1].partition(b"\n## ")
        self.assertIn(b"this section wins every conflict", email)
        self.assertIn(b"every supplied fact and qualification", email)
        self.assertIn(b"linked-evidence scope cut does not apply", email)
        self.assertIn(b"invisible characters", email)
        self.assertIn(b"claim inventory", editable)
        self.assertIn(b"Never invent", editable)
        self.assertIn(b"prose_only", suffix)
        self.assertIn(b"full_text", suffix)
        self.assertIn(b"validate_receipt.py", suffix)
        self.assertIn(b"Run a scan only when the user explicitly asks", suffix)

    def test_ordinary_email_preserves_facts_and_does_not_require_a_scan(self):
        text = SKILL.read_text(encoding="utf-8")
        _, _, rest = text.partition("## Private retailer and customer-service email\n")
        email, _, _ = rest.partition("\n## ")
        self.assertIn("this section wins every conflict", email)
        self.assertIn("every supplied fact and qualification", email)
        self.assertIn("Never drop a fact, an uncertainty, or a qualification to lower a score.", email)
        self.assertIn("including the closing and name they supplied", email)
        self.assertIn("never replace it with a different name to lower a score.", email)
        self.assertIn("It is not a way to pass a detector.", email)
        self.assertIn("The kettle sentences above limit that one email.", email)
        self.assertIn("invisible characters", email)
        self.assertIn("does not ask for a detector scan", email)
        self.assertIn("do not run a scan", email)
        self.assertNotIn("brief facts", email)
        without_prohibition = email.replace(
            "Never drop a fact, an uncertainty, or a qualification to lower a score.",
            "",
        )
        self.assertNotIn("drop a fact", without_prohibition)
        measurement = (ROOT / "skills/anti-ai-detection-writing-skill/references/measurement.md").read_text(encoding="utf-8")
        self.assertIn("The email you return still contains every fact, uncertainty, and qualification.", measurement)
        self.assertIn("Do not drop the fact.", measurement)
        self.assertIn("never replace it with a different name to lower a score.", measurement)
        self.assertIn("do not change a real sender's name", measurement)
        evidence = (ROOT / "skills/anti-ai-detection-writing-skill/references/evidence.md").read_text(encoding="utf-8")
        self.assertIn("**Hypothesis, not a result.**", evidence)
        self.assertIn("stock LLM-style persona names", evidence)
        self.assertIn("The sender's own name is a fact.", evidence)
        self.assertIn("| Dates folded into the existing first sentence | on 31 October 2026, which I ordered on 28 October 2026 | 31% |", evidence)
        self.assertIn("| Dates folded into the existing order-number sentence | via your website on 28 October 2026, and it was delivered on 31 October 2026 | 17% |", evidence)
        self.assertIn("| No name | 52% |", evidence)
        self.assertIn("| Sue Hall | 13% |", evidence)
        self.assertIn("| Helen | 100% |", evidence)
        self.assertIn("| Helen Cartwright | 100% |", evidence)
        self.assertIn("They are not a way to pass GPTZero.", evidence)
        self.assertIn("| Sue Hall kettle email, rescan of the stage 8 text | 13% | highly confident ... entirely human |", evidence)
        self.assertIn("| Return request, signed Kate Ward | 100% | Possible AI Paraphrasing |", evidence)
        self.assertIn("| Damaged lamp, signed Ann Price | 100% | Possible AI Paraphrasing |", evidence)
        self.assertIn("| Faulty blender, signed Ian Brooks | 100% | highly confident this text was AI generated |", evidence)
        self.assertIn("They are not a way to pass GPTZero.", text)
        publish = text.split("## Publish and report\n", 1)[1]
        self.assertIn("When the text is a private retailer or customer-service email", publish)
        self.assertNotIn("Return one private retailer or customer-service email to the user.", publish)
        prompt = YAML.read_text(encoding="utf-8")
        self.assertIn("every supplied fact and qualification", prompt)
        self.assertIn("Never drop a fact, an uncertainty, or a qualification to lower a score.", prompt)
        self.assertIn("keep the sign-off I supply", prompt)
        self.assertIn("Never replace a sender's name I supply to lower a score.", prompt)
        self.assertIn("If it is a private retailer or customer-service email", prompt)
        self.assertIn("only if I explicitly ask", prompt)
        self.assertNotIn("measure detector-score changes", prompt)
        self.assertIn("scripts/check_facts.py", prompt)
        self.assertIn("change as little as possible", prompt)

    def test_stage_16_rules_stay_labelled_and_do_not_promise_a_bypass(self):
        text = SKILL.read_text(encoding="utf-8")
        _, _, rest = text.partition("## Private retailer and customer-service email\n")
        email, _, _ = rest.partition("\n## ")
        self.assertIn("**[evidence + our scans]**", email)
        self.assertIn("**[our scans; mechanism hypothesis]**", email)
        self.assertIn("Do not add a new fact as a bracketed parenthetical", email)
        self.assertIn("**[hypothesis]** Prefer plain first person", email)
        self.assertIn("scripts/check_facts.py", email)
        self.assertIn("not a way to pass GPTZero", email)
        self.assertNotIn("reliably defeats", email.lower())
        measure = text.split("## Measure only when requested\n", 1)[1]
        self.assertIn("known-human control and a known-AI control", measure)
        self.assertIn("**Proposed experiments**", measure)
        self.assertIn("An unrun experiment is not a finding.", measure)
        write = text.split("## Write and review\n", 1)[1].split("## Measure only when requested\n", 1)[0]
        self.assertIn("are not detector levers", write)
        self.assertNotIn("retailer", write.lower())

    def test_short_email_probe_note_matches_the_checked_scans(self):
        skill = SKILL.read_text(encoding="utf-8")
        research_path = ROOT / "skills/anti-ai-detection-writing-skill/references/detector-research.md"
        research = research_path.read_text(encoding="utf-8")
        heading = "## Short-email edit probes checked 16 November 2026"
        self.assertEqual(research.count(heading), 1)
        slug = "short-email-edit-probes-checked-16-november-2026"
        self.assertIn(f"references/detector-research.md#{slug}", skill)
        stage = (research_path.parent / "../../../docs/reports/stage-16-pot-handle.md").resolve()
        self.assertTrue(stage.is_file())
        self.assertIn("../../../docs/reports/stage-16-pot-handle.md", research)
        section = research.split(heading, 1)[1]
        for token in (
            "100, 100, 100",
            "13→8, 14→8, 27→25",
            "13→21, 14→15, 27→34, 22→23",
            "100→100",
            "13→13, 14→14, 29→29, 100→100",
            "13→11",
            "100→8 and 100→54",
            "13→7",
            "six bases",
            "up to 8 points",
            "**[our scans]**",
            "**[vendor claim]**",
            "**[literature, not 5.0b]**",
            "designed to be indifferent to punctuation changes",
            "42–58%",
            "Nothing here is a way to pass GPTZero.",
        ):
            self.assertIn(token, section)
        self.assertNotIn("8 points or less", section)
        self.assertNotIn("exact moved wording", section)
        self.assertNotIn("one open detector", section)
        self.assertNotIn("within 30 days", section)
        self.assertIsNone(re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", section))

    def test_stages_26_31_note_stays_hedged_and_matches_the_supplied_scores(self):
        skill = SKILL.read_text(encoding="utf-8")
        write = skill.split("## Write and review\n", 1)[1].split("## Measure only when requested\n", 1)[0]
        self.assertIn("**[our scans; hedged]**", write)
        self.assertIn("does not lower the score of text that starts AI-written", write)
        self.assertIn("already human-written", write)
        self.assertIn("roughly 0.75 or higher", write)
        self.assertIn("not a tested cutoff", write)
        self.assertIn("1 − Levenshtein/max_len", write)
        self.assertIn("8/8 recorded edits", write)
        self.assertIn("eight edits, not eight drafts", write)
        self.assertIn("g1 rose to 21% (+19)", write)
        self.assertIn("0.751", write)
        self.assertIn("does not guarantee 0%", write)
        self.assertIn("a4, similarity 0.502, scored 100% AI", write)
        self.assertIn("7 drafts", write)
        self.assertIn("An eighth draft is not in those rows and is not counted", write)
        self.assertNotIn("8 drafts", write)
        self.assertIn("not tested on long documents", write)
        self.assertIn("not a way to pass GPTZero", write)
        self.assertIn("public Enron AESLC test-split emails", write)
        self.assertIn("#stages-26-31-checked-16-17-november-2026", write)
        self.assertNotIn("retailer", write.lower())
        self.assertNotIn("customer-service", write.lower())
        self.assertIn("change as little as possible", skill)
        self.assertIn("Prefer concrete nouns and verbs.", write)
        research = (ROOT / "skills/anti-ai-detection-writing-skill/references/detector-research.md").read_text(encoding="utf-8")
        self.assertEqual(research.count("## Stages 26–31 checked 16–17 November 2026"), 1)
        self.assertIn('id="stages-26-31-checked-16-17-november-2026"', research)
        section = research.split("## Stages 26–31 checked 16–17 November 2026", 1)[1]
        for token in (
            "about $0.83",
            "Qwen3-4B-Instruct-2507",
            "Llama-3.2-3B",
            "100/100/100",
            "0/6 moved",
            "moved only e04",
            "144 outputs",
            "2 of 48",
            "0/48",
            "2605.19516",
            "2608.11256",
            "0.898",
            "0.701",
            "0.904",
            "0.723",
            "0.654",
            "0.380",
            "0.535",
            "0.400",
            "0.516",
            "0.715",
            "0.502",
            "0.591",
            "0.500",
            "0.740",
            "0.751",
            "0.764",
            "0.655",
            "8/8 recorded edits still classed human",
            "eight edits, not eight drafts",
            "0–6% AI",
            "21% (+19",
            "b5, c5 0%",
            "d5 24%",
            "b4 14",
            "does not lower the score of text that starts AI-written",
            "does not guarantee 0%",
            "7 recorded drafts",
            "An eighth draft is not in those rows and is not counted",
        ):
            self.assertIn(token, section)
        self.assertNotIn("8 drafts", section)
        self.assertNotIn("b3, b4, c4, d4 human", section)
        self.assertIsNone(re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", section))
        report = (ROOT / "docs/reports/gptzero-results.md").read_text(encoding="utf-8")
        self.assertIn("177 scans, matching the CSV", report)
        self.assertIn('id="stages-26-31"', report)
        self.assertIn("Stage 27 has no CSV rows", report)
        self.assertIn("7 recorded drafts", report)
        self.assertIn("eight edits, not eight drafts", report)
        self.assertNotIn("8 drafts", report)
        csv_path = ROOT / "docs/reports/data/gptzero-scans.csv"
        rows = list(csv.reader(csv_path.read_text(encoding="utf-8").splitlines()))
        self.assertEqual(rows[0][0], "row")
        self.assertEqual(len(rows) - 1, 177)
        by_file = {row[4]: row for row in rows[1:]}
        expected = {
            "e05-qwen3-4b": "100",
            "e08-qwen3-4b": "100",
            "e03-qwen3-4b": "100",
            "e01-llama-3.2-3b": "100",
            "e02-llama-3.2-3b": "100",
            "e09-llama-3.2-3b": "100",
            "a0": "0",
            "a1": "0",
            "a2": "6",
            "b0": "0",
            "b1": "0",
            "b2": "0",
            "c0": "0",
            "c4": "0",
            "c5": "0",
            "b4": "14",
            "b5": "0",
            "a5": "100",
            "a3": "3",
            "a4": "100",
            "a5-rescan": "100",
            "d0": "0",
            "d4": "0",
            "d5": "24",
            "f0": "0",
            "f1": "0",
            "g0": "2",
            "g1": "21",
            "h0": "0",
            "h1": "0",
            "b3": "0",
        }
        self.assertEqual(len(expected), 31)
        for file_id, ai in expected.items():
            self.assertEqual(by_file[file_id][6], ai, file_id)
            self.assertEqual(by_file[file_id][7], "not logged", file_id)
            self.assertEqual(by_file[file_id][8], "not logged", file_id)
        self.assertIn("Possible AI Paraphrasing", by_file["e01-llama-3.2-3b"][5])
        self.assertIn("Possible AI Paraphrasing", by_file["e02-llama-3.2-3b"][5])
        self.assertNotIn("Possible AI Paraphrasing", by_file["e09-llama-3.2-3b"][5])
        self.assertNotIn("@", "\n".join(",".join(by_file[file_id]) for file_id in expected))

    def test_stages_32_34_note_stays_hedged_and_matches_the_supplied_scores(self):
        skill = SKILL.read_text(encoding="utf-8")
        write = skill.split("## Write and review\n", 1)[1].split("## Measure only when requested\n", 1)[0]
        for token in (
            "writer's own draft",
            "edit lightly",
            "phrasing and structure",
            "rather than polishing every sentence",
            "Heavy, uniform polishing",
            "tends to get flagged",
            "one detector version",
            "mixed scan modes as already recorded",
            "does not guarantee 0%",
            "pure Basic mode at 100, 24, and 14",
            "does not lower the score of text that starts AI-written",
            "is not a technique in this skill",
            "does not replace the light-edit note",
            "not a way to pass GPTZero",
            "#stages-32-34",
        ):
            self.assertIn(token, write, token)
        self.assertNotIn("keep at least one of that draft's own sentences word for word", write)
        self.assertNotIn("about 0.70 or higher", write)
        self.assertNotIn("8 drafts", write)
        self.assertNotIn("retailer", write.lower())
        research = (ROOT / "skills/anti-ai-detection-writing-skill/references/detector-research.md").read_text(encoding="utf-8")
        self.assertEqual(research.count("## Stages 32–34"), 1)
        self.assertIn('id="stages-32-34"', research)
        section = research.split("## Stages 32–34", 1)[1]
        for token in (
            "2% AI",
            "0.751",
            "21% AI",
            "until we have examined all",
            "without examination of all",
            "too complex and too controversial to skip the due diligence",
            "35%",
            "0.600/0.601",
            "0.616/0.609",
            "0.674/0.672",
            "a5-open 9",
            "a5-ctrl 14",
            "d5-open 0",
            "d5-ctrl 2",
            "b4-open 0",
            "b4-ctrl 0",
            "labelled human",
            "not supported",
            "−5, −2, and 0",
            "pure Basic",
            "a5 100, d5 24, b4 14",
            "6/6",
            "86–91",
            "about 0.07–0.14",
            "3 short business emails",
            "fresh or polished natural rewrites still score 100% AI",
            "Never add errors or typos",
            "one text",
            "genuinely human draft",
            "does not guarantee 0%",
            "above the 21% g1 rescan",
            "Scan mode for this stage was not in the supplied record",
            "all below 0.70",
            "not adopted as a technique",
            "17 November 2026",
            "Stage 41",
            "two of the recommender's own public posts",
            "100% AI on GPTZero Model 5.0b",
            "No letter text is recorded",
            "edit lightly",
            "phrasing and structure",
        ):
            self.assertIn(token, section, token)
        self.assertNotIn("keep at least one of the draft's own sentences word for word", section)
        self.assertNotIn("8 drafts", section)
        self.assertIsNone(re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", section))
        report = (ROOT / "docs/reports/gptzero-results.md").read_text(encoding="utf-8")
        self.assertIn("177 scans, matching the CSV", report)
        self.assertIn('id="stages-32-34"', report)
        self.assertIn("not adopted as a technique", report)
        self.assertIn("Stage 41", report)
        self.assertIn("17 November 2026", report)
        self.assertIn("two of the recommender's own public posts", report)
        self.assertIn("100% AI on GPTZero Model 5.0b", report)
        self.assertIn("No letter text is recorded", report)
        self.assertNotIn("keep at least one of that draft's own sentences word for word", report)
        self.assertNotIn("8 drafts", report)
        csv_path = ROOT / "docs/reports/data/gptzero-scans.csv"
        rows = list(csv.reader(csv_path.read_text(encoding="utf-8").splitlines()))
        self.assertEqual(len(rows) - 1, 177)
        by_file = {row[4]: row for row in rows[1:]}
        expected = {
            "g0-rescan": "2",
            "g1-rescan": "21",
            "g1-sent-open": "0",
            "g1-sent-examined": "1",
            "g1-sent-order": "14",
            "g1-sent-diligence": "35",
            "a5-open": "9",
            "a5-ctrl": "14",
            "d5-open": "0",
            "d5-ctrl": "2",
            "b4-open": "0",
            "b4-ctrl": "0",
            "a5-basic": "100",
            "d5-basic": "24",
            "b4-basic": "14",
        }
        self.assertEqual(len(expected), 15)
        for file_id, ai in expected.items():
            self.assertEqual(by_file[file_id][6], ai, file_id)
            self.assertEqual(by_file[file_id][7], "not logged", file_id)
            self.assertEqual(by_file[file_id][8], "not logged", file_id)
            self.assertEqual(by_file[file_id][10], "not logged", file_id)
            self.assertEqual(by_file[file_id][11], "not logged", file_id)
        for file_id in (
            "a5-open",
            "a5-ctrl",
            "d5-open",
            "d5-ctrl",
            "b4-open",
            "b4-ctrl",
            "g0-rescan",
            "g1-rescan",
            "g1-sent-open",
            "g1-sent-examined",
            "g1-sent-order",
            "g1-sent-diligence",
        ):
            self.assertEqual(by_file[file_id][9], "unknown", file_id)
        for file_id in ("a5-open", "a5-ctrl", "d5-open", "d5-ctrl", "b4-open", "b4-ctrl"):
            self.assertIn("Labelled human", by_file[file_id][12])
        for file_id in ("a5-basic", "d5-basic", "b4-basic"):
            self.assertEqual(by_file[file_id][9], "basic", file_id)
        self.assertIn("Scan mode was not in the supplied record", by_file["g0-rescan"][12])
        self.assertIn("0.600", by_file["a5-open"][5])
        self.assertIn("0.601", by_file["a5-ctrl"][5])
        self.assertIn("0.616", by_file["d5-open"][5])
        self.assertIn("0.609", by_file["d5-ctrl"][5])
        self.assertIn("0.674", by_file["b4-open"][5])
        self.assertIn("0.672", by_file["b4-ctrl"][5])
        self.assertIn("until we have examined all", by_file["g1-sent-examined"][5])
        self.assertIn("without examination of all", by_file["g1-sent-examined"][5])
        self.assertIn("too complex and too controversial to skip the due diligence", by_file["g1-sent-diligence"][5])
        self.assertNotIn("@", "\n".join(",".join(by_file[file_id]) for file_id in expected))

    def test_only_the_packaged_skill_is_discoverable(self):
        discovered = sorted(ROOT.rglob("SKILL.md"))
        self.assertEqual(discovered, [SKILL])
        snapshots = [
            ROOT / "studies/reader-dialogue-1/frozen/skill/SKILL.txt",
            ROOT / "studies/writing-methods-1/frozen/SKILL.txt",
        ]
        for path in snapshots:
            header = path.read_text(encoding="utf-8").split("---", 2)[1]
            self.assertIn("\nname: anti-detection-writing\n", header)

    def test_study_readme_manifests_match_the_renamed_links(self):
        local_readme = (ROOT / "studies/local-tools-1/README.md").read_bytes()
        local = json.loads((ROOT / "studies/local-tools-1/export-manifest.json").read_text())
        self.assertEqual(local["files"]["README.md"], hashlib.sha256(local_readme).hexdigest())
        proxy_readme = (ROOT / "studies/prospective-proxy-1/README.md").read_bytes()
        proxy = json.loads((ROOT / "studies/prospective-proxy-1/artifact-manifest.json").read_text())
        entry = next(item for item in proxy["files"] if item["path"] == "README.md")
        self.assertEqual(entry["sha256"], hashlib.sha256(proxy_readme).hexdigest())
        self.assertEqual(entry["bytes"], len(proxy_readme))
        methods_readme = (ROOT / "studies/writing-methods-1/README.md").read_bytes()
        methods = json.loads((ROOT / "studies/writing-methods-1/export-manifest.json").read_text())
        self.assertEqual(methods["files"]["README.md"], hashlib.sha256(methods_readme).hexdigest())
        snapshot = (ROOT / "studies/writing-methods-1/frozen/SKILL.txt").read_bytes()
        self.assertEqual(methods["files"]["frozen/SKILL.txt"], hashlib.sha256(snapshot).hexdigest())
        dialogue = json.loads((ROOT / "studies/reader-dialogue-1/export-manifest.json").read_text())
        snapshot = (ROOT / "studies/reader-dialogue-1/frozen/skill/SKILL.txt").read_bytes()
        self.assertEqual(dialogue["exact_copies"]["frozen/skill/SKILL.txt"], hashlib.sha256(snapshot).hexdigest())


if __name__ == "__main__":
    unittest.main()
