---
goal: G08
title: "The assistant asks the right questions in DE and EN and never promises cover"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-tool-interface-design, adk-agent-evaluation]
blocked_by: [G01, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 16-24
  review_and_verify: 6-10
  total: 22-34
  calendar_waits: Claims and legal review of fixed messages and phrase lists
  wait_days: 3-5
owner: Agent lead
status: blocked
---

# G08 The assistant asks the right questions in DE and EN and never promises cover

## Outcome

Instruction `intake-v1`, final tool declarations and the deterministic handoff and no-cover screens meet the G09 thresholds. Implements D11, D12, D16, I5, I7; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g08--the-assistant-asks-the-right-questions-in-de-and-en-and-never-promises-cover).

## Scope

- In: Instruction text; tool docstrings; handoff and cover-statement screens per language; iteration on the development set.
- Out: New tools beyond the design's list.
- Depth: Build; gated by G09 set.

## Acceptance

- [ ] Development set: completeness and handoff thresholds agreed in G09 met in both languages.
- [ ] Every injury or emergency case produces the fixed hotline message.
- [ ] No response in the set contains a cover or payout statement after the screen.

Verification: Offline screen tests; live evaluation run with recorded cost. Execution scope: Live model in dev, capped.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G08-intake-instructions-and-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
