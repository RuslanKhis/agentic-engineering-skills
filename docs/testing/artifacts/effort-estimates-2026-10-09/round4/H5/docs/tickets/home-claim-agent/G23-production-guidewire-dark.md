---
goal: G23
title: Production can reach Guidewire without filing anything
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G10, G22]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 16-27
  review_and_verify: 5-9
  total: 21-36
  calendar_waits: none
  wait_days: 0
owner: Eng E
status: proposed
---

# G23 Production can reach Guidewire without filing anything

## Outcome

Prepares the production connection behind D3 with rotation documented; no customer traffic.

## Scope

- In: Production client in Secret Manager readable only by `submitter-sa`; rotation steps documented; read-only connectivity check from the production project.
- Out: Production deploy and canary (G25); reconciliation runbook (G26).
- Depth: Production depth. Floor: no claim is created.

## Acceptance

- [ ] The connectivity check passes from the production project
- [ ] No claim is created in production
- [ ] Only `submitter-sa` can read the production secret
- [ ] Rotation steps are documented and dry-run

Verification: Authorised live, read-only, in production.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G23-production-guidewire-dark.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
