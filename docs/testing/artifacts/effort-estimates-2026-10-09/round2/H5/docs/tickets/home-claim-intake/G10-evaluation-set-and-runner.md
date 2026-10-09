---
goal: G10
title: A labelled evaluation set measures intake quality per release
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 60–106
  review_and_verify: 20–34
  total: 80–140
  calendar_waits: Approval to use anonymised historical FNOLs from data governance, 2–4 weeks; synthetic cases start immediately
owner: ML
status: blocked
---

# G10 A labelled evaluation set measures intake quality per release

## Outcome

80–120 cases (synthetic + anonymised historical, both languages, all A12 claim types, escalation and adversarial subsets, 60 licensed/synthetic photos) with field-level expected drafts, and a runner producing per-case results and a summary.

## Scope

- In: `eval/cases/`, `eval/run_eval.py`, metrics: required-field accuracy, completion within turn budget, escalation correctness, coverage-promise rate, photo-observation agreement with human labels; judge pinned and calibrated on 30 human-labelled cases.
- Out: CI wiring (G14); iteration (G16).
- Depth: Production: gated evaluation. Floor: no real personal data in cases.
- Route: ADK evaluation interfaces or a custom runner over the Runner with a user simulator; results as JSON under `eval/runs/`.
- Supporting skills: `adk-model-and-output-contracts` (judge model choice and pin from the lifecycle table)
- Execution scope: Dev project; anonymised data only.

## Acceptance

- [ ] Runner executes all cases and reports failed and missing results separately
- [ ] Judge agreement with human labels measured on the calibration subset and recorded
- [ ] Baseline scores recorded for the current prompt and model

Verification: Bounded live run in dev with a cost cap recorded per run.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G10-evaluation-set-and-runner.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
