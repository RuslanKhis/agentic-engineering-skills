---
goal: G16
title: Staging and production environments exist in the EU with least privilege
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets, adk-release-engineering, adk-agent-observability]
blocked_by: [G02, W13]
phase: 1
profile: production
estimate:
  hands_on: 30-44
  review_and_verify: 9-13
  total: 39-57
  calendar_waits: none
owner: Eng C
status: proposed
---

# G16 Staging and production environments exist in the EU with least privilege

## Outcome

Terraform for staging and production projects in `europe-west3`: Cloud Run
service, Cloud SQL PostgreSQL (HA in production), buckets, Cloud Tasks,
Secret Manager, service accounts and egress. Implements D2 and D4 hosting.
Handoff: 1 h from Eng A on the skeleton's entrypoint.

## Scope

- In: `infra/` modules and environments; separate deployer and runtime
  identities; Cloud NAT static egress IP for the Guidewire allowlist; first
  staging deploy of the skeleton with readback of revision, region and
  settings.
- Out: telemetry dashboards (G17); CI and canary (G19); production traffic
  (G22). Applying Terraform needs the platform team's project and an
  explicit authorisation for each environment.
- Depth: production.

## Acceptance

- [ ] A1 Staging and production resources exist in EU locations, Cloud SQL highly available in both; Cloud Run, Cloud SQL and Cloud Tasks availability in `europe-west3` is confirmed and a readback lists region, revision and settings.
- [ ] A2 The runtime service account can reach only its own buckets, database, queue and secrets; a denied access test passes; the deployer cannot act as runtime.
- [ ] A3 The production network, including the reserved static egress IP, is applied in this goal, so the allowlist requests W7 and W15 can be sent.
- [ ] A4 A Cloud SQL backup is restored to a point in time in staging and the service reads from it.
- [ ] A5 Removing one runtime role at a time (Vertex AI, Model Armor, Cloud Tasks, Cloud SQL) in staging gives an alert and the designed failure (not ready, or `degraded`), not a crash loop.
- [ ] A6 With Secret Manager unavailable at start-up the instance does not become ready; running instances keep their cached secret.

Verification: authorised staging apply and readback; production network
(A3) applied here; the rest of production is plan-only until G22. Secret
rotation moved to G37.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G16-infrastructure.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
