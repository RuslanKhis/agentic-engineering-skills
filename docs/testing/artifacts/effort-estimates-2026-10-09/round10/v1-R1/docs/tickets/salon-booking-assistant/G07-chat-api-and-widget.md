---
goal: G07
title: Chat API and plain widget on the salon site
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets, adk-operational-guardrails]
blocked_by: [G02, G03, G04a]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4.5
  review_and_verify: 1-2
  total: 4-6.5
  calendar_waits: none
owner: Dev C
status: blocked
---

# G07 Chat API and plain widget on the salon site

## Outcome

A signed-in customer on the salon website opens a chat, talks to the assistant and presses Confirm on a proposal; the status shown comes from the operation record. Implements D7's API, D8 (plain form), the per-customer caps and sign-in requirement of D9, I4.

## Scope

- In: `app/api/chat.py`: `POST /chat` taking `{session_id?, message}` with `verified_customer()` (401 without a valid token, before any model call); creates or loads an owned session, writes `customer_id` and context to state, runs the `Runner`, returns the D8 JSON (`messages`, `proposals`, `operations`). Turn counter of 40 per customer per day; the cap check fails closed (database unavailable → 503 with the salon phone, no model call). Turns on one session are serialised (Postgres advisory lock; a process lock locally with SQLite); a second concurrent message waits up to 10 s, then gets 409 "please resend". `web/widget.js`: sign-in prompt on 401, text bubbles, proposal card with salon, service, stylist, absolute date and a Confirm button calling `POST /operations/{id}/confirm`, status card polling `GET /operations/{id}`; a two-step move shows its two proposal cards in turn. Handoff from Dev B (G02's agent and Runner setup) and Dev A (G04a's confirm and status endpoints) included: 1 h.
- Out: Slot cards (G13), streaming (G19), anonymous chat and its per-IP cap (G22).
- Depth: Build (plain widget per cut line). Floor: sign-in and caps enforced in the API; no model text rendered as a status.
- Execution scope: Local only.

## Acceptance

- [ ] Browser run against the local app and fake, with a scripted model that proposes through G04a's `create_pending`: Confirm completes the booking and the status card shows the receipt time. (The real propose tools and Maya's two-step move are shown end to end in G11.)
- [ ] Model text says "booked" while the fake fails the write: the status card shows the failure, not success.
- [ ] The 41st turn for one customer in a day is refused with the salon phone number and no model call; a request with no token gets 401 with no session and no model call; a request with another customer's `session_id` is refused; with the database stopped, `/chat` returns 503 and makes no model call.

Verification: Offline: `pytest tests/test_chat_api.py`; local integration: manual browser run recorded with screenshots.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-chat-api-and-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
