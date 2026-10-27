---
document: privacy-impact-input-pack
system: Shortlisting assistant (Kestrel Logistics)
version: design accepted 2026-09-04; build v0.6.0
status: draft
jurisdictions: [au, eu]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
owner: Kestrel Logistics B.V. (Rotterdam) and Kestrel Logistik GmbH (Duisburg); counsel: single, joint or separate controllers
for: Matthias Brandt, DPO, Kestrel Logistics
sources: docs/discovery/shortlisting.md, docs/architecture/shortlisting.md, docs/plans/shortlisting.md
---

# Privacy impact input pack: Shortlisting assistant (Kestrel Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Inputs for Kestrel's data protection impact assessment under GDPR Article 35
(the DPIA signed under W2), and, for Southgate Labs' own handling, the
Australian privacy impact assessment. Kestrel writes and signs the DPIA; this
pack supplies the facts the design and plan record and the questions only
counsel can answer. The GDPR Digital Omnibus amendments were not law on 2026-10-26
and Articles 4(1), 9, 12, 13, 22, 33, 35 are treated as unamended (source:
adk-governance-pack reference privacy-and-records.md, read 2026-10-26; not re-read at the source). Not legal advice.

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| EU | WP248 rev.01 criterion 1, evaluation or scoring | yes | The assistant ranks applicants | R1, C5 |
| EU | WP248 criterion 2, automated decision with legal or similarly significant effect | counsel: ranking drives who is read, a recruiter decides | See Automated decisions | D1, D7 |
| EU | WP248 criterion 4, special-category or highly personal data | counsel: CVs are free text that may reveal age, nationality, health and family status | Photos, dates of birth, nationality and marital status are removed before the model; health and family status are not in C4's list | docs/discovery/shortlisting.md §4, C4 |
| EU | WP248 criterion 5, large scale | counsel: about 2,600 applications a month company-wide, pilot share not recorded | gap: pilot volume | docs/discovery/shortlisting.md §1 |
| EU | WP248 criterion 7, vulnerable data subjects or power imbalance | yes | Applicants seeking jobs | docs/discovery/shortlisting.md §4 |
| EU | WP248 criterion 8, innovative technology | yes | A generative model ranks CVs | D2 |
| Australia | OAIC threshold assessment: new or changed handling of personal information | yes | Southgate staff in Sydney get read access to logs and the evaluation set | D5, D6 |

Result: counsel: a DPIA is required for the EU processing (at least three WP248 criteria met); the DPO decides. Australia: a PIA for Southgate Labs' own handling is recommended, not required (source: adk-governance-pack reference australia.md, checked 2026-10-26; counsel: confirm).

## Processing description

- **Purpose:** rank applicants against a vacancy's must-have requirements and give a cited rationale, so a recruiter can shortlist faster; outcome measure is median working days to shortlist, baseline 4.5 (R1, R2, docs/discovery/shortlisting.md §3).
- **Nature:** reads CVs uploaded to the ATS, redacts dates of birth, photos, nationality and marital status, sends the redacted text to Gemini, returns a ranking and rationales; stores prompts and responses in logs for 14 days (C4, C5, D2, D4).
- **Scope:** pilot of three recruiters on warehouse and driver vacancies for eight weeks (docs/architecture/shortlisting.md, Scope gate); the company receives about 2,600 applications a month across nine recruiters (docs/discovery/shortlisting.md §1). gap: number of applicants in the pilot and per vacancy.
- **Context:** applicants in the Netherlands, Germany, Poland and Romania apply for vacancies and expect human reading of their CVs (docs/discovery/shortlisting.md §1, §4). gap: no record of what applicants are told about AI use.

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CV upload | Name, contact details, work history, education, photo and date of birth on some CVs, free text | Recruiter, ATS | Cloud Run, europe-west4 | gap: whether CVs are stored beyond the ATS | gap: unknown | Redaction of dates of birth, photos, nationality, marital status (C4); CV skipped and flagged on failure | C4, D3, docs/architecture/shortlisting.md Scope gate |
| Model request | Redacted CV text and vacancy requirements | Cloud Run | Gemini 3.5 Flash, endpoint europe-west4 | Provider retention: gap: not read from the provider's page | n/a: not stored by the client | C4 only; no detector coverage figure recorded (gap: protect-adk-sensitive-data coverage) | D2 |
| Ranking and rationale | Ranking, rationale quoting CV passages | Model | Recruiter view | gap: where rankings and rationales are stored and for how long | gap: unknown | Citation validator (C2); requirement table (C5) | C2, C5 |
| ATS read | Applicant records of owned vacancies | ATS | Cloud Run | n/a: read-only | n/a | Per-recruiter ownership check (C1); read-only credential (C3) | C1, C3 |
| Prompt and response logs | CV text and rationales | Cloud Run | gap: log sink and region | 14 days | gap: unknown | None recorded for CV text; traces keep no CV text | D4 |
| Evaluation set | 1,400 past applications with recruiter decisions, names and contact details removed | ATS export | gap: where stored | gap: retention | gap: unknown | Pseudonymisation by removing names and contact details (D6) | D6, docs/discovery/shortlisting.md §4 |
| Consultancy access | Logs and the evaluation set | Kestrel project `kestrel-talent-pilot` | Southgate Labs engineers, Sydney, Australia | Pilot and six-week support period | n/a: read access, no copy recorded; gap: whether copies are made | gap: access controls and logging of staff access | D3, D5 |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| Applicants for warehouse, driver and transport-planner vacancies | Name, contact details, work history, education, photos and dates of birth on some CVs | counsel: free text may reveal age, nationality, health and family status; C4 removes dates of birth, photos, nationality and marital status but not health or family status | The applicant, by ATS upload by the recruiter | docs/discovery/shortlisting.md §4 |
| Applicants in the evaluation set | The above plus recruiter decisions 2024 to 2026 | counsel: as above; age band and gender were measured in M3, source gap | ATS export | D6, M3 |
| Recruiters | Account identity, vacancies owned, actions | none recorded | Sign-in | C1 |

## Automated decisions

- **Facts:** the recruiter decides who is shortlisted; the assistant ranks and gives rationales, and changes nothing in the ATS (D1, R4, C3). Recruiters see rank and rationale and can open every CV (D7). The bottom half of the ranking stays visible with rationale, planned under G04 (C6). gap: share of ranked applicants a recruiter opens, time per vacancy and override rate; M1 shows agreement with past recruiter decisions of 81%, which is not an override rate (M1).
- **Explanation the design can produce:** each applicant gets the vacancy's requirements met or missed and a rationale citing the applicant's own CV passages (C2, C5). gap: who produces the explanation to an applicant on request (Article 15(1)(h), *Dun & Bradstreet Austria*) and what the recruiter may copy into a message; harms record that a wrong rationale may be copied into a rejection message (docs/discovery/shortlisting.md §5).
- counsel: GDPR Article 22: the Court of Justice in *SCHUFA* (C-634/21) treated a score on which the human "draws strongly" as the decision; the recruiter-review facts above are the evidence. counsel: Article 22(3) human intervention route and Article 13(2)(f) and 14(2)(g) meaningful information. Australia: n/a: no decision about a person by Southgate Labs (D1).

## Necessity and proportionality

- Dates of birth, photos, nationality and marital status are removed before the model sees a CV (C4, R5). Incident I1 showed that PDF uploads skipped this step for six CVs on 2026-10-06; the fix covers all upload types and the C4 test was extended (I1, closed 2026-10-07).
- The accepted risk remains: graduation years and career length can still signal age, because C4 removes explicit dates of birth only (docs/architecture/shortlisting.md, Accepted risks). M3 shows a ratio of 0.71 for applicants aged 50 and over (M3). gap: R5 also bars gender, health and family status, but C4's list does not include them and M3 measures only age band and gender (R5, C4, C7).
- Less intrusive alternative: a recruiter reading every CV, the current process at 4.5 working days (docs/discovery/shortlisting.md §2). gap: no design record of rule-based extraction of the must-have requirements (licence class, shift availability, language, years) as an alternative that avoids ranking free text.
- Re-used dataset: 1,400 past applications from 2024 to 2026 reused to build the evaluation set (D6); counsel: original purpose, retention basis and compatibility of reuse (GDPR Article 6(4)).
- Informing applicants and rights: gap: no applicant notice, no access, rectification, erasure or objection route recorded for logs, rankings or the evaluation set.

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| Cloud SQL, europe-west4 | gap: what it stores about applicants | gap: no retention decision | gap | docs/architecture/shortlisting.md Scope gate |
| Prompt and response logs | CV text, rationales | 14 days | gap: not recorded | D4 |
| Evaluation set | 1,400 pseudonymised past applications | gap: no retention decision | gap | D6 |
| Southgate access copies | gap: none recorded | gap | gap | D5 |

## Recipients and regions

| Recipient (processor, service provider, agent or data intermediary, in the regime's own word) | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| Google Cloud (Vertex AI, Cloud Run, Cloud SQL) | Processor under the client's agreement (counsel: confirm) | europe-west4, Netherlands; model processing region gap | gap: not read from the provider's page; no transfer expected on the recorded endpoint | D2, D3 |
| Southgate Labs | Processor during build, evaluation and support (counsel: confirm); APP entity in its own right in Australia (counsel: s 6D) | Sydney, Australia | Restricted transfer under GDPR Chapter V: no adequacy decision for Australia (source: adk-governance-pack reference privacy-and-records.md, read 2026-10-26); SCC Module 2 and a transfer impact assessment, gap: none recorded (W4); see transfer-assessment.md | D5 |

## Model provider data use

- Gemini 3.5 Flash through Vertex AI, endpoint in europe-west4 (D2). gap: processing region, retention, training use, abuse-monitoring logging and caching settings for the pinned model were not read from the provider pages (no network access in this run; source: adk-governance-pack reference privacy-and-records.md, read 2026-10-25, last updated 22 October 2026 on the provider's page, not re-read). The reference records that Google does not train on customer data without instruction, that implicit caching is on by default unless disabled per project, and that classifier-flagged prompts can be stored up to 90 days and reviewed by people; whether Kestrel's agreement exempts it is counsel or account-team.
- Reliance on the provider's statement that the model was not developed unlawfully (EDPB Opinion 28/2024): counsel.

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| Suitable applicant ranked low and never read | assumption: likelihood medium, severity high; job opportunity lost | Full list visible with rationale | planned: G04, in progress; C6 | C6, docs/discovery/shortlisting.md §5 |
| Ranking reproduces age patterns in past decisions | assumption: likelihood high, severity high; measured 0.71 | C4 removes dates of birth; adverse impact measured | in place, tested offline; disparity unresolved; gap: no mitigation goal | C4, C7, M3 |
| Ranking reproduces nationality, health or family patterns | assumption: likelihood unknown | C4 removes nationality and marital status | gap: not measured, C7 covers age band and gender only | C4, C7 |
| Wrong rationale copied into a rejection message | assumption: likelihood low, severity medium | Rationales must cite the applicant's own CV; no message sending in scope | in place, tested locally; M2 98.6%; accuracy of the claim itself not measured | C2, M2 |
| Unredacted personal data reaches the model | assumption: likelihood low after fix, severity high | Redaction on all upload types; CV skipped and flagged on failure | in place, tested locally after incident I1 | C4, I1 |
| Personal data in logs seen from Sydney | assumption: likelihood medium, severity medium | 14-day log retention | in place as a retention period; gap: access controls and transfer mechanism (W4) | D4, D5 |
| Recruiters defer to the ranking (automation bias) | assumption: likelihood medium | Recruiter decides; full list planned | gap: no review or override measure | R4, D7, C6 |

## Australia: APP compliance check

Scope: Southgate Labs' own handling only (D5, D6). The client's own APP duties are n/a: Kestrel is not an Australian entity.

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection | Southgate engineers read CVs in logs and the evaluation set (D5) | counsel: is reading EU applicants' data in Kestrel's project a collection by Southgate | D5 |
| APP 5 notice | No notice in the record | gap: nothing tells applicants Southgate staff may read their CVs | D5 |
| APP 6 use and disclosure | Access is for debugging and evaluation during the pilot and six weeks of support | counsel: confirm use limited to those purposes | D4, D5 |
| APP 8 and s 16C overseas recipients | Data is held in europe-west4 and read from Australia | counsel: not an overseas disclosure by Southgate on these facts | D3, D5 |
| APP 10 quality; APP 11 security and destruction | gap: no SB row covers Southgate staff access or destruction of any copies | gap: access control, logging and destruction | docs/architecture/shortlisting.md Security baseline |
| APP 12 and 13 access and correction | gap: no route for logs and the evaluation set | gap | D4, D6 |

- **PIA required?** counsel: recommended, not required, for a private organisation (source: adk-governance-pack reference australia.md, checked 2026-10-26).

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| EU applicants' CV content, in logs and the evaluation set | Debugging and evaluation of the shortlisting assistant | Kestrel's ATS, through the client's project | Southgate Labs staff | Data is held in the Netherlands and read from Australia; model processing region gap | 14 days for logs (D4); evaluation set gap | D4, D5, D6 |

- **Proposed APP 5 notice and privacy-policy additions:** counsel: whether Southgate's own privacy policy needs an entry for support access to client-held applicant data; draft wording is held until counsel confirms the Privacy Act reaches it (D5). APP 1.8 entries: n/a: not Southgate's decision.

## EU: Legal basis

- counsel: purpose, ranking applicants for recruitment; candidate basis Article 6(1)(f) legitimate interests, or (b) steps at the applicant's request before a contract; facts: the applicant sent the CV for the vacancy, the tool is faster, human decision remains (R4, docs/discovery/shortlisting.md §3). Consent is rarely freely given where there is an imbalance (WP248 criterion 7).
- counsel: Article 9 condition for any special category in free text (health, and inferred age, which is not special category); AI Act Article 4a conditions if special categories are used for bias detection (M3, C7).
- counsel: lawful basis and compatibility for the evaluation set built from 2024 to 2026 decisions (D6) and for Southgate's support access (D5).
- counsel: each Dutch, German, Polish and Romanian employment-law rule on automated recruitment tools; not covered by this pack's references (W1).

## Questions for counsel

- counsel: is a DPIA required and is residual risk high enough for Article 36 prior consultation (W5); regime EU; needed by W2.
- counsel: controller roles of the two Kestrel entities and the processor agreements with Southgate Labs and Google; regime EU; needed by W4.
- counsel: lawful basis, Article 9 condition and Article 6(4) compatibility for the evaluation set and the live ranking; regime EU; needed by W2.
- counsel: Article 22 and the explanation owed to an applicant who asks; regime EU; needed by W2.
- counsel: whether I1 required assessment or notification; regime EU; needed by W2.
- counsel: whether the Privacy Act reaches Southgate's handling and whether a notice or PIA is needed; regime Australia; needed by W3.
- counsel: the supervisory authority's national DPIA list and which authority leads; regime EU; needed by W2.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Matthias Brandt, DPO | This document | pending | pending |
| Anouk de Vries, counsel | Every counsel: item | pending | pending |
