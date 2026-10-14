---
goal: G06
title: A customer chats on the website and confirms a change with one click
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G05]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 5-7
  review_and_verify: 1-3
  total: 6-10
  calendar_waits: none
owner: Dev C
status: blocked
---

# G06 A customer chats on the website and confirms a change with one click

## Outcome

A minimal same-origin chat page with proposal cards, built against the design's
public JSON contract (D9). Works against the gateway with a mock confirm
service; the integration goal (G09) wires the real one.

## Scope

- In: `app/web/` page and script; the same-origin `/assistant` route and the account-area link on our website (Q16).
- Out: streaming, styling beyond the website's existing stylesheet.
- Depth: MVP. Plain-text rendering only.

## Acceptance

- [ ] A1 A signed-in customer sends a message and sees a proposal card with salon, service, stylist, local date and time, price, and what it replaces for a move; Confirm and Decline buttons.
- [ ] A2 Confirm is disabled after the first click; a double click sends one request; the receipt from the confirm response is shown.
- [ ] A3 `unknown` and `partial` are shown as "checking with the salon" (with status polling) and never as success; `failed` shows the reason.
- [ ] A4 A signed-out visitor sees a sign-in link; the page stores no token in `localStorage`.
- [ ] A5 Network error on chat offers retry; on confirm it polls status for the same proposal and never creates a new proposal.
- [ ] A6 Agent text containing HTML or script is rendered inert (XSS test).

Verification: browser test (Playwright or manual checklist) against the local gateway; offline.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-chat-page.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
