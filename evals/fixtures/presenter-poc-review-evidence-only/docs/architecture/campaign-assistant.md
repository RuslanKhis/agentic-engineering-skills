# Design: campaign shopping assistant

Status: accepted 2026-08-26 (Clare Hollis, Bramble & Birch; Tom Reid, Larkspur Digital)
Brief: [docs/discovery/campaign-assistant.md](../discovery/campaign-assistant.md)
Plan: [docs/plans/campaign-assistant.md](../plans/campaign-assistant.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Artifact type | proof of concept on one campaign, 10% of landing-page traffic | Clare Hollis |
| Time and people | one developer, four weeks | engagement lead |
| Who judges | Clare Hollis and the leadership team, against the success criteria below | Clare Hollis |
| Stack | Python 3.12, google-adk 2.12.0, Gemini through Vertex AI, Cloud Run, the existing Shopify storefront | engineering |

## Success criteria (agreed 2026-08-26, before the build)

| ID | Criterion | Threshold | Measured by |
| --- | --- | --- | --- |
| S1 | Checkout completion on sessions that used the assistant, against the Q2 baseline | at least 3.6 % | web analytics, at least 300 assistant sessions |
| S2 | Refund rate on orders from assistant sessions | not above 6.4 % | order system, 30 days |
| S3 | Answers about size, material and delivery that match the catalogue | at least 95 % on the test set | offline evaluation |
| S4 | Spend for the proof of concept | within £1,500 model and cloud spend | billing export |

## Contracts

| ID | From | Invariant | Enforcement | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | S3 | product answers come from the catalogue entry, with the product link | output validator | "I don't have that detail" with a link to the product page | evidenced: local, G02/A1 |
| C2 | S3 | delivery dates come from the delivery-estimate API for the shopper's postcode | tool | "delivery dates are on the checkout page" | evidenced: local, G02/A2 |
| C3 | S1 | items are added to the basket only when the shopper asks, with size and quantity confirmed | basket tool with confirmation | nothing added | evidenced: local, G03/A1 |
| C4 | S4 | model spend stops at £60 a day | Vertex AI quota | assistant hidden for the day | evidenced: local, G03/A3 |

## Decisions

- D1 Gemini 3.5 Flash pinned as `gemini-3.5-flash-001`.
- D2 Shown on 10 % of campaign landing-page sessions (A/B split by the storefront).
- D3 No customer account data is read; the basket is the storefront's own session basket.
- D4 Campaign briefs (featured products, tone, offer text) are loaded from a campaign file that
  Bramble's e-commerce team edits.
- D5 Production would add every campaign page and the account area (not decided).
- D6 Open: whether Pinwheel Studio, the creative agency, may edit campaign briefs and the
  assistant's offer text directly, without Bramble's sign-off. Owner: Clare Hollis.
