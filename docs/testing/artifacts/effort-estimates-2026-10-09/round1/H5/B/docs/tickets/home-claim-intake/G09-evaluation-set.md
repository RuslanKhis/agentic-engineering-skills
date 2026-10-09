---
goal: G09
title: Labelled DE/EN evaluation set that measures intake quality
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [G07, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 48-80
  review_and_verify: 12-20
  total: 60-100
  calendar_waits: Licence or consent for photo set; SME labelling time
owner: ML engineer with claims SMEs
status: blocked
---

# G09 Labelled DE/EN evaluation set that measures intake quality

## Outcome

The team can say how complete, correct and safe the intake is, per language and cause, with a repeatable run. Implements I5, I6, D6, O6.

## Scope

- In: ≥ 80 cases (DE/EN; water, storm, fire, theft, accidental, other; emergencies; out-of-scope; adversarial), user simulator, metrics: required-field completeness/accuracy, emergency recall, forbidden-statement rate, photo label accuracy, turns to completion; judge calibrated against 30 human-labelled cases.
- Out: CI gate (G18).
- Depth: Production: gated evaluation; frozen development and holdout split.
- Route: ADK evaluation with a pinned judge; results to `eval/results/` with run records.
- Supporting skills: `adk-model-and-output-contracts` (judge pin and output validation)
- Execution scope: Dev project model calls; licensed photos only.

## Acceptance

- [ ] Run produces per-metric results with case counts and missing results reported
- [ ] Judge agreement with human labels recorded; O6 decided
- [ ] Baseline: forbidden-statement rate 0, emergency recall ≥ 0.95, required-field completeness ≥ 0.9 (provisional targets) — or the gaps listed
- [ ] Eval set hash recorded for the release manifest

Verification: Bounded live: dev project, call cap per run declared.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
