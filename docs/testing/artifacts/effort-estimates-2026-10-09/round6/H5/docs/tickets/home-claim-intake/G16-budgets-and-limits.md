---
goal: G16
title: Bound model work and abuse per turn, per customer and overall
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G07, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 8-12
  review_and_verify: 3-5
  total: 11-17
  calendar_waits: none
  wait_days: 0
owner: Dev D
status: blocked
---

# G16 Bound model work and abuse per turn, per customer and overall

## Outcome

Call caps, per-customer daily limits and an operator stop keep spend bounded without losing drafts. Implements D10, I8; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: `max_llm_calls`, per-customer counters in Postgres, operator stop flag, limit messages.
- Out: Cost tuning (later).
- Depth: Production; limit values provisional (Q3).

## Acceptance

- [ ] A ninth call stops the invocation with the draft saved.
- [ ] The 61st turn in a day gets the limit message; counters survive restart.
- [ ] Operator stop blocks new sessions while submission and reconciliation keep running.

Verification: Offline with Postgres.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G16-budgets-and-limits.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
