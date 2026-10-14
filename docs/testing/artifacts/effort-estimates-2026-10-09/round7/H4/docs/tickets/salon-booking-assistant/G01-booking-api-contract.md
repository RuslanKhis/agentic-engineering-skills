---
goal: G01
title: Booking API write contract and policy facts
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 3-4
  review_and_verify: 1
  total: 4-5
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Booking API write contract and policy facts

## Outcome

Settle the questions that decide D4 and D5: does the booking API accept idempotency keys, and with what scope and retention? Is reschedule atomic? What are the error codes and the staging environment? Which lookup supports reconciliation? Also collect the policy values and a one-month baseline of phone changes. This is a discovery goal: it produces a decision, not code.

## Scope

- In and out: In: `docs/architecture/booking-api-contract.md` (endpoints, replay contract, error classes, timezone handling); a draft `app/policy.yaml`; the W1 email. Out: client code (G03).
- Depth: No writes to production. Staging only. Step 1, on day 1: send the W1 sign-off request to the salon owner.

## Acceptance

- [ ] The replay contract is recorded as one of: idempotency key, lookup-then-dispatch, or manual reconciliation, with evidence (a doc link or a staging call log)
- [ ] Reschedule is classified atomic or two-step. If two-step, G03's scope note is updated
- [ ] No production write is made, and no credential appears in the doc

Verification: Read the doc. Staging calls are logged with their IDs. This is authorised live work against staging only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
