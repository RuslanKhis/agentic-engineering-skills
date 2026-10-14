---
goal: G03
title: Walking skeleton: an ADK agent behind our API, with tests and CI
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-workflow-design
supporting_skills: [adk-agent-evaluation, adk-frontend-integration]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 10-18
  review_and_verify: 4-6
  total: 14-24
  calendar_waits: none
owner: Agent
status: ready
---

# G03 Walking skeleton: an ADK agent behind our API, with tests and CI

## Outcome

Gives every other goal a running, tested base (D1, D7, D9) and confirms the ADK pin (O3).

## Scope

- In: Proposed layout `app/` (App, Runner factory, intake `LlmAgent` with stub tools), FastAPI app with `/chat` (SSE) and a documented JSON event schema, `RunConfig.max_llm_calls` set, pinned model ID from config, offline scripted-model tests, CI running lint plus unit tests, dependency pins in `pyproject.toml`.
- Out: Real identity (G05), real draft logic (G06), deployment (G04).
- Depth: Floor kept: pinned model, call cap, no secrets in the repo. Production-quality layout, because this code is kept.

Supporting skills and why:
- adk-agent-evaluation (scripted-model Runner tests)
- adk-frontend-integration (JSON/SSE API contract for G11)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] **Confirm the ADK pin** against the chosen version (2.8.0 assumed vs ≥2.10.0 recommended for observability). Record the choice and the reason in the design (O3).
- [ ] A scripted-model Runner test drives one turn end to end through `/chat` and receives SSE text events and a completion event matching the documented schema.
- [ ] CI fails on a failing test (shown by a deliberately broken commit on a branch).
- [ ] `max_llm_calls` exhaustion ends the turn with the designed message, not an exception.

Verification: Offline: `pytest` in CI. Note: google-adk must be installed in the project environment.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
