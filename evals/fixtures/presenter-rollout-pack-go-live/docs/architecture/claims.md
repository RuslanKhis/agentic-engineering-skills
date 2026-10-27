# Design: claims triage assistant

Status: accepted 2026-08-06; revised 2026-10-14 for production and the Dublin office
(Helen Okafor, Fenwick Mutual; Tom Reid, Larkspur Digital)
Brief: [docs/discovery/claims.md](../discovery/claims.md)
Plan: [docs/plans/claims.md](../plans/claims.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Artifact type | production for all home-claims triage handlers in Leeds and Dublin | Helen Okafor, 2026-10-14 |
| Data | real claim notifications and policy records (personal data, UK and Ireland) | brief |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI (europe-west2), Cloud Run behind IAP, Cloud SQL for PostgreSQL, BigQuery for claim history (read-only) | engineering |
| Out of scope | motor claims; settling or paying claims; any write to the policy system; contacting customers | brief |

## Requirements

- R1 Draft a triage recommendation (type, urgency, cover position) for a new home claim.
- R2 Cite the policy clause each cover position relies on.
- R3 Handlers see only claims in their team's queue.
- R4 The handler decides; the assistant never changes a claim.
- R5 Spend stays inside the agreed allowance.

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R3 | a handler reads only claims in their team's queue | team | claims queue | API dependency filters by the verified handler's team; the tool rechecks | 404 | evidenced: local, G03/A2 |
| C2 | R2 | every cover position cites a clause from the policy's own wording version, or says none found | claim | policy wording | output validator | draft withheld, handler triages by hand | evidenced: local, G02/A1 |
| C3 | R4 | the assistant never changes a claim's status or routes a claim | claim | claims system | no write tool bound; read-only credential | refusal | evidenced: local, G02/A3 |
| C4 | R1 | claim notes reach the model only after de-identification | claim | SDP | de-identify step before the model call | draft withheld | evidenced: local, G01/A2 |
| C5 | R5 | model and BigQuery spend stop at the daily cap | project | quota | Vertex AI quota; BigQuery maximum bytes billed | "drafts are paused for today" banner | evidenced: local, G04/A2 |
| C6 | R1 | urgency "high" is shown only for the claim types in the urgency table (escape of water, fire, uninhabitable home) | claim | urgency table | code after the model | urgency left blank for the handler | evidenced: local, G09/A1 |
| C7 | R4 | a handler can report a wrong draft from the draft view | handler | feedback table | "report a problem" control writes a feedback record | message to the team lead | evidenced: local, G10/A1 |

## Decisions

- D1 A draft for a person to accept, not an automated decision.
- D2 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001`.
- D3 Policy cover read through the policy system's read-only API.
- D7 Dublin handlers use the same service; Irish policy wordings are indexed alongside UK ones.

## Deferred controls and known limits

- Motor claims and commercial policies are not supported.
- Claims lodged before 2024 have no claim history in BigQuery.
- Handwritten attachments are not read; the draft says "attachment not read".
