---
goal: G02
title: Ask a policy question in adk web and get a short answer citing title and page
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-memory-architecture]
blocked_by: [G01]
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted
  hands_on: 0.5-0.75
  review_and_verify: 0.5-0.75
  total: 1-1.5
  calendar_waits: none
owner: You
status: ready
---

# G02 Cited answers in adk web

## Outcome

You type an HR question in `adk web` and get two to four sentences that cite
`[title, p.N]`. A question the policies do not cover gets "not found in the
policies, please contact HR". Implements D2, D3 and D6.

## Scope

- In: `hr_policy_agent/search.py`. It loads `pages.jsonl` once and ranks pages
  with pure-Python BM25 (no new dependency). The function tool
  `search_policies(query: str)` returns
  `{"status": "ok"|"no_results", "passages": [{"title", "page", "text"}]}`,
  with at most 5 passages of at most ~1,500 characters each. The docstring is
  written for the model.
  `hr_policy_agent/agent.py` defines `root_agent = LlmAgent(...)` with the
  model from config and `tools=[search_policies]`. Its instruction follows D3:
  answer only from passages, cite every claim, use at most 3 searches, give
  the not-found wording, and end with "Check the cited policy before acting."
  Tool tests and instruction tests go in `tests/`.
- Out: gold-question runner (G03); citation validator in code (G06); semantic
  search (G05); hosting (G07).
- Depth: POC. The floor: one read-only tool and no write or egress tools; the
  model ID comes from config. Grounding is enforced by the instruction only;
  the code control follows in G06.

## Acceptance

- [ ] On a 3-document fixture index, "carry over annual leave" ranks the leave
      page first. An unrelated query returns `no_results`. No result exceeds
      5 passages or the character cap.
- [ ] A test asserts that the agent's tools are exactly `[search_policies]`.
      Other tests assert the instruction contains the citation rule and the
      not-found rule.
- [ ] In `adk web`, 3 questions you choose return correct `[title, p.N]`
      citations that you check against the PDFs. One out-of-scope question
      ("What is the CEO's salary?") gets the not-found answer, without
      invented policy.

Verification: `pytest tests/test_search.py` runs offline. `tests/test_agent.py`
imports google.adk and needs the dependencies installed. The `adk web` check
is a local live run against Vertex AI, authorised by G01.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G02-cited-answers.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
