---
goal: G04
title: Each helpdesk agent chats in a page and sees only their own conversations
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: internal tool
estimate:
  hands_on: 3-4
  review_and_verify: 2-3
  total: 5-7
  calendar_waits: none
owner: Dev B
status: ready
---

# G04 Each helpdesk agent chats in a page and sees only their own conversations

## Outcome

A FastAPI app derives `user_id` from a verified IAP JWT and serves a minimal chat
page; runs against a stub agent until G01 lands (D3, D7, D9; I1, I2).

## Scope

- In: `app/api.py` (JWT signature and audience check, create/list/continue own sessions, streamed reply), `app/static/` page rendering model text escaped, no auto-loaded images or links.
- Out: Cloud Run and IAP setup (G05); ADK dev UI is not served.
- Depth: authorization boundary gets a careful review; in-memory sessions (D7).

## Acceptance

- [ ] Valid JWT for user A creates and continues A's session.
- [ ] Missing, expired or wrong-audience JWT → 401; a `user_id` in the request body is ignored.
- [ ] A's token with B's session ID → 404, no content returned.
- [ ] A reply containing `![x](https://evil/?q=…)` renders as text.

Verification: offline `pytest` with locally signed test JWTs and a stub agent.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G04-identity-bound-chat.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
