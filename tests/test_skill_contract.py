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
        self.assertIn("invisible characters", email)
        self.assertIn("does not ask for a detector scan", email)
        self.assertIn("do not run a scan", email)
        self.assertNotIn("brief facts", email)
        publish = text.split("## Publish and report\n", 1)[1]
        self.assertIn("When the text is a private retailer or customer-service email", publish)
        self.assertNotIn("Return one private retailer or customer-service email to the user.", publish)
        prompt = YAML.read_text(encoding="utf-8")
        self.assertIn("every supplied fact and qualification", prompt)
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
