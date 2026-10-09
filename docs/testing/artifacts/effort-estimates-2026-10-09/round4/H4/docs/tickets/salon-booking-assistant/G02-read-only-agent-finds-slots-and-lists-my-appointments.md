---
goal: G02
title: Read-only agent finds slots and lists my appointments
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design, adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev B
status: blocked
---

# G02 Read-only agent finds slots and lists my appointments

## Outcome

A customer can ask "can I get a cut at Northgate on Friday afternoon?" and get real, bookable slots. They can also ask "what have I got booked?" and see only their own appointments. Implements D1, D7, D8 and D9.

## Scope

- In:
  - `app/agent.py`: one `LlmAgent` with four read tools: `list_salons_and_services`, `find_slots`, `list_my_appointments` and `salon_contact`.
  - The instruction `app/prompts/booking_v1.md`.
  - Injected state: today's date, each salon's time zone, and `customer_id` from trusted state.
  - `RunConfig(max_llm_calls=12)` and the pinned model in one config module.
- Out: Writes (G03) and the HTTP API (G05).
- Depth: MVP. Tool results are bounded to at most 10 slots and leave out phone, email and notes. No secrets in code or the prompt.
- Implementation route: `LlmAgent` with `FunctionTool`s over `booking_client`. Code resolves relative dates in the salon's time zone, so `find_slots` takes ISO dates. Confirm these names on the chosen pin: `LlmAgent`, `App`, `Runner`, `RunConfig.max_llm_calls`, `ToolContext.state`. Record the pin in `pyproject.toml`.
- Prerequisites: G01's fake and contract.
- Supporting skills: Adk-tool-interface-design: tool declarations and bounded results; adk-agent-instructions: the booking instruction and its rendered-request test; adk-model-and-output-contracts: the pinned model and thinking settings.
- Execution scope: Local, plus the dev Vertex AI project for the manual session.

## Acceptance

- [ ] With a scripted model, `find_slots` receives the resolved salon, service and date window.
- [ ] The reply offers only slots the fake returned.
- [ ] `list_my_appointments` uses the trusted `customer_id` even when the user's text names another customer.
- [ ] The run stops at 12 model calls.
- [ ] A captured model request contains no phone number or email.

Verification: Offline Runner tests with a scripted model and the fake (`pytest tests/test_agent_read.py`). One manual `adk web` session against the fake with the live model, transcript saved.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-agent-finds-slots-and-lists-my-appointments.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
