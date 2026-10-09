---
goal: G10
title: Deploy to staging, soft launch
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G03, G05, G06, G07, G08, G09]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 4-6
  total: 8-12
  calendar_waits: privacy-notice update and salon-owner sign-off (start day 1); Vertex quota check if needed
owner: Dev C (Dev A for the booking-API credential)
status: blocked
---

# G10 Deploy to staging, soft launch

## Outcome

The assistant runs on Cloud Run in staging, then serves signed-in customers in production behind the widget flag. D7, D9.

## Scope

- In: Dockerfile, service account and grants, Secret Manager references, Cloud SQL connection, `release/manifest.yaml` (image digest, prompt version, model ID, tool-schema hash, eval-set hash), budget alert, log-based alert on `uncertain`/`partial` operations, rollback runbook, measured cost per conversation.
- Out: Canary (later), SLO alerts (G14). Cut line: if phase 1 runs high, this goal ends at staging plus staff accounts and the public flag moves to phase 2.
- Depth: Build at MVP depth: one service, previous revision kept for rollback.

## Acceptance

- [ ] Staging smoke test completes Maya's move against the staging booking API
- [ ] Unauthenticated request rejected; rollback to the previous revision rehearsed
- [ ] Production flag stays off until sign-off is recorded and the G09 run is attached

Verification: Authorised hosted checks in staging, then a production smoke test on a test customer; needs a named project, region and explicit go-ahead.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-deploy-soft-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
