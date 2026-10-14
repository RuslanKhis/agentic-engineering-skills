---
goal: G05
title: Chat API and embeddable widget
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-operational-guardrails, protect-adk-sensitive-data]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-7
  review_and_verify: 2-3
  total: 7-10
  calendar_waits: none
owner: Dev C
status: ready
---

# G05 Chat API and embeddable widget

## Outcome

A customer on the pilot salon's page opens a chat, talks to the assistant, and
clicks Confirm on a card; the click goes straight to the backend, not through
the model. Implements D5, the admission part of D8 and the log part of D9
(I6, I7).

## Scope

- In: `app/api.py` (FastAPI) owning the ADK `Runner` with
  `DatabaseSessionService` (SQLite locally); `POST /chat` returning completed
  JSON `{messages, card?, status}`; `GET /operations/{op_id}` and
  `POST /operations/{op_id}/confirm` calling the `OperationService` interface
  from the design (built against a stub until G03 merges; real wiring is a
  one-line change checked in G09); signed HttpOnly session cookie with a
  server-generated session ID; 409 on overlapping turns; per-session turn cap
  and per-IP daily session cap; `ASSISTANT_ENABLED` kill switch; 20 s turn
  deadline; log filter dropping message bodies, phone and email patterns.
  `web/widget.js` (one script tag) rendering messages, the card and a polling
  state for a lost confirm response. Works with a stub agent; uses G02's
  factory when it lands.
- Out: GCP deployment (G06), streaming (Later).
- Depth: MVP. Floor: spend stop, no content in logs, cookie not model-settable.

## Acceptance

- [ ] Card fields in the JSON equal the stored operation; the widget never
      renders card data from `messages`.
- [ ] Confirm with a cookie for another session → 403, no `OperationService.confirm` call.
- [ ] Second concurrent `/chat` on one session → 409; limits exceeded or kill
      switch off → designed "please call the salon" response with no model call.
- [ ] Log-capture test with a known phone number and message finds neither.
- [ ] Service restart mid-conversation (SQLite file) resumes the session.

Verification: `pytest tests/test_api.py` offline; widget checked by hand in a
local browser against `uvicorn app.api:app`.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-chat-api-and-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
