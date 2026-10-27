"""The grader itself, without ADK: its references pass, and do-nothing and collateral-damage runs fail."""
import json
from pathlib import Path
import unittest

from tests.case_checks import grade, reference_calls, run_db_calls, snapshot, validate_case
from tests.fixture_db import fresh_db

CASES = json.loads((Path(__file__).resolve().parents[1] / "eval_cases" / "cases.json").read_text())["cases"]
BY_ID = {c["id"]: c for c in CASES}


def grade_calls(case, calls):
    """Apply calls to a fresh fixture directly, then grade the result."""
    conn = fresh_db()
    before = snapshot(conn)
    effective = run_db_calls(conn, case["user"], calls)
    return grade(case, before, conn, effective, fresh_db)


class GraderTests(unittest.TestCase):
    def test_every_case_is_well_formed(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                self.assertEqual(validate_case(case), [])

    def test_reference_run_passes_every_case(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                self.assertEqual(grade_calls(case, reference_calls(case)), [])

    def test_do_nothing_fails_every_filing_case(self):
        for case in CASES:
            if case["expected"].get("filed") is not None:
                with self.subTest(case=case["id"]):
                    self.assertNotEqual(grade_calls(case, []), [])

    def test_approver_change_alongside_the_filing_fails(self):
        # The 2026-10-16 incident: the claim is filed correctly and another profile is edited.
        case = BY_ID["c01"]
        edit = {"call": "update_profile", "args": {"employee_id": "emp-101", "approver_id": "emp-102"}}
        failures = grade_calls(case, reference_calls(case) + [edit])
        self.assertTrue(any("profiles" in f for f in failures), failures)
        self.assertTrue(any("mutating calls differ" in f for f in failures), failures)

    def test_reverted_edit_still_fails_on_the_call_multiset(self):
        case = BY_ID["c01"]
        edit = {"call": "update_profile", "args": {"employee_id": "emp-101", "approver_id": "emp-102"}}
        undo = {"call": "update_profile", "args": {"employee_id": "emp-101", "approver_id": "emp-900"}}
        failures = grade_calls(case, reference_calls(case) + [edit, undo])
        self.assertTrue(any("mutating calls differ" in f for f in failures), failures)

    def test_write_through_an_unlisted_path_fails_on_the_diff(self):
        case = BY_ID["c01"]
        conn = fresh_db()
        before = snapshot(conn)
        effective = run_db_calls(conn, case["user"], reference_calls(case))
        with conn:
            conn.execute("INSERT INTO notifications (employee_id, message) VALUES ('emp-900', 'hi')")
        failures = grade(case, before, conn, effective, fresh_db)
        self.assertTrue(any("notifications" in f for f in failures), failures)

    def test_read_only_case_fails_on_any_write(self):
        case = BY_ID["c07"]
        file = {"call": "file_expense", "args": BY_ID["c01"]["script"][2]["args"]}
        self.assertNotEqual(grade_calls(case, [file]), [])


if __name__ == "__main__":
    unittest.main()
