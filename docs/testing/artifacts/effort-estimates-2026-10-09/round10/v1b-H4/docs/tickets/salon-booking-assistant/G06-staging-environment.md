---
goal: G06
title: Staging environment on GCP
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev C
status: ready
---

# G06 Staging environment on GCP

## Outcome

A staging Cloud Run service with its own database, identity, secrets, limits
and alerts exists, so the launch goal only deploys and checks. Implements D6,
the platform part of D8 and D9, and the minimal release bundle.

## Scope

- In: GCP project for the assistant (region near the salons, recorded with the
  reason); Cloud SQL Postgres (smallest tier; price and date recorded);
  service account with Vertex AI user, Cloud SQL client and secret accessor
  only; booking API staging key in Secret Manager; Cloud Run service
  (`max-instances=3`, min 0) deploying a hello-world FastAPI image to prove
  the path; billing budget alert at the A2 figure (notification only, noted as
  such); Cloud Scheduler job deleting sessions and operations older than 30
  days; log-based alerts on `operation.uncertain` and tool error rate to the
  team channel; `release.json` (revision, git SHA, model ID, secret version)
  written at deploy. Scripts or Terraform in `infra/`, no credentials committed.
- Out: production project or traffic (G09); traces (G15).
- Depth: MVP. Floor: no secrets in repo; spend alert; least privilege.
- Execution scope: needs the team's GCP billing account and an explicit go-ahead
  to create resources; this ticket alone does not authorise production.

## Acceptance

- [ ] Hello-world revision serves on staging; service account has exactly the
      three roles above (IAM readback recorded).
- [ ] A backdated test session is removed by one scheduler run.
- [ ] A synthetic `operation.uncertain` log line triggers the alert.
- [ ] Budget alert exists with the agreed amount; `release.json` is readable
      from the running revision.

Verification: authorised live on the staging project only; commands and
readbacks recorded in Evidence.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-staging-environment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
