---
goal: G09
title: Per-customer allowance, limits and kill switch
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev B
status: blocked
---

# G09 Per-customer allowance, limits and kill switch

## Outcome

No customer or anonymous visitor can run up model spend or flood the booking API. Implements D7 and the floor.

## Scope

- In:
  - A per-customer daily allowance of 40 turns and at most 3 open proposals.
  - An anonymous per-IP limit of 20 turns per hour.
  - A check that `max_llm_calls=12` is in force on every run.
  - A kill switch flag that turns the chat into "please call the salon" without calling the model.
- Out: Shared token budgets (Later).
- Depth: MVP Build, a per-user allowance. Counters live in Postgres and survive a restart.
- Implementation route: An admission check in `app/limits.py` before `Runner.run`.
- Prerequisites: G04, which provides the identity the allowance is keyed on.
- Supporting skills: None
- Execution scope: Local.

## Acceptance

- [ ] The 41st turn of a day gets a polite refusal and makes zero model calls.
- [ ] With the kill switch on, chat makes zero model calls.
- [ ] Counters survive a process restart.
- [ ] A fourth open proposal is refused.

Verification: Offline `pytest tests/test_limits.py` (SQLite).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-per-customer-allowance-limits-and-kill-switch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
