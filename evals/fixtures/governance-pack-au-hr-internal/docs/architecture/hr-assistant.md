# Design: staff HR assistant

Status: accepted 2026-09-24 (Marcus Bell, Wattle & Co; Priya Raman, Southgate Labs)
Brief: [docs/discovery/hr-assistant.md](../discovery/hr-assistant.md)
Plan: [docs/plans/hr-assistant.md](../plans/hr-assistant.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Profile | pilot: 300 staff and 25 managers in NSW stores, 6 weeks | brief §6 |
| Data | real Workday leave, roster and attendance data | brief §3 |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI, Cloud Run in australia-southeast1, staff sign-in through Wattle's Entra ID | engineering |
| Out of scope | approving or changing leave; any write to Workday | brief §2 |

## Requirements

- R1 A staff member can ask about their own leave balance, roster and HR policy.
- R2 A manager can ask about the leave and attendance of people who report to them.
- R3 Nobody sees another person's data unless they manage them.
- R4 The assistant never changes leave or rosters.

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | R3 | a staff member reads only their own Workday records | tool scoped to the verified employee ID | refusal | evidenced: local, G02/A2 |
| C2 | R2, R3 | a manager reads only direct and indirect reports | Workday supervisory org check in the tool | refusal | evidenced: local, G02/A3 |
| C3 | R4 | no Workday write | read-only integration user; no write tool | refusal | evidenced: local, G02/A4 |
| C4 | R1 | union membership and medical details are masked in logs | masking step before logging | entry dropped | partially evidenced: M2 |
| C5 | R2 | an attendance summary lists the records it is built from | output schema | summary withheld | evidenced: local, G03/A1 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G02/A2 |
| SB03 | Workday integration credential | Build | G02/A4 |
| SB05 | ADK runtime | Defer | deferred: production |

## Decisions

- D1 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI in australia-southeast1.
- D2 Cloud Run, Cloud SQL and logs in australia-southeast1 (Sydney).
- D3 Prompts and answers logged for 30 days in Cloud Logging for support and quality review.
- D4 Application errors, including request and response bodies, go to the Sentry project
  `wattle-hr` hosted in Sentry's US region.
- D5 Southgate Labs engineers in Sydney read logs and Sentry during the pilot and a
  three-month support period.
- D6 Managers can ask for "a summary of <name>'s attendance this quarter", which the
  manager guide suggests before a performance conversation.
- D7 Staff sign in through Entra ID; the employee ID comes from the verified token.

## Accepted risks and deferred controls

- Masking (C4) uses a phrase list; its coverage is measured in M2.
