---
goal: G03
title: Have EU projects, identities and network ready for the service
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 9-15
  review_and_verify: 3-5
  total: 12-20
  calendar_waits: IAM grants and VPC egress to Guidewire from the platform team
  wait_days: 5-10
owner: Dev D
status: ready
---

# G03 Have EU projects, identities and network ready for the service

## Outcome

Dev, staging and production projects in `europe-west4` with service accounts, Cloud SQL, a photo bucket, Secret Manager and egress to Guidewire, through the existing Terraform. Implements D6, I6; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Terraform modules, least-privilege service accounts, Cloud SQL (HA in production), GCS bucket with uniform access and no public access, Secret Manager entries (empty), egress rule to the Guidewire host.
- Out: Application deployment (G18).
- Depth: Production; floor: no Owner/Editor roles, no secrets in Terraform state outputs.

## Acceptance

- [ ] Staging resources exist in `europe-west4`, read back from the API.
- [ ] Service account holds only Vertex user, Cloud SQL client, bucket object admin on one bucket and secret accessor on named secrets.
- [ ] The bucket rejects public access; egress reaches only the Guidewire sandbox host.

Verification: Terraform plan review, then authorised apply in staging; production apply waits for G27.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-gcp-eu-landing-zone.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
