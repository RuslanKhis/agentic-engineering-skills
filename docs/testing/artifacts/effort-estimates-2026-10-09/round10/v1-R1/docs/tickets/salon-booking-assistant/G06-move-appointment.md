---
goal: G06
title: Customer moves their own appointment in one step (phase 2)
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: [G11]
phase: 2
profile: MVP or pilot
estimate:                # human hours, agent-assisted; rough, re-estimate after G11
  hands_on: 2.5-4.5
  review_and_verify: 1-2
  total: 3.5-6.5
  calendar_waits: none
owner: Dev A
status: deferred
---

# G06 Customer moves their own appointment in one step (phase 2)

Deferred from phase 1 in revision 2 (8-day launch, A11). Until it lands, a move is book-new-then-cancel-old (G05). Re-estimate after G11; the plan's phase 2 list is its schedule.

## Outcome

Maya's journey in one proposal: a signed-in customer moves an appointment to a new free slot with one confirmed click and one reschedule call, so the move is atomic at the booking API.

## Scope

- In: `propose_move(appointment_id, new_start, stylist?)` on G04a's operations core; ownership and `changeable` checks as G05; the reschedule endpoint, or if G01 found none, keep the two-step flow and close this goal. Update the instruction's move flow and G08's move cases. Bounded staging check of one move with the W1 test customer.
- Out: Slot cards (G13).
- Depth: Build. Floor: staging only for the live check; at most 10 staging writes.
- Execution scope: Local work, then staging with the team's approval.

## Acceptance

- [ ] Offline: Maya's move from Saturday 10:00 to Thursday 14:30 with Sam results in exactly one reschedule on the fake and a status card from the receipt.
- [ ] Moving into a taken slot returns fresh slots; moving another customer's appointment is refused with no write.
- [ ] Staging: one move succeeds once with the test customer; a forced timeout ends with one appointment, not two.

Verification: Offline: `pytest tests/test_move.py`. Authorised live: `pytest -m staging tests/staging/test_move.py`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-move-appointment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
