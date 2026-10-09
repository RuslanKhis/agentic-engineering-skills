---
goal: G08
title: Hostile text or photos cannot make the agent act for someone else or run away with cost
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-operational-guardrails]
blocked_by: [G04]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 14-22
  review_and_verify: 6-10
  total: 20-32
  calendar_waits: none
owner: Eng E
status: blocked
---

# G08 Hostile text or photos cannot make the agent act for someone else or run away with cost

## Outcome

Tests invariants I4 and I7; implements D6 checks and D10 limits.

## Scope

- In:
  - Trifecta table per agent/call
  - `before_tool_callback` capability checks keyed on trusted state
  - Scripted-model adversarial cases: instructions in a photo suggestion, a foreign policy reference, a request for another claim, skipping confirmation, extracting a coverage promise, loop exhaustion
  - 20 photos and 40 turns per session; 3 new claim sessions per customer per day
- Out: Penetration test (G23), surge admission (G19)
- Depth: Build.

## Acceptance

- [ ] Each adversarial case asserts the forbidden tool call never ran and no foreign data appears
- [ ] A 4th claim session in a day is refused with the web-form link
- [ ] Limits hold across a process restart

Verification: Offline scripted-model tests.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G08-adversarial-suite-and-budgets.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
