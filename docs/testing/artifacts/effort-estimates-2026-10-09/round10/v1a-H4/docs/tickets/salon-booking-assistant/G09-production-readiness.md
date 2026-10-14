---
goal: G09
title: Production is ready to switch on for one salon and to roll back in minutes
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-release-engineering]
blocked_by: [G06]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3.5-5
  review_and_verify: 1-1.5
  total: 4.5-6.5
  calendar_waits: none
owner: Dev C
status: blocked
---

# G09 Production is ready to switch on for one salon and to roll back in minutes

## Outcome

There is a production Cloud Run service set up like staging, with every
salon's flag off and min instances 1. A rollback drill has been rehearsed on
staging. A one-page runbook covers `uncertain` and `partial` ledger rows (from
G03), the kill switch and rollback (D6, D9).

## Scope

- In: production service, service account, secrets and schema; per-salon
  flags set to off in configuration (the flag behaviour itself is checked at
  go-live, once the widget code exists); a rollback drill (deploy a bad
  revision to staging, roll back, check sessions survive); and the runbook,
  with staff steps for a `partial` move. Until G14 automates it, the on-call
  developer runs a manual reconciliation query at least once a day.
- Out: switching on any salon (go-live goal).
- Depth: MVP; the floor is that rollback is rehearsed and the kill switch is
  reachable by two people.

## Acceptance

- [ ] Prod readback: revision, service account and `release.json` recorded. All salon flags are set to off, and the production booking site does not embed the widget yet.
- [ ] Staging rollback drill completes in under 10 minutes with the session preserved. Commands are recorded.
- [ ] The runbook has been reviewed by a second developer.

Verification: authorised deploys to staging and production. The readback
commands are recorded in Evidence.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-production-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
