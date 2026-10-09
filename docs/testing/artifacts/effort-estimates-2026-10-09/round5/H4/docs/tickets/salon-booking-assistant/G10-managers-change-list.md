---
goal: G10
title: Managers' change list, runbook and briefing
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: [G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1
  total: 4-5
  calendar_waits: salon managers briefed (request the slot on day 1)
  wait_days: 0-1
owner: Dev B
status: blocked
---

# G10 Managers' change list, runbook and briefing

## Outcome

Salon managers see every assistant change daily, uncertain ones first, and know how to resolve them. I4 recovery, D5, O4. Route and rationale: [plan, G10](../../plans/salon-booking-assistant.md#g10--managers-change-list-runbook-and-briefing).

## Scope

- In: daily list per salon from `booking_operations`; runbook for an uncertain operation; 20-minute briefing
- Out: dashboards (G13)
- Depth: build minimal; read-only over the assistant's own tables

## Acceptance

- [ ] A seeded uncertain operation appears first in the list
- [ ] The runbook resolves it in a dry run; managers have been briefed
- [ ] The list contains no message text

Verification: local with seeded rows; briefing with the salons.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-managers-change-list.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
