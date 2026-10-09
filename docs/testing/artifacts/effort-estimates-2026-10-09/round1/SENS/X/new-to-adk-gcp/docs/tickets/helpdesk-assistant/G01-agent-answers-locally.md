---
goal: G01
title: An engineer chats locally with a pinned Gemini model on Vertex, and a runaway turn stops at 6 model calls
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [adk-operational-guardrails, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate: 4-6 h
status: ready
---

# G01 An engineer chats locally with a pinned Gemini model, with a call cap

## Outcome

`adk web` runs the `helpdesk_assistant` agent locally against `gemini-3.5-flash`
on Vertex AI, and a single user turn can never make more than 6 model calls.
Implements D1, D6 and invariant I5.

## Scope

- In: project skeleton (proposed layout in the plan), `pyproject.toml` with
  `google-adk==2.8.0` (confirm against what is installed and record it),
  `root_agent` with placeholder instruction and no tools, a
  `before_model_callback` call counter per invocation, `.env` git-ignored,
  a Cloud Billing budget alert at 50% and 100% of the allowance.
- Out: runbook search (G02), ticket drafts (G04), hosting (G03).
- Depth: floor only: pinned model and ADK, call cap, budget alert (which
  notifies, does not cap), no secrets in the repository.

## Acceptance

- [ ] One local `adk web` turn on Vertex returns an answer (≤ 5 live calls).
- [ ] A scripted-model test that keeps requesting calls stops the turn with the
      stop message; no 7th model call is made.
- [ ] No API key, token or project secret appears in tracked files.
- [ ] Installed ADK version, model ID and its lifecycle status (from
      `adk-model-and-output-contracts/assets/model-lifecycle-*.json`) recorded below.

Verification: offline `pytest tests/test_call_cap.py`; authorised live: one
local `adk web` turn on the user's GCP project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-agent-answers-locally.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
