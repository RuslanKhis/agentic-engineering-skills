# designer-tickets-get-journey-goal-and-lint: what the fixture holds

Base: claims-docs (discovery brief, design C1-C5 with SB01/SB03/SB05, plan). Overlay:
`docs/plans/claims.md` with four implementation goals G01-G04 and a production-approval
presentation G05 whose `blocked_by` is [G01, G02, G03, G04]; no journey goal. A "Web stack and
companion skills" table pins shadcn (shadcn@3.4.2) but gives react-router the pin "to be chosen";
G03 names both as companion skills and `docs/design/DESIGN.md` as its design system. There is no
AGENTS.md and no `docs/tickets/` directory.

What the helpers say on the composed workspace (fixture author's run):
- `check_schedule.py --plan docs/plans/claims.md` reports PROBLEM: "G05 presents built work but no
  journey goal comes before it; add a goal of type journey (primary skill adk-agent-evaluation) ..."
- After the agent writes tickets, `check_tickets.py` would warn for G03: "companion react-router
  has a row but no pin" (a warning the agent may leave and must report).

Assertion map: A1 a new journey goal (type journey, primary adk-agent-evaluation) inserted before
the presentation, the presentation now depending on it, in the schedule block and the goals table.
A2 one ticket file per goal under docs/tickets/claims/ with type, touches and pass_to_pass; the
agent has no shell, so it can only name `check_tickets.py --tickets docs/tickets/claims --project .`
and say it was not run (or lint by hand against the template). A3 errors fixed (as far as the agent
can check by reading), the react-router pin warning reported.

Original context: "A pilot plan with four implementation goals and a production-approval
presentation goal that depends on them directly; no journey goal exists. The schedule block records
goal types."
