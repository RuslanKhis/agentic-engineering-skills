---
goal: G04
title: A customer chats on the booking site and confirms changes on a card
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, 1.5x new-to-ADK applied; includes 1 h handoff from Dev B
  hands_on: 5-8
  review_and_verify: 2-3
  total: 7-11
  calendar_waits: none
owner: Dev C
status: blocked
---

# G04 Chat widget with confirmation cards

## Outcome

A chat widget on the signed-in area of the booking site (D8) sends messages
to `/chat`, reloads history from `/session`, and renders proposal cards with
**Confirm** / **No thanks** whose status comes from the proposal record, never
from model text (I4).

## Scope

- In: `widget/` built against G02's typed JSON contract and a fake backend
  returning proposal cards in each status; pilot-salon feature flag; "call
  the salon" fallback message.
- Out: streaming (later), staging deployment (G06), end-to-end launch run (G07).
- Depth: MVP Build. Floor: the widget sends the site's token, never a
  customer ID; Confirm button disabled after the first click.

## Acceptance

- [ ] Card shows exact salon, service, stylist and old/new times from the proposal payload.
- [ ] Statuses `succeeded`, `failed`, `uncertain`, `expired` render distinct, honest messages.
- [ ] Reload restores the conversation and pending cards.
- [ ] Double click sends one confirm request.

Verification: local browser run against the fake backend; component tests.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
