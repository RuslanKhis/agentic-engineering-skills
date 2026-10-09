---
goal: G03
title: Five gold questions show where answers are right before the demo, and give a backup table
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-operational-guardrails]
blocked_by: [G02]
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted
  hands_on: 0.5-0.75
  review_and_verify: 0.25
  total: 0.75-1
  calendar_waits: none
owner: You
status: ready
---

# G03 Five gold questions and a demo backup

## Outcome

Before the demo you know how many of 5 checked questions the agent gets right.
A saved results table is the fallback if the live demo fails. Implements the
D2 and D3 checks and the G03 row of the depth table.

## Scope

- In: `eval/gold_questions.json`, written by you. It holds 4 answerable
  questions, each with the expected title, page and a one-line expected
  answer, plus 1 question the policies do not cover. `scripts/run_gold.py`
  runs each question in a fresh in-memory session through an ADK `Runner`
  with `RunConfig(max_llm_calls=10)`. It records the answer, the cited pages,
  the search calls and an automatic "expected page cited" flag to
  `results/gold-<date>.md`. You judge whether each answer is correct. At most
  one tuning pass on the instruction or `top_k`; record the before and after
  results.
- Out: a labelled set of 25–40 questions and a source-support judge (G04);
  retrieval changes beyond `top_k` (G05).
- Depth: POC, with a handful of checked cases. The floor is the per-question
  call cap. Any spend from repeated runs is reported.

## Acceptance

- [ ] The results table lists all 5 questions with answer, cited pages, the
      automatic flag and your verdict. A question that hit the call cap or
      errored appears as failed, not missing.
- [ ] The out-of-scope question gets the not-found answer.
- [ ] If fewer than 4 of the 5 questions pass (the expected page is cited,
      or the not-found answer is given for the out-of-scope question), the
      table says so and the design notes that G05 moves forward. The results
      are not edited to look better.

Verification: a unit test of the table writer and the flag logic, using a
fake result, runs offline. The gold run itself is a bounded local live run
(5 questions × at most 10 calls).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G03-gold-check.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
