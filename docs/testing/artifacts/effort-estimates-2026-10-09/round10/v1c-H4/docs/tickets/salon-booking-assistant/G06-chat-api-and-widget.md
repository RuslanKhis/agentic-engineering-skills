---
goal: G06
title: Customers chat on the website and confirm changes from a card
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-operational-guardrails]
blocked_by: [G02, G03]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-8
  review_and_verify: 2-4
  total: 8-12
  calendar_waits: none
owner: Dev C
status: proposed
---

# G06 Customers chat on the website and confirm changes from a card

## Outcome

A signed-in customer chats in a widget on the salon website; booking
proposals appear as cards built from the proposal record, and the confirm
button calls the confirm route defined in G01's contract (D6, D8, I6).
Includes 1 h handoff from Dev B on G02's agent.

## Scope

- In: `POST /chat` around the ADK `Runner` with `RunConfig(max_llm_calls=12)`;
  per-customer daily allowance checked before the Runner starts; one turn at a
  time per session (overlapping message rejected); operator stop (allowance 0
  in configuration); model errors and 429 mapped to a fixed message; embeddable
  widget rendering messages, cards and operation status; tested against the
  G01 confirm-route fake. The real confirm route arrives with G04 and is
  joined in G09.
- Out: streaming, guest access, staff screens.
- Depth: build.

## Acceptance

- [ ] Card content equals the stored proposal, not model text; model text
      saying "booked" never renders as a confirmed card.
- [ ] Allowance exhausted or operator stop → fixed message, zero model calls.
- [ ] A turn exceeding `max_llm_calls` ends with the fixed message.
- [ ] Second message while a turn runs → rejected, first turn unaffected.
- [ ] Operation `failed` or `uncertain` shows the designed text.

Verification: offline API tests with a scripted model; widget tested in a
local browser against the fakes.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-chat-api-and-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
