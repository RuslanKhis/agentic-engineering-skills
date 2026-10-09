---
goal: G08
title: Deploy to staging and production with traces
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering, adk-memory-architecture]
blocked_by: [G02, G07]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev C
status: blocked
---

# G08 Deploy to staging and production with traces

## Outcome

The assistant runs in staging against booking-API staging, and in production behind a closed flag ready for G11. Traces and token cost are visible. Implements D5, D9 and D10.

## Scope

- In:
  - A `Dockerfile` and Cloud Run services for staging and production.
  - `DatabaseSessionService` and the application tables, migrated by Alembic.
  - OpenTelemetry to Cloud Trace with prompt and response content capture **off**, and token usage per invocation in structured logs.
  - A release manifest logged at startup: image digest, `google-adk` version, model ID and prompt version.
  - `ENABLED_SALONS` empty in production.
- Out: Canary (G17) and SLO alerts (G16).
- Depth: MVP: the chosen host with rollback by keeping the previous revision. Observability is Build at the level of traces and token cost.
- Implementation route: Confirm `DatabaseSessionService` and the telemetry content-capture gate on the pin. Run the service as the G07 service account.
- Prerequisites: G02 (an application to deploy) and G07. G03 and G05 must be merged before production traffic, which G11 requires.
- Supporting skills: Adk-agent-observability: traces, the content gate and token cost; adk-release-engineering: the pinned manifest and rollback unit; adk-memory-architecture: the session store and its retention.
- Execution scope: Requires the team's explicit go-ahead per environment.

## Acceptance

- [ ] After a redeploy, a staging conversation resumes from Cloud SQL.
- [ ] A trace shows agent, tool and model spans carrying the session ID, with no prompt text.
- [ ] The release manifest can be read from the logs.
- [ ] Rolling back to the previous revision works and is recorded.
- [ ] Production refuses chat while `ENABLED_SALONS` is empty.

Verification: Authorised deployment to staging, then production, with commands and revision IDs recorded.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-deploy-to-staging-and-production-with-traces.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
