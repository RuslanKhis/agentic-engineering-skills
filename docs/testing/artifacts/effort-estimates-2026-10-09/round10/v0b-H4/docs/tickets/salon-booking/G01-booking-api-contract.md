---
goal: G01
title: We know exactly how the booking API writes and how to verify a signed-in customer
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 1
  total: 3-4
  calendar_waits: none
owner: Dev B
status: ready
---

# G01 We know exactly how the booking API writes and how to verify a signed-in customer

## Outcome

A one-page decision record that settles assumptions A2 and A3 in the design
and fixes the domain types every other goal codes against. Decides the route of
D3 and D4. Discovery goal; stops when every question below has an answer or a
named owner.

## Scope

- In: read the booking API's code or docs (not production data) and the
  website's sign-in. Answer: idempotency keys or request IDs on book, move,
  cancel? Reschedule endpoint, atomic or not? Lookup of a customer's
  appointments by salon/service/start? Error codes for "slot taken", "too
  late", "not found"? Sandbox URL and credential owner? Time zone of returned
  times? Can the API accept the customer's token instead of a service
  credential? How does the site issue and sign customer sessions, and which key
  verifies them? Write `app/domain.py` (proposed) with `Salon`, `Service`,
  `Slot`, `Appointment`, `OperationKind` types and a `BookingClient` protocol.
  Send the W1 request (plan) on the same day.
- Out: any adapter code (G03), any token verification code (G04).
- Depth: discovery only; no credentials copied into the repository.

## Acceptance

- [ ] `docs/architecture/salon-booking-api-contract.md` answers each question above with a source (file, endpoint doc, or person and date)
- [ ] A2 and A3 in the design are updated to confirmed or changed, and dependent decisions D3/D4 marked accordingly
- [ ] `app/domain.py` type-checks and contains no secrets or sample personal data

Verification: offline — `python -m py_compile app/domain.py`; review by Dev A and Dev C (they consume it).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G01-booking-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
