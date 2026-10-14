---
goal: G03
title: Provision EU dev and staging environments with a deploy pipeline
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [W4, G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 32-50
  review_and_verify: 8-14
  total: 40-64
  calendar_waits: see W4
owner: Eng E
status: blocked
---

# G03 Provision EU dev and staging environments with a deploy pipeline

## Outcome

Dev and staging projects in the EU with the service accounts, Cloud SQL, buckets, Cloud Tasks queue, Secret Manager entries and two Cloud Run services from D2, deployed from CI with the G02 skeleton. Implements D2, D4 infrastructure.

## Scope

- In: infrastructure as code, `api-sa` and `worker-sa` with least privilege, resource-location policy check, CI deploy to staging with revision labels.
- Out: production (G21), telemetry (G19).
- Depth: build; only `worker-sa` can read the Guidewire secret.

## Acceptance

- [ ] A CI run deploys the skeleton to staging and a readback shows region, revision, image digest and service account
- [ ] `api-sa` cannot read the Guidewire secret (denied access test)
- [ ] Creating a resource outside the EU is refused by policy

Verification: Authorised hosted check in staging after W4; IaC plan reviewed by Eng A.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G03-eu-environments.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
