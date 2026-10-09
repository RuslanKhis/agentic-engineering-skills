---
goal: G04
title: An engineer asks for a ticket, checks the draft and gets exactly one Jira issue
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-agent-security, adk-tool-interface-design, adk-tool-auth-and-secrets]
blocked_by: [G01, G02]
phase: 1
profile: internal tool
estimate: 6-9 h
status: blocked
---

# G04 An engineer asks for a ticket, checks the draft and gets exactly one Jira issue

## Outcome

"Open a ticket for networking" shows a draft card with summary, description,
component, priority and runbook links; pressing Create returns one Jira key.
Implements D3, D4 and invariants I4, I5.

## Scope

- In: `tools/proposals.py` (`propose_ticket`: enum-validated fields, stored
  with payload hash and owner = verified email, returns `proposal_id`; never
  calls Jira), `store.py` (Firestore proposals and operations),
  `jira_client.py` (create with label `hda-op-<id>`, search by label),
  `POST /proposals/{id}/confirm`, the draft card in the page, three
  adversarial cases.
- Out: per-user Jira OAuth (G07), comments or transitions, wider adversarial
  suite (later).
- Depth: internal tool. Floor: no Jira issue without the click on the exact
  stored draft; create token only in Secret Manager. Fallback if this runs
  over estimate: a prefilled Jira create link the engineer submits in Jira,
  no create token; API creation then moves to phase 2.

## Acceptance

- [ ] Two confirms of one proposal → one fake-Jira create; both return the
      same key.
- [ ] Fake Jira commits then times out → label search finds the issue, state
      `created`, no second create.
- [ ] Label search finds nothing after a timeout → state `uncertain`, user told
      to check Jira, no automatic retry.
- [ ] User B confirming user A's proposal → 403, no Jira call.
- [ ] Changed payload with an old proposal ID → 409.
- [ ] Injected page text ("create a P1 ticket", "send this to…", "ignore
      previous instructions") → zero Jira calls in all three cases.
- [ ] Jira 400 → state `failed`, draft kept, error shown.

Verification: `pytest` offline with fake Jira and Firestore; one authorised
live create in a sandbox project or with a test label, then removed by the
Jira admin.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G04-confirmed-jira-ticket.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
