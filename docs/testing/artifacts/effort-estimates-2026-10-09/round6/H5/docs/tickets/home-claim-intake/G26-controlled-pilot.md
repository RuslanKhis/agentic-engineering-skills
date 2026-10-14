---
goal: G26
title: Run a pilot with invited customers and decide go or no-go
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G04, G21, G22, G23, G25]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 18-30
  review_and_verify: 5-9
  total: 23-39
  calendar_waits: pilot period with invited customers
  wait_days: 15-20
owner: ML
status: blocked
---

# G26 Run a pilot with invited customers and decide go or no-go

## Outcome

Invited customers file real claims; handlers review each one against the form baseline; a go/no-go decision is recorded. Implements Outcome hypothesis; all invariants; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Invitation list, pilot flag, handler review form, baseline comparison.
- Out: GA ramp (G27).
- Depth: Production with limited audience.

## Acceptance

- [ ] Every pilot claim reviewed by a handler; call-back rate, completion and correction compared with the form baseline.
- [ ] Zero duplicate claims; SLOs met or gaps listed.
- [ ] Go/no-go recorded by the product owner.

Verification: Production pilot, authorised by the product owner after DPIA sign-off.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G26-controlled-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
