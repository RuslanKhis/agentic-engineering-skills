---
goal: G05
title: Chat widget with confirmation card
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 4-6
  review_and_verify: 1.5-2.5
  total: 5.5-8.5
  calendar_waits: none
owner: Dev B
status: blocked
---

# G05 Chat widget with confirmation card

## Outcome

On the booking site a signed-in customer chats, sees a card with the proposed change, presses Confirm and sees the status from the operation record. Implements D5 and I4.

## Scope

- In: `web/widget`; JSON contract `/chat` → `{messages[], proposal?}`, `GET /proposals/{id}`, `POST /proposals/{id}/confirm`; embedding snippet for the existing site
- Out: streaming (G14)
- Depth: card text comes from the proposal row, never model text; Confirm disabled after expiry; failures show the booking-form link

## Acceptance

- [ ] Mobile browser: chat → card → Confirm → `succeeded` shown
- [ ] `uncertain` shows "We're checking this booking"; model failure shows the booking-form link
- [ ] An expired card cannot be confirmed

Verification: Local browser run against stubbed handlers, then against G03's handlers with the fake booking API.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
