---
goal: G02
title: A booking, move or cancellation happens once, and only after the customer confirms
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design (propose tools), adk-operational-guardrails (confirmation bound to stored details)]
blocked_by: [G00]
phase: 1
profile: MVP or pilot
estimate: 14-20 h
suggested_owner: Dev A (knows the booking API)
status: blocked
---

# G02 A booking, move or cancellation happens once, and only after the customer confirms

## Outcome

Maya's move runs only after she presses Confirm on the stored proposal, and runs once despite double clicks or a lost reply. Implements D2, D3; invariants I2, I3, I4.

## Scope

- In: propose_booking/propose_move/propose_cancel (validate against fresh reads, insert a proposed ledger row, 10-min expiry); app/operations/ledger.py (unique operation_id, states proposed→confirmed→dispatched→succeeded/failed/uncertain, owner customer_id); app/operations/executor.py (atomic claim, dispatch with idempotency key if G00 found one, reconcile by lookup before any retry, partial-move flag); write methods in client.py and fake.py.
- Out: Widget and HTTP routes (G04), limits (G06).
- Depth: Build: idempotent writes, bounded retry only after reconciliation, uncertain and partial outcomes logged for the front desk. Payments not in scope.

## Acceptance

- [ ] Against the fake API: a whole conversation without confirm makes zero write calls; a double confirm makes exactly one create.
- [ ] Create timeout → lookup → exactly one booking or state uncertain; 409 → failed:conflict with fresh slots offered; create-ok/cancel-fail move leaves both bookings recorded and flagged.
- [ ] Confirming an operation owned by another customer is denied with no API call.

Verification: pytest tests/test_operations.py (offline); one book, move and cancel on the staging API (local integration).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-confirmed-writes-exactly-once.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
