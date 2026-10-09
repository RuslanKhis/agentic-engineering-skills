---
goal: G17
title: Every filing can be traced from a session to its operation without exposing content
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-agent-observability
supporting_skills: [protect-adk-sensitive-data]
blocked_by: [G16]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 14-24
  review_and_verify: 4-8
  total: 18-32
  calendar_waits: none
  wait_days: 0
owner: Eng A
status: proposed
---

# G17 Every filing can be traced from a session to its operation without exposing content

## Outcome

Implements D15 spans and metrics; dashboards and alerts follow in G26.

## Scope

- In: `app/telemetry/`: one provider per process; spans per agent, tool and model call with `draft_id`, `operation_id`; metrics for T2, duplicates, uncertain age, tokens and cost per filed claim.
- Out: Dashboard, alerts, on-call (G26).
- Depth: Production depth. Floor: content capture off.

## Acceptance

- [ ] An in-memory exporter test shows one span per agent, tool and logical model call with IDs set
- [ ] No prompt, response or photo content appears in spans
- [ ] The metrics appear on staging after a test filing
- [ ] Usage is counted once per logical model call

Verification: Offline exporter test plus staging readback.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G17-telemetry.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
