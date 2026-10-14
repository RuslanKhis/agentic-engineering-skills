---
goal: G17
title: Have the security reviewer check identity, upload and submission code
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G05, G08, G09, G13]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 8-14
  review_and_verify: 2-3
  total: 10-17
  calendar_waits: none
  wait_days: 0
owner: Sec
status: blocked
---

# G17 Have the security reviewer check identity, upload and submission code

## Outcome

The reviewer reads G08, G09 and G13 changes and tests before staging. Implements I1, I2, I3, I9; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Code and test review; findings with severity.
- Out: Pen test (G24).
- Depth: Production review depth.

## Acceptance

- [ ] Findings recorded with severity and linked to code.
- [ ] No open high-severity finding.
- [ ] Each fix has a regression test.

Verification: Code review and rerun of the goals' tests.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G17-boundary-security-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
