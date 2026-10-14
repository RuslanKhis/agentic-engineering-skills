---
goal: G12
title: Measure intake quality on a frozen labelled set
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 24-42
  review_and_verify: 5-8
  total: 29-50
  calendar_waits: anonymised historical FNOL extract approved by the claims data owner
  wait_days: 5-10
owner: ML
status: blocked
---

# G12 Measure intake quality on a frozen labelled set

## Outcome

80 to 120 labelled cases with a runner and a recorded baseline. Implements D1, I7, I10; outcome hypothesis; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Synthetic and anonymised historical FNOL texts, photo sets, both languages, handoff and adversarial cases; metrics: field accuracy, loss-cause accuracy, completion, forbidden statements, handoff correctness; pinned judge.
- Out: CI gate wiring (G21).
- Depth: Production gated evaluation.

## Acceptance

- [ ] Set frozen with hash and dev/holdout split.
- [ ] Runner exits non-zero below thresholds; baseline recorded with model, prompt and judge versions.
- [ ] Anonymisation check finds no names, addresses or policy numbers in cases.

Verification: Bounded live with a spend limit agreed before the run.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-evaluation-set-and-runner.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
