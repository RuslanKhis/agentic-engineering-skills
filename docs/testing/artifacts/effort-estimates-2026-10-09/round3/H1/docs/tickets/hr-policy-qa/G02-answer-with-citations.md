---
goal: G02
title: Ask a policy question in adk web and get a cited answer or "not covered"
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md
primary_skill: adk-memory-architecture
supporting_skills: [adk-tool-interface-design, adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G01]
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted, x1.5 new-to-ADK included
  hands_on: 0.5-0.8
  review_and_verify: 0.5-0.7
  total: 1.0-1.5
  calendar_waits: data-use confirmation O1, requested before day 1
owner: Builder
status: ready
---

# G02 Ask a policy question in adk web and get a cited answer or "not covered"

## Outcome

In `adk web`, a question about an HR policy gets a short answer citing
*(Policy title, p. N)*, and a question the policies do not cover gets the fixed
"not covered by these policies, please contact HR" reply. Implements D1–D6.

## Scope

- In: `hr_policy_agent/agent.py` with one `LlmAgent` (`root_agent`), model ID
  from `config.py` pinned to `gemini-3.8-flash`; tools `list_policies()` (catalogue
  rows) and `read_policy(doc_id, first_page=1, last_page=None)` returning
  `{status, title, pages:[{page, text}], truncated, next_page}` bounded to about
  40k characters, with actionable errors for an unknown id or bad range;
  instruction per D2 (answer only from tool text, cite title and page, fixed
  refusal, no individual advice); `.env.example` with the key name only;
  offline tests for both tools; confirm the ADK 2.8.0 APIs used.
- Out: gold-question runner (G03), hosting and identity (G05), model escalation (G04).
- Depth: POC. Floor kept: key only in git-ignored `.env`; pinned model ID; read-only tools,
  no egress; budget alert on the model project noted as a manual step.
  Deferred: Secret Manager, observability, structured output schema (prose with
  citations is the contract at this profile).

## Acceptance

- [ ] Offline: `read_policy` on the largest document returns `truncated: true`
      and a `next_page`; an unknown id returns `status: "error"` with a hint to
      call `list_policies`; the agent declares exactly two tools.
- [ ] Live (after O1): one answerable question returns an answer with at least
      one correct title-and-page citation; one off-topic question returns the
      fixed "not covered" reply without invented policy text.
- [ ] No API key appears in source, prompt text or committed files.

Verification: offline `pytest tests/test_tools.py` (no network); bounded live check in
`adk web` with two questions, using the builder's own key on the approved project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G02-answer-with-citations.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
