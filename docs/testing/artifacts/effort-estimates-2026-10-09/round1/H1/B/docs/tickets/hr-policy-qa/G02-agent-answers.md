---
goal: G02
title: I ask an HR policy question in adk web and get a cited answer
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G01, O1]
phase: 1
profile: proof of concept
estimate:
  hands_on: 0.5-0.75
  review_and_verify: 0.5-0.75
  total: 1.0-1.5
  calendar_waits: O1 (data-use approval for the Gemini API), if not already given
owner: builder
status: ready
---

# G02 I ask an HR policy question in adk web and get a cited answer

## Outcome

The builder runs `adk web`, asks a policy question and gets an answer that cites
`[document title, p. N]`. If the policies do not cover the question, the answer
says so. Implements D1, D2, D4, D5 and D6.

## Scope

- In: a proposed package `hr_policy_agent/` with `agent.py` (`root_agent`) and
  `tools.py`.
  - The `LlmAgent` uses `model="gemini-3.8-flash"`, which is pinned as a
    constant.
  - Code renders the instruction from `data/catalogue.json` at import time.
    The instruction says to answer only from text returned by `read_policy`,
    to cite title and page for every claim, and to answer "not covered by the
    policies I have, please contact HR" when the text does not cover the
    question. It also tells the agent not to give legal advice.
  - `read_policy(doc_id: str, start_page: int = 1) -> dict` returns
    `{status, doc_id, title, pages_returned, total_pages, text}`. The text is
    at most 40 pages and has `--- page N ---` markers. An unknown `doc_id`
    returns `{status: "error", message, valid_ids_hint}`.
- In: `.env.example` with `GOOGLE_API_KEY=`. `.env` is git-ignored.
- In: offline tests that call `read_policy` directly with fixture pages, and a
  Runner test with a scripted model (no network) that checks
  `RunConfig(max_llm_calls=8)` stops a repeated tool loop.
- In: confirm the installed `google-adk` version against the 2.8.0
  assumption. Record any interface differences in Evidence.
- Out: the evaluation set (G03), search index (P2-1), hosting and sign-in
  (P2-2).
- Depth: POC. One read-only tool. Floor: no key in source, prompts or logs;
  the model ID is pinned; spend is bounded by the call limit and a budget
  alert the user sets on the key's project. No `output_schema`: the answer is
  prose with citations, checked in G03.

## Acceptance

- [ ] A question the user knows the answer to returns that answer with a
  citation to the correct document and page. This is a live local run that
  the user authorises; it costs a few cents.
- [ ] A question outside the policies, such as "What is the canteen menu?",
  gets the "not covered" answer without an invented citation.
- [ ] `read_policy("no-such-doc")` returns a status `error` dict and does not
  raise an exception. An over-long document returns 40 pages and
  `total_pages`, and `start_page` reaches the rest.
- [ ] A scripted-model test stops at the call limit without real model calls.
- [ ] The installed `google-adk` version is pinned in the dependency file and
  checked against the 2.8.0 assumption. Any interface difference is recorded
  in Evidence.
- [ ] `grep -r GOOGLE_API_KEY` finds only `.env.example`. The captured request
  shows `gemini-3.8-flash`.

Verification: run the offline tests with `pytest tests/test_tools.py
tests/test_agent_limits.py`, then do the local live check with `adk web`
and two questions.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G02-agent-answers.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
