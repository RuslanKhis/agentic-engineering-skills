---
goal: G03
title: A customer books, moves or cancels an appointment after confirming the exact details
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-operational-guardrails, adk-agent-security]
blocked_by: [G01, G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, 1.5x new-to-ADK applied; includes 1 h handoff from Dev B
  hands_on: 7-10
  review_and_verify: 5-8
  total: 12-18
  calendar_waits: none
owner: Dev A
status: blocked
---

# G03 Book, move and cancel with customer confirmation

## Outcome

`propose_booking`, `propose_move` and `propose_cancellation` store proposal
records; only the gateway's `POST /proposals/{id}/confirm` executes the write,
once, and reports the booking API's receipt (D4, D5; I1–I4).

## Scope

- In: settle O4 (native reschedule? fees?) first; `assistant/proposals.py`
  (Postgres table, also a SQLite/in-memory variant for tests: id,
  customer_id, kind, canonical payload, hash, status
  pending/executing/succeeded/failed/uncertain/expired, expires_at, receipt);
  atomic claim; owner and expiry re-check; one API call, no automatic retry;
  reconcile-by-read for `uncertain`; outcome written to session state;
  `/decline` endpoint; instruction v2 lines for proposing.
- Out: idempotency keys in the booking API (G11), widget cards (G04),
  durable budgets (G10).
- Depth: MVP Build for writes. Floor: the model has no tool that writes;
  confirmation binds to the stored payload. Careful review: this is the
  authorization and write boundary.

## Acceptance

- [ ] Happy path for each kind: propose → confirm → one fake-API write → `succeeded` with receipt.
- [ ] Scripted model calls every tool in any order: zero writes reach the fake API without the confirm endpoint.
- [ ] Two concurrent confirms of one proposal → exactly one API call; both return the same receipt.
- [ ] Customer B confirming A's proposal → 404, no write.
- [ ] Fake API commits then times out → `uncertain`; reconcile finds the appointment → `succeeded`; not found → `failed`, no second write.
- [ ] Slot taken, outside cancellation window, expired proposal, appointment changed since proposal → no write, actionable message.

Verification: offline `pytest` with the fake booking API (configurable
timeouts, commit-then-timeout) and scripted model; staging API run only if
authorized.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-confirmed-writes.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
