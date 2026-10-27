# Implementation plan: shortlisting assistant pilot

Status: in progress
Architecture: [docs/architecture/shortlisting.md](../architecture/shortlisting.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Redacted CV intake | 1 | implementation | 4-6 | none | protect-adk-sensitive-data | verified_local |
| G02 Recruiter-scoped vacancies, read-only ATS | 1 | implementation | 4-5 | none | adk-fastapi-backend | verified_local |
| G03 Ranking with cited rationales | 1 | implementation | 6-9 | G01, G02 | adk-model-and-output-contracts | verified_local |
| G04 Full list in the recruiter view | 1 | implementation | 3-4 | G03 | adk-frontend-integration | in_progress |
| G05 Offline evaluation and adverse impact | 1 | journey | 4-6 | G03 | adk-agent-evaluation | verified_local |
| G06 Governance papers | 1 | governance | 4-6 | G05 | adk-governance-pack | ready |
| G07 Pilot decision presentation | 1 | presentation | 2-3 | G06, W2 | adk-presenter | planned |

## Calendar waits

- W1: works council consultation on the pilot (ondernemingsraad and Betriebsrat); requested
  2026-10-02 by Femke Jansen; no date yet.
- W2: DPIA sign-off by the DPO before the first live vacancy.

## Measurement records

- M1: metric agreement with recruiter shortlist decisions; value 81%; window 2026-10-01 to 2026-10-10; sample 1,400 past applications (D6); method offline evaluation; owner Southgate Labs; build v0.6.0
- M2: metric rationales citing only the applicant's own CV; value 98.6%; window 2026-10-01 to 2026-10-10; sample 1,400; method citation validator (C2); owner Southgate Labs; build v0.6.0
- M3: metric adverse impact ratio by age band (selection rate of band over highest band); value 0.71 for applicants aged 50 and over, 0.93 to 1.00 for other bands; gender ratio 0.96; window 2026-10-01 to 2026-10-10; sample 1,400; method four-fifths comparison on top-third ranking; owner Southgate Labs; build v0.6.0
- M4: metric median seconds to rank a 120-CV vacancy; value 210; window 2026-10-08 to 2026-10-10; sample 12 vacancies; method load test; owner Southgate Labs; build v0.6.0

## Incident records

- I1: date 2026-10-06; severity 3; effect a test run sent six unredacted CVs (with dates of birth) to the model because the redaction step was skipped on PDF uploads; response PDF uploads disabled; fix redaction applied to all upload types and C4 test extended; status closed 2026-10-07

## Resume here

Next: G06 Governance papers.
