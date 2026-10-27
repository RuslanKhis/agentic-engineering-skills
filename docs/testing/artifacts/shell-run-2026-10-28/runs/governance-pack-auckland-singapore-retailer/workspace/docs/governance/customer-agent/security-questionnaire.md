---
document: security-questionnaire
system: Kowhai Retail customer agent
version: build v0.6.1 (M1, M2)
status: draft
jurisdictions: [au, nz, sg]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: privacy officer (Aroha Ngata) and Data Protection Officer (Daniel Tan)
sources: docs/architecture/customer-agent.md, docs/plans/customer-agent.md
---

# Security questionnaire answer bank: Kowhai Retail customer agent

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into Kowhai Retail's vendor or security questionnaire. Each
answer states what holds for the build above, with its status: `in place`
(evidence recorded), `planned` (goal ID), `deferred` (trigger) or `n/a`
(reason). Planned is never written as in place. The design's security
baseline table lists only three rules (SB01, SB03, SB05); every other
baseline rule is answered `gap:` below, and the CISO's questions on them go
to the design owner.

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | Cloud Run, Firestore and logs in australia-southeast1 (Sydney) for both countries; Gemini endpoint in australia-southeast1; the model's processing region is not read (gap); Salesforce CRM region not recorded (gap) | in place by design decision, not re-verified; gap for the model and CRM | D1, D2, D5 |
| Overseas access | Who can access our data from outside our country, and under what transfer mechanism? | Three Southgate Labs engineers in Sydney read traces that include CRM fields during the pilot and a six-month support period; New Zealand: s 11 agent facts; Singapore: a contract naming the countries is needed; gap: no contract in the record | gap | D4, transfer-assessment.md |
| Identity and access | How are users authenticated and authorised? | Signed-in customers only; the CRM tool is scoped to the verified customer ID and refuses otherwise; /api routes built; the sign-in mechanism is not described in the design (gap) | in place, tested locally (routes, tool scope); gap (sign-in) | SB01, C1, G01/A2 |
| Encryption | Is data encrypted in transit and at rest? | gap: not recorded; Google Cloud defaults are not cited because the provider page was not read | gap | D2 |
| Secrets | How are credentials managed? | The Salesforce integration credential is built and proved by G02/A4 per the design; the integration user with the credit permission was granted 2026-09-30 | in place, tested locally | SB03, W1, G02/A4 |
| Logging and retention | What is logged, for how long, who can read it? | Traces include CRM fields returned by tools and are read by Southgate Labs engineers; transcripts kept 12 months; trace retention and log exclusions are not recorded; the baseline rule for logs is not in the design's table | gap | D3, D4 |
| Model provider data use | Is our data used to train models? Is it retained? | See privacy-impact-input-pack.md, Model provider data use; model page not read in this session | gap | D1, privacy-impact-input-pack.md |
| Sub-processors | Which third parties process our data? | Google Cloud, Southgate Labs and Salesforce; Google's sub-processor list not read; Salesforce role not recorded | gap | D1, D4, D5 |
| Prompt injection and agency | How is the agent prevented from taking unintended actions? | The credit tool checks eligibility and the limit in code and credits once per return; tested on 200 scripted conversations, with 0 credits above the limit or for ineligible returns; no adversarial prompt-injection result is recorded | in place, tested locally (code limits); gap (adversarial test) | C2, C3, M2 |
| Output handling | How is model output rendered safely? | gap: the baseline rule for output rendering is not in the design's table | gap | docs/architecture/customer-agent.md Security baseline |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | gap: no screening evidence for prompts, logs, traces or free text; proposed goal for protect-adk-sensitive-data | gap | C1, D4 |
| Abuse and cost limits | What limits runaway use? | Per-order credit limit and once-per-return key; no call cap, spend stop or rate limit recorded | in place for credit; gap for rate and spend | C2, C3 |
| Human oversight | Who reviews or approves outputs and actions? | No approval before a credit; handover to a person on request to the queue in the customer's country, callback form otherwise | in place, tested locally (handover); gap (approval) | C4, G03/A1 |
| Vulnerability management | Dependency audits, scans, penetration test? | ADK runtime hardening is deferred to production; no scan or penetration test is recorded | deferred: production | SB05 |
| Secure development | Code review, CI gates, release and rollback? | gap: not recorded; plan state is verified_local for G01 to G04 | gap | G04 |
| Incident response | How are incidents detected, reported and handled? | No incident has occurred in the plan's records and no incident process is recorded (gap). Clocks: Southgate Labs to Kowhai without undue delay by contract (gap: no term); New Zealand: the Commissioner as soon as practicable once serious harm is reasonably believed (the OPC asks for 72 hours), agents must tell Kowhai of all breaches; Singapore: data intermediary to client without undue delay, client assesses within 30 calendar days and notifies the PDPC within 3 calendar days of determining a breach notifiable; Australia (consultancy's own handling only): eligible data breach assessed within 30 days and notified as soon as practicable; which entity notifies is counsel (source: adk-governance-pack reference system-card-and-questionnaire.md, read 2026-10-26; checked 2026-10-26) | gap (process); clocks stated | D4; counsel |
| Deletion | How is data deleted at end of contract or on request? | Transcripts kept 12 months; erasure path for transcripts, traces, evaluation sets and provider stores not recorded; the six-month support period ends access (D4) | gap | D3, D4 |
| Availability and recovery | What are the availability target and recovery plan? | gap: not recorded | gap | D2 |
| AI security baseline | Which AI security code or standard do you follow? | n/a: not requested (no UK client); IMDA Agentic MGF mapping is in impact-assessment.md | n/a | impact-assessment.md |
| Government security policy | Which government security policy does the system meet? | n/a: private client | n/a | docs/discovery/customer-agent.md §1 |
| Certifications | Which certifications apply? | Hosted on Google Cloud; its reports were not read in this session, so none is cited; the application holds none (gap for the client's vendor-risk team) | gap | D2 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy officer, Kowhai Retail Limited (Aroha Ngata) | This document | pending | pending |
| Data Protection Officer, Kowhai Retail (Singapore) Pte. Ltd. (Daniel Tan) | This document | pending | pending |
