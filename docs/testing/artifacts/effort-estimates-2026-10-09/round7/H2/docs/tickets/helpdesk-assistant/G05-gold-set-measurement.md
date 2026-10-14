---
goal: G05
title: The helpdesk lead sees how often the assistant finds the right runbook for 20 real questions
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: [G01, W1, W2]
phase: 1
profile: internal tool
estimate:
  hands_on: 2-3
  review_and_verify: 1-1
  total: 3-4
  calendar_waits: none
owner: Dev A
status: blocked
---

# G05 Gold-set measurement

## Outcome

A runner sends the 20 gold questions (W2) through the local agent against live
Confluence (read only, bot token from W1). It records hit@5, the cited-answer
rate and latency in `eval/results.md`, which sets the G09 trigger (D2, D8; I3, I8; O5).

## Scope

- In: `eval/gold.jsonl` (question, expected page IDs); runner with a call
  cap; manual judgement of each answer as correct, partial or wrong; one
  restricted test page that must never appear.
- Out: CI gate (G10), LLM judge.
- Depth: small regression set; no content in shared logs.

## Acceptance

- [ ] `eval/results.md` lists every case, with failures, hit@5, cited-answer rate and p50/p90 latency.
- [ ] The restricted test page appears in no result.
- [ ] The run makes at most 20 × 10 model calls.

Verification: bounded live read against Confluence; offline test of the runner's scoring.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G05-gold-set-measurement.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
