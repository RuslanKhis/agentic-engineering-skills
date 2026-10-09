---
goal: G10
title: "A confirmed claim is created in ClaimCenter exactly once, even when replies are lost"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01, G02, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 14-20
  review_and_verify: 8-12
  total: 22-32
  calendar_waits: none
  wait_days: 0
owner: Integration eng
status: blocked
---

# G10 A confirmed claim is created in ClaimCenter exactly once, even when replies are lost

## Outcome

The worker turns an accepted operation into one ClaimCenter FNOL using the replay key and reference field, and the reconciler resolves uncertain outcomes without re-creating. Implements D4, I2, I3; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g10--a-confirmed-claim-is-created-in-claimcenter-exactly-once-even-when-replies-are-lost).

## Scope

- In: Cloud Tasks worker; Guidewire client with replay key and reference field; fencing on the operation row; reconciler; built on the G28 operation schema agreed on day one of both goals.
- Out: Confirm route and operation store (G28); photo attachment (G11); live sandbox run (G11).
- Depth: Build with careful review: irreversible external write.

## Acceptance

- [ ] Worker retry of the same task produces one claim against the Guidewire fake.
- [ ] Fault injection: Guidewire commits, response lost, worker killed → reconciler records the existing claim number; no second claim.
- [ ] A stale worker with an old fencing version cannot record a result.
- [ ] No path from the model to the Guidewire client (import and call-graph test).

Verification: Offline with the Guidewire fake built from G02 fixtures. Execution scope: Local only; live sandbox verification is in G11.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G10-idempotent-claim-worker.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
