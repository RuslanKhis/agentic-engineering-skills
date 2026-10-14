---
goal: G08
title: The assistant meets its evaluation bar before go-live
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G02, G03, G07]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev B
status: blocked
---

# G08 The assistant meets its evaluation bar before go-live

## Outcome

Run G07 live against `gemini-3.8-flash` and tune the instruction and tool docstrings until the bar is met.

## Scope

- In: Live runs, at most 3 repeats × 30 cases per iteration, with a token count recorded
- In: Instruction and docstring changes, each with a recorded rerun
- Out: Out: model changes (a release; see Later)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] ≥ 27/30 cases pass on 2 consecutive runs (provisional bar; the user may move it)
- [ ] Zero forbidden-effect failures, including all injection cases
- [ ] Token cost per case recorded for D6

Verification: authorised live model calls against the fake booking API; spend under USD 20.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-eval-and-tuning.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
