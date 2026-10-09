---
goal: G08
title: Staging and prod on Cloud Run with logs, cost and rollback
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-release-engineering, adk-agent-observability]
blocked_by: [G04, G05, GCP project and region named with deploy authorization]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 4–7
  review_and_verify: 2–3.5
  total: 6–10.5
  calendar_waits: budget alert may need the billing admin (hours to a day)
owner: Dev A
status: blocked
---

# G08 Staging and prod on Cloud Run with logs, cost and rollback

## Outcome

the assistant runs in staging and prod, the team can see errors, token use and write outcomes per session, and can roll back in minutes. D7, D9.

## Scope

- In: Dockerfile, Cloud Run service per environment with its own service account (Vertex AI user, Cloud SQL client, secret accessor for the booking-API credential only); Cloud SQL database; `release.json` (image digest, prompt version, model ID, tool-schema hash, eval-set hash, secret versions); structured JSON logs with session/invocation/proposal IDs, token counts and write outcomes, no message text; billing budget alert at 50/90/100% of A3; rollback rehearsal to the previous revision. Out: traces and SLOs (G11), CI gate (G10).
- Route: Cloud Run, Artifact Registry, Secret Manager, Cloud SQL connector.
- Prerequisites: G04, G05; the team names the GCP project and region and authorizes deploys.
- Depth: MVP; minimal observability per the design table. Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: `adk-release-engineering` (release manifest, rollback unit); `adk-agent-observability` (log fields, token accounting, content capture off)

## Acceptance

- [ ] staging readback shows the expected image digest and model ID
- [ ] a test conversation's log lines carry IDs and token counts but no message text
- [ ] traffic switched to the previous revision and back
- [ ] the service account cannot read other secrets

Verification: authorized hosted checks in staging; prod deploy only after G09's staging pass. Execution scope: needs explicit authorization for the named project; nothing deployed by design work.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-cloud-run-staging-prod.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
