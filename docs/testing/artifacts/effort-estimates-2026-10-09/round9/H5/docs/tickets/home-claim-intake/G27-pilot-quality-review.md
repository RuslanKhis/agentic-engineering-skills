---
goal: G27
title: Judge pilot claims with adjusters and measure the outcome
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-observability]
blocked_by: [G21]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 12-22
  review_and_verify: 4-6
  total: 16-28
  calendar_waits: none
owner: ML
status: blocked
---

# G27 Judge pilot claims with adjusters and measure the outcome

## Outcome

Evidence for GA: model quality on real claims, valid transactions and the A12 outcome measures against the web-form baseline.

## Scope

- In: Sample of pilot claims reviewed with adjusters against the rubric during the pilot, web-form baseline for callbacks and time to file, SLI review (T1/T2), list of fixes.
- Out: Feeding production samples into the eval set (P2-04, needs DPIA terms).
- Depth: Evaluation with an audited, access-controlled read of pilot sessions.

Supporting skills and why:
- adk-agent-observability (session sampling)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] The report separates model quality, transaction validity and the outcome change vs baseline, with sample sizes.
- [ ] Any coverage-statement or cross-customer incident is listed (target: none).
- [ ] Missing or failed reviews are reported as missing, never as passes.

Verification: Production read under the DPIA terms.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G27-pilot-quality-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
