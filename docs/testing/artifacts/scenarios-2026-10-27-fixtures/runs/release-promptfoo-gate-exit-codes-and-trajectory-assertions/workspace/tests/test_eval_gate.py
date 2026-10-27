import unittest

from evals.gate import BLOCK, NOT_RUN, PASS, PROVISIONAL, evaluate

EXPECT = {
    "repeat": 2,
    "baseline_measured_on": "2026-11-01",
    "cases": {
        "a": {"required_assertions": ["trajectory:tool-used"]},
        "b": {"required_assertions": ["trajectory:tool-used", "javascript"]},
    },
}


def row(case, ok=True, types=("trajectory:tool-used",), error=None):
    return {
        "testCase": {"description": case}, "success": ok, "error": error,
        "failureReason": 2 if error else (0 if ok else 1),
        "gradingResult": {"reason": "x", "componentResults": [{"assertion": {"type": t}} for t in types]},
    }


def doc(rows):
    return {"results": {"results": rows}}


def good():
    return [row("a"), row("a"), row("b", types=("trajectory:tool-used", "javascript")),
            row("b", types=("trajectory:tool-used", "javascript"))]


class GateTests(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(evaluate(doc(good()), EXPECT, 0)[0], PASS)

    def test_provisional_until_baseline_measured(self):
        self.assertEqual(evaluate(doc(good()), {**EXPECT, "baseline_measured_on": None}, 0)[0], PROVISIONAL)

    def test_failed_row_blocks_on_exit_100(self):
        rows = good()
        rows[0] = row("a", ok=False)
        self.assertEqual(evaluate(doc(rows), EXPECT, 100)[0], BLOCK)

    def test_failed_row_blocks_even_if_exit_zero(self):
        rows = good()
        rows[0] = row("a", ok=False)
        self.assertEqual(evaluate(doc(rows), EXPECT, 0)[0], BLOCK)

    def test_empty_suite_exit_zero_is_not_run(self):
        self.assertEqual(evaluate(doc([]), EXPECT, 0)[0], NOT_RUN)

    def test_harness_error_exit_1_is_not_run(self):
        self.assertEqual(evaluate(doc(good()), EXPECT, 1)[0], NOT_RUN)

    def test_error_row_is_not_run_not_block(self):
        rows = good()
        rows[0] = row("a", ok=False, error="boom")
        self.assertEqual(evaluate(doc(rows), EXPECT, 100)[0], NOT_RUN)

    def test_missing_assertion_type_is_not_run(self):
        rows = good()
        rows[2] = row("b", types=("trajectory:tool-used",))
        self.assertEqual(evaluate(doc(rows), EXPECT, 0)[0], NOT_RUN)

    def test_negated_type_counts_for_its_base_type(self):
        rows = good()
        rows[0] = row("a", types=("not-trajectory:tool-used",))
        self.assertEqual(evaluate(doc(rows), EXPECT, 0)[0], PASS)

    def test_unknown_case_and_wrong_count_are_not_run(self):
        self.assertEqual(evaluate(doc(good() + [row("c")]), EXPECT, 0)[0], NOT_RUN)

    def test_garbled_document_is_not_run(self):
        self.assertEqual(evaluate({}, EXPECT, 0)[0], NOT_RUN)


if __name__ == "__main__":
    unittest.main()
