---
goal: G03
title: Confirmed, idempotent book, move and cancel
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-agent-security]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 8-12
  review_and_verify: 4-6
  total: 12-18
  calendar_waits: none
owner: Dev A
status: blocked
---

# G03 Confirmed, idempotent book, move and cancel

## Outcome

The customer presses Confirm on a card showing salon, service, stylist, date and local time, and exactly one booking, move or cancellation happens. If the outcome is uncertain, the customer is told so rather than shown a guess. Implements D3 and invariants I2 to I4.

## Scope

- In:
  - A `propose_change` tool with `kind` set to book, move or cancel. It re-checks availability and ownership, stores a `Proposal` (pending, expires in 10 minutes) and returns the card.
  - `POST /proposals/{id}/confirm` in ordinary code. It claims the proposal atomically, executes it with `idempotency_key = proposal_id` and writes an `operations` row whose status goes from `pending` to `succeeded`, `failed` or `uncertain`.
  - Reconciliation of an uncertain operation by key or lookup, never by a fresh dispatch.
  - A move uses the reschedule endpoint if G01 finds one; otherwise it books then cancels, as two operations.
  - The confirmed result is appended to the session as an event the agent sees on the next turn.
- Out: The browser card (G05) and scheduled reconciliation (G16).
- Depth: MVP Build for external writes. The model holds no write tool. Confirmation lives in code the model cannot reach. ADK's native `require_confirmation` is deliberately not used (D3).
- Implementation route: `app/proposals.py` and `app/operations.py` on SQLAlchemy: SQLite in tests, Postgres from G08. The confirm handler takes `customer_id` from the verified request and compares it with the proposal's owner.
- Prerequisites: G01. Tests inject a verified `customer_id`, so G04 is not required.
- Supporting skills: Adk-tool-interface-design: the `propose_change` declaration and its actionable errors; adk-agent-security: shows that a scripted model cannot cause a write.
- Execution scope: Local, plus booking-API staging with test customers only.

## Acceptance

- [ ] One confirm produces one API write and a receipt.
- [ ] A double click or two tabs produce one write and the same receipt twice.
- [ ] A slot taken between proposal and confirm returns "slot taken" with no write.
- [ ] A timeout after commit yields `uncertain`. Reconciliation then finds the appointment without a second dispatch.
- [ ] An expired proposal is refused.
- [ ] Another customer's `proposal_id` returns 404 with no write.
- [ ] A scripted model told to "just book it" causes zero API writes.
- [ ] In a book-then-cancel move where the cancel fails, the new booking stays. The customer sees that both appointments exist, and the operation is flagged for staff.

Verification: Offline `pytest tests/test_writes.py` against the fake's failure modes. One authorised staging run of book, move and cancel with a test customer.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-confirmed-idempotent-book-move-and-cancel.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
