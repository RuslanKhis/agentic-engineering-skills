---
goal: G05
title: Chat API and chat page with confirm card
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G02, G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev C
status: blocked
---

# G05 Chat API and chat page with confirm card

## Outcome

Customers open "Book with our assistant" from the salon site, chat, and press Confirm on a card. Implements D6.

## Scope

- In:
  - `POST /chat` returns one complete JSON turn, without streaming.
  - Wiring for `POST /proposals/{id}/confirm`.
  - A static chat page served by the application under the site's domain. It shows text, a proposal card with Confirm and Cancel, and receipt, uncertain and error states. Errors show the salon's phone number.
- Out: Embedding across the existing site, streaming and visual polish.
- Depth: MVP. Only the application's own response schema reaches the browser, never raw ADK events.
- Implementation route: FastAPI around the `Runner` in `app/api.py`, plus `app/static/chat.html` and a small script. The site's reverse proxy routes `/assistant` to the service (A6).
- Prerequisites: G02 and G04. The proposal card schema from the G01 contract document; G03's endpoint can be stubbed until it lands.
- Supporting skills: None
- Execution scope: Local and the site's staging environment.

## Acceptance

- [ ] A book-then-confirm journey works in a browser against the fake.
- [ ] A second Confirm click shows the same receipt.
- [ ] An `uncertain` result shows "we're checking this booking, please don't book again".
- [ ] The browser never receives tool arguments, `customer_id` or any internal ID other than `proposal_id`.

Verification: Local integration in a real browser against a local server and the fake, plus API tests (`pytest tests/test_api.py`).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-chat-api-and-chat-page-with-confirm-card.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
