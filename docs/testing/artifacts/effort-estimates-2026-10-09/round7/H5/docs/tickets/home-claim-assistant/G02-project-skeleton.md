---
goal: G02
title: Run a local intake agent skeleton with pinned versions
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 10-16
  review_and_verify: 3-6
  total: 13-22
  calendar_waits: none
owner: Eng C
status: ready
---

# G02 Run a local intake agent skeleton with pinned versions

## Outcome

A Python project with the proposed layout (plan, implementation map), `google-adk` pinned, an `App`/`Runner` wrapper owning `RunConfig.max_llm_calls`, a stub intake `LlmAgent` and an offline test harness with a scripted model. Confirms the ADK pin assumed in the design.

## Scope

- In: `pyproject.toml` pins, `app/agents/intake.py` stub, `app/runner.py`, `tests/` with a scripted-model fixture, CI running unit tests, `app/config/release.yaml` with model ID `gemini-3.8-flash` (provisional).
- Out: real tools (G06), cloud (G03).
- Depth: build; floor kept: pinned model, call cap, no secrets.

## Acceptance

- [ ] `pytest` passes offline with no network and no credentials
- [ ] A scripted model that loops is stopped by `max_llm_calls` with a defined error
- [ ] The chosen ADK version and the checked interfaces (`DatabaseSessionService`, `output_schema`, `tool_context.state`, `max_llm_calls`) are recorded in Evidence

Verification: Offline: `pytest -q`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G02-project-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
