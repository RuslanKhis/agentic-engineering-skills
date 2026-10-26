"""Document goals (presentation, governance, portability) in the ticket lint, the roll-up and the schedule check.

The fixture is built in a temporary directory: a project with a one-contract
design, a phase-1 plan whose portability goal G01 depends only on the design,
an implementation goal G02, its journey goal G03 and a review G04, and a
sibling skills directory of stub packages so ``--skills-dir`` resolves every
skill the tickets name, including ``adk-portability-planning``.
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
HANDOFF = Path(__file__).resolve().parents[1] / "references" / "implementation-handoff.md"

DESIGN = """# Design

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | a user reads only their own preference | user | profile store | API dependency | 404 | planned: owner test, local |
"""

PLAN = """# Plan

```yaml
- goal: G01
  phase: 1
  type: portability
  total: 2-3
  owner: Ana
  blocked_by: []
  contracts: []
- goal: G02
  phase: 1
  type: implementation
  total: 2-3
  owner: Ana
  blocked_by: []
  contracts: [C1]
- goal: G03
  phase: 1
  type: journey
  total: 1-2
  owner: Ana
  blocked_by: [G02]
  contracts: [C1]
- goal: G04
  phase: 1
  type: presentation
  total: 2-3
  owner: Ana
  blocked_by: [G03]
```
"""

PORTABILITY_TICKET = """---
goal: G01
title: Portability assessment for the support assistant
design: docs/architecture/support.md
plan: docs/plans/support.md
primary_skill: adk-portability-planning
supporting_skills: []
docs: [adk-portability-planning/references/principles.md, adk-portability-planning/references/aws.md]
blocked_by: []
touches: [docs/portability/support.md]
parallel_safe: yes
contracts: []
companion_skills: []
security: []
contract_deltas: []
pass_to_pass: []
phase: 1
profile: proof of concept
type: portability
estimate:
  total: 2-3
owner: Ana
status: ready
---

# G01 Portability assessment for the support assistant

## Outcome

Read the accepted GCP + Google ADK architecture and plan. Produce a high-level
portability assessment for AWS. Keep it separate from the baseline.

## Acceptance

- [ ] A1 THE assessment docs/portability/support.md SHALL exist and check_portability.py SHALL exit 0 with --design and --plan (deliverable)
- [ ] A2 THE assessment SHALL cover the targets recorded in the scope gate and each of the five dimensions (deliverable)
- [ ] A3 EVERY provider or framework claim that drives a classification or risk SHALL cite an official source with its read date (deliverable)
- [ ] A4 THE design document SHALL NOT change; `git diff --exit-code 3f2a1bc -- docs/architecture/support.md` exits 0 (deliverable)
- [ ] A5 THE skill SHALL NOT write application code, infrastructure code or new tickets (deliverable)

## Evidence
"""

IMPLEMENTATION_TICKET = """---
goal: G02
title: Save a preference
design: docs/architecture/support.md
plan: docs/plans/support.md
primary_skill: adk-workflow-design
supporting_skills: []
docs: []
blocked_by: []
touches: [app/profile.py]
parallel_safe: yes
contracts: [C1]
companion_skills: []
security: []
contract_deltas: []
pass_to_pass: []
phase: 1
profile: proof of concept
type: implementation
estimate:
  total: 2-3
owner: Ana
status: ready
---

# G02 Save a preference

## Acceptance

- [ ] A1 WHEN another user asks THE api SHALL return 404 (C1)

## Evidence
"""

STUB_SKILLS = ("adk-portability-planning", "adk-workflow-design", "adk-agent-evaluation", "adk-presenter",
               "adk-governance-pack")


class DocumentGoals(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root = base / "project"
        self.skills = base / "skills"
        self.design = self.write(self.root / "docs/architecture/support.md", DESIGN)
        self.plan = self.write(self.root / "docs/plans/support.md", PLAN)
        self.tickets = self.root / "docs/tickets/support"
        self.write(self.tickets / "G01.md", PORTABILITY_TICKET)
        self.write(self.tickets / "G02.md", IMPLEMENTATION_TICKET)
        for skill in STUB_SKILLS:
            self.write(self.skills / skill / "SKILL.md", f"---\nname: {skill}\ndescription: stub\n---\n")
        for ref in ("principles", "aws", "azure", "agent-frameworks"):
            self.write(self.skills / "adk-portability-planning/references" / f"{ref}.md", f"# {ref}\n")

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def edit(self, path, old, new):
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def run_script(self, name, *args):
        proc = subprocess.run([sys.executable, str(SCRIPTS / name), *args], capture_output=True, text=True,
                              cwd=self.root)
        self.assertNotEqual(2, proc.returncode, proc.stderr)
        return proc.returncode, json.loads(proc.stdout)

    def lint(self):
        return self.run_script("check_tickets.py", "--tickets", str(self.tickets), "--skills-dir", str(self.skills),
                               "--json")

    def status(self, *extra):
        return self.run_script("plan_status.py", "--plan", str(self.plan), "--tickets", str(self.tickets),
                               "--design", str(self.design), "--json", *extra)

    def test_portability_ticket_with_deliverable_items_and_no_contracts_passes(self):
        code, result = self.lint()
        self.assertEqual([], result["errors"])
        self.assertEqual(0, code)

    def test_handoff_example_front_matter_passes_with_its_acceptance_items(self):
        section = HANDOFF.read_text(encoding="utf-8").split("## Plan a portability goal", 1)[1].split("\n## ", 1)[0]
        front = section.split("```yaml\n", 1)[1].split("```", 1)[0]
        items = [line for line in section.splitlines() if line.startswith("- [ ] A")]
        self.assertEqual(5, len(items))
        self.assertTrue(all(line.endswith("(deliverable)") for line in items), items)
        body = "\n".join(items).replace("<topic>", "support").replace("<base>", "3f2a1bc")
        self.write(self.tickets / "G01.md", PORTABILITY_TICKET.split("---", 2)[0] + front.replace("goal: G02", "goal: G01")
                   + "\n# G01\n\n## Acceptance\n\n" + body + "\n\n## Evidence\n")
        code, result = self.lint()
        self.assertEqual([], result["errors"])
        self.assertEqual(0, code)

    def test_deliverable_tag_is_accepted_on_presentation_and_governance_tickets(self):
        for kind, skill in (("presentation", "adk-presenter"), ("governance", "adk-governance-pack")):
            with self.subTest(kind=kind):
                self.write(self.tickets / "G01.md", PORTABILITY_TICKET.replace("type: portability", f"type: {kind}")
                           .replace("primary_skill: adk-portability-planning", f"primary_skill: {skill}"))
                code, result = self.lint()
                self.assertEqual([], result["errors"])

    def test_deliverable_tag_on_an_implementation_ticket_is_an_error(self):
        self.edit(self.tickets / "G02.md", "contracts: [C1]", "contracts: []")
        self.edit(self.tickets / "G02.md", "(C1)", "(deliverable)")
        code, result = self.lint()
        self.assertEqual(1, code)
        errors = [e for e in result["errors"] if e.startswith("G02.md")]
        self.assertEqual(1, len(errors), errors)
        self.assertIn("acceptance A1 cites no contract, security rule or (floor)", errors[0])
        self.assertIn("(deliverable) only on a presentation, governance or portability ticket", errors[0])
        self.assertEqual([], [e for e in result["errors"] if e.startswith("G01.md")])

    def test_ticket_naming_an_uninstalled_portability_skill_is_an_error(self):
        (self.skills / "adk-portability-planning").rename(self.root / "not-installed")
        code, result = self.lint()
        self.assertEqual(1, code)
        errors = "\n".join(result["errors"])
        self.assertIn("G01.md: skill 'adk-portability-planning' is not an installed skill", errors)
        self.assertIn("G01.md: docs path 'adk-portability-planning/references/principles.md' does not resolve", errors)

    def test_roll_up_lists_the_portability_goal_and_the_gate_waits_for_it(self):
        code, result = self.status()
        self.assertEqual(["G01", "G02"], result["ready"])
        code, result = self.status("--gate")
        reasons = "\n".join(result["gate"]["reasons"])
        self.assertIn("G01 is ready", reasons)
        self.assertNotIn("journey", reasons)

    def test_a_review_that_depends_only_on_the_portability_goal_needs_no_journey_goal(self):
        self.write(self.plan, PLAN.split("- goal: G02")[0] + """- goal: G02
  phase: 1
  type: presentation
  total: 2-3
  owner: Ana
  blocked_by: [G01]
```
""")
        self.write(self.tickets / "G02.md", "no front matter\n")
        code, schedule = self.run_script("check_schedule.py", "--plan", str(self.plan), "--json")
        self.assertEqual([], [p for p in schedule["problems"] if "journey" in p])
        self.edit(self.tickets / "G01.md", "status: ready", "status: verified_local")
        code, result = self.status("--gate")
        self.assertEqual([], result["gate"]["reasons"])
        self.assertEqual(0, code)


if __name__ == "__main__":
    unittest.main()
