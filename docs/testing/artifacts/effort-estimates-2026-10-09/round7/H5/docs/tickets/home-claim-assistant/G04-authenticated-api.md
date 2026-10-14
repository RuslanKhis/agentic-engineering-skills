---
goal: G04
title: Only the signed-in customer can use their session
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-frontend-integration]
blocked_by: [G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 20-32
  review_and_verify: 10-16
  total: 30-48
  calendar_waits: none
owner: Eng A
status: blocked
---

# G04 Only the signed-in customer can use their session

## Outcome

A JSON API (D8) that verifies the portal's OIDC token, derives `customer_id`, binds sessions to it and checks the owner on every route. Implements D3, I4.

## Scope

- In: `app/api/` routes `/sessions`, `/turns`, `/status`; token verification against a fake CIAM issuer in tests; `DatabaseSessionService` on Postgres; trusted state key for `customer_id`.
- Out: photo routes (G07), submit (G11), real CIAM client (W5, used in G12).
- Depth: build; customer ID never accepted from body or model.

## Acceptance

- [ ] A valid token creates a session and a turn returns a completed reply
- [ ] Expired, wrong-audience or unsigned tokens get 401
- [ ] Customer B using customer A's session ID gets 404 on every route and nothing is written

Verification: Offline: `pytest tests/api` with fake issuer; local integration with a real Postgres restart.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G04-authenticated-api.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
