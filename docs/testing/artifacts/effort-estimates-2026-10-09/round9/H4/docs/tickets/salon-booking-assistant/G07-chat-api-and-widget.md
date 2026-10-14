---
goal: G07
title: Chat API and plain widget on the salon site
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets, adk-operational-guardrails]
blocked_by: [G02, G03]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev B
status: blocked
---

# G07 Chat API and plain widget on the salon site

## Outcome

A customer on the salon website opens a chat, signs in through the existing login, talks to the assistant and presses Confirm on a proposal; the status shown comes from the operation record. Implements D7's API, D8 (plain form), the per-customer and per-IP caps of D9, I4.

## Scope

- In: `app/api/chat.py`: `POST /chat` taking `{session_id?, message}` with `verified_customer()`; creates or loads an owned session, writes `customer_id` and context to state, runs the `Runner`, returns the D8 JSON (`messages`, `proposals`, `operations`). Turn counters (40 per customer per day, 20 per anonymous IP per hour). Turns on one session are serialised (Postgres advisory lock locally replaced by a process lock with SQLite); a second concurrent message waits up to 10 s, then gets 409 "please resend". `web/widget.js`: text bubbles, proposal card with salon, service, stylist, absolute date and a Confirm button calling `POST /operations/{id}/confirm`, status card polling `GET /operations/{id}`.
- Out: Slot cards (G13), streaming (G19).
- Depth: Build (plain widget per cut line). Floor: caps enforced in the API; no model text rendered as a status.
- Notes: Pick up G03's auth dependency; handoff 0.5 h included.
- Execution scope: Local only.

## Acceptance

- [ ] Browser run against the local app and fake: Maya's move completes through the widget and the status card shows the receipt time.
- [ ] Model text says "booked" while the fake fails the write: the status card shows the failure, not success.
- [ ] The 41st turn for one customer in a day and the 21st anonymous turn from one IP in an hour are refused with the salon phone number and no model call; a request with another customer's `session_id` is refused.

Verification: Offline: `pytest tests/test_chat_api.py`; local integration: manual browser run recorded with screenshots.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-chat-api-and-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
