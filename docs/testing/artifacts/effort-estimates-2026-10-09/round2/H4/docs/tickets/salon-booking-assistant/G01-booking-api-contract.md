---
goal: G01
title: Booking API contract and fake
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 3–4
  review_and_verify: 1.5–2
  total: 4.5–6
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Booking API contract and fake

## Outcome

the team knows exactly how the assistant reads and writes appointments, and everyone tests against the same fake. Settles A6, A7; feeds D3, D4, D5.

## Scope

- In: read the booking API code/docs; write `docs/booking-api-contract.md` (endpoints for salons, services, slots, customer appointments, create, move, cancel; auth; error codes; slot uniqueness; idempotency key or status lookup support; timezone handling; staging URL); write `app/booking_client.py` interface and `tests/fakes/booking_api.py` with scriptable outcomes (success, conflict, timeout-after-commit, 5xx). Record how the website's customer token can be verified (A7). Out: any change to the booking API itself (if idempotency keys are missing, record it as a phase 2 item; D4's reconciliation still works).
- Route: plain Python client with per-call deadline; no ADK.
- Prerequisites: read access to the booking API repository.
- Depth: MVP; no real customer data in fixtures. Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: `adk-tool-auth-and-secrets` (record how the service credential and customer token work)

## Acceptance

- [ ] contract doc answers each open question in the design's Open decisions rows A6/A7 with a file:line pointer into the API code
- [ ] the fake reproduces commit-then-timeout
- [ ] client tests pass offline

Verification: `pytest tests/test_booking_client.py` offline; no network. Execution scope: local code only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
