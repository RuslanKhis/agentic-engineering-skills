---
goal: G16
title: On-call can see when claims stop flowing and trace a failure to its session
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: [protect-adk-sensitive-data]
blocked_by: [G02, G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 20-30
  review_and_verify: 6-8
  total: 26-38
  calendar_waits: none
owner: Eng D
status: blocked
---

# G16 On-call can see when claims stop flowing and trace a failure to its session

## Outcome

One OpenTelemetry provider per process exporting to EU sinks with content
capture off; the SLIs of the design (I7 ratio, tool errors, tokens per
submitted claim, p95 turn, old `UNCERTAIN` rows); dashboards; burn-rate
alerts; a runbook entry per alert.

## Scope

- In: spans per agent, tool and logical model call carrying session,
  invocation and `operation_id`; metrics for the ledger states; dashboards
  and alerts on dev and staging; 1 h handoff from Eng A.
- Out: production thresholds (set from G20 and the pilot).
- Depth: production.

## Acceptance

- [ ] In-memory exporter test: one span per agent, tool and model call with the session ID set; no prompt text in attributes.
- [ ] A forced Guidewire failure on dev raises the alert and the trace links to the ledger row.
- [ ] Tokens per submitted claim is visible per release.

Verification: offline exporter test; authorised dev-project check.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G16-observability-slos.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
