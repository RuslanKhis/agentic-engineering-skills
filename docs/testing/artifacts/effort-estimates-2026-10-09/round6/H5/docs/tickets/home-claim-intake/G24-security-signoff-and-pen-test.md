---
goal: G24
title: Have an external pen test and the reviewer's sign-off
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G17, G18, G20]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 2-3
  total: 7-11
  calendar_waits: external penetration test window and report
  wait_days: 10-15
owner: Sec
status: blocked
---

# G24 Have an external pen test and the reviewer's sign-off

## Outcome

An external pen test runs against staging and the reviewer lists sign-off conditions. Implements Security posture; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Scope letter, test window, triage.
- Out: Fixes (G25).
- Depth: Production.

## Acceptance

- [ ] Pen test report received.
- [ ] Findings triaged with severity and owner.
- [ ] Sign-off conditions listed.

Verification: Vendor test against staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G24-security-signoff-and-pen-test.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
