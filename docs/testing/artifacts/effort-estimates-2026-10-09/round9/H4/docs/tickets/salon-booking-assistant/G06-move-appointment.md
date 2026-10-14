---
goal: G06
title: Customer moves their own appointment
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: [G03, G04, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev A
status: blocked
---

# G06 Customer moves their own appointment

## Outcome

Maya's journey: a signed-in customer moves their appointment to a new free slot with one confirmed click, and the staging booking API shows the result. Implements D4/D5 for reschedule and the bounded live check for book, move and cancel.

## Scope

- In: `propose_move(appointment_id, new_start, stylist?)` reusing G04's operations; ownership and policy-window checks as G05; uses the reschedule endpoint or, if G01 found none, the documented cancel-plus-rebook fallback (two operations, both shown). Then a bounded live check against the staging booking API (W1): book, move, cancel for one test customer, plus one forced timeout to observe reconciliation.
- Out: Widget (G07); production (G11).
- Depth: Build. Floor: staging only; the test customer and salon from W1; at most 20 staging writes.
- Notes: Pick up G03's `verified_customer()`; handoff 0.5 h included.
- Execution scope: Local work is ready. The staging check needs W1 (staging key, test customer and salon) and the team's approval for the staging writes.

## Acceptance

- [ ] Offline: Maya's move from Saturday 10:00 to Thursday 14:30 with Sam results in exactly one reschedule on the fake and a status card from the receipt.
- [ ] Moving into a taken slot returns fresh slots; moving another customer's appointment is refused with no write.
- [ ] Staging: book, move and cancel each succeed once with the test customer; the evidence lists the staging booking IDs, and the forced timeout ends with one booking, not two.

Verification: Offline: `pytest tests/test_move.py`. Authorised live: `pytest -m staging tests/staging/` against the W1 staging key.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-move-appointment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
