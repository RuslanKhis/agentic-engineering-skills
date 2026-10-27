---
document: regulatory-memo
system: Thamesbridge customer service assistant
version: design accepted 2026-09-18, build v0.8.0
status: draft
jurisdictions: [au, eu, uk]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Thamesbridge counsel for the UK and Ireland (not named in the record), with the UK DPO and the Ireland DPO
sources: docs/discovery/service-assistant.md, docs/architecture/service-assistant.md, docs/plans/service-assistant.md
---

# Regulatory memo: Thamesbridge customer service assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Thamesbridge's counsel and its two DPOs. It records which regimes the jurisdiction
screen found in scope, the facts the design records, and the provisions that appear relevant in
each regime: the EU AI Act classification, and a screen of the existing laws that apply in
Australia and the United Kingdom, neither of which has an AI Act or assigns a risk tier.
Conclusions are proposals for counsel; not legal advice. No network was available when this was
drafted, so nothing was re-read at a primary source: each legal fact is copied from the skill's
references with the date they give.

## Summary

- **Regimes in scope:** Australia (through the consultancy's own handling only), EU, United Kingdom (Jurisdiction screen below; counsel: confirm the screen, and the three regimes left out).
- **Proposed EU classification:** transparency obligations only (Article 50(1)), not prohibited and not Annex III high-risk, because the assistant reads reason codes from the decision engine and does not score or evaluate creditworthiness (C3, D3, R4). Article 6(3) is not argued. counsel: confirm that explaining a declined overdraft is not Annex III point 5(b) and that the CreditLens decision engine is assessed separately (D3).
- **Main obligations, UK:** UK GDPR Articles 22A to 22D safeguards for the decision engine's declines that the assistant explains; a restricted transfer for Sydney access; a DPIA (W2); Consumer Duty (docs/discovery/service-assistant.md §5; checked 2026-10-26).
- **Main obligations, EU:** GDPR Article 22 and Articles 13(2)(f), 14(2)(g) and 15(1)(h) for the declines; Chapter V transfer for Sydney access; DPIA under Article 35 (W2); Article 50(1) disclosure, applicable now; DORA contract terms for the Irish bank (counsel: confirm) (checked 2026-10-26).
- **Main obligations, Australia:** the consultancy's own APP 8 and APP 11 position and the notifiable data breach scheme, if the Privacy Act reaches its handling of UK and EU customers' data (counsel: confirm).
- **Proposed roles:** Thamesbridge Bank plc controller for UK customers; Thamesbridge Bank Ireland DAC controller for Irish and EU customers; Southgate Labs processor; Google Cloud processor (Roles below; counsel: confirm).
- **Blocking questions:** counsel: 14 questions, listed under Questions for counsel; the first five block the pilot decision on 2026-12-03 (W3).
- **Direct answer, is a DPIA needed?** counsel: yes for both the UK and the EU on the facts: a generative model (D1), financial data revealing health, religion and union payments (docs/discovery/service-assistant.md §3), and automated declines explained to customers (D3) meet more than two WP248 criteria. W2 already schedules sign-off by both DPOs; the DPOs decide.

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes (gap: consultancy turnover and entity status) | Southgate Labs engineers in Sydney have access to logs, traces and pseudonymised transcripts for six months (D4); the client, the customers and the hosting are not in Australia (docs/discovery/service-assistant.md §1, D2) | The consultancy's own handling only; counsel: whether the Privacy Act reaches Australian-based handling of UK and EU customers' data; the client's own APP 1.7 and sector rows are n/a: client not Australian, no Australian data subjects |
| United States | no | No US client, customers or processing; customers are in the UK, Ireland and other EU countries (docs/discovery/service-assistant.md §1, §3) | n/a: no US data subjects, client or processing purpose; counsel: confirm no US-resident customer is in the pilot (gap: residency check at opt-in) |
| EU | yes | Thamesbridge Bank Ireland DAC is established in Ireland and serves customers in Ireland and other EU countries; Belgium hosting (docs/discovery/service-assistant.md §1, D2) | Establishment and services offered to people in the EU; GDPR Article 3 and AI Act Article 2 are counsel: conclusions |
| United Kingdom | yes | Thamesbridge Bank plc is a UK retail bank regulated by the FCA and PRA; London hosting (docs/discovery/service-assistant.md §1, D2) | Establishment and services offered to people in the UK; a UK pack with EU users keeps the EU sections as well |
| New Zealand | no | No New Zealand client, customers or data (docs/discovery/service-assistant.md §1, §3) | n/a: no trigger fact in the record |
| Singapore | no | No Singapore client, customers or data (docs/discovery/service-assistant.md §1, §3) | n/a: no trigger fact in the record |
| Canada | no | No Canadian client, customers or data, and no Quebec enterprise (docs/discovery/service-assistant.md §1, §3) | n/a: no trigger fact in the record |

- **Processing locations:** UK traffic in europe-west2 (London) and Irish and EU traffic in europe-west1 (Belgium), with logs and traces in the traffic's region (D2); consultancy access from Sydney (D4); the model's processing region and the abuse-monitoring, caching and grounding locations are gap: not recorded in D1 and not readable without network access; proposed goal for adk-model-and-output-contracts.
- **Government client:** private client, a regulated bank; n/a: no Commonwealth, NSW, UK central government or other public body (docs/discovery/service-assistant.md §1).
- **Consultancy home:** assumption: Australia, from the record that the engineers are in Sydney (D4, docs/discovery/service-assistant.md §5).

## System and intended purpose

- **What it does:** answers balance and transaction questions for the signed-in customer, freezes a card after the customer confirms, and explains a declined overdraft from the decision engine's reason codes (R1, R2, R3).
- **Who uses it and who it affects:** opted-in retail customers in the app chat, 5,000 in the UK and 1,000 in Ireland for 8 weeks; the people named in transaction merchant names are also affected (docs/discovery/service-assistant.md §3, §6).
- **What the model decides and what code or people decide:** the CreditLens decision engine, run by Thamesbridge, makes every credit decision (D3); code enforces own-account scope, freeze confirmation and the reason-code limit (C1, C2, C3); the model words answers.
- **Effects it can cause:** reads accounts, transactions and decision reason codes; freezes a card after confirmation; no unfreeze, payments or credit changes (R1, R2, R4, D5).
- **Human review of decisions about people:** the assistant makes no decision about a person; a failed explanation returns a fixed message and handover (C3). gap: the share handed over and the hand-off time are not measured; no M record exists.

## Roles

- **Facts:** the bank commissions the assistant and runs it in its apps (docs/discovery/service-assistant.md §1, §2); Southgate Labs built it and supports it for six months from Sydney (D4); Google Cloud hosts the model and services in the two regions (D1, D2). gap: which Thamesbridge entity owns the Google Cloud project in each region, and which entity signs the Southgate Labs contract.
- **Australia, Privacy Act:** Southgate Labs is an APP entity in its own right if its turnover is above $3 million or an exemption does not apply (gap: turnover not recorded); no processor category exists in Australian law (counsel: confirm entity status, the s 6D position and whether the Act reaches handling of non-Australians' data).
- **EU AI Act:** Thamesbridge is provider (it has the system developed) and deployer; the entity differs by region (counsel: which entity is provider; Article 25 is not triggered on the facts because Southgate Labs builds under contract, not under its own name, assumption: no resale or reuse of the build for other clients) (D3, docs/discovery/service-assistant.md §1).
- **EU GDPR and UK GDPR, separately:** Bank plc controller under UK GDPR; Bank Ireland DAC controller under GDPR; Southgate Labs and Google Cloud processors; whether Google is a controller for any part such as abuse monitoring is counsel: (privacy-impact-input-pack.md; counsel: confirm, including whether the two banks are joint controllers for the shared assistant).

## Australia: Privacy Act and APPs

- **No AI-specific regime:** Australia has no AI Act; the 2024 mandatory guardrails proposal will not proceed, and obligations come from the laws screened here (source: adk-governance-pack reference, read 2026-10-26; checked 2026-10-26).
- **APPs engaged:** APP 11 for pseudonymised transcripts, logs and traces the engineers hold, and APP 8 only if an Australian-law disclosure is made; APP 1.7 does not engage because Southgate Labs makes no decision about a person (D4, C5, D3; counsel: confirm).
- **Overseas disclosure (APP 8, s 16C):** the personal information is UK and EU customers' data accessed from Australia, so the flow is inbound to Australia; counsel: whether APP 8 has any role; the outbound facts are in the transfer-assessment.md for the UK and EU rules (D4).
- **Notifiable data breaches:** if the Privacy Act reaches the handling, an eligible data breach in the engineers' environment is assessed within 30 days and notified as soon as practicable (security-questionnaire.md; counsel: which entity notifies, and the interaction with the 72-hour UK and EU clocks).
- **Pending, not law:** the tranche 2 exposure draft is not law (source: adk-governance-pack reference, read 2026-10-26); not relevant to a decision here beyond watching it.

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| n/a: the consultancy makes no decision about a person; the client's own APP 1.7 duty does not arise because its customers are in the UK and EU | n/a: not an Australian client | n/a: no Australian decision | n/a | Balances, transactions and decision reason codes are visible to the program (R1, R3) | D3, D4; counsel: confirm n/a |

- **Privacy policy inputs (APP 1.8):** n/a: no Australian customers; the consultancy's own privacy policy should describe the Sydney access (system-card.md, D4).

## Australia: Sector, state and government AI policy

- **Sector laws:** n/a: APRA CPS 234 and CPS 230 bind APRA-regulated entities and the client is regulated by the FCA, the PRA and the Central Bank of Ireland (docs/discovery/service-assistant.md §1); Australian Consumer Law ss 18 and 29 n/a: no Australian consumers.
- **Government AI policy:** n/a: private client; no DTA or NSW AIAF form is required (docs/discovery/service-assistant.md §1).

## EU: Prohibited practices (Article 5)

| Point | Applies? | Facts | Evidence |
| --- | --- | --- | --- |
| (a) manipulation, (b) exploiting vulnerabilities | no, counsel: confirm for customers in financial difficulty | The assistant explains decline reason codes and may not promise or invite a reapplication outcome | C4, R4 |
| (ba), (bb) generated intimate or abuse material | no | Text-only banking assistant | R1, R2, R3 |
| (c) social scoring, (d) crime prediction by profiling | no | No scoring of customers; fraud detection is not part of the assistant | D3, R4 |
| (e) facial scraping, (g) biometric categorisation, (h) real-time remote identification | no | No biometric input is recorded in the design | D1, D5 |
| (f) emotion inference at work or in education | no | No inference about staff or students | R1, R2, R3 |

## EU: High-risk classification (Article 6 and Annex III)

- **Annex I product:** no; assumption: not a safety component of a regulated product.
- **Annex III area touched:** point 5(b) creditworthiness is the only candidate; the assistant does not evaluate creditworthiness or produce a score, it relays reason codes the decision engine produced (R3, C3, D3; counsel: is relaying and explaining a decision "used to evaluate creditworthiness"?).
- **Profiling of natural persons:** the assistant does not profile; the decision engine may (D3; gap: engine inputs and logic are not in the record; counsel: classify CreditLens as its own AI system).
- **Article 6(3) derogation facts, if argued:** not argued; the proposed classification does not depend on it (counsel: confirm).
- **If high-risk:** Chapter III obligations, Article 26 deployer duties and the Article 27 FRIA (credit) would follow, from 2 December 2027 (Article 113(c), checked 2026-10-26); no plan goals exist for them (gap: proposed goals if counsel classifies it as high-risk).
- **Article 25(4) agreement (if high-risk):** gap: no written agreement between Thamesbridge and Southgate Labs is in the record; counsel: needed only if high-risk.

## EU: Transparency obligations (Article 50)

| Paragraph | Applies? | How the design meets it | Evidence |
| --- | --- | --- | --- |
| 50(1) told they interact with AI | yes | The chat header says customers are talking to the bank's assistant (D6); gap: the wording does not say it is an AI, there is no contract or test for it, and answers to "are you a human?" are not recorded | D6; proposed goal for adk-operational-guardrails |
| 50(2) machine-readable marking of generated content | counsel: text answers in a private chat | No marking decision is recorded (gap: D-level decision needed; counsel: which exception under the guidelines paragraphs 87 to 91, if any) | D1 |
| 50(3) emotion recognition or biometric categorisation notice | n/a: neither is performed | No such feature in the design | R1, R2, R3 |
| 50(4) deepfakes or public-interest text | n/a: private account chat | Not published to the public | R1, R2, R3 |

## EU: General-purpose AI model

- **Model and provider:** Gemini 3.5 Flash, pinned as gemini-3.5-flash-001 on Vertex AI, Google as model provider (D1).
- **Obligations under Articles 53 and 55:** sit with the model provider; Thamesbridge relies on its documentation (source: adk-governance-pack reference, read 2026-10-26; counsel: confirm reliance).
- **Fine-tuning or modification:** none recorded (D1; assumption: no fine-tuning).
- **Downstream modification compute:** none recorded (assumption: none, D1).

## EU: Other regimes

- **GDPR Article 22:** the decision engine's declines are the candidate decisions; the assistant explains them (privacy-impact-input-pack.md; D3; counsel: Article 22 applies to the engine, and what the assistant must say).
- **DORA, Regulation (EU) 2022/2554:** Thamesbridge Bank Ireland DAC is a financial entity; Article 30 contract terms reach Southgate Labs as an ICT third-party service provider, and Google Cloud likewise; applies from 17 January 2025 (checked 2026-10-26; counsel: is the assistant supporting a critical or important function, which contract terms and incident clock apply) (D4).
- **NIS2:** counsel: whether the Irish bank is in scope; the reporting clocks are in security-questionnaire.md (D4).
- **Product Liability Directive (EU) 2024/2853:** applies to products placed on the market after 9 December 2026 (checked 2026-10-26); software is a product, and the pilot starts after the 2026-12-03 decision (docs/discovery/service-assistant.md §6; counsel: who is the manufacturer and what indemnities apply).
- **Cyber Resilience Act and Data Act:** n/a: a bespoke hosted assistant for one client is not a product made available on the market (source: adk-governance-pack reference, read 2026-10-26); DSA n/a: not an intermediary service.
- **Irish sector rules, including the Central Bank of Ireland's consumer and outsourcing requirements:** counsel: not covered by the skill's references; facts at docs/discovery/service-assistant.md §1.

## United Kingdom: UK GDPR and automated decisions

- **No AI-specific statute:** the UK has no AI Act; the King's Speech of 13 May 2026 announced no AI bill (checked 2026-10-26).
- **Regulator:** the Information Commission (formerly the ICO), since 30 September 2026 (checked 2026-10-26).
- **Significant decisions (Articles 22A to 22D):** the decision engine decides declines with some degree of human involvement unknown (gap: whether any person reviews a CreditLens decline, and the share, is not in the record); the assistant adds no decision (D3, R4). Article 22B bites if special category data feeds the engine (gap: engine inputs; transactions reveal health, religion and union payments, docs/discovery/service-assistant.md §3). The four Article 22C safeguards need a contest route the assistant can point to (gap: no route is recorded; R4 bars the assistant from promising outcomes) (privacy-impact-input-pack.md; counsel: significant? meaningful involvement?). The draft ICO ADM guidance is a consultation draft, final due Winter 2026 (checked 2026-10-26).
- **Restricted transfers:** Southgate Labs access from Sydney is a restricted transfer, with no UK adequacy regulations for Australia (checked 2026-10-26); the IDTA or Addendum and the data protection test are needed (transfer-assessment.md, D4, W4; counsel: test met?).

## United Kingdom: Equality, consumer, online safety and sector

- **Equality Act 2010:** the assistant makes no decision; the equality risk is unequal explanation quality or access for protected groups (impact-assessment.md; gap: no group-level or accessibility testing is recorded; counsel: justified?).
- **Consumer law and CMA guidance:** the CMA's AI-agent guidance of 9 March 2026 (checked 2026-10-26) says tell people they deal with AI where it could change a decision and do not overstate AI's role; the bank is accountable for a third party's build (D6, system-card.md).
- **FCA, Consumer Duty and SM&CR:** the FCA says no new AI regulations (8 June 2026, checked 2026-10-26); the Consumer Duty applies and the board champion is Ian Shah (docs/discovery/service-assistant.md §5); gap: the accountable senior manager is not named; PRA and FCA operational resilience and outsourcing rules: counsel: not covered by the skill's references.
- **Online Safety Act:** n/a: customers cannot share outputs with each other and the assistant does not search several sites; assumption: R1, R2, R3 are the complete function; counsel: confirm.
- **ATRS:** n/a: private bank, not a central government body (docs/discovery/service-assistant.md §1).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| EU | Article 50 transparency | 2 August 2026 (Article 113, checked 2026-10-26) | Already applicable; D6 wording and test needed before the pilot |
| EU | Annex III high-risk obligations and Article 27 | 2 December 2027 (Article 113(c), checked 2026-10-26) | Matters only if counsel classes the assistant as point 5(b) |
| EU | Article 4 AI literacy, revised wording | 27 July 2026 (Regulation 2026/1744, checked 2026-10-26) | Training for contact-centre staff who receive handovers; gap: no plan goal |
| EU | DORA | 17 January 2025 (checked 2026-10-26) | Contract terms and incident reporting for Southgate Labs and Google (D4) |
| EU | Product Liability Directive | 9 December 2026 (Article 2(1), checked 2026-10-26) | Pilot products placed after that date; counsel: manufacturer |
| UK | Articles 22A to 22D and Article 44A transfers | 5 February 2026 (DUAA, checked 2026-10-26) | Decline explanations and Sydney access |
| UK | Complaints route, DPA 2018 s 164A | 19 June 2026 (checked 2026-10-26) | System card contact; gap: route not confirmed |
| UK | Information Commission replaces the Information Commissioner | 30 September 2026 (SI 2026/1015, checked 2026-10-26) | Name the Commission in notices |

- **AI literacy (EU AI Act Article 4) and staff training:** gap: no goal covers training for the staff who take handovers; proposed goal for adk-governance-pack hand-over to the rollout pack.
- **Documents the client's own process produces:** the DPIA (W2); prior consultation only if the DPIA records high residual risk (W5); the model risk review (W1); counsel's review of this memo (W3); transfer instruments (W4); the CISO security approval (W6); Consumer Duty outcome record owned by the board champion (agency: n/a, the owner is Ian Shah per docs/discovery/service-assistant.md §5; gap: no wait recorded).

## Assumptions and questions for the client

- assumption: Southgate Labs processes only on Thamesbridge's instructions and uses no data to train models (D4); question for Thamesbridge procurement: which contract and data processing terms exist.
- assumption: pilot customers are adults; gap: whether any pilot customer is under 18 (UK Article 25(1A) children's higher protection matters) (docs/discovery/service-assistant.md §6).
- assumption: the 1,000 Irish pilot customers are resident in Ireland; gap: whether any are resident in another EU country (docs/discovery/service-assistant.md §1).
- assumption: Southgate Labs support lasts six months after launch (D4) although the pilot runs 8 weeks (docs/architecture/service-assistant.md Scope gate); question: should engineer access to production data stop at pilot end unless extended?
- gap: model retirement date and processing region for gemini-3.5-flash-001 (D1); the model lifecycle table is not installed and no network access exists; proposed goal for adk-model-and-output-contracts to read the model page and compare the retirement date with the six-month support horizon.

## Questions for counsel

- counsel: which Thamesbridge entity is controller for the assistant in each region, and are the two banks joint controllers; regime EU and UK; facts at D2, docs/discovery/service-assistant.md §1; needed before W2.
- counsel: is Southgate Labs access from Sydney to logs, traces and transcripts a restricted transfer under UK GDPR and GDPR, who exports, which instrument (UK IDTA or Addendum; EU SCC module), and is the data protection test or transfer impact assessment met; regime EU and UK; facts at D4, C5; needed before W4.
- counsel: does the Privacy Act reach Southgate Labs' handling of UK and EU customers' data, and is Southgate Labs an APP entity; regime Australia; facts at D4; needed before W3.
- counsel: is explaining a declined overdraft within Annex III point 5(b), and is CreditLens a separate AI system with its own classification; regime EU; facts at R3, C3, D3; needed before the pilot decision on 2026-12-03.
- counsel: does Article 22 or Article 22A apply to the decision engine's declines, are the Article 22C safeguards and Article 15(1)(h) explanation delivered, and does Article 22B apply given transaction data revealing health, religion and union payments; regime EU and UK; facts at D3, C3; needed before W2.
- counsel: what lawful basis and Article 9 condition fit each purpose, including whether the pilot opt-in is consent or only a participation control; regime EU and UK; facts at docs/discovery/service-assistant.md §3, §6; needed before W2.
- counsel: are the pseudonymised transcripts personal data for Southgate Labs and for Thamesbridge (they remain personal data for Thamesbridge), and does C5 cover logs and traces (it does not on the record); regime EU and UK; facts at C5, D4; needed before W4.
- counsel: does Google act only as processor, including for abuse monitoring, and does the client's agreement exempt prompts from abuse-monitoring storage; regime EU and UK; facts at D1; needed before W2.
- counsel: is DORA Article 30 contract content in place for Southgate Labs and Google, and is the assistant a critical or important function; regime EU; facts at D4, D1; needed before W3.
- counsel: what do the Central Bank of Ireland, the PRA and the FCA require for outsourcing, operational resilience and incident reporting here; regime EU and UK; the skill's references do not cover them; needed before W1.
- counsel: does the Article 50(1) disclosure as worded in D6 suffice, and is marking under Article 50(2) needed; regime EU; facts at D6; needed before the pilot decision on 2026-12-03.
- counsel: who is manufacturer under the Product Liability Directive and what indemnities between Thamesbridge and Southgate Labs apply; regime EU; facts at D4; needed before the pilot decision on 2026-12-03.
- counsel: is Article 36 prior consultation needed if the DPIA records high residual risk, given the eight-week clock cannot fit before 2026-12-03; regime EU and UK; facts at W2, W5; needed before W2.
- counsel: the sector rules for the Irish and UK banks on consumer duty, complaints handling and vulnerable customers are not covered by the skill's references; regime EU and UK; facts at docs/discovery/service-assistant.md §4; needed before W3.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Thamesbridge counsel for the UK and Ireland (not named: gap) | this document | pending | pending |
| UK DPO (Oliver Grant) | this document | pending | pending |
| Ireland DPO (Siobhán Kelly) | this document | pending | pending |
