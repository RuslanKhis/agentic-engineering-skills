---
goal: G22
title: Production Guidewire access is requested early enough for the dark connection
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 2-3
  review_and_verify: 1-1
  total: 3-4
  calendar_waits: Guidewire production change approval and IP allow-list
  wait_days: 10-15
owner: Eng D
status: ready
---

# G22 Production Guidewire access is requested early enough for the dark connection

## Outcome

Starts the 10-15 day production change approval on day 1 so G23 is not delayed.

## Scope

- In: Request for a production OAuth client and IP allow-list; the static IP amended when G02 reserves it.
- Out: Configuration (G23).
- Depth: Floor: no credentials in the request record.

## Acceptance

- [ ] The request reference and date are recorded
- [ ] The IP amendment has been sent once G02 reserves the address
- [ ] The approver and expected date are recorded
- [ ] No secret is stored in the repository

Verification: Document evidence only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G22-request-production-guidewire-access.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
