---
goal: G03
title: Propose and confirm book, move, cancel exactly once
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-agent-security]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 5-8
  review_and_verify: 3-5
  total: 8-13
  calendar_waits: none
owner: Dev B
status: blocked
---

# G03 Propose and confirm book, move, cancel exactly once

## Outcome

The agent proposes a booking, move or cancel; only the confirm endpoint changes the booking system, once per proposal, and the customer sees the real outcome. Implements D3, D4 and invariants I2–I4.

## Scope

- In: `app/tools/propose.py`, `app/executor.py` (atomic claim, recheck, write, reconcile), `app/store.py` proposals table, confirm and status handler functions for G05 to mount
- Out: widget (G05); provider idempotency if G01 finds none (G11); background reconciliation worker (later)
- Depth: idempotency key = proposal ID when supported, else lookup-before-retry; `executing` > 60 s treated as `uncertain`; proposals expire after 10 min

## Acceptance

- [ ] Confirm twice gives one booking-API write and the same result
- [ ] Fake commit-then-timeout gives `uncertain`, then `succeeded` after lookup, never a second create; slot taken before confirm gives `failed: conflict`
- [ ] A scripted model calling every tool performs zero booking-API writes; another customer's proposal ID returns 404

Verification: `pytest tests/test_executor.py tests/test_propose.py` offline; one staging book → move → cancel run for the test customer.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-propose-and-confirm.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
