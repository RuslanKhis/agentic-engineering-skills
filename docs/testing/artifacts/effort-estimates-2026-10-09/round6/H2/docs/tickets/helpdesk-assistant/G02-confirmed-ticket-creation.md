---
goal: G02
title: Asking for a ticket shows a preview; only Create makes it
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-agent-security, adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  calendar_waits: none
owner: Dev B
status: ready
---

# G02 Asking for a ticket shows a preview; only Create makes it

## Outcome

`propose_ticket` stores a validated proposal; only the same user's confirm call creates one Jira issue. Implements D4, D5; guarantees I2 (proposals), I3, I4. First step: request W1 (bot accounts, Jira sandbox).

## Scope

- In: `app/tools/tickets.py`, in-process proposal registry (owner, 30-min TTL, one-shot state), `POST /api/proposals/{id}/confirm`, Jira client interface plus fake.
- Out: durable records and reconciliation (G07), reporter mapping (G08), live sandbox call (G05). Final fields wait on A8.
- Depth: confirmation for writes; floor: no create without a human; no automatic retry of a create.

## Acceptance

- [ ] Confirm creates exactly one fake issue with fixed project, labels `helpdesk-assistant` and `op-<id>`, and the verified-email footer; a second confirm returns the same key
- [ ] Jira timeout → state `uncertain` with the label hint; expired proposal → "expired"
- [ ] Another user's proposal → 404; scripted model fed an injected runbook makes proposals only and the fake Jira records 0 creates

Verification: offline `pytest tests/test_tickets.py tests/test_confirm_endpoint.py`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G02-confirmed-ticket-creation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
