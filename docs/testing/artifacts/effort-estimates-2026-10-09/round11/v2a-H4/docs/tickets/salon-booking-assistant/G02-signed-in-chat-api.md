---
goal: G02
title: A signed-in customer can chat, and only with their own session
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-frontend-integration, adk-memory-architecture]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 3-5
  review_and_verify: 2-3
  total: 5-8
  calendar_waits: none
owner: Dev C
status: ready
---

# G02 A signed-in customer can chat, and only with their own session

## Outcome

The chat API (`POST /chat`, design "Chat API contract") verifies the existing
login's token, binds the ADK session to the verified customer and puts
`customer_id` into trusted session state each turn. Implements D2, D7 (sessions)
and invariant I1 at the entry point.

## Scope

- In: FastAPI app, token verification against the existing login's JWKS (first
  step: confirm Q6; if there is no verifiable token, stop and record OD1),
  session ownership check, `DatabaseSessionService` on Postgres (local Postgres
  in tests), a stub agent for tests.
- Out: admission and logging controls, confirm endpoints, the real agent.
- Depth: Build at MVP depth; careful review of the auth boundary.

## Acceptance

- [ ] A1 A valid customer token gets a reply, and the ADK session's `user_id`
  equals the verified customer ID.
- [ ] A2 Missing, expired, wrong-audience or badly signed token → 401; the
  Runner is not invoked (no model call recorded).
- [ ] A3 Customer B posting to, or reading, customer A's `session_id` → 404;
  no events read, no model call.
- [ ] A4 JWKS endpoint unavailable or rate limited → cached keys used until
  they expire, then 503 "sign-in unavailable"; never an unauthenticated
  fallback.
- [ ] A5 `customer_id` in state is overwritten from the verified token on every
  turn; a test that tampers with the stored value sees it replaced.
- [ ] A6 After a process restart the same customer resumes the same session.
- [ ] A7 A token that expires mid-conversation → 401 with "please sign in
  again"; nothing is executed on the customer's behalf.
- [ ] A8 A token signed with a rotated key (unknown `kid`) triggers one JWKS
  refetch; a key that is still unknown or has been revoked → 401.

Verification: offline tests with locally signed test tokens and a local
Postgres; `pytest tests/api` (proposed path).

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-signed-in-chat-api.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
