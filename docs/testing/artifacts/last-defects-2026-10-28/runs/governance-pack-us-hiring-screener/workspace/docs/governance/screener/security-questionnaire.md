---
document: security-questionnaire
system: applicant screener (build v0.5.2)
version: build v0.5.2
status: draft
jurisdictions: [au, us]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Monica Alvarez, General Counsel, Redwood Freight Inc.
sources: docs/architecture/screener.md, docs/plans/screener.md
---

# Security questionnaire answer bank: applicant screener

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into Redwood's vendor or security questionnaire. Each answer states what holds for build v0.5.2, with its status: `in place` (evidence recorded; all evidence so far is local), `planned`, `deferred` or `n/a`. The design's security baseline lists only SB01, SB03 and SB05; every other baseline rule is answered `gap:`.

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | Cloud Run in us-west1 (Oregon), BigQuery for scores, Gemini on Vertex AI in us-west1; model processing region and BigQuery region gap: not read from the provider page | in place for the stack choice; gap: regions | docs/architecture/screener.md Scope gate, D1, D2 |
| Overseas access | Who can access our data from outside our country? | Two Southgate Labs engineers in Sydney read the evaluation set of real past applications and logs during the build and a three-month support period; Australian APP 8 and s 16C facts are in privacy-impact-input-pack.md; no US transfer mechanism applies on the record; contract gap: not in the record | in place as a fact; gap: contract and access controls | D4, D5 |
| Identity and access | How are users authenticated and authorised? | Recruiters use Greenhouse; the screener holds a custom-field-only API scope and cannot change stages; user sign-in for the screener's own API routes is covered by /api route protection tested locally; other baseline rules gap: not in the design's table | in place, tested locally | SB01, C2, G03/A1 |
| Encryption | Is data encrypted in transit and at rest? | gap: provider default not read and no design decision recorded | gap | D1 |
| Secrets | How are credentials managed? | The Greenhouse API key is handled as a baseline item, tested locally; secret store and scanning gap: not recorded | in place, tested locally for the key; gap: store | SB03, G03/A2 |
| Logging and retention | What is logged, for how long, who can read it? | gap: log contents, sink, region, retention and readers are not recorded; Sydney engineers read logs (D4) | gap | D4 |
| Model provider data use | Is our data used to train models? Is it retained? | gap: see privacy-impact-input-pack.md Model provider data use; provider page not read | gap | D1 |
| Sub-processors | Which third parties process our data? | Google Cloud (Vertex AI, Cloud Run, BigQuery) and Greenhouse as the client's ATS; Southgate Labs as service provider; no further list recorded | in place as a list; gap: contracts | D1, D2, privacy-impact-input-pack.md Recipients and regions |
| Prompt injection and agency | How is the agent prevented from taking unintended actions? | The screener cannot change an application's stage (custom-field-only scope); applicant free text is untrusted input and no injection test is recorded | in place for write scope, tested locally; gap: injection testing; ADK runtime hardening deferred | C2, G03/A2, SB05 |
| Output handling | How is model output rendered safely? | Output is a score and structured evidence written to a Greenhouse field (output schema); rendering rule gap: not in the design's table | in place for schema, tested locally; gap: rendering | C1, G02/A1 |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | Age, date of birth, graduation years and photos are removed before scoring; an application that fails redaction is flagged; no measured detector coverage recorded for free-text sensitive data | in place, tested locally; gap: coverage figure | C4, G01/A2 |
| Abuse and cost limits | What limits runaway use? | gap: no rate or spend limit recorded | gap | docs/architecture/screener.md Scope gate |
| Human oversight | Who reviews or approves outputs and actions? | A recruiter makes every rejection; 6% of "not recommended" applications were opened before rejecting in the shadow trial (denominator gap:) | in place for write scope; oversight not enforced: gap | R4, C2, M4 |
| Vulnerability management | Dependency audits, scans, penetration test? | gap: none recorded | gap | docs/plans/screener.md |
| Secure development | Code review, CI gates, release and rollback? | gap: none recorded beyond local verification of G01 to G04 | gap | G01, G02, G03, G04 |
| Incident response | How are incidents detected, reported and handled? | gap: no owner, alert or contract term recorded. Clocks that apply: Southgate to Redwood without undue delay (contract term gap:); Australia: an eligible data breach is assessed within 30 days and notified as soon as practicable if Southgate is an APP entity (counsel: which entity notifies; checked 2026-10-26); US state breach-notification statutes are not covered by the skill reference (counsel); GLBA n/a: no financial institution | gap | docs/plans/screener.md; no incident records |
| Deletion | How is data deleted at end of contract or on request? | gap: no erasure path or period for the evaluation set, BigQuery, logs or the Greenhouse field | gap | D2, D4, D5 |
| Availability and recovery | What are the availability target and recovery plan? | gap: none recorded; pilot only | gap | docs/architecture/screener.md Scope gate |
| AI security baseline | Which AI security code or standard do you follow? | n/a: not requested by Redwood | n/a | docs/discovery/screener.md §1 |
| Government security policy | Which government security policy does the system meet? | n/a: private client | n/a | docs/discovery/screener.md §1 |
| Certifications | Which certifications apply? | gap: Google Cloud's reports not read from its compliance page; the application holds none | gap | D1 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Monica Alvarez, General Counsel, Redwood Freight | this document | pending | pending |
| Redwood CISO or security lead (not named in the record) | this document | pending | pending |
