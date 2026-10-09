---
goal: G02
title: Assistant answers availability and lists my appointments
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 1.5-3
  review_and_verify: 2.5-4
  total: 4-7
  calendar_waits: none
owner: Dev B
status: ready
---

# G02 Assistant answers availability and lists my appointments

## Outcome

A customer asking "What's free Saturday morning with Sam at Elm St?" or "What do I have booked?" gets answers from the (fake) booking API, scoped to them. D1, D7.

## Scope

- In: `app/agent.py` agent factory with pinned model, `app/instruction.md` v1 with date and salon time zone injected from state, four read tools in `app/tools/read.py`, `app/fake_booking_api.py` fixtures for five salons, scripted-model offline tests. Record installed ADK version and Vertex availability of `gemini-3.8-flash` (fallback `gemini-3.5-flash`).
- Out: Propose tools (G05), HTTP server (G06), real API client (G03).
- Depth: Build. Floor: pinned model ID, `customer_id` read from trusted state only, results bounded (10 slots, 20 appointments), free-text notes stripped.

## Acceptance

- [ ] Scripted model calling `search_availability` gets at most 10 slots from the fake API
- [ ] `list_my_appointments` returns only the session customer's appointments; no tool declares a `customer_id` parameter
- [ ] ADK version and model/region choice recorded in the Evidence section

Verification: `pytest tests/test_read_tools.py tests/test_agent_offline.py` (offline); optional bounded live `adk web` session of at most 10 model calls on a named Vertex project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
