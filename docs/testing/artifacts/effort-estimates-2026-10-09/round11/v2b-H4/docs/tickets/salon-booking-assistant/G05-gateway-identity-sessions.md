---
goal: G05
title: Only a signed-in customer reaches the assistant, in their own conversation, within a daily allowance
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-operational-guardrails, adk-memory-architecture]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 6-8
  review_and_verify: 3-5
  total: 9-13
  calendar_waits: none
owner: Dev C
status: ready
---

# G05 Only a signed-in customer reaches the assistant, in their own conversation, within a daily allowance

## Outcome

FastAPI gateway around the ADK `Runner`: verifies the website JWT, derives
`customer_id`, owns session lookup and creation, enforces the allowance and kill
switch, and exposes the public JSON routes. Implements D3, D6 (sessions), D10, D11 (logs).
Uses a stub agent with a scripted model and a mock confirm service; the real
ones are wired in by the integration goal (G09). Includes adding our token
audience to the website's login (Q16).

## Scope

- In: `app/gateway/` (auth dependency, routes, allowance, kill switch, logging), `DatabaseSessionService` on local PostgreSQL, 30-day session delete job, token audience configuration on our website.
- Out: chat page, Cloud Run, the agent's tools.
- Depth: MVP. If Q5 is wrong (token not verifiable), stop and report: G15 replaces part of this ticket.

## Acceptance

- [ ] A1 Valid website JWT: `customer_id` from the verified subject is written to session state before the Runner runs; the reply returns.
- [ ] A2 Missing, expired, wrong-audience, wrong-issuer or forged token: 401, no Runner invocation, no model call.
- [ ] A3 A session ID owned by another customer: 404, no model call, no content returned.
- [ ] A4 The 41st turn in a day for one customer gets 429 with the salon phone number and no model call; with the kill switch on, every chat returns the same message without a model call while the (mock) confirm/status routes still work.
- [ ] A5 Sessions persist across a gateway restart (local PostgreSQL); sessions older than 30 days are deleted by the job and only those.
- [ ] A6 Logs carry request, session, invocation and hashed customer IDs and token counts, and no message text or token (log-capture test).
- [ ] A7 JWKS endpoint down or rate limited: cached keys used up to 1 h, then 503; never an unauthenticated fallback. A token signed with a new key ID triggers one JWKS refresh (at most once a minute); a removed key is rejected after refresh.
- [ ] A8 Vertex AI unavailable, 429 or a blocked/rejected response (scripted): the SDK's own retry only, then a "temporarily unavailable" reply; no proposal stored.
- [ ] A9 Database unavailable or connection pool exhausted: chat returns 503 before any model call.
- [ ] A10 Two concurrent chat turns on one session (two tabs): the second gets 409 "still answering" and no events interleave in the stored session.

Verification: `pytest tests/gateway/` with local PostgreSQL and a local JWKS fixture (needs google-adk installed).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-gateway-identity-sessions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
