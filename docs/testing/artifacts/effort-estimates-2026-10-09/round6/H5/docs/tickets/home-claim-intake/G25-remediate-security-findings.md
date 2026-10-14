---
goal: G25
title: Fix what the pen test found
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G24]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 9-18
  review_and_verify: 5-8
  total: 14-26
  calendar_waits: none
  wait_days: 0
owner: Dev E
status: blocked
---

# G25 Fix what the pen test found

## Outcome

Critical and high findings are fixed with regression tests. Implements Security posture; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Fixes, tests, re-test request.
- Out: Medium/low items scheduled with owners.
- Depth: Production.

## Acceptance

- [ ] All critical and high findings fixed with regression tests.
- [ ] Medium findings have an owner and date.
- [ ] Security reviewer signs off.

Verification: Offline regression tests; vendor re-test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G25-remediate-security-findings.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
