# Implementation plan: claims triage assistant pilot

Status: phase 1 complete; pilot live since 2026-08-25
Architecture: [docs/architecture/claims.md](../architecture/claims.md)
Continuation source of truth: this plan

## Summary for the reader

- **Profile and phase 1:** pilot; 14 triage handlers on new home claims since 2026-08-25.
- **Decision:** pilot approved by Helen Okafor on 2026-08-20; monthly value reports to the
  decider from September.

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Triage draft from a de-identified notification | 1 | implementation | 4-5.5 | none | protect-adk-sensitive-data | done |
| G02 Cover position with the clause it relies on | 1 | implementation | 4-6.5 | G01, W1 | adk-tool-interface-design | done |
| G03 Handler queue scoped to the team | 1 | implementation | 4-5.5 | none | adk-fastapi-backend | done |
| G04 Claim history and the daily spend stop | 1 | implementation | 3-5 | G03 | adk-operational-guardrails | done |
| G05 Journey check | 1 | journey | 3-4 | G02, G04 | adk-agent-evaluation | done |
| G06 Pilot approval presentation | 1 | presentation | 3-6.5 | G05, W2 | adk-presenter | done |
| G07 Usage and cost reporting | 2 | implementation | 2-3 | G06 | adk-agent-observability | done |
| G08 Monthly value report, September | 2 | presentation | 1-2 | G07 | adk-presenter | ready |

## Measurement records

- M1: metric median triage time per claim; value 21 minutes; window 2026-08-01 to 2026-08-22; sample 400 new home claims; method claims MI report; owner claims MI analyst; kind baseline
- M2: metric median triage time on pilot claims; value 13 minutes; window 2026-09-01 to 2026-09-30; sample 1,184 pilot claims; method claims MI report; owner claims MI analyst; build v1.0.3
- M3: metric re-routing rate after triage on pilot claims; value 8.6%; baseline 9% (brief §4); window 2026-08-25 to 2026-08-31; sample 236 pilot claims; method claims MI report; owner claims MI analyst; build v1.0.1
- M4: metric drafts accepted without change; value 69%; window 2026-09-01 to 2026-09-30; sample 1,184 drafts; method decisions table; owner Larkspur Digital; build v1.0.3
- M5: metric active handlers (opened a draft on 5 or more claims in a week, every week of the month); value 12 of 14; window 2026-09-01 to 2026-09-30; sample all pilot handlers; method decisions table; owner Larkspur Digital; build v1.0.3
- M6: metric pilot cost (Vertex AI, Cloud Run, Cloud SQL, BigQuery); value £512; window 2026-09-01 to 2026-09-30; sample billing export rows labelled app=claims-triage; method Cloud Billing export to BigQuery; owner Larkspur Digital; build v1.0.3
- M7: metric pilot claims triaged with a draft; value 1,184; window 2026-09-01 to 2026-09-30; sample all pilot claims; method decisions table; owner Larkspur Digital; build v1.0.3
- M8: metric estimated cost per claim at full home volume (4,800 claims a month); value £0.31; method projected from M6 assuming fixed costs unchanged; kind assumption

## Incident records

- I1: date 2026-09-16; severity 2; effect 37 drafts cited a clause from a superseded wording version; response drafts withheld for two hours and handlers triaged by hand; fix wording index rebuilt with a version filter and a C2 test for superseded wordings; status closed 2026-09-19

## Resources created

- Cloud SQL for PostgreSQL `fm-claims-pilot-sql`: retained: pilot running; cleanup: `deploy/delete_sql.sh --project fm-claims-pilot --instance fm-claims-pilot-sql`; verified: listed 2026-10-01

## Change log

| Date | Change | By |
| --- | --- | --- |
| 2026-08-20 | Pilot approved (G06) | Helen Okafor |
| 2026-08-25 | Pilot live for 14 handlers | Tom Reid |
| 2026-10-02 | Usage and cost records added (G07) | Sara Lin |

## Resume here

Next: G08, September value report.
