---
goal: G23
title: The team can run, roll back and recover the service on the first day of GA
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G18, G20]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 16-24
  review_and_verify: 6-8
  total: 22-32
  calendar_waits: none
owner: Eng D
status: blocked
---

# G23 The team can run, roll back and recover the service on the first day of GA

## Outcome

Runbooks, on-call rota, alert routing, rollback rehearsal in production,
backup restore test, ops-queue ownership in claims operations, and the
change-board pack for go-live.

## Scope

- In: runbook per alert; rehearsed rollback of image, prompt and model
  together; Cloud SQL restore into a scratch instance; owned-resource list
  and cleanup check; production thresholds from the load test; the
  change-board pack; 2 h handoff from Eng B.
- Out: post-GA tuning.
- Depth: production.

## Acceptance

- [ ] Rollback rehearsed in production within the target time with no data loss.
- [ ] Restore test recovers drafts and ledger to a point in time.
- [ ] On-call rota and escalation to the Guidewire team published.
- [ ] Change-board pack submitted.

Verification: authorised production rehearsal and restore test with
recorded commands.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G23-ga-operations-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
