---
document: impact-assessment
system: Public enquiries assistant
version: design accepted 2026-09-15, build v0.7.0
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Accountable Official for AI (Ruth Abbott), as risk owner
trigger: pilot decision on 2026-12-10 (docs/discovery/enquiries.md §6)
sources: docs/discovery/enquiries.md, docs/architecture/enquiries.md, docs/plans/enquiries.md, docs/contract/order-form-summary.md, regulatory-memo.md
---

# AI system impact assessment: Public enquiries assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 and mapped to NIST AI RMF 1.0 and NIST AI 600-1. Draft for the Office's risk owner; scores are provisional until they set them. Not legal advice.

## Scope and intended use

- **System and functions:** answers licensing questions from published guidance and reports application status after number and date of birth match; hands over to the contact centre (R1, R2, R3).
- **Intended use:** public web chat on the "Apply for a licence" pages for a six-week pilot (docs/discovery/enquiries.md §6); **foreseeable misuse:** guessing application numbers and dates of birth to see others' status, limited by a three-failure block (C3); typing health or criminal-history details, with no control recorded (gap); asking for licensing advice beyond the guidance, limited by the citation rule (C1).
- **Organisation's role:** the Office is the public sector agency and deployer; Southgate Labs is the developer and contracted service provider (regulatory-memo.md Roles; counsel: confirm).
- **Lifecycle stage and trigger:** pilot, before the executive board decision on 2026-12-10 (G05, docs/discovery/enquiries.md §6).

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| Members of the public asking about licences | direct users | assumption: some may be anxious about a livelihood; gap: accessibility and language needs not recorded | docs/discovery/enquiries.md §1 |
| Applicants whose status is looked up | their personal information is shown to a caller | assumption: no recorded vulnerable group; criminal-history or health documents may be in the missing-documents list | R2, docs/discovery/enquiries.md §3 |
| Contact-centre staff in Parramatta | receive handovers and fewer status calls | no | C4, docs/discovery/enquiries.md §1 |
| Southgate staff | read transcripts and logs | no | D5 |

## System information

- **Data:** published guidance pages (no personal data), application status read from the licensing system, and chat transcripts that may hold names, addresses, health and criminal-history disclosures (docs/discovery/enquiries.md §3).
- **Model and logic:** `gemini-3.5-flash-001` pinned on Vertex AI, retirement 2027-02-26 (D1, model page read 2026-10-20, not re-read); the output validator and the lookup tool are deterministic (C1, C2, C3).
- **Deployment environment:** Cloud Run, Firestore and Cloud Logging in australia-southeast1, operated by Southgate for the Office (D2, D5).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | Applicants | harm | a status lookup for the wrong application discloses another person's information | assumption: low after C2, C3 and 0 of 250 scripted mismatches returned | assumption: high, personal information of a third party | docs/discovery/enquiries.md §4, M2 |
| H2 | Members of the public | harm | wrong guidance about what a licence allows leads to unlicensed work | assumption: moderate; 94% of 400 historical enquiries got a correct cited page, so about 6% did not (offline only) | assumption: moderate to high | docs/discovery/enquiries.md §4, M1 |
| H3 | Callers | harm | health or criminal-history details typed in chat are kept in transcripts and logs and seen outside NSW | assumption: moderate | assumption: high | docs/discovery/enquiries.md §3, D3, D5 |
| H4 | The Office | harm | the pinned model retires on 2027-02-26, inside the six-month notice window in the contract, forcing an unplanned model change in the pilot or production | assumption: high on the dates | assumption: moderate; an untested model could change answer quality | D1, `docs/contract/order-form-summary.md` |
| B1 | The Office and callers | benefit | fewer calls about application status from a baseline of 17,500 a month | hypothesis: not yet measured in the pilot | n/a: benefit | docs/discovery/enquiries.md §2 |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1 | number and date-of-birth match; three failed lookups block further lookups | in place, tested locally | C2, C3, M2 |
| H2 | every answer cites a guidance page; handover when it cannot | in place, tested locally; offline only | C1, C4, M1 |
| H2 | counter-metric: complaints about wrong or misleading information, baseline 14 a month | in place as a measure to watch; not yet measured in the pilot | docs/discovery/enquiries.md §2 |
| H3 | screening or redaction of free text; retention limit of 90 days | gap: no screening; retention planned only as a 90-day deletion | D3 |
| H4 | model-change plan and notice agreement | gap for adk-model-and-output-contracts and adk-release-engineering; counsel: notice period | D1, W7 |

## Residual risk and decision

- H1 residual is low to moderate until live; H2 residual is moderate, since 6% of the offline sample did not cite a correct page (M1); H3 residual is high until screening exists or the notice tells callers not to type such details; H4 residual is high on the dates alone (H1, H2, H3, H4 above).
- **Accepted by:** gap: acceptance by the Accountable Official; the sponsor and the Accountable Official are the same person (docs/discovery/enquiries.md §5); agency: confirm that is intended.
- **Conditions that end acceptance:** a mismatched status returned live (C2); the complaints counter-metric rising above its baseline of 14 a month (docs/discovery/enquiries.md §2); a model change (D1); a new use beyond guidance and status.

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | Accountable Official, privacy officer, CISO and records manager are named; no AI training goal recorded (gap) | docs/discovery/enquiries.md §5 |
| Map | scope, parties and the NSW regime screen | regulatory-memo.md, R1, R2 |
| Measure | M1 (94%, 400 historical enquiries) and M2 (0 of 250); unmeasured: live accuracy, bias and accessibility, handover time, transcript screening coverage | M1, M2 |
| Manage | C1 to C4, SB01, SB03 and SB05; no incident record exists | C1, C2, C3, C4, SB01, SB03, SB05 |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| CBRN information | n/a: answers are limited to licensing guidance | citation rule | C1 |
| Confabulation | yes | citation validator; offline accuracy 94%; no suggested-action IDs recorded: gap | C1, M1 |
| Dangerous, violent or hateful content | yes, low | gap: no safety evaluation recorded for abusive callers | R3 |
| Data privacy | yes | match and lookup limit; screening of free text is a gap | C2, C3, D3 |
| Environmental | n/a: not assessed for a pilot of this size | assumption: negligible | D1 |
| Harmful bias or homogenisation | yes | gap: no bias or language-group evaluation | M1 |
| Human-AI configuration | yes | handover on request or when it cannot answer; gap: AI disclosure and measured handover time | C4, R3 |
| Information integrity | yes | answers cite the Office's own pages | C1 |
| Information security | yes | credential and runtime baseline rules; gap: no red-team or prompt-injection results recorded | SB01, SB03, SB05 |
| Intellectual property | n/a: answers draw on the Office's own published guidance | assumption: no third-party content | R1 |
| Obscene, degrading or abusive content | yes, low | gap: no evaluation recorded | R3 |
| Value chain and component integration | yes | Google is a subcontractor; model retirement 2027-02-26; abuse monitoring location unknown | D1, D4 |

## Monitoring and review

- Watch the complaints counter-metric (baseline 14 a month) and the status-call outcome measure (baseline 17,500 a month); owner Ruth Abbott as decider (docs/discovery/enquiries.md §2); gap: thresholds and a live monitoring goal.
- **Review triggers:** model change, new user group or data, incident, change in law or regulator guidance; the first is dated 2027-02-26 (D1).

## Australia: Guidance for AI Adoption mapping

| Practice | Content in this assessment | Evidence |
| --- | --- | --- |
| 1 Decide who is accountable | Accountable Official; Southgate as developer; Google as model and cloud provider | docs/discovery/enquiries.md §5, D6 |
| 2 Understand impacts and plan accordingly | H1 to H4; contest route is handover to the contact centre | C4 |
| 3 Measure and manage risks | measures above; M1 and M2 | M1, M2 |

## Australia: NSW AIAF inputs (NSW agency clients)

- **Registration and assessment:** answers are in `government-form-answers-nsw-aiaf-registration.md` and `government-form-answers-nsw-aiaf-assessment.md`; agency: the Accountable Owner completes them and says which AIAF version applies (W5).
- **Proposed band:** medium, intrinsic under the Operational Policy: a public-facing agent that handles applicants' personal information but decides nothing and cannot change applications (docs/architecture/enquiries.md Scope gate, C2); assumption: the harm in H1 is noticeable but limited; agency: sets the band; counsel: a high band follows if the agency treats H1 or H3 as significant.
- **Review committee:** referral within 5 business days of completing the AIAF if the band is high or critical (checked 2026-10-26, source: adk-governance-pack reference australia.md, read 2026-10-26); wait W6, conditional; counsel: referral needed.
- **Contract and records:** ICTA clause 6.11 six-month model-change notice against retirement on 2027-02-26 (D1; `docs/contract/order-form-summary.md`); gap: Order Form AI list of model IDs not in the summary; gap: no export of outputs and metadata to the agency's recordkeeping system as State records (D3).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Accountable Official for AI (Ruth Abbott) | this document | pending | pending |
| Privacy officer (Sam Taylor) | privacy impacts H1 and H3 | pending | pending |
| CISO (Nikhil Rao) | security rows and information security | pending | pending |
