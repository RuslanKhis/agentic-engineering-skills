---
goal: G19
title: "Storm-level traffic keeps limits, latency and cost within targets"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [adk-operational-guardrails]
blocked_by: [G18]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 8-12
  review_and_verify: 2-4
  total: 10-16
  calendar_waits: Guidewire pre-prod load-test window
  wait_days: 3-8
owner: Platform eng
status: blocked
---

# G19 Storm-level traffic keeps limits, latency and cost within targets

## Outcome

Measured latency, cost per claim and behaviour at 50 concurrent sessions, with limits holding. Implements T1, D14, I8; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g19--storm-level-traffic-keeps-limits-latency-and-cost-within-targets).

## Scope

- In: Load script with synthetic customers; cost measurement with dated prices.
- Out: Tuning (P2-06) unless targets fail.
- Depth: Build: one storm-shaped test.

## Acceptance

- [ ] At 50 concurrent sessions, T1 measured and reported.
- [ ] No duplicate claims; budgets and admission hold.
- [ ] Cost per completed claim recorded with dated prices.

Verification: Authorised staging run with request and cost limits. Execution scope: Staging and Guidewire pre-prod, after approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G19-storm-load-test.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
