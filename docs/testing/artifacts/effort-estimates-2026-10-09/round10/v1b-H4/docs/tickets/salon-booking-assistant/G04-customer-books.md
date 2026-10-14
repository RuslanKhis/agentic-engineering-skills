---
goal: G04
title: Customer books through the assistant
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-agent-evaluation]
blocked_by: [G02, G03]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev B
status: blocked
---

# G04 Customer books through the assistant

## Outcome

Maya picks 17:30, gives her name and phone, and receives a confirmation card
whose details come from the stored pending operation; the booking exists only
after she confirms. Implements the booking half of D2 and the instruction rule
"never claim a booking is done".

## Scope

- In: `propose_booking(slot_id, name, phone, email?)` tool: validates the slot
  is still offered, normalises phone, calls `OperationService.propose`, returns
  `{status, op_id, card}` where `card` follows the design's fixed schema
  (service, salon, local start time, staff, duration, customer name). Instruction
  update and rendered-request test. Scripted-model Runner tests through a
  confirm call on `OperationService`. Includes 1 h handoff from Dev A on G03.
- Out: HTTP and widget rendering of the card (G05), move/cancel (G11),
  verification (G10).
- Depth: MVP. Floor: model cannot commit; card from tool result, not model text.

## Acceptance

- [ ] Happy path: propose → confirm → fake shows 1 booking matching the card.
- [ ] Slot taken between propose and confirm: confirm returns `rejected(slot_taken)`
      and the agent's next turn offers new slots from `find_slots`.
- [ ] Scripted model calling `propose_booking` 5 times and stating "booked!"
      produces 0 fake writes and 5 pending rows (I1).
- [ ] Invalid phone or unknown slot returns `needs_input` with an actionable message.

Verification: `pytest tests/test_booking_flow.py` offline.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-customer-books.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
