---
goal: G04
title: Pressing Confirm makes exactly one change in the booking system
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G03, G05]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev A
status: blocked
---

# G04 Pressing Confirm makes exactly one change in the booking system

## Outcome

`POST /operations/{id}/confirm` runs the stored operation once (D3, D4, D5). Implements I2 and I3.

## Scope

- In: Executor in `assistant/operations.py`: atomic claim `pending→executing`; `op_id` as `Idempotency-Key`; no resend after dispatch
- In: Timeout → `uncertain` → one reconciliation lookup within 60 s; log-based alert on unresolved operations
- In: Route mounted on the G05 gateway router; the caller must own the operation; `GET /operations/{id}` returns status
- Out: Out: scheduled reconciliation job (G13)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] Two concurrent confirms → one API call, and both callers see the same final status
- [ ] Timeout after commit → `uncertain`, then `succeeded` by lookup, with no second write
- [ ] Another customer's confirm → 404; expired → 410; nothing is sent in either case

Verification: offline `pytest tests/test_execute.py` against the fake, with concurrency and timeout cases.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-confirmed-execution.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
