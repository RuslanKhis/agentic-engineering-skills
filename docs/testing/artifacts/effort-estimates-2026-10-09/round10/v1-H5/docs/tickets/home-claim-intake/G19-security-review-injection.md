---
goal: G19
title: The security reviewer has checked the injection and output controls before external testing
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G14, G25]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 4-8
  review_and_verify: 2-3
  total: 6-11
  calendar_waits: none
owner: Sec
status: blocked
---

# G19 The security reviewer has checked the injection and output controls before external testing

## Outcome

The reviewer reads the adversarial suite, the capability checks and the
release check, runs a few cases of their own, and records findings and
acceptance; this is the internal gate before the pen test and the pilot.

## Scope

- In: review of the suite's coverage against the design's posture table;
  three to five reviewer-authored cases added to the suite; findings with
  severity and owner; 1 h handoff from Eng E.
- Out: identity and write review (done when those land).
- Depth: production.

## Acceptance

- [ ] Every row of the design's security-posture table has a passing test the reviewer agrees covers it.
- [ ] No open high-severity finding.
- [ ] Reviewer-authored cases are in the suite and pass.

Verification: the reviewer's own run of the offline suite; written findings.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G19-security-review-injection.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
