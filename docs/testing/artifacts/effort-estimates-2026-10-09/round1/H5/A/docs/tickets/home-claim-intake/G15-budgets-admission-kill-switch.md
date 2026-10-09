---
goal: G15
title: Storm-day surges and runaway sessions degrade to the form, never to errors or unbounded spend
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-operational-guardrails
supporting_skills: [optimise-adk-on-google-cloud]
blocked_by: [G04, G05]
phase: 1
profile: production
estimate: 48-80 h
status: blocked
---

# G15 Storm-day surges and runaway sessions degrade to the form, never to errors or unbounded spend

## Outcome

Per-session turn and photo caps, a per-customer daily allowance, a global active-session admission cap and an operator kill switch, with the form/phone fallback, while confirmed submissions always complete. Implements D9, I9 in the design.

## Scope

- In: `app/guardrails/allowances.py`, admission counter with TTL leases in Postgres, kill-switch flag, fallback responses, metrics, budget alert configuration described for G16.
- Out: Cost tuning (P2-05).
- Depth: Build; floor: operator stop independent of automatic resets.
- Route: Checks in the API before `run_async` and upload URL issue; worker exempt.
- Prerequisites: G04, G05; budget figures (defaults usable).
- Supporting skills:
  - `optimise-adk-on-google-cloud`: per-instance concurrency and admission sizing
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls.

## Acceptance

- [ ] Each cap, when exhausted, returns the fallback response and keeps the draft.
- [ ] With the kill switch on, new sessions get the fallback while an in-flight submission still reaches `SUBMITTED`.
- [ ] Forbidden: two concurrent admissions cannot exceed the global cap (concurrency test).

Verification: Offline tests on local Postgres with concurrent requests.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G15-budgets-admission-kill-switch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
