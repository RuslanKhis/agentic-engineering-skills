---
goal: G01
title: An agent asks a runbook question locally and gets a cited answer
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-memory-architecture
supporting_skills: [adk-tool-interface-design, adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate:
  hands_on: 2-4
  review_and_verify: 1-2
  total: 3-6
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 An agent asks a runbook question locally and gets a cited answer

## Outcome

`adk run` / a local Runner answers "VPN error 809 on Windows 11" from the runbook
spaces with page URL and version (D1, D2, D6, D8, D11; I3, I4, I5, I7).

## Scope

- In: day 1, request W1 (bot account, helpdesk Google group); confirm the
  `google-adk` pin against the specialists' 2.8.0 reference; `app/agent.py`,
  `app/tools/confluence.py`, instruction, `RunConfig(max_llm_calls=8)`; fixture-based tests.
- Out: web API (G04), deployment (G05), gold set (G02), any Jira tool (G03, G07).
- Depth: read-only tools; space allow-list in config; local token from env only.

## Acceptance

- [ ] Fixture search returns ≤ 5 bounded hits with URL and version; the answer cites one.
- [ ] Empty search or Confluence timeout yields "no runbook found" / "unavailable", no broader query.
- [ ] A query naming another space or containing CQL does not leave the allow-list; declaration dump shows no write tool; a scripted model hits the 8-call cap.
- [ ] One live call confirms `gemini-3.8-flash` on Vertex in the project's region, or the fallback is pinned.

Verification: offline `pytest tests/` with fixtures; one authorised live read and model call.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
