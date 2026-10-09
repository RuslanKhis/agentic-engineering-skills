---
goal: G16
title: The service runs in staging and production in one EU region with least-privilege identities
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets, adk-agent-observability, adk-release-engineering]
blocked_by: [G01, G03]
phase: 1
profile: production
estimate: 100-160 h
status: blocked
---

# G16 The service runs in staging and production in one EU region with least-privilege identities

## Outcome

Terraform for staging and production: two Cloud Run services, Cloud SQL, GCS buckets with lifecycle rules, Cloud Tasks, Secret Manager, VPC egress to Guidewire, org policy for locations; a readback proves region, identities and serving revision. Implements D6, D7, I7 in the design.

## Scope

- In: `infra/` modules per landing-zone conventions; service accounts `sa-intake-api`, `sa-submit-worker`, deployer; deployment readback script; rollback procedure.
- Out: Canary automation (G18).
- Depth: Build: chosen host with rollback; floor: no broad roles, no public unauthenticated worker.
- Route: Terraform plan reviewed before apply; Cloud Run revisions; private connectivity to Guidewire per G02.
- Prerequisites: G01, G03; authorised GCP projects; landing-zone access; user authorisation for apply.
- Supporting skills:
  - `adk-tool-auth-and-secrets`: serving, worker and deployer identities; Secret Manager grants
  - `adk-agent-observability`: telemetry sinks in the EU wired at first shared deployment
  - `adk-release-engineering`: revision labels carrying the release manifest
- Execution scope: Requires authorised GCP projects and explicit approval for each `terraform apply`.

## Acceptance

- [ ] Readback lists every resource in the chosen EU region and the serving revision's image digest.
- [ ] Only `sa-submit-worker` can read the Guidewire secret; the API cannot reach Guidewire write endpoints.
- [ ] Forbidden: plan contains no resource outside the EU region and no `allUsers` binding on the worker.

Verification: Offline: `terraform validate` and plan review; authorised live: apply to staging then production with readback.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G16-eu-deployment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
