---
goal: G12
title: A team member files a claim with photos on staging and gets a Guidewire sandbox claim number
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [safe-api-tool-calls]
blocked_by: [G04, G05, G06, G07, G10, G11]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 8-14
  review_and_verify: 4-6
  total: 12-20
  calendar_waits: none
owner: Eng A
status: blocked
---

# G12 A team member files a claim with photos on staging and gets a Guidewire sandbox claim number

## Outcome

Phase 1 done: the journey end to end with I2 checked against the sandbox.

## Scope

- In:
  - Run the journey on staging against the Guidewire sandbox
  - Run the G07 eval set against staging
  - Sandbox replay check of I2
- Out: Production connection (G14)
- Depth: Synthetic customers and sandbox only.

## Acceptance

- [ ] A sandbox claim number is returned with six documents attached
- [ ] A duplicate Submit creates nothing new in the sandbox
- [ ] Staging eval results are within tolerance of the G07 baseline

Verification: Authorised live run, staging and sandbox only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-staging-end-to-end-guidewire-sandbox.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
