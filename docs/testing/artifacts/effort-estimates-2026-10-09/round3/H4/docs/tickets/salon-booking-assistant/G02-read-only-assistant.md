---
goal: G02
title: Read-only assistant answers availability and my appointments locally
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 2-3.5
  review_and_verify: 1-1.5
  total: 3-5
  calendar_waits: none
owner: Dev A
status: blocked
---

# G02 Read-only assistant answers availability and my appointments locally

## Outcome

"What's free with Jo on Saturday morning at Riverside?" returns at most 10 correct slots in the salon's time zone, and "what have I got booked?" lists only the caller's appointments. Implements D1 and the model-facing contracts.

## Scope

- In: `app/agent.py` (LlmAgent, instruction `booking-v1`, `RunConfig(max_llm_calls=12)`), `app/tools/read.py` (`list_services`, `find_slots`, `list_my_appointments`); pin `google-adk` (working assumption 2.8.0) and `gemini-3.8-flash` after checking Vertex availability in region
- Out: propose tools (G03), gateway and real identity (G04)
- Depth: `customer_id`, `today`, `salon_tz` come from state (test fixture until G04); no customer contact fields in tool results

## Acceptance

- [ ] Scripted-model Runner tests choose the right tool and arguments for 5 phrasings
- [ ] Past dates or dates > 60 days ahead return an actionable error
- [ ] No tool has a customer-ID parameter; the captured model request has no phone or email

Verification: `pytest tests/test_agent_read.py` offline; one manual `adk web` session against the fake (≤ 20 model calls).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
