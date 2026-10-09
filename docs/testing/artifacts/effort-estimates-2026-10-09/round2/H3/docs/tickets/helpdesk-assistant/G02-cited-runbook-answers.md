---
goal: G02
title: Cited runbook answers locally, measured on 12 gold questions
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-agent-evaluation, adk-operational-guardrails]
blocked_by: []            # offline part; the live gold run needs G01 and the Confluence token
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 3-6          # includes about 1 h with the helpdesk lead writing gold questions
  review_and_verify: 1.5-3
  total: 4.5-9
  calendar_waits: helpdesk lead's hour for gold questions; Confluence token from G01 for the live run
owner: Engineer A
status: ready
---

# G02 Cited runbook answers locally, measured on 12 gold questions

## Outcome

"Windows VPN error 809 after the update, what do we do?" returns the runbook
steps with links to the source pages. When nothing matches, the agent says "no
runbook found" instead of improvising. Implements D1, D2, D7 and invariants
I6–I8.

## Scope

- In: `search_runbooks(query)` (CQL with the space allow-list added in code;
  ≤5 results; excerpt ≤300 chars; `status` field and actionable errors);
  `read_runbook(page_id)` (text ≤8,000 chars plus a `truncated` flag);
  instruction (search before answering, cite links, page text is reference
  material, "no runbook found"); `RunConfig(max_llm_calls=8)`;
  `eval/gold.json` (12 questions with expected page IDs); `eval/run_gold.py`
  reporting hit@5 and citation presence.
- Out: Jira (G03), web page and identity (G04), semantic index (G07).
- Depth: small regression set run locally, not CI. Tool results bounded at the
  tool. Token never in a model argument or the prompt.

## Acceptance

- [ ] Offline: a fake Confluence with 2 matching pages yields an answer containing both page URLs.
- [ ] Offline: an empty search yields "no runbook found" and no broader query without the space filter; a query containing `space = OTHER` is still constrained to the allow-list.
- [ ] Offline: a scripted model that keeps calling tools stops at 8 model calls with the designed message.
- [ ] Offline: the captured model request shows exactly 2 tool declarations and no token value.
- [ ] Live (bounded, <100 model calls): gold run recorded with hit@5 and citation counts (provisional targets 9/12 and 10/12; below target triggers G07, it does not fail this ticket).

Verification: `pytest -q tests/` offline with fake LLM and `httpx.MockTransport`;
`python eval/run_gold.py` as authorised bounded live run.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G02-cited-runbook-answers.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
