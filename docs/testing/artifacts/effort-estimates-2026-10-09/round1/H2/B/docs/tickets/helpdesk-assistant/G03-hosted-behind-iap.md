---
goal: G03
title: Helpdesk colleagues sign in and use the assistant; nobody else can
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets, adk-frontend-integration, adk-agent-observability, adk-release-engineering]
blocked_by: [G02, authorised GCP project and region]
phase: 1
profile: internal tool
estimate: 5-7 h
status: blocked
---

# G03 Helpdesk colleagues sign in and use the assistant; nobody else can

## Outcome

A member of the helpdesk Workspace group opens the page and gets G02's
answers under their own identity; others are refused. Implements D6, D7 and
invariants I1, I6.

## Scope

- In: `app.py` (IAP JWT verification middleware, `/chat`, per-user daily turn
  counter, session ownership by verified email), `static/index.html` with
  completed-JSON replies, Dockerfile, one Cloud Run service (max 1 instance)
  behind IAP, Secret Manager for the Confluence token, Cloud Billing budget
  alert, structured logs, revision labels with image digest, ADK pin, model ID
  and prompt hash.
- Out: tickets (G04), persistent sessions (G09), streaming and SLOs (later).
- Depth: internal tool. Floor: least-privilege service identity, secrets only
  in Secret Manager, no prompt or runbook content in logs, previous revision
  kept for rollback.

## Acceptance

- [ ] Missing or forged IAP assertion → 401 before any model call.
- [ ] User B requesting user A's session → 403.
- [ ] 41st turn in a day for one user → limit message, no model call.
- [ ] Hosted: a group member completes the VPN journey with cited pages.
- [ ] Hosted: a non-member is blocked by IAP.
- [ ] Logs show session, invocation IDs and token counts, and no runbook text.
- [ ] Previous revision retained and the rollback command recorded.

Verification: `pytest` offline for the middleware and counters; the hosted
checks run once in the authorised project. Deployment, IAM and IAP changes
need explicit approval for that named project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G03-hosted-behind-iap.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
