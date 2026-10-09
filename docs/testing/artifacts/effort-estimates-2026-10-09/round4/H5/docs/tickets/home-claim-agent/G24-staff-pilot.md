---
goal: G24
title: Staff file synthetic claims end to end and adjusters judge the result
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-observability]
blocked_by: [G04, G06, G08, G10, G11, G12, G13, G14, G15, G17]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 20-34
  review_and_verify: 6-10
  total: 26-44
  calendar_waits: none
  wait_days: 0
owner: Eng B
status: proposed
---

# G24 Staff file synthetic claims end to end and adjusters judge the result

## Outcome

Phase 1 'done': the whole journey on staging with every floor control, measured, plus the form baseline for phase 2.

## Scope

- In: ~20 staff, scripted and free-form synthetic claims on the sandbox; two adjusters review created claims; release candidate passes the G08 gate; baseline figures from today's form.
- Out: Real customers (G31).
- Depth: Production depth on synthetic data. Floor: no real personal data.

## Acceptance

- [ ] A report with completion rate, adjuster-judged completeness, latency against T1 and cost per filed claim
- [ ] Zero duplicate claims across the pilot
- [ ] Failing sessions are turned into eval cases
- [ ] Issues are triaged into phase 2 goals

Verification: Authorised live on staging with the Guidewire sandbox.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G24-staff-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
