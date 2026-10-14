---
goal: G01
title: Booking API contract and fake
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-3.5
  review_and_verify: 1-2
  total: 3-5.5
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Booking API contract and fake

## Outcome

The team knows exactly how the assistant reads and writes bookings, and every later goal can test offline against a faithful fake. Settles A6 and A7; implements the client side of D5.

## Scope

- In: `docs/architecture/booking-api-contract.md` (endpoints for salons, services, stylists, availability, create, reschedule, cancel and list-by-customer; auth; error codes; idempotency-key support; cancellation-window behaviour; lookup able to find a booking by customer and slot); `app/booking_client.py` with typed methods, per-call timeouts and error classes (`SlotTaken`, `OutsidePolicyWindow`, `NotFound`, `Transient`, `Uncertain`); `tests/fakes/booking_api.py`, an in-process fake with fixtures for the pilot salon and one other salon (3 stylists each) and two customers.
- Out: Model-facing tools (G02), operations and confirmation (G04a), staging calls (G10). Fixtures for the remaining salons come with G12; the reschedule client method is documented here but first used by G06 (phase 2).
- Depth: Build. Floor: the booking-API key comes from the environment and appears in no file or log. Retries in the client only for reads; writes never retried here (D5 owns that).
- Notes: Read the booking API's own code, docs or OpenAPI file (the team owns it). Where it lacks an idempotency key, record the lookup used for reconciliation. Send the W2 request to the salon owner on day 1.
- Execution scope: Local only; reading the booking API's source or docs is within the team's own repositories.

## Acceptance

- [ ] The contract note answers A6 and A7 with the endpoint or code line that shows it; the design's A6/A7 rows are updated to confirmed or corrected.
- [ ] Client tests against the fake: each call's happy path; a read timeout retried at most twice; a write timeout raises `Uncertain` and is not retried; a 429 on a write raises without retry.
- [ ] No test or log line contains the API key; `grep -r` for the key value in the repo and test output finds nothing.

Verification: Offline: `pytest tests/test_booking_client.py` (no google.adk import needed).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
