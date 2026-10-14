---
goal: G03
title: The assistant proposes a booking, move or cancellation as a card, without changing anything
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 3-5
  review_and_verify: 2-3
  total: 5-8
  calendar_waits: none
owner: Dev A
status: blocked
---

# G03 The assistant proposes a booking, move or cancellation as a card, without changing anything

## Outcome

Propose tools write a pending operation instead of calling the API (D3). Implements I2 (proposal side) and I4.

## Scope

- In: `propose_booking`, `propose_move`, `propose_cancel` in `assistant/tools/propose.py`
- In: Operation table: `op_id`, `customer_id`, kind, canonical payload, payload hash, summary, status, `expires_at` (10 min)
- In: Fresh availability and ownership re-check before writing the row
- Out: Out: executing the change (G04), UI (G06)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] A proposal creates one `pending` row and makes no API write call
- [ ] A slot not offered by the API, or another customer's appointment, gives an actionable error and no row
- [ ] Tool results carry `op_id` and summary only; code builds the card

Verification: offline `pytest tests/test_propose.py` (SQLite or a local Postgres fixture).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-change-proposals.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
