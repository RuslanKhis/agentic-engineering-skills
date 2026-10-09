---
goal: G13
title: "Model work is bounded per turn, draft, customer and globally, with an operator stop"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-operational-guardrails
supporting_skills: []
blocked_by: [G01]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 10-14
  review_and_verify: 4-6
  total: 14-20
  calendar_waits: none
  wait_days: 0
owner: Agent lead
status: blocked
---

# G13 Model work is bounded per turn, draft, customer and globally, with an operator stop

## Outcome

Every limit in D14 enforced with a clear customer message; confirmed submissions unaffected by the stop. Implements D14, I8; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g13--model-work-is-bounded-per-turn-draft-customer-and-globally-with-an-operator-stop).

## Scope

- In: `max_llm_calls`; counters; stop flag; messages.
- Out: Shared reservations (P2-01).
- Depth: Build at per-request admission depth.

## Acceptance

- [ ] A scripted model looping on a tool stops at 15 calls with the handoff message.
- [ ] Sixth draft in a day is refused; operator stop blocks new sessions but a queued submission completes.
- [ ] Counters survive a restart.

Verification: Offline tests; restart test. Execution scope: Local.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-budgets-and-operator-stop.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
