---
goal: G05
title: Customer moves or cancels their appointment
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: [G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 2-3
  total: 5-8
  calendar_waits: none
  wait_days: 0
owner: Dev A
status: blocked
---

# G05 Customer moves or cancels their appointment

## Outcome

Maya's journey (move Thursday to Saturday) works end to end locally; I1–I4 for move and cancel. Route and rationale: [plan, G05](../../plans/salon-booking-assistant.md#g05--customer-moves-or-cancels-their-appointment).

## Scope

- In: `propose_move`, `propose_cancel`, executor branches; cancellation-window errors surfaced from the API
- Out: guest flows (G17)
- Depth: build, reusing G04's operation record; tool count stays 6

## Acceptance

- [ ] Move and cancel each change exactly one appointment after confirm
- [ ] Slot taken between propose and confirm → `failed` and the agent offers alternatives
- [ ] Another customer's appointment ID → refused without any call to the write endpoint

Verification: offline `pytest`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-move-and-cancel.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
