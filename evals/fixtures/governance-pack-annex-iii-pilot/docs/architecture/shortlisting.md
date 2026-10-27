# Design: shortlisting assistant

Status: accepted 2026-09-04 (Femke Jansen, Kestrel; Priya Raman, Southgate Labs)
Brief: [docs/discovery/shortlisting.md](../discovery/shortlisting.md)
Plan: [docs/plans/shortlisting.md](../plans/shortlisting.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Profile | pilot: 3 recruiters, warehouse and driver vacancies, 8 weeks | brief §3 |
| Data | real applicant CVs from the ATS | brief §4 |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI, Cloud Run in europe-west4 (Netherlands), Cloud SQL for PostgreSQL in europe-west4 | engineering |
| Out of scope | sending messages to applicants; any change to an applicant's ATS status | brief §5 |

## Requirements

- R1 Rank the applicants for a vacancy against its must-have requirements.
- R2 Give a rationale per applicant that cites the CV passages it relies on.
- R3 Recruiters see only vacancies they own.
- R4 The recruiter decides who is shortlisted; the assistant changes nothing in the ATS.
- R5 The ranking does not use age, nationality, gender, health or family status.

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | R3 | a recruiter reads only vacancies and CVs they own | API dependency on the verified recruiter; tool rechecks ownership | 404 | evidenced: local, G02/A2 |
| C2 | R2 | every rationale cites passages from the applicant's own CV | output validator | rationale withheld | evidenced: local, G03/A1 |
| C3 | R4 | no write to the ATS | ATS credential is read-only; no write tool bound | refusal | evidenced: local, G02/A3 |
| C4 | R5 | dates of birth, photos, nationality and marital status are removed before the model sees a CV | redaction step before the model call | CV skipped and flagged | evidenced: local, G01/A2 |
| C5 | R1 | the ranking is shown with the vacancy's requirement each applicant meets or misses | output schema | ranking withheld | evidenced: local, G03/A2 |
| C6 | R4 | an applicant ranked in the bottom half is still visible in the list with its rationale | UI shows the full list | n/a | planned: G04 |
| C7 | R5 | adverse impact by age band and gender is measured before each pilot phase | evaluation job (G05) | pilot paused | evidenced: offline, M3 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G02/A2 |
| SB03 | ATS credential | Build | G02/A3 |
| SB05 | ADK runtime | Defer | deferred: production |

## Decisions

- D1 A ranked list with rationales for a recruiter to act on; no automatic rejection.
- D2 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI, endpoint in europe-west4.
- D3 Applicant data stays in Kestrel's GCP project `kestrel-talent-pilot` (europe-west4).
- D4 Prompts and responses are logged for 14 days for debugging; traces keep no CV text.
- D5 Southgate Labs engineers in Sydney have read access to logs and to the evaluation set
  during the pilot and the six-week support period that follows.
- D6 The evaluation set is 1,400 past applications with recruiter decisions (2024-2026),
  pseudonymised by removing names and contact details.
- D7 Recruiters see a rank and a rationale; they can open every CV.

## Accepted risks and deferred controls

- Ranking from free-text CVs may still pick up age signals through graduation years and
  career length (C4 removes explicit dates of birth only).
