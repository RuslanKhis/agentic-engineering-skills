---
goal: G06
title: Customers chat in the booking web app and confirm changes on a card
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G05]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 5-8
  review_and_verify: 1-2
  total: 6-10
  calendar_waits: none
owner: Dev C
status: blocked
---

# G06 Customers chat in the booking web app and confirm changes on a card

## Outcome

The widget renders text and proposal cards from data, and results from the operation status (D7). Implements I4 on screen.

## Scope

- In: `web/widget/`, embedded in the existing booking web app; it reuses the app's session token
- In: Card states: pending (Confirm / Not now), confirming, succeeded, slot taken, uncertain ("we're confirming"), expired
- Out: Out: streaming, other channels
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] Confirm → the card shows the API result, never model text
- [ ] "Slot taken" and "uncertain" render distinctly, and a reload shows the current status
- [ ] A double click sends one confirm request

Verification: local integration: the widget against the gateway with the fake API, checked in a real browser.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
