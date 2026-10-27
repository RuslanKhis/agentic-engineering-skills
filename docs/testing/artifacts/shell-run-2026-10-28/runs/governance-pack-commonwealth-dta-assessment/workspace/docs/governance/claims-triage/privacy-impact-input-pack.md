---
document: privacy-impact-input-pack
system: Claims triage assistant (Compensation Claims Office)
version: design accepted 2026-09-19, build v0.6.3
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
owner: Compensation Claims Office (non-corporate Commonwealth entity)
for: CCO Privacy Officer (James Whitlam)
sources: docs/discovery/claims-triage.md, docs/architecture/claims-triage.md, docs/plans/claims-triage.md
---

# Privacy impact input pack: Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Inputs for the CCO's privacy impact assessment under the Australian Privacy Principles and the Agencies Privacy Code (W2). The CCO writes and signs the assessment; this pack supplies the facts the design and plan record and the questions only counsel can answer. Not legal advice.

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| Australia | OAIC threshold assessment: new or changed handling of personal information | yes | New automated handling of claim forms, notes and medical reports, including sensitive information | D1, docs/discovery/claims-triage.md §3 |
| Australia | Agencies Privacy Code: high privacy risk project (significant impact on privacy) | yes (proposed) | Health and mental-health information, family violence disclosures, generative AI | docs/discovery/claims-triage.md §3; counsel: confirm |

Result: counsel: a PIA is proposed as required for the CCO (a Commonwealth agency on a high privacy risk project, checked 2026-10-26); the Privacy Officer decides. It is wait W2.

## Processing description

- **Purpose:** draft a triage recommendation (category, priority, missing evidence) for an officer to accept or change (R1, R4).
- **Nature:** reads claim form, claim notes and medical reports from the case system, sends them to Gemini, shows a draft citing claim passages, records the officer's accept or change with the draft (R2, C2, C3, C4, D1).
- **Scope:** about 1,900 new claims a month across 120 officers; pilot of 20 officers in Canberra for 8 weeks (docs/discovery/claims-triage.md §1, §6). Pilot volume: gap: claims routed to pilot officers not estimated.
- **Context:** claimants are former Commonwealth contractors injured at work, who lodge claims and cannot choose whether the CCO uses tools on them; expectations of AI use are not recorded (docs/discovery/claims-triage.md §1, §3). gap: whether claimants have been told AI is used.

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Officer opens a claim | Claim form, notes, medical reports | Case management system (read only) | Cloud Run service, australia-southeast1 | gap: not recorded whether the service caches the claim | gap: unknown | Team-scoped read (C1), read-only account (C3) | C1, C3, D2 |
| Model request | Claim content in the prompt | Cloud Run service | Gemini `gemini-3.5-flash-001` on Vertex AI, endpoint australia-southeast1 | gap: provider retention and abuse-monitoring storage not read at the source | n/a: not stored by the CCO | gap: no sensitive data screening evidence recorded | D1 |
| Draft returned | Category, priority, missing evidence, cited passages (generated personal information) | Gemini | Officer's screen | Prompts and drafts logged for 30 days | gap: no per-claimant lookup recorded | Output validator withholds uncited drafts (C2) | C2, D3 |
| Officer decision | Accept or change, with the draft | Officer | Decisions table, Cloud SQL, australia-southeast1 | gap: retention period not decided | gap: unknown | n/a: no model | C4, D2 |
| Logs | Prompts and drafts | Cloud Run | Logging in australia-southeast1 | 30 days | gap: unknown | gap: no log scrubbing evidence | D2, D3 |
| Consultancy access | Logs and the evaluation set | CCO environment | Southgate Labs staff, Sydney, Australia | gap: access period and approvals not recorded | n/a: staff access | gap: staff clearances and logging of staff access not recorded | D4 |
| Evaluation set | 900 past claims with officer decisions, names and identifiers removed | Case system export (2023 to 2026) | Evaluation environment; gap: location not recorded | gap: retention not recorded | n/a: de-identified | Names and identifiers removed (D5) | D5, M1, M2 |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| Claimants (Australian residents) | Claim form, claim notes, employment history | Injury and medical details, mental-health history, sometimes family violence disclosures (sensitive information; counsel: confirm) | Case management system, supplied by the claimant | docs/discovery/claims-triage.md §3 |
| Claimants | Attached medical reports | Health information (sensitive) | Case management system | docs/discovery/claims-triage.md §3 |
| Claimants | Draft triage recommendations (inferences) | Possibly inferred health information; generated information is a collection (counsel: confirm) | Generated by the assistant | R1, C2 |
| Third parties named in notes | Family members, others | Possible, gap: not assessed (family violence disclosures) | Claim notes | docs/discovery/claims-triage.md §3 |
| Claims officers | Sign-in identity, accept or change decisions | None recorded | CCO identity provider | docs/architecture/claims-triage.md Scope gate, C4 |

## Automated decisions

- **Facts:** an officer accepts or changes every draft (R4, C4). Officers' training and authority to override: agency: not recorded. Offline agreement with officer decisions on 900 past claims: category 88% (M1), priority 79% (M2). Pilot override rate and review time: gap: not measured; baseline 11% of triage decisions changed at assessment (docs/discovery/claims-triage.md §2).
- **Explanation the design can produce:** each field of the draft cites claim passages (R2, C2); explanation of factors to a claimant: gap: no route recorded.
- counsel: APP 1.7 substantially and directly related decision, from 10 December 2026 (checked 2026-10-26); the OAIC fact sheet says human review does not itself take a use out of scope (checked 2026-10-26); see regulatory-memo.md. Officers may rely on the draft without reading the notes (docs/discovery/claims-triage.md §4).

## Necessity and proportionality

- Claim notes and medical reports are needed because category, priority and missing evidence depend on them (R1); the least intrusive alternative, an officer reading every claim unaided, is the baseline of 6 working days to triage (docs/discovery/claims-triage.md §2). gap: no option for a smaller data set (for example excluding medical reports) was recorded as considered.
- Minimisation: the officer sees only claims in their team's queue (R3, C1); the assistant is read-only (C3); the evaluation set has names and identifiers removed (D5). gap: claim notes themselves are not redacted before the model request.
- Re-used data: 2023 to 2026 officer decisions are re-used as an evaluation set (D5); original purpose was handling the claims. counsel: is evaluation a related secondary purpose within reasonable expectations (APP 6)? Is de-identification adequate given free-text notes?
- Notice and rights: agency: how claimants are told that AI is used, who the recipients are, and how they seek access or correction; gap: no notice text exists (see proposed APP 5 text below).

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| Logs | Prompts and drafts | 30 days | Expiry; gap: path for an access or deletion request not recorded | D3 |
| Decisions table (Cloud SQL) | Draft with officer accept or change | gap: retention not decided; agency: records disposal authority | gap: not recorded | C4, D2 |
| Evaluation set | 900 de-identified claims with decisions | gap: not recorded | gap: not recorded | D5 |
| Model provider | Prompts and outputs | gap: not read at the provider's page | gap: not recorded | D1 |
| Case management system | Claim record (unchanged by the assistant) | agency: CCO records schedule | n/a: assistant writes nothing there | C3 |

## Recipients and regions

| Recipient (processor, service provider, agent or data intermediary, in the regime's own word) | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| Google Cloud (Cloud Run, Cloud SQL, logging, Vertex AI) | Cloud and model provider to the CCO; contracted service provider if the contract carries s 95B terms (counsel: confirm) | australia-southeast1 for hosting, database, logs and the endpoint; gap: model processing region not read | counsel: use or disclosure under APP 8 and s 16C; gap: contract terms and any offshore abuse monitoring unknown | D1, D2 |
| Southgate Labs | Contracted service provider and system developer (counsel: confirm APP entity status) | Sydney, Australia | n/a: access from within Australia, so no overseas disclosure on the record; gap: sub-contractors and remote access from elsewhere not recorded | D4 |
| CCO identity provider | Authenticates officers | agency: not recorded | agency: confirm | docs/architecture/claims-triage.md Scope gate |

## Model provider data use

- Model and endpoint: `gemini-3.5-flash-001` through Vertex AI, endpoint australia-southeast1 (D1). gap: whether prompts and outputs are used to train models, whether abuse monitoring stores flagged prompts, caching and zero data retention were not read at the provider's page or terms (no network); propose as a goal for adk-model-and-output-contracts and a check by the contract owner. Not asserted either way.
- Whether the model was trained on personal data and what the CCO relies on: counsel: question for the CCO; the OAIC guidance on commercially available AI products (21 October 2024, checked 2026-10-26) recommends due diligence and a PIA.

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| A wrong low priority delays payment to an injured person | assumption: likelihood medium (priority agreement 79% offline), severity high (delays payment) | Officer accepts or changes every draft; citations of claim passages | in place, tested locally (C2, C4); pilot override rate gap: not measured | M2, C2, C4 |
| Officers rely on the draft without reading the notes (automation bias) | assumption: likelihood medium, severity high | Cited passages shown to the officer (R2); no measure of review depth | partly in place; gap: no measure of review time or unread drafts | docs/discovery/claims-triage.md §4, R2, C2 |
| Claim data seen by an officer outside their team | assumption: likelihood low, severity high | Tool scoped to the verified officer's team | in place, tested locally | C1, G02/A2 |
| Sensitive information in prompts and logs retained or exposed | assumption: likelihood medium, severity high | Logs kept 30 days in australia-southeast1; no scrubbing recorded | gap: no sensitive data screening evidence (goal for protect-adk-sensitive-data) | D2, D3 |
| Unauthorised change to the case record | assumption: likelihood low, severity high | Read-only service account | in place, tested locally | C3, G02/A3 |
| Offshore processing or provider retention not matching the CCO's expectation | assumption: likelihood unknown | none until the provider's page is read | gap: goal for adk-model-and-output-contracts | D1 |
| Re-identification from the evaluation set or staff access | assumption: likelihood low, severity medium | Names and identifiers removed; Sydney staff only | partly in place; gap: access controls and clearances not recorded | D4, D5 |
| ADK runtime hardening | assumption: low for the pilot | Deferred until production | deferred: production | SB05 |

## Australia: APP compliance check

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection (3.3 consent for sensitive information; generated or inferred information is collected) | Claim notes hold health and mental-health information; drafts are generated | counsel: is generated triage output a collection; does 3.3 or an exception cover it | R1, docs/discovery/claims-triage.md §3 |
| APP 5 notice | gap: no notice text mentions AI or Google as a recipient | counsel: confirm notice content; agency: owner | docs/discovery/claims-triage.md §3 |
| APP 6 use and disclosure (primary purpose; secondary use) | Triage is proposed as the primary purpose; evaluation re-uses past decisions | counsel: related secondary purpose within reasonable expectations | R1, D5 |
| APP 8 and s 16C overseas recipients | Endpoint and hosting in australia-southeast1 | gap: model processing region and support access; counsel: use or disclosure | D1, D2 |
| APP 10 quality; APP 11 security and destruction | Offline agreement 88% category and 79% priority; team scope and read-only access; 30-day logs; IRAP assessment booked 2026-11-16 | gap: no pilot accuracy figure, no destruction path for the decisions table | M1, M2, C1, C3, D3, W1 |
| APP 12 and 13 access and correction (memory, logs, evaluation sets) | Decisions table, logs and evaluation set hold claim-linked data (the evaluation set is de-identified) | gap: no access and correction path recorded; counsel: is a draft held information | C4, D3, D5 |

- **PIA required?** Commonwealth agency on a high privacy risk project: required (Agencies Privacy Code, checked 2026-10-26) (counsel: high privacy risk?). The PIA is W2.

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Claim form and notes, including injury, mental-health and family violence details | Triage drafting for an officer | Claimant, via the case system | Google Cloud as host and model provider; Southgate Labs for support | gap: none recorded; model processing region not read | Logs 30 days; gap: other stores | D1, D2, D3, D4 |
| Medical reports | Triage drafting | Claimant's providers, via the case system | As above | As above | As above | docs/discovery/claims-triage.md §3, D1 |
| Draft recommendations (generated) | Show the officer a proposal | Generated | Officer; Southgate Labs (logs) | As above | Logs 30 days; decisions table gap: retention | C2, C4, D3 |
| Officer decisions on past claims 2023 to 2026, names and identifiers removed | Evaluation | CCO case system export | Southgate Labs | none recorded | gap: not recorded | D5 |

- **Proposed APP 5 notice and privacy-policy additions, including APP 1.8 entries:** "The CCO uses a computer program to draft a recommended category, priority and list of missing evidence for each new claim from the information you give us, including health information. A claims officer reviews every draft and decides. The program is hosted in Australia by Google Cloud; Southgate Labs supports it from Australia." gap: model processing region and provider retention must be confirmed before the sentence about hosting is used (system-card.md; counsel: confirm; agency: the Privacy Officer owns the notice and the privacy policy; W5).

## Questions for counsel

- counsel: is the PIA required under the Agencies Privacy Code, and does the high privacy risk finding follow? Needed by W2.
- counsel: APP 3.3 and APP 5 for health information in notes and for generated drafts. Needed by W2.
- counsel: APP 6 for evaluation use of 2023 to 2026 decisions, and whether the de-identification (D5) is sufficient. Needed by W2.
- counsel: APP 8 use or disclosure for the Gemini endpoint, abuse monitoring and Google support access, once read at the source. Needed by W2.
- counsel: s 95B terms and flow-down to Southgate Labs; who notifies an eligible data breach. Needed by W2.
- counsel: APP 1.7 scope and the privacy policy wording before 10 December 2026. Needed by W5.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO Privacy Officer (James Whitlam) | this document | pending | pending |
