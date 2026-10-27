---
document: privacy-impact-input-pack
system: Kowhai Retail customer agent
version: design accepted 2026-09-09; build v0.6.1 (M1, M2)
status: draft
jurisdictions: [au, nz, sg]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
owner: Kowhai Retail Limited (Auckland; agency for New Zealand customers) and Kowhai Retail (Singapore) Pte. Ltd. (organisation for Singapore customers); which entity is exporter of each transfer is counsel's
for: privacy officer (Aroha Ngata) and Data Protection Officer (Daniel Tan)
sources: docs/discovery/customer-agent.md, docs/architecture/customer-agent.md, docs/plans/customer-agent.md
---

# Privacy impact input pack: Kowhai Retail customer agent

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Inputs for Kowhai Retail's privacy assessments of this system: the New
Zealand privacy impact assessment the Privacy Commissioner expects, a
Singapore data protection impact assessment and the PDPA's required
assessments, and, for the consultancy's own handling only, an Australian
privacy impact assessment. The client writes and signs each assessment; this
pack supplies the facts the design and plan record and the questions only
counsel can answer. Not legal advice.

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| Australia | OAIC threshold assessment: new or changed handling of personal information | yes | Southgate Labs engineers in Sydney read traces that include CRM fields | D4 |
| New Zealand | OPC expects a PIA before using AI tools | yes | A generative agent reads customer order history and writes store credit | D1, D5, R2 |
| Singapore | DPIA encouraged, not required; deemed consent by notification, legitimate interests and business improvement assessments are required where relied on | yes | Transcripts are reused to build evaluation sets; assessments are not recorded | D3 |

Result: counsel: a New Zealand PIA recommended and a Singapore DPIA recommended; an Australian PIA recommended for the consultancy only; the privacy officer and the DPO decide (W2, W3).

## Processing description

- **Purpose:** answer order and returns questions and issue store credit for eligible returns in web chat, to raise the share of enquiries resolved without an agent from an 18% baseline (R1, R2, docs/discovery/customer-agent.md §2).
- **Nature:** reads customer profile and order history from Salesforce at the time of the question, composes answers with a model, writes a store credit, keeps transcripts for 12 months and reuses them to build evaluation sets; engineers read traces (D5, R2, D3, D4).
- **Scope:** signed-in web chat customers in New Zealand and Singapore for 6 weeks; the service handles 22,000 enquiries a month across both countries; the pilot population is not recorded (gap) (docs/discovery/customer-agent.md §1, §6).
- **Context:** existing customers whose data Kowhai collected through shops and its loyalty programme; they have not been told the data is used by an AI agent or reused for evaluation (docs/discovery/customer-agent.md §3; gap: no notice text recorded).

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Customer prompt | Name, order references, free text which may hold more | Browser of a signed-in customer | Cloud Run, australia-southeast1 | Yes, in the transcript, 12 months | gap: no lookup path recorded | gap: no screening evidence | D2, D3 |
| CRM read | Name, email, phone, address, orders, returns | Salesforce CRM | Cloud Run, australia-southeast1 | D5 says no copy is kept; the data reappears in traces (D4), so retention is a gap | gap | Tool scoped to verified customer ID | C1, D5, D4 |
| Model request | Prompt and CRM fields returned by tools | Cloud Run | Gemini endpoint, australia-southeast1; processing region unread (gap) | Provider retention unread (gap) | n/a: not stored by the client | gap: no screening evidence | D1 |
| Credit write | Customer ID, return ID, amount | Cloud Run | Salesforce CRM ledger; region not recorded (gap) | Ledger retention is Kowhai's own | yes, in the CRM | Limit and eligibility in code; idempotency key | C2, C3, W1 |
| Logs and traces | Prompts and CRM fields returned by tools | Cloud Run | Logs in australia-southeast1 | gap: trace retention not recorded | gap | gap | D2, D4 |
| Evaluation sets | Transcripts | Firestore | gap: location and holder not recorded | gap | gap | gap: pseudonymisation not recorded | D3 |
| Consultancy access | What traces show, CRM fields included | Client environment | Southgate Labs engineers, Sydney, Australia | During the pilot and a six-month support period | n/a: staff read, not search | gap: no masking recorded | D4 |
| Handover | Conversation context | Cloud Run | Service queue in the customer's country, or callback form | gap | gap | none recorded | C4 |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| Customers in New Zealand and Singapore, signed in | Name, email, phone, address, orders, returns, store credit ledger, chat transcripts | None recorded; free text could hold more (counsel; New Zealand has no statutory sensitive category, Singapore has data classes deemed significant harm) | CRM (Kowhai collected it through shops and the loyalty programme); chat (from the person); generated answers (generated) | docs/discovery/customer-agent.md §3 |

## Automated decisions

- **Facts:** code checks eligibility and the limit and issues the credit with no person approving it; a person receives a handover only on request; handover share and override rate are not measured (C2, C4; gap).
- **Explanation the design can produce:** gap: no contract records an explanation of why a credit was refused; the refusal outcome is a handover (C2).
- counsel: New Zealand IPP 8 accuracy before use (no automated-decision rule); Singapore accuracy (s 23) and the PDPC's recommended disclosures (no automated-decision provision); APP 1.7 for the consultancy only.

## Necessity and proportionality

- The CRM read is limited to the verified customer's own records and no copy is kept by the agent design (C1, D5); assumption: the data categories read are needed for order and returns answers, and the record does not list which CRM fields the tool returns (gap).
- Less intrusive alternative: reading order status only without address or phone; not recorded as considered (D5; gap; proposed goal for safe-api-tool-calls).
- Reuse of transcripts: original purpose was answering the customer's enquiry; reuse to build evaluation sets is the purpose in D3; no consent or notice is recorded (D3; counsel: compatible, directly related, or business improvement).
- People are informed through notices naming Google and Southgate Labs as recipients, the 12-month transcript retention, Sydney processing and the evaluation reuse; no notice text exists in the record (gap); access, correction and erasure reach transcripts only if a path exists (D3; gap).

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| Transcripts (Firestore) | Chat conversations | 12 months | gap: not recorded | D3 |
| Evaluation sets | Transcripts reused | gap: not recorded | gap | D3 |
| Traces and logs | Prompts and CRM fields returned by tools | gap: not recorded | gap | D4 |
| Model provider caches and abuse-monitoring store | Prompts | gap: not read (provider page up to 90 days for flagged prompts, source: adk-governance-pack reference privacy-and-records.md, read 2026-10-25) | gap | D1 |
| Salesforce CRM | Profile, orders, ledger | Kowhai's own retention | Kowhai's own process | D5 |

## Recipients and regions

| Recipient (agent, data intermediary or service provider, in the regime's own word) | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| Google Cloud (Cloud Run, Firestore, logs, Vertex AI) | New Zealand: s 11 agent proposed; Singapore: data intermediary proposed; Australia: n/a for the client | australia-southeast1, Sydney | transfer-assessment.md rows; counsel: agent or foreign recipient; gap: Cloud agreement terms | D1, D2 |
| Southgate Labs | New Zealand: s 11 agent proposed; Singapore: data intermediary proposed; Australia: consultancy, APP entity status counsel | Sydney, Australia | transfer-assessment.md; gap: written contract | D4 |
| Salesforce | gap: role and region not recorded | gap | gap | D5 |

## Model provider data use

- Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI, endpoint in australia-southeast1; the model's processing region, any training use of prompts, abuse-monitoring logging, caching and zero data retention status are not recorded and the model page could not be read in this session (D1; gap: proposed goal for adk-model-and-output-contracts).
- Provider statements as read in the skill reference: Google does not train on customer data without permission; implicit caching is on by default and deleted within 24 hours; flagged prompts can be stored up to 90 days in the project's region and reviewed by people (source: adk-governance-pack reference privacy-and-records.md, pages updated 22 October 2026, read 2026-10-25; not re-read). Whether Kowhai's agreement exempts it is open (counsel).

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| Another customer's order or personal data appears in an answer or credit is issued to the wrong customer | assumption: low likelihood, high severity | Tool scoped to verified customer ID | in place, tested locally | C1, G01/A2 |
| Credit above limit or for an ineligible return | assumption: low likelihood, medium severity | Eligibility and limit in code; idempotency key | in place, tested locally; M2: 0 in 200 scripted conversations | C2, C3, M2 |
| Wrong delivery or returns answer or an outdated address used | assumption: medium likelihood, medium severity | Order status from CRM at question time; 93% correct on 300 test chats; 27% of test customers have an address older than 24 months | in place, tested locally; address freshness not controlled (gap) | M1, M3, D5 |
| Customer data retained in traces, logs and evaluation sets beyond need | assumption: medium likelihood, medium severity | none recorded | gap: retention and masking; proposed goals for protect-adk-sensitive-data and adk-agent-observability | D3, D4 |
| Offshore access by Sydney engineers without a comparable contract | assumption: medium likelihood, medium severity | none recorded | gap: contract | D4 |

## Australia: APP compliance check

Scope: the consultancy's own handling only; the client's own APP rows are n/a: the client's customers are not in Australia (docs/discovery/customer-agent.md §3).

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection | Southgate Labs reads traces that include CRM fields | counsel: collection or use of information held for the client | D4 |
| APP 5 notice | n/a: no notice is given by the consultancy to customers | counsel: whether any notice duty arises | D4 |
| APP 6 use and disclosure | Transcripts reused to build evaluation sets | counsel: secondary purpose | D3 |
| APP 8 and s 16C overseas recipients | Hosting and endpoint in Australia; gap: processing region of the model | counsel: use or disclosure; gap: model page | D1, D2 |
| APP 10 quality; APP 11 security and destruction | Salesforce credential and API routes built; ADK runtime hardening deferred to production; destruction path not recorded | gap: retention; deferred: production for the runtime | SB01, SB03, SB05 |
| APP 12 and 13 access and correction | Evaluation sets and traces may be held information | gap: path | D3, D4 |

- **PIA required?** Recommended, not required for a private entity (counsel: confirm the Act applies to the consultancy; source: adk-governance-pack reference australia.md, read 2026-10-26).

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Customer profile and order history fields returned by tools, in traces | Support and troubleshooting of the agent during the pilot and six-month support period | Client's CRM | Southgate Labs engineers | None for Southgate Labs (Sydney); gap for Google | gap | D4, D5 |
| Chat transcripts | Evaluation of the agent | The customer, generated answers | Southgate Labs engineers; gap: others | None; gap | 12 months | D3 |

- **Proposed APP 5 notice and privacy-policy additions, including APP 1.8 entries:** for the consultancy's own policy only: it handles client customer data under contract in Sydney to build, evaluate and support a customer agent; whether APP 1.8 applies is counsel (system-card.md; counsel: confirm).

## New Zealand: IPP compliance check

| IPP (or the code rule that replaces it) | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| IPP 1 necessary for a lawful purpose; IPP 4 fair means (children) | Purpose is answering the customer's order and returns enquiries; no children recorded | gap: which CRM fields are necessary; assumption: no children in the pilot | R1, docs/discovery/customer-agent.md §3 |
| IPP 5 security, and 5(b) for each service provider | Route scoping, credential handling in build; runtime hardening deferred | gap: contract terms with Google and Southgate Labs; deferred: production for the runtime | SB01, SB03, SB05 |
| IPP 6 and 7 access and correction (20 working days) | Transcripts and traces hold customer data | gap: how a request reaches Firestore, traces and evaluation sets | D3, D4 |
| IPP 8 accuracy before use | 93% correct order status on 300 test chats; 27% of test customers have an address older than 24 months | counsel: steps reasonable? | M1, M3 |
| IPP 9 retention; IPP 10 use of existing data; IPP 11 disclosure | Transcripts 12 months and reused to build evaluation sets; Sydney engineers read traces | counsel: directly related purpose? | D3, D4 |
| IPP 12 and s 11 (agent or foreign recipient) | Google and Southgate Labs hold data in Sydney for Kowhai | counsel: agent or recipient; own-purpose use unread | D1, D4 |
| IPP 13 unique identifiers | Customer and loyalty numbers may appear in outputs | gap: not recorded | C1 |
| Biometric Processing Privacy Code rules 1, 3 and 10 | n/a: no biometric processing in web chat | n/a: no voice or face | R1 |

## New Zealand: Collection and notice inputs

| Source | Direct (IPP 3) or indirect (IPP 3A) | Collected after IPP 3A began? | Who notifies | Exception relied on, with its documented rationale | Evidence |
| --- | --- | --- | --- | --- | --- |
| Customer chat | Direct | yes (from 1 May 2026, checked 2026-10-26; chat begins at pilot) | Kowhai Retail Limited as agency, not the agents | none; gap: no notice text | R1, docs/discovery/customer-agent.md §3 |
| Salesforce CRM read | Direct at the time Kowhai collected it through shops and the loyalty programme; assumption: reading its own CRM is not indirect collection | no (collected before) | Kowhai Retail Limited | none; counsel | D5 |

- **Proposed notice text, overseas recipients and the opt-out for training or evaluation use of transcripts:** "This assistant is an AI. Your chat and order details are processed by Google Cloud in Sydney, Australia, and read by our technology partner Southgate Labs in Sydney to run and improve the service; we keep chats for 12 months and may use them to test the assistant. You can ask for a person at any time." The opt-out route is a gap (system-card.md; counsel: confirm).

## Singapore: PDPA obligations check

| Purpose or obligation | Basis or how it is met (consent, deemed consent, exception with its Schedule paragraph) | Assessment kept (ID and owner) | Client or data intermediary | Evidence |
| --- | --- | --- | --- | --- |
| Answering order and returns enquiries | Proposed: deemed consent by conduct or contractual necessity; counsel: basis | n/a: no notification-based assessment needed if conduct or necessity holds; counsel | Client | R1, R2 |
| Evaluation sets built from transcripts | Proposed: business improvement exception or deemed consent by notification; counsel: not a significant departure while no training or fine-tuning occurs; assumption: no fine-tuning (D1) | gap: assessment ID and owner | Client; consultancy only if it reuses outside the contract | D3 |
| Access and correction (30 days; RAG stores in scope) | gap: how a request reaches Firestore, traces and evaluation sets | n/a: | Client; intermediary assists | D3, D4 |
| Protection and retention (prompts, outputs, agent activity data) | Route scoping and credential handling built; retention gap | n/a: | Both | SB01, SB03, D3 |
| Transfer Limitation Obligation | transfer-assessment.md | n/a: | Client, also for its intermediaries' transfers | D2, D4 |

## Singapore: Notification and policy inputs

- **Notification text and the four AI recommendation and decision items (function, data types, relevance, influential features):** function: answers order and returns questions and issues store credit within a limit; data types: name, contact details, orders, returns, store credit; relevance: eligibility is checked in code against the order and return record; influential features: the return record and the per-order limit (system-card.md; C2, D5; counsel: confirm).
- **AI-Specific Notification, if any model is trained or fine-tuned on user data:** n/a: retrieval and prompting only; assumption: no fine-tuning is recorded (D1).
- **Legitimate interests disclosure and contact, if relied on:** n/a: not proposed as a basis.
- **Written policies (fairness, safeguards, human oversight) and the DPO's business contact:** gap: no policy or published contact for Daniel Tan is in the record.

## Questions for counsel

- counsel: Is reuse of transcripts to build evaluation sets allowed for each country without fresh consent or an opt-out, regime New Zealand, Singapore and Australia, needed by W2, W3 and W4.
- counsel: Does the Sydney hosting and engineer access need a contract naming Australia and a comparable standard, regime Singapore, needed by W3.
- counsel: Are the CRM address age (M3) and the 93% accuracy (M1) enough "reasonable steps" for accuracy, regime New Zealand and Singapore, needed by W2 and W3.
- counsel: Does Google act only for Kowhai, regime New Zealand and Singapore, needed by W4.
- counsel: Does the consultancy fall under the Privacy Act for the traces it reads, regime Australia, needed by W4.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy officer, Kowhai Retail Limited (Aroha Ngata) | New Zealand sections and shared sections of this document | pending | pending |
| Data Protection Officer, Kowhai Retail (Singapore) Pte. Ltd. (Daniel Tan) | Singapore sections and shared sections of this document | pending | pending |
