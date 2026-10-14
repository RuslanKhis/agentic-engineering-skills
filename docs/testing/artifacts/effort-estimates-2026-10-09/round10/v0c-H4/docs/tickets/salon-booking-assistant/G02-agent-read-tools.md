---
goal: G02
title: A customer can ask about services, free slots and their own appointments
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
owner: Dev B
status: ready
---

# G02 A customer can ask about services, free slots and their own appointments

## Outcome

Locally, `adk run`/a test Runner answers "what's free with Jo on Saturday morning at Riverside?" and "when is my next appointment?" from a fake booking API, with the customer ID taken from session state. Implements D1, D5 (read side), D10.

## Scope

- In:
  - Project skeleton: `pyproject.toml` with `google-adk` pinned (confirm 2.8.0 or record the chosen pin), `app/agent/agent.py` factory, `app/agent/instruction.md` (v1)
  - `app/booking/client.py` read methods and `tests/fakes/booking_api.py`
  - Tools `list_services`, `find_slots` (≤ 8 slots, opaque `slot_id`, salon-local and absolute times), `list_my_appointments` (customer ID from `tool_context.state`, never a parameter)
  - `RunConfig(max_llm_calls=8)` in the runner helper; today's date and salon time zones injected into state
- Out: Proposal tools (G03); Gateway/JWT (G05); Eval set (G07)
- Depth: Build at MVP depth. Floor: pinned model ID, no secrets in code, call cap. Deferred: per-customer allowance (G05).
- Supporting skills, purpose: adk-agent-instructions: instruction v1 with date/salon state templating; adk-model-and-output-contracts: pin gemini-3.8-flash and its settings

## Acceptance

- [ ] Offline tests: each tool returns the bounded, status-carrying result; `find_slots` across a DST change returns correct absolute times
- [ ] No tool declaration has a `customer_id` parameter (declaration dump test); a test with customer Y's state never returns customer X's appointments
- [ ] Booking API unavailable → tool returns `status: error` with an actionable message, agent replies with the salon phone
- [ ] ADK pin confirmed and recorded in the ticket's Evidence

Verification: `pytest tests/agent` offline with a scripted model where possible; one bounded live call to Vertex (≤ 5 requests) once credentials exist. Not runnable in the design session (ADK not installed).

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-agent-read-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
