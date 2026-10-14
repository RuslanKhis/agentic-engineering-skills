---
goal: G22
title: Operators can recover uncertain claims, roll back and restore
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, safe-api-tool-calls]
blocked_by: [G16, G24]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 14-24
  review_and_verify: 4-6
  total: 18-30
  calendar_waits: none
owner: Platform
status: blocked
---

# G22 Operators can recover uncertain claims, roll back and restore

## Outcome

The recovery owner for the failure table in the design exists before real customers.

## Scope

- In: Runbooks: UNCERTAIN op reconciliation, Guidewire outage, kill switch, model 429 storm, rollback, Cloud SQL restore (RPO 15 min assumption). On-call rota, rollback rehearsal in staging, backup restore test.
- Out: Multi-region (Later).
- Depth: Build.

Supporting skills and why:
- adk-agent-observability (alert-to-runbook links)
- safe-api-tool-calls (reconciliation runbook)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] Rollback rehearsal in staging: previous revision serving within the target, and live sessions continue.
- [ ] A Cloud SQL point-in-time restore into a scratch instance succeeds. Then the scratch instance is deleted and its absence verified.
- [ ] Each alert from G16 links to a runbook step.

Verification: Authorised live: staging and a scratch instance.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G22-operational-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
