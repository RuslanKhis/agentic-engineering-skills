---
goal: G01
title: GCP project, model and Atlassian access ready
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate:
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: GCP project and billing link from the org or finance admin (1-5 working days); Atlassian bot accounts and permissions from the Atlassian admin (1-5 working days). Request both on day 1.
owner: Engineer B
status: ready
---

# G01 GCP project, model and Atlassian access ready

## Outcome

Both developers can call the pinned model on Vertex AI and read the two
Atlassian tokens through Application Default Credentials (ADC). Nothing secret
is in the repository. Implements D5 and D6 and the floor (secrets, spend
alert).

## Scope

- In:
  - A GCP project with billing and the Vertex AI API enabled.
  - A region choice, recorded in the design.
  - A Cloud Billing budget alert at US$100 a month.
  - Secret Manager secrets `confluence-read-token` and `jira-create-token`.
  - Developer IAM roles, including Secret Accessor on those two secrets.
  - `pyproject.toml` pins (`google-adk==2.8.0`, Python 3.11) and `.env.example`
    with resource names only.
  - Re-reading the Vertex model and pricing pages for `gemini-3.8-flash`, then
    recording the URL, date, availability and cost estimate in the design (O5).
- Out: Cloud Run, IAP and the hosting service account (G07).
- Depth: internal tool. Keyless ADC and least privilege. The bots are
  read-only in the runbook space(s) and create-only in `ITHD`.

## Acceptance

- [ ] A one-call smoke test with `gemini-3.8-flash` returns text. If the model
  is unavailable, the fallback `gemini-3.5-flash` is recorded in the design
  with its lifecycle date.
- [ ] Both secrets are read via ADC. A principal without Secret Accessor is denied.
- [ ] The budget alert exists, and `git grep` for the token prefixes finds nothing.

Verification: authorised live, at most 5 model calls. Project creation and
billing need the user's explicit go-ahead.

## Evidence

<!-- Filled in by the agent that carries this ticket out. -->

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-gcp-and-atlassian-access.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
