---
goal: G02
title: Read-only assistant answers availability questions locally
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 2-3
  total: 5-8
  calendar_waits: none
  wait_days: 0
owner: Dev A
status: ready
---

# G02 Read-only assistant answers availability questions locally

## Outcome

In `adk web`, a fixture customer asks "what's free with Jo on Saturday at Northside?" and gets correct slots from the fake booking API. D1, D2 (read half), D6. Route and rationale: [plan, G02](../../plans/salon-booking-assistant.md#g02--read-only-assistant-runs-locally).

## Scope

- In: `booking_assistant/agent.py`, `prompts/instruction.md`, `tools/read.py`, `booking_client.py` protocol, `fake_booking.py` (five salons)
- Out: proposals (G04), gateway (G03), hosting (G09)
- Depth: pinned model `gemini-3.8-flash`, `google-adk==2.8.0` confirmed or changed with a note; `max_llm_calls`; `customer_id` read from state only

## Acceptance

- [ ] Slot and appointment results bounded to 10; a tool error returns `status: error` and the agent offers the salon phone
- [ ] Declaration dump shows no `customer_id` parameter on any tool
- [ ] No tool can change a booking

Verification: offline `pytest` with a scripted model; one manual `adk web` run (small model spend).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
