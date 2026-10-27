---
document: impact-assessment
system: applicant screener (build v0.5.2)
version: build v0.5.2, design accepted 2026-09-02
status: draft
jurisdictions: [au, us]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Monica Alvarez, General Counsel, Redwood Freight Inc.
trigger: California pilot decision on 2026-11-18 (docs/discovery/screener.md §6; G05)
sources: docs/discovery/screener.md, docs/architecture/screener.md, docs/plans/screener.md, regulatory-memo.md
---

# AI system impact assessment: applicant screener

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 (topic headings from public abstracts, not the standard; conformity needs Redwood's own copy) and mapped to NIST AI RMF 1.0 and NIST AI 600-1. Draft for Redwood's risk owner; scores are provisional until they set them. Not legal advice.

## Scope and intended use

- **System and functions:** scores applications 0-100, ranks them per requisition and labels scores under 40 "not recommended"; the model produces the score and evidence, code applies the label and the redaction (R1, R2, C1, C3, C4).
- **Intended use:** first screen of warehouse associate and forklift operator applications at the California warehouses, used by recruiters (docs/discovery/screener.md §2, §5); **unintended or foreseeable misuse:** use on New York candidates (design excludes it, docs/architecture/screener.md Scope gate); bulk rejection of the "not recommended" group without reading (source: requester (Southgate Labs), 2026-10-28; M4); no control stops either (gap).
- **Organisation's role:** Redwood is the deployer and employer; Southgate Labs is the developer under contract (regulatory-memo.md Roles; counsel: confirm).
- **Lifecycle stage and trigger:** pilot, 8 weeks, decision 2026-11-18 (docs/architecture/screener.md Scope gate; G05).

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| Applicants for California warehouse roles | scored, ranked and possibly never read | assumption: older applicants, applicants with disabilities and applicants whose national origin shows in free text are at higher risk | docs/discovery/screener.md §3, §4 |
| Applicants in New York | not in scope of the pilot; present in the data register | assumption: same as above | docs/discovery/screener.md §3, docs/architecture/screener.md Scope gate |
| Recruiters (11 Oakland, 3 New York) | users; their actions are logged (M4) | no | docs/discovery/screener.md §5 |
| Redwood | employer liability; time to first contact | n/a: not a person at risk | docs/discovery/screener.md §2 |
| Southgate Labs engineers (two, Sydney) | handle real applications | no | D4 |

## System information

- **Data:** real applications from Greenhouse; past applications with hiring outcomes 2023-2026 (6,000 used, names and contact details removed) (docs/discovery/screener.md §3, D5). Provenance risk: outcomes are past human decisions, which may carry past patterns (docs/discovery/screener.md §4).
- **Model and logic:** Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` (D1); retirement date gap: not read from the lifecycle page or table (no network access); deterministic parts: label threshold 40 (C3) and redaction (C4).
- **Deployment environment:** Python 3.12, google-adk 2.12.0, Cloud Run in us-west1 (Oregon), BigQuery, Greenhouse custom field; operator gap: not recorded (docs/architecture/screener.md Scope gate, D2).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | Applicants | harm | A "not recommended" applicant is never read by a person | assumption: likely; recruiters usually reject in bulk | assumption: high; lost job opportunity | docs/discovery/screener.md §4, M4 |
| H2 | Applicants aged 40 and over | harm | Lower rate of "recommended": ratio 0.74 | measured in backtest: ratio 0.74 | assumption: high | M2 |
| H3 | Applicants with disabilities or protected national origin | harm | Free text signals affect scores; not measured | assumption: possible | assumption: high | docs/discovery/screener.md §3 |
| H4 | Applicants by sex and by race or ethnicity | harm | Sex ratio 0.91 measured; race and ethnicity not measured | sex ratio 0.91 (M3); race and ethnicity gap: not measured | assumption: moderate | M3 |
| H5 | Past applicants | harm | Real data exposed in the evaluation set and logs | assumption: possible | assumption: moderate | D4, D5 |
| H6 | Recruiters and applicants | harm | Automation bias: recruiters trust the label | assumption: likely | assumption: moderate | M4 |
| B1 | Redwood and applicants | benefit | Median days to first recruiter contact falls from the 9-day baseline | hypothesis: not yet measured | n/a: benefit | docs/discovery/screener.md §2 |
| B2 | Redwood | benefit | 90-day retention of hires holds or rises from 71% | hypothesis: not yet measured | n/a: benefit | docs/discovery/screener.md §2 |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1 | Recruiter makes every rejection; screener cannot change stage; "not recommended" group can be opened | in place, tested locally for C2; the reading itself is not enforced: gap: proposed goal for adk-engineer on a sampling or open-before-reject rule | R4, C2, D3, G03/A2 |
| H2 | Age, date of birth, graduation years and photos removed | in place, tested locally; ratio remains 0.74 so insufficient: gap: remediation goal | C4, G01/A2, M2 |
| H3 | none | gap: measurement and accommodation route; proposed goal for adk-agent-evaluation | docs/discovery/screener.md §3 |
| H4 | sex ratio measured | in place for sex (M3); gap: race and ethnicity, intersections | M3 |
| H5 | names and contact details removed from the evaluation set | in place per D5; gap: access controls, retention, log contents | D5, D4 |
| H6 | requirements evidence shown per score (C1) | in place, tested locally; gap: reviewer sampling and training | C1, G02/A1 |
| B1, B2 | pilot measurement | planned: not in any goal in docs/plans/screener.md; gap | docs/plans/screener.md |

## Residual risk and decision

- H1, H2 and H3 remain high on the record: the only mitigations are C2 and C4 and M2 shows the age ratio is still 0.74 after C4 (H1, H2, C2, C4, M2).
- **Accepted by:** gap: acceptance by Kevin Ortiz (the decider, docs/discovery/screener.md §2); counsel: whether acceptance is proper before the open questions in regulatory-memo.md close.
- **Conditions that end acceptance:** any impact ratio below 0.8 on a protected group on the pilot's data; a recruiter-opened share (M4) that stays near 6%; any New York use; a model change (D1); a new role family (docs/discovery/screener.md §2).

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | decider Kevin Ortiz; General Counsel reviewer; acceptance not recorded; AI literacy for recruiters gap | docs/discovery/screener.md §5, W2 |
| Map | scope, parties, regimes: Australia (consultancy only) and United States; no AI Act classification | regulatory-memo.md, D4 |
| Measure | M1 78% agreement; M2 age ratio 0.74; M3 sex ratio 0.91; M4 6%; unmeasured: race and ethnicity, disability, pilot-time ratios, retention counter-metric | M1, M2, M3, M4 |
| Manage | C2, C4, C3 in place locally; production hardening deferred; no incident records | C2, C3, C4, SB05 |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| CBRN information or capabilities | n/a: narrow scoring tool | none | R1 |
| Confabulation | yes | requirements met and missed must cite application text; score withheld otherwise; no suggested-action IDs recorded | C1, G02/A1 |
| Dangerous, violent or hateful content | n/a: no generated public text | none | R3 |
| Data privacy | yes | redaction; evaluation set de-identification in part | C4, D5 |
| Environmental impacts | n/a: noted only, not measured | none | D1 |
| Harmful bias or homogenisation | yes | age removal; impact ratios M2, M3; no red-team or suggested-action IDs recorded | C4, M2, M3 |
| Human-AI configuration | yes | recruiter decides; automation bias risk shown by M4 | R4, M4 |
| Information integrity | n/a: output is internal, not published text | none | D2 |
| Information security | yes | SB01 and SB03 in place locally; SB05 deferred; no red-team result; applicant text as injection route: gap | SB01, SB03, SB05 |
| Intellectual property | n/a: no generated or retrieved third-party content | none | R1 |
| Obscene, degrading or abusive content | n/a: text scoring of applications | none | R1 |
| Value chain and component integration | yes | pinned model, retirement date gap, Greenhouse API scope | D1, W1 |

Texas TRAIGA's NIST defence is n/a: no Texas applicants recorded (docs/discovery/screener.md §3); gap: residence data.

## Monitoring and review

- Watch the impact ratio by age, sex, race and ethnicity on pilot data, threshold 0.8 proposed, owner Southgate Labs with Redwood talent operations (M2, M3; threshold: assumption: four-fifths rule, 29 CFR 1607.4(D), checked 2026-10-26).
- Watch the share of "not recommended" applications opened before rejection, owner Redwood talent operations (M4).
- **Review triggers:** model change or retirement (D1), a new user group such as New York recruiters, new data, an incident, a change in law (docs/discovery/screener.md §6; counsel: dates in regulatory-memo.md Applicable dates).

## Adverse impact and equality

| Group or characteristic | Selection or outcome rate | Ratio to the highest group | Test and sample | Proxies removed | Evidence |
| --- | --- | --- | --- | --- | --- |
| Age 40 and over versus under 40, "recommended" | gap: rates not recorded in the plan | 0.74 | four-fifths comparison, 6,000 past applications, 2026-09-22 to 2026-10-03, build v0.5.2; age inferred from work-history length where no date of birth | age, date of birth, graduation years, photos (C4); work-history length not removed | M2 |
| Sex | gap: rates not recorded | 0.91 | four-fifths comparison, 6,000, same window and build | none recorded | M3 |
| Race and ethnicity, and intersections with sex | gap: not measured | gap | gap: required for NYC Local Law 144 (checked 2026-10-26) | none recorded | gap |
| Disability | gap: not measured | gap | gap | none recorded | gap |

- **Less discriminatory alternatives considered and accessibility route:** gap: none recorded in docs/architecture/screener.md; no accommodation route in the workflow (ADA); counsel: is the age disparity justified, and what is the accommodation duty.
- **Regime checklists:** n/a: no Ontario, New Zealand or Singapore use.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Monica Alvarez, General Counsel, Redwood Freight | this document | pending | pending |
| Kevin Ortiz, VP People (risk owner, residual-risk acceptance) | Residual risk and decision | pending | pending |
