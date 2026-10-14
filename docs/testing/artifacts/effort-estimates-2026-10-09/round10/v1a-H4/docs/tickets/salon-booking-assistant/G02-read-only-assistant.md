---
goal: G02
title: A signed-in customer asks for free slots and her own appointments and gets true answers
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design, adk-agent-instructions, adk-tool-auth-and-secrets]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 1.5-3
  total: 5.5-9
  calendar_waits: none
owner: Dev A
status: blocked
---

# G02 A signed-in customer asks for free slots and her own appointments and gets true answers

## Outcome

`assistant/agent.py` builds an `App` with one `LlmAgent` on the pinned model
(D1, D7) and three read tools: `list_salons_and_services`, `find_slots` and
`list_my_appointments`. `customer_id` comes only from app-owned session state
(D2, I1). Answers quote only tool data (I5).

## Scope

- In: the agent factory, the instruction module (today's date and the salon
  timezone injected from code), the three tools with bounded results (at most
  10 slots) and actionable error dicts, a booking read client with a 5 s
  timeout and one retry, a fake booking API fixture for tests, and
  `RunConfig(max_llm_calls=10)`.
- Out: write tools, HTTP API and widget (later goals G04, G05).
- Depth: MVP; the floor is pinned model, no secrets in code, and no customer
  argument on any tool.

## Acceptance

- [ ] Scripted-model Runner test: "Saturday morning with Alex at Downtown" calls `find_slots` with the resolved IDs and the reply lists only fixture slots.
- [ ] Booking API timeout yields the "can't reach bookings, use the booking page" reply after one retry; no invented times.
- [ ] Forbidden: no tool declaration has a customer or token parameter (declaration dump), and a session whose state lacks `customer_id` makes zero booking API calls.
- [ ] Rendered-request test shows the instruction with the injected date and six or fewer tool declarations.

Verification: `pytest tests/agent` offline with a scripted model and the fake API. One bounded live
smoke against Vertex and staging, with at most 5 model calls.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
