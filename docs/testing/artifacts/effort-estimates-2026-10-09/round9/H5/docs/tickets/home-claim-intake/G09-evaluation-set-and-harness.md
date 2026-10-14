---
goal: G09
title: Measure intake quality on a labelled German and English case set
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 40-70
  review_and_verify: 6-10
  total: 46-80
  calendar_waits: none
owner: ML
status: blocked
---

# G09 Measure intake quality on a labelled German and English case set

## Outcome

Gives D15, I4 and D12 measurable evidence and the baseline G17 gates on and G19 improves.

## Scope

- In: 80–120 labelled cases: synthetic DE/EN conversations (simulated customers), staff-made or licensed damage photos, emergency subset, coverage-bait subset, cross-language. Metrics: field accuracy, completeness, number of questions, photo-description agreement, emergency recall, coverage violations. Runner script producing `eval/summary.md`.
- Out: Real customer content: needs W1 and becomes P2-04. Tuning: G19.
- Depth: Build, with the judge pinned to the same model ID and its own prompt. Deterministic metrics first.

Supporting skills and why:
- none

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] The harness runs all cases and writes a per-case result, including failed and missing runs (never dropped).
- [ ] The baseline is recorded: per-metric scores for the G06 agent, with model ID, prompt version and eval-set hash.
- [ ] No real customer data is in the set (checked by the data source list).

Verification: Offline harness tests. Bounded live eval run under a stated call and cost cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-evaluation-set-and-harness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
