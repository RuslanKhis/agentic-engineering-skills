---
goal: G01
title: Booking API client, fake and contract
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Booking API client, fake and contract

## Outcome

Every other goal can call the booking API through one typed client, and test
against an in-memory fake that behaves like the API, including its failures.
Settles design O1 (idempotency and lookup by operation ID) and O3 (atomic
move) with evidence from the API's own code. Implements the read and write
rows of the failure grid for the client layer (D3).

## Scope

- In: `app/booking_client.py` with list salons/services/staff, find slots,
  get booking, create, update (move), cancel, and lookup by `op_id`. Typed
  results; 5 s read timeout with 1 retry; 10 s write deadline with no retry;
  errors mapped to `unavailable / rejected(reason) / not_found / uncertain`.
  `app/fake_booking_api.py` with scripted failures (timeout after commit,
  slot taken, 429, 5xx, malformed body). `docs/booking-api-contract.md`: the
  API facts found (auth, idempotency header, move semantics, business-rule
  codes, time zone fields). If the API has no idempotency key or lookup and
  the team owns it, write the smallest API change as a separate proposal; do
  not change the API in this ticket. API key read from the environment only.
- Out: tools and the agent (G02), the operations table (G03), reconciliation (G07).
- Depth: MVP. Build: timeouts, error mapping, no blind write retries.
  Floor: no key in code or logs.

## Acceptance

- [ ] Contract tests pass against the fake, and against booking API staging
      for read endpoints (authorised live, staging only).
- [ ] A write that times out after the fake committed returns `uncertain`,
      never `rejected`, and the client does not retry it.
- [ ] A 429 or 5xx on a read gives exactly 2 attempts, then `unavailable`.
- [ ] O1 and O3 answered in `docs/booking-api-contract.md` with file/route
      pointers; design A5 updated to confirmed or changed.
- [ ] No API key or customer phone appears in captured logs.

Verification: `pytest tests/test_booking_client.py` offline; staging contract
tests behind an env flag, read-only.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-client-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
