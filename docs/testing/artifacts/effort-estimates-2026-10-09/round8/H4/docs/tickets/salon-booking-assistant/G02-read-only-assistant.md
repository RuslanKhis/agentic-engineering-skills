---
goal: G02
title: The assistant answers availability and "my appointments" questions
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [adk-agent-instructions, adk-tool-interface-design, adk-model-and-output-contracts]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 2-3
  total: 8-12
  calendar_waits: none
owner: Dev B
status: blocked
---

# G02 The assistant answers availability and "my appointments" questions

## Outcome

A customer asks "what's free with Sam next Tuesday after 5?" or "when is my next appointment?" and gets a correct answer from the fake API (D1, D7).

## Scope

- In: Project skeleton and CI running unit tests; `assistant/agent.py` agent factory; read tools `list_salons_and_services`, `search_availability`, `list_my_appointments` and `salon_contact`, with results capped at 10 and `customer_id` and the token read from trusted context, never from arguments; instruction v1 with templated date and time zones; `RunConfig(max_llm_calls=8)`; pinned model ID.
- Out: Proposal tools (G04); HTTP gateway (G05).
- Depth: Build. Keep the floor: pinned model, call cap, no token in state.

## Acceptance

- [ ] Runner tests with a scripted model cover an availability search and the customer's own appointments
- [ ] A model-supplied `customer_id` argument does not exist in any declaration (declaration dump test)
- [ ] The rendered request shows today's date and the salon time zone, filled by code

Verification: offline Runner tests with a scripted model and the G01 fake; not runnable in this design session (google-adk not installed).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
