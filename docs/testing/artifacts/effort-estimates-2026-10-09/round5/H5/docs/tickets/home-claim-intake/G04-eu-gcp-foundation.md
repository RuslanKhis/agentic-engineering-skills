---
goal: G04
title: "The team can deploy to EU dev, staging and prod projects with least-privilege identities"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: []
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 16-24
  review_and_verify: 4-8
  total: 20-32
  calendar_waits: Project creation and org-policy grants from the cloud team
  wait_days: 3-10
owner: Platform eng
status: ready
---

# G04 The team can deploy to EU dev, staging and prod projects with least-privilege identities

## Outcome

Three EU projects with Cloud Run, Cloud SQL, GCS buckets, Cloud Tasks, Secret Manager, service accounts and a budget alert, created by IaC, plus a hello-world API deployed to dev. Implements D7, D10, D14; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g04--the-team-can-deploy-to-eu-dev-staging-and-prod-projects-with-least-privilege-identities).

## Scope

- In: IaC for projects and services; region pinned; org policy restricting resource locations to EU; service accounts `claim-assistant-api`, `claim-submission-worker`; budget alert; dated price lookup for the cost formula in the design.
- Out: Application features; telemetry (G16); release pipeline (G17).
- Depth: Build; least privilege; no secrets in IaC.

## Acceptance

- [ ] Readback shows every resource in the chosen EU region and the location org policy active.
- [ ] The API service account cannot read the Guidewire write secret; only the worker can.
- [ ] Budget alert configured; cost formula in the design filled with dated prices.

Verification: Authorised cloud apply in dev; readback commands recorded. Execution scope: Needs user approval to create projects and IAM.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-eu-gcp-foundation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
