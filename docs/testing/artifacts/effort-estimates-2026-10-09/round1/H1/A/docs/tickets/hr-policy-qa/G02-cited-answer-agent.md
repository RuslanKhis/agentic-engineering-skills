---
goal: G02
title: I ask an HR policy question in adk web and get a short answer citing the policy, or "not covered, contact HR"
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G01, "open decision 1: approval to send policy text to the Gemini API (live calls only)"]
phase: 1
profile: proof of concept
estimate: 1.25–1.75 h (includes about 0.5 h first-time ADK setup)
status: blocked (by predecessor goals; ready in design)
---

# G02 I ask an HR policy question in adk web and get a short answer citing the policy, or "not covered, contact HR"

## Outcome

`adk web` shows an `hr_policy_agent`. A question such as "How many days of annual leave can I carry over?" gets a short answer quoting or paraphrasing the operative section and naming document, section and page. A question the policies do not cover gets "not covered in the policies provided; please contact HR". Implements D1, D3 and D4. The offline tests and the tool can be built before data approval; only the live check waits for it.

## Scope

- In: `hr_policy_agent/tools.py` with one function tool `search_hr_policies(query: str) -> dict`. It opens the G01 index read-only, returns at most 5 sections and about 6,000 characters in total, each with `document`, `heading`, `pages` and `text`, and `status` set to `ok`, `no_match` or `index_unavailable`. The docstring says when to search and how to rephrase. `hr_policy_agent/agent.py` with one `LlmAgent` (`root_agent`) and the literal model ID `gemini-3.8-flash`. The instruction says: answer only from returned sections, cite each claim, state a conflict between two policies, decline when nothing relevant comes back, never give advice about a named person's case, and make at most three searches. Settings live in one module, and `GEMINI_API_KEY` is read from `.env`.
- Out: question set and runner (G03), spend cap and rehearsal (G04), sign-in and hosting (G05), structured output schema (not needed: the answer is prose for a person).
- Depth: build at POC depth. Keep the floor: key never in code, prompt or logs; read-only tool, with no write or egress tool on the agent; pinned model ID. Left for later: per-user allowance (phase 2), log redaction (G08), observability (G09).

## Acceptance

- [ ] Constructor and tool names (`LlmAgent`, `FunctionTool` or plain-function tools, `adk web` app discovery) are confirmed against the pinned `google-adk` version. Differences from 2.8.0 are recorded.
- [ ] Offline: `search_hr_policies` returns `ok` with at most 5 bounded sections for a fixture query, `no_match` for nonsense, and `index_unavailable` when the index file is missing. It never raises to the model.
- [ ] Offline: the agent declares exactly one tool, and its model is the literal `gemini-3.8-flash`. The model ID was re-checked as stable on Google's models page on the run date.
- [ ] Live, after data approval: three real questions are answered with a citation that matches a returned section, and one off-topic question ("What is the company's share price?") is declined.
- [ ] Forbidden: no file is written, and nothing besides the model API is called, during a question.

Verification: offline is `pytest tests/test_tool.py tests/test_agent_config.py`. The second file imports `google.adk`, so it needs the pinned install. Live is authorised manual use of `adk web` with the paid key, 4 questions.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G02-cited-answer-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
