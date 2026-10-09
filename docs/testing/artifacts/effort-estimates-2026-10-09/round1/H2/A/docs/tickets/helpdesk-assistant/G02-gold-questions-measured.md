---
goal: G02
title: Answer quality is measured on real helpdesk questions
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G01]
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  calendar_waits: one hour of the helpdesk lead's time to choose and label questions
owner: Engineer A
status: blocked
---

# G02 Answer quality is measured on real helpdesk questions

## Outcome

A measured citation hit rate on 20-25 real questions decides whether live CQL search (D2) is good enough or G08 starts. Implements I5. Every decision is provisional on the assumed answers at the top
of the design. The implementation route is in the plan's G02 section.

## Scope

- In: `eval/gold.jsonl` (question, expected page IDs or `none`), `eval/run_gold.py` recording model ID, prompt version, answer, cited URLs, tool-returned URLs, LLM call count and pass/fail per case
- Out: CI gate (G09), LLM judge, instruction rewrites beyond what error analysis shows
- Depth: small regression set (internal tool). Floor: per-turn call cap; total run of about 100 model calls stated before it starts; questions from recent `ITHD` issues with names removed.

## Acceptance

- [ ] Every case appears in the run record with pass/fail; failed or missing runs count as failures
- [ ] Citation hit rate and no-runbook pass rate (at least 3 no-runbook cases) recorded against the provisional 80% target
- [ ] No case cites a URL that its tools did not return in that turn
- [ ] Decision on G08 (start or not) recorded in the plan

Verification: `python eval/run_gold.py --out eval/runs/<date>.jsonl`: bounded live run against Vertex in a dev project, after the user's go-ahead.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G02-gold-questions-measured.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
