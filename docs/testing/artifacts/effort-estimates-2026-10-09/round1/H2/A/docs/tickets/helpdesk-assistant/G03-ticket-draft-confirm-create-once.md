---
goal: G03
title: A confirmed draft becomes exactly one Jira issue
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-agent-security, adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 1.5-2.5
  review_and_verify: 2.5-3.5
  total: 4-6
  calendar_waits: Jira sandbox project or create rights on ITHD (same Atlassian request as G01); live check only
owner: Engineer B
status: ready
---

# G03 A confirmed draft becomes exactly one Jira issue

## Outcome

"Raise a P3 incident for jane.doe" produces a stored draft. When its owner confirms, application code (not the model) creates one `ITHD` issue labelled `hda-<draft_id>` and returns the key. Implements D3, D5 and invariant I4. Every decision is provisional on the assumed answers at the top
of the design. The implementation route is in the plan's G03 section.

## Scope

- In: `tools/tickets.py` (`propose_ticket`), `drafts.py` (DraftStore protocol, Firestore and in-memory implementations, statuses pending/dispatching/created/failed/uncertain), `clients/jira.py`, a `confirm_draft(draft_id, user_id)` service function, offline tests
- Out: HTTP routes and UI (G04), automatic JQL reconciliation and reporter mapping (G07)
- Depth: internal-tool external writes: human confirmation bound to the stored payload, and an at-most-once operation record. Floor: the agent holds no create path; project and issue types come from a code allowlist; Jira token chosen in code, never in model arguments.

## Acceptance

- [ ] Scripted model calls `propose_ticket`: a draft exists and the Jira fake received 0 calls
- [ ] Owner confirms: exactly 1 Jira call; status `created` with the key
- [ ] Repeat confirm and two concurrent confirms: still 1 Jira call in total
- [ ] Another user confirms: not found, 0 Jira calls; expired draft refused
- [ ] Jira 400 gives `failed` with Jira's message; a timeout gives `uncertain`, and the next confirm does not dispatch
- [ ] Disallowed project or issue type refused before any call
- [ ] (live, authorised) one create in the sandbox, closed afterwards

Verification: `pytest tests/test_tickets.py` (offline, in-memory store; one Firestore-emulator test if the team uses one). The live item needs a named sandbox and the user's go-ahead.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G03-ticket-draft-confirm-create-once.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
