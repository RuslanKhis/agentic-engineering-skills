---
document: security-questionnaire
system: Staff HR assistant (Wattle & Co)
version: build v0.4.1 (M1 to M3)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Head of Security (Daniel Okoro)
sources: docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md
---

# Security questionnaire answer bank: Staff HR assistant (Wattle & Co)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into Wattle & Co's security review (W2). Each answer states
what holds for the build above, with its status: `in place` (evidence
recorded), `planned` (goal ID), `deferred` (trigger) or `n/a` (reason).
Planned is never written as in place. The design's baseline table lists only
SB01, SB03 and SB05; other baseline rules are answered `gap:`.

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | Cloud Run, Cloud SQL and logs in australia-southeast1; Gemini endpoint in australia-southeast1; error bodies, including request and response bodies, in Sentry's US region. gap: the model's processing region is unread | in place for Sydney hosting; US flow is live in the design | D1, D2, D4 |
| Overseas access | Who can access our data from outside our country, and under what transfer mechanism? | Southgate Labs engineers read logs and Sentry from Sydney, so no staff access from outside Australia is recorded; Sentry holds data in the US; APP 8 and s 16C facts are in privacy-impact-input-pack.md; gap: Sentry contract and its staff access | gap | D4, D5 |
| Identity and access | How are users authenticated and authorised? | Entra ID sign-in, employee ID from the verified token; tools scoped to own record or to reports; the /api routes and Workday credential are baseline items | in place, tested locally | D7, C1, C2, SB01, SB03, G02/A2 |
| Encryption | Is data encrypted in transit and at rest? | gap: not recorded; Google Cloud defaults not checked in this session | gap | D2 |
| Secrets | How are credentials managed? | Workday integration user with read-only scope, granted 2026-10-08; storage of the credential is baseline item SB03 | in place, tested locally | W1, SB03, G02/A4 |
| Logging and retention | What is logged, for how long, who can read it? | Prompts and answers after phrase-list masking, for 30 days in Cloud Logging; Southgate Labs engineers read them; masking caught 82% of synthetic union and medical phrases; Sentry retention is unknown | partially in place; masking planned under G04 | D3, D5, C4, M2 |
| Model provider data use | Is our data used to train models? Is it retained? | gap: not recorded and the model page was not read in this session | gap | D1 |
| Sub-processors | Which third parties process our data? | Google Cloud (Sydney), Sentry (US), Workday (source system); gap: no contracts recorded | gap | D1, D2, D4 |
| Prompt injection and agency | How is the agent prevented from taking unintended actions? | No write tool; read-only Workday user; refusal on out-of-scope reads; gap: no injection test recorded | in place, tested locally for write and scope | C1, C2, C3 |
| Output handling | How is model output rendered safely? | gap: rendering is not in the record; the attendance summary uses an output schema | gap | C5 |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | Phrase-list masking before logging; entry dropped on failure; no screening before the model; not recorded for Sentry | partially in place | C4, M2 |
| Abuse and cost limits | What limits runaway use? | gap: no rate or spend limit is recorded | gap | SB05 |
| Human oversight | Who reviews or approves outputs and actions? | The assistant takes no action; the manager reviews summaries; gap: checking not measured | in place, tested locally | C3, C5 |
| Vulnerability management | Dependency audits, scans, penetration test? | gap: none recorded | gap | SB05 |
| Secure development | Code review, CI gates, release and rollback? | gap: not recorded; ADK runtime baseline deferred | deferred: production | SB05 |
| Incident response | How are incidents detected, reported and handled? | No incident records exist in the plan; Australian eligible data breach assessed within 30 days (s 26WH, checked 2026-10-26); gap: who notifies, contact and alerts; counsel: which entity notifies | gap | docs/plans/hr-assistant.md, D4 |
| Deletion | How is data deleted at end of contract or on request? | Logs expire after 30 days; gap: Sentry, Cloud SQL and per-person deletion | partially in place | D3, D4 |
| Availability and recovery | What are the availability target and recovery plan? | gap: none recorded | gap | D2 |
| AI security baseline | Which AI security code or standard do you follow? | n/a: not requested | n/a | D1 |
| Government security policy | Which government security policy does the system meet? | n/a: private client | n/a | docs/discovery/hr-assistant.md §1 |
| Certifications | Which certifications apply? | Google Cloud's own, not cited in this session; gap: the application has none recorded | gap | D2 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Head of Security (Daniel Okoro) | this document | pending | pending |
