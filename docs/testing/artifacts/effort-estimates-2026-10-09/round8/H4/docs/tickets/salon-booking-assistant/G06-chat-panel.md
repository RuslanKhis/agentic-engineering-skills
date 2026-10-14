---
goal: G06
title: Customers chat and confirm changes in the booking web app
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G05]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-7
  review_and_verify: 2-3
  total: 7-10
  calendar_waits: none
owner: Dev B
status: blocked
---

# G06 Customers chat and confirm changes in the booking web app

## Outcome

The design's journey works in a browser: messages and cards, Confirm and Dismiss, and the card states proposed, executing, succeeded, failed, uncertain and expired (D8).

## Scope

- In: A chat panel in the existing booking web app calling the G05 JSON API with the signed-in token; card rendering bound to `operation_id`; the confirm button disables after the first click; a sign-in prompt on 401.
- Out: Slot-picker buttons (G14); streaming.
- Depth: Build at MVP depth: no styling beyond the chain's colours.

## Acceptance

- [ ] A real browser run books, moves and cancels against the fake
- [ ] A double click sends one confirm
- [ ] An `uncertain` card shows the "don't rebook" text and the salon phone

Verification: local integration in a real browser against G05 and the fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-chat-panel.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
