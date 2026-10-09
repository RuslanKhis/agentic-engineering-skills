---
goal: G07
title: Chat widget with confirmation card
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G06 (API contract agreed)]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-4
  review_and_verify: 4-6
  total: 6-10
  calendar_waits: none
owner: Dev C
status: blocked
---

# G07 Chat widget with confirmation card

## Outcome

On the website a signed-in customer chats, sees a card built from the stored operation, confirms, and sees the real status. D6; I2, I4.

## Scope

- In: `web/widget/`: embeddable chat, confirmation card (old and new details), Confirm/Decline, states for succeeded/failed/checking/partial/expired, salon phone fallback, kill-switch flag.
- Out: Streaming (later), guest flows (G11).
- Depth: Build. The card renders `pending_operation`, never model text.

## Acceptance

- [ ] A test where reply text disagrees with the operation record shows the record's details
- [ ] Double tap sends one confirm request; `uncertain` never renders "booked"
- [ ] Widget hidden when the flag is off or the customer is signed out

Verification: Component tests plus a manual browser run against local G06 (local integration).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
