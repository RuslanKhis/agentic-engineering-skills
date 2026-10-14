---
goal: G04
title: Confirming a card changes the appointment exactly once, or says honestly that it is checking
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 3-4
  total: 8-12
  calendar_waits: none
owner: Dev A
status: blocked
---

# G04 Confirming a card changes the appointment exactly once, or says honestly that it is checking

## Outcome

`POST /operations/{id}/confirm` (ordinary code, no model) claims the proposal atomically, rechecks owner, expiry, 24-h window and slot, calls the booking API with `Idempotency-Key = operation_id`, stores the receipt and writes `last_operation` to the session. Implements D2 (commit side), D3, D11; invariants I1–I5.

## Scope

- In:
  - `app/api/confirm.py` and write methods in `app/booking/client.py` (write credential only here)
  - State machine proposed → confirming → succeeded / failed / uncertain, one transaction per transition, against `OperationsStore` from D3 (test rows inserted directly if G03 has not merged)
  - Timeout/5xx after send → `uncertain`; up to 3 lookups by key; otherwise left for the runbook
  - Runbook section in `docs/runbook.md`: listing and resolving `uncertain` operations
- Out: Background reconciler (G14); UI (G06)
- Depth: Build: at-most-once and recheck are MVP floor for writes. Deferred: automatic reconciliation (G14).
- Supporting skills, purpose: adk-operational-guardrails: confirmation bound to the stored proposal and rechecked before execution

## Acceptance

- [ ] Double confirm (two concurrent requests) → one booking API call, same receipt to both
- [ ] Booking API commits then the reply is lost → status `uncertain`, lookup finds the appointment, status `succeeded`, no second create
- [ ] Slot taken (409), expired proposal, inside 24 h, or another customer's session → no write, clear reason
- [ ] Restart between claim and send → no duplicate after restart (operation remains `confirming` and is resolved by lookup)

Verification: Offline `pytest tests/confirm` with the fake API simulating lost replies and 409s; local integration with Docker Postgres and a process restart. Careful review of the claim transaction.

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-confirm-executor.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
