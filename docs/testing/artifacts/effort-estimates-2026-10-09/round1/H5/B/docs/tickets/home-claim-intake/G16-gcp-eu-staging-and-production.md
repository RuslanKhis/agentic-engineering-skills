---
goal: G16
title: Staging and production on Cloud Run in the EU
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets, adk-agent-observability, adk-release-engineering]
blocked_by: [G04, G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 36-60
  review_and_verify: 24-40
  total: 60-100
  calendar_waits: Project creation and org policy (1-2 weeks); Guidewire allow-listing of the static egress IP (2-4 weeks)
owner: E4 with the platform team
status: blocked
---

# G16 Staging and production on Cloud Run in the EU

## Outcome

The service runs in staging and production in the EU region with least-privilege identities, secrets, database, bucket, jobs and a rollback path. Implements D2, D13, I9.

## Scope

- In: Terraform for Cloud Run service and jobs, Cloud SQL, GCS, Secret Manager, Cloud NAT static IP, service accounts per identity, resource-location policy, Cloud Scheduler; deployment readback; rollback rehearsal.
- Out: Canary automation (G18).
- Depth: Build with recovery and cleanup.
- Route: Existing Terraform convention; CI deployer identity separate from runtime identity.
- Supporting skills: `adk-tool-auth-and-secrets` (workload identity and secret access); `adk-agent-observability` (first shared environment: telemetry wiring); `adk-release-engineering` (first shared environment: release manifest readback)
- Execution scope: Needs projects, IAM and an explicit apply authorization per environment.

## Acceptance

- [ ] Staging serves `/chat` with the pinned model and a sandbox Guidewire
- [ ] Every resource is in the EU region (policy check passes)
- [ ] Rollback to the previous revision rehearsed and timed
- [ ] Runtime service account cannot read the deployer's secrets

Verification: Authorized live in staging; production apply after review.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G16-gcp-eu-staging-and-production.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
