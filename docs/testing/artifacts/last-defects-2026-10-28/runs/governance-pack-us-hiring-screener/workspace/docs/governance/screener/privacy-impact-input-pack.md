---
document: privacy-impact-input-pack
system: applicant screener (build v0.5.2)
version: design accepted 2026-09-02; build v0.5.2
status: draft
jurisdictions: [au, us]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
owner: Redwood Freight Inc. (CCPA business, employer); Southgate Labs Pty (service provider and APP entity in its own right, counsel: confirm entity name and status)
for: Monica Alvarez, General Counsel, Redwood Freight Inc.
sources: docs/discovery/screener.md, docs/architecture/screener.md, docs/plans/screener.md
---

# Privacy impact input pack: applicant screener

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Inputs for Redwood's privacy assessments of this system: the California CPPA risk assessment (§7150 and §7152) and any other US state assessment, and, for Southgate Labs' own Sydney handling, the Australian privacy impact assessment. Redwood writes and signs each assessment; this pack supplies the facts the design and plan record and the questions only counsel can answer. Not legal advice.

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| Australia | OAIC threshold assessment: new or changed handling of personal information | yes | Southgate engineers in Sydney read real past applications and logs (counsel: whether the Act applies) | D4, D5 |
| United States | CPPA §7150(b): using ADMT for a significant decision | yes (counsel:) | Scores and ranks applicants for hiring (employment is a significant decision) | R1, R2, C3 |
| United States | CPPA §7150(b): processing sensitive personal information | yes (counsel:) | Free text may reveal age, disability, national origin | docs/discovery/screener.md §3 |
| United States | CPPA §7150(b): inference of aptitude or performance from systematic observation of applicants | yes (counsel:) | Score inferred from application content | R1, C1 |
| United States | CPPA §7150(b): training ADMT for significant decisions | no (counsel: confirm) | No training recorded; the model is Gemini used as is; evaluation set is for backtest | D1, D5 |

Result: counsel: a US risk assessment is required before the pilot on these facts, subject to the CCPA business test (gap: revenue and consumer counts); an Australian PIA is recommended for Southgate's own handling; Redwood's privacy officer decides (not named in the record, gap).

## Processing description

- **Purpose:** first screen of applications for warehouse associate and forklift operator roles at the California warehouses, to cut median days from application to first recruiter contact from 9 days, with 90-day retention (71%) as the counter-metric (docs/discovery/screener.md §2; R1, R2).
- **Nature:** reads applications from Greenhouse, removes age, date of birth, graduation years and photos, scores 0-100 with requirements evidence, ranks, labels scores under 40 "not recommended", writes results back (C1, C3, C4, D2).
- **Scope:** about 9,000 applications a month across Redwood (docs/discovery/screener.md §1); pilot is California warehouses for 8 weeks (docs/architecture/screener.md Scope gate); gap: the pilot's expected application volume and start date.
- **Context:** applicants expect a recruiter to read their application; those labelled "not recommended" may never be read by a person (docs/discovery/screener.md §4). gap: the applicant notice they saw is not in the record.

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Application intake | name, contact, address, work history, availability, certifications, screening answers | Greenhouse ATS | screener on Cloud Run, us-west1 | gap: retention not recorded | gap: not recorded | redaction of age, date of birth, graduation years, photos; flagged if it fails; free text not otherwise screened (gap) | C4, G01/A2, docs/architecture/screener.md Scope gate |
| Model request | redacted application text | Cloud Run | Gemini `gemini-3.5-flash-001` on Vertex AI, us-west1; processing region gap | gap: provider retention not read | n/a: not stored by the client on the record | C4 redaction | D1 |
| Result write-back | score, rank, label, requirements evidence | screener | Greenhouse custom field and BigQuery (region gap) | gap: retention not recorded | yes in Greenhouse (per applicant) | n/a: derived output | D2, C1, C2 |
| Recruiter view | ranked list, collapsed "not recommended" group | Greenhouse | 11 Oakland recruiters, 3 New York recruiters (New York use not decided) | per Greenhouse | yes | n/a | D3, docs/discovery/screener.md §5, §6 |
| Evaluation set | 6,000 past applications 2023-2026 with hiring outcomes, names and contact details removed | Greenhouse export | evaluation store; location gap | gap: retention not recorded | gap | removal of names and contact details only; free text and address not stated as removed (gap) | D5, docs/discovery/screener.md §3 |
| Logs | gap: contents not recorded | screener | gap: sink and region not recorded | gap | gap | gap | D4 |
| Recruiter audit log | recruiter actions in Greenhouse (used for M4) | Greenhouse | Redwood talent operations | per Greenhouse | gap | n/a | M4 |
| Consultancy access | evaluation set and logs | Redwood environment | two Southgate engineers, Sydney, Australia, during the build and a three-month support period | until the end of the support period; destruction gap | n/a: staff access | gap: access controls not recorded | D4 |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| Current applicants in California (pilot), and in New York if used | contact, address, work history, availability, certifications, screening answers; generated score, rank and label | free text may reveal age, disability, national origin; counsel: sensitive personal information; work-history length can proxy age (M2 method) | the applicant; generated by the screener | docs/discovery/screener.md §3, D2, M2 |
| Past applicants 2023-2026 (6,000 in the evaluation set) | as above with hiring outcomes; names and contact details removed | as above | Greenhouse export | D5 |
| Recruiters (11 Oakland, 3 New York) | actions in the Greenhouse audit log | none recorded | Greenhouse audit log | docs/discovery/screener.md §5, M4 |

## Automated decisions

- **Facts:** the screener scores, ranks and labels; the recruiter decides and the screener cannot change an application's stage (R2, R4, C2). Recruiters are Redwood employees (11 Oakland, 3 New York); their training and authority to change outcomes are gap: not recorded. Recruiters usually reject "not recommended" applicants in bulk (source: requester (Southgate Labs), 2026-10-28); M4: 6% opened before rejecting (410 applications, shadow trial 2026-10-06 to 2026-10-17, build v0.5.2; denominator gap:). Override rate: gap: not measured.
- **Explanation the design can produce:** each score lists the requirements met and missed with the application text behind each (C1); a counterfactual or adverse-outcome reason in applicant-facing form is gap: none designed.
- counsel: APP 1.7 is n/a: client is outside the Privacy Act on the record; CPPA ADMT: does the output replace or substantially replace a human decision, given the three-part review facts (interpret C1, review with other information, authority R4) and M4; state profiling opt-out laws: gap: applicants' states unknown beyond California and New York.

## Necessity and proportionality

- Age, date of birth, graduation years and photos are removed before scoring (C4, evidenced local, G01/A2); work-history length remains available and is used in M2 as the age proxy (M2); gap: whether it is a scoring input.
- Less intrusive alternatives (unranked list, rules-only requirements check, no "not recommended" label) are gap: not recorded in docs/architecture/screener.md; proposed question to the design owner.
- Re-used data: 6,000 past applications for the backtest (D5); original purpose was applying for a job; counsel: compatible with the applicants' notices, and whether removal of names and contact details is enough given free text (gap: whether addresses were removed).
- People are informed by Redwood's applicant notice and exercise rights by Redwood's channels; gap: neither the notice nor the access, correction, deletion and appeal routes are in the record (docs/discovery/screener.md §3).

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| Greenhouse custom field | score, rank, label | gap: not recorded | gap | D2 |
| BigQuery | scores, ranks, labels | gap: not recorded; counsel: FEHA four-year record rule for selection criteria and ADS data (§11013(c), checked 2026-10-26) | gap | D2 |
| Evaluation set | 6,000 past applications | gap: until when; at least the end of the three-month support period | gap | D4, D5 |
| Logs | gap | gap | gap | D4 |
| CPPA risk assessment | the assessment itself | keep five years, review every three years, update within 45 days of a material change (CPPA §7152, checked 2026-10-26) | n/a: Redwood's record | W3 |

## Recipients and regions

| Recipient (service provider or contractor in CCPA terms; APP entity in Australian terms) | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| Google Cloud (Vertex AI, Cloud Run, BigQuery) | service provider or contractor, counsel: confirm | us-west1 Oregon; model processing region and BigQuery region gap | US: no US transfer rule on the record; Australia: counsel: APP 8 use or disclosure (Southgate's side) | D1, D2, docs/architecture/screener.md Scope gate; gap: contract |
| Southgate Labs | service provider or contractor for Redwood; APP entity in its own right, counsel: confirm | Australia (Sydney) | APP 8 and s 16C facts: staff access to data held in the US; counsel: use or disclosure | D4; gap: contract |
| Greenhouse | the client's existing ATS and system of record | gap: region not recorded | n/a: existing Redwood system | docs/discovery/screener.md §3 |

## Model provider data use

- Model `gemini-3.5-flash-001` on Vertex AI in us-west1 (D1). Whether prompts and outputs are used for training, abuse-monitoring logging, caching, zero data retention status, the processing region and the retirement date: gap: not read from the provider page (no network access in this session); proposed goal for adk-model-and-output-contracts to read and record them with the read date.
- Whether the model was trained on personal data and what Redwood relies on: counsel: question to put to Google's terms; no statement is in the record.

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| Applicant labelled "not recommended" is never read by a person | assumption: likely given bulk rejection, severe for the applicant | recruiter makes every rejection; collapsed group can be opened | in place, tested locally (C2); the review itself not enforced: gap | R4, C2, D3, M4 |
| Scores reproduce age patterns in past hiring | assumption: likely, ratio 0.74 | age removal | in place, tested locally (C4); ratio still 0.74: gap: remediation | C4, M2 |
| Disability or national origin signals in free text affect scores | assumption: possible, severe | none recorded | gap: no measurement and no accommodation route | docs/discovery/screener.md §3 |
| Real applications exposed through Sydney access or logs | assumption: possible, moderate | removal of names and contact details from the evaluation set | gap: access controls, log contents, retention | D4, D5 |
| Applicant text manipulates the score (prompt injection) | assumption: possible | none recorded; SB05 ADK runtime hardening deferred | deferred: production (SB05); gap for the pilot | SB05 |

## Australia: APP compliance check

Scope: Southgate Labs' own handling in Sydney only (D4, D5).

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection (3.3 consent for sensitive information; generated or inferred information is collected) | Southgate receives real applications, which may contain sensitive information in free text | counsel: is access from Sydney a collection by Southgate; gap: sensitive data in free text | D4, docs/discovery/screener.md §3 |
| APP 5 notice | applicants are told nothing by Southgate; Redwood's notice not in the record | gap: whether notice names Australian access | D4 |
| APP 6 use and disclosure | access for build, evaluation and support | counsel: primary purpose of building and supporting the system | D4 |
| APP 8 and s 16C overseas recipients | the stack runs in us-west1; Sydney staff read it | counsel: use or disclosure; gap: contract with Google and Redwood | D1, D4 |
| APP 10 quality; APP 11 security and destruction | M1 78% agreement, M2 and M3 ratios; access controls and destruction not recorded | gap: destruction at end of support period | M1, M2, M3, D4 |
| APP 12 and 13 access and correction (evaluation sets, logs) | evaluation set holds applicants' data without names | counsel: held information; gap: request route | D5 |

- **PIA required?** recommended, not required for a private organisation (australia reference, checked 2026-10-26); counsel: whether the Privacy Act applies at all.

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Applications and hiring outcomes (past), including free-text that may be sensitive | build, backtest and support of the screener | Redwood's Greenhouse export | Southgate engineers; Google | United States (hosting); Australia (staff) | gap | D4, D5 |

- **Proposed APP 5 notice and privacy-policy additions, including APP 1.8 entries:** Southgate Labs' own privacy policy should name the Redwood engagement, the kinds of information it reads, that it is held in the United States and read from Sydney (counsel: confirm); APP 1.8 entries n/a: Southgate makes no decision about a person (system-card.md; C3).

## United States: Notice, consent and opt-out

- **States and thresholds:** California applicants for the pilot and New York applicants in the data register (docs/discovery/screener.md §3); CCPA business test gap: revenue and consumer counts; other states gap: residence data (counsel: confirm).
- **Notice and opt-outs:** CPPA pre-use ADMT notice elements (§7220): purpose, opt-out or exception, access right, plain-language logic, alternative process; opt-out with two methods in 15 business days (§7221) or a human-appeal exception; access responses (§7222) (all checked 2026-10-26). gap: none designed; facts for the notice are in system-card.md (C1, C3); Redwood writes it, W5.
- **Sensitive data:** free text may reveal age, disability, national origin (docs/discovery/screener.md §3); counsel: whether inferences or incidental disclosures need opt-in consent or a right to limit.
- **Level of human involvement:** human reviewed in form (R4, C2); in practice bulk-rejected (M4 6% opened; source: requester (Southgate Labs), 2026-10-28).

## United States: Assessment approval

- **Whether the business will proceed:** counsel: not proposed as a go until the gating questions 1 to 6 in the regulatory memo close; the decision is Redwood's (docs/discovery/screener.md §2, §6).
- **Approver:** gap: approver not named; Kevin Ortiz is the pilot decider (docs/discovery/screener.md §2) but his role as CPPA approver is not recorded.
- **Contributors:** Kevin Ortiz, Monica Alvarez, Priya Raman, recruiters (docs/discovery/screener.md §5); source: docs/discovery/screener.md §5.
- **Review cycle and retention:** review every three years, update within 45 days of a material change, keep five years (CPPA section 7152, checked 2026-10-26); calendar wait W3.

## Questions for counsel

- counsel: Is a CPPA risk assessment required before the pilot, and may processing begin before it is approved; regime United States; needed by W3.
- counsel: Is work-history length a sensitive-data or discrimination proxy that must be removed or measured; regime United States; needed by W2.
- counsel: Is the evaluation set adequately de-identified, and is its use compatible with applicants' notices; regime United States and Australia; needed by W2.
- counsel: Is Southgate an APP entity and is Sydney access a use or a disclosure; regime Australia; needed by W2.
- counsel: Who is the approver of the CPPA assessment; regime United States; needed by W3.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Monica Alvarez, General Counsel, Redwood Freight | this document | pending | pending |
| Redwood privacy officer (not named in the record) | this document | pending | pending |
