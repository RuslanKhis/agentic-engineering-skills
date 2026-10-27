# Design: claims triage assistant

Status: accepted 2026-09-19 (Helen Park, CCO; Priya Raman, Southgate Labs)
Brief: [docs/discovery/claims-triage.md](../discovery/claims-triage.md)
Plan: [docs/plans/claims-triage.md](../plans/claims-triage.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Profile | pilot: 20 officers, 8 weeks | brief §6 |
| Data | real claims including sensitive health information | brief §3 |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI, Cloud Run and Cloud SQL in australia-southeast1, officer sign-in through the CCO's identity provider | engineering |
| Out of scope | determining liability or payment; contacting claimants | brief §2 |

## Requirements

- R1 Draft a triage recommendation (category, priority, missing evidence) for a new claim.
- R2 Show the claim passages each part of the draft relies on.
- R3 Officers see only claims in their team's queue.
- R4 The officer accepts or changes every draft; the assistant records nothing in the case.

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | R3 | an officer reads only claims in their team's queue | tool scoped to the verified officer's team | refusal | evidenced: local, G02/A2 |
| C2 | R2 | each draft field cites claim passages | output validator | draft withheld | evidenced: local, G01/A2 |
| C3 | R4 | the assistant writes nothing to the case system | read-only service account | refusal | evidenced: local, G02/A3 |
| C4 | R4 | the officer's accept or change is recorded with the draft | decisions table | n/a | evidenced: local, G03/A1 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G02/A2 |
| SB03 | case system credential | Build | G02/A3 |
| SB05 | ADK runtime | Defer | deferred: production |

## Decisions

- D1 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI in australia-southeast1.
- D2 Hosting, database and logs in australia-southeast1; the environment is assessed against
  PROTECTED by the CCO's security team.
- D3 Prompts and drafts logged for 30 days.
- D4 Southgate Labs supports the pilot from Sydney with access to logs and the evaluation set.
- D5 Evaluation set: 900 past claims with officer decisions, names and identifiers removed.
