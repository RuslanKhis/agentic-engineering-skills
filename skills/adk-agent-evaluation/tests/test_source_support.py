"""Exercise calibration scoring and deliberately inadequate judges offline."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "check_source_support.py"
spec = importlib.util.spec_from_file_location("source_support", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class SourceSupportTests(unittest.TestCase):
    def setUp(self):
        self.fixture = checker.read_json(SKILL / "assets" / "source-support-cases.json")
        self.labels = checker.read_json(SKILL / "assets" / "source-support-expectations.json")
        self.ids = {c["case_id"] for c in self.fixture["cases"]}
        self.expected = checker.index_judgments(self.labels, self.ids)

    def control(self, name):
        result = checker.weak_judgments(self.fixture, name)
        return checker.score(self.expected, checker.index_judgments(result, self.ids))

    def test_valid_identity_and_true_fact_do_not_repair_incomplete_selection(self):
        cases = {c["case_id"]: c for c in self.fixture["cases"]}
        self.assertEqual(cases["s03"]["observation"], cases["s04"]["observation"])
        result = self.control("id_only")
        self.assertIn("s03", result["false_accepts"])
        self.assertNotIn("s04", result["false_accepts"])
        self.assertIn("s15", result["false_accepts"])
        self.assertIn("s17", result["false_accepts"])

    def test_substring_judge_accepts_truncated_rule_and_rejects_valid_paraphrase(self):
        result = self.control("literal_substring")
        self.assertIn("s05", result["false_accepts"])
        self.assertIn("s02", result["false_rejects"])
        self.assertNotIn("s01", result["false_rejects"])

    def test_reject_all_cannot_pass_positive_controls(self):
        result = self.control("reject_all")
        self.assertEqual(result["false_accepts"], [])
        self.assertGreater(len(result["false_rejects"]), 0)
        self.assertLess(result["exact_matches"], len(self.ids))

    def test_all_dimensions_and_unresolved_outcomes_affect_agreement(self):
        for field, choices in checker.LABELS.items():
            with self.subTest(field=field):
                candidate = deepcopy(self.expected)
                candidate["s14"][field] = next(v for v in choices if v != candidate["s14"][field])
                result = checker.score(self.expected, candidate)
                self.assertEqual(result["exact_matches"], len(self.ids) - 1)
                self.assertEqual(result["mismatches_by_dimension"][field], ["s14"])

    def test_missing_duplicate_unknown_and_invalid_judgments_fail_closed(self):
        variants = [self.labels["judgments"][:-1], self.labels["judgments"] + [self.labels["judgments"][0]]]
        for field, value in (("case_id", "unknown"), ("support", "probably"),
                             ("applicability", None), ("rationale", "")):
            rows = deepcopy(self.labels["judgments"])
            rows[0][field] = value
            variants.append(rows)
        for rows in variants:
            with self.assertRaises(ValueError):
                checker.index_judgments({"judgments": rows}, self.ids)

    def test_cli_demo_and_independent_input_scoring(self):
        def run(*args):
            return subprocess.run([sys.executable, str(SCRIPT), *args], text=True,
                                  capture_output=True, timeout=10, check=False)
        demo = run("--demo")
        self.assertEqual(demo.returncode, 0, demo.stderr)
        self.assertEqual(json.loads(demo.stdout)["results"]["label_replay_scorer_self_check"]["exact_matches"], len(self.ids))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "judgments.json"
            path.write_text(json.dumps(self.labels))
            before = path.read_bytes()
            self.assertEqual(run("--judgments", str(path)).returncode, 0)
            self.assertEqual(path.read_bytes(), before)
            path.write_text(json.dumps(checker.weak_judgments(self.fixture, "id_only")))
            self.assertEqual(run("--judgments", str(path)).returncode, 1)
            path.write_text('{"judgments": [], "judgments": []}')
            self.assertEqual(run("--judgments", str(path)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
