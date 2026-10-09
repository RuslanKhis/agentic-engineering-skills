---
goal: G08
title: Cloud foundation provisioned
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: GCP project, billing and Vertex AI access
  wait_days: 0-1
owner: Dev C
status: ready
---

# G08 Cloud foundation provisioned

## Outcome

Infrastructure for D6, D7 exists before the gateway is ready. Route and rationale: [plan, G08](../../plans/salon-booking-assistant.md#g08--cloud-foundation-provisioned).

## Scope

- In: Cloud SQL Postgres; runtime service account (Vertex AI user, Cloud SQL client, Secret Manager accessor); booking API credentials in Secret Manager; billing budget alert; dated monthly cost estimate; a placeholder Cloud Run revision
- Out: deploying the gateway (G09)
- Depth: build minimal; floor: no secrets in code, budget alert

## Acceptance

- [ ] Placeholder revision reads one secret version and makes one model call as the runtime service account
- [ ] Budget alert configured; cost estimate written with sources and date
- [ ] No user-managed service-account key file exists

Verification: authorized hosted check in the team's GCP project (needs explicit authorization to provision).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-cloud-foundation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
