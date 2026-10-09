---
goal: G01
title: Booking API client, fake and contract answers
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 2.5-4
  review_and_verify: 1-2
  total: 3.5-6
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Booking API client, fake and contract answers

## Outcome

Every other ticket codes against one typed booking API client and an in-memory fake, and the team knows whether writes accept an idempotency key (A5). Implements D3, D4.

## Scope

- In: `app/booking_api.py` (`BookingApi` protocol, HTTP client with per-call deadlines, `FakeBookingApi` with a commit-then-timeout mode); `docs/architecture/booking-api-contract.md` answering A5
- Out: tools, executor and retries on writes (G03); provider idempotency work (G11)
- Depth: staging only; credential from the environment, never committed; write timeouts map to `uncertain`

## Acceptance

- [ ] Contract tests pass against the fake and once against staging for a test customer
- [ ] A write timeout maps to `uncertain`, never `failed`
- [ ] No credential appears in code, tests or the contract note; no production URL is called

Verification: `pytest tests/test_booking_api.py` offline; `pytest -m staging` local integration, authorised against staging only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-client.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
