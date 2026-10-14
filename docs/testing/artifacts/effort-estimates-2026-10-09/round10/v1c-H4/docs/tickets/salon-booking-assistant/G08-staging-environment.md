---
goal: G08
title: The assistant runs on staging with its own identity, database and limits
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering, protect-adk-sensitive-data]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 2-3
  total: 8-12
  calendar_waits: none
owner: Dev B
status: proposed
---

# G08 The assistant runs on staging with its own identity, database and limits

## Outcome

A staging Cloud Run service in `australia-southeast1` serves the G01
skeleton (and later builds) with Cloud SQL, Secret Manager, a dedicated
service account, traces and token counts without message content, and a
project budget alert (D7, D8, D9). Includes 1 h handoff from Dev A.

## Scope

- In: GCP project or folder, service account with Vertex AI user, Cloud SQL
  client and one secret accessor; Cloud SQL Postgres smallest tier; image
  build and deploy script; OpenTelemetry with content capture off;
  structured logs of operation status changes only; budget alert at 50/90/100
  %; release note per deploy (image digest, prompt hash, model ID, ADK
  version); current Vertex pricing and model location checked and recorded.
- Out: production switch-on (G09), SLOs and alerts (phase 2).
- Depth: build at MVP depth; previous revision kept for rollback.

## Acceptance

- [ ] Deploy, create a session, deploy a new revision: the session and an
      operation row survive.
- [ ] A sample of 20 log entries and traces contains no message text, names,
      phone numbers or emails.
- [ ] Rollback to the previous revision works and is written in the runbook.
- [ ] Budget alert exists; service account has no broader role than listed.

Verification: authorised live checks on the team's staging project only;
not run in this session (no cloud access).

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-staging-environment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
