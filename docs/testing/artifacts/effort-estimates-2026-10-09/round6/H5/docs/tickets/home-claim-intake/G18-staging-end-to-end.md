---
goal: G18
title: Run the whole journey in EU staging against the Guidewire sandbox
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G02, G03, G09, G13, G14, G16]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 15-27
  review_and_verify: 5-8
  total: 20-35
  calendar_waits: none
  wait_days: 0
owner: Dev D
status: blocked
---

# G18 Run the whole journey in EU staging against the Guidewire sandbox

## Outcome

Staging Cloud Run with Cloud SQL, the photo bucket, Vertex EU and the Guidewire sandbox runs the burst-pipe journey end to end. Implements D6, I6; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Container image, Cloud Run service, secrets from Secret Manager, migrations, smoke test.
- Out: Canary and production (G21, G27).
- Depth: Production hosting depth.

## Acceptance

- [ ] Deployed revision read back with image digest, model ID and region.
- [ ] The journey creates a sandbox claim with photos attached.
- [ ] Every resource is in the EU region; no secret values in environment variables.

Verification: Authorised live in staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G18-staging-end-to-end.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
