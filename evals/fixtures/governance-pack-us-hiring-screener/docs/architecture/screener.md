# Design: applicant screener

Status: accepted 2026-09-02 (Kevin Ortiz, Redwood Freight; Priya Raman, Southgate Labs)
Brief: [docs/discovery/screener.md](../discovery/screener.md)
Plan: [docs/plans/screener.md](../plans/screener.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Profile | pilot: California warehouses, 8 weeks | brief §2 |
| Data | real applications from Greenhouse | brief §3 |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI, Cloud Run in us-west1 (Oregon), BigQuery for scores | engineering |
| Out of scope | rejecting applicants; messaging applicants; New York warehouses | brief §6 |

## Requirements

- R1 Score each application 0-100 against the role's requirements.
- R2 Rank applications per requisition and label the bottom group "not recommended".
- R3 Show the requirements behind each score.
- R4 A recruiter makes every rejection.

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | R1, R3 | a score lists the requirements met and missed with the application text behind each | output schema | score withheld | evidenced: local, G02/A1 |
| C2 | R4 | the screener never changes an application's stage in Greenhouse | custom-field-only API scope | refusal | evidenced: local, G03/A2 |
| C3 | R2 | "not recommended" is applied to scores under 40 | code | n/a | evidenced: local, G02/A3 |
| C4 | R1 | age, date of birth, graduation years and photos are removed before scoring | redaction step | application flagged | evidenced: local, G01/A2 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G03/A1 |
| SB03 | Greenhouse API key | Build | G03/A2 |
| SB05 | ADK runtime | Defer | deferred: production |

## Decisions

- D1 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI in us-west1.
- D2 Scores, ranks and labels written to a Greenhouse custom field and to BigQuery.
- D3 Recruiters see the ranked list in Greenhouse; "not recommended" applicants are in a
  collapsed group they can open.
- D4 Southgate Labs engineers in Sydney read the evaluation set (real past applications) and
  logs during the build and a three-month support period.
- D5 Evaluation set: 6,000 past applications with hiring outcomes, names and contact details
  removed.
