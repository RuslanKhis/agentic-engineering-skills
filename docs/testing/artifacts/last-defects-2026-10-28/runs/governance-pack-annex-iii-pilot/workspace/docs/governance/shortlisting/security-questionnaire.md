---
document: security-questionnaire
system: Shortlisting assistant (Kestrel Logistics)
version: build v0.6.0
status: draft
jurisdictions: [au, eu]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Matthias Brandt, DPO, Kestrel Logistics (gap: no CISO or security reviewer named in the record)
sources: docs/architecture/shortlisting.md, docs/plans/shortlisting.md
---

# Security questionnaire answer bank: Shortlisting assistant (Kestrel Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into Kestrel's vendor or security questionnaire. Status words:
`in place` (evidence recorded; all of it is local or offline in this build),
`planned` (goal ID), `deferred` (trigger) or `n/a` (reason). The design's
security baseline table lists only SB01, SB03 and SB05; every other baseline
topic is answered gap.

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | Cloud Run and Cloud SQL in europe-west4; Gemini endpoint in europe-west4; project `kestrel-talent-pilot`. gap: the model's processing region from the provider's page; the log sink region | in place for hosting as designed; gap for the model's processing region | D2, D3 |
| Overseas access | Who can access our data from outside our country, and under what transfer mechanism? | Two Southgate Labs engineers in Sydney have read access to logs and the evaluation set during the pilot and six weeks after. gap: SCC Module 2 and transfer impact assessment (W4); Australian Privacy Act position of Southgate, counsel | gap | D5, W4, transfer-assessment.md |
| Identity and access | How are users authenticated and authorised? | The API acts as the verified recruiter; the tool rechecks ownership; a recruiter reads only the vacancies and CVs they own, otherwise 404. gap: no SB row for sign-in, session or administrative access | in place, tested locally | C1, SB01, G02/A2 |
| Encryption | Is data encrypted in transit and at rest? | gap: not recorded in the design; provider default is not cited (no network access in this run) | gap | docs/architecture/shortlisting.md |
| Secrets | How are credentials managed? | The ATS credential is read-only and no write tool is bound. gap: storage, rotation and scanning of credentials | in place for read-only scope, tested locally; gap for custody | C3, SB03, G02/A3 |
| Logging and retention | What is logged, for how long, who can read it? | Prompts and responses are logged for 14 days for debugging; traces keep no CV text; Southgate engineers can read the logs. gap: sink, region, access controls and audit of readers; the log-hygiene baseline rule is not in the design's table | in place as a retention decision; gap for controls | D4, D5 |
| Model provider data use | Is our data used to train models? Is it retained? | See privacy-impact-input-pack.md, Model provider data use (one home for this fact) | gap: provider page not read | D2 |
| Sub-processors | Which third parties process our data? | Google Cloud (hosting, Vertex AI) and Southgate Labs (support access). gap: Google's sub-processor list, and Kestrel's agreements with both | gap | D2, D3, D5 |
| Prompt injection and agency | How is the agent prevented from taking unintended actions? | No write tool is bound and the ATS credential is read-only, so a manipulated model cannot change applicant status; a CV is untrusted text that could try to steer the ranking. gap: no adversarial test of CV content steering the ranking and no red-team result | in place for write prevention, tested locally; gap for ranking manipulation | C3, R4 |
| Output handling | How is model output rendered safely? | gap: no rendering rule for rationales in the recruiter view in the design | gap | C2, C5 |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | Dates of birth, photos, nationality and marital status are removed before the model call; a CV that fails is skipped and flagged. Incident I1 showed that PDF uploads skipped redaction (six CVs, 2026-10-06); fixed for all upload types and the test extended. gap: measured detector coverage not recorded (protect-adk-sensitive-data evidence); health and family status in free text are not removed; logs hold CV text | in place, tested locally after I1; gap for coverage | C4, I1, G01/A2, D4 |
| Abuse and cost limits | What limits runaway use? | gap: no call cap, spend stop or rate limit recorded; M4 measured ranking time only | gap | M4 |
| Human oversight | Who reviews or approves outputs and actions? | The recruiter decides who is shortlisted; no automatic rejection; the full list view is planned. gap: review and override rates | in place by design (D1, R4); planned for the full list: G04 | D1, R4, C6 |
| Vulnerability management | Dependency audits, scans, penetration test? | gap: none recorded in the design | gap | docs/architecture/shortlisting.md |
| Secure development | Code review, CI gates, release and rollback? | gap: not recorded; the pilot pauses on adverse-impact failure (C7); build v0.6.0 | gap | C7, M1 |
| Incident response | How are incidents detected, reported and handled? | One incident is recorded: I1, severity 3, response PDF uploads disabled, closed 2026-10-07. Clocks in scope: Southgate to Kestrel without undue delay (contract: gap); GDPR 72 hours from Kestrel to the supervisory authority (counsel: whether I1 was reportable); AI Act Article 73 if high-risk, from 2 December 2027 (checked 2026-10-26); NIS2 24 and 72 hours if Kestrel is in scope (counsel); Australia: an eligible data breach assessed within 30 days and notified as soon as practicable, only if Southgate is an APP entity and the Act reaches the handling (counsel; source: adk-governance-pack reference system-card-and-questionnaire.md, read 2026-10-26) | in place for the one incident record; gap for the process | I1, W2 |
| Deletion | How is data deleted at end of contract or on request? | gap: no erasure path or end-of-contract deletion recorded; logs expire at 14 days | gap | D4, D6 |
| Availability and recovery | What are the availability target and recovery plan? | gap: none recorded; pilot scale only | gap | M4 |
| AI security baseline | Which AI security code or standard do you follow? | n/a: not requested; UK DSIT code not in scope (no UK client) | n/a | docs/discovery/shortlisting.md §1 |
| Government security policy | Which government security policy does the system meet? | n/a: private client | n/a | docs/discovery/shortlisting.md §1 |
| Certifications | Which certifications apply? | The application has none. Google Cloud's certifications cover its infrastructure only; gap: not read in this run (no network access) | gap | D3 |

- Runtime hardening for ADK is deferred until production (SB05, deferred: production). The pilot uses real applicant data, so reviewers may query it; counsel and the DPO should decide whether the pilot can start under it (D3, SB05).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Matthias Brandt, DPO | This document | pending | pending |
| Kestrel security reviewer (gap: not named) | Technical answers | pending | pending |
| Anouk de Vries, counsel | Overseas access and incident rows | pending | pending |
