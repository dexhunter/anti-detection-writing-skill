"""Packaged skill boundaries. These checks do not measure a detector."""

import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

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
