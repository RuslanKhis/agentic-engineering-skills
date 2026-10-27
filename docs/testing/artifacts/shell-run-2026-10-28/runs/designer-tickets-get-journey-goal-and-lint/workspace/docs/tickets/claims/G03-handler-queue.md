---
goal: G03
title: Handler queue scoped to the team
design: docs/architecture/claims.md
plan: docs/plans/claims.md
primary_skill: adk-fastapi-backend
supporting_skills: [adk-tool-auth-and-secrets (tool-hop recheck of the claim's team)]
docs: []
blocked_by: []
touches: [app/main.py, app/queue.py, app/auth.py, web/, deploy/create_sql.sh, deploy/delete_sql.sh, tests/test_queue.py, AGENTS.md]
parallel_safe: yes
contracts: [C1]
companion_skills: [shadcn, react-router]
security: [SB01]
design_system: docs/design/DESIGN.md
contract_deltas: [none]
pass_to_pass: []
phase: 1
type: implementation
profile: MVP or pilot
estimate:
  hands_on: 3-4
  review_and_verify: 1-1.5
  total: 4-5.5
  handoff: none
  calendar_waits: none
owner: Dev B (Sara Lin)
status: ready
---

# G03 Handler queue scoped to the team

## Outcome

A handler sees only their team's claims in the queue view; another team's claim returns 404. Implements R3.

## Scope

- In: FastAPI dependency that reads the IAP-verified handler and filters the queue by team; queue route under `/api`; React SPA with two routes (queue, claim); handler decisions table in Cloud SQL; the tool-hop recheck of the claim's team.
- Out: draft content (G01, G02); claim history and spend stop (G04).
- Depth: pilot depth; floor kept. SB01 built here; SB05 deferred to production hardening (Later).

## Constraints

Identity from IAP; stack and pins as in the design (D5) and AGENTS.md. This ticket writes the plan's web-stack companion table into AGENTS.md. The react-router pin is "to be chosen" in the plan: choose it here, record it in AGENTS.md as a ruling, and install nothing beyond what the pin names.

## Resources created

- Cloud SQL for PostgreSQL `fm-claims-pilot-sql` (db-custom-1-3840, 10 GB SSD, europe-west2, no HA) in `fm-claims-pilot`; idle cost about £1.60 per day (pricing page read 2026-10-05, https://cloud.google.com/sql/pricing); cleanup `deploy/delete_sql.sh --project fm-claims-pilot --instance fm-claims-pilot-sql`; absence verified with `gcloud sql instances list --project fm-claims-pilot`; lifetime owned by the Later item "Decommission" in the plan. The delete script is written and tested here beside the create script. Creating the instance is a paid cloud action: do it only with the owner's go-ahead; tests run against a local PostgreSQL or an in-memory double.

## Acceptance

- [ ] A1 WHEN a handler opens the queue THE app SHALL list only their team's claims (C1)
- [ ] A2 IF a handler requests another team's claim THEN THE app SHALL return 404 (C1, SB01)
- [ ] A3 IF the claim tool is called for a claim outside the caller's team THEN THE tool SHALL refuse (C1)
- [ ] A4 THE deletion script SHALL exist and its dry run SHALL name the instance and project in this ticket's Resources line (floor)

Verification, automated: `python -m unittest tests.test_queue` on Python 3.12 with a stub IAP identity; offline; expected exit code 0.
Verification, manual: UI check against docs/design/DESIGN.md by Dev A or Helen Okafor. The agent never ticks it.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/claims/G03-handler-queue.md. Read its design and plan,
use its primary and supporting skills and its companion skills at the pins
in AGENTS.md, keep its constraints and security rules, run its
verification locally, fill in the Evidence section and set status
(verified_local when every
acceptance case that can run offline has run here, in_progress with the owed
run named when the SDK is absent, verified_live after the authorised run,
done only when every acceptance item has fresh evidence and the owner
accepts). If Evidence starts with a Progress block, resume from it. Leave
changes uncommitted.
```
