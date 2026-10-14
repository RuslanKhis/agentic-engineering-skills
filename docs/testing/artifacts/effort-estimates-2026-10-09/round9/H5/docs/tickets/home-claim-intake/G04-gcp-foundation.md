---
goal: G04
title: Dev and staging GCP foundation in the EU
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [W5]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 20-34
  review_and_verify: 6-10
  total: 26-44
  calendar_waits: W5
owner: Platform
status: blocked
---

# G04 Dev and staging GCP foundation in the EU

## Outcome

Provides the EU environments that G07, G10, G18 and others deploy into (D7).

## Scope

- In: Terraform (`infra/`, proposed) for the dev and staging projects: Cloud Run services `intake-api` and `submit-worker` with separate service accounts, Cloud SQL Postgres, an EU GCS bucket with uniform access, Cloud Tasks queue, Secret Manager entries (empty), Artifact Registry, egress to the company API gateway, budget alerts.
- Out: Production (G24). Observability wiring (G16).
- Depth: Least privilege per service account. The intake SA cannot read the Guidewire secret. Location restricted to the EU.

Supporting skills and why:
- adk-tool-auth-and-secrets (service accounts, Secret Manager)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] `terraform plan` for dev and staging shows only EU locations, and two service accounts with disjoint secret access.
- [ ] A hello-world revision of `intake-api` is served in staging and reaches Cloud SQL using its service account, with no keys.
- [ ] Attempting to read the Guidewire secret as `intake-api` SA is denied (recorded command and result).

Verification: Authorised live: staging only, after W5 grants the projects. Name the project IDs when running.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-gcp-foundation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
