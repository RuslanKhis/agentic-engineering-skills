---
goal: G23
title: "Real customers file claims in a small pilot and we measure the outcome"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-observability]
blocked_by: [G03, G08, G22, G26]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 24-36
  review_and_verify: 6-10
  total: 30-46
  calendar_waits: Pilot traffic period
  wait_days: 10-15
owner: ML eng
status: blocked
---

# G23 Real customers file claims in a small pilot and we measure the outcome

## Outcome

A 2–3 week pilot for a small share of portal users with baselines compared, failures turned into evaluation cases and SLO targets set. Implements T1, T2, A13; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g23--real-customers-file-claims-in-a-small-pilot-and-we-measure-the-outcome).

## Scope

- In: Pilot cohort flag; daily review of failed intakes; handler feedback; SLO targets; new cases into the G09 set.
- Out: GA rollout (G24).
- Depth: Build.

## Acceptance

- [ ] Completion and completeness compared with the web-form baseline (O7).
- [ ] Zero duplicate claims; every uncertain operation reconciled.
- [ ] Go/no-go recommendation written.

Verification: Production pilot evidence. Execution scope: Production with pilot cohort, after user approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G23-controlled-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
