---
goal: G01
title: GCP foundation and a pinned model answering locally
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 5-8          # includes the 4-6 h first-GCP-project day
  review_and_verify: 0.5-1
  total: 5.5-9
  calendar_waits: GCP project + billing link from cloud admin (assume 1-5 working days); Atlassian bot accounts + API tokens (assume 1-5 working days). File both on day 1.
owner: Engineer B
status: ready
---

# G01 GCP foundation and a pinned model answering locally

## Outcome

An engineer runs a minimal agent locally that answers through the pinned
Vertex AI model (`gemini-3.8-flash`), with both Atlassian tokens held in
Secret Manager and a billing budget alert in place. Implements D6, D7 and the
version decision in the design.

## Scope

- In: GCP project and region; Vertex AI API; budget alert at 50/90/100%;
  Secret Manager secrets `confluence-token` and `jira-token` (values entered by
  a person); runtime service account (created, not deployed); repository
  skeleton with `google-adk==2.8.0` pinned and a lock file; `config.py`
  holding `MODEL_ID`; hello `LlmAgent`; `.gitignore` for env files.
- Out: Confluence and Jira tools (G02, G03); hosting (G05).
- Depth: secrets built properly; budget alert only (observation, not a cap);
  no CI (G09).

## Acceptance

- [ ] A local call returns a model response; the logged model ID equals `config.py`'s `MODEL_ID`.
- [ ] `LlmAgent`, `App`, `Runner`, `RunConfig.max_llm_calls` and `FunctionTool(require_confirmation=...)` are confirmed against the installed pin, with differences recorded.
- [ ] Region availability and price of the pinned model are recorded with source URL and access date.
- [ ] No token or key appears in git (`git grep` for token prefixes and `.env` finds nothing); both secrets exist in Secret Manager.
- [ ] A budget alert exists on the project's billing account.

Verification: local integration with the engineer's own credentials;
`pytest -q` (skeleton import test) offline.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-gcp-foundation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
