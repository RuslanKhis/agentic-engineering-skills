---
goal: G05
title: Helpdesk staff open the assistant in their browser, signed in with Google
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets, adk-agent-observability, adk-release-engineering]
blocked_by: [G01, G04, W1]
phase: 1
profile: internal tool
estimate:
  hands_on: 2-3
  review_and_verify: 1-1
  total: 3-4
  calendar_waits: W1 access requests, 3-5 working days, requested in G01
owner: Dev B
status: blocked
---

# G05 Helpdesk staff open the assistant in their browser, signed in with Google

## Outcome

The G01 agent inside the G04 app runs on Cloud Run with direct IAP for the
helpdesk group, bot token in Secret Manager, content-free logs (D3, D4, D7, D10, D11; I1, I8).
Includes 0.5 h handoff from Dev A.

## Scope

- In: dedicated service account, Secret Manager secret, max instances 1, OTel content capture off, release manifest with pins.
- Out: alerts, traces, durable sessions (Later).
- Depth: needs explicit authorization for the named project and IAP change; A5 answered before go-live.

## Acceptance

- [ ] A group member gets a cited answer in the browser.
- [ ] A non-member account is denied by IAP; a direct request without IAP fails.
- [ ] Bot token cannot read a non-runbook space; logs of a full turn contain no question or answer text.
- [ ] After a redeploy the user gets a fresh session and no error.

Verification: authorised live checks in the team's existing project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G05-deploy-behind-iap.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
