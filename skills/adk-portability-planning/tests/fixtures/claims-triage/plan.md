# Implementation plan: claims triage assistant

Status: in progress
Architecture: docs/architecture/claims-triage.md

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Classify a claim end to end | 1 | implementation | 6-10 | D1, D2 | adk-workflow-design | verified_local |
| G02 Coverage note with cited clause | 1 | implementation | 10-16 | G01, D4 | adk-memory-architecture | verified_local |
| G03 Approved write to the claims platform | 1 | implementation | 8-12 | G01, D5 | safe-api-tool-calls | in_progress |
| G04 Journey run before the pilot review | 1 | journey | 3-5 | G01, G02, G03 | adk-agent-evaluation | planned |
| G05 Portability assessment | 1 | portability | 3-5 | design only | adk-portability-planning | ready |

### G01 — Classify a claim end to end

- **Status and evidence:** verified_local. C4 evidenced, local, A1.
  M1: metric triage label accuracy; value 0.88; baseline manual triage sample; window 2026-10-06 to 2026-10-10; sample 150 labelled claims; method adk eval with Gemini judge; owner claims lead; build g01-3

### G02 — Coverage note with cited clause

- **Status and evidence:** verified_local. C1 evidenced, local, A2.
  M2: metric actual hands-on hours for G02; value 14; baseline estimate 10-16; window 2026-10-13 to 2026-10-17; sample 1 goal; method developer log; owner developer; build g02-2

### G05 — Portability assessment

- **Phase and estimate:** 1; hands-on 2-3, review 1-2, total 3-5; calendar waits none; owner developer
- **Outcome, contracts and decisions:** answers the CTO's question (design scope gate) with a separate document; contracts: none
- **Primary skill:** adk-portability-planning
- **Acceptance:**
  - [ ] A1 THE assessment docs/portability/claims-triage.md SHALL exist and check_portability.py SHALL exit 0 with --design and --plan (deliverable)
  - [ ] A2 THE assessment SHALL cover aws and azure and each of the five dimensions (deliverable)
  - [ ] A3 EVERY provider or framework claim that drives a classification or risk SHALL cite an official source with its read date (deliverable)
  - [ ] A4 THE design document SHALL NOT change (deliverable)
  - [ ] A5 THE skill SHALL NOT write application code, infrastructure code or new tickets (deliverable)
