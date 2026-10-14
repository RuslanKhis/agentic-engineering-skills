---
goal: G04
title: A confirmed booking is created exactly once and the card shows the real result
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 7-10
  review_and_verify: 3-5
  total: 10-15
  calendar_waits: none
owner: Dev A
status: proposed
---

# G04 A confirmed booking is created exactly once and the card shows the real result

## Outcome

When Maya presses Confirm on a booking card, the booking API creates one
appointment, even with double clicks, timeouts or a restart, and the card
shows the API's receipt (D4, D5, I2, I3, I4).

## Scope

- In: Postgres tables for proposals, operations and allowances (local
  Postgres in tests); `/proposals/{id}/confirm` and `/operations/{id}`
  routes; executor that re-checks ownership, expiry, content hash and slot,
  records `sent` before calling the API, sends the proposal ID as
  idempotency key (or the agreed fallback from G01), and reconciles
  `uncertain` by lookup before any retry; card status from the operation
  record. The `propose_booking` tool from G02 writes into this store once
  both are merged.
- Out: move and cancel (G05), the widget (G06).
- Depth: build; careful review of the write path.

## Acceptance

- [ ] Confirm once → one create call, operation `confirmed` with receipt.
- [ ] Double confirm and concurrent confirm → one create call; both return
      the same operation.
- [ ] Commit-then-lost-response → `uncertain`, reconciled to `confirmed` by
      lookup, no second create.
- [ ] Changed or expired proposal, or slot taken → refused, zero writes.
- [ ] Process restart with an operation in `sent` → next status read
      reconciles it.

Verification: offline tests against the G01 fake and a local Postgres.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-confirmed-booking-write.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
