---
goal: G06
title: Loops, abusive customers and floods stop politely
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G04]
phase: 1
profile: MVP or pilot
estimate: 4-6 h
suggested_owner: Dev A (knows the booking API)
status: blocked
---

# G06 Loops, abusive customers and floods stop politely

## Outcome

Spend is bounded per turn, per customer and per IP (D8, I5).

## Scope

- In: RunConfig max_llm_calls=8; per-customer daily turn counter (40) in Postgres; per-IP limiter (30/min) in the gateway; a written checklist of Vertex quota and budget alert values for G07.
- Out: Cloud Armor, shared budgets (later).
- Depth: Build at MVP depth; part of the floor, not cuttable — only the per-IP limiter may move to phase 2.

## Acceptance

- [ ] Scripted looping model stops at the call cap with a friendly message.
- [ ] The 41st turn of a customer's day is refused; the counter survives a restart.
- [ ] Nothing is written to the booking API by a refused request.

Verification: pytest tests/test_limits.py (offline).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-spend-and-abuse-limits.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
