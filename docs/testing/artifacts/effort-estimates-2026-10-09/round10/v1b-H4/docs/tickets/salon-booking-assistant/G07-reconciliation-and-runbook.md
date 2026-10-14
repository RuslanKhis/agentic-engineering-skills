---
goal: G07
title: Uncertain-outcome reconciliation and front-desk runbook
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-agent-observability]
blocked_by: [G03]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-5
  review_and_verify: 1-2
  total: 5-7
  calendar_waits: none
owner: Dev C
status: blocked
---

# G07 Uncertain-outcome reconciliation and front-desk runbook

## Outcome

When the booking API may have committed but we did not hear back, the customer
is told "we're checking", the system finds out, and if it cannot, the salon
front desk gets a clear task. Implements invariant I4 and the `committing`
sweep in the failure grid.

## Scope

- In: `OperationService.reconcile(op_id)` using the client's lookup by `op_id`
  (or the fallback from `docs/booking-api-contract.md` if O1 found none);
  sweep of `uncertain` rows and `committing` rows older than 1 minute;
  structured `operation.uncertain` / `operation.reconciled` log events (no
  customer content); the customer-visible status text for `GET
  /operations/{op_id}`; `docs/runbooks/front-desk-uncertain-booking.md` (one
  page: how staff check the booking, what to tell the customer). Includes 1 h
  handoff from Dev A on G03.
- Out: alert wiring (G06), staff UI.
- Depth: MVP. Floor: an uncertain write is never reported as done or failed.

## Acceptance

- [ ] Fake commits then times out: row `uncertain` → reconcile finds it → `done`; 0 extra writes.
- [ ] Fake did not commit: reconcile finds nothing → `rejected(not_committed)`
      only if the API lookup is authoritative per the contract doc; otherwise
      stays `uncertain` and emits the alert event.
- [ ] A `committing` row older than 1 minute is picked up by the sweep.
- [ ] Runbook reviewed by the salon contact during the W1 conversation.

Verification: `pytest tests/test_reconcile.py` offline.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-reconciliation-and-runbook.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
