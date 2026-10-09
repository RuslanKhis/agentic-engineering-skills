---
goal: G17
title: On-call can see a failing filing, find its session and act within minutes
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: [protect-adk-sensitive-data]
blocked_by: [G16]
phase: 1
profile: production
estimate: 64-100 h
status: blocked
---

# G17 On-call can see a failing filing, find its session and act within minutes

## Outcome

One telemetry owner per service, traces and token cost per filed claim, SLIs and alerts (submission success, oldest pending/uncertain operation, tool error rate, turn p95, release-check hits, admission rejections) and runbooks for uncertain operations, Guidewire outage and kill switch. Implements I3, I8, SLIs in the design in the design.

## Scope

- In: `app/telemetry/`; dashboards and alert policies (as code); runbooks in `docs/runbooks/`.
- Out: Analytics and feedback (P2-08).
- Depth: Build: SLOs and alerts; targets provisional until pilot baselines.
- Route: OTel setup with ADK content capture off; trace, session and op IDs on every log line.
- Prerequisites: G16 staging.
- Supporting skills:
  - `protect-adk-sensitive-data`: content-free telemetry policy and sink retention
- Execution scope: Offline tests locally; the alert drill needs authorised staging.

## Acceptance

- [ ] An in-memory exporter test shows one span per agent, tool and logical model call with the session ID set.
- [ ] In staging, a forced `UNCERTAIN` operation older than 15 minutes fires the alert and the runbook leads to the operation and session.
- [ ] Forbidden: no conversation content in spans or logs (shared check with G13).

Verification: Offline exporter test; authorised staging alert drill.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G17-observability-and-runbooks.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
