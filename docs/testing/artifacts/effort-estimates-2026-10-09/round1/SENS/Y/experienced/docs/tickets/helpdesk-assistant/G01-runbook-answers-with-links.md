---
goal: G01
title: A technician gets runbook steps with links (local)
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 2-3
  total: 4-6
  calendar_waits: Atlassian Confluence read-only token, 1-3 days (live check only; start on recorded fixtures)
owner: Engineer A
status: ready
---

# G01 A technician gets runbook steps with links (local)

## Outcome

Asking "VPN error 809 on Windows" returns the steps from the matching runbook with its page URL, reading only allowlisted spaces. Implements D1, D2, D6 and invariants I3, I5, I6. Every decision is provisional on the assumed answers at the top
of the design. The implementation route is in the plan's G01 section.

## Scope

- In: `helpdesk_assistant/config.py`, `prompt.py` (instruction v1), `agent.py` (`build_agent()`), `tools/runbooks.py` (`search_runbooks`, `read_runbook`), `clients/confluence.py`, offline tests (all proposed paths)
- Out: ticket drafting (G03), HTTP and web page (G04), gold-set measurement (G02), injection cases (G10)
- Depth: internal-tool depth: space allowlist built in code and checked on every page, results bounded (5 hits, 8,000 characters per page). Floor: token from environment or Secret Manager only, model `gemini-3.8-flash` pinned, `RunConfig(max_llm_calls=8)`. Adversarial cases are left to G10.

## Acceptance

- [ ] ADK version confirmed against the team's pin (assumed `google-adk==2.8.0`) and recorded in Evidence
- [ ] Scripted-model Runner test: `search_runbooks` then `read_runbook`; final reply contains the page URL
- [ ] `read_runbook` with a page ID from a non-allowlisted space returns `status: not_allowed` and no page text
- [ ] Empty search returns `status: no_results`; scripted flow answers "no runbook found" and never searches outside the allowlist
- [ ] Confluence 401/5xx becomes an actionable error result, not an exception
- [ ] Tool declaration dump shows exactly 2 tools; results stay within bounds
- [ ] (live, authorised) one read-only query against real Confluence returns allowlisted pages

Verification: `pytest tests/test_runbooks.py tests/test_agent_g01.py` (offline); item 7 is a bounded live check needing the token and the user's go-ahead.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-answers-with-links.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
