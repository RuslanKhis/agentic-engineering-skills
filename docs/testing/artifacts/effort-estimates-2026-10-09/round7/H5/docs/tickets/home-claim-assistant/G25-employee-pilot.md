---
goal: G25
title: Employees file real claims through the assistant
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-observability]
blocked_by: [G10, G12, G14, G19, G21]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 24-36
  review_and_verify: 6-10
  total: 30-46
  calendar_waits: two-week employee pilot
  wait_days: 10
owner: Eng D
status: blocked
---

# G25 Employees file real claims through the assistant

## Outcome

A two-week pilot in production with employees who are policyholders, measuring quality, latency and the product outcome, with claims handlers reviewing every resulting FNOL.

## Scope

- In: invite list, feedback form, handler review sheet, exit criteria (minimum 30 claims, zero duplicate or misattributed claims).
- Out: real customers (G27).
- Depth: hosted trial.

## Acceptance

- [ ] Every pilot claim is reviewed by a handler and errors become eval cases
- [ ] Zero duplicate or wrong-policy claims
- [ ] SLO baselines are recorded for G19

Verification: Production, employees only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G25-employee-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
