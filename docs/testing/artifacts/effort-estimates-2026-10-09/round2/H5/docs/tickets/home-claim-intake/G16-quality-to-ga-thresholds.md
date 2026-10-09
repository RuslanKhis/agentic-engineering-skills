---
goal: G16
title: Intake quality meets the GA thresholds on the evaluation set
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G10, G07]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 42–70
  review_and_verify: 18–30
  total: 60–100
  calendar_waits: none
owner: ML
status: blocked
---

# G16 Intake quality meets the GA thresholds on the evaluation set

## Outcome

Error analysis and iterations bring required-field accuracy, escalation correctness and coverage-promise rate to thresholds agreed with claims ops; the final prompt version is frozen for the pilot.

## Scope

- In: Threshold proposal and sign-off; error analysis; prompt versions; regenerated results with the final method.
- Out: New languages (G24).
- Depth: Production. Floor: pinned judge; held-out subset not used for tuning.
- Route: Quality-iteration loop on a development split, held-out split for the decision.
- Supporting skills: `adk-agent-instructions` (prompt and exemplar changes); `adk-model-and-output-contracts` (model escalation or thinking-level decision)
- Execution scope: Dev project.

## Acceptance

- [ ] Thresholds written and signed off by claims ops
- [ ] Held-out results meet thresholds with the frozen prompt and model
- [ ] Coverage-promise rate on the adversarial subset at or below threshold

Verification: Bounded live eval runs in dev with recorded cost.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G16-quality-to-ga-thresholds.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
