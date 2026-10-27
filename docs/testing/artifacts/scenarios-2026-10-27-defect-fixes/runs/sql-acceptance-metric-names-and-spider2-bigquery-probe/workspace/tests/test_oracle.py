import json
from pathlib import Path
import unittest

from eval.harness import execution_match, gate, public_response_accuracy, report
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

    def test_bird_style_ex_passes_what_the_oracle_rejects(self):
        case = CASES["q01-top-customers-q3"]
        reversed_rows = list(reversed(case["expected_rows"]))
        self.assertTrue(execution_match(reversed_rows, case["expected_rows"]))
        self.assertFalse(check(case, reversed_rows)["passed"])

    def test_gate_uses_oracle_and_needs_enough_cases(self):
        results = {c["id"]: c["expected_rows"] for c in CASES.values()}
        self.assertEqual(public_response_accuracy(results), 1.0)
        self.assertFalse(gate(results))  # only a handful of cases: not enough evidence yet

    def test_negative_control_lowers_reported_accuracy(self):
        results = {c["id"]: c["expected_rows"] for c in CASES.values()}
        for control in CONTROLS:
            results[control["case"]] = control["rows"]
        rep = report(results)
        self.assertLess(rep["public_response_accuracy"], 1.0)
        self.assertIn("q04-invoices-per-region-september", rep["failed"])


if __name__ == "__main__":
    unittest.main()
