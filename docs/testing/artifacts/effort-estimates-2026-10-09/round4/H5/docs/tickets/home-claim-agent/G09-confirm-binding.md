---
goal: G09
title: Pressing Confirm files exactly the summary the customer saw, once
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 16-26
  review_and_verify: 8-14
  total: 24-40
  calendar_waits: none
  wait_days: 0
owner: Eng B
status: proposed
---

# G09 Pressing Confirm files exactly the summary the customer saw, once

## Outcome

Implements D3, I2 and I3 on our side: confirmation bound to the displayed draft version, a durable operation and dispatch.

## Scope

- In: `POST /drafts/{id}/confirm` with `version_hash`; fresh policy ownership/status check; draft frozen and unique `submission_operation` in one transaction; Cloud Tasks dispatch (fake in tests); `GET /operations/{id}`.
- Out: Guidewire calls (G10); UI (G12).
- Depth: Production depth. Floor: no path from the model to confirm.

## Acceptance

- [ ] Two confirms of the same draft produce one operation and the same status
- [ ] A stale `version_hash` returns 409 and dispatches nothing
- [ ] A lapsed or foreign policy at confirm time dispatches nothing
- [ ] A scripted model has no tool or route that reaches confirm

Verification: Offline plus local Postgres integration.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G09-confirm-binding.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
