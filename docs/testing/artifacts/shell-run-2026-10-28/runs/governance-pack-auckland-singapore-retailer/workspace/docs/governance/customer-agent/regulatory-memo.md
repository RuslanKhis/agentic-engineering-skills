---
document: regulatory-memo
system: Kowhai Retail customer agent
version: design accepted 2026-09-09; build v0.6.1 (M1, M2)
status: draft
jurisdictions: [au, nz, sg]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: privacy officer (Aroha Ngata, Kowhai Retail Limited, Auckland) and Data Protection Officer (Daniel Tan, Kowhai Retail (Singapore) Pte. Ltd.), with Kowhai Retail's counsel (not yet named; gap)
sources: docs/discovery/customer-agent.md, docs/architecture/customer-agent.md, docs/plans/customer-agent.md
---

# Regulatory memo: Kowhai Retail customer agent

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Kowhai Retail's privacy officer, Data Protection Officer and
counsel. It records which regimes the jurisdiction screen found in scope, the
facts the design records, and the provisions that appear relevant in each
regime: a screen of the existing laws that apply in Australia (through the
consultancy's own handling only), New Zealand and Singapore, none of which
has an AI Act or assigns a risk tier. Conclusions are proposals for counsel;
not legal advice.

## Summary

- **Regimes in scope:** Australia (the consultancy's own handling only), New Zealand, Singapore (Jurisdiction screen below; counsel: confirm the screen, in particular that no United States, EU, UK or Canadian people use the pilot).
- **Main obligations in the other regimes:**
  - New Zealand: IPP 5 security, IPP 8 accuracy before use, IPPs 9 to 11 retention, use and disclosure (transcript reuse for evaluation, D3), s 11 agent status of Southgate Labs and Google, notifiable privacy breaches (D1, D2, D3, D4, M3; checked 2026-10-26).
  - Singapore: the client's Transfer Limitation Obligation for data held in Sydney (D2) and read from Sydney (D4); Southgate Labs as data intermediary only while it stays inside the written contract; an assessed basis for reusing transcripts to build evaluation sets (D3); the 3-calendar-day PDPC clock (checked 2026-10-26).
  - Australia: the consultancy's own APP 8, APP 11 and notifiable-data-breach position for Sydney access to traces (D4; counsel: whether the Privacy Act reaches it).
- **Proposed roles:** Kowhai Retail Limited and Kowhai Retail (Singapore) Pte. Ltd. each as agency and organisation for their own customers; Southgate Labs as s 11 agent and data intermediary for the pilot; Google as s 11 agent and data intermediary for model processing (Roles below; counsel: confirm).
- **Direct questions:** none was asked beyond "draft the papers" (source: requester, 2026-10-28); proposed answers to the two likely ones, each counsel:
  - Is a privacy impact assessment needed? The Act in New Zealand does not require one but the OPC expects one before AI tools are used; Singapore does not require one. Proposed: complete the New Zealand PIA and a Singapore DPIA before the pilot (privacy-impact-input-pack.md Screening; W2, W3).
  - Can Sydney engineers read traces with customer data? Proposed: only under a written contract that names Australia (Singapore) and holds the data for Kowhai only (New Zealand); the record holds no such contract (D4; gap: contract).
- **Blocking questions:** counsel: 14 questions, listed under Questions for counsel; the first five block the pilot decision of 2026-11-26 (docs/discovery/customer-agent.md §6).
- **Assumptions this draft proceeds on** (no one was available to ask): assumption: pilot starts on or after 2026-11-26 (docs/discovery/customer-agent.md §6); assumption: consultancy home Australia (default); assumption: no customer in the pilot is in the United States, EU, UK or Canada (docs/discovery/customer-agent.md §3); assumption: Southgate Labs engineers reach traces only from Sydney (D4); assumption: Kowhai is not a MAS-regulated or health client (docs/discovery/customer-agent.md §1).

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes | Southgate Labs engineers in Sydney read traces that include CRM fields (D4); hosting in australia-southeast1 (D2); assumption: consultancy home Australia (default) | The consultancy's own handling only; counsel: whether the Privacy Act reaches it. The client's customers are in New Zealand and Singapore (docs/discovery/customer-agent.md §3), so the client's own APP 1.7 and sector rows are n/a: no Australian client or customers in the record |
| United States | no | Customers and stores in New Zealand and Singapore only (docs/discovery/customer-agent.md §1) | n/a: no US data subject, client or processing purpose in the record; assumption: online shops reach only incidental visitors elsewhere; counsel: confirm |
| EU | no | Customers and stores in New Zealand and Singapore only (docs/discovery/customer-agent.md §1) | n/a: no EU establishment, EU customer or EU output use in the record; assumption: incidental visitors only |
| United Kingdom | no | Customers and stores in New Zealand and Singapore only (docs/discovery/customer-agent.md §1) | n/a: no UK establishment, customer or central government client in the record |
| New Zealand | yes | Kowhai Retail Limited is in Auckland with 41 stores and an online shop (docs/discovery/customer-agent.md §1); New Zealand customers' CRM data (docs/discovery/customer-agent.md §3); Sydney hosting and access (D2, D4) | Client is a New Zealand agency; personal information about people in New Zealand is handled; the consultancy accesses it from Australia |
| Singapore | yes | Kowhai Retail (Singapore) Pte. Ltd. has 9 stores and an online shop (docs/discovery/customer-agent.md §1); Singapore customers' CRM data (docs/discovery/customer-agent.md §3); Sydney hosting and access (D2, D4) | Client collects, uses and discloses personal data in Singapore; every flow to Sydney is a transfer |
| Canada | no | Customers and stores in New Zealand and Singapore only (docs/discovery/customer-agent.md §1) | n/a: no Canadian client, customer or Quebec enterprise in the record |

- **Processing locations:** Cloud Run, Firestore and logs in australia-southeast1 for both countries (D2); Gemini endpoint in australia-southeast1 (D1); gap: the model's machine-learning processing region and the retirement date of `gemini-3.5-flash-001` were not read from the model page (no web access in this session), so neither is assumed; proposed goal for adk-model-and-output-contracts; the Salesforce CRM region is not recorded (D5; gap); abuse monitoring, caching and grounding settings are not recorded (D1; gap); consultancy access from Sydney (D4).
- **Government client:** private client, Kowhai Retail Limited and its Singapore subsidiary (docs/discovery/customer-agent.md §1); no public body.

## System and intended purpose

- **What it does:** a web chat agent answers order and returns questions for the signed-in customer, reads order history from the Salesforce CRM at the time of the question, and issues store credit for an eligible return up to NZD 150 or SGD 130 per order (R1, R2, D5).
- **Who uses it and who it affects:** signed-in web chat customers in New Zealand and Singapore during a 6-week pilot; assumption: no staff are monitored (docs/discovery/customer-agent.md §6, R1). The number of pilot customers is not recorded (gap); monthly enquiry volume is 22,000 across both countries (docs/discovery/customer-agent.md §1).
- **What the model decides and what code or people decide:** code decides eligibility and the limit, and credits once per return (C2, C3); the model composes answers scoped to the verified customer's own records (C1); a person receives a handover on request (R3, C4). The record shows no human approval before a credit is issued (C2).
- **Effects it can cause:** reads CRM profile and order history; writes a store credit to the ledger; hands over to the service queue in the customer's country or a callback form (D5, R2, C4); cash refunds, order changes and marketing messages are out of scope (docs/architecture/customer-agent.md Scope gate).
- **Human review of decisions about people:** no review step before a credit is issued; handover share and time to connect are not measured (C4; gap: measure; proposed goal for adk-agent-evaluation). Test evidence: M2 records 0 credits above the limit or for ineligible returns in 200 scripted conversations (M2).

## Roles

- **Facts:** Kowhai Retail Limited (Auckland) and Kowhai Retail (Singapore) Pte. Ltd. commission the agent and run it under the Kowhai name; Mere Walker is sponsor and decider; Southgate Labs built it and its three engineers in Sydney read traces during the pilot and a six-month support period; Google hosts and runs the model (docs/discovery/customer-agent.md §1, §5; D1, D2, D4). Which entity is exporter or controller of which customers' data is not recorded for the group (gap).
- **Australia, Privacy Act:** the client is not an APP entity for these customers on the record; whether Southgate Labs is an APP entity in its own right depends on its turnover or contracts, which the record does not hold (gap: consultancy turnover); no processor category exists in Australian law today (counsel: confirm that the Privacy Act reaches Sydney staff reading New Zealand and Singapore customers' data).
- **New Zealand, Privacy Act 2020:** Kowhai Retail Limited is the agency; Southgate Labs and Google are proposed as s 11 agents if they hold the information only on Kowhai's behalf; s 11(3) makes them agencies in their own right if either uses it for its own purposes; whether Southgate Labs is caught by s 4(1)(b) as an overseas agency carrying on business in New Zealand is open; Aroha Ngata is the privacy officer (D4, D3; source: adk-governance-pack reference new-zealand.md, read 2026-10-26; counsel: confirm).
- **Singapore, PDPA:** Kowhai Retail (Singapore) Pte. Ltd. is the organisation; Southgate Labs is proposed as data intermediary only under a contract evidenced in writing, which the record does not hold (gap: contract); using client data for the consultancy's own evaluation sets beyond that contract would make it an organisation for that use (D3); Google is proposed as data intermediary for model inference; Daniel Tan is the DPO (D3, D4; source: adk-governance-pack reference singapore.md, read 2026-10-26; counsel: confirm).

## Australia: Privacy Act and APPs

Scope: the consultancy's own handling only (assumption: consultancy home Australia (default)).

- **No AI-specific regime:** Australia has no AI Act; the government will not proceed with the 2024 mandatory guardrails proposal and the National AI Plan relies on existing laws (source: adk-governance-pack reference australia.md, read 2026-10-26; checked 2026-10-26).
- **APPs engaged:** APP 11 for traces held in Sydney that include CRM fields (D4, D2); APP 6 for reuse of transcripts in evaluation sets (D3); APP 8 for any onward disclosure by Southgate Labs, for example to Google (D1); APP 12 and 13 if an access request reaches evaluation sets (D3). The inventory describes the consultancy's handling only (privacy-impact-input-pack.md; counsel: do the APPs apply at all).
- **Overseas disclosure (APP 8, s 16C):** hosting and the Gemini endpoint are in Australia (D1, D2), so the offshore question for Australian law arises only if Google's processing region, abuse review or a support desk is outside Australia (gap: model page not read); the client's own overseas-disclosure analysis is n/a: the client's customers are not in Australia (counsel: use or disclosure).
- **Notifiable data breaches:** assessment within 30 days and notice to the OAIC and individuals as soon as practicable where the Act applies; which entity notifies is open (security-questionnaire.md; source: adk-governance-pack reference australia.md, read 2026-10-26; counsel: which entity notifies).
- **Pending, not law:** tranche 2 exposure draft of the privacy reforms and the Children's Online Privacy Code are not law (source: adk-governance-pack reference australia.md, read 2026-10-26; checked 2026-10-26); n/a: no children are recorded as users (docs/discovery/customer-agent.md §3).

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| Whether a return is eligible for store credit, and the amount (R2) | Code makes the decision in the tool (C2); no person approves it | None before issue; handover on request (C4); share not measured (gap) | Money value to the customer under the returns policy | Order history, return record, customer ID (D5) | C2, C3, M2; counsel: significantly affects, and whether the consultancy rather than the client "arranges" the program |

- **Client's own APP 1.7 row:** n/a: the client's customers are not in Australia (docs/discovery/customer-agent.md §3). APP 1.7 applies from 10 December 2026 (checked 2026-10-26), which falls inside the pilot if it starts on 2026-11-26 (docs/discovery/customer-agent.md §6).
- **Privacy policy inputs (APP 1.8):** system-card.md, Automated-decision disclosure (C2), kept for the consultancy's own policy only.

## Australia: Sector, state and government AI policy

- **Sector laws:** n/a: retail client, not a bank, insurer, health provider, or My Health Record participant (docs/discovery/customer-agent.md §1); Spam Act n/a: marketing messages are out of scope (docs/architecture/customer-agent.md Scope gate); Australian Consumer Law n/a: no Australian consumers in the record.
- **Government AI policy:** n/a: private client (docs/discovery/customer-agent.md §1).

## New Zealand: Privacy Act and IPPs

- **No AI-specific statute:** New Zealand has no AI Act; the July 2025 AI Strategy relies on existing law (source: adk-governance-pack reference new-zealand.md, read 2026-10-26; checked 2026-10-26).
- **IPPs engaged:**
  - IPPs 1 to 3: collection from customers by chat and through shops and the loyalty programme (docs/discovery/customer-agent.md §3); the CRM read is Kowhai's own data, so IPP 3A is proposed as not engaged, with generated or inferred statements about a person as counsel (D5; counsel).
  - IPP 5: Salesforce credential and API routes (SB01, SB03) and 5(b) for each service provider (D1, D2, D4).
  - IPPs 6 and 7: access and correction within 20 working days reach transcripts and traces (D3, D4; checked 2026-10-26).
  - IPP 8: 93% correct order status answers on 300 test chats and 27% of test customers with a CRM address older than 24 months (M1, M3); whether the steps are "reasonable" is counsel's.
  - IPP 9: transcripts kept 12 months; trace retention is not recorded (D3; gap: trace retention).
  - IPPs 10 and 11: reuse of transcripts to build evaluation sets and Sydney access to traces (D3, D4; counsel: directly related purpose).
  - IPP 12: only if a party uses information for its own purposes (D1; counsel).
  - IPP 13: no unique identifier handling is recorded (gap: whether customer or loyalty numbers appear in outputs; C1).
- **Offshore processing (s 11 and IPP 12):** Cloud Run, Firestore, logs and the Gemini endpoint are in Sydney (D1, D2); the Vertex AI data residency page lists no New Zealand machine-learning region, the nearest being australia-southeast1 (source: adk-governance-pack reference new-zealand.md, page updated 22 October 2026, read 2026-10-26; page not re-read this session); Sydney staff read traces (D4); whether Google's abuse monitoring or retention is use "for its own purposes" is open (D1; counsel: agent or foreign recipient).
- **Notifiable privacy breaches:** the Commissioner is notified as soon as practicable once serious harm is reasonably believed (the OPC asks for 72 hours); the agency stays responsible and the agents must tell it of all breaches under contract, which the record does not hold (security-questionnaire.md; gap: contract term; counsel: serious harm).
- **Biometric Processing Privacy Code:** n/a: no voice or face processing in a web chat (R1, R2, R3).

## New Zealand: Sector, consumer and government AI policy

- **Consumer and human rights law:** Fair Trading Act ss 9, 12A and 13 engage because the agent answers refund and returns questions and offers store credit (R2); capability claims must cite M1 and M2; whether steering a customer to store credit instead of a statutory refund is misleading is open (counsel: Consumer Guarantees Act and Fair Trading Act; M1). Human Rights Act s 65: code-based eligibility rules could have indirect effects; no measurement by group (gap; impact-assessment.md; counsel).
- **Sector codes and clocks:** n/a: retail client, not a health, credit reporting or telecommunications agency (docs/discovery/customer-agent.md §1).
- **Government client:** n/a: private client; the MBIE Responsible AI Guidance (July 2025) is voluntary (source: adk-governance-pack reference new-zealand.md, read 2026-10-26; impact-assessment.md).
- **Māori data and engagement:** customers' names and addresses may include data about Māori; the engagement owner and any te reo content are not recorded (docs/discovery/customer-agent.md §3; gap: engagement owner).

## Singapore: PDPA and roles

- **No AI-specific statute:** no AI-specific statute applies in Singapore (MDDI, 7 July 2026; source: adk-governance-pack reference singapore.md, read 2026-10-26; checked 2026-10-26).
- **Consent or exception per purpose:** answering order and returns questions (R1, R2) is proposed as deemed consent by conduct or contractual necessity; evaluation sets built from transcripts (D3) is proposed under the business improvement exception or by notification, with the assessment kept; a later fine-tune would need fresh consent or an AI-Specific Notification (counsel: basis per purpose; gap: assessment IDs and owner; source: adk-governance-pack reference singapore.md, read 2026-10-26).
- **Transfer Limitation Obligation:** the client's duty for data held in Sydney (D2) and read from Sydney (D4), and for the Gemini endpoint (D1); Australia is not on any adequacy list, so a contract naming the countries or another listed mechanism is needed (transfer-assessment.md; counsel: mechanism; gap: contract).
- **Data breach notification:** data intermediary to client without undue delay; client assesses within 30 calendar days of credible grounds; PDPC notified within 3 calendar days of determining a breach notifiable, in force since 1 February 2021 (security-questionnaire.md; checked 2026-10-26; counsel: who leads).
- **Penalty cap and pending law:** up to S$1 million or 10% of annual Singapore turnover where that exceeds S$10 million, since 1 October 2022; a data intermediary can be penalised for its own protection and retention failures; data portability is not in force (checked 2026-10-26; source: adk-governance-pack reference singapore.md).

## Singapore: AI governance frameworks

- **Voluntary frameworks:** IMDA Model AI Governance Framework for Agentic AI v1.5 (published 20 May 2026) applies to a write-capable agent (R2); IMDA Transparency Guidelines for Generative AI Chatbots (20 July 2026) for an external chat agent; PDPC Advisory Guidelines on generative AI (20 July 2026) and on AI recommendation and decision systems (1 March 2024) (impact-assessment.md; system-card.md; checked 2026-10-26).

## Singapore: Sector and employment

- **Sector rules:** n/a: Kowhai is not a MAS-regulated, health or critical information infrastructure client (assumption: docs/discovery/customer-agent.md §1; counsel: confirm); Do Not Call n/a: marketing messages are out of scope (docs/architecture/customer-agent.md Scope gate); consumer protection law for refunds and store credit in Singapore is not covered by this pack (counsel: question).
- **Employment:** n/a: no staff monitoring or hiring use (R1, R2, R3).
- **Public agency client:** n/a: private client (docs/discovery/customer-agent.md §1).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| Australia | APP 1.7 to 1.9 privacy policy entries | 10 December 2026 (Privacy Act APP 1.7, checked 2026-10-26) | Inside the 6-week pilot if it starts on 2026-11-26; client rows n/a, consultancy position counsel |
| New Zealand | IPP 3A indirect collection notice | 1 May 2026 (Privacy Amendment Act 2025, checked 2026-10-26) | CRM read treated as direct collection; open for generated information |
| New Zealand | Access and correction within 20 working days | 24 September 2025 (Privacy Act 2020 s 44(1), s 63(1), checked 2026-10-26) | Transcripts and traces are searchable by customer ID only if a path exists (D3, D4; gap) |
| New Zealand | IPP 12(1)(e) replaced | 27 November 2025 (Privacy Act 2020, checked 2026-10-26) | Only if a party uses information for its own purposes |
| Singapore | Data breach notification, 3 calendar days to the PDPC | 1 February 2021 (PDPA, checked 2026-10-26) | Pilot incident clock |
| Singapore | Higher financial penalty cap | 1 October 2022 (PDPA, checked 2026-10-26) | Risk statement only |

- **AI literacy and staff training:** no training for service staff who receive handovers is recorded (C4; gap: proposed goal for adk-workflow-design).
- **Documents the client's own process produces:** New Zealand privacy impact assessment the OPC expects before AI tools are used (owner: Aroha Ngata; W2); Singapore DPIA, encouraged but not required, and the PDPA assessments for any deemed consent by notification, legitimate interests or business improvement basis (owner: Daniel Tan; W3); privacy-policy and notice text for both countries (owner: privacy officer and DPO; gap: no notice text in the record).

## Questions for counsel

- counsel: Is Southgate Labs only an s 11 agent for New Zealand data, or an agency in its own right (s 4(1)(b), s 11(3)), and is it a data intermediary for every step in Singapore, including evaluation sets; regime New Zealand and Singapore; facts at D3, D4; needed before W4 and the pilot decision.
- counsel: Does Sydney staff access to Singapore customers' traces and the Sydney hosting satisfy the Transfer Limitation Obligation, and does the written contract name Australia; regime Singapore; facts at D2, D4; gap: contract; needed before the pilot decision.
- counsel: Is reuse of transcripts to build evaluation sets (12 months, D3) within purpose for New Zealand (IPP 10), within business improvement or notification for Singapore, and within APP 6 for the consultancy's handling; facts at D3; needed before the pilot decision.
- counsel: Does Google's abuse monitoring or prompt retention count as use for its own purposes (s 11(3)) and does the Cloud agreement exempt Kowhai; facts at D1; gap: agreement terms; needed before the pilot decision.
- counsel: Does offering store credit instead of a refund breach the Fair Trading Act or Consumer Guarantees Act, and which Singapore consumer law applies; regime New Zealand and Singapore; facts at R2, M1; needed before the pilot decision.
- counsel: Does the Privacy Act 1988 reach Southgate Labs' handling of New Zealand and Singapore customers' data, and is the consultancy an APP entity; regime Australia; facts at D4; gap: consultancy turnover.
- counsel: Does the store credit decision significantly affect a customer for APP 1.7, and does it matter given customers are not in Australia; regime Australia; facts at C2.
- counsel: Are the steps taken before the agent uses order data "reasonable" for IPP 8 and sufficient for Singapore's accuracy duty, given M1 at 93% and M3 at 27% outdated addresses; facts at M1, M3.
- counsel: Are generated or inferred statements about a customer an indirect collection under IPP 3A; facts at D3, D5.
- counsel: Which entity is the exporter, and which assesses and notifies a breach, where the New Zealand company, the Singapore company, Southgate Labs and Google all hold the data; facts at D2, D4.
- counsel: Is the notifiable-breach assessment in each country led by the client, and what contract notice period binds the consultancy; facts at D4; gap: contract.
- counsel: Is customer data about Māori subject to a Te Tiriti or Māori data governance expectation the client should address; facts at docs/discovery/customer-agent.md §3.
- counsel: Are the incidental-visitor assumptions for United States, EU, UK and Canadian visitors safe; facts at docs/discovery/customer-agent.md §1.
- counsel: Which counsel reviews this pack for each country; gap: none named in the record; W4.

## Gaps and proposed goals

| Gap | Proposed goal and owner skill | Evidence |
| --- | --- | --- |
| Retirement date and processing region of `gemini-3.5-flash-001` not read from the model page | Read the model page and record both; adk-model-and-output-contracts | D1 |
| Abuse monitoring, caching, grounding and logging settings not recorded | Record the settings and whether Kowhai's agreement exempts abuse review; adk-model-and-output-contracts | D1 |
| Trace and Firestore session retention; D5 says no copy is kept while D3 and D4 retain transcripts and CRM fields | Decide and record retention and an erasure path per store; adk-agent-observability and protect-adk-sensitive-data | D3, D4, D5 |
| No sensitive-data screening evidence for free-text chat or traces | Measure masking coverage in prompts, logs and traces; protect-adk-sensitive-data | C1, D4 |
| No AI-disclosure contract in the design | Add a disclosure contract and test; adk-model-and-output-contracts | R3, C4 |
| Handover share and time to connect not measured | Add measures; adk-agent-evaluation | C4 |
| No written Kowhai to Southgate Labs data contract in the record | Client and consultancy contract with scope, countries, breach notice and deletion; client's counsel | D4 |
| Salesforce CRM region and any offshore access not recorded | Record region and support access; client IT | D5 |
| Evaluation set location, access and any use for other clients | Record where sets live and who reads them; adk-agent-evaluation | D3 |
| Security baseline rules beyond SB01, SB03, SB05 absent from the design table | Complete the baseline table; adk-agent-security | docs/architecture/customer-agent.md Security baseline |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy officer, Kowhai Retail Limited (Aroha Ngata) | New Zealand sections and shared sections of this document | pending | pending |
| Data Protection Officer, Kowhai Retail (Singapore) Pte. Ltd. (Daniel Tan) | Singapore sections and shared sections of this document | pending | pending |
| Counsel for Kowhai Retail (not named; gap) | Questions for counsel | pending | pending |
