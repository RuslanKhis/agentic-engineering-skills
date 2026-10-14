---
goal: G37
title: Rotating the Guidewire secret causes no failed requests
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [deploy-adk-on-google-cloud]
blocked_by: [G16, G34, W1]
phase: 1
profile: production
estimate:
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  calendar_waits: none
owner: Eng C
status: proposed
---

# G37 Rotating the Guidewire secret causes no failed requests

## Outcome

Moved from G16 after the independent review: rotation can only be shown with the real non-prod client from W1. Handoff: 1 h from Eng D on the client's token cache.

## Scope

- In: rotation procedure and test in staging.
- Out: production rotation schedule (runbook).
- Depth: production.

## Acceptance

- [ ] A1 Rotating the Guidewire client secret in Secret Manager takes effect without downtime or failed requests in staging against Guidewire non-prod; an expired or revoked secret raises an alert and stops retries.

Verification: authorised staging with Guidewire non-prod.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G37-secret-rotation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
