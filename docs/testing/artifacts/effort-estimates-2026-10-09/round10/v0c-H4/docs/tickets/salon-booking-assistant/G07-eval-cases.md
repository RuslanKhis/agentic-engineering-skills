---
goal: G07
title: Thirty labelled conversations describe what a good assistant does
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-security]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev A
status: blocked
---

# G07 Thirty labelled conversations describe what a good assistant does

## Outcome

About 30 labelled conversations in `evals/cases/` covering book, move, cancel, clarification, out-of-scope, policy window, time-zone/relative dates and adversarial asks, each with the expected tool calls, proposal (or none) and forbidden effects. Feeds D12. Dev A writes them because they know the salons' real requests; 1 h handoff from Dev B on tool names and case format.

## Scope

- In:
  - Case format agreed with Dev B (initial turn, fake API fixtures, expected tool trajectory, expected proposal fields, forbidden calls)
  - ~30 cases: ≥ 6 book, ≥ 5 move, ≥ 4 cancel, ≥ 4 clarification, ≥ 3 policy/time, ≥ 4 adversarial, ≥ 2 out of scope
  - Fixtures for the fake booking API per case
- Out: Running and scoring (G08); Production-derived cases (G12)
- Depth: Build at MVP depth (development set only; no holdout split yet).
- Supporting skills, purpose: adk-agent-security: adversarial cases (other customer's appointment, "confirm it for me", "cancel everything")

## Acceptance

- [ ] Every case loads and validates against the format schema
- [ ] Each case names its forbidden effects (e.g. no write call, no other customer's data)
- [ ] A second developer has reviewed the labels of the adversarial and policy cases

Verification: `pytest tests/evals/test_case_format.py` offline.

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-eval-cases.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
