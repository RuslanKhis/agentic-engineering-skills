---
goal: G03
title: Ten gold questions show how often the agent is right, and the demo has a recorded fallback
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: [G02]
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted, x1.5 new-to-ADK included
  hands_on: 0.6-1.0
  review_and_verify: 0.2-0.3
  total: 0.8-1.3
  calendar_waits: none
owner: Builder
status: ready
---

# G03 Ten gold questions show how often the agent is right, and the demo has a recorded fallback

## Outcome

The builder can tell HR leadership "it answered N of 10 checked questions
correctly, with citations" and has a recording to play if the live demo fails.
Checks D1 and D2.

## Scope

- In: `eval/gold_questions.yaml` written by the builder (question, expected
  doc_id, expected page(s), expected key fact): 7 answerable, 2 not covered,
  1 needing two documents; `scripts/run_gold.py` running each through an ADK
  `Runner` with `InMemorySessionService` and `RunConfig(max_llm_calls=8)`,
  writing `eval/results-<date>.md` (question, answer, cited pages, opened docs,
  pass/fail column for the builder); a screen recording of a 5-question dry run.
- Out: a larger labelled set and automatic judging (G06); prompt fixes for
  misses (G04).
- Depth: POC, judged by hand. Floor kept: call cap per question; total run
  of 10 questions only; no personal data in questions.

## Acceptance

- [ ] The results table lists all 10 questions with the builder's pass/fail and
      the pass count stated as measured, not rounded up.
- [ ] Both not-covered questions get the fixed refusal and cite nothing.
- [ ] A run that hits `max_llm_calls` is recorded as a failure, not retried silently.

Verification: local integration, `python scripts/run_gold.py` (10 live model calls'
worth of questions, bounded by the cap), plus the builder's hand judgement.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G03-gold-questions-and-dry-run.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
