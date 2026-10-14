---
goal: G03
title: Only the logged-in customer can use and see their conversation
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-memory-architecture, adk-operational-guardrails]
blocked_by: []
mentions_only: [G02, G06, G07]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 3-7
  total: 8-15
  calendar_waits: none
owner: Dev B
status: ready
---

# G03 Only the logged-in customer can use and see their conversation

## Outcome

The gateway turns the website's login token into a trusted `customer_id`,
binds each ADK session to its owner, and enforces the per-customer allowance
and the kill switch before any model call. Implements D3, D6, D8 (`/config`,
CORS) and D9 (gateway part). Depends on
assumption Q2; if the website token cannot be verified, stop and report.

## Scope

- In: FastAPI gateway `POST /chat` wrapping `Runner` with
  `DatabaseSessionService` (local Postgres in tests); JWKS-based token
  verification with key caching; session owner check; daily allowance (40
  turns) and 1,000-character cap; same-session serialization; global and
  per-salon flags (a `feature_flags` table) with `GET /config` and the 503
  "assistant off" response; CORS allowlist of the website's origins.
- Out: widget (G06), deployment (G07), proposal confirm route (wired in G08).
  Uses a placeholder agent in tests so it does not wait for G02.
- Depth: MVP build with careful review (authorization boundary).

## Acceptance

- [ ] A1 Valid website token → `customer_id` from the verified subject; a new session stores it in state at creation; the agent runs.
- [ ] A2 Missing, expired, wrong-audience or forged-signature token → 401, no model call, no session write.
- [ ] A3 Customer B sends customer A's `session_id` → 404, no read of A's events, no model call.
- [ ] A4 JWKS endpoint unavailable, slow (2 s timeout) or rate limited → cached keys used until their TTL, then 503 fail-closed; never accept an unverified token.
- [ ] A5 Restart the process; the same customer resumes the same session with history intact.
- [ ] A6 The 41st turn of a day or a message over 1,000 characters returns the limit message with no model call.
- [ ] A7 A second request on a session while one is in flight → 409 "still working"; events are not interleaved.
- [ ] A8 Postgres unavailable, connection pool exhausted, permission denied or schema missing → 503 with an honest message, no model call; the readiness check fails so a new revision with a missing migration takes no traffic.
- [ ] A9 Global flag off, or the customer's salon flag off → `/chat` and `/proposals/{id}/confirm` return 503 "assistant off" with no model or provider call; `GET /config` reports the flags; flipping a flag takes effect on the next request without a redeploy.

Verification: offline `pytest tests/gateway/` with a local JWKS fixture and
Postgres in Docker; one manual run with a real staging website token.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-verified-customer-sessions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
