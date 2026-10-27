"""Offline checks that keep the eval gate honest. No model calls, no ADK import."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class EvalGateContractTests(unittest.TestCase):
    def test_expectations_list_exactly_the_evalset_cases(self):
        evalset = json.loads((ROOT / "eval/support.evalset.json").read_text())
        expected = json.loads((ROOT / "eval/ci-expectations.json").read_text())
        self.assertEqual(expected["eval_set_id"], evalset["eval_set_id"])
        self.assertEqual(expected["cases"], [c["eval_id"] for c in evalset["eval_cases"]])

    def test_config_and_expectations_agree_on_criteria(self):
        config = json.loads((ROOT / "eval/test_config.json").read_text())
        expected = json.loads((ROOT / "eval/ci-expectations.json").read_text())
        self.assertEqual(set(config["criteria"]), set(expected["criteria"]))

    def test_no_model_id_is_hardcoded_outside_settings(self):
        pattern = re.compile(r"gemini-[0-9][\w.\-]*")
        for path in (ROOT / "app").rglob("*.py"):
            if path.name == "settings.py":
                continue
            self.assertIsNone(pattern.search(path.read_text()), f"hardcoded model ID in {path}")


if __name__ == "__main__":
    unittest.main()
