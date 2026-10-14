---
goal: G03
title: The team has EU-only dev, staging and prod environments it can deploy to
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [W3, G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 24-36
  review_and_verify: 6-10
  total: 30-46
  calendar_waits: none on this goal; waits on W3 before it
owner: Eng D
status: blocked
---

# G03 The team has EU-only dev, staging and prod environments it can deploy to

## Outcome

Three projects in the landing zone with resources pinned to one EU region
(D6), the service accounts of the design's identity paragraph, Secret
Manager, Cloud SQL Postgres, two GCS buckets with lifecycle rules, an
Artifact Registry and a first Cloud Run deployment of the skeleton.

## Scope

- In: infrastructure as code in the landing zone's convention; org policy
  restricting resource locations to the EU (I6); `sa-intake`, `sa-reconciler`,
  deployer and CI identities with least privilege; Guidewire client secret
  slot (no value); Cloud SQL with IAM authentication and backups; buckets
  `photos-quarantine` and `photos-clean`; Cloud Run service deploying the
  G02 image to dev; the CI system choice recorded.
- Out: observability sinks (G16), release gates (G17), prod traffic.
- Depth: production; the region follows O1's answer.

## Acceptance

- [ ] Readback shows every resource in the chosen EU region and the location org policy active.
- [ ] The skeleton answers a turn on dev Cloud Run using `sa-intake` and a regional Vertex endpoint.
- [ ] Creating a resource outside the EU in the dev project is refused.
- [ ] No service-account keys exist; secrets are readable only by their two service accounts.

Verification: authorised deployment to the dev project with readback
commands recorded; no staging or prod traffic.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-gcp-eu-foundation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
