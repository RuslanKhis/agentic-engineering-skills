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
estimate:
  hands_on: 6-8
  review_and_verify: 2-3
  total: 8-11
  calendar_waits: none
owner: Dev C
status: blocked
---

# G05 Chat widget with confirmation card

## Outcome

Implements D10 on the client. Maya chats on the booking site and confirms a change on a card rendered from the stored operation, not from model text.

## Scope

- In and out: In: `web/widget/` embedded in the booking site's signed-in area; it sends the site token; it renders replies and a card from `pending_operation` in the `/chat` response, with Confirm and Cancel; it polls `/operations/{id}` for `uncertain`; error and phone-number states. Out: streaming and styling polish.
- Depth: Build. Floor: Confirm is the only path to a write. The card shows the stored old and new details.

## Acceptance

- [ ] Against the G04 gateway with a fake agent, the card shows the stored payload and Confirm calls `/confirm/{id}` once, even when double-clicked
- [ ] An `uncertain` result shows "we're confirming with the salon" and settles after polling
- [ ] No card and no Confirm appear when the response has no `pending_operation`, whatever the reply text says

Verification: Local integration: the gateway running locally with a fake agent; manual browser walkthrough plus a component test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
