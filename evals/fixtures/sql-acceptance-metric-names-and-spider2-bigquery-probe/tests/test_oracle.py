import json
from pathlib import Path
import unittest

from eval.harness import execution_match
from eval.oracle import check

EVAL = Path(__file__).resolve().parents[1] / "eval"
CASES = {c["id"]: c for c in json.loads((EVAL / "cases.json").read_text())}
CONTROLS = json.loads((EVAL / "negative_controls.json").read_text())


class OracleTests(unittest.TestCase):
    def test_gold_rows_pass(self):
        for case in CASES.values():
            with self.subTest(case=case["id"]):
                self.assertTrue(check(case, case["expected_rows"])["passed"])

    def test_negative_controls_fail(self):
        for control in CONTROLS:
            with self.subTest(control=control["id"]):
                self.assertFalse(check(CASES[control["case"]], control["rows"])["passed"])

    def test_ranking_order_matters(self):
        case = CASES["q01-top-customers-q3"]
        self.assertFalse(check(case, list(reversed(case["expected_rows"])))["passed"])

    def test_execution_match_is_set_equality(self):
        rows = [{"a": 1}, {"a": 2}]
        self.assertTrue(execution_match(list(reversed(rows)), rows))


if __name__ == "__main__":
    unittest.main()
