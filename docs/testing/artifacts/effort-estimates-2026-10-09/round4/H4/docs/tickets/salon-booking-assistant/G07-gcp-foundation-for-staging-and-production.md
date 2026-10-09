---
goal: G07
title: GCP foundation for staging and production
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev B
status: ready
---

# G07 GCP foundation for staging and production

## Outcome

Staging and production have what the application needs before it exists. Implements D5, D7 and D10.

## Scope

- In:
  - A dedicated runtime service account per environment with Vertex AI User, Cloud SQL Client and Secret Accessor on named secrets only.
  - One Cloud SQL Postgres instance at the smallest tier, with a database per environment.
  - Secret Manager entries, empty or placeholder, for the booking API key, the token verification key and the DB URL.
  - An Artifact Registry repository.
  - A project budget with alerts at 50, 90 and 100 % of the assumed allowance (A4).
  - Scripts in `deploy/foundation.sh`, or Terraform if the team already uses it.
- Out: Deploying the application (G08).
- Depth: MVP: least-privilege workload identity and no keys in code. A budget alert is an observation, not a cap; G09 owns enforcement.
- Implementation route: `gcloud` scripts committed to the repository, run by a person with the team's go-ahead. Region per A10.
- Prerequisites: The team's go-ahead to create resources in the existing project. This design does not authorise it.
- Supporting skills: Adk-tool-auth-and-secrets, for secret layout and service-account grants.
- Execution scope: Requires the team's explicit go-ahead.

## Acceptance

- [ ] The service account can read only its listed secrets; reading any other fails.
- [ ] A database connection from Cloud Shell succeeds using the service account.
- [ ] The budget and its alert recipients exist.
- [ ] No secret value appears in the repository.

Verification: Authorised, recorded commands against the team's project, with resource names in the evidence and not in shared documents.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-gcp-foundation-for-staging-and-production.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
