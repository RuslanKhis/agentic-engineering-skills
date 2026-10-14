---
goal: G09
title: The assistant runs in staging on Cloud Run with its own identity and no content in logs
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-tool-auth-and-secrets]
blocked_by: [G02, G05]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 2-3
  total: 8-12
  calendar_waits: none
owner: Dev C
status: blocked
---

# G09 The assistant runs in staging on Cloud Run with its own identity and no content in logs

## Outcome

A staging Cloud Run service (gateway + agent) with a dedicated service account, Cloud SQL Postgres for sessions/operations/allowance, Secret Manager, Vertex AI in the chosen region, traces and token cost, a budget alert, and a deploy script later goals reuse. Implements D6, D9. 1 h handoff from Dev B on the agent factory.

## Scope

- In:
  - Dockerfile, deploy script, `DatabaseSessionService` on Cloud SQL, migrations for operations and allowance tables
  - Service account with only Vertex user, Cloud SQL client and secret accessor; booking API credential in Secret Manager
  - OpenTelemetry to Cloud Trace with prompt/response capture off; structured logs without message text
  - Budget alert at 50/90/100 % of the A3 allowance (alerts only); record region, Vertex prices and quotas with dates in the design
  - 30-day session deletion job (Cloud Scheduler + SQL)
- Out: Production and launch (G11); SLO alerts (G13)
- Depth: Build at MVP depth. Floor: no secrets in code, budget alert, pinned model. Deferred: SLO alerts (G13), canary (later).
- Supporting skills, purpose: adk-agent-observability: traces and token counts with content capture off; adk-tool-auth-and-secrets: service account and Secret Manager for the booking API credential

## Acceptance

- [ ] Readback: the serving revision reports its image digest, ADK version, model ID and prompt version
- [ ] A chat turn in staging creates one trace with agent, tool and model spans; a search of logs and traces for the message text finds nothing
- [ ] Restarting the service keeps the conversation (session in Cloud SQL)

Verification: Authorised live check in the staging project only (needs explicit go-ahead for that project); exporter test offline.

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-staging-deploy.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
