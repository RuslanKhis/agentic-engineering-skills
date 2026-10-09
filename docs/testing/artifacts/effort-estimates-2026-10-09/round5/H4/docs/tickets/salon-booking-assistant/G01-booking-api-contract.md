---
goal: G01
title: Booking API contract confirmed
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: staging booking API credentials from its owner
  wait_days: 0-1
owner: Dev B
status: ready
---

# G01 Booking API contract confirmed

## Outcome

Settle O1 (customer token), O2 (idempotency) and O3 (staging) so D3 and D5 stop being provisional. Implements the evidence behind D3, D5. Route and rationale: [plan, G01](../../plans/salon-booking-assistant.md#g01--booking-api-contract-confirmed).

## Scope

- In: booking API docs/code; bounded **staging-only** calls; `docs/architecture/booking-api-contract.md`; final `BookingClient` protocol signatures
- Out: any production call; the agent itself (G02)
- Depth: discovery; writes only to staging test salons; stop at 6 hours or when O1–O3 are answered

## Acceptance

- [ ] Contract doc answers O1–O3 with request/response excerpts and no secrets
- [ ] A recorded decision for D5: idempotency-key replay or lookup-before-retry
- [ ] No call is made to the production booking API

Verification: authorized live calls against the staging booking API, listed with results.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
