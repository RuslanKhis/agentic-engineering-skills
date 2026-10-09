---
goal: G16
title: "On-call can see a failing intake and reach its session in minutes"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: []
blocked_by: [G04, G01]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 14-20
  review_and_verify: 4-6
  total: 18-26
  calendar_waits: none
  wait_days: 0
owner: Platform eng
status: blocked
---

# G16 On-call can see a failing intake and reach its session in minutes

## Outcome

Traces, SLIs from the design, dashboards, the uncertain-operation alert and a runbook. Implements D10, I3, T1; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g16--on-call-can-see-a-failing-intake-and-reach-its-session-in-minutes).

## Scope

- In: One OTel owner per process; SLIs; alerts; runbook for uncertain submissions.
- Out: Production sample to eval loop (P2-04).
- Depth: Build.

## Acceptance

- [ ] In-memory exporter test: one span per agent, tool and model call with session ID.
- [ ] An operation stuck 15 minutes fires an alert to claims ops in dev.
- [ ] Runbook walks from alert to session and Guidewire claim.

Verification: Offline exporter test; dev alert test. Execution scope: Dev only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G16-observability-and-alerts.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
