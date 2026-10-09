---
goal: G04
title: Customers chat on the website and confirm on a card
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate: 12-18 h
suggested_owner: Dev C (web and infra)
status: ready
---

# G04 Customers chat on the website and confirm on a card

## Outcome

A customer chats in a widget on the salon website; proposals appear as a card rendered from the ledger with Confirm/Cancel (D7, I4). Confirm becomes live when G02 lands; build the skeleton against a stub until then.

## Scope

- In: FastAPI POST /chat → {reply_text, pending_operation?}; POST /operations/{id}/confirm; GET /operations/{id}; embeddable widget in web/widget with card states proposed, succeeded, failed, uncertain, expired.
- Out: Streaming, styling beyond basics, staff UI (G11).
- Depth: Build without streaming. Card fields come only from the ledger row, never the model's prose.

## Acceptance

- [ ] The card shows the ledger's salon, service, stylist and times even when the model's text differs.
- [ ] Every card state renders; refresh after Confirm shows the same result, not a second confirm.
- [ ] No route accepts a customer ID from the browser.

Verification: API tests offline; a browser check against local + staging (local integration).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-chat-widget-and-card.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
