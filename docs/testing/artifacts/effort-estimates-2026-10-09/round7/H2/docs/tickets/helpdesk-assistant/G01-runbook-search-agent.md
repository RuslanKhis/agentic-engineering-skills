---
goal: G01
title: A helpdesk agent asks a question locally and gets runbook steps with cited pages
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, safe-api-tool-calls, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate:
  hands_on: 2-3
  review_and_verify: 1-1
  total: 3-4
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Cited runbook search, local

## Outcome

A local `LlmAgent` answers from Confluence runbooks through `search_runbooks`
and `read_runbook`, and cites the pages it used (D1, D2, D3, D8; I3, I7, I8).

## Scope

- In: pin `google-adk` (confirm 2.8.0 or record the chosen pin and any
  signature differences); `agent.py`; `tools/confluence.py` with an 8 s
  timeout, one retry on reads, spaces from config added in code, results
  bounded as in the design; versioned instruction file; `gemini-3.8-flash`
  pinned; `RunConfig(max_llm_calls=10)`; fake Confluence client.
- Out: drafts (G02), web (G03), live Confluence (G05).
- Depth: build. Floor: token from env or Secret Manager only.

## Acceptance

- [ ] Scripted model: search → read → answer cites the returned page.
- [ ] Confluence timeout or 5xx → `status: unavailable`; the answer says so and invents no steps.
- [ ] No tool declares a space argument; the CQL always contains the config spaces (I3).
- [ ] A looping scripted model stops at 10 calls (I7).

Verification: offline `pytest tests/` with fakes and a scripted model; a rendered-request dump lists 2 tools.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
