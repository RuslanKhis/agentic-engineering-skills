---
goal: G19
title: Storm-day surge does not lose claims or blow the budget
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [deploy-adk-on-google-cloud]
blocked_by: [G11, G15, G16]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 20-34
  review_and_verify: 10-16
  total: 30-50
  calendar_waits: Vertex AI quota confirmation (G02)
owner: E4
status: blocked
---

# G19 Storm-day surge does not lose claims or blow the budget

## Outcome

The team knows the assistant handles twice the assumed storm peak with a fake Guidewire, where it saturates, and that limits degrade to the form. Implements Budgets and capacity, A8.

## Scope

- In: Load script at 2× assumed peak (≈ 80 concurrent sessions) with simulated conversations; fake Guidewire with latency/outage; quota and Cloud SQL connection checks; report with p95 reply time and cost per claim.
- Out: Tuning (phase 2 G26).
- Depth: Minimal performance work; build the surge evidence.
- Route: Staging with a declared call and cost cap.
- Supporting skills: `deploy-adk-on-google-cloud` (instance and connection limits)
- Execution scope: Staging, with a declared model-call cap approved before the run.

## Acceptance

- [ ] At 2× peak, p95 reply ≤ 8 s or the bottleneck is named
- [ ] Guidewire outage during load: zero lost submissions, all reconciled after recovery
- [ ] Global ceiling reached: fallback served, no 5xx storm
- [ ] Run cost within the declared cap

Verification: Authorized live in staging with caps.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G19-storm-surge-load-test.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
