---
goal: G18
title: Anna's journey works end to end in staging against the Guidewire sandbox
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G04, G05, G07, G10, G11]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 12-20
  review_and_verify: 4-8
  total: 16-28
  calendar_waits: none
owner: Platform
status: blocked
---

# G18 Anna's journey works end to end in staging against the Guidewire sandbox

## Outcome

This is the first place where all components run together. The pen test (W3) and the load test (G20) start from it.

## Scope

- In: Deploy API, worker and frontend build to staging with synthetic customers, readback of the serving revision and config, persistence across a revision restart, smoke test script.
- Out: Production (G24). Load (G20).
- Depth: Synthetic data only.

Supporting skills and why:
- adk-agent-observability (first shared environment)
- adk-release-engineering (first shared environment)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] The scripted journey with synthetic customer and photos ends with a claim number from the Guidewire sandbox and photos attached.
- [ ] After forcing a new revision mid-session, the session and draft resume.
- [ ] The served revision, model ID and prompt version match the release manifest (readback).
- [ ] W3 pen test is triggered against this environment.

Verification: Authorised live: staging and Guidewire sandbox only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G18-staging-end-to-end.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
