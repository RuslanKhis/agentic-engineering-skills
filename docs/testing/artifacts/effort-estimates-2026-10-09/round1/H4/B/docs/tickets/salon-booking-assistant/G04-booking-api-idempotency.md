---
goal: G04
title: Idempotency keys in the booking API (only if G01 finds none)
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 1.5-3
  review_and_verify: 2.5-5
  total: 4-8 (0 if not needed)
  calendar_waits: the booking API's normal release
owner: Dev B (Dev A reviews)
status: blocked
---

# G04 Idempotency keys in the booking API (only if G01 finds none)

## Outcome

A replayed confirm can never create a second appointment. D4, invariant I3.

## Scope

- In: Booking API repository: `Idempotency-Key` on create, reschedule and cancel; key table with payload hash, unique constraint and 7-day retention; lookup by key for reconciliation.
- Out: Client-side changes (G03/G05).
- Depth: Build, only if G01 records that keys are missing; otherwise close as not needed.

## Acceptance

- [ ] Same key and payload twice: one appointment, identical response
- [ ] Same key with a changed payload: 409, no effect
- [ ] Lookup by key returns the original result

Verification: Booking API test suite plus a staging replay test (authorised live, staging).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-booking-api-idempotency.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
