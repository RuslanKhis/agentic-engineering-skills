# Design: HR assistant

Status: accepted 2026-09-11 (Luc Tremblay, Érable Logistics; Priya Raman, Southgate Labs)
Brief: [docs/discovery/hr-assistant.md](../discovery/hr-assistant.md)
Plan: [docs/plans/hr-assistant.md](../plans/hr-assistant.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Profile | pilot: one shift per centre, 6 weeks | brief §6 |
| Data | real employee and leave data | brief §3 |
| Stack | Python 3.12, google-adk 2.12.0, Cloud Run and Cloud SQL in northamerica-northeast2 (Toronto), Gemini through Vertex AI | engineering |
| Out of scope | pay; discipline; leave of two days or more | brief §2 |

## Requirements

- R1 Answer HR policy questions in French or English from the published policies.
- R2 Take leave requests and record them in UKG.
- R3 Approve routine leave requests automatically.
- R4 Send all other requests to the employee's manager.

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | R1 | every policy answer cites the policy section | output validator | handover to HR | evidenced: local, G01/A1 |
| C2 | R2 | an employee reads and requests leave only for themselves | tool scoped to the verified employee ID | refusal | evidenced: local, G02/A2 |
| C3 | R3 | a request is auto-approved only when it is under two days, the balance covers it and no blackout date applies | rule in code before the UKG write | sent to the manager | evidenced: local, G03/A1 |
| C4 | R3 | auto-approved requests are written to UKG with approver "HR assistant" and no human review | UKG integration | n/a | evidenced: local, G03/A2 |
| C5 | R4 | every other request reaches the manager's UKG queue | UKG integration | HR notified | evidenced: local, G03/A3 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G02/A2 |
| SB03 | UKG integration credential | Build | G03/A4 |
| SB05 | ADK runtime | Defer | deferred: production |

## Decisions

- D1 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001`, called through the Vertex AI global
  endpoint; the model page lists processing in the United States for this model (read
  2026-09-10).
- D2 Cloud Run, Cloud SQL and logs in northamerica-northeast2 (Toronto).
- D3 Prompts and answers logged for 60 days with the employee ID.
- D4 Southgate Labs engineers in Sydney read logs during the pilot and a three-month support
  period.
- D5 The rule in C3 decides routine requests; the model only extracts dates and leave type from
  the request.
