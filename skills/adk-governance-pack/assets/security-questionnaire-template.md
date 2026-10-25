---
document: security-questionnaire
system: <system name>
version: <build the answers describe>
status: draft
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
sources: <docs/architecture/<topic>.md (contracts, SB table), docs/plans/<topic>.md>
---

# Security questionnaire answer bank: <system name>

Answers to paste into <client>'s vendor or security questionnaire. Each answer
states what holds for the build above, with its status: `in place` (evidence
recorded), `planned` (goal ID), `deferred` (trigger) or `n/a` (reason).
Planned is never written as in place. Cite only the SB rules the
design's table lists; a baseline rule the design omits is answered `gap:`
or `n/a:` with its ID.

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | <services and regions> | <status> | <D IDs> |
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
| Incident response | How are incidents detected, reported and handled? | <alerts, owner, notification window> | <status> | <D/G IDs, I IDs> |
| Deletion | How is data deleted at end of contract or on request? | <erasure path and period> | <status> | <C/D IDs> |
| Availability and recovery | What are the availability target and recovery plan? | <SLO, backup, restore test> | <status> | <C/D IDs> |
| Certifications | Which certifications apply? | <the cloud provider's, cited; the application's own, if any> | <status> | <source:> |
