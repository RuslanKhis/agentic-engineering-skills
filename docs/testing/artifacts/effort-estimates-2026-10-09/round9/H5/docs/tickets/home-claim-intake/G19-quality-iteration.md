---
goal: G19
title: Bring intake quality to the agreed thresholds
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G06, G08, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 36-60
  review_and_verify: 8-14
  total: 44-74
  calendar_waits: none
owner: ML
status: blocked
---

# G19 Bring intake quality to the agreed thresholds

## Outcome

Moves the G09 baseline to thresholds that justify a pilot.

## Scope

- In: Error analysis on the dev split, instruction and exemplar changes, schema tweaks, at most two rounds, holdout run at the end. Thresholds (provisional, to be confirmed): field accuracy ≥ 95 %, emergency recall 100 %, coverage violations 0, median questions ≤ 8.
- Out: Model escalation beyond the pinned ID: that needs a release decision.
- Depth: Build. Each change is a versioned prompt release.

Supporting skills and why:
- adk-agent-instructions (prompt and exemplar changes)
- adk-model-and-output-contracts (schema and model settings)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] Holdout results meet the thresholds or the gap is reported with the next experiment.
- [ ] Each round is recorded with prompt version, model ID, eval-set hash and cost.

Verification: Bounded live eval runs under a stated call and cost cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G19-quality-iteration.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
