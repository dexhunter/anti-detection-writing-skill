"""Packaged skill boundaries. These checks do not measure a detector."""

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/anti-detection-writing/SKILL.md"
YAML = ROOT / "skills/anti-detection-writing/agents/openai.yaml"
SCRIPT = ROOT / "skills/anti-detection-writing/scripts/autoresearch.py"


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
        self.assertNotIn(b"Private retailer", editable)
        self.assertIn(b"every supplied fact and qualification", prefix)
        self.assertIn(b"linked-evidence scope cut does not apply", prefix)
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
        self.assertIn("every supplied fact and qualification", email)
        self.assertIn("does not ask for a detector scan", email)
        self.assertIn("That request does not run a scan.", email)
        self.assertNotIn("brief facts", email)
        prompt = YAML.read_text(encoding="utf-8")
        self.assertIn("every supplied fact and qualification", prompt)
        self.assertIn("only if I explicitly ask", prompt)
        self.assertNotIn("measure detector-score changes", prompt)


if __name__ == "__main__":
    unittest.main()
