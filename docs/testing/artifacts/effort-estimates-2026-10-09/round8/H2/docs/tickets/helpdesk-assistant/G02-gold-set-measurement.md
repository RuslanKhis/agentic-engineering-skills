---
goal: G02
title: We know how often the assistant finds and cites the right runbook
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-memory-architecture]
blocked_by: [G01]
phase: 1
profile: internal tool
estimate:
  hands_on: 2-4
  review_and_verify: 1-1
  total: 3-5
  calendar_waits: none
owner: Dev A
status: blocked
---

# G02 We know how often the assistant finds and cites the right runbook

## Outcome

A 15-case gold set and a runner report retrieval hit@5, citation correctness and
honest "not found" (I4, D2). The baseline decides whether the later index is needed.

## Scope

- In: `eval/gold.jsonl` with 15 real questions from a helpdesk lead (12 answerable, 3 with no runbook), expected page IDs; a runner script; a results table.
- Out: CI gate and growing the set (G09); ticket cases (G09).
- Depth: small regression set; questions contain no personal data.

## Acceptance

- [ ] Runner prints hit@5, cited-page-correct rate and not-found accuracy per case.
- [ ] A case whose search errors is reported as failed, not skipped.
- [ ] The three no-runbook cases do not produce an invented procedure.

Verification: local run against live Confluence with a bounded call count (≤ 15 × 8 model calls).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G02-gold-set-measurement.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
