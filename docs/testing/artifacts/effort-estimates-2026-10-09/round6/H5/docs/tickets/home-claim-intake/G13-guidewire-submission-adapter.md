---
goal: G13
title: Turn one confirmed draft into exactly one claim with its photos
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01, G07]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 21-36
  review_and_verify: 8-12
  total: 29-48
  calendar_waits: none
  wait_days: 0
owner: Dev B
status: blocked
---

# G13 Turn one confirmed draft into exactly one claim with its photos

## Outcome

A confirmed draft creates one ClaimCenter claim, photos attach as documents and uncertain outcomes are reconciled. Implements D4, I2, I3, I5; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Submission route, operation table (unique per draft), canonical payload and hash, adapter with the G01 replay contract, reconciliation and document retry jobs.
- Out: UI (G14), load drills (G23).
- Depth: Production external-write depth.

## Acceptance

- [ ] Confirm creates an operation and returns the claim number; a second confirm returns the same claim.
- [ ] Timeout after commit (fake) leaves `uncertain`; reconciliation finds the claim and never sends a second create; a restart mid-dispatch reconciles.
- [ ] Stale version or wrong hash gets 409 with no outbound call; a failed photo upload retries per document.

Verification: Offline with a fake ClaimCenter; then sandbox, at most 30 test claims.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-guidewire-submission-adapter.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
