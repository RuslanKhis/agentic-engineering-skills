---
goal: G01
title: A developer runs the intake agent locally behind the API with a pinned model and a call cap
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-workflow-design
supporting_skills: [adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: production
estimate: 40-64 h
status: ready
---

# G01 A developer runs the intake agent locally behind the API with a pinned model and a call cap

## Outcome

The repository has a runnable FastAPI service that runs a one-agent ADK App through a Runner with a pinned `gemini-3.8-flash` model and `RunConfig(max_llm_calls=8)`, plus CI running offline tests. Every later goal builds on this. Implements D1, D7, D10, I9 (per-invocation cap) in the design.

## Scope

- In: `pyproject.toml` with exact `google-adk` pin; `app/agent/factory.py` (LlmAgent, no real tools yet); `app/api` with `POST /sessions`, `POST /sessions/{id}/messages` (unauthenticated placeholder, guarded by a dev-only flag); local Postgres via `DatabaseSessionService`; scripted-model Runner test; CI workflow for lint and offline tests.
- Out: Authentication (G04), real tools (G05), photos (G06), deployment (G16).
- Depth: Production layout kept for later goals; floor: no secrets in repo, model pinned, call cap set. Telemetry and release manifest are left to G17/G18.
- Route: `App`/`Runner` invoked from the message route; `DatabaseSessionService` with a Postgres URL from env; model configured as Vertex AI in an EU location from a single settings value. Confirm constructor names and session-service support against the chosen pin.
- Prerequisites: None. Python toolchain; local Postgres (container).
- Supporting skills:
  - `adk-model-and-output-contracts`: pinned model ID and Vertex backend configuration
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls.

## Acceptance

- [ ] A scripted-model Runner test sends a message and receives the scripted reply through the API route, and the session persists across a process restart (local Postgres).
- [ ] Exceeding `max_llm_calls` returns the designed apology result, not a 500, and the session remains usable.
- [ ] Forbidden: no model ID alias (`-latest`) and no credential appear in the repository; the installed `google-adk` version equals the pin and is recorded in Evidence (acceptance item: confirm the design's ADK 2.8.0 assumption against the chosen pin).

Verification: Offline: `pytest -q` with scripted model; local integration: restart test against local Postgres.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
