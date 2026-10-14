---
goal: G05
title: Only the signed-in customer's conversation and data are reachable, within a daily allowance
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-frontend-integration, adk-operational-guardrails]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 6-9
  review_and_verify: 3-4
  total: 9-13
  calendar_waits: none
owner: Dev C
status: ready
---

# G05 Only the signed-in customer's conversation and data are reachable, within a daily allowance

## Outcome

A FastAPI gateway around the Runner with verified identity (D2, D7). Implements I1 and I5.

## Scope

- In: Verify the booking app token (A7); `user_id = customer_id`; trusted state is set by code; session ownership is checked on every call
- In: `DatabaseSessionService` on Postgres; `POST /chat` returns `{messages[], proposal?}`
- In: Per-customer allowance of 40 turns a day, checked before any model call
- Out: Out: the widget (G06), the confirm route (G04 mounts it)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] A valid token completes a turn; a missing or forged token → 401 before the Runner runs
- [ ] Customer B using A's session ID → 404, and no events are read
- [ ] Turn 41 → limit message, with zero model calls in the capture

Verification: offline `pytest tests/test_gateway.py` with a test JWKS and a scripted model.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-gateway-identity.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
