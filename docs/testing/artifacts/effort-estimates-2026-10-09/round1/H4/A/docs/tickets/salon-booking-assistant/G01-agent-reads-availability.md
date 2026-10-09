---
goal: G01
title: The agent finds real availability for a customer's request
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design (read tool declarations), adk-agent-instructions (prompt and state templating), adk-model-and-output-contracts (pinned gemini-3.8-flash, settings)]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate: 8-10 h
suggested_owner: Dev B (agent and Python)
status: ready
---

# G01 The agent finds real availability for a customer's request

## Outcome

In `adk web`, "any colour slots at Northside Saturday morning?" returns real slots from the fake booking API (staging after G00). Implements D1, D5 and the read half of the model-facing contract.

## Scope

- In: app/agent.py (LlmAgent + App/Runner, RunConfig max_llm_calls=8), app/prompts/booking_assistant.md, read tools list_services_and_salons / find_availability (≤10 slots) / list_my_appointments in app/tools/booking.py, read methods of app/booking_api/client.py, app/booking_api/fake.py. Today's date, time zone and salon list injected from state by code.
- Out: Propose tools and writes (G02), identity (G03 — use a fixed test customer in state until then), HTTP gateway (G04).
- Depth: Build at MVP depth; floor kept: pinned model ID, call cap, no secrets in code. Confirm ADK interfaces against the chosen pin (working assumption google-adk 2.8.0) and record the pin.

## Acceptance

- [ ] Scripted-model Runner test: read tools called with valid arguments and results bounded to 10 slots.
- [ ] An ambiguous salon or service produces a clarifying question, not a guessed tool call.
- [ ] No tool declaration exposes a customer identifier parameter; declaration dump under 3 KB.

Verification: pytest tests/test_agent_reads.py (offline); one adk web session on the pinned model (bounded live, within allowance).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-agent-reads-availability.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
