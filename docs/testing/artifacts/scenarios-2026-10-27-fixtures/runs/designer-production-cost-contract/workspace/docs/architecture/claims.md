# Design: claims triage assistant

Status: accepted 2026-10-06 (Helen Okafor, Fenwick Mutual; Tom Reid, Larkspur Digital); phase 1 complete 2026-10-23
Production version (draft, 2026-10-27): [claims-production.md](claims-production.md); it supersedes C5 and widens C4
Brief: [docs/discovery/claims.md](../discovery/claims.md)
Plan: [docs/plans/claims.md](../plans/claims.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Artifact type | proof of concept with four triage handlers on new home claims | brief |
| Time and people | two Larkspur developers, about 30 h each of agent-assisted work | engagement lead |
| Who judges | Helen Okafor against the brief's outcome and counter-metric | brief |
| Data | real claim notifications and policy records (personal data) | brief |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI (europe-west2), Cloud Run behind IAP, Cloud SQL for PostgreSQL for sessions, BigQuery for claim history (read-only) | engagement lead |
| Out of scope | motor claims; settling or paying claims; any write to the policy system | brief |

## Requirements

- R1 Draft a triage recommendation (type, urgency, cover position) for a new home claim.
- R2 Cite the policy clause each cover position relies on.
- R3 Handlers see only claims in their team's queue.
- R4 The handler decides; the assistant never changes a claim.
- R5 Spend stays inside the pilot allowance.

## Components

- Handler web view (React SPA) served by the FastAPI service on Cloud Run; identity from IAP.
- ADK agent in process: `draft_triage` flow with tools `get_policy` (policy API, read-only),
  `claim_history` (BigQuery, parameterised read of the claimant's previous claims) and
  `search_wording` (policy wording index).
- Cloud SQL for PostgreSQL: ADK `DatabaseSessionService` and the handler decisions table.
- Sensitive Data Protection de-identification of claim notes before the model call.

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R3 | a handler reads only claims in their team's queue | team | claims queue | API dependency filters by the verified handler's team; the tool rechecks the claim's team | 404 | evidenced: local, G03/A1, G03/A2 |
| C2 | R2 | every cover position cites a clause from the policy's own wording, or says none found | claim | policy wording | output validator rejects an uncited position | draft withheld, handler triages by hand | evidenced: local, G02 |
| C3 | R4 | the assistant never changes a claim's status | claim | claims system | no write tool bound; policy API credential is read-only | refusal | evidenced: local, G02 |
| C4 | R1 | claim notes reach the model only after de-identification | claim | SDP | de-identify step before the model call | draft withheld | evidenced: local, G01/A2 |
| C5 | R5 | model and BigQuery spend stop at the daily cap | project | quota | Vertex AI quota; BigQuery maximum bytes billed | refusal with fixed message | evidenced: local, G04 (configuration only; no live overrun) |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G03/A2 |
| SB03 | policy API credential | Build | G02/A3 |
| SB05 | ADK runtime | Defer | deferred: production |

## Decisions

- D1 A draft for a person to accept, not an automated decision (brief, technology fit).
- D2 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001`; judge pinned as `gemini-3.5-pro-001`.
- D3 Policy cover read through the policy system's read-only API, never a copy of the database.
- D4 Claim history from BigQuery with a parameterised query and maximum bytes billed.
- D5 The pilot runs in Fenwick Mutual's GCP project `fm-claims-pilot` in europe-west2.

## Journey

A handler opens a new escape-of-water claim, sees the draft with urgency "high", the cover
position citing section 3.2 of the wording, accepts it, and the claim routes to the
property team; a handler from another team cannot open it.
