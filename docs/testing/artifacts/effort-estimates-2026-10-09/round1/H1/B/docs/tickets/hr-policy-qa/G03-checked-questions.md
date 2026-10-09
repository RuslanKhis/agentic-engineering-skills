---
goal: G03
title: Ten checked questions show HR leadership how often the agent is right
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: [G02]
phase: 1
profile: proof of concept
estimate:
  hands_on: 0.75-1.0
  review_and_verify: 0.25-0.5
  total: 1.0-1.5
  calendar_waits: none
owner: builder
status: ready
---

# G03 Ten checked questions show HR leadership how often the agent is right

## Outcome

A results table with 10 questions, the expected document and page, the agent's
answer, the documents it opened and the user's verdict. Three demo questions are
chosen, and their answers are saved as a fallback. Implements the measurement
for D1 and D2.

## Scope

- In: `eval/questions.yaml`, which the user writes. It has 10 questions in
  the words an HR manager would use. Eight have `expected_doc` and
  `expected_page`, and at least one of those needs an exception or a second
  document. Two are not covered by the policies.
- In: `eval/run_questions.py`, which runs each question once in a fresh
  in-memory session through the Runner with `RunConfig(max_llm_calls=8)`. It
  records the answer, the `read_policy` calls and the cited pages.
  - A deterministic check confirms that each cited document exists and each
    page is within range.
  - The script writes `eval/results.md`.
- Hands-on: the user marks each row correct, partly correct or wrong.
- Out: CI gate and a larger set (P2-3), and a judge model (not needed for 10
  rows).
- Depth: POC with a handful of checked cases. Cost is bounded: 10 questions ×
  up to 8 calls. If the work runs high, cut to 6 questions and skip prompt
  revision (see the cut line).

## Acceptance

- [ ] `eval/results.md` has 10 rows, each with an answer, the documents opened,
  a deterministic citation-check result and a verdict. A failed run shows as
  a row marked `error` and is never dropped.
- [ ] Both uncovered questions get the "not covered" answer. If not, it is
  recorded as a failure, not hidden.
- [ ] Every row records whether the expected document was opened. This decides
  whether P2-1 is needed.
- [ ] Three demo questions and their saved answers are in `eval/demo.md`.

Verification: run `python eval/run_questions.py` live and locally on the
authorised key, at about 80 calls at most. The user reviews every row by hand.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G03-checked-questions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
