# Design: public enquiries assistant

Status: accepted 2026-09-15 (Ruth Abbott, NSW Trades Licensing Office; Priya Raman, Southgate Labs)
Brief: [docs/discovery/enquiries.md](../discovery/enquiries.md)
Plan: [docs/plans/enquiries.md](../plans/enquiries.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Profile | pilot: web chat on the application pages, 6 weeks | brief §6 |
| Data | real application status data and public transcripts | brief §3 |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI, Cloud Run, Firestore and Cloud Logging in australia-southeast1 (Sydney) | engineering |
| Out of scope | deciding or changing applications; payments | brief §2 |

## Requirements

- R1 Answer licensing questions from the Office's published guidance only, with a link.
- R2 Give an application's status only to a caller who supplies its number and the applicant's
  date of birth.
- R3 Hand the conversation to the contact centre on request or when the assistant cannot answer.

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | R1 | every answer cites a published guidance page | output validator | handover message | evidenced: local, G01/A1 |
| C2 | R2 | status is returned only when number and date of birth match | lookup tool | "we couldn't find that application" | evidenced: local, G02/A2 |
| C3 | R2 | three failed lookups in a session block further lookups | tool counter in session state | handover | evidenced: local, G02/A3 |
| C4 | R3 | a handover request reaches the contact-centre queue | handover tool | callback form | evidenced: local, G03/A1 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G02/A2 |
| SB03 | licensing system credential | Build | G02/A4 |
| SB05 | ADK runtime | Build | G04/A2 |

## Decisions

- D1 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI in australia-southeast1.
  Model page read 2026-10-20: retirement date 2027-02-26.
- D2 Hosting, Firestore and logs in australia-southeast1.
- D3 Chat transcripts kept 90 days in Firestore for quality review, then deleted.
- D4 Google's abuse monitoring for Vertex AI applies with the project's default settings;
  where that processing happens is not recorded.
- D5 Southgate Labs supports the pilot from Sydney and from Brisbane (one support engineer),
  with access to transcripts and logs.
- D6 The service is procured under the NSW ICTA (Core& not used); Order Form summary in
  `docs/contract/order-form-summary.md`.
