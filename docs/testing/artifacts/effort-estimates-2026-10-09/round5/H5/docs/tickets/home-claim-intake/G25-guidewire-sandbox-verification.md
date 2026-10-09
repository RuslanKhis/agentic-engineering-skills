---
goal: G25
title: "The ClaimCenter contract is verified in the sandbox"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: [G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 6-10
  review_and_verify: 1-2
  total: 7-12
  calendar_waits: Guidewire sandbox credentials and ClaimCenter reference-field change from the Guidewire platform team
  wait_days: 10-20
owner: Integration eng
status: blocked
---

# G25 The ClaimCenter contract is verified in the sandbox

## Outcome

Every 'unknown' in the G02 contract is answered from the sandbox and the fixtures are replaced with recorded responses. Implements D4, O1; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g25--the-claimcenter-contract-is-verified-in-the-sandbox).

## Scope

- In: Exercise endpoints with synthetic policies; test the replay header twice with one key; record fixtures; update the fake.
- Out: Production code changes beyond the fake (G10, G11).
- Depth: Discovery with a stopping condition: stop when the contract has no 'unknown' rows.

## Acceptance

- [ ] Same create sent twice with one key yields one claim, or the contract records that it does not and D4 switches to lookup-only reconciliation.
- [ ] Lookup by the reference field returns the claim.
- [ ] Recorded fixtures replace doc-derived ones.

Verification: Bounded live checks against the Guidewire sandbox with synthetic data only. Execution scope: Sandbox only, after user approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G25-guidewire-sandbox-verification.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
