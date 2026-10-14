---
goal: G11
title: Complete the burst-pipe intake conversation correctly and safely
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-tool-interface-design, adk-agent-evaluation]
blocked_by: [G01, G07, G10]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-21
  review_and_verify: 5-8
  total: 17-29
  calendar_waits: none
  wait_days: 0
owner: Dev A
status: blocked
---

# G11 Complete the burst-pipe intake conversation correctly and safely

## Outcome

The intake agent gathers every required field, handles safety and handoff, and never talks about coverage. Implements D1, D9, I7, I10; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Instruction as versioned code, four tools, `missing_fields` computed in code from the G01 mapping, loss-cause taxonomy, handoff reasons, fixed safety text.
- Out: Language variants (G22), adversarial suite (G20).
- Depth: Production.

## Acceptance

- [ ] On 10 development cases the draft is complete with correct loss cause.
- [ ] "Water is still running" gets the safety text in the first reply; an injury mention leads to `request_handoff(injury)`.
- [ ] "Is this covered?" gets a neutral answer with no coverage statement; four tools, each result under 2 KB.

Verification: Offline scripted tests; bounded live, at most 200 calls.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-intake-conversation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
