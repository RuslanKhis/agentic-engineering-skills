---
document: security-questionnaire
system: <system name>
version: <build the answers describe>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <the reviewer who relies on it: counsel, DPO or privacy officer, CISO, risk owner>
sources: <docs/architecture/<topic>.md (contracts, SB table), docs/plans/<topic>.md>
---

# Security questionnaire answer bank: <system name>

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into <client>'s vendor or security questionnaire. Each answer
states what holds for the build above, with its status: `in place` (evidence
recorded), `planned` (goal ID), `deferred` (trigger) or `n/a` (reason).
Planned is never written as in place. Cite only the SB rules the
design's table lists; a baseline rule the design omits is answered `gap:`
or `n/a:` with its ID.

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | <services and regions; the model's processing region> | <status> | <D IDs> |
| Overseas access | Who can access our data from outside our country, and under what transfer mechanism? | <consultancy staff and their country; support and abuse review; SCCs, IDTA or APP 8 facts> | <status> | <D IDs, transfer-assessment.md or gap:> |
| Identity and access | How are users authenticated and authorised? | <sign-in, principal from token, per-user scope> | <status> | <SB02, SB03, SB04, C IDs> |
| Encryption | Is data encrypted in transit and at rest? | <provider default or CMEK> | <status> | <D ID, source:> |
| Secrets | How are credentials managed? | <Secret Manager, workload identity, scan> | <status> | <SB16, C IDs> |
| Logging and retention | What is logged, for how long, who can read it? | <what is excluded from logs> | <status> | <SB14, D IDs> |
| Model provider data use | Is our data used to train models? Is it retained? | <provider terms and configuration> | <status> | <D ID, source:> |
| Sub-processors | Which third parties process our data? | <list with regions> | <status> | <D IDs, source:> |
| Prompt injection and agency | How is the agent prevented from taking unintended actions? | <trifecta split, tool tiers, confirmation> | <status> | <SB17, SB18, C IDs> |
| Output handling | How is model output rendered safely? | <text or sanitised markdown> | <status> | <SB10> |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | <SDP or Model Armor placement> | <status> | <C IDs, protect-adk-sensitive-data evidence> |
| Abuse and cost limits | What limits runaway use? | <call caps, spend stop, rate limits> | <status> | <SB19, SB25, C IDs> |
| Human oversight | Who reviews or approves outputs and actions? | <approval points> | <status> | <SB18, C IDs> |
| Vulnerability management | Dependency audits, scans, penetration test? | <audits in CI, ZAP, pen test> | <status> | <SB15, SB21, SB24> |
| Secure development | Code review, CI gates, release and rollback? | <gates and rollback unit> | <status> | <D/G IDs> |
| Incident response | How are incidents detected, reported and handled? | <alerts, owner; notification clocks that apply in the regimes in scope: agency to client without undue delay; GDPR or UK GDPR 72 hours to the authority; Australian eligible data breach assessed within 30 days and notified as soon as practicable; APRA CPS 234 72 hours; GLBA Safeguards 30 days; NIS2 24 and 72 hours if the client is in scope; DORA major ICT incident reporting for EU financial entities (counsel: clock); CRA 24 and 72 hours if a product; AI Act Art 73 if high-risk> | <status> | <D/G IDs, I IDs> |
| Deletion | How is data deleted at end of contract or on request? | <erasure path and period> | <status> | <C/D IDs> |
| Availability and recovery | What are the availability target and recovery plan? | <SLO, backup, restore test> | <status> | <C/D IDs> |
| AI security baseline | Which AI security code or standard do you follow? | <for UK clients who ask: DSIT Code of Practice principles mapped to SB and C IDs; otherwise n/a: not requested> | <status> | <SB/C IDs> |
| Certifications | Which certifications apply? | <the cloud provider's, cited; the application's own, if any> | <status> | <source:> |

## Review and sign-off

<!-- Only the reviewer fills Decision and Date. Leave both `pending` while
status is draft; the reviewer sets status: reviewed when they sign. One row
per reviewer: the role from `for:` first, then any other reviewer. -->

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| <the reviewer named in for:> | <this document, or the sections reviewed> | pending | pending |
