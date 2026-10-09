---
goal: G03
title: Real booking API client against staging
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 1.5-3
  review_and_verify: 2.5-4
  total: 4-7
  calendar_waits: none
owner: Dev A
status: blocked
---

# G03 Real booking API client against staging

## Outcome

The read tools and the executor talk to the staging booking API through the same interface as the fake. D4 (transport).

## Scope

- In: `app/booking_client.py`: `BookingClient` protocol, HTTP implementation with deadlines (5 s reads, 10 s writes), retries on reads and keyed writes only, error mapping to `slot_unavailable`, `outside_cancellation_window`, `not_found`, `unavailable`, `uncertain`; shared contract test suite for fake and real.
- Out: Operation record and executor (G05); idempotency in the API (G04).
- Depth: Build. Service credential from Secret Manager or environment, never in code or logs.

## Acceptance

- [ ] Fake and HTTP clients pass the same contract suite; staging create/cancel round trip on a test customer succeeds
- [ ] A timed-out write returns `uncertain` and is never retried without its idempotency key
- [ ] No credential appears in code, logs or test output

Verification: `pytest tests/contract -m staging` (authorised live, staging only, test customer).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-booking-api-client.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
