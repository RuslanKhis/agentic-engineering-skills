---
goal: G21
title: GA go/no-go with rehearsed recovery, rollback and erasure
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-release-engineering, adk-agent-observability]
blocked_by: [G20, G17]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 22–38
  review_and_verify: 10–18
  total: 32–56
  calendar_waits: Go/no-go meeting with claims, compliance and security
owner: E3
status: blocked
---

# G21 GA go/no-go with rehearsed recovery, rollback and erasure

## Outcome

Recovery, rollback, database-restore and erasure drills pass; SLO targets are set from pilot data; on-call rota and runbooks are live; go/no-go recorded.

## Scope

- In: Drills in staging and production-safe forms; SLO documents; on-call rota; GA flag plan.
- Out: Phase 2 goals.
- Depth: Production. Floor: previous revision ready 7 days after GA.
- Route: Cloud SQL point-in-time restore rehearsal; Cloud Run revision rollback; erasure job on a test customer.
- Supporting skills: `adk-release-engineering` (rollback drill of the full bundle); `adk-agent-observability` (SLO targets reset from pilot baseline)
- Execution scope: Staging drills; production readbacks under the GA change.

## Acceptance

- [ ] Rollback and DB restore drills pass with measured time
- [ ] Erasure drill deletes a test customer's session, draft and photos, and leaves unrelated data
- [ ] Go/no-go decision recorded with open risks and owners

Verification: Staging drills plus production readbacks.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G21-ga-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
