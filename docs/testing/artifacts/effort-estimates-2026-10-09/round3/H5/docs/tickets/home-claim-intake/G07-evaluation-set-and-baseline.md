---
goal: G07
title: We know how well the agent fills claims before any customer uses it
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 30-44
  review_and_verify: 5-8
  total: 35-52
  calendar_waits: none
owner: ML
status: blocked
---

# G07 We know how well the agent fills claims before any customer uses it

## Outcome

Measures I5 and T2 for the pinned model (D9).

## Scope

- In:
  - 50 synthetic German/English conversations from personas, reviewed by a claims handler
  - 60 labelled damage photos (licensed or staff-taken; no customer photos)
  - Deterministic scorers: required-field accuracy, cause-code accuracy, turns to complete, coverage-promise rate, photo damage-type accuracy; judge for tone only
  - Versioned eval set with hash; baseline report
- Out: CI gate (G17), pilot error analysis (G22)
- Depth: Build; synthetic data only.

## Acceptance

- [ ] Eval set versioned with a recorded hash
- [ ] Baseline report lists each metric with failed and missing cases
- [ ] Coverage-promise rate is reported, not assumed zero

Verification: Offline scorer tests; bounded live baseline run within the phase-1 budget.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G07-evaluation-set-and-baseline.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
