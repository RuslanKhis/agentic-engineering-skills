---
goal: G16
title: The release candidate runs on EU staging with a recorded, reversible release
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-release-engineering, adk-agent-observability]
blocked_by: [G02, G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 32-56
  review_and_verify: 10-16
  total: 42-72
  calendar_waits: none
  wait_days: 0
owner: Eng E
status: proposed
---

# G16 The release candidate runs on EU staging with a recorded, reversible release

## Outcome

Implements D6 and D14 on staging.

## Scope

- In: Two Cloud Run services behind staff-only access, service accounts, Cloud SQL connector, Secret Manager, NAT IP; CI builds, tests and writes `release-manifest.json`; G08 gate once the set exists; deploy readback; G05's live bucket check.
- Out: Production (G25); dashboards and alerts (G26).
- Depth: Production depth. Floor: staff-only access until G04 is deployed.

## Acceptance

- [ ] The readback shows image digest, model ID, prompt version and secret versions on the serving revision
- [ ] A failing gate blocks the deploy
- [ ] The previous revision is restored with one command
- [ ] A live photo upload to the staging bucket passes G05's checks

Verification: Authorised live on staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G16-staging-deployment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
