---
goal: G01
title: Booking API contract, typed client and fake
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Booking API contract, typed client and fake

## Outcome

Settle A7 and A8 against the real booking API, and give every other goal a typed client and an in-memory fake. Implements D4, D5, D6.

## Scope

- In: Ask the chain owner for go-live approval and the name of the pilot salon (G10 wait); confirm the ADK pin (2.8.0) and `gemini-3.8-flash` availability in the region
- In: `assistant/booking_client.py`: availability, create, reschedule, cancel, list-mine, lookup; timeouts and typed errors (`conflict`, `not_found`, `uncertain`)
- In: `tests/fakes/booking_api.py` with scripted conflict, timeout-after-commit and idempotent replay
- In: If the API lacks `Idempotency-Key` or atomic reschedule: add it to the API, or record the D5 fallback
- Out: Contract notes in `docs/architecture/booking-api-contract.md`. Out: agent and tools (G02, G03)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] A7 and A8 answered in the design's Assumed answers table, with evidence (endpoint, staging call)
- [ ] The fake replays the same idempotency key with no second booking; a timeout after commit returns `uncertain`
- [ ] No credentials in the repo; the staging token comes from the environment

Verification: offline `pytest tests/test_booking_client.py` plus one authorised staging read call.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
