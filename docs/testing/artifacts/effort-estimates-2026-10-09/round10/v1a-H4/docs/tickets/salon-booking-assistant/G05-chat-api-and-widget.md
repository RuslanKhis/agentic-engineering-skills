---
goal: G05
title: A signed-in customer chats in a widget on the booking site and confirms changes on a card
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets, adk-operational-guardrails]
blocked_by: [G02, G06]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 2-4
  total: 8-13
  calendar_waits: none
owner: Dev C
status: blocked
---

# G05 A signed-in customer chats in a widget on the booking site and confirms changes on a card

## Outcome

`assistant/api/` (FastAPI) exposes `POST /chat` and `POST /confirm`. It
verifies the site JWT and sets `customer_id` in session state before running
the Runner. It binds each session to its owner and enforces the per-customer
allowance and the kill switch. A widget in the booking site renders replies
and a Confirm/Cancel card from the typed confirmation object (D2, D8, D9, I1,
I6). Includes 1 h of handoff from G02.

## Scope

- In: JWT/JWKS verification with a cache. Session create and resume with an
  owner check. A 30 turns/day allowance in Postgres. Kill switch and
  per-salon flags from configuration. Non-streaming replies. The widget's
  chat panel and confirmation card. "Please sign in again" on 401. Deployed
  to the G06 staging service.
- Out: streaming and the staff handoff (Later list).
- Depth: MVP build; the floor is no anonymous use and a spend stop.

## Acceptance

- [ ] Staging, browser: sign in as the test customer, ask for slots, then book with Confirm. The card shows API data and the reply reports the booked time.
- [ ] Tampered or expired JWT gives 401 and no Runner call. Another customer's `session_id` gives 403 and no session data.
- [ ] The 31st turn in a day and the kill switch each return the fallback message without a model call.
- [ ] Forbidden: `/confirm` with a confirmation ID from another session makes zero write calls.

Verification: `pytest tests/api` offline with a scripted model and a test JWKS.
Then a manual browser run on staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-chat-api-and-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
