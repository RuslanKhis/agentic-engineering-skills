# Implementation plan: claims triage assistant pilot

Status: ready goals identified
Architecture: [docs/architecture/claims.md](../architecture/claims.md)
Continuation source of truth: this plan

## Summary for the reader

- **Profile and phase 1:** pilot; phase 1 gives 14 triage handlers a draft triage
  recommendation with cited cover on new home claims, ending in the pilot approval review.
- **Effort and finish:** 21-33 human hours, agent-assisted, against 45 h capacity (two
  developers, 30 h each, reserve 25 %); finish 11-20 working days including waits W1 and W2.
- **Largest risks:** the policy API credential arriving late (W1, owner Raj Mehta); uncited
  cover positions (C2, G02); de-identification missing free-text names (C4, G01).
- **Decisions needed from you:** the date of the pilot approval review.
- **Next prompt:** `/adk-engineer Carry out G01 from docs/plans/claims.md.`

## Destination and constraints

Handlers on new home claims get a draft they accept or change; nothing writes to the policy
or claims systems (C3). Accepted stack and pins as in the design (D2, D5). Inspected
repository: none yet; module paths below are proposed.

## Delivery profile and capacity

Profile: pilot.

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | triage drafts for pilot handlers, approval review | G01 to G06 | 21-33 | 2 × 30 h × 0.75 = 45 h |
| 2, harden | production readiness after the pilot decision | later | not estimated | after the review |

| Person or role | Goals | Hours | Their capacity |
| --- | --- | --- | --- |
| Dev A (Tom Reid) | G01, G02, G05 | 11-16 | 22.5 h |
| Dev B (Sara Lin) | G03, G04, G06 | 10-17 | 22.5 h |

Schedule block:

```yaml
- goal: G01
  phase: 1
  hands_on: 3-4
  review: 1-1.5
  total: 4-5.5
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C4]
  security: []
  mentions_only: []
  type: implementation
  status: planned
- goal: G02
  phase: 1
  hands_on: 3-5
  review: 1-1.5
  total: 4-6.5
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: W1 policy API read-only credential from the policy systems manager
  wait_days: 5-10
  handoff: 0
  contracts: [C2, C3]
  security: [SB03]
  mentions_only: []
  type: implementation
  status: planned
- goal: G03
  phase: 1
  hands_on: 3-4
  review: 1-1.5
  total: 4-5.5
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1]
  security: [SB01]
  mentions_only: []
  type: implementation
  status: planned
- goal: G04
  phase: 1
  hands_on: 2-3.5
  review: 1-1.5
  total: 3-5
  owner: Dev B
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C5]
  security: []
  mentions_only: []
  type: implementation
  status: planned
- goal: G05
  phase: 1
  hands_on: 2-3
  review: 1
  total: 3-4
  owner: Dev A
  blocked_by: [G02, G04]
  calendar_waits: none
  wait_days: 0
  handoff: 1-2
  contracts: [C1, C2, C3, C4, C5]
  security: [SB01, SB03]
  mentions_only: []
  type: journey
  status: planned
- goal: G06
  phase: 1
  hands_on: 2-4
  review: 1-2.5
  total: 3-6.5
  owner: Dev B
  blocked_by: [G05]
  calendar_waits: W2 client security review before the pilot approval
  wait_days: 3-5
  handoff: 0.5-1
  contracts: []
  security: []
  mentions_only: []
  type: presentation
  status: planned
```

## Implementation map

| Contract / decision | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| C4, D1 | `app/deidentify.py` before the agent's model call; `app/agent.py` draft flow (proposed) | Sensitive Data Protection | protect-adk-sensitive-data | canary test, local |
| C2, C3, D3 | `get_policy`, `search_wording` tools; output validator (proposed) | none | adk-tool-interface-design | citation test, local |
| C1 | FastAPI dependency and queue route (proposed) | IAP | adk-fastapi-backend | owner test, local |
| C5, D4 | `claim_history` tool with maximum bytes billed; Vertex AI quota | BigQuery, Vertex AI | adk-operational-guardrails | config test, local |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Triage draft from a de-identified notification | 1 | implementation | 4-5.5 | none | protect-adk-sensitive-data | ready |
| G02 Cover position with the clause it relies on | 1 | implementation | 4-6.5 | G01, W1 | adk-tool-interface-design | blocked: W1 |
| G03 Handler queue scoped to the team | 1 | implementation | 4-5.5 | none | adk-fastapi-backend | ready |
| G04 Claim history and the daily spend stop | 1 | implementation | 3-5 | G03 | adk-operational-guardrails | proposed |
| G05 Journey check | 1 | journey | 3-4 | G02, G04 | adk-agent-evaluation | proposed |
| G06 Pilot approval presentation | 1 | presentation | 3-6.5 | G05, W2 | adk-presenter | proposed |

### G01 — Triage draft from a de-identified notification

- **Phase and estimate:** 1; hands-on 3-4, review and verify 1-1.5, total 4-5.5; calendar waits none; owner Dev A
- **Outcome, contracts and decisions:** a handler sees a draft type and urgency for a new home claim; C4; D1
- **Scope:** notification parsing, de-identification, draft schema; not cover (G02)
- **Depth:** pilot depth; floor kept (no secrets in code, pinned model, a person accepts every draft)
- **Implementation route:** `app/deidentify.py` (SDP de-identify template), `app/agent.py` LlmAgent with an output schema
- **Resources created:** none
- **Prerequisites:** none
- **Primary skill:** protect-adk-sensitive-data
- **Supporting skills:** adk-model-and-output-contracts (draft schema)
- **Companion skills:** none
- **Design system:** none
- **Security rules:** none
- **Acceptance:** A1 WHEN a notification arrives THE app SHALL return a draft with type and urgency (C4); A2 IF a note contains a name, phone or email THEN THE model request SHALL NOT contain it (C4)
- **Verification:** `python -m unittest tests.test_draft` with a recorded model double; offline
- **Execution scope:** local only
- **Status and evidence:** planned

### G03 — Handler queue scoped to the team

- **Phase and estimate:** 1; hands-on 3-4, review and verify 1-1.5, total 4-5.5; calendar waits none; owner Dev B
- **Outcome, contracts and decisions:** a handler sees only their team's claims; C1
- **Resources created:** Cloud SQL for PostgreSQL `fm-claims-pilot-sql` (db-custom-1-3840, 10 GB SSD, europe-west2, no HA); idle cost about £1.60 per day (pricing page read 2026-10-05, https://cloud.google.com/sql/pricing); cleanup `deploy/delete_sql.sh --project fm-claims-pilot --instance fm-claims-pilot-sql`; absence verified with `gcloud sql instances list --project fm-claims-pilot`; owned by the cost contract (Later)
- **Primary skill:** adk-fastapi-backend
- **Supporting skills:** adk-tool-auth-and-secrets (tool-hop recheck of the claim's team)
- **Acceptance:** A1 WHEN a handler opens the queue THE app SHALL list only their team's claims (C1); A2 IF a handler requests another team's claim THEN THE app SHALL return 404 (C1, SB01)
- **Status and evidence:** planned

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Motor claims | home pilot meets its threshold | none | adk-system-designer |
| Recurring cost review | first monthly bill of the pilot project | spend drifts unnoticed for a month | adk-agent-observability |
| Decommission: delete `fm-claims-pilot-sql`, the BigQuery dataset `claims_pilot` and the Cloud Run service; backups retained 7 days | pilot stops or moves to production | idle Cloud SQL cost continues if forgotten | deploy-adk-on-google-cloud |
| Production hardening (SB05, HA database, alerting) | pilot approval | pilot runs without HA | adk-system-designer |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/claims.md | Method and accepted decisions |
| this plan | Remaining limits and deferred controls |

## Resume here

- **Next goal:** G01 Triage draft from a de-identified notification (no prerequisites)
- **Continuation prompt:** `/adk-engineer Carry out G01 from docs/plans/claims.md.`
