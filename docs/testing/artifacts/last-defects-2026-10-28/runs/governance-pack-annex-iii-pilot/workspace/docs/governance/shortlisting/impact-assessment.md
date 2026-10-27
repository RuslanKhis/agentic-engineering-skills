---
document: impact-assessment
system: Shortlisting assistant (Kestrel Logistics)
version: design accepted 2026-09-04; build v0.6.0
status: draft
jurisdictions: [au, eu]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Matthias Brandt, DPO, Kestrel Logistics
trigger: pilot decision at the 2026-11-20 steering meeting (G06, G07)
sources: docs/discovery/shortlisting.md, docs/architecture/shortlisting.md, docs/plans/shortlisting.md, regulatory-memo.md
---

# AI system impact assessment: Shortlisting assistant (Kestrel Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 (paraphrased from the public
abstract, not from the standard, which Kestrel must obtain for conformity;
source: adk-governance-pack reference impact-assessment.md, read 2026-10-25) and mapped to NIST AI RMF 1.0 and
NIST AI 600-1. Draft for Kestrel's risk owner; scores are provisional until
they set them. The Australian Guidance for AI Adoption mapping is skipped:
Australia is in scope only through Southgate Labs' own handling (regulatory-memo.md). Not legal advice.

## Scope and intended use

- **System and functions:** ranks applicants for a vacancy against its must-have requirements and writes a rationale citing the applicant's own CV; the model ranks and explains, the recruiter decides, no write to the ATS (R1, R2, R4, C3, D1).
- **Intended use:** shortlisting for warehouse and driver vacancies by three recruiters for eight weeks (docs/architecture/shortlisting.md Scope gate, docs/discovery/shortlisting.md §3); **unintended or foreseeable misuse:** using the rank as the decision, copying a rationale into a rejection message, using the tool on other vacancy types, sending messages or changing ATS status (docs/discovery/shortlisting.md §5; C3 blocks ATS writes; no control stops copying text, gap).
- **Organisation's role:** Kestrel as provider and deployer, Southgate Labs as builder (regulatory-memo.md Roles; counsel: confirm).
- **Lifecycle stage and trigger:** pilot with real applicant data, before the pilot decision on 2026-11-20 (docs/discovery/shortlisting.md §7, G06).

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| Recruiters (three in the pilot; nine in total) | Use the ranking to decide whom to read and shortlist | no | docs/discovery/shortlisting.md §1 |
| Applicants in the Netherlands, Germany, Poland and Romania | Ranked by a model; may not be read if ranked low | yes: imbalance of power in recruitment, counsel: confirm | docs/discovery/shortlisting.md §4, §5 |
| Applicants aged 50 and over | Lower selection ratio (0.71) | yes | M3 |
| Hiring managers | Receive the shortlist; counter-metric is their interview-stage rejection of shortlisted applicants, baseline 38% | no | docs/discovery/shortlisting.md §3 |
| Works councils (Rotterdam and Duisburg) | Consulted on the pilot | no | W1 |
| Southgate Labs engineers | Read logs and the evaluation set | no | D5 |

## System information

- **Data:** CVs and cover letters with names, contact details, work history, education, and on some CVs photos and dates of birth; free text may reveal age, nationality, health and family status; evaluation set of 1,400 past applications with recruiter decisions (docs/discovery/shortlisting.md §4, D6). Provenance and quality of the recruiter decisions as a "gold label" is not assessed (gap).
- **Model and logic:** gemini-3.5-flash-001 pinned (D2). gap: retirement date and processing region not read from the provider's page or a lifecycle table in this run; proposed goal for adk-model-and-output-contracts. Deterministic parts: redaction step, ownership check, citation validator, output schema (C1, C2, C4, C5).
- **Deployment environment:** Cloud Run and Cloud SQL in europe-west4, Kestrel's project `kestrel-talent-pilot` (D3, docs/architecture/shortlisting.md Scope gate). Operated by Southgate Labs during the pilot; support access from Sydney (D5).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | Applicants aged 50 and over | harm | Ranked lower and so less often in the top third and shortlisted | assumption: high, a ratio of 0.71 was measured offline | assumption: high, loss of a job opportunity | M3, docs/discovery/shortlisting.md §5 |
| H2 | Any applicant | harm | Suitable applicant ranked low is never read | assumption: medium, no measure of how often bottom-half CVs are opened | assumption: high | docs/discovery/shortlisting.md §5, C6 |
| H3 | Applicants by nationality, health or family status | harm | Patterns in past decisions reproduced through free text | assumption: unknown; not measured | assumption: high | R5, C4, C7 |
| H4 | Applicants | harm | A wrong rationale copied into a rejection message | assumption: low to medium | assumption: medium | docs/discovery/shortlisting.md §5, M2 |
| H5 | Applicants | harm | Personal data (dates of birth) reached the model once, in a test run | assumption: low after the fix | assumption: medium | I1 |
| H6 | Applicants | harm | CV text in logs readable from Sydney without a transfer mechanism | assumption: medium | assumption: medium | D4, D5 |
| B1 | Recruiters, hiring managers | benefit | Faster shortlist, from a baseline of 4.5 working days | hypothesis: no measured shortlist-time result yet; M4 measures ranking time only (210 seconds for 120 CVs) | n/a: benefit | docs/discovery/shortlisting.md §3, M4 |
| B2 | Hiring managers | benefit | Fewer shortlisted applicants rejected at interview, from 38% | hypothesis: not measured | n/a: benefit | docs/discovery/shortlisting.md §3 |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1 | Adverse impact measured by age band and gender before each pilot phase; pilot paused on failure | in place, tested offline as a measurement; the failure outcome has not been decided on (M3 is below 0.8); gap: no mitigation goal | C7, M3 |
| H2 | Full list with rationale visible in the recruiter view; recruiters can open every CV | planned: G04 in progress (C6); D7 | C6, D7 |
| H3 | Nationality and marital status removed before the model | in place, tested locally; health and family status not removed; measurement gap | C4, C7 |
| H4 | Rationale must cite the applicant's own CV; ranking shows requirements met or missed; no message sending | in place, tested locally; citing is not the same as being correct | C2, C5, docs/architecture/shortlisting.md Scope gate |
| H5 | Redaction applied to all upload types; C4 test extended; CV skipped and flagged on failure | in place, tested locally after the fix; PDF uploads were disabled until it | I1, C4 |
| H6 | 14-day retention; traces keep no CV text | in place as a retention period; gap: transfer mechanism (W4), access controls | D4, D5 |

## Residual risk and decision

- H1 remains unmitigated: the ratio for applicants aged 50 and over is 0.71, below 0.8, and the accepted-risk entry records that graduation years and career length can signal age (M3, docs/architecture/shortlisting.md Accepted risks). H2 and H3 remain open (C6, C7). H5 is closed as an incident, with redaction tested locally (I1).
- **Accepted by:** gap: acceptance by Kestrel's risk owner; the decider named in the brief is the Head of Talent Acquisition (docs/discovery/shortlisting.md §3); counsel: whether acceptance of H1 is open to the decider at all.
- **Conditions that end acceptance:** any adverse-impact ratio below 0.8 for an age band or gender (C7); a redaction failure (C4, I1); a model change (D2); a new vacancy type (docs/architecture/shortlisting.md Scope gate).

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | Roles (regulatory-memo.md); decider named; risk acceptance not recorded; AI literacy training for recruiters not planned (gap) | docs/discovery/shortlisting.md §6 |
| Map | Scope, parties, EU high-risk proposal (Annex III point 4), Australia through Southgate's own handling | regulatory-memo.md, R1 |
| Measure | M1 agreement 81%, M2 citation 98.6%, M3 adverse impact, M4 time; not measured: override rate, review share, nationality, health and family status, shortlist time | M1, M2, M3, M4 |
| Manage | Contracts C1 to C7, one incident I1, security baseline SB01, SB03, SB05 deferred | C1, I1, SB05 |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| Confabulation | yes | Citation validator withholds rationales that do not cite the applicant's own CV; M2 98.6% on 1,400; suggested action IDs not recorded (gap) | C2, M2 |
| Data privacy | yes | Redaction before the model; 14-day logs; incident I1 | C4, D4, I1 |
| Harmful bias or homogenisation | yes | Adverse impact by age band and gender; disparity measured | C7, M3 |
| Human-AI configuration | yes | Recruiter decides; full list planned; review and override not measured | R4, C6 |
| Information security | yes | ATS credential read-only; route ownership checks; ADK runtime controls deferred; no red-team result recorded (gap) | C1, C3, SB05 |
| Value chain and component integration | yes | Model pinned; provider page not read in this run (gap) | D2 |
| CBRN information or capabilities | n/a: ranks CVs, no open-ended assistant | None | R1 |
| Dangerous, violent or hateful content | n/a: ranking and rationale text for internal users | None | R2 |
| Environmental impacts | n/a: small pilot volume; noted, not measured | None | M4 |
| Information integrity | n/a: no publication of generated text | None | R4 |
| Intellectual property | n/a: output cites the applicant's own CV only | None | C2 |
| Obscene, degrading or abusive content | n/a: text tool on internal data | None | R2 |

## Monitoring and review

- Adverse-impact ratio by age band and gender before each pilot phase, with "pilot paused" as the failure outcome; owner Southgate Labs (C7, M3). gap: the pass threshold and the person who decides are not recorded.
- Share of rationales citing only the applicant's own CV (M2) and ranking agreement (M1) are one-off offline measures; gap: no live monitoring recorded.
- **Review triggers:** model change (D2), new vacancy type or recruiter group, a new incident, a change in law (Annex III date, checked 2026-10-26 in regulatory-memo.md), a change in the GDPR text (D2, I1).

## Adverse impact and equality (if the system ranks, scores or decides about people)

| Group or characteristic | Selection or outcome rate | Ratio to the highest group | Test and sample | Proxies removed | Evidence |
| --- | --- | --- | --- | --- | --- |
| Age 50 and over | gap: rates not recorded in the plan | 0.71 | Four-fifths comparison on top-third ranking, 1,400 past applications, 2026-10-01 to 2026-10-10, build v0.6.0 | Dates of birth; graduation years and career length not removed | M3, C4 |
| Other age bands | gap: rates not recorded | 0.93 to 1.00 | As above | As above | M3 |
| Gender | gap: rate not recorded | 0.96 | As above | Gender cues in names or free text: gap | M3 |
| Nationality | not measured | not measured | gap: not measured | Nationality removed before the model | C4, R5 |
| Health and family status | not measured | not measured | gap: not measured | Not removed | R5, C4 |

- **Less discriminatory alternatives considered and accessibility route:** none recorded (gap: no design record of removing graduation years, capping career-length signals, or ranking by the vacancy's explicit requirements only). counsel: is any disparity justified under EU and national equality law; the four-fifths comparison is a measurement method (M3), and this pack has not verified it as a legal test in the EU. The measurement compares selection rates on the top third of the ranking against recruiter decisions that the model agrees with 81% of the time (M1); counsel: whether this reproduces historical recruiter patterns.
- **Regime checklists:** n/a: no Ontario, New Zealand or Singapore applicants.

## Australia: DTA and AIAF inputs

n/a: no Commonwealth or NSW agency client; not drafted (docs/discovery/shortlisting.md §1).

## EU: FRIA crosswalk (AI Act Article 27, if required)

| Article 27(1) | Pack section | Evidence |
| --- | --- | --- |
| (a) deployer's processes using the system | Scope and intended use; privacy-impact-input-pack.md Processing description | R1, docs/discovery/shortlisting.md §2 |
| (b) period and frequency of use | privacy-impact-input-pack.md Processing description | docs/architecture/shortlisting.md Scope gate |
| (c) categories of persons and groups affected | Interested parties | docs/discovery/shortlisting.md §4 |
| (d) specific risks of harm | Impacts; privacy-impact-input-pack.md Risks and measures | M3 |
| (e) human oversight measures | system-card.md Human oversight | R4, D7, C6 |
| (f) measures if risks materialise, governance, complaints | Measures; Residual risk and decision | C7; gap: complaints route; counsel: required under Article 27? Not apparent for a private employer under Annex III point 4 (checked 2026-10-26) |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Matthias Brandt, DPO | This document | pending | pending |
| Anouk de Vries, counsel | Every counsel: item | pending | pending |
| Femke Jansen, Head of Talent Acquisition (risk owner) | Residual risk and decision | pending | pending |
