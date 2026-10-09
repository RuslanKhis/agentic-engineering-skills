---
goal: G06
title: 30-case evaluation set and runner
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 4.5-8
  review_and_verify: 1.5-2.5
  total: 6-10.5
  calendar_waits: none
owner: Dev A
status: blocked
---

# G06 30-case evaluation set and runner

## Outcome

A labelled set the team runs before each release: 10 book, 6 move, 5 cancel, 5 clarify, 4 refuse. Deterministic assertions on tool calls and proposal fields; no judge model. Supports D1.

## Scope

- In: `evals/cases.jsonl`, `evals/run.py` (Runner + fake booking API + pinned model), `evals/results/latest.md`
- Out: CI gate (G10); write cases are rerun in G09 after G03 merges
- Depth: run by hand; ≤ 200 model calls per run

## Acceptance

- [ ] Read and clarify cases report a pass rate per category
- [ ] Failed and errored cases are listed separately
- [ ] Each run records model ID, prompt version and date

Verification: `python evals/run.py`, bounded live against Vertex AI on the dev project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
