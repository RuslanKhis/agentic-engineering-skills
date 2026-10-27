---
document: security-questionnaire
system: HR assistant (Érable Logistics)
version: build v0.5.0
status: draft
jurisdictions: [au, ca]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Érable security lead (not named in the record; gap: the CISO or equivalent)
sources: docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md
---

# Security questionnaire answer bank: HR assistant (Érable Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into Érable's vendor or security questionnaire. Each answer states what holds for build v0.5.0, with its status: `in place` (evidence recorded), `planned` (goal ID), `deferred` (trigger) or `n/a` (reason). The design's baseline table lists only SB01, SB03 and SB05; every other rule is answered `gap:` (docs/architecture/hr-assistant.md Security baseline). Counsel flag: the system decides leave for staff, so counsel reviews this too (counsel: confirm).

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | Cloud Run, Cloud SQL and logs in northamerica-northeast2 (Toronto); Gemini 3.5 Flash through the global endpoint, processing in the United States per the model page read 2026-09-10, not re-read | in place as designed, tested locally only (no production deployment recorded) | D1, D2 |
| Overseas access | Who can access our data from outside our country, and under what transfer mechanism? | Southgate Labs engineers in Sydney read logs during the pilot and a three-month support period; no mechanism yet: a Quebec s 17 assessment and written agreement are needed (counsel: adequate protection) | planned: wait W4; gap: contract and access method | D4, transfer-assessment.md |
| Identity and access | How are users authenticated and authorised? | A tool scoped to the verified employee ID; an employee reads and requests leave only for themselves; /api routes at Build depth | in place, tested locally | C2, SB01, G02/A2 |
| Encryption | Is data encrypted in transit and at rest? | gap: not recorded in the design; Google Cloud defaults not cited | gap: proposed goal for adk-release-engineering | D2 |
| Secrets | How are credentials managed? | The UKG integration credential is at Build depth; storage mechanism not recorded (gap) | in place at Build depth, tested locally (SB03); gap: rotation and storage | SB03, G03/A4, W1 |
| Logging and retention | What is logged, for how long, who can read it? | Prompts and answers with the employee ID for 60 days; readable by Southgate engineers in Sydney; no redaction recorded | in place as designed; gap: log pseudonymisation and role scoping | D3, D4 |
| Model provider data use | Is our data used to train models? Is it retained? | See privacy-impact-input-pack.md Model provider data use; Google's page states no training without permission, caching up to 24 hours, abuse-monitoring storage up to 90 days (source: adk-governance-pack reference privacy-and-records.md, pages read 2026-10-25, not re-read); the project's settings are not recorded | gap: project settings | D1, privacy-impact-input-pack.md |
| Sub-processors | Which third parties process our data? | Google Cloud and Gemini; Southgate Labs; UKG as the system of record; Google's own sub-processor list not reviewed | gap: sub-processor list not read | D1, D2, D4 |
| Prompt injection and agency | How is the agent prevented from taking unintended actions? | The rule, not the model, decides approval (D5); the model only extracts dates and leave type; the tool is scoped to the employee. No adversarial results recorded | in place for the split, tested locally; gap: adversarial suite | D5, C2, C3 |
| Output handling | How is model output rendered safely? | gap: not recorded; SB10 is not in the design's baseline table | gap | SB01 |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | No screening is recorded; leave reasons may mention health or family matters | gap: proposed goal for protect-adk-sensitive-data | docs/discovery/hr-assistant.md §3, D3 |
| Abuse and cost limits | What limits runaway use? | gap: no call cap, rate limit or spend stop recorded in the contracts | gap | C1 |
| Human oversight | Who reviews or approves outputs and actions? | Managers review non-routine requests (C5); no person reviews auto-approvals (C4); HR receives handovers on uncited answers (C1) | in place, tested locally | C1, C4, C5 |
| Vulnerability management | Dependency audits, scans, penetration test? | SB05 (ADK runtime) is deferred until production | deferred: production | SB05 |
| Secure development | Code review, CI gates, release and rollback? | Four goals verified locally; no CI gate, release or rollback record in the plan | gap: proposed goal for adk-release-engineering | docs/plans/hr-assistant.md |
| Incident response | How are incidents detected, reported and handled? | No incident process or owner recorded (gap). Clocks that apply: Quebec, notify the CAI and the person on a risk of serious injury and keep an incident register; PIPEDA, where it applies, as soon as feasible and a 24-month record of every breach; Alberta not in scope; Australia, an eligible data breach assessed within 30 days and notified as soon as practicable (all checked 2026-10-26); counsel: which entity notifies which commissioner; Southgate to tell Érable without undue delay (assumption: to be written into the contract) | gap: owner and contract flow-down | docs/plans/hr-assistant.md, regulatory-memo.md |
| Deletion | How is data deleted at end of contract or on request? | Logs expire at 60 days; request path, Cloud SQL contents and Southgate's copies are not recorded | in place for log expiry as designed; gap: the rest | D3 |
| Availability and recovery | What are the availability target and recovery plan? | gap: not recorded; a failure sends the request to the manager or HR (C1, C5) | gap | C1, C5 |
| AI security baseline | Which AI security code or standard do you follow? | n/a: not requested; no UK client | n/a | docs/discovery/hr-assistant.md §1 |
| Government security policy | Which government security policy does the system meet? | n/a: private client | n/a | docs/discovery/hr-assistant.md §1 |
| Certifications | Which certifications apply? | gap: Google Cloud's reports were not read; the application holds none | gap | D2 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Érable security lead (not named in the record) | this document | pending | pending |
| Me Geneviève Roy, counsel, Érable Logistics Inc. | this document | pending | pending |
