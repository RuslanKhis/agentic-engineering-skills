---
goal: G02
title: Runbook answers with citations, offline
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate:
  hands_on: 1-2
  review_and_verify: 2-3
  total: 3-5
  calendar_waits: none
owner: Engineer A
status: ready
---

# G02 Runbook answers with citations, offline

## Outcome

An analyst's question produces an answer that cites runbook URLs. It runs
against a fake Confluence through the real ADK `Runner`. Implements D1, D2, D4
and D6, and invariants I1, I4 and I5.

## Scope

- In (all proposed modules):
  - `helpdesk_assistant/agent.py`, which builds `root_agent`.
  - `prompt.md`.
  - `config.py`: `MODEL_ID`, `CONFLUENCE_SPACES`, limits.
  - `confluence.py`: a CQL search with the space filter added in code, and a
    page fetch with a space check.
  - `tools.py`: `search_runbooks(query)` returns 5 or fewer hits with title,
    URL, page ID and excerpt; `read_runbook(page_id)` returns text of 8,000
    characters or fewer, or `not_allowed`.
  - `tests/fakes.py` and the tests.
  - `RunConfig(max_llm_calls=8)`.
  - Recording the confirmed ADK 2.8.0 interfaces used.
- Out: live Confluence and the gold set (G03), Jira tools (G04).
- Depth: results bounded at the tool; the space allow-list is enforced in
  code, never in a model argument; pinned model. No write tool yet, so no
  security split.

## Acceptance

- [ ] A scripted model runs search → read → an answer containing the page URL.
- [ ] An empty search returns "no runbook found", and the CQL is not widened.
  A page from space `HR` returns `not_allowed`.
- [ ] A looping scripted model stops at 8 LLM calls. The declaration dump
  shows 4 or fewer tools, with their byte size recorded.

Verification: offline, `pytest tests/` (requires google-adk installed).

## Evidence

<!-- Filled in by the agent that carries this ticket out. -->

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G02-runbook-answers-offline.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
