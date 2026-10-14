---
goal: G19
title: See SLIs, get alerted and follow a runbook for uncertain submissions
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: []
blocked_by: [G18]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-21
  review_and_verify: 3-6
  total: 15-27
  calendar_waits: none
  wait_days: 0
owner: Dev B
status: blocked
---

# G19 See SLIs, get alerted and follow a runbook for uncertain submissions

## Outcome

Traces, metrics, dashboards and alerts for the design's SLIs, with content capture off and a runbook. Implements D12; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: OpenTelemetry setup, SLI metrics, alerts (uncertain operations > 15 min, error-budget burn), runbook.
- Out: Production-to-eval sampling (phase 2).
- Depth: Production.

## Acceptance

- [ ] In-memory exporter test: one span per agent, tool and logical model call with session ID.
- [ ] No message content in spans or logs.
- [ ] Alerts fire in staging on an injected uncertain operation; runbook reviewed.

Verification: Offline exporter test; staging alert drill.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G19-observability-and-runbook.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
