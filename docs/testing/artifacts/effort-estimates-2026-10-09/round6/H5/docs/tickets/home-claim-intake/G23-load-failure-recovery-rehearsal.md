---
goal: G23
title: Show the service survives a storm peak and recovers from failures
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [safe-api-tool-calls, deploy-adk-on-google-cloud]
blocked_by: [G18, G19]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 14-23
  review_and_verify: 5-8
  total: 19-31
  calendar_waits: none
  wait_days: 0
owner: Dev B
status: blocked
---

# G23 Show the service survives a storm peak and recovers from failures

## Outcome

Load and failure drills in staging confirm targets or record gaps. Implements I2, I8; failure table; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Load at 2× storm peak, instance kill mid-submit, Cloud SQL restore, rollback timing.
- Out: Tuning (later).
- Depth: Production.

## Acceptance

- [ ] p95 latencies at 2× storm peak meet the provisional targets or the gap is recorded.
- [ ] Killing an instance mid-submit ends in one claim after reconciliation.
- [ ] Cloud SQL restore into a new instance succeeds with measured RPO; rollback completes in under 5 minutes.

Verification: Authorised staging drills with a spend limit.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G23-load-failure-recovery-rehearsal.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
