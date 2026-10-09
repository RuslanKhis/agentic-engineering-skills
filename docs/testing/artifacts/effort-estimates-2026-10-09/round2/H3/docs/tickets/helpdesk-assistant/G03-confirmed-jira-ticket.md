---
goal: G03
title: Create a Jira ticket after explicit confirmation
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-agent-security]
blocked_by: [G02]
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 1.5-3
  review_and_verify: 1.5-3   # write boundary: careful read and adversarial checks, by Engineer B
  total: 3-6
  calendar_waits: Jira bot create permission on sandbox project ITSDTEST and on ITSD (requested in G01)
owner: Engineer A
status: blocked
---

# G03 Create a Jira ticket after explicit confirmation

## Outcome

"Open an incident for the network team" shows the user the exact draft.
Approve returns the new ticket key and link; Reject creates nothing.
Implements D3, invariants I3–I5 and the design's security posture.

## Scope

- In: `create_ticket(issue_type: enum, summary ≤200, description ≤4000,
  priority: enum, runbook_urls ≤3)` wrapped in
  `FunctionTool(..., require_confirmation=True)`. Code supplies the project
  from config, the footer "Requested by <verified email> via helpdesk
  assistant" (email from session state set by trusted code, never a model
  argument), and labels `helpdesk-assistant` and `asst-op-<id>` (from
  `function_call_id`). Validation runs before confirmation is requested and
  again before dispatch. No retry of the POST. On a timeout or 5xx after send:
  one label search, then "created as KEY" or "uncertain: check JQL
  `labels = asst-op-<id>`". Plus a ≤30-minute documentation check on whether
  Jira Cloud create supports an idempotency key, with the answer recorded.
- Out: assignee and components; per-user reporter (G08); durable operation
  record (G12).
- Depth: confirmation for writes; reconciliation by label, not deduplication.
  Floor: no ticket without confirmation of the exact payload; live writes only
  to `ITSDTEST`.

## Acceptance

- [ ] Offline, fake Jira: Approve → exactly 1 POST, to the configured project, with both labels and the footer.
- [ ] Offline: Reject → 0 POSTs; no confirmation → 0 POSTs; project `HR` or a 10 kB summary → refused before confirmation, 0 POSTs.
- [ ] Offline adversarial: (a) page text instructing the agent to create a ticket → 0 POSTs without confirmation; (b) the model proposes another project → refused; (c) a confirmation for payload X replayed with payload Y → refused, 0 POSTs.
- [ ] Offline: a fake that commits and then times out → user sees "found KEY" or "uncertain", and there is no second POST.
- [ ] Live: one confirmed ticket in `ITSDTEST` with labels and footer, then closed by hand.

Verification: `pytest -q tests/test_jira*.py` offline; one authorised live
create in `ITSDTEST` only.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G03-confirmed-jira-ticket.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
