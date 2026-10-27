import json
import math
import pathlib
import unittest

from tests import end_state as es
from tests import reliability as rel

EVALSET = pathlib.Path(__file__).resolve().parent.parent / "eval_cases" / "booking.evalset.json"


def case(prefix):
    cases = json.loads(EVALSET.read_text())["eval_cases"]
    return next(c for c in cases if c["eval_id"].startswith(prefix))


def run(case_, calls):
    """Execute calls on a fresh seeded backend as an 'agent' would; return (calls, snapshot)."""
    backend = es.seeded_backend(case_)
    done = es.replay(calls, case_["session_input"]["user_id"], backend)
    return done, backend.snapshot()


class EndStateTests(unittest.TestCase):
    def setUp(self):
        self.move = case("booking-01-move")
        self.ref = es.reference_calls(self.move)

    def test_reference_passes_itself(self):
        self.assertEqual(es.grade(self.move, *run(self.move, self.ref)), [])

    def test_different_but_correct_read_order_passes(self):
        swapped = [self.ref[1], self.ref[0], *self.ref[2:]]  # search before listing bookings
        self.assertEqual(es.grade(self.move, *run(self.move, swapped)), [])

    def test_extra_read_calls_pass(self):
        extra = [self.ref[0], self.ref[0], *self.ref[1:]]
        self.assertEqual(es.grade(self.move, *run(self.move, extra)), [])

    def test_cancel_before_book_fails_on_safety_rule(self):
        reordered = [*self.ref[:2], self.ref[3], self.ref[2]]
        problems = es.grade(self.move, *run(self.move, reordered))
        self.assertEqual(problems, ["cancelled the old booking before the new one was booked"])

    def test_book_cancel_detour_fails_though_state_nets_out(self):
        detour = [*self.ref, es.Call("book_slot", {"slot_id": "S-0901"}),
                  es.Call("cancel_booking", {"booking_id": "B-003"})]
        problems = es.grade(self.move, *run(self.move, detour))
        self.assertTrue(any("effective mutating calls" in p for p in problems))

    def test_wrong_slot_fails(self):
        wrong = [*self.ref[:2], es.Call("book_slot", {"slot_id": "S-0901"}), self.ref[3]]
        self.assertTrue(es.grade(self.move, *run(self.move, wrong)))

    def test_do_nothing_fails_every_action_case_and_passes_the_rest(self):
        cases = json.loads(EVALSET.read_text())["eval_cases"]
        self.assertEqual(len(cases), 40)
        for c in cases:
            with self.subTest(c["eval_id"]):
                failed = bool(es.do_nothing_passes(c))
                self.assertEqual(failed, es.is_action_case(c))


class ReliabilityTests(unittest.TestCase):
    def test_unbiased_formula(self):
        self.assertAlmostEqual(rel.pass_hat_k(5, 4, 3), 4 / 10)  # C(4,3)/C(5,3)
        self.assertEqual(rel.pass_hat_k(5, 5, 3), 1.0)
        self.assertEqual(rel.pass_hat_k(5, 2, 3), 0.0)

    def test_refuses_k_above_trials(self):
        with self.assertRaises(ValueError):
            rel.pass_hat_k(2, 2, 3)

    def trials(self, outcomes_by_case):
        return [{"case_id": c, "trial_id": f"{c}-{i}", "outcome": o}
                for c, outs in outcomes_by_case.items() for i, o in enumerate(outs)]

    def test_short_cohort_is_not_run_not_pass(self):
        r = rel.evaluate(self.trials({"booking-01-move": ["pass"] * 2}), ["booking-01-move"], 3, 0.5)
        self.assertEqual(r["verdict"], "NOT RUN")

    def test_missing_case_is_not_run(self):
        r = rel.evaluate(self.trials({"booking-01-move": ["pass"] * 3}),
                         ["booking-01-move", "booking-02-cancel"], 3, 0.5)
        self.assertEqual(r["verdict"], "NOT RUN")

    def test_infra_error_leaves_denominator_but_is_reported(self):
        recs = self.trials({"booking-01-move": ["pass", "pass", "pass", "pass", "infra_error"]})
        r = rel.evaluate(recs, ["booking-01-move"], 3, 0.9)
        self.assertEqual((r["verdict"], r["infra_errors"]), ("PASS", 1))

    def test_one_flaky_case_lowers_the_figure(self):
        recs = self.trials({"booking-01-move": ["pass"] * 5,
                            "booking-02-cancel": ["pass", "pass", "pass", "pass", "fail"]})
        r = rel.evaluate(recs, ["booking-01-move", "booking-02-cancel"], 3, 0.8)
        self.assertTrue(math.isclose(r["pass_hat_k"], (1 + 0.4) / 2))
        self.assertEqual(r["verdict"], "FAIL")
        self.assertFalse(r["scenario_all_pass"]["cancel"])


if __name__ == "__main__":
    unittest.main()
