---
goal: G04
title: Signed-in customer reaches only their own data
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-operational-guardrails, adk-frontend-integration]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 6-8
  review_and_verify: 3-4
  total: 9-12
  calendar_waits: none
owner: Dev C
status: ready
---

# G04 Signed-in customer reaches only their own data

## Outcome

Implements D3, D9 and D10 (server side) and invariants I1 and I5. Step 1 settles A5: how our service verifies the booking site's customer token.

## Scope

- In and out: In: `app/gateway.py` (FastAPI) with `POST /chat`, `POST /confirm/{id}` (calls G03's `confirm_operation`, stubbed until merged) and `GET /operations/{id}`; token verification, then `customer_id` and `salon_id` written into session state the client cannot set; session ownership check; 30 turns per customer per day; `RunConfig(max_llm_calls=12)`; `ASSISTANT_ENABLED` kill switch. Built against a stub agent. Out: widget (G05), deploy (G07).
- Depth: Build. Floor: no token or message text in logs.

## Acceptance

- [ ] A valid token reaches the agent with the right `customer_id` in state. The verification method is recorded in the design (A5)
- [ ] Customer X using customer Y's session ID or operation ID gets 404 and no Runner call
- [ ] The 31st turn of the day and the kill switch both return the phone-number message with no model call

Verification: Offline: `pytest tests/test_gateway.py` with FastAPI TestClient, a stub agent and signed test tokens.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-identity-gateway.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
