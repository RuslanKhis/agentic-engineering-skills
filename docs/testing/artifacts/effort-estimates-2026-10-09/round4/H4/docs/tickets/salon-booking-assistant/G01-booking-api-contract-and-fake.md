---
goal: G01
title: Booking API contract and fake
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Booking API contract and fake

## Outcome

Answers open decisions O2 to O5 behind D2 and D3. Produces a contract document and an in-process fake that every other goal tests against.

## Scope

- In:
  answer five questions from the booking API's source or docs:
  1. Does it accept idempotency keys, and how long does it retain them?
  2. Is there an atomic reschedule endpoint?
  3. Can an appointment be looked up by customer and slot, or by key?
  4. Where are cancellation-window and lead-time rules enforced?
  5. Which error codes does it return?
  Write `docs/booking-api-contract.md`, including the `Proposal` card schema that G03 and G05 share. Write `tests/fake_booking_api.py` with scripted failure modes.
- Out: Any agent code.
- Depth: Discovery, bounded to the five questions. It stops when each question is answered from source or a staging call, or marked unsupported with the workaround the design names (D3).
- Implementation route: Plain Python, no ADK. Proposed `app/booking_client.py` interface: `list_salons()`, `list_services(salon_id)`; `search_slots(salon_id, service_id, date_from, date_to, stylist_id=None)`; `list_appointments(customer_id)`; `book(customer_id, slot_id, key)`, `reschedule(appointment_id, slot_id, key)`, `cancel(appointment_id, key)`; `find_operation(key)`, or `find_appointment(customer_id, slot_id)` when keys are unsupported.
- Prerequisites: The booking API source or docs, and staging credentials Dev A already holds. No new grant is needed.
- Supporting skills: None
- Execution scope: Local code, plus booking-API staging with test customers only.

## Acceptance

- [ ] The contract document answers O2 to O5 and defines the proposal card schema.
- [ ] The fake simulates slot taken (409), timeout after commit, timeout before commit and policy rejection.
- [ ] The contract tests pass against the fake and once against staging, with the staging run recorded.
- [ ] No staging call touches a real customer.

Verification: Offline `pytest tests/test_booking_contract.py` against the fake. One authorised, recorded run against booking-API staging with test customers.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
