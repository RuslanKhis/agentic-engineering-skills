---
goal: G08
title: The team can measure whether the agent collects claims correctly and safely
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts, adk-release-engineering]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 50-84
  review_and_verify: 8-14
  total: 58-98
  calendar_waits: none
  wait_days: 0
owner: ML
status: ready
---

# G08 The team can measure whether the agent collects claims correctly and safely

## Outcome

A labelled, frozen evaluation set and runner that gate every release (D14), covering I5 and I6.

## Scope

- In: `evals/cases/` 80-120 cases (launch language + English) with gold FNOL fields; runner with deterministic field checks and a pinned judge chosen from the lifecycle table; dev/holdout split; per-run cost ceiling; eval-set hash.
- Out: Launch-language expansion (G30); production samples (G26).
- Depth: Production depth. Floor: synthetic data only; judge pinned.

## Acceptance

- [ ] The runner exits non-zero below threshold and counts missing results as failures
- [ ] Judge agreement with two human labellers on 30 cases is reported
- [ ] The eval-set hash is stable across runs and recorded
- [ ] No real customer data is in the set

Verification: Local runner; judge calls bounded by the cost ceiling.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G08-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
