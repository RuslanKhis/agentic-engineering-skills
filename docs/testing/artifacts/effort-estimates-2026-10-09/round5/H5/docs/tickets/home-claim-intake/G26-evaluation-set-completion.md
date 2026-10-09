---
goal: G26
title: "The labelled set covers handoffs, edge cases and adversarial-lite inputs in both languages"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: [G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 14-20
  review_and_verify: 4-6
  total: 18-26
  calendar_waits: none
  wait_days: 0
owner: Integration eng
status: blocked
---

# G26 The labelled set covers handoffs, edge cases and adversarial-lite inputs in both languages

## Outcome

A further 40–50 labelled scenarios following the G09 guide, bringing the set to 80–100 for the CI gate and the pilot comparison. Implements T2, I5, I7; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g26--the-labelled-set-covers-handoffs-edge-cases-and-adversarial-lite-inputs-in-both-languages).

## Scope

- In: Labelling with the G09 guide (handoff hours included); injury, emergency, liability, out-of-scope, poor photos, injection-in-photo cases; judge agreement on 30 cases.
- Out: Harness changes (G09).
- Depth: Build.

## Acceptance

- [ ] Set has 80–100 cases with both languages in every slice.
- [ ] Judge agreement with human labels measured on at least 30 cases.
- [ ] ML engineer has reviewed a sample of the new labels.

Verification: Local runs with live model in dev, cost recorded. Execution scope: Live model in dev, capped.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G26-evaluation-set-completion.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
