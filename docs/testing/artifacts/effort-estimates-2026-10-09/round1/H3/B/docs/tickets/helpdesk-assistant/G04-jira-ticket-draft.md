---
goal: G04
title: Asking for a ticket gives a pre-filled Jira create link that the helpdesk agent submits under their own login
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions]
blocked_by: [G01, "A7: Jira site, project key and issue type"]
phase: 1
profile: internal tool
estimate: 3-6 h
status: blocked
---

# G04 Pre-filled Jira ticket draft the user submits

## Outcome

"Raise a ticket for network ops about this" returns a summary, a description
from the conversation and a link that opens Jira's create screen with those
fields filled; the person reviews and submits it themselves. Implements D4
and I4. First goal to move to phase 2 if phase 1 runs over.

## Scope

- In: a spike of at most 1 hour confirming Jira Cloud's create-URL pre-fill
  for project, issue type, summary and description; if unsupported, stop and
  fall back to copyable text plus a plain create link. `draft_ticket(summary,
  description, component=None)` pure function tool: site, project and issue
  type from configuration, URL-encoded, length-bounded. Instruction: draft
  only when asked; never claim a ticket was created.
- Out: creating tickets through the Jira API, confirmation and duplicate
  protection (G05).
- Depth: no Jira credential, no network call, no write: the human submitting
  in Jira is the approval.

## Acceptance

- [ ] The generated link opens Jira's create screen with fields filled
      (manual local check, or the documented fallback).
- [ ] Model arguments cannot change the Jira host, project or issue type.
- [ ] The agent never says a ticket was created; no Jira secret or write tool
      exists in the project.

Verification: offline `pytest tests/test_jira_draft.py`; one manual link
check by a person.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G04-jira-ticket-draft.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
