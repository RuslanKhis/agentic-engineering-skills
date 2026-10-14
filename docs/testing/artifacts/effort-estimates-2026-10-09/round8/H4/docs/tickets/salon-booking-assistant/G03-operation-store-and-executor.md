---
goal: G03
title: A confirmed proposal changes the booking exactly once, or says honestly that it is unsure
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-agent-security]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-8
  review_and_verify: 3-4
  total: 9-12
  calendar_waits: none
owner: Dev C
status: blocked
---

# G03 A confirmed proposal changes the booking exactly once, or says honestly that it is unsure

## Outcome

Implements D2 and D4 and guarantees I2–I4: the executor is the only code that writes to the booking API.

## Scope

- In: `assistant/operations/store.py` (Postgres table, states, canonical payload, 10-minute expiry, atomic claim) and `executor.py` (ownership and freshness recheck, idempotency key if G01 confirms support, outcome mapping: conflict and policy refusal → `failed`, timeout or 5xx after dispatch → `uncertain`, never retried). Includes a staff-facing `uncertain` log line.
- Out: Automatic reconciliation (G10); the HTTP endpoint (G05).
- Depth: Build at MVP depth; the review is careful because this is the write boundary.

## Acceptance

- [ ] Two concurrent confirms on one operation cause one fake-API call and return the same outcome
- [ ] Timeout-after-commit leaves the operation `uncertain` with no second dispatch
- [ ] Confirming an expired operation, or another customer's operation, makes no API call

Verification: local integration against a disposable Postgres and the G01 fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-operation-store-and-executor.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
