---
goal: G27
title: Open the service to all EU home customers and hand it over
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability]
blocked_by: [G26]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 8-14
  review_and_verify: 3-5
  total: 11-19
  calendar_waits: none
  wait_days: 0
owner: Dev D
status: blocked
---

# G27 Open the service to all EU home customers and hand it over

## Outcome

Traffic ramps to all customers with gates, and on-call runbooks are handed over. Implements D13; Q14; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Ramp 10 %, 50 %, 100 % with gates; on-call handover; deferred-items review.
- Out: Phase 2.
- Depth: Production.

## Acceptance

- [ ] Each ramp step passes its gate.
- [ ] Previous revision retained and rollback tested.
- [ ] On-call runbook accepted by the platform on-call.

Verification: Production, authorised by the product owner.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G27-ga-ramp-and-handover.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
