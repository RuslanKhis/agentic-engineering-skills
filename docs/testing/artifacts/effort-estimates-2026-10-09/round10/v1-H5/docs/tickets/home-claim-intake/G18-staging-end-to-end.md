---
goal: G18
title: The whole journey works in staging against Guidewire non-prod
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability]
blocked_by: [G10, G11, G12, G13, G16, G17]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 20-30
  review_and_verify: 8-12
  total: 28-42
  calendar_waits: none
owner: Eng D
status: blocked
---

# G18 The whole journey works in staging against Guidewire non-prod

## Outcome

All components deployed to staging through the release pipeline, connected
to Guidewire non-prod and the CIAM test tenant, and Maria's journey plus the
design's failure scenarios exercised there.

## Scope

- In: staging deployment of API, reconciler job and portal panel; Cloud SQL
  migrations; secrets; synthetic test customers; scripted run of the
  journey and of the cross-cutting failure table (lost response, double
  submit, kill switch, Guidewire down, rollback); 3 h handoff across owners.
- Out: load (G20); real customers.
- Depth: production.

## Acceptance

- [ ] Maria's journey with four photos produces a submitted claim in non-prod with photos attached, in under 10 minutes.
- [ ] Each cross-cutting failure row has a recorded staging result matching the design.
- [ ] Rollback to the previous release keeps drafts and ledger usable.
- [ ] Deployment readback shows the manifest of the serving revision.

Verification: authorised staging deployment and runs with synthetic data.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G18-staging-end-to-end.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
