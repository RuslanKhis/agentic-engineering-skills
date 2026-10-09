---
goal: G17
title: Storm-surge traffic degrades predictably and quotas are sized
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [adk-operational-guardrails]
blocked_by: [G04, G08, G12]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 22–38
  review_and_verify: 10–18
  total: 32–56
  calendar_waits: Vertex AI EU quota increase 1–2 weeks
owner: E2
status: blocked
---

# G17 Storm-surge traffic degrades predictably and quotas are sized

## Outcome

A load test at 20× average against staging with the fake Guidewire measures latency, quota headroom and DB connections, and confirms the kill switch and limits behave as designed.

## Scope

- In: Load scripts with simulated customers; measurements; quota requests; Cloud Run concurrency and instance settings.
- Out: Cost tuning (G27).
- Depth: Production. Floor: load test uses fake Guidewire and synthetic data.
- Route: Measured, not configured: p50/p95 turn latency cold and warm, 429 rate, Cloud SQL connections.
- Supporting skills: `adk-operational-guardrails` (admission and backpressure behaviour under load)
- Execution scope: Staging only, with a call cap the user approves.

## Acceptance

- [ ] p95 turn latency at 20× recorded against the provisional target
- [ ] 429s from Vertex lead to the designed message, not errors
- [ ] Quota and instance settings recorded in the plan

Verification: Authorised load run in staging with a model-call cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G17-load-and-storm-surge.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
