---
goal: G03
title: Every booking change goes through one ledgered, idempotent operation
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6.5-9.5
  review_and_verify: 3-5
  total: 9.5-14.5
  calendar_waits: none
owner: Dev B
status: blocked
---

# G03 Every booking change goes through one ledgered, idempotent operation

## Outcome

Plain Python service `assistant/booking/` (no ADK) with `book`, `move` and
`cancel`. Each is keyed by `operation_id` with a canonical payload hash and
written to `assistant.operations` before dispatch (D4, I3, I4). Includes
0.5 h of handoff from G01's note.

## Scope

- In: a ledger table and migration, and state transitions proposed →
  dispatched → succeeded / failed / uncertain / partial. Uses the API
  idempotency key if G01 found one. Otherwise timeouts become `uncertain` and
  `reconcile(operation_id)` lists the customer's appointments, never resending
  blindly. Move uses the atomic reschedule, or create-new-then-cancel-old with
  `partial` on a cancel failure. Errors (`slot_taken`,
  `outside_cancellation_window`, `not_found`, `forbidden`) are mapped to
  typed results.
- Out: the agent tools and confirmation (G04). Automated background
  reconciliation is deferred to G14 and runs manually through the runbook for
  now.
- Depth: MVP build for reversible writes; the floor is no write without a
  ledger row first.

## Acceptance

- [ ] Fake API: the same `operation_id` dispatched twice gives one create and the second call returns the stored result.
- [ ] Fake API: provider commits, then the response is lost. The state is `uncertain`, `reconcile` finds the appointment, the state becomes `succeeded`, and there is no second create.
- [ ] Fake API: the same `operation_id` with a changed payload is rejected without a dispatch.
- [ ] Move fallback: create succeeds and cancel fails. The state is `partial` and both appointment IDs are recorded.
- [ ] Postgres unavailable: no dispatch happens.
- [ ] Staging: one book, move and cancel on the test customer, each with its ledger row (live, authorised test customer).

Verification: `pytest tests/booking` offline with the fake API and a local
Postgres container. Then a bounded staging run.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-booking-write-service.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
