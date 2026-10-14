---
goal: G16
title: SLIs, alerts and no-content telemetry
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: [protect-adk-sensitive-data]
blocked_by: [G04, G10]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 18-30
  review_and_verify: 6-10
  total: 24-40
  calendar_waits: none
owner: Frontend
status: blocked
---

# G16 SLIs, alerts and no-content telemetry

## Outcome

Implements D14 and supports T1/T2 and I6.

## Scope

- In: One OTel provider per process → Cloud Trace/Monitoring. ADK content capture off. Session, invocation and op IDs on spans and logs. SLIs: submission success, UNCERTAIN op age, turn latency, tool error rate by tool, tokens per completed claim. Alert policies and dashboards. Screening error rate.
- Out: Runbooks (G22).
- Depth: Build, with targets provisional until pilot data (G27).

Supporting skills and why:
- protect-adk-sensitive-data (content-capture gates)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] An in-memory exporter test shows one span per agent, tool and logical model call, with IDs set.
- [ ] A sentinel PII string sent through a full turn does not appear in any exported span or log.
- [ ] An UNCERTAIN op older than 15 min triggers the alert in staging.

Verification: Offline exporter test. Authorised live: staging alerts.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G16-observability.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
