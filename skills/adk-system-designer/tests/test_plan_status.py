"""Exercise the build-time roll-up and the ticket lint through their CLIs on a plan in progress.

The fixture is a five-goal proof of concept: G01 finished with an overrun, a
contract delta and an open ruling; G02 interrupted with a Progress block; G03
ready; G04 the journey goal; G05 the review presentation waiting on decision D3.
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "plan-in-progress"


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        shutil.copytree(FIXTURE, self.root)
        self.design = self.root / "docs/architecture/support.md"
        self.plan = self.root / "docs/plans/support.md"
        self.tickets = self.root / "docs/tickets/support"

    def run_script(self, name, *args):
        proc = subprocess.run([sys.executable, str(SCRIPTS / name), *args], capture_output=True, text=True,
                              cwd=self.root)
        return proc.returncode, proc.stdout, proc.stderr

    def status(self, *extra):
        code, out, err = self.run_script("plan_status.py", "--plan", str(self.plan), "--tickets", str(self.tickets),
                                         "--design", str(self.design), "--json", *extra)
        self.assertNotEqual(2, code, err)
        return code, json.loads(out)

    def edit(self, path, old, new):
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")


class PlanInProgress(Fixture):
    def test_rolls_up_evidence_frontier_and_checkpoint_triggers(self):
        code, result = self.status("--capacity", "10")
        self.assertEqual(1, code)
        self.assertEqual({"C1": ["G01 local"], "C2": ["G01 local"]}, result["contracts"]["evidenced"])
        self.assertEqual(["C1", "C2"], result["contracts"]["stale_design_cells"])
        self.assertIn("C4", result["contracts"]["settled"])
        self.assertEqual({"C3": ["G02", "G04"], "C5": ["G03", "G04"]}, result["contracts"]["planned"])
        self.assertEqual(["G01 tier 1"], result["security"]["evidenced"]["SB01"])
        self.assertEqual(["G02", "G03"], result["ready"])
        self.assertIn("G02", result["interrupted"])
        self.assertEqual(["G02", "G03"], result["waiting"]["G04"])
        self.assertEqual(["G04", "D3"], result["waiting"]["G05"])
        self.assertEqual(["G02 and G03 both write web/src/chat/Message.tsx"], result["touch_overlaps"])
        triggers = "\n".join(result["checkpoint"])
        self.assertIn("contract delta not yet in the design: G01: C2", triggers)
        self.assertIn("open ruling: G01: forget is a soft delete", triggers)
        self.assertNotIn("profile table", triggers)  # a resource line after the rulings is not a ruling
        self.assertNotIn("overrun", triggers)  # a finished overrun shows up through the phase fit instead
        self.assertIn("G01: 6 h against an estimate of 2-3 h; re-estimate similar tickets",
                      result["effort"]["above_estimate"])
        self.assertIn("phase no longer fits: 12-17 h projected against 10 h", triggers)
        self.assertTrue(result["next"].startswith("/adk-system-designer Checkpoint"))

    def test_checkpoint_clears_once_the_design_and_tickets_take_the_decisions(self):
        self.edit(self.design, "| C2 | R1 | forget removes the preference before the next session",
                  "| C2 | R1 | forget removes the preference and its cached copy before the next session "
                  "(revised G01, 25 Oct)")
        self.edit(self.tickets / "G01.md", "(why: audit; cost if wrong: retention breach)",
                  "(why: audit; cost if wrong: retention breach) settled: D6")
        self.edit(self.tickets / "G01.md", "- actual: 6 h", "- actual: 3.5 h")
        code, result = self.status("--capacity", "20")
        self.assertEqual(0, code, result["checkpoint"])
        self.assertEqual([], result["checkpoint"])
        self.assertTrue(result["next"].endswith("G02.md from its Progress block."), result["next"])
        self.assertEqual(["G01: 3.5 h, above its 2-3 h estimate"], result["effort"]["above_estimate"])

    def test_orphaned_contract_and_blocked_ticket_need_a_checkpoint(self):
        self.edit(self.tickets / "G03.md", "contracts: [C5]", "contracts: []")
        self.edit(self.tickets / "G03.md", "(C5)", "(floor)")
        self.edit(self.plan, "  contracts: [C5]\n", "  contracts: []\n")
        self.edit(self.plan, "contracts: [C1, C2, C3, C5]", "contracts: [C1, C2, C3]")
        self.edit(self.tickets / "G04.md", "contracts: [C1, C2, C3, C5]", "contracts: [C1, C2, C3]")
        self.edit(self.tickets / "G03.md", "status: ready", "status: blocked")
        self.edit(self.tickets / "G02.md", "Progress:", "- actual: 5 h\n\nProgress:")
        _, result = self.status()
        self.assertIn("C5", result["contracts"]["orphaned"])
        triggers = "\n".join(result["checkpoint"])
        self.assertIn("orphaned contract C5", triggers)
        self.assertIn("blocked: G03", triggers)
        self.assertIn("overrun: G02: already 5 h against 2-4 h, unfinished", triggers)
        self.assertNotIn("G03", result["ready"])

    def test_gate_lists_every_reason_then_passes_when_the_phase_is_complete(self):
        code, result = self.status("--gate")
        self.assertEqual(1, code)
        reasons = "\n".join(result["gate"]["reasons"])
        for expected in ("G02 is in_progress", "G05 is without a status", "contract C3 is neither evidenced",
                         "open ruling", "contract delta not in the design"):
            self.assertIn(expected, reasons)
        self.edit(self.design, "before the next session | user", "before the next session (revised G01) | user")
        self.edit(self.tickets / "G01.md", "retention breach)", "retention breach) settled: D6")
        for goal, contract in (("G02", "C3"), ("G03", "C5"), ("G04", "C3")):
            path = self.tickets / f"{goal}.md"
            text = path.read_text(encoding="utf-8")
            text = text.replace("status: in_progress", "status: verified_local").replace("status: ready",
                                                                                       "status: verified_local")
            text = text.split("## Evidence")[0] + f"## Evidence\n\n- {contract}: evidenced, local, A1\n- actual: 2 h\n"
            path.write_text(text, encoding="utf-8")
        self.edit(self.plan, "  type: presentation\n", "  type: presentation\n  status: done\n")
        code, result = self.status("--gate")
        self.assertEqual(0, code, result["gate"]["reasons"])

    def test_weekly_update_has_effort_next_and_raid(self):
        code, out, err = self.run_script("plan_status.py", "--plan", str(self.plan), "--tickets", str(self.tickets),
                                         "--design", str(self.design), "--capacity", "20", "--weekly")
        self.assertEqual(0, code, err)
        self.assertIn("**Effort:** 6 h spent, 6-11 h remaining", out)
        self.assertIn("| Issue | above estimate: G01: 6 h against an estimate of 2-3 h", out)
        self.assertIn("| Dependency | G05 waits for D3 |", out)

    def test_plan_without_tickets_reads_statuses_from_the_schedule_and_goal_sections(self):
        plan = self.root / "docs/plans/plan-only.md"
        plan.write_text("""# Plan

```yaml
- goal: G01
  phase: 1
  type: implementation
  total: 1-2
  status: verified_local
  blocked_by: []
- goal: G02
  phase: 1
  type: implementation
  total: 1-2
  blocked_by: [G01]
```

### G01 — Save

- **Status and evidence:** verified_local; C1 evidenced, local, A1. actual: 1.5 h

### G02 — Forget

- **Status and evidence:** planned
""", encoding="utf-8")
        code, out, err = self.run_script("plan_status.py", "--plan", str(plan), "--design", str(self.design), "--json")
        self.assertNotEqual(2, code, err)
        result = json.loads(out)
        self.assertEqual(["G02"], result["ready"])
        self.assertEqual(["G01 local"], result["contracts"]["evidenced"]["C1"])
        self.assertIn("C2", result["contracts"]["orphaned"])

    def test_unreadable_input_exits_2(self):
        code, _, err = self.run_script("plan_status.py", "--tickets", str(self.root / "missing"))
        self.assertEqual(2, code)
        self.assertIn("not a directory", err)


class TicketLint(Fixture):
    def lint(self, *extra):
        code, out, err = self.run_script("check_tickets.py", "--tickets", str(self.tickets), "--json", *extra)
        self.assertNotEqual(2, code, err)
        return code, json.loads(out)

    def test_fixture_problems_are_reported(self):
        code, result = self.lint()
        self.assertEqual(1, code)
        errors = "\n".join(result["errors"])
        self.assertIn("G02.md: parallel_safe is yes but G03.md also writes web/src/chat/Message.tsx", errors)
        self.assertIn("G04.md: missing profile", errors)
        self.assertIn("G04.md: contract C1 is cited by no acceptance item", errors)
        self.assertGreater(result["tokens_per_ticket"]["G01"], 1000)

    def test_unknown_skill_contract_doc_placeholder_and_pass_to_pass(self):
        path = self.tickets / "G03.md"
        self.edit(path, "primary_skill: adk-frontend-integration", "primary_skill: adk-frontend-wizard")
        self.edit(path, "contracts: [C5]", "contracts: [C5, C9]")
        self.edit(path, "docs: []", "docs: [adk-frontend-integration/references/missing.md]")
        self.edit(path, "pass_to_pass: []", "pass_to_pass: [G01/A9, G07/A1, tests/test_ui.py::test_ok]")
        self.edit(path, "title: Failed state", "title: <first useful behaviour>")
        self.edit(path, "- [ ] A1 IF the stream fails THEN THE app SHALL show failed (C5)",
                  "- [ ] A1 IF the stream fails THEN THE app SHALL show failed (C5)\n- [ ] A2 THE app SHALL log it")
        _, result = self.lint()
        errors = "\n".join(e for e in result["errors"] if e.startswith("G03.md"))
        for expected in ("skill 'adk-frontend-wizard' is not an installed skill",
                         "contract C9 is not in the design's contracts table",
                         "docs path 'adk-frontend-integration/references/missing.md' does not resolve",
                         "pass_to_pass G01/A9: G01 has no acceptance item A9",
                         "pass_to_pass G07/A1 names goal G07",
                         "unfilled placeholder <first useful behaviour>",
                         "acceptance A2 cites no contract",
                         "contract C9 is cited by no acceptance item"):
            self.assertIn(expected, errors)
        self.assertNotIn("test_ui", errors)

    def test_companion_pin_google_skill_and_budget_warnings(self):
        (self.root / "AGENTS.md").write_text("| Companion | Source | Pin |\n| --- | --- | --- |\n"
                                             "| shadcn | npx skills add shadcn/ui | 4.1.0 |\n"
                                             "| playwright-cli | microsoft/playwright | latest |\n", encoding="utf-8")
        path = self.tickets / "G03.md"
        self.edit(path, "companion_skills: []", "companion_skills: [shadcn, playwright-cli, impeccable]")
        self.edit(path, "supporting_skills: []",
                  "supporting_skills: [google/skills:cloud-run-basics (deploy), google/skills:made-up (x)]")
        _, result = self.lint("--budget", "100")
        warnings = "\n".join(w for w in result["warnings"] if w.startswith("G03.md"))
        self.assertIn("companion playwright-cli has a row but no pin", warnings)
        self.assertIn("companion impeccable has no row", warnings)
        self.assertNotIn("companion shadcn", warnings)
        self.assertIn("google/skills:made-up is not in the implementation handoff's dated table", warnings)
        self.assertNotIn("cloud-run-basics", warnings)
        self.assertIn("about", warnings)

    def test_ticket_template_left_unfilled_fails(self):
        template = Path(__file__).resolve().parents[1] / "assets" / "ticket-template.md"
        shutil.copy(template, self.tickets / "G09.md")
        _, result = self.lint()
        errors = [e for e in result["errors"] if e.startswith("G09.md")]
        self.assertTrue(any("unfilled placeholder" in e for e in errors), errors)


del Fixture  # a base class only; keeps unittest from collecting it


if __name__ == "__main__":
    unittest.main()
