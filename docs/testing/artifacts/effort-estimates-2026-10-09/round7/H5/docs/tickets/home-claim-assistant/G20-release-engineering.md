---
goal: G20
title: Releases move and roll back as one unit
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G03, G13]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 26-40
  review_and_verify: 6-10
  total: 32-50
  calendar_waits: none
owner: Eng D
status: blocked
---

# G20 Releases move and roll back as one unit

## Outcome

The release manifest, CI eval gate using G13, Cloud Run traffic-split canary and joint rollback per D14.

## Scope

- In: manifest file, gate thresholds and cost cap per run, canary script with predefined thresholds, rollback procedure.
- Out: production samples to eval (G30).
- Depth: build.

## Acceptance

- [ ] A seeded prompt regression fails the gate by exit code
- [ ] A canary to staging with a bad revision is rolled back with prompt, model and image together
- [ ] A skipped eval run is reported as missing, not passed

Verification: CI and staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G20-release-engineering.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
