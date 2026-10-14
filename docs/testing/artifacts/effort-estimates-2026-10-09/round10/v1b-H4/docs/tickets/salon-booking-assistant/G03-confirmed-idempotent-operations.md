---
goal: G03
title: Confirmed, idempotent operations
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-5
  review_and_verify: 2-4
  total: 6-9
  calendar_waits: none
owner: Dev A
status: blocked
---

# G03 Confirmed, idempotent operations

## Outcome

A booking change reaches the booking API only once, and only after the
customer confirms the exact details. Implements D2 and D3 and invariants I1
and I3 in ordinary code the model cannot reach.

## Scope

- In: `app/operations.py` `OperationService` with `propose(kind, payload,
  session_id) -> op` (canonical payload, SHA-256 hash, 10 min expiry,
  status `pending`), `confirm(op_id, session_id, payload_hash)` (atomic
  `pending→committing` claim, re-check expiry and owner session, call the
  client with `Idempotency-Key = op_id`, record `done / rejected(reason) /
  uncertain`), and `get(op_id, session_id)`. `operations` table migration
  (Postgres; SQLite locally) — additive only. The public `OperationService`
  interface is the one the chat API's confirm route will call.
- Out: lookup-based reconciliation and alerting (G07); tools that call
  `propose` (G04); HTTP routes.
- Depth: MVP. Build: atomic claim, payload binding, expiry. Floor: no write
  without confirm. Review is heavy on purpose (2–4 h): read the claim and the
  status transitions adversarially.

## Acceptance

- [ ] Confirm with the stored hash commits exactly once; the fake records 1 call.
- [ ] Double confirm and two concurrent confirms (real Postgres in Docker)
      produce 1 fake call; the second caller gets the first result.
- [ ] Confirm with a changed payload hash, another session, or after expiry
      is refused with no fake call.
- [ ] A commit timeout leaves the row `uncertain`, never `rejected` or `done`.
- [ ] No code path outside `confirm` calls the client's write methods (test
      greps the import graph or asserts via fake).

Verification: `pytest tests/test_operations.py` offline plus the Postgres
concurrency test (local integration, `docker compose up db`).

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-confirmed-idempotent-operations.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
