---
goal: G03
title: A signed-in helpdesk member chats with the assistant in a simple page and sees only their own sessions
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets, adk-agent-security]
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

# G03 Authenticated chat page

## Outcome

A FastAPI app verifies the IAP JWT, runs the agent with that user's ID and
server-generated, owner-scoped sessions, and serves a minimal page with
cited answers and a read-only draft card with Copy (D5, D9; I1, I2).

## Scope

- In: `web/app.py` middleware verifying the signature and audience of
  `x-goog-iap-jwt-assertion` (test signer locally); `POST /chat`,
  `GET /sessions`; agent factory interface, with a stub agent until G01 lands;
  escaped rendering with links only to the Confluence and Jira hosts and no
  images; citations taken from tool results.
- Out: hosting and real IAP (G04); Create button (G06).
- Depth: build; careful review of the auth path.

## Acceptance

- [ ] A valid JWT chats; a missing, forged or wrong-audience JWT → 401 with no Runner call.
- [ ] User B using user A's session ID → 404; a client-sent `user_id` is ignored.
- [ ] `![x](https://evil/?q=secret)` and a non-allow-listed link render as inert text.

Verification: offline `pytest` with FastAPI TestClient and a stub or scripted agent.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G03-authenticated-chat-page.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
