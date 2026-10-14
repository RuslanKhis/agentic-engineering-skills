---
goal: G15
title: Spend and abuse are bounded, with a kill switch an operator controls
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 12-20
  review_and_verify: 4-8
  total: 16-28
  calendar_waits: none
owner: Agent
status: blocked
---

# G15 Spend and abuse are bounded, with a kill switch an operator controls

## Outcome

Implements D11 and I7.

## Scope

- In: `RunConfig.max_llm_calls`, session turn cap, per-customer daily draft allowance with atomic increment in Cloud SQL, photo limits wired to G07, kill-switch flag read per request (not settable by the agent), degraded message with web form / phone.
- Out: Cost tuning (P2-05).
- Depth: Build. The submission worker is deliberately not stopped by the kill switch.

Supporting skills and why:
- none

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] Each limit, when hit, ends the turn with the designed message, and the draft is kept.
- [ ] Two concurrent requests at the allowance boundary cannot both pass (concurrency test).
- [ ] With the kill switch on, new sessions are declined, and a queued submission still completes.

Verification: Offline tests, with Postgres for the concurrency case.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G15-budgets-and-kill-switch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
