---
goal: G28
title: "Confirming the summary records one durable submission bound to what the customer saw"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G01, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 8-12
  review_and_verify: 4-6
  total: 12-18
  calendar_waits: none
  wait_days: 0
owner: Agent lead
status: blocked
---

# G28 Confirming the summary records one durable submission bound to what the customer saw

## Outcome

The confirm route checks owner, draft version and policy, freezes the payload, inserts one operation and enqueues one named task; repeated confirms return the same operation. Implements D3, D4, I2; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g28--confirming-the-summary-records-one-durable-submission-bound-to-what-the-customer-saw).

## Scope

- In: Confirm route; operation table and state machine (schema agreed with G10 on day one, handoff hours included); policy re-check; Cloud Tasks named enqueue; status route data.
- Out: Worker and Guidewire client (G10).
- Depth: Build with careful review: authorization and write intent.

## Acceptance

- [ ] Double confirm returns the same operation ID; one task enqueued.
- [ ] Draft changed after display → confirm refused, customer must re-confirm.
- [ ] Another customer's draft cannot be confirmed; policy not in force on loss date is refused before any operation exists.

Verification: Offline tests with real Postgres. Execution scope: Local only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G28-confirm-and-operation-record.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
