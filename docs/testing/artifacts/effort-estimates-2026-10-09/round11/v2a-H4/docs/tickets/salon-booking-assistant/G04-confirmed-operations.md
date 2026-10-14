---
goal: G04
title: A clicked confirmation books, moves or cancels exactly once
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G01]
mentions_only: [W1]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 5-7
  review_and_verify: 3-4
  total: 8-11
  calendar_waits: none
owner: Dev A
status: ready
---

# G04 A clicked confirmation books, moves or cancels exactly once

## Outcome

The operations service behind the propose tools and the confirm endpoint:
pending proposals, atomic claim, recheck, idempotent dispatch and
reconciliation, against a fake write adapter. Implements D3, D4, D5, I2–I4.

## Scope

- In: `operations` table and store, the operations interface used by the
  propose tools, confirm and status routes as a router (mounted later),
  notice-window policy from config (values arrive with W1; placeholders until
  then), reconciliation, fake write adapter.
- Out: the real booking API write adapter, operator controls, widget. G01's
  findings arrive before this starts; the adapter interface keeps the
  idempotency key optional so either D6 outcome fits.
- Depth: Build; review as a money-like write path (adversarial cases).

## Acceptance

- [ ] A1 Book: `propose_booking` stores a pending operation (owner from trusted
  state, canonical payload, expires in 10 min); confirm by the owner → one
  adapter write with key = `operation_id` → `succeeded` with reference.
- [ ] A2 Confirm rechecks: expired → `expired`, no call; slot taken → 
  `rejected`; price, duration or appointment changed or already cancelled →
  `changed`, customer must confirm a new proposal.
- [ ] A3 Proposing or confirming on another customer's appointment or
  operation → refused; adapter write count 0.
- [ ] A4 Adapter commits then times out → `uncertain`; reconciliation runs
  before any re-dispatch and resolves to `succeeded` without a second write;
  if lookup fails it stays `uncertain` and is listed for the operator.
- [ ] A5 Double click, two tabs, or confirm after a restart → one adapter
  write (conditional update claims `pending → dispatching`); a restart that
  leaves `dispatching` is treated as `uncertain`; later confirms return the
  stored result.
- [ ] A6 Confirm executes only the stored payload; a request body naming
  another slot or salon is ignored.
- [ ] A7 No bulk operation exists; "cancel all" gives one proposal per
  appointment, and confirming one executes only that one.
- [ ] A8 Move or cancel inside the salon's notice window → refused at propose
  and rechecked at confirm, with the salon's phone number; no write.
- [ ] A9 4xx validation → `rejected`, no retry; 429/503 with no effect → up to
  2 retries within a 10 s deadline, then `failed`; ambiguous → A4.
- [ ] A10 Adapter credential refused (401/403) → `failed`, operator log
  event, no retry loop.
- [ ] A11 Move is one adapter call; a failed move leaves the original
  appointment untouched and the customer is told it is still booked.
- [ ] A12 Operations store unavailable at propose or confirm → "can't make
  changes right now"; nothing dispatched without a durable record.
- [ ] A13 The adapter commits but recording `succeeded` fails → the record
  stays `dispatching`, is read back as `uncertain` and reconciled (A4 path)
  without a second write.
- [ ] A14 A serialisation or constraint error on the claim → the claim is
  retried once, then the confirm returns "try again"; a lost commit
  acknowledgement → the record is re-read before any dispatch; nothing is
  dispatched without a committed claim.

Verification: offline with local Postgres and the fake adapter, including a
concurrency test and a killed-process test.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-confirmed-operations.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
