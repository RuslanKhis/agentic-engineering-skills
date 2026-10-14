---
goal: G01
title: The team knows exactly what the booking API does, behind one tested interface
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 The team knows exactly what the booking API does, behind one tested interface

## Outcome

Every later goal codes against one `BookingPort` and a scriptable fake instead
of guessing the API. Answers Q6 and decides D5 (move semantics).

## Scope

- In: `docs/architecture/booking-api-contract.md` from the booking API's code;
  `app/booking/port.py` (protocol, closed result type, domain records for
  appointment, slot, proposal and operation); in-memory fake with scripted
  outcomes; offline tests.
- Out: the real HTTP adapter and any change to the booking API (G02 owns both).
- Depth: MVP. No network calls; fake only. Credentials not touched.

## Acceptance

- [ ] A1 The contract note lists each endpoint used (salons, services, stylists, availability, list by customer, get by ID, create, reschedule or equivalent, cancel): request, response, error codes, auth, and whether idempotency keys, atomic reschedule and lookup by client reference exist.
- [ ] A2 The fake implements every port operation and can be scripted per call to return: success, rejection with reason, timeout, 429, 401, malformed payload, and "committed but response lost".
- [ ] A3 The port maps every scripted outcome to a closed result type (`ok`, `rejected`, `transient`, `unknown_outcome`, `auth_error`, `invalid_response`); malformed payloads never raise into callers. Offline tests cover each.
- [ ] A4 D5 is decided and written into the design: atomic reschedule (existing or to be added) or book-then-cancel with a `partial` state.

Verification: `pytest tests/booking/` offline; no google.adk import needed.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
