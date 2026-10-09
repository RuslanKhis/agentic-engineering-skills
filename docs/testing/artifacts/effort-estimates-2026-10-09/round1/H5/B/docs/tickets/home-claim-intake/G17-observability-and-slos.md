---
goal: G17
title: On-call can see failures, cost and stuck claims
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: []
blocked_by: [G16]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 22-38
  review_and_verify: 18-32
  total: 40-70
  calendar_waits: On-call owner decision (O7)
owner: E5
status: blocked
---

# G17 On-call can see failures, cost and stuck claims

## Outcome

Each design guarantee has a signal, an alert and a runbook, and an alert leads to a stored session and operation. Implements SLIs in the design, I7, O7.

## Scope

- In: One OpenTelemetry owner; Cloud Trace/Monitoring/Logging in the EU; SLIs from the design; alerts on burn rate and on uncertain operations older than 1 h; dashboards; runbooks.
- Out: BigQuery analytics (phase 2).
- Depth: Build: SLOs and alerts.
- Route: ADK telemetry with content capture off; custom metrics for operations and budgets.
- Supporting skills: none
- Execution scope: Staging monitoring config.

## Acceptance

- [ ] In-memory exporter test: one span per agent, tool and model call, session ID set, no content
- [ ] Staging: an injected Guidewire outage fires the uncertain-operations alert
- [ ] Tokens and cost per submitted claim visible per day
- [ ] Runbook links alert → session → operation

Verification: Offline exporter test; staging fault injection.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G17-observability-and-slos.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
