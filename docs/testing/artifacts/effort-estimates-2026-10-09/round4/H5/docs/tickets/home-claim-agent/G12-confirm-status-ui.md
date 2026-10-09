---
goal: G12
title: Customers confirm the exact summary and see the true filing status
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G04, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 20-34
  review_and_verify: 6-10
  total: 26-44
  calendar_waits: none
  wait_days: 0
owner: Eng D
status: proposed
---

# G12 Customers confirm the exact summary and see the true filing status

## Outcome

Implements D12, I4 and I9 in the browser: confirmation card with hash, status from the operation record, form fallback.

## Scope

- In: Confirmation card, status view polling G09's endpoint, 409 handling, kill-switch fallback to the standard form.
- Out: Chat UI (G11).
- Depth: Production depth. Floor: 'Filed' only from the status endpoint.

## Acceptance

- [ ] 'Filed: CLM-…' appears only after the status endpoint reports `filed`
- [ ] A late execution error after HTTP 200 shows an error, not success
- [ ] A 409 shows the new summary for re-confirmation
- [ ] With the kill switch on, the form link appears

Verification: Local browser tests against the gateway and a fake worker.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G12-confirm-status-ui.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
