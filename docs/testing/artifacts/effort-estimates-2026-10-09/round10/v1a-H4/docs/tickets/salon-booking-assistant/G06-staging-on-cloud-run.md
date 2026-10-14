---
goal: G06
title: The assistant runs on a staging Cloud Run service with its own identity, secrets and content-free telemetry
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering, adk-memory-architecture]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 1.5-3
  total: 7.5-12
  calendar_waits: none
owner: Dev C
status: ready
---

# G06 The assistant runs on a staging Cloud Run service with its own identity, secrets and content-free telemetry

## Outcome

A staging Cloud Run service serves a stub ADK app, later replaced by the real
one. It runs with a dedicated service account, Vertex AI access, booking API
credentials from Secret Manager, the `assistant` Postgres schema
(`DatabaseSessionService` tables plus migrations) and Cloud Trace. Content
capture is off. Each deploy writes `release.json` (D5, D6, D10, I7). Starts on
day 1 with the assumed google-adk 2.8.0 pin. If G01 picks another pin, the
image is rebuilt.

## Scope

- In: Dockerfile, deploy script, service account and least-privilege grants,
  secrets, schema migration, OpenTelemetry export with prompt and response
  capture disabled, a billing budget alert (an alert, not a cap), and
  `release.json` (image digest, prompt version, model ID, tool schema hash).
- Out: production (G09); SLOs and alerts (G13).
- Depth: MVP; the floor is no secrets in the image or env files, and a pinned
  model.

## Acceptance

- [ ] A deploy readback shows the serving revision, its service account and `release.json` matching the source.
- [ ] After one test conversation, Cloud Trace shows agent, tool and model spans with the session ID and no message text. Logs hold IDs only.
- [ ] Forbidden: no secret value appears in the image layers, env listing or logs.
- [ ] A restarted revision resumes an existing session from Postgres.

Verification: authorised staging deploy, then a manual readback and trace
inspection. The commands are recorded in Evidence.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-staging-on-cloud-run.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
