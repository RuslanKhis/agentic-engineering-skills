---
goal: G06
title: Signed-in chat API with customer-owned sessions
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-memory-architecture, adk-frontend-integration]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 5-8
  total: 8-12
  calendar_waits: none
owner: Dev C
status: blocked
---

# G06 Signed-in chat API with customer-owned sessions

## Outcome

Only the verified customer can chat in, resume or confirm operations in their own sessions. D3, D6, D8; invariant I1.

## Scope

- In: `app/server.py` FastAPI: token verification middleware, `POST /chat`, `POST /operations/{id}/confirm|decline`, `GET /operations/{id}`; session create/resume with owner check; `DatabaseSessionService` on Postgres; response schema `{reply, pending_operation?, operation_status?}`; 30-day session deletion script.
- Out: Widget (G07), limits and telemetry (G08).
- Depth: Build. `customer_id` only from the verified token; session IDs are locators, not permission.

## Acceptance

- [ ] Customer B cannot read, continue or confirm A's session or operation (403/404, no model call)
- [ ] Missing or expired token returns 401; the conversation continues after a process restart
- [ ] Response bodies validate against the schema and contain no internal IDs beyond operation ID

Verification: `pytest tests/test_server.py` with local Postgres and a test token issuer (local integration).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-chat-api-identity.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
