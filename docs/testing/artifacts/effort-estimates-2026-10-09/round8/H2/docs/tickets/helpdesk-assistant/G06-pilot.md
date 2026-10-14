---
goal: G06
title: Three helpdesk agents use it on real calls and we record what they found
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: [G05, G02]
phase: 1
profile: internal tool
estimate:
  hands_on: 1-2
  review_and_verify: 0.5-0.5
  total: 1.5-2.5
  calendar_waits: none
owner: Dev A
status: blocked
---

# G06 Three helpdesk agents use it on real calls and we record what they found

## Outcome

A short pilot gives usefulness feedback and tokens per turn, and turns failed
questions into gold cases (A12; hypothesis of time saved stays labelled). Includes 0.5 h handoff from Dev B.

## Scope

- In: brief three agents, collect their failed or wrong answers, read token counts from logs, add up to five cases to `eval/gold.jsonl`, write a one-page pilot note.
- Out: rollout to all 25 (decision after the note), ticketing (phase 2).
- Depth: no conversation text copied into the note beyond the question.

## Acceptance

- [ ] Pilot note lists questions asked, found/not found, and median tokens per turn.
- [ ] Every wrong answer reported becomes a gold case or a stated reason why not.
- [ ] No case added contains personal data.

Verification: G02 runner re-run on the enlarged set.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G06-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
