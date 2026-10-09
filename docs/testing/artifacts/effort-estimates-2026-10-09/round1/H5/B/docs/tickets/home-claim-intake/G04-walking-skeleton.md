---
goal: G04
title: Walking skeleton: intake agent behind an API with a pinned ADK and model
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-workflow-design
supporting_skills: [adk-release-engineering, adk-agent-instructions]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 10-16
  review_and_verify: 10-16
  total: 20-32
  calendar_waits: none
owner: E2 (agent lead)
status: ready
---

# G04 Walking skeleton: intake agent behind an API with a pinned ADK and model

## Outcome

A local FastAPI service runs the intake agent through an ADK Runner with a pinned model and a fake Guidewire, and CI runs its offline tests. Implements D1, D5, D6, D13; ADK version assumption.

## Scope

- In: Proposed layout `src/claim_intake/{api,agent,tools,drafts,guidewire,ops}`; `pyproject.toml` with exact pins; ADK `App`/`Runner` wiring; placeholder instruction; in-memory session for now; fake Guidewire module; pytest with a scripted model; CI workflow running unit tests.
- Out: Identity (G05), drafts DB (G06), real instruction (G07).
- Depth: Production layout kept from day one; floor: pinned model ID, `max_llm_calls` set, no secrets.
- Route: ADK `LlmAgent` + `Runner` invoked from a FastAPI route; confirm `RunConfig.max_llm_calls`, `DatabaseSessionService`, `ToolContext` user access and `before_tool_callback` against the chosen pin.
- Supporting skills: `adk-release-engineering` (dependency and model pins recorded in a first release manifest); `adk-agent-instructions` (prompt-as-code layout with a rendered-request test)
- Execution scope: Local code and dependency pins in the new repository are authorized by running this goal.

## Acceptance

- [ ] `POST /chat` returns an assistant reply from a scripted model in tests
- [ ] ADK version chosen and pinned; each ADK interface named in the design confirmed against that version (note in the plan)
- [ ] Rendered request test shows the pinned model ID and instruction version
- [ ] CI fails on a failing test

Verification: Offline: `pytest` with a scripted model; no network.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
