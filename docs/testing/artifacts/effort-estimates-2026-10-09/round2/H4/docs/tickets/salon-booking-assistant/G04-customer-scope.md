---
goal: G04
title: Signed-in customer sees only their own appointments
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-agent-security]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 3–6
  review_and_verify: 3–6
  total: 6–12
  calendar_waits: none if the website is the team's own
owner: Dev C
status: ready
---

# G04 Signed-in customer sees only their own appointments

## Outcome

only a verified customer can chat, and every read and confirm is scoped to them. D3; I1.

## Scope

- In: `app/auth.py` verifying the website token (per G01's finding); session creation writes `customer_id` into state; session ownership check on every `/chat` and `/proposals/*` call; denial responses. Out: one-time-code login (only if A7 is false — then stop and re-plan per the design's D3 note).
- Route: FastAPI dependency before the Runner; tools trust only state.
- Prerequisites: G01's A7 answer; the website's token verification key.
- Depth: MVP build; signing keys from Secret Manager or JWKS, never in code. Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: `adk-agent-security` (cross-customer denial cases)

## Acceptance

- [ ] missing/forged/expired token → 401, Runner not invoked
- [ ] customer A using B's session ID → 404
- [ ] A naming B's appointment ID in chat → tool returns not-found and the fake API saw only A-scoped calls
- [ ] A confirming B's proposal → 404, zero writes

Verification: offline `pytest` with test-signed tokens. Execution scope: local code only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-customer-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
