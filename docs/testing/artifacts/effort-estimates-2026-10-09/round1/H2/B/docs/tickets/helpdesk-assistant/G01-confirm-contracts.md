---
goal: G01
title: Confirm the Atlassian, model and ADK pin contracts the build depends on
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [safe-api-tool-calls, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: internal tool
estimate: 2-3 h
status: ready
---

# G01 Confirm the Atlassian, model and ADK pin contracts the build depends on

## Outcome

The team knows the facts that assumptions A5–A7 and decisions D2, D4 and D5
rest on, recorded in `docs/architecture/helpdesk-assistant-contracts.md`.
Settles open decisions O1, O2, O3 and O5.

## Scope

- In: read-only inspection of Confluence and Jira configuration and REST
  documentation; the Vertex AI model-versions page for the chosen region; the
  specialists' `references/compatibility.md` for the ADK pin.
- Out: creating tokens, service accounts or Jira projects (the Atlassian admin
  does that separately); any code.
- Depth: discovery; no secrets or private resource IDs in the record.

## Acceptance

- [ ] Cloud or Data Center recorded for Confluence and Jira, with the auth
      method each needs.
- [ ] Runbook space keys listed; whether any page restriction is narrower than
      the helpdesk group (if yes, D2 is blocked and the design is updated).
- [ ] Jira project key, issue type, required fields, component and priority
      values; whether the create token can set reporter.
- [ ] Whether Jira create supports an idempotency key, and whether a label
      search finds a just-created issue immediately (reconciliation in G04).
- [ ] `gemini-3.8-flash` confirmed on Vertex in the region, or the fallback
      `gemini-3.5-flash` chosen; ADK pin chosen (working assumption 2.8.0).
- [ ] No credential or token value appears in the record.

Verification: reviewed record; stop when every item has an answer or a named
owner. Read-only; any live call goes to a read-only or sandbox target.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-confirm-contracts.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
