---
goal: G05
title: Book, move and cancel exactly once after confirmation
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-operational-guardrails, adk-agent-security]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 6-10
  total: 10-16
  calendar_waits: none
owner: Dev A
status: blocked
---

# G05 Book, move and cancel exactly once after confirmation

## Outcome

Maya's move works end to end in tests: proposal, card data, confirm, one booking-API effect, status from the receipt. D2, D4, D5; invariants I2-I4.

## Scope

- In: `app/tools/propose.py` (`propose_booking`, `propose_move`, `propose_cancel`: ownership and input checks, canonical payload, 15-minute expiry, summary); `app/operations.py` operations table, migration and executor (atomic `proposed->dispatching` claim, recheck, idempotency key = operation ID, statuses `succeeded/failed/uncertain/partial/expired`); move path per G01 (atomic reschedule, or create-then-cancel, never cancel first); `scripts/reconcile_operations.py` and a one-page runbook.
- Out: HTTP endpoint wiring (G06), automated reconciliation (G13).
- Depth: Build at MVP depth; reconciliation is a manual script; the agent holds no write tool.

## Acceptance

- [ ] Concurrent double confirm produces one booking-API call; slot taken produces `failed` with fresh options
- [ ] Lost response produces `uncertain`; the reconcile script finds the appointment by key; move with failing cancel produces `partial` with both IDs
- [ ] Another customer's appointment ID returns `not_found` and model text claiming success without confirm causes no write

Verification: `pytest tests/test_operations.py tests/test_propose_tools.py` with the fake API and local Postgres (offline and local integration); one staging round trip after G03.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-confirmed-writes.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
