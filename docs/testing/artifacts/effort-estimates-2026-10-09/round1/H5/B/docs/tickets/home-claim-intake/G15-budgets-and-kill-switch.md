---
goal: G15
title: Spend and abuse limits with a kill switch that falls back to the form
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-20
  review_and_verify: 12-20
  total: 24-40
  calendar_waits: none
owner: E4
status: blocked
---

# G15 Spend and abuse limits with a kill switch that falls back to the form

## Outcome

No customer, session or bad day can run up model spend beyond set limits, and operators can turn the assistant off without a deploy. Implements D12, I8; A7.

## Scope

- In: `max_llm_calls` per invocation; atomic counters for session turns/photos, customer drafts per day and a global daily ceiling; kill switch flag; UI fallback contract; budget alert.
- Out: Cost tuning (phase 2).
- Depth: Build; floor kept.
- Route: Admission check before each Runner invocation and upload; counters in Postgres.
- Supporting skills: none
- Execution scope: Local.

## Acceptance

- [ ] The 41st turn in a session returns the fallback and makes no model call
- [ ] Concurrent requests cannot exceed the global ceiling (race test)
- [ ] Kill switch takes effect within one request without redeploy
- [ ] Counters survive a restart

Verification: Offline and local integration with Postgres.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G15-budgets-and-kill-switch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
