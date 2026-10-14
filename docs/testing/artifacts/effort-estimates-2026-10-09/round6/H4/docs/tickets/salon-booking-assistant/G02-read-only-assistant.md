---
goal: G02
title: A signed-in customer asks about services, free slots and their appointments
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-workflow-design]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev B
status: blocked
---

# G02 A signed-in customer asks about services, free slots and their appointments

## Outcome

One `LlmAgent` (D1) answers read questions using real data from the fake or staging API. Implements I1 for reads.

## Scope

- In: `assistant/agent.py`: `App` and `LlmAgent` with model `gemini-3.8-flash`; instruction with injected date, salon time zone and first name
- In: Read tools `find_services`, `find_slots`, `my_appointments`: `customer_id` from `tool_context.state`, results bounded to 10, no contact fields
- In: `RunConfig(max_llm_calls=10)`
- Out: Out: propose tools (G03), gateway (G05)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] "Free slots with Sam at Northside next Tuesday after 5" lists only slots the fake returned
- [ ] A scripted model passing another customer's appointment ID gets `not_found` and discloses nothing
- [ ] The captured request shows no `customer_id` parameter in any tool declaration

Verification: offline `pytest tests/test_agent_read.py` with a scripted model through the Runner.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
