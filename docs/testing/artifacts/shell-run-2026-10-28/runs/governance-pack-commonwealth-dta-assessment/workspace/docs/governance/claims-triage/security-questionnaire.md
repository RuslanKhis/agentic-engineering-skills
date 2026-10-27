---
document: security-questionnaire
system: Claims triage assistant (Compensation Claims Office)
version: build v0.6.3
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CCO Chief Security Officer (Anita Desai)
sources: docs/architecture/claims-triage.md, docs/plans/claims-triage.md
---

# Security questionnaire answer bank: Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into the CCO's vendor or security questionnaire. Each answer states what holds for build v0.6.3, with its status. Planned is never written as in place. The design's security baseline lists SB01, SB03 and SB05 only; other baseline rules are answered `gap:`.

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | Cloud Run, Cloud SQL and logs in australia-southeast1; Gemini on Vertex AI with the endpoint in australia-southeast1. gap: the model's processing region not read at the provider's page | in place for hosting (design); gap for model region | D1, D2 |
| Overseas access | Who can access our data from outside our country? | Southgate Labs staff in Sydney access logs and the evaluation set, within Australia. gap: remote access from elsewhere and subcontractors not recorded; counsel: APP 8 use or disclosure for any offshore Google support access | gap | D4 |
| Identity and access | How are users authenticated and authorised? | Officers sign in through the CCO's identity provider; an officer reads only claims in their team's queue; /api routes secured | in place, tested locally | C1, SB01, G02/A2 |
| Encryption | In transit and at rest? | gap: not recorded in the design; provider defaults not read | gap | D2 |
| Secrets | How are credentials managed? | The case system credential is a read-only service account | in place, tested locally | C3, SB03, G02/A3 |
| Logging and retention | What is logged, for how long, who reads it? | Prompts and drafts are logged for 30 days in australia-southeast1; Southgate Labs can read logs; gap: no scrubbing of claim content | in place for retention; gap for scrubbing | D2, D3, D4 |
| Model provider data use | Is our data used to train models? Retained? | gap: not read at the provider's terms or page; see privacy-impact-input-pack.md | gap | D1 |
| Sub-processors | Which third parties process our data? | Google Cloud (hosting, database, model); gap: any others not recorded | gap | D1, D2 |
| Prompt injection and agency | How is unintended action prevented? | The assistant has no write path: read-only account; the officer decides | in place, tested locally for no write; adversarial testing gap | C3, R4 |
| Output handling | How is model output rendered safely? | gap: SB10 is not in the design's baseline table | gap | SB05 |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | gap: no screening evidence; a goal for protect-adk-sensitive-data | gap | D3 |
| Abuse and cost limits | What limits runaway use? | gap: no call caps recorded; pilot size is 20 officers | gap | docs/discovery/claims-triage.md §6 |
| Human oversight | Who reviews outputs? | The officer accepts or changes every draft and it is recorded | in place, tested locally | R4, C4, G03/A1 |
| Vulnerability management | Dependency audits, scans, penetration test? | gap: not recorded; IRAP assessment booked 2026-11-16 | planned: W1 | W1 |
| Secure development | Code review, CI gates, release and rollback? | gap: not recorded; google-adk 2.12.0 and Python 3.12 are pinned | gap | docs/architecture/claims-triage.md Scope gate |
| Incident response | How are incidents detected and reported? | gap: no incident procedure recorded. Clocks: the supplier tells the CCO under its contract (gap: the contract); an eligible data breach is assessed within 30 days and notified as soon as practicable (checked 2026-10-26); the CCO's own ISM and PSPF reporting is agency: | gap | docs/architecture/claims-triage.md |
| Deletion | How is data deleted at end of contract or on request? | Logs expire at 30 days; decisions table and evaluation set: gap: retention undecided | gap | D3, D5 |
| Availability and recovery | Availability target and recovery plan? | gap: none recorded; pilot only | gap | docs/discovery/claims-triage.md §6 |
| AI security baseline | Which AI security code do you follow? | n/a: not requested | n/a | SB05 |
| Government security policy | Which policy does the system meet? | Commonwealth agency: ISM and PSPF as the agency directs; the environment is assessed against PROTECTED by the CCO's security team; IRAP assessment booked 2026-11-16; ADK runtime hardening deferred until production | planned: W1; deferred: production (SB05); agency: direction | D2, W1, SB05 |
| Certifications | Which certifications apply? | gap: the cloud provider's reports were not read in this session; the application holds none | gap | D2 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO Chief Security Officer (Anita Desai) | this document | pending | pending |
