---
goal: G04a
title: Confirmed operations core (propose, confirm, dispatch, reconcile)
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails, adk-agent-security]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3.5-5.5
  review_and_verify: 2.5-3
  total: 6-8.5
  calendar_waits: none
owner: Dev A
status: blocked
---

# G04a Confirmed operations core (propose, confirm, dispatch, reconcile)

## Outcome

Any booking change the assistant proposes becomes real only through the customer's confirm click, and a retry, double click or lost response never makes two changes. Implements D4, D5, I2 and I3 once, for every operation kind. New in revision 2: split out of the old G04 so the booking tool and the cancel goal can proceed in parallel; same work and hours as before.

## Scope

- In: `app/operations.py`: operations table (SQLite locally, Postgres-compatible SQL) with `operation_id`, `customer_id`, kind, canonical payload and hash, status, expiry, receipt; `create_pending(kind, payload, customer_id)` for the propose tools; atomic claim on confirm; dispatcher for `create` and `cancel` via G01's client; lease of 60 s for `dispatching`; reconciliation by lookup for `uncertain`. `app/api/operations.py`: `POST /operations/{id}/confirm` and `GET /operations/{id}`, both requiring `verified_customer()` (tests use a fixture dependency until G03 lands).
- Out: Model-facing propose tools (G04, G05), widget button (G07), staging drill (G10), automated background reconciliation (G18).
- Depth: Build (MVP: idempotent writes). Floor: the model holds no tool that writes to the booking API. Here reconciliation runs on the next status read.
- Execution scope: Local only.

## Acceptance

- [ ] A pending `create` operation causes zero writes on the fake until confirm; after confirm exactly one booking exists and `GET` shows the receipt.
- [ ] Double confirm, two concurrent confirms, and a fake that commits then drops the response each end with one booking; the dropped-response case shows `uncertain` then `succeeded` after lookup, with no second create call; an unreadable receipt is treated as `uncertain`.
- [ ] Confirm by another customer → 404 and no write; confirm after expiry or with a changed payload → refused and no write; slot taken at confirm → `failed: slot_taken`, no write.

Verification: Offline: `pytest tests/test_operations.py` with the G01 fake (no model needed).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04a-operations-core.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
