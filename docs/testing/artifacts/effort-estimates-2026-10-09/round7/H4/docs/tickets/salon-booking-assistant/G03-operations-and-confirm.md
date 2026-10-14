---
goal: G03
title: A confirmed operation changes the booking exactly once
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 5-7
  review_and_verify: 3-4
  total: 8-11
  calendar_waits: none
owner: Dev A
status: blocked
---

# G03 A confirmed operation changes the booking exactly once

## Outcome

Implements D2, D4 and D5 and invariants I2, I3, I4 and I6. A stored proposal, once confirmed, produces at most one booking-API change, and its success text comes from the API response.

## Scope

- In and out: In: `app/operations.py` (table, statuses `pending → dispatching → done/failed/uncertain/expired`, atomic claim, 10-minute expiry); `confirm_operation(customer_id, operation_id)`, which re-checks ownership, policy and slot freshness and then dispatches with the G01 replay contract; reconciliation on read; write methods in `app/booking_client.py`. Out: HTTP routes (G04), model tools (G06), automatic reconciliation job (G16).
- Depth: Build. Review by Dev B (irreversible-effect code).

## Acceptance

- [ ] Confirm on a fresh, owned proposal creates one booking, and the result text is copied from the API response
- [ ] A double confirm, a retry after a timeout, and a restart while `dispatching` all give one API write. `uncertain` is never re-sent blind
- [ ] Another customer's operation ID gives not-found and no API call. A policy breach at 23 h 59 min is refused at confirm

Verification: Offline: `pytest tests/test_operations.py` with a fake API that times out after committing. Local Postgres in Docker or SQLite with a documented difference.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-operations-and-confirm.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
