---
goal: G11
title: "Confirmed photos appear on the ClaimCenter claim, with honest partial status"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: [G10, G28, G06, G25]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 13-18
  review_and_verify: 5-8
  total: 18-26
  calendar_waits: none
  wait_days: 0
owner: Integration eng
status: blocked
---

# G11 Confirmed photos appear on the ClaimCenter claim, with honest partial status

## Outcome

Each clean photo becomes a ClaimCenter document through its own idempotent operation; the customer sees per-photo status. Implements D4, D6, I3; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g11--confirmed-photos-appear-on-the-claimcenter-claim-with-honest-partial-status).

## Scope

- In: Child attach operations; retries; status in the status route.
- Out: Re-upload UI polish (G27).
- Depth: Build.

## Acceptance

- [ ] Five photos attach once each despite a retried task.
- [ ] Attach failure after claim creation shows the claim number and pending photos; claim is never re-created.
- [ ] Only photos of the confirmed draft are attached.
- [ ] Sandbox run: double confirm, worker retry and lost-response replay produce one claim with each photo attached once.

Verification: Offline fake; sandbox run. Execution scope: Sandbox only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-photo-attachment-to-claim.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
