---
goal: G06
title: Hold a local intake conversation that fills a claim draft
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 6-11
  review_and_verify: 3-5
  total: 9-16
  calendar_waits: none
  wait_days: 0
owner: Dev A
status: ready
---

# G06 Hold a local intake conversation that fills a claim draft

## Outcome

A local intake agent, run through an application-owned `App` and `Runner`, talks about a burst pipe and updates an in-memory draft. Implements D1, D7, D13 (pin); route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Proposed layout `claim_intake/{agent.py,tools.py,draft.py,app.py}`, `tests/`; `pyproject.toml` with the chosen ADK pin; pinned model ID; `RunConfig.max_llm_calls=8`.
- Out: Persistence (G07), identity (G08), photos (G09, G10).
- Depth: Production code kept; floor: pinned model, call cap, no secrets.

## Acceptance

- [ ] Scripted model calls `update_claim_draft`; the draft then has `loss_cause=escape_of_water`.
- [ ] A ninth model call in one invocation is refused (`max_llm_calls=8`).
- [ ] Configured model ID is exactly `gemini-3.8-flash`, no alias; chosen ADK pin recorded and the APIs used checked against it.

Verification: Offline pytest with a scripted model; no network.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
