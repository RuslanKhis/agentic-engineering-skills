---
document: system-card
system: applicant screener (build v0.5.2)
version: build v0.5.2
status: draft
jurisdictions: [au, us]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Monica Alvarez, General Counsel, Redwood Freight Inc.
sources: docs/discovery/screener.md, docs/architecture/screener.md, docs/plans/screener.md
---

# System card: applicant screener

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Redwood reviewers. It describes build v0.5.2 and nothing later. Not legal advice. Every statement cites a design, plan or evidence ID, a dated source, or is marked `assumption:` or `counsel:`. All controls below are evidenced locally only; none is in production.

## Intended use

- **Purpose:** scores each application 0-100 against the role's requirements, shows the requirements behind each score, ranks applications per requisition and labels the bottom group "not recommended" (scores under 40) for recruiters (R1, R2, R3, C1, C3).
- **Users:** 11 recruiters in Oakland; 3 in New York if later approved; internal (docs/discovery/screener.md §5).
- **Deployer and provider:** Redwood Freight puts it into service for its own hiring; Southgate Labs built it (regulatory-memo.md Roles; counsel: confirm).
- **Decisions it informs:** which applications a recruiter reads first and which are rejected; it may not change an application's stage (C2, R4).

## Out-of-scope use

- Rejecting applicants and messaging applicants (docs/architecture/screener.md Scope gate).
- Use at the New York warehouses or on New York City candidates: not designed, evaluated or approved; NYC Local Law 144 conditions are not met (docs/architecture/screener.md Scope gate; regulatory-memo.md Summary; W4).
- Other roles than warehouse associate and forklift operator (docs/discovery/screener.md §2).
- Bulk rejection of the "not recommended" group without opening applications: foreseeable and, per the requester, usual (source: requester (Southgate Labs), 2026-10-28); no control limits it (gap; M4).

## Limits

- Age impact ratio for "recommended" is 0.74, below the four-fifths rule of thumb of 0.8 (M2).
- Age is inferred from work-history length for the measurement where no date of birth exists, and work-history length is not removed by C4 (M2, C4); gap: whether it is a scoring input.
- Sex ratio 0.91 (M3); no measurement by race, ethnicity, national origin or disability (gap).
- M1 is agreement with past recruiter advance decisions, so it also reproduces past patterns (M1, docs/discovery/screener.md §4).
- Only warehouse roles in California were designed for; languages and application formats not evaluated (gap).
- Free text may reveal age, disability or national origin (docs/discovery/screener.md §3).
- **Model:** `gemini-3.5-flash-001` (D1); retirement date and processing region gap: not read from the lifecycle table or model page (no network access, 2026-10-28).

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| Backtest agreement with recruiter advance decisions | 78% | none set: gap | 6,000 past applications, 2026-09-22 to 2026-10-03 | v0.5.2 | M1 |
| Impact ratio by age, "recommended" (40 and over divided by under 40) | 0.74 | four-fifths rule of thumb 0.8 (29 CFR 1607.4(D), checked 2026-10-26) | 6,000, 2026-09-22 to 2026-10-03; age inferred from work-history length where no date of birth | v0.5.2 | M2 |
| Impact ratio by sex | 0.91 | 0.8 as above | 6,000, 2026-09-22 to 2026-10-03 | v0.5.2 | M3 |
| Share of "not recommended" applications a recruiter opened before rejecting | 6% | none set: gap | 410 applications, shadow trial 2026-10-06 to 2026-10-17 | v0.5.2 | M4 |

Not yet measured: impact ratios by race, ethnicity and disability; median days to first recruiter contact (baseline 9 days) and 90-day retention (baseline 71%) with the screener; pilot-time ratios (gap; no goal in docs/plans/screener.md; proposed goal for adk-agent-evaluation).

## Human oversight

- A recruiter makes every rejection (R4) and the screener cannot change an application's stage (C2, evidenced local, G03/A2). The share of "not recommended" applications opened before rejection was 6% (M4; denominator gap:). Override rate: gap: not measured.
- How an applicant contests or corrects an output, and who owns corrections: gap: no route in the design.
- How the system is stopped or rolled back, and by whom: gap: not recorded; SB05 on the ADK runtime is deferred to production (SB05).

## Automated-decision disclosure

- **Kinds of personal information used:** name, contact, address, work history, availability, certifications and answers to screening questions; age, date of birth, graduation years and photos are removed first (docs/discovery/screener.md §3, C4).
- **Decisions made solely by the system:** none recorded; the screener does not reject (C2, R4); counsel: whether in practice the "not recommended" label decides (M4).
- **Decisions where the system does something substantially and directly related:** scores, ranks and labels applicants for hiring (R1, R2, C3).
- **Meaningful information about the logic:** a score lists the requirements met and missed with the application text behind each (C1); the label applies to scores under 40 (C3).
- **Human review, representations and contest:** recruiter reviews (R4); applicant representations and contest route gap: none designed.
- **Opt-out or appeal, where offered:** none offered (gap); counsel: whether a human-appeal exception or opt-out is required from 1 January 2027 (checked 2026-10-26; W5).
- **Government client facts:** n/a: private client (docs/discovery/screener.md §1).
- **APP 1.8 block:** n/a: Redwood is not an Australian APP entity on the record (regulatory-memo.md Australia: Automated decisions (APP 1.7)).

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** n/a: no conversational interface; applicants do not interact with the screener (docs/architecture/screener.md Scope gate); whether applicants are told AI scores their application: gap: not in the record (W5).
- **Hand-off to a person:** n/a: recruiters are the human route (R4).
- **Persona, memory of the user or relationship features:** none (R1 to R4).
- **Public claims about the system:** none recorded; any accuracy or fairness claim must cite M1 to M4 as defined, and "bias-free" is not supported (M2; gap: no claim approved).
- **Ontario job-posting disclosure:** n/a: no Ontario use.

## Data

- The screener reads applications from Greenhouse and writes a score, rank and label to a Greenhouse custom field and BigQuery; the evaluation set is 6,000 past applications with names and contact details removed (D2, D5; privacy-impact-input-pack.md Data flows).
- Redaction before scoring (C4, evidenced local, G01/A2); retention and log controls gap: not recorded (privacy-impact-input-pack.md Retention and erasure).

## Contact

- **Owner:** Southgate Labs engagement lead Priya Raman for the build; Redwood owner and Kevin Ortiz as decider (source: docs/discovery/screener.md §5, 2026-08-14); gap: Redwood's operating owner after the pilot.
- **Report a problem or make a privacy complaint:** gap: no channel confirmed by Redwood.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Monica Alvarez, General Counsel, Redwood Freight | this document | pending | pending |
