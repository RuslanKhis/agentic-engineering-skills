---
goal: G22
title: "Security signs off the service for real customers"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G21]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  calendar_waits: none
  wait_days: 0
owner: Security reviewer
status: blocked
---

# G22 Security signs off the service for real customers

## Outcome

Signed security approval for the pilot and GA, with any accepted risks named with owner and end condition. Implements I1, I2, I4; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g22--security-signs-off-the-service-for-real-customers).

## Scope

- In: Final review of G21 evidence.
- Out: —
- Depth: Build.

## Acceptance

- [ ] Signed record.
- [ ] Accepted risks listed with owner and end condition.

Verification: Document review. Execution scope: People work only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G22-security-sign-off.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
