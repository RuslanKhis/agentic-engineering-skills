---
goal: G04
title: Customer books with one confirmed click
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails, adk-tool-interface-design, adk-agent-security]
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

# G04 Customer books with one confirmed click

## Outcome

A customer can ask for a booking, see an exact proposal and make it real only by confirming it, and a retry or double click never makes two bookings. Implements D4, D5, I2, I3 for the create operation; the machinery G05 and G06 reuse.

## Scope

- In: `app/operations.py`: operations table (SQLite locally, Postgres-compatible SQL) with `operation_id`, `customer_id`, kind, canonical payload and hash, status, expiry, receipt; atomic claim on confirm; lease of 60 s for `dispatching`; reconciliation by lookup for `uncertain`. `app/tools/propose.py`: `propose_booking` (validates salon, service, stylist, ISO start; rechecks the slot; stores a pending proposal; returns the summary and `operation_id`). `app/api/operations.py`: `POST /operations/{id}/confirm` and `GET /operations/{id}`, both requiring `verified_customer()` from G03 (tests use a fixture dependency until G03 lands).
- Out: Cancel (G05), move (G06), widget button (G07), staging live check (G06).
- Depth: Build (MVP: idempotent writes). Floor: the model holds no tool that writes to the booking API. Automated background reconciliation is G18; here reconciliation runs on the next status read.
- Execution scope: Local only.

## Acceptance

- [ ] Scripted model proposes a booking; the fake booking API records zero writes until confirm; after confirm exactly one booking exists and `GET` shows the receipt.
- [ ] Double confirm, two concurrent confirms, and a fake that commits then drops the response each end with one booking; the dropped-response case shows `uncertain` then `succeeded` after lookup, with no second create call.
- [ ] Confirm by another customer → 404 and no write; confirm after expiry or with a changed payload → refused and no write; slot taken at confirm → `failed: slot_taken`, no write.

Verification: Offline: `pytest tests/test_operations.py tests/test_propose_booking.py` with the G01 fake and a scripted model.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-book-with-confirmation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
