# Design: customer agent

Status: accepted 2026-09-09 (Mere Walker, Kowhai Retail; Priya Raman, Southgate Labs)
Brief: [docs/discovery/customer-agent.md](../discovery/customer-agent.md)
Plan: [docs/plans/customer-agent.md](../plans/customer-agent.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Profile | pilot: signed-in web chat customers in NZ and Singapore, 6 weeks | brief §6 |
| Data | real CRM order history | brief §3 |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI, Cloud Run and Firestore in australia-southeast1 (Sydney) | engineering |
| Out of scope | cash refunds; changing orders; marketing messages | brief §2 |

## Requirements

- R1 Answer order and returns questions for the signed-in customer's own orders.
- R2 Issue store credit for an eligible return up to NZD 150 / SGD 130 per order.
- R3 Hand over to a person on request.

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | R1 | a customer reads only their own CRM records | tool scoped to the verified customer ID | refusal | evidenced: local, G01/A2 |
| C2 | R2 | credit is issued only for an eligible return and never above the limit | tool checks eligibility and limit in code | handover | evidenced: local, G02/A1 |
| C3 | R2 | a credit is issued once per return | idempotency key on the return ID | n/a | evidenced: local, G02/A3 |
| C4 | R3 | a handover reaches the service queue in the customer's country | handover tool | callback form | evidenced: local, G03/A1 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G01/A2 |
| SB03 | Salesforce integration credential | Build | G02/A4 |
| SB05 | ADK runtime | Defer | deferred: production |

## Decisions

- D1 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI in australia-southeast1.
- D2 Hosting, Firestore and logs in australia-southeast1 for both countries.
- D3 Transcripts kept 12 months and reused to build evaluation sets.
- D4 Southgate Labs engineers in Sydney read traces (which include CRM fields returned by
  tools) during the pilot and a six-month support period.
- D5 Order history read from Salesforce at the time of the question; no copy is kept.
