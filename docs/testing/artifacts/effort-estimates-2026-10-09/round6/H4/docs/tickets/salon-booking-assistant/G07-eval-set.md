---
goal: G07
title: 30 labelled conversations define what correct looks like
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev B
status: ready
---

# G07 30 labelled conversations define what correct looks like

## Outcome

A labelled set and runner for D1's tool choices. It uses the tool names fixed in the design, so it starts on day 1.

## Scope

- In: `evals/cases.yaml`: book, move, cancel, ambiguous dates, no availability, out of scope, another customer's ID, and 4 injection attempts
- In: Each case: user turns, fake API state, expected tool calls or proposal, forbidden effects
- In: `evals/run.py` scores tool choice, proposal match and forbidden effects
- Out: Out: tuning (G08), CI gate (G11)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] 30 cases reviewed by a second developer
- [ ] The runner reports per-case pass or fail and missing results
- [ ] The runner fails if any case creates an operation outside its customer

Verification: offline: the runner works with a scripted model; live runs belong to G08.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-eval-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
