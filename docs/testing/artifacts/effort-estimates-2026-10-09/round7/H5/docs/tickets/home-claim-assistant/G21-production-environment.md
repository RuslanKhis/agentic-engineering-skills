---
goal: G21
title: Production is ready and can be restored
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G03, G15]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 30-46
  review_and_verify: 8-12
  total: 38-58
  calendar_waits: none
owner: Eng E
status: blocked
---

# G21 Production is ready and can be restored

## Outcome

The production project mirroring staging, with Cloud SQL HA and point-in-time recovery, bucket retention, secret rotation and a restore drill.

## Scope

- In: prod IaC, backup policy, restore runbook draft, rotation of the Guidewire client secret.
- Out: on-call runbooks (G26).
- Depth: build.

## Acceptance

- [ ] A restore of Cloud SQL to a point in time in a scratch instance succeeds within the agreed time
- [ ] Secret rotation does not interrupt a running worker
- [ ] Deploy readback shows the production revision, region and service accounts

Verification: Authorised hosted check.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G21-production-environment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
