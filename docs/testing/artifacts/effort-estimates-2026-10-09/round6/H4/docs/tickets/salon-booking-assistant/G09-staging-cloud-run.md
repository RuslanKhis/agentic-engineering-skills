---
goal: G09
title: The assistant runs on staging with persistent state and a rollback
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 4-7
  review_and_verify: 1-2
  total: 5-9
  calendar_waits: none
owner: Dev C
status: ready
---

# G09 The assistant runs on staging with persistent state and a rollback

## Outcome

Cloud Run with Cloud SQL, a service account and secrets in the booking API's region (D6). Implements I6.

## Scope

- In: New GCP project (A12); Cloud SQL Postgres; Secret Manager; Vertex AI access for the service account
- In: Structured logs with IDs, status and token counts, and content capture off; billing budget alert
- In: Deploy the current build; record image, prompt hash and model ID; rehearse traffic back to the previous revision
- Out: Out: SLO alerts (G12), CI gate (G11)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] A staging turn survives an instance restart (session reloads)
- [ ] A captured log and span carry no message text
- [ ] Rollback to the previous revision completes in under 5 min

Verification: authorised staging deployment; the user approves creating the project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-staging-cloud-run.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
