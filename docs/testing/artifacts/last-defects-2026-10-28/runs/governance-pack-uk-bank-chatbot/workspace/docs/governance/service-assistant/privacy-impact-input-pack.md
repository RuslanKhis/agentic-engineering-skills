---
document: privacy-impact-input-pack
system: Thamesbridge customer service assistant
version: design accepted 2026-09-18, build v0.8.0
status: draft
jurisdictions: [au, eu, uk]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
owner: Thamesbridge Bank plc (controller for UK customers) and Thamesbridge Bank Ireland DAC (controller for Irish and EU customers); counsel: confirm roles
for: UK DPO (Oliver Grant) and Ireland DPO (Siobhán Kelly)
sources: docs/discovery/service-assistant.md, docs/architecture/service-assistant.md, docs/plans/service-assistant.md
---

# Privacy impact input pack: Thamesbridge customer service assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Inputs for Thamesbridge's data protection impact assessments of this system: the UK GDPR Article 35 DPIA for Bank plc, the GDPR Article 35 DPIA for Bank Ireland DAC, and the Australian privacy impact assessment for the consultancy's own handling, as the jurisdiction screen found them in scope. The two DPOs write and sign each assessment; this pack supplies the facts the design and plan record and the questions only counsel can answer. Not legal advice. The GDPR amendments in the Digital Omnibus were not law on 2026-10-26 and are treated as unamended (source: adk-governance-pack reference, read 2026-10-26).

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| EU and UK | WP248 rev.01 criterion 2, automated decision with legal or similar effect | counsel: yes for the engine, not the assistant | The engine decides declines; the assistant explains them | D3, C3 |
| EU and UK | WP248 criterion 4, special-category or highly personal data | yes | Financial data is highly personal; merchant names reveal health, religion and union payments | docs/discovery/service-assistant.md §3 |
| EU and UK | WP248 criterion 5, large scale | counsel: pilot 6,000 customers; contact centres take 610,000 chats and calls a month, so production is large scale | Pilot is small; the rollout is not | docs/discovery/service-assistant.md §1, §6 |
| EU and UK | WP248 criterion 6, matching or combining datasets | yes | Core banking, card platform and decision engine are combined in one answer | R1, R2, R3 |
| EU and UK | WP248 criterion 7, vulnerable data subjects | counsel: customers declined credit may be in financial difficulty | assumption: some pilot customers are vulnerable; gap: no vulnerability data in the record | docs/discovery/service-assistant.md §4 |
| EU and UK | WP248 criterion 8, innovative technology | yes | Generative model, Gemini 3.5 Flash | D1 |
| EU and UK | WP248 criterion 9, prevents using a service | no | The assistant adds a channel; agents remain available | docs/discovery/service-assistant.md §2 |
| UK | ICO list: innovative technology including AI, with another criterion; denial of service by ADM; special category data | yes | AI plus special-category-revealing data; declines are explained by the assistant | D1, D3 |
| Australia | OAIC threshold assessment: new or changed handling of personal information | yes | Engineers in Sydney read logs, traces and pseudonymised transcripts | D4, C5 |

Result: counsel: a DPIA is required in the EU and the UK on these facts and recommended in Australia; the DPOs decide; W2 already requires both DPOs' sign-off.

## Processing description

- **Purpose:** answer balance and transaction questions, freeze a card after confirmation and explain a declined overdraft, so more chats resolve without an agent (R1, R2, R3, docs/discovery/service-assistant.md §2).
- **Nature:** reads account, card status and decision reason-code data through APIs; sends them to a Gemini model to word answers; stores chat transcripts, logs and traces; pseudonymises transcripts for support (R1, R3, D1, C5).
- **Scope:** pilot of 5,000 UK and 1,000 Irish opted-in customers for 8 weeks; support by four Sydney engineers for six months (docs/discovery/service-assistant.md §5, §6, D4).
- **Context:** existing retail customers of a regulated bank using in-app chat, who expect their account data to be seen only by the bank and its suppliers; the existing menu bot resolves 22 % (docs/discovery/service-assistant.md §2).

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Customer message | Free text, which may name health, religion or union membership | App | Assistant service, London for UK and Belgium for EU | gap: session and retention period not recorded | gap: not recorded | gap: no input screening recorded | D2, C1 |
| Model request | Message, balances, transactions with merchant names, reason codes | Assistant service | Gemini 3.5 Flash on Vertex AI, endpoint in the serving region; processing region gap | gap: provider caching and abuse-monitoring retention not configured in the record | n/a: not stored by the client | gap: no masking of merchant names recorded | D1, D2 |
| Tool call, read | Balances, transactions, card status, decision reason codes | Assistant service | Core banking API, card platform API, CreditLens (location gap) | Not stored by the tool; source systems hold their own | yes in source systems | Scoped to the verified customer ID | C1, C3, D3 |
| Tool call, freeze | Card ID, customer confirmation | Assistant service | Card platform API | Card platform records the freeze | yes in source | Confirmation bound to the card ID | C2, D5 |
| Logs and traces | gap: content not recorded; likely messages and tool outputs | Assistant service | Logging sink in the traffic's region | gap: retention not recorded | gap: not recorded | gap: no log redaction recorded | D2 |
| Transcript copies | Chat text, pseudonymised | Assistant service | Support store, region gap | gap: retention not recorded | gap: pseudonym key holder not recorded | Pseudonymisation job; coverage not measured | C5, D4 |
| Consultancy access | Logs, traces and pseudonymised transcripts | Thamesbridge environment | Southgate Labs engineers, Sydney, six months | Not stored by Southgate Labs as far as recorded; gap: no download restriction recorded | n/a: access only | C5 covers transcripts only; gap: logs and traces | D4, C5 |
| Evaluation sets | Synthetic declined applications (500) and staff test chats (120) | Southgate Labs and Thamesbridge customer operations | Evaluation tooling | Not recorded | n/a: no customer data recorded | n/a: synthetic and staff data | M1, M3 |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| Pilot customers in the UK, Ireland and other EU countries | Identity from sign-in, balances, transactions, card status, overdraft decisions and reason codes, chat text | counsel: merchant names reveal health, religion and union payments; free text can state them | Core banking, card platform, decision engine, and the customer | docs/discovery/service-assistant.md §3 |
| People named in transactions (payees, merchants) | Names within transaction descriptions | counsel: may include individuals | Core banking | docs/discovery/service-assistant.md §3 |
| Southgate Labs engineers and contact-centre staff | Access logs and handover records | n/a: not assessed | Systems | D4; gap: no staff data flow recorded |

## Automated decisions

- **Facts:** the decision engine makes every decision and the assistant only explains reason codes (D3, R4, C3). gap: whether any person reviews a decline, who they are and the share and override rate are not in the record; no M record exists for this.
- **Explanation the design can produce:** the decision engine's reason codes for the customer's own application, worded by the model; mismatches with the reason codes were 0.8 % on 500 synthetic declined applications (C3, M1). gap: M1 used synthetic applications, not customer data; no counterfactual explanation is produced.
- counsel: EU Article 22 and Articles 13(2)(f), 14(2)(g) and 15(1)(h) for the engine's declines and what the assistant must say; UK Articles 22A to 22D, including the 22C safeguards (information, representations, human intervention, contest) and the Article 22B bar if special category data feeds the engine (D3; gap: engine inputs); Australian APP 1.7 n/a: the consultancy makes no decision about a person.

## Necessity and proportionality

- Each category is needed to answer the question asked: balances and transactions for R1, card status for R2, reason codes for R3 (R1, R2, R3). Scope is limited to the signed-in customer's own accounts (C1).
- Minimisation gap: the model receives merchant names that can reveal special categories; no control removes or masks them (docs/discovery/service-assistant.md §3; proposed goal for protect-adk-sensitive-data).
- Less intrusive alternative: the existing menu bot; the assistant lifts resolution from 22 % to a test figure of 41 % on 120 staff test chats, which is not comparable to customer traffic (docs/discovery/service-assistant.md §2, M3).
- Re-use: transcripts are copied for support (docs/discovery/service-assistant.md §3, C5); counsel: is support a compatible purpose, and is evaluation or improvement use planned (gap: not recorded).
- Informing people and rights: the chat header names the bank's assistant (D6); gap: notice text naming Google as recipient and Sydney access, access and erasure routes for transcripts, logs and traces, and the opt-in wording.

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| Session store | Conversation | gap: not recorded | gap: not recorded | D2 |
| Logs and traces | gap: content not recorded | gap: not recorded | gap: not recorded | D2 |
| Pseudonymised transcripts | Chat text with pseudonyms | gap: not recorded | gap: includes the key and any backups | C5 |
| Provider caches and abuse-monitoring storage | Prompts and outputs | gap: depends on configuration not recorded | n/a: not controlled by the client | D1 |

## Recipients and regions

| Recipient (processor, service provider, agent or data intermediary, in the regime's own word) | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| Google Cloud | Processor under the client's agreement (counsel: confirm) | London europe-west2 and Belgium europe-west1; model processing region gap | None recorded; counsel: UK to Belgium is covered by UK adequacy for the EEA and EU to London by the EU adequacy renewed 19 December 2025, read via a search extract (checked 2026-10-26) | D1, D2 |
| Southgate Labs | Processor during build and support; APP entity in its own right in Australia (counsel: confirm) | Sydney, Australia | Restricted transfer for UK and EU data; no UK or EU adequacy for Australia; IDTA or Addendum and SCCs needed (transfer-assessment.md; W4); gap: no contract is in the record | D4 |
| CreditLens (decision engine vendor) | gap: role and hosting region not recorded | gap | gap | D3 |
| Thamesbridge Bank plc and Bank Ireland DAC | Controllers; group transfers between them are gap | UK and Ireland | counsel: which entity exports (transfer-assessment.md) | docs/discovery/service-assistant.md §1 |
| Australia: overseas disclosure facts | The flow is into Australia, so APP 8 is not engaged by access from Sydney (counsel: confirm) | Australia | n/a: inbound | D4 |

## Model provider data use

- Model and endpoint: gemini-3.5-flash-001 pinned on Vertex AI in the serving region (D1). gap: the model's processing region as the model page lists it, caching setting, grounding use and abuse-monitoring exemption are not recorded and could not be read without network access; proposed goal for adk-model-and-output-contracts.
- Provider terms read on 2026-10-25 by the skill's references: Google does not use customer data to train without permission, implicit caching is on by default for up to 24 hours unless disabled, abuse monitoring can store flagged prompts up to 90 days in the project region and may involve human review, and regional endpoints keep cached data in the location (source: adk-governance-pack reference, read 2026-10-25; not re-read for this draft).
- counsel: reliance on Google's documentation that the model was not developed unlawfully (EDPB Opinion 28/2024) and whether Google is a controller for abuse monitoring (D1).

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| Another customer's balance or transactions shown | assumption: unlikely and severe | Tool scoped to the verified customer ID | in place, tested locally (G01/A2); not measured on real traffic | C1, docs/discovery/service-assistant.md §4 |
| Misleading explanation of a declined overdraft | assumption: possible, moderate to severe | Reason-code-only tool, output validator, fixed message and handover | in place, tested locally; 99.2 % match on 500 synthetic applications | C3, C4, M1 |
| Card frozen in error, or fraud left running | assumption: possible, moderate | Confirmation bound to the card ID | in place, tested locally; 0 unconfirmed freezes in 300 scripted conversations; missed freezes not measured | C2, M2 |
| Special-category inference from merchant names sent to the model and logs | assumption: likely, moderate | None recorded | gap: proposed goal for protect-adk-sensitive-data | docs/discovery/service-assistant.md §3 |
| Sydney engineers see identifiable data in logs and traces | assumption: possible, severe | Pseudonymised transcripts only | partly in place for transcripts (G04/A1, tested locally, coverage unmeasured); gap: logs and traces | C5, D4 |
| Pseudonymised transcripts re-identified | assumption: possible, moderate | Pseudonymisation job | gap: re-identification test and key custody not recorded | C5 |
| Over-reliance on the assistant by customers in financial difficulty | assumption: possible, moderate | Cannot promise or change credit outcomes | in place, tested locally | C4, R4 |
| Invisible processing: customers unaware of Google and Sydney access | assumption: likely without notice | Chat header disclosure only | gap: notice text | D6 |
| Memory and purpose creep (ICO agentic risks) | assumption: unlikely | No memory beyond transcripts recorded | gap: confirm no cross-session memory | D2 |

## Australia: APP compliance check

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection | Southgate Labs collects nothing from customers directly; it views the bank's logs and transcripts | counsel: is viewing a collection, and does the Act reach UK and EU customers' data | D4 |
| APP 5 notice | n/a: no Australian individuals | counsel: confirm n/a | docs/discovery/service-assistant.md §3 |
| APP 6 use and disclosure | Use only for support under the client's instruction (assumption) | gap: contract terms | D4 |
| APP 8 and s 16C overseas recipients | Inbound flow to Australia, not an Australian disclosure overseas | counsel: use or disclosure not engaged | D4 |
| APP 10 quality; APP 11 security and destruction | Build SB01, SB03, SB05 evidenced locally | gap: destruction of data held in Sydney at the end of the six months | SB01, SB03, SB05 |
| APP 12 and 13 access and correction | n/a: the consultancy holds no Australian individuals' information | counsel: confirm | D4 |

- **PIA required?** recommended for the consultancy's handling; not required (counsel: not a Commonwealth agency project).

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| UK and EU customers' account data and chat text, viewed as logs, traces and pseudonymised transcripts | Supporting the assistant for the bank | The bank's systems | Southgate Labs engineers | Australia (viewing location) | gap: not recorded | D4, C5 |

- **Proposed privacy-policy addition for Southgate Labs:** "We may view UK and EU bank customers' pseudonymised chat transcripts, logs and traces from Australia to support a client's service" (system-card.md; counsel: confirm).

## EU: Legal basis

- counsel: answering balance and transaction questions and freezing a card, candidate basis Article 6(1)(b) contract (account service) or 6(1)(f); why it may fit: the customer asked in the app (R1, R2).
- counsel: explaining a declined overdraft, candidate basis 6(1)(b) or 6(1)(f); why it may fit: the explanation supports transparency to the applicant (R3, D3).
- counsel: support analysis of pseudonymised transcripts, candidate basis 6(1)(f); why it may fit: running and fixing the service (C5, D4); whether the pilot opt-in is also consent is counsel: (docs/discovery/service-assistant.md §6).
- counsel: Article 9 condition for special-category data revealed by merchant names or free text; no Article 4a AI Act bias-detection use is planned (docs/discovery/service-assistant.md §3).

## United Kingdom: Lawful basis and ADM safeguards

- counsel: the same purposes with candidate bases Article 6(1)(b) and 6(1)(f); Article 6(1)(ea) recognised legitimate interest does not fit these purposes (R1, R2, R3).
- **Article 22C safeguards, if a decline is a solely automated significant decision:** information about the decision is the assistant's explanation (C3); gap: how the person makes representations, human intervention and the contest route are not recorded; R4 bars the assistant from promising an outcome (C4).
- **Complaints process (DPA 2018 s 164A):** gap: the client's process and the 30-day acknowledgement are not recorded (system-card.md).
- **ICO agentic risks:** controllership across the supply chain, ADM, special category inference, invisible processing, security and memory appear as rows in Risks and measures (D1, D3, D4).

## Questions for counsel

- counsel: are the controller roles per entity right, and is Google processor-only; regimes EU and UK; needed by W2.
- counsel: lawful basis and Article 9 condition per purpose, and whether the opt-in is consent; regimes EU and UK; needed by W2.
- counsel: do Article 22 and Article 22A apply to the engine's declines, and are the safeguards the assistant must support defined; regimes EU and UK; needed by W2.
- counsel: is the pseudonymised transcript personal data for each party; regimes EU and UK; needed by W4.
- counsel: is Article 36 prior consultation needed if residual risk is high; regimes EU and UK; needed by W5.
- counsel: does the Privacy Act reach Southgate Labs' handling of this data; regime Australia; needed by W3.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| UK DPO (Oliver Grant) | UK sections and common sections | pending | pending |
| Ireland DPO (Siobhán Kelly) | EU sections and common sections | pending | pending |
| Thamesbridge counsel for the UK and Ireland (not named: gap) | counsel: items | pending | pending |
