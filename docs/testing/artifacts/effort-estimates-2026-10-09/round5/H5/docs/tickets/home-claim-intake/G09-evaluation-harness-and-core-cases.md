---
goal: G09
title: "We can measure intake quality on a first labelled DE and EN set"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [G01]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 18-27
  review_and_verify: 4-6
  total: 22-33
  calendar_waits: none
  wait_days: 0
owner: ML eng
status: blocked
---

# G09 We can measure intake quality on a first labelled DE and EN set

## Outcome

A runner with simulated customers and 40–50 labelled core scenarios (synthetic customers, staff-donated or licensed photos), enough for G08 to iterate on. Implements T2, I5, I7; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g09--we-can-measure-intake-quality-on-a-first-labelled-de-and-en-set).

## Scope

- In: Case schema and labelling guide; core scenarios across claim types and both languages; deterministic metrics (fields complete, handoff correct, no cover statement); judged summary quality with the pinned judge; `eval/SUMMARY.md`.
- Out: Second half of the set (G26); real customer data (only after G03); CI wiring (G17).
- Depth: Build.

## Acceptance

- [ ] Runner produces per-case and per-slice results including failed and missing runs.
- [ ] Labelling guide written so another person can label (used by G26).
- [ ] Thresholds for G08 written down.

Verification: Local runs with live model in dev, cost recorded. Execution scope: Live model in dev, capped.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-evaluation-harness-and-core-cases.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
