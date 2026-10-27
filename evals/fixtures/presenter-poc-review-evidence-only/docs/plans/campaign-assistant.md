# Implementation plan: campaign shopping assistant proof of concept

Status: phase 1 build complete
Architecture: [docs/architecture/campaign-assistant.md](../architecture/campaign-assistant.md)

## Goals

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Assistant on the campaign page | 1 | implementation | 4-6 | none | adk-frontend-integration | done |
| G02 Catalogue and delivery answers | 1 | implementation | 5-7 | G01 | adk-tool-interface-design | done |
| G03 Basket adds with confirmation; spend stop | 1 | implementation | 3-5 | G02 | adk-operational-guardrails | done |
| G04 Campaign run and measurement | 1 | journey | 3-4 | G03 | adk-agent-evaluation | done |
| G05 Leadership review presentation | 1 | presentation | 3-4 | G04, D6 | adk-presenter | ready |

### G01 Assistant on the campaign page

- A1 WHEN a shopper opens the chat THE page SHALL show the assistant within 2 seconds: passed, local and live, 2026-09-08
- A2 WHEN the session is not in the 10 % split THE page SHALL NOT show the assistant: passed, live, 2026-09-15
- Spend: model £4, cloud £22 (billing export, 2026-09-01 to 2026-09-14)
- actual: 5 h

### G02 Catalogue and delivery answers

- A1 WHEN a shopper asks about size or material THE answer SHALL match the catalogue entry and link it (C1): passed, offline, 2026-09-18 (M3)
- A2 WHEN a shopper asks about delivery THE answer SHALL use the delivery API for their postcode (C2): passed, local, 2026-09-18
- A3 IF the delivery API is down THEN THE assistant SHALL point to the checkout page (C2): not run (the delivery API has no test double for outages yet)
- Spend: model £31, cloud £18 (billing export, 2026-09-15 to 2026-09-21)
- actual: 7 h

### G03 Basket adds with confirmation; spend stop

- A1 WHEN a shopper asks to add an item THE assistant SHALL confirm size and quantity before adding (C3): passed, local, 2026-09-24
- A2 IF the item is out of stock in that size THEN THE assistant SHALL NOT add it (C3): passed, local, 2026-09-24
- A3 WHEN the day's spend reaches £60 THE assistant SHALL be hidden (C4): not run (quota alert verified; hiding the widget at the cap needs the storefront team's flag, not delivered)
- Spend: model £12, cloud £15
- actual: 4 h

### G04 Campaign run and measurement

- Ran on the autumn campaign, 2026-09-29 to 2026-10-19, 10 % of landing-page sessions.
- Spend: model £188, cloud £96 (billing export, 2026-09-29 to 2026-10-19)
- actual: 3.5 h

## Measurement records

- M1: metric checkout completion, sessions that used the assistant; value 4.2%; baseline 3.1% (brief §4, Q2 2026); window 2026-09-29 to 2026-10-19; sample 312 assistant sessions; method web analytics; owner Raj Patel; build v0.4.0
- M2: metric checkout completion, campaign sessions without the assistant (same campaign); value 3.4%; window 2026-09-29 to 2026-10-19; sample 27,600 sessions; method web analytics; owner Raj Patel; build n/a
- M3: metric catalogue-matching answers on the test set; value 96.5%; window 2026-09-16 to 2026-09-18; sample 200 questions; method offline evaluation; owner Larkspur Digital; build v0.3.2
- M4: metric refund rate on campaign orders; value 1 of 13 orders from assistant sessions, 6.3% of 938 orders from sessions without it; baseline 6.4% (brief §4); window 2026-09-29 to 2026-10-19 orders, refunds to 2026-10-24; sample 951 orders; method order system; owner Raj Patel; build v0.4.0
- M5: metric total proof-of-concept spend; value £386 (model £235, cloud £151); window 2026-09-01 to 2026-10-24; method billing export filtered by label app=campaign-assistant; owner Larkspur Digital

## Open decisions

- D6 agency delegation (see the design): open, owner Clare Hollis.

## Resume here

Next: G05 leadership review presentation (business audience, 15 minutes).
