"""Exercise the SOW check through its public CLI with hand-computed fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_sow.py"

PLAN = """# Plan

```yaml
- goal: W1
  phase: 1
  total: 0
  wait_days: 5
  blocked_by: []
- goal: G01
  phase: 1
  total: 4-6
  owner: Ana
  blocked_by: []
- goal: G02
  phase: 1
  total: 2-4
  owner: Ana
  blocked_by: [G01, W1]
- goal: G03
  phase: 1
  total: 3-5
  owner: Ana
  blocked_by: [G02]
- goal: G04
  phase: 2
  total: 10
  owner: Ana
  blocked_by: [G03]
```
"""

DESIGN = """# Design

| ID | From | Invariant | Scope | Authority | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | answers cite the policy | user | policy store | tool | refusal | G01/A1 |
| C2 | R2 | no email without approval | user | approvals | gate | blocked | G02/A1 |
"""

SOW = """# Statement of work

## 2. Deliverables

| ID | Deliverable | Plan goals | Phase | Acceptance |
| --- | --- | --- | --- | --- |
| DL1 | Claims assistant | {dl1_goals} | 1 | AC1, AC2 |
| DL2 | Review and close-out | G03 | 1 | AC1 |

## 3. Acceptance criteria

| ID | Criterion | Threshold | Cases | Method | Measured by | Date | Contracts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC1 | Grounded answers | {threshold} | 40 gold cases agreed with claims leads | adk eval, rubric v1, 3 repeats | Agency; client witnesses | 2026-12-04 | {contracts} |
| AC2 | No email without approval | 0 of 25 | 25 adversarial cases | deterministic check | Agency | 2026-12-04 | C2 |

## 5. Client dependencies

| ID | Dependency | Owner | Needed by | Blocks | From plan |
| --- | --- | --- | --- | --- | --- |
| CD1 | SME hours | {owner} | {needed_by} | G02 | W1 |

## 6. Effort, fees and run cost

| Phase | Goals | Human hours | Rate per hour | Fees |
| --- | --- | --- | --- | --- |
| 1 | G01-G03 | {hours} | {rate} | {fees} |
| Total | | {total_hours} | | {total_fees} |
"""

GOOD = dict(dl1_goals="G01, G02", threshold="≥ 85% pass", contracts="C1", owner="Claims ops lead",
            needed_by="2026-11-06", hours="9-15", rate="£100", fees="£900–£1,500",
            total_hours="9-15", total_fees="£900–£1,500")

CHANGE = """# Change request CR1

| Kind | IDs | Change |
| --- | --- | --- |
| Contracts | {contracts} | tighten |
| Goals | {goals} | add a channel |

| | Before | After | Difference |
| --- | --- | --- | --- |
| Human hours | 9-15 | {after} | 3-5 |
"""


class CheckSowTest(unittest.TestCase):
    def run_check(self, sow=None, change=None, design=False, **overrides):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "plan.md").write_text(PLAN, encoding="utf-8")
            (root / "design.md").write_text(DESIGN, encoding="utf-8")
            args = [sys.executable, str(SCRIPT), "--plan", str(root / "plan.md"), "--json"]
            if sow is not False:
                fields = dict(GOOD, **overrides)
                (root / "sow.md").write_text((sow or SOW).format(**fields), encoding="utf-8")
                args += ["--sow", str(root / "sow.md")]
            if change is not None:
                (root / "cr.md").write_text(change, encoding="utf-8")
                args += ["--change", str(root / "cr.md")]
            if design:
                args += ["--design", str(root / "design.md")]
            proc = subprocess.run(args, capture_output=True, text=True)
            data = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else None
            return proc, data

    def problems(self, **overrides):
        proc, data = self.run_check(**overrides)
        return proc.returncode, " | ".join(data["problems"]) if data else proc.stderr

    def test_consistent_sow_passes_with_hand_computed_totals(self):
        proc, data = self.run_check(design=True)
        self.assertEqual(proc.returncode, 0, data)
        self.assertEqual(data["plan_hours"], [9.0, 15.0])
        self.assertEqual(data["priced_phases"], ["1"])

    def test_ranges_in_plan_goals_expand(self):
        code, text = self.problems(dl1_goals="G01–G02")
        self.assertEqual(code, 0, text)

    def test_unknown_goal_and_unmapped_goal_fail(self):
        code, text = self.problems(dl1_goals="G01, G09")
        self.assertEqual(code, 1)
        self.assertIn("G09 is not in the plan", text)
        self.assertIn("G02 (phase 1, 2-4 h) belongs to no deliverable", text)

    def test_goal_in_two_deliverables_fails(self):
        code, text = self.problems(dl1_goals="G01, G02, G03")
        self.assertIn("G03 belongs to both DL1 and DL2", text)

    def test_hours_must_match_schedule_block(self):
        code, text = self.problems(hours="9-14", total_hours="9-14", fees="£900–£1,400",
                                   total_fees="£900–£1,400")
        self.assertEqual(code, 1)
        self.assertIn("differs from the schedule block's 9-15 h", text)

    def test_fees_must_equal_hours_times_rate(self):
        code, text = self.problems(fees="£900–£1,600")
        self.assertIn("fees should be 900-1,500", text)

    def test_fees_without_rate_fail_but_open_rate_passes(self):
        code, text = self.problems(rate="rate to be supplied")
        self.assertIn("fees given without an hourly rate", text)
        proc, data = self.run_check(rate="rate to be supplied", fees="open", total_fees="open")
        self.assertEqual(proc.returncode, 0, data)
        self.assertIn("rate not supplied", " ".join(data["notes"]))

    def test_total_row_must_add_up(self):
        code, text = self.problems(total_hours="9-16")
        self.assertIn("effort total 9-16 h differs", text)

    def test_vague_threshold_fails(self):
        code, text = self.problems(threshold="answers correctly")
        self.assertEqual(code, 1)
        self.assertIn("needs a number and a comparator", text)
        code, text = self.problems(threshold="85% pass")
        self.assertIn("needs a number and a comparator", text)

    def test_zero_count_threshold_is_measurable(self):
        code, text = self.problems(threshold="0 uncited claims")
        self.assertEqual(code, 0, text)

    def test_dependency_needs_owner_and_date(self):
        code, text = self.problems(owner="TBC", needed_by="early November")
        self.assertIn("CD1: no owner", text)
        self.assertIn("CD1: no date", text)
        code, text = self.problems(needed_by="5 working days after signature")
        self.assertEqual(code, 0, text)

    def test_placeholder_left_fails(self):
        code, text = self.problems(needed_by="<YYYY-MM-DD>")
        self.assertIn("placeholder '<YYYY-MM-DD>'", text)

    def test_unknown_contract_fails_with_design(self):
        proc, data = self.run_check(design=True, contracts="C7")
        self.assertIn("cites C7, which is not in the design", " ".join(data["problems"]))

    def test_comparator_inside_cell_is_not_a_placeholder(self):
        code, text = self.problems(threshold="p95 < 8 s and > 0 of 40 timeouts")
        self.assertEqual(code, 0, text)

    def test_change_request_cites_ids_and_estimate(self):
        good = CHANGE.format(contracts="C2 (revised)", goals="G02 (re-estimated), G11 (new)", after="12-20")
        proc, data = self.run_check(sow=False, change=good, design=True)
        self.assertEqual(proc.returncode, 0, data)
        bad = CHANGE.format(contracts="C9", goals="G12", after="")
        proc, data = self.run_check(sow=False, change=bad, design=True)
        text = " ".join(data["problems"])
        self.assertIn("G12 is not in the plan", text)
        self.assertIn("C9 is not in the design", text)
        self.assertIn("hours before and after", text)

    def test_missing_table_is_an_input_error(self):
        proc, _ = self.run_check(sow="# Empty SOW\n")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("no deliverables table", proc.stderr)


if __name__ == "__main__":
    unittest.main()
