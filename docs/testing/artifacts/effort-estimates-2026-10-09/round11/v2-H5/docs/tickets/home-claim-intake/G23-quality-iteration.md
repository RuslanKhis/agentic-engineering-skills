---
goal: G23
title: The assistant meets the release quality threshold on held-out claims
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G06, G07]
phase: 1
profile: production
estimate:
  hands_on: 28-40
  review_and_verify: 6-9
  total: 34-49
  calendar_waits: none
owner: ML
status: proposed
---

# G23 The assistant meets the release quality threshold on held-out claims

## Outcome

Error analysis on the dev set and measured changes to instruction, tool
descriptions and model settings until T3 holds on the held-out set.
Handoff: 1 h from Eng A on the instruction.

## Scope

- In: dev-set runs, failure categories, prompt versions `intake-v2…`,
  thinking-level comparison, one held-out run at the end.
- Out: a model change (that is a release through G19 and a design change).
- Depth: production.

## Acceptance

- [ ] A1 The held-out set, run once at the end, shows required-field accuracy ≥ 95 %, 0 coverage statements and a median of ≤ 12 turns, or the gap is reported as a GA blocker with its cause.
- [ ] A2 No dev case that passed at the G07 baseline fails at the final version without a recorded reason.

Verification: bounded live runs under the non-prod cap, recorded in
`evals/summary.md`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G23-quality-iteration.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
