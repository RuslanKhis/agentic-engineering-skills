---
goal: G04
title: Customer books a slot with one confirm
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-operational-guardrails, adk-agent-security]
blocked_by: [G01, G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 3-5
  total: 7-11
  calendar_waits: none
  wait_days: 0
owner: Dev A
status: blocked
---

# G04 Customer books a slot with one confirm

## Outcome

The agent proposes a booking; only the customer's Confirm on the stored details creates it, exactly once. I2, I3, I4; D2, D4, D5. Route and rationale: [plan, G04](../../plans/salon-booking-assistant.md#g04--customer-books-a-slot-with-one-confirm).

## Scope

- In: `tools/propose.py` (`propose_booking`), `operations.py` (proposals, `booking_operations`, confirm executor with atomic claim, idempotency per G01, uncertain-outcome reconciliation)
- Out: move and cancel (G05)
- Depth: build; the model holds no write tool

## Acceptance

- [ ] Confirm → exactly one appointment in the fake and a reference; double confirm → same result, still one
- [ ] Fake commits then times out → `uncertain`, then reconciled to one appointment
- [ ] Expired, foreign or unknown proposal → rejected and nothing written; a scripted model calling every tool never mutates the fake

Verification: offline `pytest` using the fake's fault modes.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-book-with-confirm.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
