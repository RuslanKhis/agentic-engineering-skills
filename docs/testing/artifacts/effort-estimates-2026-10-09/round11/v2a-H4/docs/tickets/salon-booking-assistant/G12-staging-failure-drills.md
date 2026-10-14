---
goal: G12
title: Failures on staging end the way the design says
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-evaluation, safe-api-tool-calls]
blocked_by: [G10]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 1.5-2
  review_and_verify: 0.5-1
  total: 2-3
  calendar_waits: none
owner: Dev C
status: ready
---

# G12 Failures on staging end the way the design says

## Outcome

Failure drills and the evaluation run against the staging deployment, while
the salon chain's approval is pending. Evidence for I1–I5 on the deployed
system.

## Scope

- In: drills on staging with two test customers; evaluation set against the
  staging deployment; results recorded in the plan.
- Out: production.
- Depth: Build; staging only.

## Acceptance

- [ ] A1 Kill switch off and on: chat and new dispatches stop and resume.
- [ ] A2 Booking API stopped during a confirm → `uncertain` → reconciled with
  the operator script once it is back; no duplicate appointment.
- [ ] A3 Double-click confirm → one appointment.
- [ ] A4 A second test customer cannot see or act on the first's
  appointments, sessions or operations.
- [ ] A5 The evaluation set runs against the staging deployment and meets its
  thresholds; results recorded in the plan.

Verification: authorised staging runs only.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G12-staging-failure-drills.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
