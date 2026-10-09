---
goal: G15
title: Runaway conversations and storm bursts are bounded and degrade to the standard form
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 16-28
  review_and_verify: 6-10
  total: 22-38
  calendar_waits: none
  wait_days: 0
owner: Eng C
status: proposed
---

# G15 Runaway conversations and storm bursts are bounded and degrade to the standard form

## Outcome

Implements D11 and I9.

## Scope

- In: `app/guards/`: per-invocation cap, 60-call session cap, 3 drafts per customer per day (atomic in Cloud SQL), admission limit, kill switch from config; confirm and status exempt from model admission.
- Out: Threshold tuning under load (G27).
- Depth: Production depth. Floor: a spend stop exists before any shared environment.

## Acceptance

- [ ] The 61st model call and the 4th draft of the day are refused with the form link
- [ ] Two concurrent requests cannot both consume the last allowance
- [ ] The kill switch stops new sessions within one config refresh
- [ ] Confirm and status still work while model admission is stopped

Verification: Offline plus local Postgres concurrency test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G15-budgets-and-admission.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
