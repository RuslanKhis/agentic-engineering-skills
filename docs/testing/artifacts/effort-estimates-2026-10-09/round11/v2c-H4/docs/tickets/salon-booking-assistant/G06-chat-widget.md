---
goal: G06
title: A customer chats on the salon website and confirms a change with one tap
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-operational-guardrails]
blocked_by: []
mentions_only: [G03, G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 3-5
  total: 9-14
  calendar_waits: none
owner: Dev B
status: ready
---

# G06 A customer chats on the salon website and confirms a change with one tap

## Outcome

A small widget on the website's logged-in pages sends messages, renders
proposal cards and outcomes from structured fields, and confirms through the
D8 contract. Built against D8 fixtures and a stub server; the real gateway and
executor are wired in G08.

## Scope

- In: `web/widget/` (plain JS or the website's existing framework), embedding
  in the logged-in layout of the website's staging site (the team maintains
  the website, assumption Q16), sending the website token as a Bearer header
  (D8), stub server serving D8 fixtures, flags read from `GET /config`.
- Out: gateway auth (G03 owns it), executor (G04), streaming (later).
- Depth: MVP build; floor: Confirm is the only path to a write.

## Acceptance

- [ ] A1 A logged-in customer on the pilot salon page opens the widget, sends a message and sees the reply.
- [ ] A2 Proposal cards render from the `proposals` field, never from model text; Confirm posts `/proposals/{id}/confirm`; Dismiss sends nothing to the executor.
- [ ] A3 Each operation status (`succeeded`, `failed`, `stale`, `uncertain`, `partial`) has a designed message, shown from the response fixture.
- [ ] A4 Confirm is disabled after the first tap until a response arrives.
- [ ] A5 Chat request timeout (30 s) or network error shows a retry message; a confirm that times out shows "checking" and polls `GET /operations/{id}` instead of resubmitting.
- [ ] A6 Global or salon flag off → widget hidden; the API's 503 "assistant off" is shown politely if a page was already open.
- [ ] A7 Model text containing HTML or script is rendered as plain text (XSS test).

Verification: local browser test against the stub server (Playwright or
manual checklist recorded in Evidence).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
