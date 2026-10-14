---
goal: G18
title: Spend and abuse stay bounded, even in a storm
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G06, G07, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 18-28
  review_and_verify: 6-10
  total: 24-38
  calendar_waits: none
owner: Eng C
status: blocked
---

# G18 Spend and abuse stay bounded, even in a storm

## Outcome

Per-invocation, per-session and per-customer limits, an operator stop and a degrade mode, as in D10.

## Scope

- In: allowance table in Cloud SQL with atomic admission, operator flag independent of resets, degrade response, metrics for refusals.
- Out: final thresholds (O3).
- Depth: build.

## Acceptance

- [ ] A looping scripted model stops at the call cap with the defined message
- [ ] The fourth draft in a day is refused with the phone line; the existing drafts remain
- [ ] Operator stop blocks new turns within one minute while status and submit of already confirmed drafts continue

Verification: Offline plus local Postgres concurrency test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G18-budgets-and-limits.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
