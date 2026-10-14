---
goal: G02
title: The assistant answers "what's free at Camden on Saturday morning?" from booking data
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design, adk-model-and-output-contracts]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev A
status: blocked
---

# G02 The assistant answers "what's free at Camden on Saturday morning?" from booking data

## Outcome

A local ADK agent that lists services, finds slots and lists the customer's
appointments through the `BookingClient` from G01, using a fake client.
Implements D1, D6, D7 and the read part of the tool contract. Includes 1 h
handoff from Dev B (G01).

## Scope

- In: `app/agent.py` (one `LlmAgent`, pinned `gemini-3.8-flash` per D6),
  `app/tools/read.py` (`list_services`, `find_slots`, `list_my_appointments`
  reading `customer_id` from session state only), `app/booking_client.py`
  fake implementation with fixtures for five salons, `RunConfig(max_llm_calls=8)`,
  today's date and salon time zone injected into state before each turn,
  results bounded to 10 slots, notes fields dropped (D9). Pin
  `google-adk==2.8.0` and Python 3.11 in `pyproject.toml`.
- Out: propose tools (G05), real HTTP adapter (G03), token verification
  (G04 supplies `customer_id`; here a test fixture sets it), instruction
  polish (G07).
- Depth: MVP. Floor: pinned model, call cap, no secrets.

## Acceptance

- [ ] Confirm the ADK pin installs, and that `DatabaseSessionService` and `RunConfig.max_llm_calls` exist at that version; record in Evidence
- [ ] Confirm `gemini-3.8-flash` is offered on Vertex AI in the chosen region (documentation, dated)
- [ ] Runner test with a scripted model: `find_slots` returns at most 10 slots with IDs and no notes field
- [ ] No tool declaration has a `customer_id` parameter (declaration dump test)
- [ ] With the call cap at 8, a scripted model that loops on tool calls stops and returns the "can't help right now" message

Verification: offline `pytest tests/test_agent_read.py` with a scripted model; one manual `adk web` run against the fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G02-agent-skeleton-read-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
