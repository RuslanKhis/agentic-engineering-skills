---
goal: G04
title: Technicians use a signed-in page that shows only their own chats and drafts
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01, G03]
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 1-2
  review_and_verify: 2-3
  total: 3-5
  calendar_waits: none
owner: Engineer B
status: blocked
---

# G04 Technicians use a signed-in page that shows only their own chats and drafts

## Outcome

A browser page for chat shows answers with links, a draft card with a Create button and the issue key. The user ID always comes from the verified IAP JWT. Implements D4, D7 and invariant I2. Every decision is provisional on the assumed answers at the top
of the design. The implementation route is in the plan's G04 section.

## Scope

- In: `web/main.py` (IAP JWT middleware, `POST /api/chat`, `GET /api/drafts/{id}`, `POST /api/drafts/{id}/confirm`), one static HTML/JS page, the created key written to session state via an event `state_delta` (check this API against the pin)
- Out: streaming, Google Chat, durable sessions (G06)
- Depth: authenticated page at internal-tool depth. Floor: `user_id` never taken from the request; a local-dev auth bypass starts only when the environment is explicitly `local`.

## Acceptance

- [ ] No JWT or an invalid one: 401
- [ ] User B gets 404 for user A's session or draft and cannot confirm it
- [ ] Full journey through the API with fakes: question, then answer with URL, then draft, then confirm, then key
- [ ] After the runner is rebuilt (simulated restart), confirming an existing draft still works
- [ ] The bypass refuses to start when the environment is not `local`

Verification: `pytest tests/test_web.py` with FastAPI TestClient and test-signed JWTs (offline), then a manual browser check locally.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G04-signed-in-page-per-user-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
