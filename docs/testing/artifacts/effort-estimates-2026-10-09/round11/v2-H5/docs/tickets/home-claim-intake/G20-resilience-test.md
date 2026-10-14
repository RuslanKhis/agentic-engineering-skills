---
goal: G20
title: A storm-day surge and dependency failures in staging lose no confirmed claim
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [safe-api-tool-calls, adk-operational-guardrails]
blocked_by: [G09, G12, G18, G25, G35, W4, W15]
phase: 1
profile: production
estimate:
  hands_on: 16-24
  review_and_verify: 6-9
  total: 22-33
  calendar_waits: none
owner: Eng A
status: proposed
---

# G20 A storm-day surge and dependency failures in staging lose no confirmed claim

## Outcome

Measured latency, cost per claim and behaviour under surge and failures in
staging, before the external test. Needs the EU quota increase (W4) and the
live contract check (G25). Handoff: 2 h from Eng B and Eng C.

## Scope

- In: load script with simulated customers (scripted and live model mix
  within a declared spend limit), Guidewire fake fault modes in staging plus
  a short run against Guidewire non-prod, Cloud SQL failover, worker kills;
  a results note with token counts and dated prices.
- Out: tuning (phase 2 G30) unless a target in the design is missed.
- Depth: production.

## Acceptance

- [ ] A1 At 10× the assumed peak arrival rate, admission and fallback behave as in G18; no confirmed operation is lost; turn latency p95 and tokens per filed claim are measured and the cost per claim computed with dated prices for approval.
- [ ] A2 With the Guidewire fake unavailable for 30 minutes, confirmed operations wait and complete after recovery; customers see "received, number follows".
- [ ] A3 Killing workers mid-operation 20 times yields exactly one claim per confirmed draft.
- [ ] A4 A Cloud SQL failover during load fails in-flight turns cleanly with a retry message; no duplicate claims and no lost operation rows.

Verification: authorised staging run with request, time and spend limits
declared beforehand.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G20-resilience-test.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
