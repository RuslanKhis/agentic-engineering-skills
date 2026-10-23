"""Exercise the schedule check through its public CLI with hand-computed fixtures."""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_schedule.py"

PLAN = """# Plan

Some prose with 99 h that the check ignores.

```yaml
- goal: G01
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Ana
  blocked_by: []
- goal: G02
  phase: 1
  total: 2-4
  owner: {g02_owner}
  blocked_by: [G01]
- goal: G03
  phase: 1
  total: 6 to 8 h
  owner: Ana
  blocked_by: [G01, D2]
- goal: G04
  phase: 1
  total: 2
  owner: Ben
  blocked_by: [G02, G03]
  calendar_waits: security review
  wait_days: 1-2
- goal: G05
  phase: 2
  total: 10
  owner: Ana
  blocked_by: [G04]
```
"""

TICKET = """---
goal: {goal}
title: something
phase: 1
estimate:
  hands_on: {hands_on}
  review_and_verify: {review}
  total: {total}
  calendar_waits: none
owner: {owner}
blocked_by: {blocked}
status: ready
---

# {goal}
"""

CONTRACTS = """| ID | From | Invariant | Scope | Authority | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | rights | account | rights system | filter | fewer results | planned |
| C2 | R2 | confirm | quote | proposal | binding | refused | planned |
"""

SECURITY = """| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | {sb01} |
| SB05 | ADK runtime | Build | {sb05} |
"""


class ScheduleTests(unittest.TestCase):
    def run_check(self, *args):
        if "--reserve" not in args:
            args = (*args, "--reserve", "0")
        proc = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
        return proc.returncode, proc.stdout, proc.stderr

    def write_plan(self, root, g02_owner="Ben"):
        path = Path(root) / "plan.md"
        path.write_text(PLAN.format(g02_owner=g02_owner))
        return path

    def test_totals_chain_and_finish_with_dependencies(self):
        with tempfile.TemporaryDirectory() as root:
            code, out, err = self.run_check("--plan", str(self.write_plan(root)), "--person", "Ana=2",
                                            "--person", "Ben=2", "--capacity", "24", "--days", "10", "--json")
            self.assertEqual(code, 0, err + out)
            result = json.loads(out)
            self.assertEqual(result["goals"], 4)
            self.assertEqual(result["total_hours"], [14.0, 20.0])
            self.assertEqual(result["chain_low"], {"goals": ["G01", "G03", "G04"], "days": 7.0})
            self.assertEqual(result["chain_high"]["days"], 10.0)
            self.assertEqual(result["finish_days_low"], 7.0)
            self.assertEqual(result["load_by_person"]["Ana"], [10.0, 14.0])
            self.assertEqual(result["outside_dependencies"], ["D2"])
            self.assertEqual(result["fits_calendar"], "yes")

    def test_busy_person_sets_finish_beyond_chain(self):
        with tempfile.TemporaryDirectory() as root:
            code, out, _ = self.run_check("--plan", str(self.write_plan(root, g02_owner="Ana")),
                                          "--person", "Ana=2", "--person", "Ben=2", "--days", "7", "--json")
            result = json.loads(out)
            self.assertEqual(result["chain_low"]["days"], 7.0)
            self.assertEqual(result["finish_days_low"], 8.0)
            self.assertEqual(result["fits_calendar"], "no")
            self.assertEqual(code, 1)

    def test_reserve_is_held_back_on_the_calendar(self):
        with tempfile.TemporaryDirectory() as root:
            code, out, _ = self.run_check("--plan", str(self.write_plan(root)), "--person", "Ana=2",
                                          "--person", "Ben=2", "--days", "8", "--reserve", "0.5", "--json")
            result = json.loads(out)
            self.assertEqual(result["finish_days_low"], 13.0)
            self.assertEqual(result["person_capacity"]["Ana"], 8.0)
            self.assertEqual(result["fits_calendar"], "no")
            self.assertEqual(code, 1)

    def test_capacity_is_computed_from_people_and_days(self):
        with tempfile.TemporaryDirectory() as root:
            code, out, _ = self.run_check("--plan", str(self.write_plan(root)), "--person", "Ana=2",
                                          "--person", "Ben=2", "--days", "10", "--reserve", "0.25", "--json")
            self.assertEqual(json.loads(out)["capacity_hours"], 30.0)

    def test_cross_person_dependencies_are_listed_until_handoff_recorded(self):
        with tempfile.TemporaryDirectory() as root:
            code, out, _ = self.run_check("--plan", str(self.write_plan(root)), "--json")
            self.assertEqual(json.loads(out)["handoffs_without_hours"],
                             ["G01 (Ana) -> G02 (Ben)", "G03 (Ana) -> G04 (Ben)"])
            plan = Path(root) / "plan.md"
            plan.write_text(plan.read_text().replace("  owner: Ben\n  blocked_by: [G01]",
                                                     "  owner: Ben\n  handoff: 0.5\n  blocked_by: [G01]"))
            code, out, _ = self.run_check("--plan", str(plan), "--json")
            self.assertEqual(json.loads(out)["handoffs_without_hours"], ["G03 (Ana) -> G04 (Ben)"])
            plan.write_text(plan.read_text().replace("handoff: 0.5", "handoff: 0"))
            code, out, _ = self.run_check("--plan", str(plan), "--json")
            self.assertEqual(len(json.loads(out)["handoffs_without_hours"]), 2)

    def test_handoff_none_from_the_ticket_template_is_no_handoff(self):
        with tempfile.TemporaryDirectory() as root:
            tickets = Path(root)
            (tickets / "a.md").write_text(TICKET.format(goal="G01", hands_on="1", review="1", total="2",
                                                        owner="Ana", blocked="[]"))
            ticket = TICKET.format(goal="G02", hands_on="1", review="1", total="2", owner="Ben", blocked="[G01]")
            (tickets / "b.md").write_text(ticket.replace("  calendar_waits: none", "  handoff: none\n  calendar_waits: none"))
            code, out, err = self.run_check("--tickets", str(tickets), "--json")
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)["handoffs_without_hours"], ["G01 (Ana) -> G02 (Ben)"])

    def test_list_values_accept_trailing_comments(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("check_schedule_under_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        parse_scalar = module.parse_scalar
        self.assertEqual(parse_scalar("[G03]   # cross-person mention"), ["G03"])
        self.assertEqual(parse_scalar("[G01, G02] # two"), ["G01", "G02"])
        self.assertEqual(parse_scalar("none   # or what"), "none")

    def test_plan_template_schedule_block_passes_design_check(self):
        # Regression: the template's commented list lines once parsed as "[C1" and "C3]",
        # so every plan that kept the comments failed --design.
        template = SCRIPT.parents[1] / "assets" / "implementation-plan-template.md"
        block = re.search(r"^```yaml\n(- goal: G01\n.*?)^```", template.read_text(), re.M | re.S).group(1)
        self.assertIn("  contracts: [C1, C3]    # design contracts", block)
        self.assertIn("  mentions_only: []      # IDs", block)
        with tempfile.TemporaryDirectory() as root:
            plan = Path(root) / "plan.md"
            plan.write_text("```yaml\n" + block + "```\n")
            design = Path(root) / "design.md"
            design.write_text(CONTRACTS.replace("| C2 | R2 | confirm | quote |", "| C3 | R2 | confirm | quote |")
                              + "\n" + SECURITY.format(sb01="G01/A1", sb05="G01/A2"))
            code, out, err = self.run_check("--plan", str(plan), "--design", str(design), "--json")
            result = json.loads(out)
            self.assertEqual(result["problems"], [], err + out)
            self.assertEqual(code, 0)
            self.assertEqual(result["contract_coverage"]["cited"], ["C1", "C3"])
            self.assertEqual(result["settled_as_mention_only"], [])

    def test_every_build_or_minimal_rule_is_cited_or_settled(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            text = plan.read_text().replace("  owner: Ana\n  blocked_by: []\n",
                                            "  owner: Ana\n  blocked_by: []\n  security: [SB01, SB99]\n", 1)
            plan.write_text(text + "\n### G02 Chat\n- [ ] A1 another user's session is not found (C2, SB03)\n")
            design = Path(root) / "design.md"
            design.write_text("| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |\n"
                              "| --- | --- | --- | --- |\n"
                              "| SB01 | /api routes | Build | G01/A1 |\n"
                              "| SB03 | agent routes | Build | G02/A1 |\n"
                              "| SB05 | ADK runtime | Build | planned |\n"
                              "| SB07 | API config | Minimal | |\n"
                              "| SB11 | uploads | n/a | n/a: no uploads |\n"
                              "| SB14 | logging | Build | deferred: internal-tool depth |\n"
                              "| SB20 | identity | Defer | MVP |\n")
            code, out, _ = self.run_check("--plan", str(plan), "--design", str(design), "--json")
            result = json.loads(out)
            self.assertEqual(code, 1)
            self.assertEqual(len(result["problems"]), 3, result["problems"])
            self.assertIn("G01 cites SB99, which is not in the design's web security baseline", result["problems"][0])
            self.assertIn("security rule SB05 (Build): no goal cites it", result["problems"][1])
            self.assertIn("security rule SB07 (Minimal): no goal cites it", result["problems"][2])
            self.assertEqual(result["security_coverage"]["cited"], ["SB01", "SB03"])
            self.assertEqual(sorted(result["security_coverage"]["not_covered_by_choice"]), ["SB11", "SB14"])

    def test_only_lists_and_acceptance_items_cite_rules(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            plan.write_text(plan.read_text() + "\n### G02 Handover\nThe evidence lists SB01\u2013SB25; SB14: deferred.\n"
                            "- [ ] A1 another user's record is not found (C2, `SB04`)\n")
            design = Path(root) / "design.md"
            design.write_text("| Rule | Component | Depth now | Proved by |\n| --- | --- | --- | --- |\n"
                              "| `SB01` | /api | **Build** | G01/A1 |\n"
                              "| SB04 | records | Minimal | G02/A1 |\n"
                              "| SB14 | logging | **Build** | |\n"
                              "| SB25 | edge | Build | |\n"
                              "| SB07 | config | Tier 3 | G05/A2 |\n")
            code, out, _ = self.run_check("--plan", str(plan), "--design", str(design), "--json")
            result = json.loads(out)
            self.assertEqual(code, 1)
            problems = result["problems"]
            self.assertEqual(len(problems), 4, problems)
            self.assertIn("security rule SB01 (Build): no goal cites it", problems[0])
            self.assertIn("security rule SB14 (Build): no goal cites it", problems[1])
            self.assertIn("security rule SB25 (Build): no goal cites it", problems[2])
            self.assertIn("security rule SB07: depth 'Tier 3' is not Build", problems[3])
            self.assertEqual(result["security_coverage"]["cited"], ["SB04"])

    def test_design_without_security_table_skips_rule_coverage(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            plan.write_text(plan.read_text().replace("  owner: Ana\n  blocked_by: []\n",
                                                     "  owner: Ana\n  blocked_by: []\n  contracts: [C1, C2]\n", 1))
            design = Path(root) / "design.md"
            design.write_text(CONTRACTS)
            code, out, _ = self.run_check("--plan", str(plan), "--design", str(design), "--json")
            result = json.loads(out)
            self.assertEqual(result["problems"], [])
            self.assertNotIn("security_coverage", result)

    def test_ticket_security_rules_must_match_the_plan(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            plan.write_text(plan.read_text().replace("  owner: Ana\n  blocked_by: []\n",
                                                     "  owner: Ana\n  blocked_by: []\n  security: [SB01]\n", 1))
            tickets = Path(root) / "tickets"
            tickets.mkdir()
            ticket = TICKET.format(goal="G01", hands_on="3-4", review="1-2", total="4-6", owner="Ana", blocked="[]")
            (tickets / "G01.md").write_text(ticket.replace("status: ready", "security: [SB01, SB05]\nstatus: ready"))
            code, out, _ = self.run_check("--plan", str(plan), "--tickets", str(tickets))
            self.assertEqual(code, 1)
            self.assertIn("G01.md: security ['SB01', 'SB05'] differ from plan ['SB01']", out)

    def test_prose_mentions_outside_the_schedule_are_listed_for_review(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            plan.write_text(plan.read_text() + """
### G02 Booking tool
Its acceptance runs once G03 lands. Later G04 builds on it.

### G04 Release
Needs the legal review before go-live.
""")
            code, out, _ = self.run_check("--plan", str(plan), "--json")
            result = json.loads(out)
            self.assertEqual(code, 0, "mentions are for review and must not fail the run")
            self.assertEqual(len(result["mentions_to_review"]), 2, result["mentions_to_review"])
            self.assertIn("G02 mentions G03, which is neither before nor after it", result["mentions_to_review"][0])
            self.assertIn("G04 mentions 'legal review' but no wait for it", result["mentions_to_review"][1])
            plan.write_text(plan.read_text().replace("  owner: Ben\n  blocked_by: [G01]",
                                                     "  owner: Ben\n  mentions_only: [G03]\n  blocked_by: [G01]")
                            .replace("calendar_waits: security review", "calendar_waits: security review; legal review"))
            result = json.loads(self.run_check("--plan", str(plan), "--json")[1])
            self.assertEqual(result["mentions_to_review"], [])
            self.assertEqual(result["settled_as_mention_only"], ["G02: G03"])

    def test_approval_needs_its_own_wait_not_any_wait(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "plan.md"
            path.write_text("```yaml\n- goal: W1\n  phase: 1\n  total: 0\n  wait_days: 5\n"
                            "  calendar_waits: Vertex quota increase\n  blocked_by: []\n"
                            "- goal: G01\n  phase: 1\n  total: 6\n  owner: Ana\n  blocked_by: [W1]\n```\n"
                            "### G01 Launch\nNeeds the pen test report and sign-off from the owner.\n")
            result = json.loads(self.run_check("--plan", str(path), "--json")[1])
            self.assertEqual(len(result["mentions_to_review"]), 1, result["mentions_to_review"])
            self.assertIn("'pen test'", result["mentions_to_review"][0])
            path.write_text(path.read_text().replace("Vertex quota increase", "Vertex quota increase; pentest slot"))
            result = json.loads(self.run_check("--plan", str(path), "--json")[1])
            self.assertEqual(result["mentions_to_review"], [])

    def test_grid_cells_cite_acceptance_or_give_a_reason(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            plan.write_text(plan.read_text() + "\n### G02 Booking tool\n- [ ] A1 booking API down shows retry\n"
                            "- [ ] A2 timeout is reconciled\n")
            design = Path(root) / "design.md"
            design.write_text("| Integration | Unavailable or slow | Write outcome unknown | Rate limited |\n"
                              "| --- | --- | --- | --- |\n"
                              "| Booking API | retry shown (G02/A1) | reconcile (G02/A2) | n/a: one call per turn |\n"
                              "| Model | G02/A7 | n/a | |\n")
            code, out, _ = self.run_check("--plan", str(plan), "--design", str(design), "--json")
            problems = json.loads(out)["problems"]
            self.assertEqual(code, 1)
            self.assertEqual(len(problems), 3, problems)
            self.assertIn("G02/A7 is not an acceptance item of G02", problems[0])
            self.assertIn("Model / Write outcome unknown", problems[1])
            self.assertIn("Model / Rate limited", problems[2])
            self.assertNotIn("contract_coverage", json.loads(out))

    def test_every_contract_is_cited_or_marked_as_a_gap(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            text = plan.read_text().replace("  owner: Ana\n  blocked_by: []\n",
                                            "  owner: Ana\n  blocked_by: []\n  contracts: [C1, C9]\n", 1)
            plan.write_text(text + "\n### G02 Purchase\n- [ ] A1 changed payload is refused (C2)\n")
            design = Path(root) / "design.md"
            design.write_text("| ID | From | Invariant | Scope | Authority | Enforcement | Failure outcome | Evidence |\n"
                              "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                              "| C1 | R1 | rights | account | rights system | filter | fewer results | planned |\n"
                              "| C2 | R2 | confirm | quote | proposal | binding | refused | planned |\n"
                              "| C3 | R2 | one order | operation | receipts | record | pending | planned |\n"
                              "| C4 | R3 | status | order | receipts | read | unknown | deferred: real orders |\n")
            code, out, _ = self.run_check("--plan", str(plan), "--design", str(design), "--json")
            result = json.loads(out)
            self.assertEqual(code, 1)
            self.assertEqual(len(result["problems"]), 2, result["problems"])
            self.assertIn("G01 cites C9, which is not in the design", result["problems"][0])
            self.assertIn("contract C3: no goal cites it", result["problems"][1])
            self.assertEqual(result["contract_coverage"]["cited"], ["C1", "C2"])
            self.assertEqual(list(result["contract_coverage"]["not_covered_by_choice"]), ["C4"])

    def test_ticket_contracts_must_match_the_plan(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            plan.write_text(plan.read_text().replace("  owner: Ana\n  blocked_by: []\n",
                                                     "  owner: Ana\n  blocked_by: []\n  contracts: [C1]\n", 1))
            tickets = Path(root) / "tickets"
            tickets.mkdir()
            ticket = TICKET.format(goal="G01", hands_on="3-4", review="1-2", total="4-6", owner="Ana", blocked="[]")
            (tickets / "G01.md").write_text(ticket.replace("status: ready", "contracts: [C1, C2]\nstatus: ready"))
            code, out, _ = self.run_check("--plan", str(plan), "--tickets", str(tickets))
            self.assertEqual(code, 1)
            self.assertIn("G01.md: contracts ['C1', 'C2'] differ from plan ['C1']", out)

    def test_outside_approval_needs_a_wait_before_it(self):
        with tempfile.TemporaryDirectory() as root:
            tickets = Path(root)
            (tickets / "a.md").write_text(TICKET.format(goal="G01", hands_on="1", review="1", total="2",
                                                        owner="Ana", blocked="[]")
                                          + "Go live needs sign-off from the salon owner.\n")
            code, out, _ = self.run_check("--tickets", str(tickets), "--json")
            self.assertIn("G01 mentions 'sign-off' but no wait for it",
                          json.loads(out)["mentions_to_review"][0])
            (tickets / "w.md").write_text(TICKET.format(goal="W1", hands_on="0", review="0", total="0",
                                                        owner="", blocked="[G01]")
                                          .replace("calendar_waits: none", "calendar_waits: owner sign-off")
                                          .replace("status: ready", "wait_days: 1-2\nstatus: ready"))
            text = (tickets / "a.md").read_text().replace("blocked_by: []", "blocked_by: []\nmentions_only: wait")
            (tickets / "a.md").write_text(text)
            code, out, _ = self.run_check("--tickets", str(tickets), "--json")
            self.assertEqual(json.loads(out)["mentions_to_review"], [])

    def test_a_wait_can_depend_on_a_goal(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "plan.md"
            path.write_text("```yaml\n- goal: G01\n  phase: 1\n  total: 6\n  owner: Ana\n  blocked_by: []\n"
                            "- goal: W1\n  phase: 1\n  total: 0\n  wait_days: 5\n"
                            "  calendar_waits: DPIA sign-off needs G01 evidence\n  blocked_by: [G01]\n"
                            "- goal: G02\n  phase: 1\n  total: 6\n  owner: Ana\n  blocked_by: [W1]\n```\n")
            code, out, _ = self.run_check("--plan", str(path), "--person", "Ana=6", "--json")
            result = json.loads(out)
            self.assertEqual(result["problems"], [])
            self.assertEqual(result["finish_days_high"], 7.0)

    def test_capacity_low_end_only_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            code, out, _ = self.run_check("--plan", str(self.write_plan(root)), "--capacity", "16")
            self.assertEqual(code, 1)
            self.assertIn("fits: low end only", out)

    def test_ticket_mismatches_and_unknown_goal(self):
        with tempfile.TemporaryDirectory() as root:
            plan = self.write_plan(root)
            tickets = Path(root) / "tickets"
            tickets.mkdir()
            (tickets / "G01.md").write_text(TICKET.format(goal="G01", hands_on="3-4", review="1-2", total="4-6",
                                                          owner="Ana", blocked="[]"))
            (tickets / "G02.md").write_text(TICKET.format(goal="G02", hands_on="1-2", review="1", total="2-3",
                                                          owner="Ben", blocked="[]"))
            (tickets / "G09.md").write_text(TICKET.format(goal="G09", hands_on="1", review="1", total="2",
                                                          owner="Ben", blocked="[]"))
            code, out, _ = self.run_check("--plan", str(plan), "--tickets", str(tickets))
            self.assertEqual(code, 1)
            self.assertIn("G02.md: total 2-3 differs from plan 2-4", out)
            self.assertIn("G02.md: blocked_by [] differs from plan ['G01']", out)
            self.assertIn("G09 is not in the plan", out)
            self.assertNotIn("G01.md", out)

    def test_parts_must_add_up_to_total(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "plan.md"
            path.write_text("```yaml\n- goal: G01\n  phase: 1\n  hands_on: 1-2\n  review: 1\n  total: 3\n```\n")
            code, out, _ = self.run_check("--plan", str(path))
            self.assertEqual(code, 1)
            self.assertIn("hands_on + review = 2-3 but total is 3-3", out)

    def test_fixed_review_ratio_is_flagged(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "plan.md"
            goals = "".join(f"- goal: G0{i}\n  phase: 1\n  hands_on: {2 * i}\n  review: {i}\n  total: {3 * i}\n"
                            for i in range(1, 6))
            path.write_text("```yaml\n" + goals + "```\n")
            code, out, _ = self.run_check("--plan", str(path))
            self.assertEqual(code, 1)
            self.assertIn("review is 0.50-0.50 of hands-on on every goal", out)

    def test_tickets_alone_are_enough(self):
        with tempfile.TemporaryDirectory() as root:
            tickets = Path(root)
            (tickets / "a.md").write_text(TICKET.format(goal="G01", hands_on="1", review="1", total="2",
                                                        owner="Ana", blocked="[]"))
            (tickets / "b.md").write_text(TICKET.format(goal="G02", hands_on="2", review="1", total="3",
                                                        owner="Ana", blocked="[G01]"))
            code, out, _ = self.run_check("--tickets", str(tickets), "--person", "Ana=1", "--json")
            self.assertEqual(code, 0, out)
            self.assertEqual(json.loads(out)["finish_days_high"], 5.0)

    def test_unreadable_input_exits_2(self):
        with tempfile.TemporaryDirectory() as root:
            cycle = Path(root) / "cycle.md"
            cycle.write_text("```yaml\n- goal: A\n  phase: 1\n  total: 1\n  blocked_by: [B]\n"
                             "- goal: B\n  phase: 1\n  total: 1\n  blocked_by: [A]\n```\n")
            code, _, err = self.run_check("--plan", str(cycle))
            self.assertEqual(code, 2)
            self.assertIn("dependency cycle", err)
            bad = Path(root) / "bad.md"
            bad.write_text("```yaml\n- goal: A\n  total: a few\n```\n")
            code, _, err = self.run_check("--plan", str(bad))
            self.assertEqual(code, 2)
            self.assertIn("cannot read hours range", err)
            code, _, err = self.run_check("--plan", str(Path(root) / "missing.md"))
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
