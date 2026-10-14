---
goal: G02
title: Local agent answers availability and "my appointments"
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts, adk-workflow-design]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev B
status: ready
---

# G02 Local agent answers availability and "my appointments"

## Outcome

Maya can ask "what does Jo have free on Saturday morning?" and "what's booked for me?" in `adk web` against a fake booking API. Implements D1, D5 and D8.

## Scope

- In and out: In: `app/agent.py` (one `LlmAgent`, pinned `gemini-3.8-flash`); `list_services`, `find_slots` and `list_my_appointments` in `app/tools/`, reading `customer_id` from state only; a fake `app/booking_client.py`; today's date and timezone injected into the instruction; Runner tests. Out: propose tools (G06) and the gateway (G04).
- Depth: Build. Floor: a pinned model, `max_llm_calls`, and no customer ID in tool parameters. Pin `google-adk` and confirm the APIs used against that version (working assumption 2.8.0).

## Acceptance

- [ ] Runner test with a scripted model: "Saturday morning with Jo" calls `find_slots` with the right date range and returns bounded results
- [ ] Tool declarations dumped, with no `customer_id` parameter. The ADK pin is recorded and its APIs are confirmed
- [ ] `list_my_appointments` with customer X in state never returns customer Y's appointments

Verification: Offline: `pytest tests/` with a scripted model. One manual `adk web` session, live model, fake API.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-local-agent-read-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
