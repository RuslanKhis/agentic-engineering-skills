---
goal: G11
title: A runaway conversation or a storm of abuse cannot run up cost, and operators can switch the agent off
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 16-24
  review_and_verify: 6-8
  total: 22-32
  calendar_waits: none
owner: Eng A
status: blocked
---

# G11 A runaway conversation or a storm of abuse cannot run up cost, and operators can switch the agent off

## Outcome

Implements D11: the per-invocation cap, per-customer allowances and an
operator kill switch that sends customers to the web form, with drafts kept.

## Scope

- In: allowance table (claims per day, turns per session, photos per claim)
  checked atomically before each turn; `max_llm_calls` from configuration;
  kill-switch flag read per request, outside agent authority; the fallback
  response with the form link; usage counters per session.
- Out: shared token budget (later list).
- Depth: production.

## Acceptance

- [ ] The fourth new claim in a day for one customer is refused with the form link.
- [ ] A scripted model that keeps calling tools stops at the cap with a clean message.
- [ ] Kill switch on: new turns get the form link within one request; drafts and ledger untouched; executor keeps running.
- [ ] Two concurrent turns cannot both pass the last allowance unit.

Verification: offline tests with Postgres for the concurrency case.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-budgets-kill-switch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
