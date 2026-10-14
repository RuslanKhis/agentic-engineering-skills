---
goal: G21
title: Release with a gate, a canary and a joint rollback
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G12, G18]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 14-23
  review_and_verify: 5-8
  total: 19-31
  calendar_waits: none
  wait_days: 0
owner: Dev A
status: blocked
---

# G21 Release with a gate, a canary and a joint rollback

## Outcome

Every release carries a manifest, passes a CI gate and rolls out through a canary with a rehearsed rollback. Implements D7, D13; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Manifest, CI gate (deterministic every change, eval subset per release), Cloud Run traffic split, rollback script, model-retirement calendar.
- Out: Production ramp (G27).
- Depth: Production.

## Acceptance

- [ ] Manifest has no model alias and records image, prompt, model, judge, tool-schema and eval-set versions.
- [ ] The gate fails by exit code on a deterministic failure or an eval below threshold.
- [ ] Rollback rehearsal in staging restores the previous image, prompt and model together.

Verification: CI run and staging rehearsal.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G21-release-gate-and-canary.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
