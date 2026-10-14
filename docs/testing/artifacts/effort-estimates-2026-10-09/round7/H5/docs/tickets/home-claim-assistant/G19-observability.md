---
goal: G19
title: On-call can see failures without seeing content
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-observability
supporting_skills: [adk-release-engineering]
blocked_by: [G03, G11]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 26-40
  review_and_verify: 6-10
  total: 32-50
  calendar_waits: none
owner: Eng B
status: blocked
---

# G19 On-call can see failures without seeing content

## Outcome

Traces, metrics and alerts per D13 with the SLIs in the design, correlation IDs at every hop and dashboards.

## Scope

- In: OTel setup per service, SLIs, burn-rate alerts, a dashboard, trace-to-session lookup.
- Out: runbooks (G26).
- Depth: build; targets from pilot data.

## Acceptance

- [ ] An in-memory exporter test shows one span per agent, tool and model call with session and operation IDs
- [ ] No content attributes in spans
- [ ] A forced Guidewire failure in staging fires the submission alert

Verification: Offline exporter test; staging check.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G19-observability.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
