# Design: Tidewater claims assistant

Status: accepted 2026-09-22 (Joanne Price, Head of Claims; Martin Cole, CTO; Tom Reid, Larkspur Digital)
Plan: [docs/plans/claims.md](../plans/claims.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Artifact type | production service for 40,000 policyholders, after a pilot | Joanne Price |
| People and time | two developers, twelve weeks | engagement lead |
| Stack | Python 3.12, google-adk 2.12.0 on Cloud Run (europe-west2); Gemini through Vertex AI; Agent Platform sessions and Memory Bank; Vertex AI Search over policy wordings; Firestore for claims; Identity Platform sign-in | engagement lead |
| Portability | a concern: the CTO wants to know what a later move to AWS would involve. Targets: AWS and Azure. Framework to compare: LangGraph. The build stays on GCP and ADK. | Martin Cole, 2026-09-18 |
| Out of scope | claim decisions and payments | Joanne Price |

## Requirements

- R1 A policyholder sees and updates only their own claims.
- R2 A returning policyholder does not repeat what they told the assistant about an open claim.
- R3 Policy questions are answered from the policyholder's own policy wording, with the clause.
- R4 Photos uploaded to a claim are stored with the claim.
- R5 The assistant never makes or promises a claim decision.
- R6 Spend stays within the monthly ceiling the sponsor accepted.

## Components

- Web chat in the customer portal (React), served by the FastAPI service on Cloud Run.
- ADK agent (`claims/agent.py`) with tools `get_claim`, `add_note`, `upload_photo`,
  `search_wording`, and `PreloadMemoryTool`.
- Agent Platform: `VertexAiSessionService` and `VertexAiMemoryBankService`.
- Vertex AI Search data store over policy wordings (one document per product version).
- Firestore: claims, notes and photo metadata; Cloud Storage for photos.
- Identity Platform: sign-in; the verified `sub` is the user ID.

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | a tool returns or changes only the caller's claims | user | Firestore | owner check on the verified ID in each tool | not found | evidenced: local, G01/A2 |
| C2 | R2 | recall returns only the caller's memories | user | Memory Bank scope `{user_id}` | scope from the verified ID | no recall | evidenced: local, G02/A2 |
| C3 | R3 | answers cite a clause from the caller's policy version | claim | Vertex AI Search filter on product version | filter in `search_wording` | "I couldn't find that in your policy" | planned: G03 |
| C4 | R4 | a photo is stored only on the caller's claim | user | Cloud Storage path from claim ID | tool check | refusal | planned: G04 |
| C5 | R5 | no reply contains a payout promise | session | output check | after-model callback | fixed reply | planned: G05 |
| C6 | R6 | model spend stops at the daily cap | project | Vertex AI quota | quota | refusal | planned: G06 |

## Decisions

- D1 Agent Platform Memory Bank for cross-session recall, scope `{user_id}`, recalled with
  `PreloadMemoryTool`.
- D2 Agent Platform sessions (`VertexAiSessionService`).
- D3 Vertex AI Search for policy wordings, filtered by product version.
- D4 Firestore for claims and notes; Cloud Storage for photos.
- D5 Gemini 3.5 Flash on Vertex AI, pinned as `gemini-3.5-flash-001`.
- D6 Cloud Run behind the existing external load balancer; Identity Platform for sign-in.
