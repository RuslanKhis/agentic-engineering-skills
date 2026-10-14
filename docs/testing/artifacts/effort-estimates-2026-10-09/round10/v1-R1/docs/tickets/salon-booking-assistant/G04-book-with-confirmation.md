---
goal: G04
title: Customer books with one confirmed click
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [safe-api-tool-calls, adk-agent-instructions]
blocked_by: [G04a]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 0.5-1
  total: 2.5-4
  calendar_waits: none
owner: Dev B
status: blocked
---

# G04 Customer books with one confirmed click

## Outcome

A customer can ask for a booking in chat, see an exact proposal and make it real only by confirming it. Adds the `propose_booking` tool on top of G04a's operations core; the first half of a phase-1 move (A11).

## Scope

- In: `app/tools/propose.py`: `propose_booking(salon, service, stylist, start_iso)` validates salon, service, stylist and ISO start against the salon's hours (D12), rechecks the slot, stores a pending operation through `create_pending`, and returns the summary fields and `operation_id`. Register it on the agent; add the booking step to the instruction. Handoff from Dev A (G04a's module) included: 0.5 h.
- Out: Cancel and the move order (G05), widget (G07).
- Depth: Build. Floor: `customer_id` from `ToolContext.state`, never an argument; the tool writes only to our store.
- Execution scope: Local only.

## Acceptance

- [ ] Scripted model proposes a booking; the fake booking API records zero writes until confirm; after confirm exactly one booking exists.
- [ ] A start outside opening hours or an invalid ISO string returns an actionable error and stores nothing; a taken slot at propose returns `slot_taken` with fresh slots.
- [ ] The captured request shows `propose_booking` with no `customer_id` parameter.

Verification: Offline: `pytest tests/test_propose_booking.py` with the G01 fake and a scripted model.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-book-with-confirmation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
