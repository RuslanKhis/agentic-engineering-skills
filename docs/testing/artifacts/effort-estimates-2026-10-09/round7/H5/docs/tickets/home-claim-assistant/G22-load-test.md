---
goal: G22
title: It holds up after a storm
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [adk-operational-guardrails]
blocked_by: [G18, G21, W6]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 18-28
  review_and_verify: 4-8
  total: 22-36
  calendar_waits: see W6
owner: Eng A
status: blocked
---

# G22 It holds up after a storm

## Outcome

A bounded load test at the A7 peak against staging with a Guidewire stub, measuring turn latency, model quota use and degrade behaviour.

## Scope

- In: load script, quota plan with W6 result, report with cold and warm runs and failures kept.
- Out: tuning (G33).
- Depth: measure only.

## Acceptance

- [ ] Report shows p95 turn latency and error rate at the assumed peak
- [ ] When quota is exhausted the degrade mode appears, not errors
- [ ] The spend of the test stayed under its cap

Verification: Authorised hosted check in staging with request and cost limits.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G22-load-test.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
