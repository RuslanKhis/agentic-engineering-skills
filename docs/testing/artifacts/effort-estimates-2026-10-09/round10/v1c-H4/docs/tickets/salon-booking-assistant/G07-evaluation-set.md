---
goal: G07
title: We know how often the assistant gets real requests right before customers use it
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 1-2
  total: 6-10
  calendar_waits: none
owner: Dev B
status: proposed
---

# G07 We know how often the assistant gets real requests right before customers use it

## Outcome

A labelled set of 20 to 25 conversations, written from real phrasing the
salons hear (dates like "next Friday", stylist nicknames, wrong salon,
past appointments, policy edge cases, three adversarial cases), runs against
the pinned model with a result per case (D1, D2, F1, F6).

## Scope

- In: case file, runner against the G02 agent with the booking API fake,
  expected tool calls and proposal fields per case, summary report; prompt
  fixes from error analysis; token counts per case for OD5.
- Out: CI gate and the full adversarial suite (phase 2).
- Depth: build an evaluation set, run by hand before launch.

## Acceptance

- [ ] Every case has expected proposal fields or an expected refusal.
- [ ] Report shows pass/fail per case, failures analysed; launch threshold
      (assumption: no wrong-date or wrong-customer proposal; 90 % overall)
      met or the gap recorded for the go/no-go in G09.
- [ ] Adversarial cases: zero booking API writes, no claim of a completed
      change.

Verification: live model calls on the team's own Vertex project, bounded to
the case count × 3 repeats; not run in this session.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
