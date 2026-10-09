---
goal: G10
title: The whole system runs on staging in the EU, traceable without customer content in telemetry
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 18-28
  review_and_verify: 5-8
  total: 23-36
  calendar_waits: GCP staging projects and IAM from platform team
owner: Eng B
status: blocked
---

# G10 The whole system runs on staging in the EU, traceable without customer content in telemetry

## Outcome

Implements D11, invariant I6 and the release manifest.

## Scope

- In:
  - Two Cloud Run services in europe-west3 with separate service accounts; Cloud SQL, Cloud Tasks, GCS, Secret Manager (requested through the platform team's Terraform)
  - OTel traces with content capture off; `session_id`, `invocation_id`, `submission_id` on spans
  - Release manifest; deterministic tests in CI
- Out: Eval gate and canary (G17); SLOs and alerts (G18); production (G24)
- Depth: Build for staging only.

## Acceptance

- [ ] Deployed revision readback matches the manifest
- [ ] Exporter test shows one span per agent, tool and model call, with no prompt or response content
- [ ] The chat-api service account is denied on the Guidewire secret

Verification: Offline exporter test; authorised staging deployment after the platform team's grants.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G10-staging-deployment-and-telemetry.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
