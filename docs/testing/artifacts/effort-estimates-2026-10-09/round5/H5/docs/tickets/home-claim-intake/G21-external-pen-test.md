---
goal: G21
title: "An external test of staging finds no open critical or high issues"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G18, G20]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 10-14
  review_and_verify: 3-4
  total: 13-18
  calendar_waits: External penetration test and fix verification
  wait_days: 10-15
owner: Security eng
status: blocked
---

# G21 An external test of staging finds no open critical or high issues

## Outcome

Pen test run against staging, findings triaged into owning goals and fixes verified. Implements I1, I2, I4; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g21--an-external-test-of-staging-finds-no-open-critical-or-high-issues).

## Scope

- In: Vendor coordination, test accounts, triage, fix verification.
- Out: Fixes land in the owning goals' code.
- Depth: Build.

## Acceptance

- [ ] Report received; no open critical or high findings.
- [ ] Fix verification evidence linked.

Verification: External test in staging. Execution scope: Staging; external tester under contract.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G21-external-pen-test.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
