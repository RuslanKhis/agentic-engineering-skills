---
goal: G02
title: The assistant knows who the customer is and serves only their own sessions
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-frontend-integration]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, 1.5x new-to-ADK applied
  hands_on: 3-6
  review_and_verify: 3-5
  total: 6-11
  calendar_waits: none
owner: Dev B
status: ready
---

# G02 Verified customer identity and session ownership

## Outcome

A FastAPI gateway (D3, D8) verifies the booking site's customer token,
derives `customer_id`, creates and owns ADK sessions for that customer, and
refuses any request for another customer's session. Implements I1 at the
ingress.

## Scope

- In: first, settle O1 (how our backend verifies the site token) and record
  it; `assistant/gateway.py` with token middleware, `POST /chat`,
  `GET /session`, session owner check before `Runner.run_async`,
  `customer_id` written to session state by code; works with a stub agent so
  it does not wait for G01. The JSON contract for `/chat` (text + optional
  proposal card) as a typed schema, shared with G04.
- Out: confirm endpoint (G03), rate limits and caps (G06), widget (G04).
- Depth: MVP Build. Floor: no tokens or keys logged; signing keys or
  introspection secret from environment/Secret Manager only.

## Acceptance

- [ ] Valid token → session created with `customer_id` from the token, not from the request body.
- [ ] Expired, forged or missing token → 401, no Runner call.
- [ ] Customer A requesting customer B's session ID → 404, no history disclosed, no Runner call.
- [ ] A `customer_id` sent in the request body or message text is ignored.

Verification: offline `pytest` with locally signed test tokens and an
in-memory session service.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-verified-customer-identity.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
