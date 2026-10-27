# Design: customer service assistant

Status: accepted 2026-09-18 (Laura Whitfield, Thamesbridge; Priya Raman, Southgate Labs)
Brief: [docs/discovery/service-assistant.md](../discovery/service-assistant.md)
Plan: [docs/plans/service-assistant.md](../plans/service-assistant.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Profile | pilot: 6,000 opted-in customers, 8 weeks | brief §6 |
| Data | real account, card and overdraft decision data | brief §3 |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI; UK customers served from europe-west2 (London), Irish and EU customers from europe-west1 (Belgium) | engineering |
| Out of scope | making or changing credit decisions; payments; unfreezing cards | brief §2 |

## Requirements

- R1 Answer balance and transaction questions for the signed-in customer's own accounts.
- R2 Freeze a card after the customer confirms.
- R3 Explain a declined overdraft from the decision engine's reason codes.
- R4 Never decide, promise or change a credit outcome.

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | R1 | a customer reads only their own accounts | tool scoped to the verified customer ID from app sign-in | refusal | evidenced: local, G01/A2 |
| C2 | R2 | a card is frozen only after an explicit confirmation of that card | require_confirmation on freeze_card, bound to the card ID | no freeze | evidenced: local, G02/A1 |
| C3 | R3 | an overdraft explanation uses only the decision engine's reason codes for that application | tool returns codes; output validator | fixed message and handover | evidenced: local, G03/A1 |
| C4 | R4 | the assistant does not say a decision will change or invite a reapplication outcome | output check | fixed message | evidenced: local, G03/A2 |
| C5 | R1 | transcripts are pseudonymised before Southgate Labs can read them | pseudonymisation job | transcript withheld | evidenced: local, G04/A1 |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G01/A2 |
| SB03 | core banking and card credentials | Build | G02/A3 |
| SB05 | ADK runtime | Build | G04/A2 |

## Decisions

- D1 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI, in the serving region.
- D2 UK traffic in europe-west2 (London), Irish and EU traffic in europe-west1 (Belgium);
  logs and traces in the same region as the traffic.
- D3 The assistant explains overdraft declines from reason codes; the credit decision engine
  (vendor CreditLens, run by Thamesbridge) makes every decision.
- D4 Southgate Labs supports the service for six months after launch from Sydney, with
  access to logs, traces and pseudonymised transcripts.
- D5 Card freeze through the card platform API; no unfreeze.
- D6 Customers are told in the chat header that they are talking to the bank's assistant.
