---
goal: G24
title: "All customers in the market can file a home claim with the assistant"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-observability]
blocked_by: [G19, G23]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 10-16
  review_and_verify: 4-6
  total: 14-22
  calendar_waits: Canary ramp 5 % to 100 %
  wait_days: 5
owner: Agent lead
status: blocked
---

# G24 All customers in the market can file a home claim with the assistant

## Outcome

Go/no-go held, canary ramp completed with thresholds, runbooks handed to on-call and claims operations. Implements D15; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g24--all-customers-in-the-market-can-file-a-home-claim-with-the-assistant).

## Scope

- In: Go/no-go; canary; comms with claims ops and hotline.
- Out: Phase 2.
- Depth: Build.

## Acceptance

- [ ] Canary thresholds decided before traffic moves and met at each step.
- [ ] Previous revision kept ready 7 days.
- [ ] On-call and claims ops sign the handover.

Verification: Production release evidence. Execution scope: Production, after user approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G24-ga-rollout.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
