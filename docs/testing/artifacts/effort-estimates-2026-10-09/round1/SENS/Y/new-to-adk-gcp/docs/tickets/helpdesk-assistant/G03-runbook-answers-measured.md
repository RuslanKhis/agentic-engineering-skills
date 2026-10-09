---
goal: G03
title: Runbook answers measured on real Confluence
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions, protect-adk-sensitive-data]
blocked_by: [G01, G02]
phase: 1
profile: internal tool
estimate:
  hands_on: 2-4
  review_and_verify: 2-3
  total: 4-7
  calendar_waits: about 2 hours of the helpdesk lead's time to label the gold questions
owner: Engineer A
status: ready
---

# G03 Runbook answers measured on real Confluence

## Outcome

The helpdesk lead sees a scored table showing how often the assistant cites
the right runbook on real questions. This is the phase 1 quality evidence.
Implements D2 and D5, and invariant I4.

## Scope

- In:
  - `eval/gold_questions.yaml`: about 20 real questions with expected page
    IDs, 3 of them with no runbook.
  - `eval/run_gold.py`, producing hit @1 and @5 and a "none found"
    correctness check.
  - A summary under `eval/results/`.
  - Prompt adjustments for misses.
  - A secret-pattern scan of the configured space(s).
- Out: semantic retrieval (Later), CI gate (G08), judge model.
- Depth: small regression set, scored by exact page ID match plus a human read
  of the answers. At most 200 model calls per run. No message content in logs.

## Acceptance

- [ ] The results table reports hit @1 and @5 against the provisional target
  of 70% @5, with the run's model ID and prompt hash.
- [ ] All 3 no-runbook questions are answered "none found" with no invented
  steps.
- [ ] The secret scan finds 0 hits, or its hits are reported to the knowledge
  owner and that space stays out of config until they are fixed.

Verification: authorised live (Confluence read-only and Vertex AI), with call
limits written in the run record.

## Evidence

<!-- Filled in by the agent that carries this ticket out. -->

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G03-runbook-answers-measured.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
