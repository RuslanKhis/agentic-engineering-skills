---
goal: G04
title: Customers can book, move and cancel by chat through confirmation cards
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-agent-evaluation]
blocked_by: [G02, G03]
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

# G04 Customers can book, move and cancel by chat through confirmation cards

## Outcome

The journey in the design works end to end in a Runner test: a proposal creates a card and only the confirm call changes the booking (D1, D2; I5).

## Scope

- In: `propose_booking`, `propose_move` and `propose_cancel` taking `slot_id` or `appointment_id`; resolve slot IDs from this session's stored search results; return card data; instruction v2 ("never claim success before the card says succeeded"); the agent reads an operation's outcome from state on the next turn.
- Out: Browser rendering (G06).
- Depth: Build. The agent holds no write tool.

## Acceptance

- [ ] A booking, a move and a cancel each produce exactly one card with the details shown, and the fake changes only after the executor runs
- [ ] A made-up time or slot ID returns an actionable tool error and no operation
- [ ] A scripted model that "says" it booked without a card is caught by the test

Verification: offline Runner tests with a scripted model, the G01 fake and the G03 store.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-proposal-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
