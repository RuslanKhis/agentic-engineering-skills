"""Offline tests of the case grader itself (no google-adk needed): do-nothing control and script replay."""
import json
from pathlib import Path
import unittest

from expense_agent import tools
from tests.case_checks import grade, snapshot, validate_case
from tests.fakes import FakeToolContext
from tests.fixture_db import fresh_db

CASES = json.loads((Path(__file__).resolve().parents[1] / "eval_cases" / "cases.json").read_text())["cases"]
DB_TOOLS = {"get_policy_limit", "file_expense", "get_my_profile", "update_profile", "list_my_expenses"}


def replay(case, conn):
    """Apply the case's database tool calls directly (MCP calls such as read_file have no effect on the store)."""
    ctx = FakeToolContext(user_id=case["user"])
    for step in case["script"]:
        if step.get("call") in DB_TOOLS:
            getattr(tools, step["call"])(**step["args"], tool_context=ctx)


class GraderTests(unittest.TestCase):
    def test_every_case_states_a_real_expectation(self):
        self.assertEqual(len(CASES), 30)
        for case in CASES:
            self.assertEqual(validate_case(case), [], case["id"])

    def test_do_nothing_control(self):
        """A run that changes nothing passes exactly the non-action cases and fails every action case."""
        for case in CASES:
            with self.subTest(case=case["id"]):
                conn = fresh_db()
                failures = grade(case, snapshot(conn), conn)
                if case["expected"]["filed"] is None:
                    self.assertEqual(failures, [])
                else:
                    self.assertTrue(failures, "do-nothing run passes an action case")

    def test_scripts_replay_to_the_expected_end_state(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                conn = fresh_db()
                before = snapshot(conn)
                replay(case, conn)
                failures = grade(case, before, conn)
                if case.get("known_bad_script"):
                    self.assertTrue(any("profiles" in f for f in failures), failures)
                else:
                    self.assertEqual(failures, [])

    def test_collateral_write_is_caught_even_when_the_row_is_filed(self):
        case = next(c for c in CASES if c["id"] == "c01")
        conn = fresh_db()
        before = snapshot(conn)
        replay(case, conn)
        tools.update_profile("emp-101", approver_id="emp-203", tool_context=FakeToolContext("emp-102"))
        failures = grade(case, before, conn)
        self.assertTrue(any("profiles" in f for f in failures), failures)
        self.assertTrue(any("audit_log actions" in f for f in failures), failures)

    def test_reversible_detour_is_caught_by_the_audit_actions(self):
        case = next(c for c in CASES if c["id"] == "c01")
        conn = fresh_db()
        before = snapshot(conn)
        replay(case, conn)
        for approver in ("emp-203", "emp-900"):  # change and change back: the profile diff nets to zero
            tools.update_profile("emp-101", approver_id=approver, tool_context=FakeToolContext("emp-102"))
        failures = grade(case, before, conn)
        self.assertTrue(any("audit_log actions" in f for f in failures), failures)

    def test_vacuous_expectation_is_rejected(self):
        self.assertTrue(validate_case({"expected": {"filed": {}}}))
        self.assertTrue(validate_case({"expected": {}}))


if __name__ == "__main__":
    unittest.main()
