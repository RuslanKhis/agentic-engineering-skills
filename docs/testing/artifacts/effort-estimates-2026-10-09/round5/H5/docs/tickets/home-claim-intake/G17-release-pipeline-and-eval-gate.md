---
goal: G17
title: "Every change ships as one pinned release unit through an evaluation gate"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: []
blocked_by: [G04, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 16-24
  review_and_verify: 4-8
  total: 20-32
  calendar_waits: none
  wait_days: 0
owner: Platform eng
status: blocked
---

# G17 Every change ships as one pinned release unit through an evaluation gate

## Outcome

CI builds the manifest, runs unit, adversarial and deterministic eval checks, deploys to staging and supports canary and rollback. Implements D9, D15; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g17--every-change-ships-as-one-pinned-release-unit-through-an-evaluation-gate).

## Scope

- In: Manifest; gate thresholds; scheduled judge run; traffic split; rollback procedure; model retirement calendar entry.
- Out: Production rollout (G24).
- Depth: Build.

## Acceptance

- [ ] Seeded regression fails the gate by exit code.
- [ ] Manifest has no model alias and records prompt, model, judge, schema and secret versions.
- [ ] Rollback to the previous revision rehearsed in staging.

Verification: CI runs; staging rehearsal. Execution scope: CI and staging, after approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G17-release-pipeline-and-eval-gate.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
