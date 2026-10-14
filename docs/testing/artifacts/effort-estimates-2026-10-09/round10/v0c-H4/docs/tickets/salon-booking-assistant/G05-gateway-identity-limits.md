---
goal: G05
title: A signed-in customer reaches only their own conversation, within limits
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-operational-guardrails]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev C
status: ready
---

# G05 A signed-in customer reaches only their own conversation, within limits

## Outcome

A FastAPI gateway verifies the existing customer JWT, derives `customer_id`, creates or loads only that customer's ADK sessions, enforces the allowance and kill switch, and runs the Runner with `max_llm_calls=8`. Implements D4, D8; invariants I1, I6.

## Scope

- In:
  - `app/api/gateway.py`: `POST /chat`, `GET /sessions/{id}`, JWT verification (issuer, audience, expiry, JWKS) — confirm against the auth code (A7) and record in `docs/booking-api-contract.md`
  - Session ownership check on every route, including `/operations/{id}/confirm` (shared dependency used by G04)
  - Allowance table (40 turns/customer/day, 20 turns/session) in Postgres; global and per-salon kill switch from config
  - Starts with a stub agent; swaps in G02's factory when merged
- Out: Widget (G06); Deployment (G09)
- Depth: Build. Floor: spend stop, no secrets in code. Deferred: shared reservations across instance pools (later).
- Supporting skills, purpose: adk-operational-guardrails: per-customer daily allowance, session turn cap, kill switch

## Acceptance

- [ ] Valid JWT → reply; expired, wrong audience or unsigned token → 401 with no model call
- [ ] Customer Y requesting customer X's session or operation → 404, no data, no model call
- [ ] 41st turn of the day or kill switch on → polite refusal with the salon phone, no model call

Verification: Offline `pytest tests/api` with locally signed test JWTs and a stub Runner; local integration with Docker Postgres.

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-gateway-identity-limits.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
