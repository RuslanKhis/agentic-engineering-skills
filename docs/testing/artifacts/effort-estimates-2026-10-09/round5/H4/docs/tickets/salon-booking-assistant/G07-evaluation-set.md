---
goal: G07
title: Evaluation set of 25–30 conversations
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-security]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 1-2
  total: 6-10
  calendar_waits: none
  wait_days: 0
owner: Dev B
status: blocked
---

# G07 Evaluation set of 25–30 conversations

## Outcome

A measured baseline for the agent's decisions; settles O6. D1. Route and rationale: [plan, G07](../../plans/salon-booking-assistant.md#g07--evaluation-set-of-2530-conversations).

## Scope

- In: `evals/` cases (book, move, cancel, ambiguous dates, unknown stylist, out of hours, cancellation window, three injection attempts) and a runner against the fake asserting tool trajectory and arguments; write cases use the planned `propose_*` names
- Out: CI gate (G12)
- Depth: build; run by hand before each deploy; ≤ 3 repeats per case

## Acceptance

- [ ] Runner reports pass rate per category; baseline recorded with model ID and prompt SHA
- [ ] A failed or missing run is reported as missing, not as a pass
- [ ] Injection cases never produce a proposal for another customer

Verification: local runner with the pinned model (bounded live model calls).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
