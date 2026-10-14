---
goal: G01
title: A signed-in customer asks for free slots or their appointments and gets correct answers
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, 1.5x new-to-ADK applied
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Read-only assistant answers availability and "my appointments"

## Outcome

A local `LlmAgent` (D1, D2) with `search_availability`, `list_my_appointments`
and `get_salon_info` answers "what's free Saturday morning at Riverside with
Jo?" and "when is my next appointment?" from the booking API, with
`customer_id` read from session state (I1), never from model arguments.

## Scope

- In: `assistant/booking_client.py` (typed adapter + in-memory fake),
  `assistant/tools/booking.py` read tools, `assistant/agent.py` with
  instruction v1 (salon list, today's date and time zone from state);
  confirm the ADK pin (O2) and record it; first step: send the W1 request to
  the salon chain.
- Out: write/propose tools (G03), gateway and auth (G02), deployment (G06).
- Depth: MVP. Floor: model ID pinned, API key from environment only, results
  capped at 10 items, no phone/email fields in tool results (D9).

## Acceptance

- [ ] Scripted-model Runner test: availability and my-appointments questions call the right tool with valid arguments; results bounded to 10.
- [ ] API error or empty result returns an actionable `{status: ...}`, and the agent says so instead of inventing slots.
- [ ] No tool declaration has a `customer_id` parameter; a test with state `customer_id=A` never returns customer B's appointments from the fake.
- [ ] Rendered request shows instruction v1 with the injected date and ≤ 6 declarations.
- [ ] ADK version pinned in the dependency file; W1 request sent (date recorded).

Verification: offline `pytest` with fake booking client and scripted model;
one bounded live call against the staging booking API, if authorized.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
