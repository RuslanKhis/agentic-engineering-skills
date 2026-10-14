---
goal: G01
title: A staff member asks a runbook question and gets cited steps
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-agent-evaluation, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  calendar_waits: helpdesk lead supplies ~20 gold questions (needed by day 3)
owner: Dev A
status: ready
---

# G01 A staff member asks a runbook question and gets cited steps

## Outcome

Local agent answers from the allowlisted Confluence runbook spaces with a cited URL; implements D1, D2, D3, D8 and measures I5.

## Scope

- In: `app/agent.py`, `app/tools/confluence.py` (search_runbooks, get_runbook), instruction, `eval/gold.jsonl` and runner, offline fakes.
- Out: tickets (G02), UI (G03), deployment (G04).
- Depth: small measured gold set; floor: pinned model, `max_llm_calls=8`, token from env/Secret Manager; retrieval index deferred to G10.

## Acceptance

- [ ] Search returns ≤5 bounded hits; page text capped at 8,000 chars; recall@5 and cited-page rate recorded on the gold set (target ≥80%, assumed)
- [ ] Confluence 503 → agent says search unavailable and gives no steps; looping scripted model stops at 8 calls
- [ ] A page outside the space allowlist is refused and never reaches the model
- [ ] `google-adk` pin and model ID confirmed against the lifecycle file

Verification: offline `pytest tests/test_confluence.py tests/test_agent_limits.py`; bounded live `python eval/run_gold.py` with a read-only token.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
