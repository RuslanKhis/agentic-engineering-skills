---
goal: G20
title: "The security reviewer has reviewed the threat model and adversarial evidence"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G15]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 6-9
  review_and_verify: 1-2
  total: 7-11
  calendar_waits: none
  wait_days: 0
owner: Security reviewer
status: blocked
---

# G20 The security reviewer has reviewed the threat model and adversarial evidence

## Outcome

Reviewer findings on the G15 threat model and suite, with pen-test scope agreed. Implements I1, I2, I4; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g20--the-security-reviewer-has-reviewed-the-threat-model-and-adversarial-evidence).

## Scope

- In: Review of threat model, enforcement-point map and suite; pen-test scope.
- Out: Pen test (G21).
- Depth: Build.

## Acceptance

- [ ] Review record with findings and owners.
- [ ] Pen-test scope written.

Verification: Document review. Execution scope: People work only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G20-threat-model-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
