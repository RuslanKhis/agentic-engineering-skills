---
goal: G14
title: Security review I: identity, upload and agent structure
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G05, G07, G13]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 8-12
  review_and_verify: 2-4
  total: 10-16
  calendar_waits: none
owner: Security
status: blocked
---

# G14 Security review I: identity, upload and agent structure

## Outcome

An independent review of I1, I5 and D5/D6 before any real customer touches them.

## Scope

- In: Review G05, G07, G13 code and threat model. Findings filed as tickets with severity.
- Out: Submission and data review (G25). Pen test (W3).
- Depth: Reviewer time is the constraint (part-time). Prioritise the authorization paths.

Supporting skills and why:
- none

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] A written review with findings and severity exists. Critical/high findings have a fix ticket or a documented acceptance by the Lead.
- [ ] The reviewer has run the cross-customer and injection tests themselves.

Verification: Review of code and test runs. No live access required.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G14-security-review-identity-upload.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
