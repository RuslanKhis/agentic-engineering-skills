---
goal: G20
title: Measured latency, capacity and cost per claim at storm peak
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: optimise-adk-on-google-cloud
supporting_skills: [adk-operational-guardrails]
blocked_by: [G18, W4]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 12-20
  review_and_verify: 4-6
  total: 16-26
  calendar_waits: W4
owner: Agent
status: blocked
---

# G20 Measured latency, capacity and cost per claim at storm peak

## Outcome

Replaces the illustrative A4/A14 figures with measurements (T2).

## Scope

- In: Bounded load test in staging: about 25 concurrent simulated sessions with scripted customers, on the real model under the W4 quota. It measures time to first token, complete turn, tokens and cost per completed claim, 429 behaviour and Cloud SQL connections.
- Out: Tuning (P2-05).
- Depth: Measurement only, with a fixed request and cost ceiling stated before running.

Supporting skills and why:
- adk-operational-guardrails (limits under load)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] A report with p50/p95 TTFT, cost per completed claim and the saturation point, with cold and warm runs recorded separately.
- [ ] At the stated ceiling, limits engage as designed. No unbounded retries.

Verification: Authorised live: staging, within the stated cost cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G20-load-and-cost-test.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
