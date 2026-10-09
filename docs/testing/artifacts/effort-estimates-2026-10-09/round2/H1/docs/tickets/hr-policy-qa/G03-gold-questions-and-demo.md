---
goal: G03
title: Six known HR questions are measured and the demo is scripted
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: [G02]
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted, x1.5 new-to-ADK applied
  hands_on: 0.5-0.75
  review_and_verify: 0.25
  total: 0.75-1
  calendar_waits: none
owner: the builder
status: ready
---

# G03 Six known HR questions are measured and the demo is scripted

## Outcome

HR leadership sees a table showing how the agent did on six questions
whose answers the builder checked in the PDFs, and the builder has a rehearsed
demo script with a fallback. Checks D1 and D2.

## Scope

- In: `eval/gold.json` with 6 questions written by the builder: 5 answerable,
  each with expected doc and page(s); 1 off-corpus, expecting the fixed reply;
  `eval/run_gold.py`, which runs each question through `Runner` with
  `RunConfig(max_llm_calls=6)` and a fresh in-memory session, then writes
  `eval/results.md` with columns: question, expected doc in top 5 retrieved,
  every cited (doc, page) among the retrieved passages (code check), answer (for
  the builder to mark right or wrong by eye); `docs/demo-script.md` with 4–5
  questions in order, the "POC, check the cited page" line, and the fallback
  (show `results.md` if the model is unavailable).
- Out: an LLM judge, repeated runs and a larger set (P2-2).
- Depth: POC: a handful of checked cases. Floor kept: invented questions, no
  real employee data; call cap per question.
- Cut rule from the plan: if G01 + G02 took more than 2.75 h, do only 4
  questions by eye in `adk web` and move `run_gold.py` to phase 2.

## Acceptance

- [ ] `eval/results.md` is generated from one run of all 6 questions.
- [ ] At least 5 of 6 rows show the expected document retrieved, or each miss
      is written in the demo script as a known limit.
- [ ] The off-corpus question gets the fixed reply, not an invented policy.
- [ ] No cited (doc, page) falls outside the retrieved passages; any such row is flagged.

Verification: `pytest tests/test_run_gold.py` (offline, stubbed agent output, checks
the citation checker); `python eval/run_gold.py` (authorised live, ≤ 36 model calls).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G03-gold-questions-and-demo.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
