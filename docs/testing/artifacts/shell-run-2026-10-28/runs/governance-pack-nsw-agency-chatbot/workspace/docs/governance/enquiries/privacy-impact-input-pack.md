---
document: privacy-impact-input-pack
system: Public enquiries assistant
version: design accepted 2026-09-15, build v0.7.0
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
owner: NSW Trades Licensing Office (public sector agency); Southgate Labs Pty Ltd as contracted service provider
for: Privacy officer (Sam Taylor)
sources: docs/discovery/enquiries.md, docs/architecture/enquiries.md, docs/plans/enquiries.md, docs/contract/order-form-summary.md, regulatory-memo.md
---

# Privacy impact input pack: Public enquiries assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Inputs for the Office's privacy impact assessment under the PPIP and HRIP Acts and the IPC's guide to PIAs on AI systems. The Office writes and signs the assessment; this pack supplies the facts the design and plan record and the questions only counsel can answer. Not legal advice.

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| Australia, OAIC | Threshold assessment: new or changed handling of personal information | yes | Real application status data and transcripts are handled (docs/architecture/enquiries.md Scope gate) | D2, D3 |
| Australia, NSW agency | IPC: a PIA is typically required when an AI system handles personal information; expected, not statutory | yes | Status lookups and free-text transcripts hold personal information (docs/discovery/enquiries.md §3); source: adk-governance-pack reference au-government-crosswalks.md, read 2026-10-26 | C2, D3 |

Result: counsel: a PIA is recommended and, on the IPC's expectation, required before the pilot; the privacy officer decides (W4).

## Processing description

- **Purpose:** answer licensing enquiries from published guidance and let a caller check their own application's status (R1, R2).
- **Nature:** the model drafts answers from guidance (C1); a tool reads status from the licensing system after number and date of birth match (C2); transcripts are stored and reviewed for quality (D3); Google applies abuse monitoring (D4).
- **Scope:** the Office handles about 48,000 calls and web enquiries a month, with 17,500 calls a month about application status (docs/discovery/enquiries.md §1, §2); the pilot covers the "Apply for a licence" pages for six weeks (docs/discovery/enquiries.md §6); gap: expected pilot chat volume is not recorded.
- **Context:** members of the public who expect licensing information from a government agency (docs/discovery/enquiries.md §1); the status lookup returns another person's information if matched wrongly (docs/discovery/enquiries.md §4).

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Caller message | free text: names, addresses, possibly health and criminal-history disclosures | browser | Cloud Run agent, australia-southeast1 | transcript, 90 days | gap: no search by person recorded | gap: no screening of free text recorded | D2, D3, docs/discovery/enquiries.md §3 |
| Model request | message and guidance context | agent | Gemini on Vertex AI, endpoint australia-southeast1; processing region gap | provider retention gap; abuse-monitoring storage not recorded | n/a: not stored by the client | none recorded | D1, D4 |
| Status lookup | application number, date of birth; returns stage and missing documents | agent | licensing system API (read) | not stored beyond transcript | n/a: the transcript holds what the agent said | C2 match, C3 limit of three failed lookups | C2, C3, SB03, M2 |
| Transcripts | all of the above | agent | Firestore, australia-southeast1 | 90 days, then deleted | gap | gap | D2, D3 |
| Logs | request and response metadata; content gap | Cloud Run | Cloud Logging, australia-southeast1 | gap: log retention not recorded | gap | gap: SB14 not in the design's baseline table | D2 |
| Handover | transcript and contact details given | agent | contact-centre queue or callback form | gap: queue retention not recorded | gap | none recorded | C4 |
| Consultancy access | transcripts and logs | Firestore and Cloud Logging | Southgate staff in Sydney and one support engineer in Brisbane | n/a: access, not copy; gap: whether staff download data | n/a: access control | gap: access controls and logging of staff access | D5 |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| Applicants for trade licences in NSW | application number, date of birth, stage, missing documents | none recorded for status; counsel: the missing-documents field may reveal a criminal-history or medical document | licensing system API (read) | docs/discovery/enquiries.md §3, C2 |
| Members of the public typing in chat | names, addresses, free text | health and criminal-history disclosures may be typed (health information under the HRIP Act; counsel: s 19(1) sensitive information) | from the person | docs/discovery/enquiries.md §3 |
| Southgate staff | access records | none recorded | generated | D5 |

## Automated decisions

- **Facts:** n/a: the assistant makes no decision about a person; it cannot decide or change applications (docs/architecture/enquiries.md Scope gate); no human review share is recorded because there is no decision (C2, M2).
- **Explanation the design can produce:** a guidance answer carries its source link (C1); a failed status lookup returns "we couldn't find that application" without a reason (C2).
- counsel: n/a: no decision about a person; confirm that IPP 9 accuracy before use is met by C1 and M1 and that no output feeds an administrative decision under an Act.

## Necessity and proportionality

- Date of birth and application number are the minimum for matching; no other identifier is asked (R2, C2).
- Transcript retention of 90 days is for quality review (D3); gap: whether review needs full-content transcripts or could use redacted ones; counsel: is 90 days necessary for the purpose.
- Less intrusive alternative: a web status page behind a login was not recorded as considered; gap: record why chat was chosen (docs/discovery/enquiries.md §2 states the outcome measure only).
- Re-used data: none; guidance is public and status data is read in place (docs/discovery/enquiries.md §3).
- How people are informed and exercise rights: gap: no AI disclosure, s 10 notice or privacy-collection text is recorded as a contract (C1 to C4 do not cover it); proposed notice text is below; access, correction and deletion of transcripts has no recorded path.

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| Firestore transcripts | conversation | 90 days, then deleted | gap: deletion mechanism and request path not recorded | D3 |
| Cloud Logging | request metadata | gap: not recorded | gap | D2 |
| Contact-centre queue | handover | gap: not recorded | gap | C4 |
| Google abuse-monitoring store | prompts and outputs as configured by default | not recorded | not recorded | D4 |

State record: agency: the disposal authority and whether 90 days meets it (records manager Fiona Lee, docs/discovery/enquiries.md §5; W4).

## Recipients and regions

| Recipient (processor, service provider, agent or data intermediary, in the regime's own word) | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| Google Cloud: hosting, Firestore, Cloud Logging | subcontractor to Southgate | australia-southeast1, Sydney | none outside NSW recorded; counsel: use under the contract | D2, `docs/contract/order-form-summary.md` |
| Google: Gemini model processing | subcontractor to Southgate | gap: model page's processing region not read | counsel: use or disclosure, and s 19(2) ground, if outside NSW | D1 |
| Google: abuse monitoring | subcontractor | gap: where it happens is not recorded | counsel: as above; gap for adk-model-and-output-contracts | D4 |
| Southgate Labs, Sydney | contracted service provider | Sydney, NSW | use for the contracted service (counsel: confirm) | D5 |
| Southgate Labs, Brisbane support engineer | contracted service provider | Brisbane, Queensland: outside NSW | counsel: use or disclosure; s 19(2) and HPP 14 ground; agency: whether the Order Form (item 14, Australia) permits it | D5, `docs/contract/order-form-summary.md` |

## Model provider data use

- Model `gemini-3.5-flash-001` on Vertex AI in australia-southeast1 (D1); abuse monitoring applies with default settings (D4). gap: whether prompts and outputs are retained or used for training, and where abuse monitoring processes them, are not recorded; proposed goal for adk-model-and-output-contracts to read Google's data-use terms and model page and record the date; not re-read on 2026-10-28 (no web access).
- counsel: whether the agency may rely on provider statements for what the model was trained on.

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| Status for the wrong application disclosed to another person | assumption: low likelihood after C2 and C3, high severity (docs/discovery/enquiries.md §4) | match on number and date of birth; three failures block lookups | in place, tested locally: 0 mismatched lookups returned in 250 scripted attempts | C2, C3, M2 |
| Wrong or misleading guidance leads to unlicensed work | assumption: moderate likelihood, moderate severity | answers cite a guidance page; handover | in place, tested locally: 94% of answers cited a correct page on 400 historical enquiries; 6% did not, and no live measure exists | C1, M1 |
| Health or criminal-history disclosures retained in transcripts, logs and abuse-monitoring stores | assumption: moderate likelihood, high severity | none recorded | gap: no screening or redaction goal; proposed goal for protect-adk-sensitive-data | D3, D4 |
| Access outside NSW by support staff or Google | assumption: moderate | contract and access limits | gap: no access control or logging evidence | D4, D5 |
| Transcripts kept longer than the disposal authority allows, or deleted too early | assumption: low | 90-day deletion | planned: agency to confirm authority (W4) | D3 |
| Breach of transcripts or credentials | assumption: low | credential handling and runtime baseline | in place, tested locally for SB01, SB03, SB05; other baseline rules not listed: gap | SB01, SB03, SB05 |

## Australia: APP compliance check

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection | Southgate collects through the agency's chat as its contracted service | counsel: s 7B(5) covers it; the agency's own collection is under the IPPs below | D5 |
| APP 5 notice | n/a: the agency gives the notice for its own collection | agency: see the proposed notice below | D5 |
| APP 6 use and disclosure | Southgate's own reuse of transcripts for its own purposes is not recorded | counsel: confirm none, and that the contract forbids it | D3 |
| APP 8 and s 16C overseas recipients | all recorded processing is in Australia | counsel: use or disclosure if the model or abuse-monitoring processing is overseas | D1, D4 |
| APP 10 quality; APP 11 security and destruction | 90-day deletion; three baseline rules listed | gap: destruction evidence and remaining baseline rules | D3, SB01 |
| APP 12 and 13 access and correction | the agency holds the transcripts | n/a: the agency answers requests under the IPPs | D3 |

- **PIA required?** counsel: recommended for the consultancy's own handling; the agency's PIA is in the NSW check below (D5).

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Application number and date of birth | status lookup | the person | licensing system, Southgate staff | none recorded; gap for the model and abuse monitoring | 90 days in transcripts | C2, D3 |
| Chat free text | answer enquiries; quality review | the person | Google Cloud, Southgate staff | gap | 90 days | D3, D5 |
| Status result | tell the caller | licensing system | Google model, transcript | gap | 90 days | C2, D3 |

- **Proposed notice and privacy-policy additions:** "You are chatting with an automated assistant for the NSW Trades Licensing Office. It answers from the Office's published guidance and can check your application status if you give the number and date of birth. Please don't type health or criminal-history details. Conversations are kept for 90 days for quality review and may be seen by the Office's service provider's staff." Text is a proposal only (docs/discovery/enquiries.md §3, D3, D5); counsel: confirm, and add where the model and abuse monitoring process data once known.

## Australia: NSW IPP and HPP check

| IPP / HPP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| IPP/HPP 1 Lawful; IPP 2 / HPP 3 Direct (generated outputs are "collection through creation") | information comes from the person and the licensing system (docs/discovery/enquiries.md §3); generated answers are transcripts | counsel: collection is necessary for the Office's function | D3, C2 |
| IPP 3 / HPP 4 Open (s 10 notice; chatbot notice during the conversation) | no notice or AI disclosure contract recorded | gap: notice at the time of the conversation; proposed text above | C1 |
| IPP 4 / HPP 2 Relevant; IPP/HPP 9 Accurate | only number and date of birth requested; 94% correct citation on 400 historical enquiries | counsel: accuracy steps reasonable; live accuracy gap | C2, M1 |
| IPP/HPP 5 Secure (retention to State Records Act minimums; contract terms) | 90-day deletion; three baseline rules listed | gap: logging, encryption and access evidence; agency: disposal authority (W4); counsel: contract terms | D3, SB01, SB03, SB05 |
| IPP/HPP 6 to 8 Transparent, Accessible, Correct (privacy management plan update) | no access or correction path for transcripts recorded | agency: privacy management plan update should cover AI use (W4); gap: access and correction path | D3 |
| IPP/HPP 10 Limited use; IPP 11 Restricted disclosure (vendor access for the contracted service is likely a use) | Southgate staff can read transcripts and logs for support (D5) | counsel: use or disclosure | D5 |
| IPP 12 Safeguarded and s 19(2); HPP 14 (any recipient outside NSW, including other Australian states) | Brisbane support access (D5); abuse monitoring (D4) and model processing (D1) outside NSW not ruled out | counsel: which s 19(2) ground; HPP 14 for health information | D1, D4, D5 |

| Flow (from Data flows) | Outside NSW? | Use or disclosure | s 19(2) or HPP 14 ground proposed | Evidence |
| --- | --- | --- | --- | --- |
| Model request | gap: processing region not read; endpoint in Sydney | assumption: use, contracted service only | counsel: ground, if outside NSW | D1 |
| Logs and transcripts in Firestore and Cloud Logging | no: Sydney | assumption: use, contracted service only | n/a: inside NSW | D2 |
| Abuse monitoring | gap: location not recorded | counsel: use or disclosure | counsel: ground | D4 |
| Support access from Sydney | no | assumption: use, contracted service only | n/a: inside NSW | D5 |
| Support access from Brisbane | yes: Queensland | assumption: use, contracted service only; counsel: confirm | counsel: ground, for example a contract with enforceable IPP-compliant handling, breach notice and flow-down; gap: contract text not in the record | D5 |

## Questions for counsel

- counsel: is a PIA required for this system, and does the PIA need to name the model and abuse-monitoring flows; Australia, NSW; needed by W4.
- counsel: is each flow outside NSW (Brisbane access, abuse monitoring, model processing if outside NSW) a use or a disclosure, and which s 19(2) or HPP 14 ground applies; needed by W3.
- counsel: does the contract meet the IPC reasonable-steps minimum for recipients outside NSW; gap: contract text; needed by W3.
- counsel: is 90 days of full-content transcripts necessary and proportionate, given health and criminal-history disclosures; needed by W4.
- counsel: does s 7B(5) cover Southgate's handling of transcripts, and is Southgate bound by the HRIP Act; needed by W3.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy officer (Sam Taylor) | this document | pending | pending |
