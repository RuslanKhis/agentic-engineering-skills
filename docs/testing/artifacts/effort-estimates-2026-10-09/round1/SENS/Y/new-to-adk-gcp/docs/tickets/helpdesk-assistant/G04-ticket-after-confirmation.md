---
goal: G04
title: Ticket created only after confirmation
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails, adk-tool-interface-design, adk-agent-security]
blocked_by: [G02]
phase: 1
profile: internal tool
estimate:
  hands_on: 1-3
  review_and_verify: 3-4
  total: 4-7
  calendar_waits: the Jira admin decides between the real ITHD project and a sandbox (O4); blocks only the live check
owner: Engineer B
status: ready
---

# G04 Ticket created only after confirmation

## Outcome

"Raise a ticket for network" shows the exact draft. Only the analyst's
confirmation creates the Jira issue, and the reply gives its key. Implements
D3, and invariants I2 and I3.

## Scope

- In:
  - `jira.py`: a single POST with no automatic retry.
  - `draft_jira_ticket`: allow-listed fields, a canonical draft stored in
    session state with `draft_id`, a hash and an `op_id`.
  - `create_jira_ticket(draft_id)`, wrapped with ADK tool confirmation (check
    it at 2.8.0 with `adk web` and the in-memory session; O6).
  - The draft states `proposed → submitted → created / failed / uncertain`.
  - The `hda-<op_id>` label and the "Requested by" line.
  - Tests.
- Out: reporter attribution (G10), adversarial suite (G09),
  retry/reconciliation.
- Depth: internal-tool write control. Confirmation is in code, there is one
  project, and an uncertain outcome is shown to the analyst. If ADK
  confirmation does not work in `adk web` at the pin, the create tool stays
  disabled there and the confirm action moves to G06.

## Acceptance

- [ ] Draft, then confirm, gives one fake Jira POST and the issue key in the
  reply. One live confirmed ticket is created in the agreed project.
- [ ] A timeout gives the status `uncertain` and exactly one POST; a second
  confirm is refused. A 400 response gives `failed` with the field error.
- [ ] No confirmation, or an altered draft, gives 0 POSTs. The reply never
  claims a ticket without a key.

Verification: offline `pytest tests/test_ticket_flow.py`, plus one authorised
live create after O4.

## Evidence

<!-- Filled in by the agent that carries this ticket out. -->

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G04-ticket-after-confirmation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
