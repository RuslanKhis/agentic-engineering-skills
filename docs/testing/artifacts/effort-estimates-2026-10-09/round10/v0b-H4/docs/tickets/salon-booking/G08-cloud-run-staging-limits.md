---
goal: G08
title: The assistant runs in staging on Cloud Run with spend limits, a kill switch and clean logs
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-operational-guardrails, adk-agent-observability, adk-release-engineering]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 2-3
  total: 8-12
  calendar_waits: none
owner: Dev A
status: blocked
---

# G08 The assistant runs in staging on Cloud Run with spend limits, a kill switch and clean logs

## Outcome

A walking skeleton in staging early, so G10 only releases the finished
service. Implements D5, D8 and the logging half of D9; holds I5 and I6.

## Scope

- In: Dockerfile for the FastAPI service; Cloud Run staging service with its own
  service account (Vertex AI user, Cloud SQL client, Secret Manager accessor
  only); Cloud SQL Postgres for sessions, operations and allowances; secrets in
  Secret Manager; per-customer 40 turns/day allowance and `ASSISTANT_ENABLED`
  per salon checked before any model call; Cloud Billing budget alert
  (USD 150/270/300, alerts only); structured logs with session ID, tool name,
  operation status and token counts, ADK content capture off; 30-day session
  deletion job; release manifest (image digest, prompt version, model ID,
  tool-schema hash, eval-set hash, secret versions).
- Out: production release and pilot flag (G10), traces and alerts (G12).
- Depth: MVP; observability Minimal by plan cut. Floor: spend stop, no secrets in image or logs.
- Execution scope: needs the GCP project and permission to create these
  resources; record each resource for cleanup.

## Acceptance

- [ ] 41st turn of the day for one customer → refusal, no model call (offline test)
- [ ] Kill switch off for a salon → fallback message, no model call
- [ ] A full staging conversation leaves no message text, phone or email pattern in Cloud Logging (query recorded)
- [ ] Session and a pending proposal survive a new revision deploy
- [ ] Deletion job removes a session dated 31 days ago and keeps one dated 29 days ago (fixture)
- [ ] Release manifest has no model alias

Verification: offline tests; authorised staging deployment readback (`gcloud run services describe`) recorded in Evidence.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G08-cloud-run-staging-limits.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
