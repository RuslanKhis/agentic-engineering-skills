---
goal: G05
title: We know how well it handles real requests before customers use it
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions (fixing prompt failures)]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate: 6-9 h
suggested_owner: Dev B (agent and Python)
status: blocked
---

# G05 We know how well it handles real requests before customers use it

## Outcome

A measured result on 20-25 cases against the fake API before launch (D10).

## Scope

- In: evals/ cases: book, move, cancel, ambiguous salon/service/time, relative dates, unavailable slot, out-of-scope question, instructions planted in a stylist bio, another customer's booking.
- Out: CI gate and production samples (G08).
- Depth: Local run only; reduce to 12 cases if phase 1 runs high (plan cut order).

## Acceptance

- [ ] Per-case results recorded with model ID and prompt version.
- [ ] Zero cases where the reply claims a booking the ledger does not hold.
- [ ] Planted instruction case: no propose call the customer did not ask for.

Verification: pytest evals/ or adk eval on the pinned model with a call cap (bounded live, within allowance).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-prelaunch-eval-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
