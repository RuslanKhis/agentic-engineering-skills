---
goal: G02
title: A developer can run the intake agent locally and get a reply from the pinned model
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-workflow-design
supporting_skills: [adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 12-18
  review_and_verify: 4-6
  total: 16-24
  calendar_waits: none
owner: Eng A
status: ready
---

# G02 A developer can run the intake agent locally and get a reply from the pinned model

## Outcome

The project skeleton every other goal builds on: a FastAPI app owning an ADK
`App` and `Runner`, one `intake_agent` with a placeholder instruction and no
tools, a JSON turn endpoint, an offline test with a scripted model and CI
running it. Implements the structure of D1 and the pins of D7 and D14.

## Scope

- In: `pyproject.toml` with Python 3.11 and google-adk pinned (2.8.0 unless
  the check below says otherwise); `app/main.py`, `app/agent/`; `POST
  /sessions/{id}/turns` returning completed JSON (D8); `RunConfig` with
  `max_llm_calls=10`; model ID from configuration, pinned to
  `gemini-3.8-flash`; in-memory session service behind an interface that
  `DatabaseSessionService` replaces later; the turn API schema documented in
  `docs/api/turns.md`; a CI workflow running lint and offline tests.
- Out: identity (G04), tools and instruction content (G06), Cloud SQL (G03).
- Depth: production code layout from the start; local only.

## Acceptance

- [ ] **Confirm against the chosen pin:** ADK constructors and `RunConfig` fields used here exist in the pinned version; record the version and the source read.
- [ ] O1 answered with a dated source: whether `gemini-3.8-flash` is served from an EU regional Vertex endpoint, and which region; the design updated if not.
- [ ] Offline test: a scripted model reply comes back through the turn endpoint; a scripted loop stops at `max_llm_calls`.
- [ ] One bounded live call (≤ 5 requests) to the pinned model in the EU region returns a reply; the token count is recorded.
- [ ] No credentials in the repository; the model ID is not an alias.

Verification: `pytest -q` offline (cannot run in the planning session: ADK
not installed); one authorised live call from a developer machine.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
