---
goal: G25
title: Security review II: submission path and data handling
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [safe-api-tool-calls, protect-adk-sensitive-data]
blocked_by: [G10, G12, G23]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 4-7
  review_and_verify: 2-3
  total: 6-10
  calendar_waits: none
owner: Security
status: blocked
---

# G25 Security review II: submission path and data handling

## Outcome

An independent review of I2, I3, I6 and I8 before the pilot.

## Scope

- In: Review G10, G12 and G23 code, the data-flow table and the Guidewire credential handling. Findings filed with severity.
- Out: Pen test (W3).
- Depth: Reviewer time is the constraint.

Supporting skills and why:
- safe-api-tool-calls (replay review)
- protect-adk-sensitive-data (data-flow review)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] A written review with findings exists. Critical/high findings are fixed or formally accepted by the Lead before G21.
- [ ] The reviewer has run the G10 replay matrix and the erasure test themselves.

Verification: Review of code and test runs.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G25-security-review-submission-data.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
