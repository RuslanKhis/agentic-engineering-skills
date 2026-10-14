---
goal: G24
title: The agent's conversations are measured on realistic cases in both languages
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G07, G17]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 32-50
  review_and_verify: 6-8
  total: 38-58
  calendar_waits: claims-handler review of labels
owner: ML
status: blocked
---

# G24 The agent's conversations are measured on realistic cases in both languages

## Outcome

A conversation evaluation set of about 120 cases across both languages and
the main home-claim types (water, storm, fire, theft, accidental damage,
emergency, out-of-scope, hostile), with expected draft fields, simulated
customers, and the cases added to the CI gate; claims handlers review the
labels.

## Scope

- In: case design; simulated-customer profiles; expected required fields and
  forbidden statements; metrics (field accuracy, completeness, turns to
  complete, coverage-promise count, emergency recall); baseline run of the
  current agent; handler label review; 1 h handoff from Eng D.
- Out: production samples (phase 2).
- Depth: production.

## Acceptance

- [ ] Baseline run recorded in `evals/SUMMARY.md` with run ID and cost.
- [ ] Emergency recall 100% and coverage promises 0 on the set, or the failures filed against the agent.
- [ ] Handlers' label corrections applied and counted.
- [ ] The gate runs the deterministic subset on every change.

Verification: offline replay plus a bounded live run within the gate's cost
cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G24-conversation-eval-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
