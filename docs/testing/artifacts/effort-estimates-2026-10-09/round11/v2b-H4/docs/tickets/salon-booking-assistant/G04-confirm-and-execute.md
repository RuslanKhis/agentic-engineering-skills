---
goal: G04
title: Pressing Confirm changes the appointment exactly once, or says honestly that it is being checked
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails, adk-memory-architecture]
blocked_by: [G01, G03]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 5-9
  review_and_verify: 4-6
  total: 9-15
  calendar_waits: none
owner: Dev A
status: blocked
---

# G04 Pressing Confirm changes the appointment exactly once, or says honestly that it is being checked

## Outcome

Postgres `ProposalStore` and operations table, and the confirm/decline/status
service behind the public JSON contract. Implements D2, D4, D5 and D6's app
tables. Review is heavy: this is the only write path. Builds on the agent's
`ProposalStore` interface and tools (A9 is a Runner test of them).

## Scope

- In: `app/operations/` (store, confirm service, reconciliation-on-demand), migrations, tests against local PostgreSQL and the fake port.
- Out: HTTP routing and JWT (gateway ticket), scheduled reconciliation job (phase 2), the real adapter.
- Depth: MVP. Idempotency key = proposal ID. No blind write retries.

## Acceptance

- [ ] A1 Confirm by the owning customer rechecks owner, `pending` status and expiry, inserts an operation `executing`, calls the port once with `Idempotency-Key = proposal_id`, and records `succeeded` with the booking API's receipt.
- [ ] A2 Confirm by any other customer returns not-found and makes no port call.
- [ ] A3 Two concurrent confirms of one proposal make exactly one port call; both return the same receipt (row lock and state transition test).
- [ ] A4 Booking API rejects because the slot is taken or policy forbids: operation `failed` with reason; no appointment created; result says the slot has gone. A 401/403 or 429 on the write is not retried automatically: the proposal stays `pending`, the customer may press Confirm again (same key), and a 401/403 logs at ERROR for the developer.
- [ ] A5 Expired proposals (> 10 min, including ones left by a turn that failed after the tool ran) and proposals whose appointment changed since proposal (rechecked by reading it first) are refused with "please review again" and no write.
- [ ] A6 Commit-then-lost-response, timeout, or a crash after the call and before recording leaves the operation `unknown`/`executing`; one lookup by client reference runs on the status call and settles it; no write with a new key ever happens.
- [ ] A7 Move: with atomic reschedule, one port call; with book-then-cancel, new-booked-old-not-cancelled ends `partial`, shows both appointments, and appears in the reconciliation list.
- [ ] A8 After a process restart (local PostgreSQL), status and repeat confirm return the recorded result.
- [ ] A9 The agent learns the outcome from the operations store through `list_my_appointments`/a status read, so a failed session-state write cannot hide it (Runner test).
- [ ] A10 Store unavailable at confirm: 503 and no port call.
- [ ] A11 A lock timeout, serialization failure or constraint error at confirm returns a retryable 503, leaves the proposal `pending`, and makes no port call.

Verification: `pytest tests/operations/` with local PostgreSQL (docker) and the fake port; offline.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-confirm-and-execute.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
