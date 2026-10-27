---
document: impact-assessment
system: Thamesbridge customer service assistant
version: design accepted 2026-09-18, build v0.8.0
status: draft
jurisdictions: [au, eu, uk]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: UK DPO (Oliver Grant), Ireland DPO (Siobhán Kelly) and group CISO (Rachel Adeyemi), with Laura Whitfield as risk owner
trigger: pilot decision on 2026-12-03 at the Customer Operations Committee (G06)
sources: docs/discovery/service-assistant.md, docs/architecture/service-assistant.md, docs/plans/service-assistant.md, docs/governance/service-assistant/regulatory-memo.md
---

# AI system impact assessment: Thamesbridge customer service assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 and mapped to NIST AI RMF 1.0 and NIST AI 600-1 (the ISO text was not available; headings are in our own words). Draft for Thamesbridge's risk owner; scores are provisional until they set them. Not legal advice.

## Scope and intended use

- **System and functions:** reads balances and transactions, freezes a card after confirmation, explains a declined overdraft from reason codes; the decision engine decides, code enforces scope, confirmation and the reason-code limit, the model words answers (R1, R2, R3, C1, C2, C3, D3).
- **Intended use:** in-app chat for opted-in retail customers, 5,000 UK and 1,000 Irish, 8 weeks (docs/discovery/service-assistant.md §2, §6); **unintended or foreseeable misuse:** asking for payments or unfreezing (out of scope, D5), asking whether a decision will change (C4), another customer's data (C1), prompt injection through free text (gap: SB17 and SB18 not in the design's security baseline).
- **Organisation's role:** Thamesbridge is provider and deployer; Southgate Labs is developer and support supplier (regulatory-memo.md Roles; counsel: confirm).
- **Lifecycle stage and trigger:** pilot approval, build v0.8.0 verified locally (G05, docs/plans/service-assistant.md).

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| Pilot customers, UK and Ireland | Direct users; their money, card access and credit information | assumption: some are vulnerable, for example in financial difficulty; gap: no vulnerability data | docs/discovery/service-assistant.md §4, §6 |
| Customers whose overdraft was declined | Told why by the assistant; misleading explanation affects their view of their credit | assumption: yes | R3, docs/discovery/service-assistant.md §4 |
| People named in transactions and other customers | Their data appears in transaction descriptions; another customer's balance if scope fails | no | docs/discovery/service-assistant.md §3, C1 |
| Contact-centre staff in Leeds and Cork | Receive handovers; possible change in workload | no | docs/discovery/service-assistant.md §1, C3 |
| Southgate Labs engineers | Handle bank customers' data under access terms | no | D4 |

## System information

- **Data:** account, transaction, card status and decision reason-code data from the core banking, card platform and decision engine; transcripts; transactions reveal health, religion and union payments (docs/discovery/service-assistant.md §3). Quality and provenance are those of the source systems; gap: not assessed.
- **Model and logic:** gemini-3.5-flash-001 pinned (D1); gap: retirement date not read, relevant because support runs six months (D4). Deterministic parts: own-account scope, freeze confirmation, reason-code tool, output validator, pseudonymisation (C1, C2, C3, C4, C5).
- **Deployment environment:** Vertex AI in London for UK and Belgium for EU; logs and traces in the same region; engineers in Sydney (D2, D4).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | Customers | harm | A balance or transaction from the wrong account discloses another customer's data | assumption: low, scoped by verified ID | assumption: high | docs/discovery/service-assistant.md §4, C1 |
| H2 | Customers whose overdraft was declined | harm | Wrong explanation misleads a customer about their credit | assumption: low to moderate, 0.8 % mismatch on synthetic data | assumption: high | docs/discovery/service-assistant.md §4, M1 |
| H3 | Customers | harm | A card frozen in error stops a customer paying; a freeze not made leaves fraud running | assumption: low to moderate | assumption: moderate to high | docs/discovery/service-assistant.md §4, M2 |
| H4 | Customers | harm | Health, religion or union membership inferred from merchant names is seen by the model, logs and Sydney engineers | assumption: moderate | assumption: moderate | docs/discovery/service-assistant.md §3, D4 |
| H5 | Customers in financial difficulty | harm | An explanation read as advice or as a promise that a decision will change | assumption: low | assumption: moderate | C4, R4 |
| H6 | Customers | harm | Customers do not know Google and Sydney engineers are involved | assumption: moderate without notice | assumption: low to moderate | D1, D4 |
| H7 | Customers needing support in other languages or with accessibility needs | harm | Explanations less accurate or usable | hypothesis: possible | hypothesis: moderate | gap: no group-level or language test recorded |
| B1 | Customers | benefit | More chats resolved without waiting for an agent: 41 % on 120 staff test chats against a 22 % baseline for the menu bot (different populations, not comparable) | hypothesis: improvement on real traffic | n/a: benefit | M3, docs/discovery/service-assistant.md §2 |
| B2 | Customers | benefit | Faster card freezes | hypothesis: faster than the menu bot; no measure | n/a: benefit | R2, gap: freeze time not measured |
| CD1 | Customers | harm or benefit | Consumer Duty, products and services: the assistant adds a channel and does not change products | hypothesis: neutral | n/a: no product change | docs/discovery/service-assistant.md §5 |
| CD2 | Customers | harm or benefit | Consumer Duty, price and value: no price effect | n/a: no charge for the chat | n/a | R1, R2, R3 |
| CD3 | Customers | harm or benefit | Consumer Duty, consumer understanding: explanations must be understood | hypothesis: understanding unmeasured | assumption: moderate | M1, gap: no customer comprehension test |
| CD4 | Customers | harm or benefit | Consumer Duty, consumer support: handover to a person when the assistant cannot answer | hypothesis: works as C3 describes | assumption: moderate | C3, gap: hand-off time not measured |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1 | Tool scoped to the verified customer ID; refusal on failure | in place, tested locally | C1, G01/A2 |
| H2 | Reason-code-only tool, output validator, fixed message and handover | in place, tested locally; 99.2 % on 500 synthetic applications, not customer data | C3, M1 |
| H3 | Freeze only after explicit confirmation bound to the card ID | in place, tested locally; 0 unconfirmed freezes in 300 scripted conversations; missed freezes unmeasured | C2, M2 |
| H4 | Pseudonymised transcripts for engineers | partly in place, tested locally; gap: merchant-name masking, logs and traces, coverage | C5, G04/A1 |
| H5 | The assistant may not say a decision will change or invite a reapplication outcome | in place, tested locally | C4, G03/A2 |
| H6 | Chat-header disclosure | in place as a design decision; gap: notice naming Google and Sydney access | D6 |
| H7 | None recorded | gap: proposed goal for adk-agent-evaluation | docs/discovery/service-assistant.md §4 |
| CD3, CD4 | Fixed message and handover on failure | in place, tested locally; comprehension and hand-off time unmeasured | C3, D6 |

## Residual risk and decision

- H1 and H3 are limited by deterministic controls but proven only on test data; H2 is limited by M1 on synthetic data; H4, H6 and H7 have no or partial controls (C1, C2, C3, C5).
- **Accepted by:** gap: acceptance by Laura Whitfield, Customer Operations Committee, on 2026-12-03; no acceptance is recorded (docs/discovery/service-assistant.md §6).
- **Conditions that end acceptance:** the share of explanations not matching reason codes on real traffic rises above the figure the risk owner sets (gap: no threshold recorded; M1); any freeze without confirmation (M2); any cross-customer disclosure (C1); a model retirement or change (D1).

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | Sponsor and decider named; both DPOs, the CISO and the Consumer Duty champion named; gap: accountable senior manager, counsel and the AI literacy measures not named | docs/discovery/service-assistant.md §5 |
| Map | Scope, parties, regimes AU, EU and UK, EU classification proposed as transparency only | regulatory-memo.md, R1, R2, R3 |
| Measure | M1, M2 and M3 are offline, scripted or staff tests; not measured: real customer traffic, complaints per 10,000 chats against the 3.1 baseline, groups, languages, hand-off time | M1, M2, M3, docs/discovery/service-assistant.md §2 |
| Manage | Controls C1 to C5 tested locally; W1 model risk review; no incident records exist (gap: no incident records, none expected before the pilot) | C1, C2, C3, C4, C5, W1 |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| CBRN information or capabilities | n/a: narrow banking tools | Scope instruction | R1, R2, R3 |
| Confabulation | yes | Reason-code tool, validator, fixed message; no suggested action IDs recorded | C3, C4, M1 |
| Dangerous, violent or hateful content | n/a: customer account chat, no screening recorded; gap: confirm provider safety filters | none recorded | D1 |
| Data privacy | yes | Scoped reads, transcript pseudonymisation; gaps on logs, retention and masking | C1, C5 |
| Environmental impacts | n/a: noted, not measured | none | D1 |
| Harmful bias or homogenisation | yes | gap: no bias or language testing | docs/discovery/service-assistant.md §4 |
| Human-AI configuration | yes | Chat-header disclosure; handover; no over-reliance test | D6, C3 |
| Information integrity | n/a: private chat, not published | none | R1, R2, R3 |
| Information security | yes | Build rules SB01, SB03, SB05; gap: no red-team results recorded | SB01, SB03, SB05 |
| Intellectual property | n/a: no third-party content retrieved | none | R1, R2, R3 |
| Obscene, degrading or abusive content | n/a: text banking tool | none | D1 |
| Value chain and component integration | yes | Pinned model; gap: retirement date, sub-processor list, CreditLens role | D1, D3 |

## Monitoring and review

- Watched in operation: explanation match to reason codes, unconfirmed freezes, cross-customer disclosure, handover rate, complaints mentioning the chat per 10,000 chats against 3.1 (M1, M2, docs/discovery/service-assistant.md §2); gap: owners and thresholds not recorded.
- **Review triggers:** model change or retirement, new customer group such as under-18s or other EU countries, a new data source, an incident, a change in law or ICO guidance (D1, docs/discovery/service-assistant.md §6).

## EU: FRIA crosswalk (AI Act Article 27, if required)

| Article 27(1) | Pack section | Evidence |
| --- | --- | --- |
| (a) deployer's processes using the system | Scope and intended use; privacy-impact-input-pack.md Processing description | R1, R2, R3 |
| (b) period and frequency of use | privacy-impact-input-pack.md Processing description | docs/discovery/service-assistant.md §6 |
| (c) categories of persons and groups affected | Interested parties | docs/discovery/service-assistant.md §6 |
| (d) specific risks of harm | Impacts; privacy-impact-input-pack.md Risks and measures | H1, H2, H3, H4 |
| (e) human oversight measures | system-card.md Human oversight | C2, C3 |
| (f) measures if risks materialise, governance, complaints | Measures; Residual risk and decision | gap: complaints route; counsel: required under Article 27 only if the assistant is Annex III point 5(b) |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| UK DPO (Oliver Grant) | this document | pending | pending |
| Ireland DPO (Siobhán Kelly) | this document | pending | pending |
| Group CISO (Rachel Adeyemi) | Measures and Information security rows | pending | pending |
| Risk owner (Laura Whitfield) | Residual risk and decision | pending | pending |
