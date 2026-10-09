---
goal: G02
title: Read-only assistant answers availability and "my appointments"
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design, adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 2.5–4
  review_and_verify: 2–3.5
  total: 4.5–7.5
  calendar_waits: none
owner: Dev B
status: ready
---

# G02 Read-only assistant answers availability and "my appointments"

## Outcome

in a local run, Priya asks "what's free Saturday morning at Northside for a cut?" and "when is my next appointment?" and gets correct answers from the fake API. D1, D7, D8, I4.

## Scope

- In: `app/agent.py` (`LlmAgent`, instruction v1 with today's date and salon list injected from state by code), the three read tools, a minimal FastAPI `/chat` around the Runner with `RunConfig(max_llm_calls=8)`, in-memory sessions for now. Choose and record the `google-adk` pin (2.8.0 assumed; consider ≥2.10.0 for production). Out: proposals (G03), auth (G04), persistence (G05).
- Route: `LlmAgent` + `FunctionTool`s; tools read `customer_id` from `tool_context.state` (G04 sets it; tests set it directly).
- Prerequisites: G01's fake (or a temporary one from the design's tool list).
- Depth: MVP; pinned model ID; bounded tool results (≤10 items, no notes fields). Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: `adk-tool-interface-design` (tool declarations, result bounds, errors); `adk-agent-instructions` (instruction v1, date/timezone templating); `adk-model-and-output-contracts` (pin `gemini-3.8-flash`, sampling, thinking setting)

## Acceptance

- [ ] scripted-model Runner test calls each read tool with valid args
- [ ] ambiguous "Saturday" across a DST change resolves to salon-local time
- [ ] a 9th model call in one turn stops with the designed message
- [ ] declaration dump shows no customer-ID parameter
- [ ] pinned ADK and model IDs recorded

Verification: offline `pytest` with a scripted model; a live smoke run against the fake API is optional and needs a Vertex AI project. Execution scope: local code; live model calls only if the team supplies a project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
