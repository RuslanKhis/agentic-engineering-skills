---
goal: G05
title: The customer presses Confirm on the exact change before anything is booked, moved or cancelled
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: adk-operational-guardrails
supporting_skills: [adk-tool-interface-design, safe-api-tool-calls]
blocked_by: [G02, G03, G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-7
  review_and_verify: 3-4
  total: 8-11
  calendar_waits: none
owner: Dev B
status: blocked
---

# G05 The customer presses Confirm on the exact change before anything is booked, moved or cancelled

## Outcome

Maya's move happens only after she presses Confirm on a card that shows the
old and new time, and the card shows the API's answer. Implements D2 and the
code side of D7; holds I2 and I4. Includes 1 h handoff from Dev A (G02) and Dev
C (G04).

## Scope

- In: `app/tools/propose.py` with `propose_booking(slot_id)`,
  `propose_move(appointment_id, slot_id)`, `propose_cancellation(appointment_id)`
  — validate slot IDs were offered in this session, ownership, the 24-hour rule
  (A6), at most 2 open proposals; store an operation `proposed` with a 15-minute
  expiry; return `{status, proposal_id, summary}` or an actionable error.
  `POST /operations/{id}/confirm` and `GET /operations/{id}`: verify caller owns
  it, not expired, recheck slot availability, then G03's `execute`.
- Out: card rendering (G06), instruction wording (G07).
- Depth: MVP Build. Floor: no write reachable by the model.

## Acceptance

- [ ] Scripted model calls every tool and says "booked!": the fake API records zero writes until `/confirm`
- [ ] `/confirm` by another customer → 403, no write; expired proposal → 410, no write; double `/confirm` → one write
- [ ] Slot taken between propose and confirm → `failed` with "no longer available"
- [ ] Move inside 24 h → proposal refused with the salon phone number, nothing stored
- [ ] A slot ID never returned by `find_slots` in this session → refused

Verification: offline `pytest tests/test_confirm.py` with a scripted model, the booking fake and Postgres in a container.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G05-propose-confirm-flow.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
