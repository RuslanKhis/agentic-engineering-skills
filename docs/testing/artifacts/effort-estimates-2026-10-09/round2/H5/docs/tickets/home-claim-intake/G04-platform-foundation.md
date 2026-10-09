---
goal: G04
title: Three EU environments exist and the skeleton is deployed to dev
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-release-engineering, adk-agent-observability]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 28–44
  review_and_verify: 12–20
  total: 40–64
  calendar_waits: Project creation and org-policy exceptions by the cloud platform team, 1–2 weeks
owner: E3
status: ready
---

# G04 Three EU environments exist and the skeleton is deployed to dev

## Outcome

dev/staging/prod projects in the EU with Cloud Run, Cloud SQL (private IP), the photos bucket, Secret Manager, Artifact Registry and service accounts, defined in Terraform; the G03 skeleton runs in dev. D4, D6, D7, I7.

## Scope

- In: Terraform modules under `infra/`; `sa-intake-run` and `sa-deployer` with least privilege; CI pipeline building and deploying to dev; residency policy test (all resources in EU locations); `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` set.
- Out: Staging/prod deploy of the app (G14/G20); alerts (G13).
- Depth: Production foundation. Floor: no keys, workload identity, budgets alerts on each project.
- Route: Cloud Run service `claim-intake-api`, Cloud SQL Postgres, GCS regional bucket, Secret Manager; deploy readback of revision and env.
- Supporting skills: `adk-release-engineering` (image digest and manifest stub from the first build); `adk-agent-observability` (telemetry content capture off from the first deploy)
- Execution scope: Creating resources in the three named projects is authorised once the platform team hands them over; no other projects.

## Acceptance

- [ ] `terraform plan` for each env shows only EU locations; policy test fails on a non-EU location
- [ ] Dev revision serves the skeleton; readback shows image digest, service account and content-capture off
- [ ] No service-account key exists in any project (check)

Verification: Authorised dev deploy; policy test offline in CI.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-platform-foundation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
