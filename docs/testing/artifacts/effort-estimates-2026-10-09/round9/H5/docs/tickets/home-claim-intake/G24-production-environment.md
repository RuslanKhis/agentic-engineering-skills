---
goal: G24
title: Production environment in the EU
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G04]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 14-24
  review_and_verify: 6-10
  total: 20-34
  calendar_waits: none
owner: Platform
status: blocked
---

# G24 Production environment in the EU

## Outcome

This is the environment the pilot and GA run in (D7).

## Scope

- In: Terraform for prod: same modules as G04, min instances 1, Cloud SQL HA and PITR, Guidewire production client secret with a rotation procedure, budget alerts, least-privilege deployer identity.
- Out: Runbooks (G22).
- Depth: Build.

Supporting skills and why:
- adk-tool-auth-and-secrets (production secrets and rotation)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] `terraform plan` for prod shows only EU locations and no broader IAM than staging.
- [ ] Secret rotation is rehearsed: the new version is picked up without a redeploy, or the redeploy step is documented.
- [ ] The deployer identity cannot read customer data buckets (checked).

Verification: Authorised live: production project, with named approver.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G24-production-environment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
