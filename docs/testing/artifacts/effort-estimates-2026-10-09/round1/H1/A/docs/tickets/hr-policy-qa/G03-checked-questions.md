---
goal: G03
title: Twelve checked questions show HR leadership how often the answers are right and cited
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: [G02]
phase: 1
profile: proof of concept
estimate: 0.75–1.0 h
status: blocked (by predecessor goals; ready in design)
---

# G03 Twelve checked questions show HR leadership how often the answers are right and cited

## Outcome

`python scripts/run_questions.py evals/questions.json` runs 12 questions through the agent and writes `evals/results/<date>.md`. The table has one row per question: the question, the expected document and section, the retrieved documents, the answer, the cited sections, and a pass/fail column for retrieval and for answer. That table is the demo's evidence that the agent is right, and the record of where it misses. Implements the "core judgment, measured" depth and the D5 runner limit.

## Scope

- In: `evals/questions.json` with 12 questions you write from the PDFs: 8 answerable from one policy, 2 that need an exception or a second document, and 2 the policies do not cover. Each has its expected document and section. `scripts/run_questions.py` uses the ADK `Runner` with in-memory sessions, a fresh session per question and `RunConfig(max_llm_calls=6)`. It records the tool calls and returned section IDs from events. You score the answers by hand; the script scores retrieval automatically against the expected section.
- Out: an LLM judge, repeats or statistics (G07), CI (G07), more than 12 questions.
- Depth: POC. One run of a handful of checked cases is enough. Keep the floor: per-question call limit and a hard stop after 12 questions. Left for later: HR-reviewed expected answers (G07).
- If time runs short, cut to 6 questions (4 answerable, 1 exception, 1 not covered). Never drop the not-covered cases.

## Acceptance

- [ ] The results table exists with 12 rows. Retrieval hit rate and hand-scored answer correctness are written at the top.
- [ ] Both not-covered questions are declined without an invented policy. A fluent invented answer counts as a fail.
- [ ] Each miss is labelled `query_miss`, `empty_extraction` or `answer_error` from the recorded tool results, not from the model's explanation.
- [ ] Forbidden: no question runs more than 6 model calls. The runner reports and stops a question that hits the limit instead of retrying.

Verification: authorised live, local. About 12 × 3 model calls on the paid key. An offline `pytest tests/test_runner.py` with a stubbed model checks the table writer and the call-limit handling (it needs the pinned `google-adk`).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G03-checked-questions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
