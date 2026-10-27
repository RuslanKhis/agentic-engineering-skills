# Design: Coastline claims assistant

Status: accepted 2026-09-29 (Marta, claims operations; Leon, CTO)
Plan: [docs/plans/claims.md](../plans/claims.md)

## Scope gate

| Question | Answer |
| --- | --- |
| Artifact type | pilot for 300 policyholders, then production |
| People | two developers, ten weeks |
| Stack | Google ADK 2.12.0 (Python) on Cloud Run, Gemini through Vertex AI, Agent Platform sessions and Memory Bank, Firestore for claims, Identity Platform sign-in, `europe-west2` |
| Portability | The CTO asked for a separate assessment of a later move to AWS (G07); the build stays on GCP and ADK |

## Requirements

- R1 A policyholder sees and updates only their own claims.
- R2 A returning policyholder does not have to repeat what they told the assistant in earlier conversations about an open claim.
- R3 Nothing is remembered about a policyholder who declined memory in their account settings.
- R4 Claim decisions are never made or promised by the assistant.

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | a tool returns or changes only the caller's claims | user | Firestore | tool owner check on the verified ID | not found | evidenced: local, G01 |
| C2 | R2 | recall returns only the caller's memories about their open claims | user | Memory Bank scope `{user_id}` | scope set from the verified ID | no recall | planned: G02 |
| C3 | R3 | no memory is generated for a policyholder who declined | user | account setting | write-back callback checks the setting | nothing written | planned: G02 |
| C4 | R4 | no reply contains a payout promise | session | instruction plus output check | after-model check | replaced with a fixed reply | planned: G04 |

## Decisions

- D1 Agent Platform Memory Bank for cross-session recall (R2), scope
  `{user_id: <Identity Platform sub>}`, topics limited to claim facts the
  policyholder stated; `PreloadMemoryTool` for recall.
- D2 Sessions in Agent Platform (`VertexAiSessionService`).
- D3 Claims stay in Firestore; the assistant never writes claim decisions.
- D4 Gemini on Vertex AI, model pinned in configuration.
- D5 Identity from Identity Platform tokens verified in `claims/server.py`.
