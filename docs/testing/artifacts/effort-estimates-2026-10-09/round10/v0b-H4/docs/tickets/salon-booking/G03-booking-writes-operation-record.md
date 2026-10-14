---
goal: G03
title: A confirmed booking, move or cancellation happens exactly once, even after a timeout
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 3-5
  total: 9-14
  calendar_waits: none
owner: Dev B
status: blocked
---

# G03 A confirmed booking, move or cancellation happens exactly once, even after a timeout

## Outcome

The real booking-API adapter and the durable operation record behind I3.
Implements D4. Review is deliberately heavy: this is the code that changes real
appointments.

## Scope

- In: `app/booking_client.py` real HTTP adapter (reads and writes, deadlines,
  error classification into invalid / denied / slot-taken / transient /
  uncertain); `app/operations.py` with the Postgres `operations` table
  (`proposed → executing → succeeded | failed | uncertain`), atomic claim,
  canonical payload, receipt storage, reconcile-by-lookup before any retry;
  move via the reschedule endpoint, or book-new-then-cancel-old with both
  effects recorded if G01 found none; booking-API credential read from the
  environment (Secret Manager in G08). Additive migrations only.
- Out: proposal creation and the confirm endpoint (G05), the scheduled sweep
  (G13, phase 2).
- Depth: MVP Build for writes. Floor: no blind retries of writes, no
  credentials in code or logs.

## Acceptance

- [ ] Fake API commits then times out: operation ends `succeeded` via lookup, fake shows exactly one booking
- [ ] Two concurrent `execute(op_id)` calls on a real Postgres (container) produce one API write
- [ ] Process killed between claim and write, then restarted: the next status read reconciles instead of writing again
- [ ] "Slot taken" returns `failed` with a reason code, no retry
- [ ] Ambiguous lookup (two matching bookings) ends `uncertain`, never a second write
- [ ] Changed payload under the same operation ID is rejected

Verification: offline `pytest tests/test_operations.py` with the fake; local integration with Postgres in a container; one bounded call set against the booking sandbox if G01 found one.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G03-booking-writes-operation-record.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
