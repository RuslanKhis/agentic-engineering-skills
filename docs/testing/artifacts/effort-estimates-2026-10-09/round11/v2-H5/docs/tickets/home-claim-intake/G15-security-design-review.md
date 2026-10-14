---
goal: G15
title: An independent security reviewer has checked the design before code is written
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: []
phase: 1
profile: production
estimate:
  hands_on: 5-8
  review_and_verify: 1-1
  total: 6-9
  calendar_waits: none
owner: SecRev
status: ready
---

# G15 An independent security reviewer has checked the design before code is written

## Outcome

The part-time security reviewer reviews the design's trust boundaries,
D1, D6, D7, D9 and the security posture section in the first weeks, so
findings change the design while it is cheap.

## Scope

- In: written findings against the design, each settled in the design or
  its change table by the authors.
- Out: code review (G26); external testing.
- Depth: production.

## Acceptance

- [ ] A1 Findings on the design are recorded with severity, and each is settled (changed, or recorded why not) in the design's change table.
- [ ] A2 The reviewer lists the cases the adversarial suite must contain beyond those already named, and they are added to G14's scope.

Verification: document review; no code.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G15-security-design-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
