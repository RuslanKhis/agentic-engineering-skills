---
goal: G02
title: Writes to the booking API are safe to repeat and their outcome can be looked up
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 8-11
  review_and_verify: 3-4
  total: 11-15
  calendar_waits: none
owner: Dev B
status: blocked
---

# G02 Writes to the booking API are safe to repeat and their outcome can be looked up

## Outcome

The real HTTP adapter behind `BookingPort`, and the booking API changes D4
needs: idempotency keys on create, reschedule and cancel, and lookup by client
reference. Implements D4 and the API side of D5. Includes 1 h handoff from Dev A,
the staging release of the booking API changes and a staging-only fault toggle.

## Scope

- In: `app/booking/http_adapter.py`; booking API changes listed in the
  contract note as missing; contract tests shared with the fake; releasing
  those changes to the staging booking API; a staging-only fault toggle in the
  adapter that drops the response after a committed write.
- Out: the confirm flow and operation records (separate ticket); reconciliation job (phase 2);
  production release of the booking API (part of go-live).
- Depth: MVP. Writes never retried blindly; staging or local booking API only.

## Acceptance

- [ ] A1 The HTTP adapter passes the same contract tests as the fake against a local or staging booking API.
- [ ] A2 Replaying create, reschedule or cancel with the same `Idempotency-Key` and payload returns the original result and creates no second change; the same key with a different payload is rejected.
- [ ] A3 Lookup by client reference returns the appointment change made under that key, or not-found.
- [ ] A4 Timeouts are set (connect 3 s, read 10 s); reads retry at most twice with jitter on timeout, 503 and 429 (honouring `Retry-After`); writes are not retried by the adapter; 401/403 map to `auth_error` with no retry.
- [ ] A5 The booking API key is read from the environment (Secret Manager in deployment); a test asserts it never appears in logs, exceptions or tool results.
- [ ] A6 Two concurrent creates for the same slot produce one appointment and one rejection (test against the booking API).
- [ ] A7 The booking API changes are released to staging; the fault toggle is off by default, refuses to start in production configuration, and when on in staging produces a committed write with a lost response.

Verification: `pytest tests/booking/ -m contract` against a local booking API; staging run only with the team's staging key.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-booking-api-adapter-idempotency.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
