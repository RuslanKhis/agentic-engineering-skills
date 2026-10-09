---
goal: G19
title: We know the service survives a storm-day surge and where it degrades
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [adk-operational-guardrails, adk-agent-observability]
blocked_by: [G11, G15, G16, G17]
phase: 1
profile: production
estimate: 48-80 h
status: blocked
---

# G19 We know the service survives a storm-day surge and where it degrades

## Outcome

A bounded load test in staging measures turn latency, tokens and cost per filed claim, admission behaviour at 10× surge and downstream saturation (Vertex quota, Guidewire sandbox limits). Implements D9, Q12, Q14 in the design.

## Scope

- In: Load profile, simulated users, measurement report, capacity settings changes, updated cost estimate.
- Out: Tuning (P2-05) unless a target is missed.
- Depth: Measure; cut-line option 4: steady load plus admission test only.
- Route: Staging with Guidewire sandbox or the fake behind a latency model, as authorised.
- Prerequisites: G11, G15, G16, G17; authorised spend for the test.
- Supporting skills:
  - `adk-operational-guardrails`: admission behaviour under surge
  - `adk-agent-observability`: measurement from traces and SLIs
- Execution scope: Requires authorised staging and a spend limit for the test.

## Acceptance

- [ ] Report shows p95 turn time, tokens and € per filed claim at steady load with cold and warm runs labelled.
- [ ] At the surge profile, excess sessions receive the fallback and no confirmed submission is lost.
- [ ] Forbidden: test traffic never reaches production Guidewire.

Verification: Authorised live in staging with declared request, time and cost limits.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G19-load-and-surge-test.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
