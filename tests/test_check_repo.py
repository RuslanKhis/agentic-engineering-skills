"""Regression checks for empty discovery and invalid evaluation evidence setup."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_repo.py"
spec = importlib.util.spec_from_file_location("check_repo", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class CheckRepoTests(unittest.TestCase):
    def test_empty_suite_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            run = subprocess.run([sys.executable, str(SCRIPT), "--suite", directory],
                                 capture_output=True, text=True, timeout=20)
            self.assertNotEqual(run.returncode, 0)

    def test_failing_suite_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "test_failure.py").write_text(
                "import unittest\nclass Failure(unittest.TestCase):\n"
                " def test_value(self): self.assertEqual(1, 2)\n")
            run = subprocess.run([sys.executable, str(SCRIPT), "--suite", directory],
                                 capture_output=True, text=True, timeout=20)
            self.assertEqual(run.returncode, 1)

    def fixture(self, root):
        (root / "skills/example").mkdir(parents=True)
        (root / "skills/example/SKILL.md").touch()
        (root / "evals").mkdir()
        self.activation = {"version": 1, "cases": [
            {"id": "positive", "skill": "example", "prompt": "Do the task",
             "should_trigger": True, "rationale": "In scope"},
            {"id": "negative", "skill": "example", "prompt": "Different task",
             "should_trigger": False, "rationale": "Outside scope"}]}
        self.scenarios = {"version": 1, "cases": [
            {"id": "scenario", "prompt": "Inspect a project", "context": "Example project",
             "available_skills": ["example"], "expected_primary": "example",
             "assertions": ["Reports the observed project configuration"]}]}
        self.save(root)

    def save(self, root):
        (root / "evals/activation.json").write_text(json.dumps(self.activation))
        (root / "evals/scenarios.json").write_text(json.dumps(self.scenarios))

    def test_positive_and_negative_cases_are_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.assertEqual(checker.validate_cases(root), [])
            self.activation["cases"].pop()
            self.save(root)
            self.assertTrue(checker.validate_cases(root))

    def test_typo_in_skill_and_string_boolean_are_rejected(self):
        for key, value in (("skill", "exmaple"), ("should_trigger", "false")):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.fixture(root)
                self.activation["cases"][0][key] = value
                self.save(root)
                self.assertTrue(checker.validate_cases(root))

    def test_duplicate_ids_and_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.scenarios["cases"][0]["id"] = "positive"
            self.save(root)
            self.assertTrue(checker.validate_cases(root))
            (root / "evals/activation.json").write_text('{"version":1,"version":2,"cases":[]}')
            self.assertTrue(checker.validate_cases(root))


if __name__ == "__main__":
    unittest.main()
