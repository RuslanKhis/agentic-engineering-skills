---
goal: G03
title: A staff member chats in a signed-in page and confirms a ticket card
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01]
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  calendar_waits: none
owner: Dev A
status: blocked (ready when G01 is complete)
---

# G03 A staff member chats in a signed-in page and confirms a ticket card

## Outcome

IAP-verified identity owns sessions and proposals; the page renders answers safely and the proposal card. Implements D6; guarantees I1, I2.

## Scope

- In: IAP JWT middleware in `app/server.py`, `/api/chat` around the Runner with server-derived `user_id`, `app/static/index.html` with safe Markdown and the card calling G02's endpoint.
- Out: streaming polish, history list, deployment (G04).
- Depth: build identity and ownership; floor: no remote images, links only to Atlassian domains.

## Acceptance

- [ ] Valid IAP token reaches chat; a full local journey with fakes ends at a ticket key
- [ ] Missing, forged or wrong-audience token → 401
- [ ] User B gets 404 on user A's session and proposal; an answer with a remote image and a foreign link renders neither

Verification: offline `pytest tests/test_iap_middleware.py tests/test_sessions.py`; local browser run against fakes.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G03-iap-page-and-sessions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
