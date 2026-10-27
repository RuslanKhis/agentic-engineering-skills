---
document: system-card
system: Shortlisting assistant (Kestrel Logistics)
version: build v0.6.0 (M1 to M4)
status: draft
jurisdictions: [au, eu]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Anouk de Vries, counsel, Kestrel Logistics
sources: docs/discovery/shortlisting.md, docs/architecture/shortlisting.md, docs/plans/shortlisting.md
---

# System card: Shortlisting assistant (Kestrel Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Kestrel reviewers. It describes build v0.6.0 and nothing later. Not
legal advice. Every statement cites a design, plan or evidence ID, a dated
source, or is marked `assumption:` or `counsel:`.

## Intended use

- **Purpose:** ranks the applicants for a warehouse or driver vacancy against its must-have requirements and gives a rationale per applicant citing the applicant's own CV (R1, R2, C2, C5).
- **Users:** three recruiters for eight weeks in the pilot; nine recruiters in Rotterdam and Duisburg in total; internal (docs/architecture/shortlisting.md Scope gate, docs/discovery/shortlisting.md §1).
- **Deployer and provider:** Kestrel Logistics B.V. puts it into service for its own recruiting; Southgate Labs builds it (regulatory-memo.md Roles; counsel: confirm).
- **Decisions it informs:** which applicants a recruiter reads and shortlists. It changes nothing in the ATS and sends no messages (D1, R4, C3).

## Out-of-scope use

- Automatic rejection or any change to an applicant's ATS status (D1, C3).
- Sending messages to applicants (docs/architecture/shortlisting.md Scope gate).
- Vacancy types other than warehouse and driver, such as transport planners, which are in the data register but not in the pilot workflow (docs/discovery/shortlisting.md §3, §4).
- Ranking by age, nationality, gender, health or family status (R5); misuse by copying a rationale into a rejection message has no control (gap; docs/discovery/shortlisting.md §5).

## Limits

- Adverse-impact ratio 0.71 for applicants aged 50 and over, against 0.93 to 1.00 for other bands and 0.96 for gender (M3).
- Age signals can still pass through graduation years and career length (docs/architecture/shortlisting.md Accepted risks).
- Nationality, health and family status are not measured for adverse impact (C7, R5; gap).
- Agreement with past recruiter shortlist decisions is 81%, so the ranking differs from the recruiter's decision about one time in five (M1).
- Incident I1: on 2026-10-06 a test run sent six unredacted CVs with dates of birth to the model because redaction was skipped on PDF uploads; fixed and closed 2026-10-07 (I1).
- Languages and populations not evaluated: gap: no breakdown by language (Dutch, German, Polish, Romanian) or by vacancy type.
- **Model:** gemini-3.5-flash-001 (D2). gap: retirement date and processing region not read from the provider's page or lifecycle table; proposed goal for adk-model-and-output-contracts.

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| Agreement with recruiter shortlist decisions | 81% | No threshold recorded (gap) | 1,400 past applications, 2026-10-01 to 2026-10-10 | v0.6.0 | M1 |
| Rationales citing only the applicant's own CV | 98.6% | No threshold recorded (gap) | 1,400, 2026-10-01 to 2026-10-10 | v0.6.0 | M2 |
| Adverse impact ratio by age band | 0.71 for 50 and over; 0.93 to 1.00 for other bands; gender 0.96 | Four-fifths comparison (0.8) is the method; no pass threshold in the design (gap) | 1,400, 2026-10-01 to 2026-10-10 | v0.6.0 | M3 |
| Median seconds to rank a 120-CV vacancy | 210 | No threshold recorded (gap) | 12 vacancies, 2026-10-08 to 2026-10-10 | v0.6.0 | M4 |

Not yet measured: median working days to shortlist (baseline 4.5) and the interview-stage rejection share (baseline 38%) in the pilot (docs/discovery/shortlisting.md §3; gap: measured by the pilot, no goal); review share and override rate (gap: proposed goal for adk-agent-evaluation); adverse impact for nationality, health and family status (gap).

## Human oversight

- A recruiter decides who is shortlisted and can open every CV; the assistant is read-only (R4, D7, C3). The bottom half of the list stays visible with its rationale: planned, G04 in progress (C6). No share of outputs reviewed or override rate is measured (gap).
- How an applicant or recruiter contests an output, and who owns corrections: gap: no route recorded.
- How the system is stopped: C7 names "pilot paused" when adverse impact fails; gap: who can pause it and how.

## Automated-decision disclosure

- **Kinds of personal information used:** name, work history, education and free-text CV content with dates of birth, photos, nationality and marital status removed first (docs/discovery/shortlisting.md §4, C4).
- **Decisions made solely by the system:** none recorded; no automatic rejection (D1, C3). counsel: whether a ranking that a recruiter relies on is a decision under GDPR Article 22.
- **Decisions where the system does something substantially and directly related:** ranks applicants and writes rationales that inform shortlisting (R1, R2, D1). Australia: n/a: no Australian entity makes the decision (regulatory-memo.md).
- **Meaningful information about the logic:** the model compares each CV with the vacancy's must-have requirements (licence class, shift availability, language, years of experience) and shows which each applicant meets or misses, with cited CV passages (docs/discovery/shortlisting.md §2, C2, C5). The ranking is not deterministic; the model's internal weighting is not available (assumption: LLM ranking; D2).
- **Human review, representations and contest:** recruiter review as above; gap: no applicant route to make representations or contest.
- **Opt-out or appeal, where offered:** counsel: whether Article 22 or national law requires an alternative route; none recorded.
- **Quebec s 12.1 notice and review:** n/a: no Canadian applicants (docs/discovery/shortlisting.md §4).
- **Government client facts:** n/a: private client (docs/discovery/shortlisting.md §1).

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** the users are recruiters who are told it is an assistant (README.md); applicants do not interact with it. counsel: Article 50(1) and applicant information duties; gap: no disclosure contract or UI test recorded.
- **Hand-off to a person:** n/a: the recruiter is the person; no applicant-facing channel.
- **Persona, memory of the user or relationship features:** none recorded (R1, R2).
- **Public claims about the system:** none recorded; any claim about speed or fairness needs M records; the only speed measure is ranking time (M4), not shortlist time, and the fairness measure shows a disparity (M3).
- **Singapore chatbot info card and Ontario job-posting disclosure:** n/a: no Singapore or Ontario applicants (docs/discovery/shortlisting.md §4).

## Data

- Reads CVs and vacancy requirements from the ATS with a read-only credential; stores prompts and responses in logs for 14 days; the evaluation set holds 1,400 past applications with names and contact details removed (C3, D4, D6). See privacy-impact-input-pack.md; gap: stores, retention and erasure beyond logs.
- Controls: redaction before the model (C4), recruiter-scoped access (C1), traces keep no CV text (D4).

## Contact

- **Owner:** Femke Jansen, Head of Talent Acquisition (source: brief accepted 2026-08-21, docs/discovery/shortlisting.md §6).
- **Report a problem or make a privacy complaint:** gap: no channel confirmed; Kestrel's DPO is Matthias Brandt (source: docs/discovery/shortlisting.md §6, 2026-08-21; counsel: confirm the complaint route to the supervisory authority).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Anouk de Vries, counsel | This document | pending | pending |
| Matthias Brandt, DPO | Automated-decision disclosure and Data | pending | pending |
