---
document: security-questionnaire
system: Thamesbridge customer service assistant
version: build v0.8.0
status: draft
jurisdictions: [au, eu, uk]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: group CISO (Rachel Adeyemi), with the UK DPO and the Ireland DPO
sources: docs/architecture/service-assistant.md, docs/plans/service-assistant.md
---

# Security questionnaire answer bank: Thamesbridge customer service assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into Thamesbridge's vendor or security questionnaire. Each answer states what holds for build v0.8.0, with its status: `in place` (evidence recorded, here at local test tier only), `planned` (goal ID), `deferred` (trigger) or `n/a` (reason). Planned is never written as in place. The design's security baseline table lists only SB01, SB03 and SB05; every other baseline rule is answered `gap:` and the CISO should read each gap as "no evidence recorded", not as "absent".

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | UK traffic in europe-west2 (London), Irish and EU traffic in europe-west1 (Belgium), with logs and traces in the traffic's region; gap: the model's processing region and the location of core banking, card platform and CreditLens for Irish customers | gap | D1, D2, D3 |
| Overseas access | Who can access our data from outside our country, and under what transfer mechanism? | Four Southgate Labs engineers in Sydney for six months, to logs, traces and pseudonymised transcripts; UK IDTA or Addendum and EU SCCs are required and not yet executed (W4); gap: engineer access controls and download restrictions | gap | D4, transfer-assessment.md, W4 |
| Identity and access | How are users authenticated and authorised? | The customer signs in to the app; tools use the verified customer ID and read only that customer's accounts; /api routes are covered by the build rule | in place, tested locally | C1, SB01, G01/A2 |
| Identity and access, engineers | How is staff access to production data controlled? | gap: no engineer identity, approval or logging control is recorded; SB02 and SB04 are not in the design's table | gap | D4 |
| Encryption | Is data encrypted in transit and at rest? | gap: provider defaults or customer-managed keys are not recorded; read the Google Cloud documentation (not read, no network access) | gap | D1 |
| Secrets | How are credentials managed? | Core banking and card platform credentials are covered by the build rule | in place, tested locally | SB03, G02/A3 |
| Logging and retention | What is logged, for how long, who can read it? | Logs and traces are held in the traffic's region and readable by Southgate Labs (D2, D4); gap: SB14 not in the design's table, content, redaction and retention not recorded | gap | D2, D4 |
| Model provider data use | Is our data used to train models? Is it retained? | See the input pack's Model provider data use (one home); configuration of caching, abuse monitoring and grounding is gap | gap | D1, privacy-impact-input-pack.md |
| Sub-processors | Which third parties process our data? | Google Cloud, Southgate Labs and CreditLens are known; gap: Google's sub-processor list and CreditLens hosting not read | gap | D1, D3, D4 |
| Prompt injection and agency | How is the agent prevented from taking unintended actions? | The only write is a card freeze, which needs an explicit confirmation bound to the card ID, with no unfreeze and no payments; gap: SB17 and SB18 not in the design's table and no adversarial suite results | in place for the freeze, tested locally (M2 0 of 300 unconfirmed); gap for injection | C2, D5, M2 |
| Output handling | How is model output rendered safely? | Overdraft explanations pass an output validator and a no-promise check, with a fixed message and handover on failure; gap: SB10 rendering rule not in the design's table | in place for content, tested locally; gap for rendering | C3, C4 |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | Transcripts are pseudonymised before engineers read them; gap: coverage not measured, merchant names and free text reach the model, logs and traces unscreened | in place for transcripts, tested locally; gap otherwise | C5, G04/A1 |
| Abuse and cost limits | What limits runaway use? | gap: SB19 and SB25 not in the design's table; no call cap, spend stop or rate limit is recorded | gap | docs/architecture/service-assistant.md |
| Human oversight | Who reviews or approves outputs and actions? | The customer confirms each freeze (C2); a failed explanation hands over to an agent (C3); gap: share handed over not measured | in place, tested locally | C2, C3 |
| Vulnerability management | Dependency audits, scans, penetration test? | gap: SB15, SB21 and SB24 not in the design's table; no scan or penetration test is recorded | gap | docs/architecture/service-assistant.md |
| Secure development | Code review, CI gates, release and rollback? | ADK runtime rule is evidenced locally; gap: release gates and the rollback unit are not recorded; proposed goal for adk-release-engineering | in place for runtime, tested locally; gap otherwise | SB05, G04/A2 |
| Incident response | How are incidents detected, reported and handled? | Clocks that apply: Southgate Labs tells the banks without undue delay (gap: contract term absent); UK GDPR and GDPR 72 hours to the Information Commission and the Irish supervisory authority (source: adk-governance-pack reference, read 2026-10-26); Australian eligible data breach assessed within 30 days and notified as soon as practicable, if the Privacy Act reaches the consultancy (counsel:); DORA major ICT incident reporting for the Irish bank (counsel: clock); NIS2 24 and 72 hours if in scope (counsel:); FCA, PRA and Central Bank of Ireland notices (counsel: not covered by the references); AI Act Article 73 n/a: not high-risk on the proposed classification; no incident records exist and no alerting or owner is recorded | gap | D4, regulatory-memo.md, docs/plans/service-assistant.md |
| Deletion | How is data deleted at end of contract or on request? | gap: no retention decision or erasure path for sessions, logs, traces, transcripts or Sydney copies; Southgate Labs' access ends after six months (D4) but destruction is not recorded | gap | D4, privacy-impact-input-pack.md |
| Availability and recovery | What are the availability target and recovery plan? | gap: no target, backup or restore test recorded; the pilot is 8 weeks and 6,000 customers | gap | docs/discovery/service-assistant.md §6 |
| AI security baseline | Which AI security code or standard do you follow? | n/a: not requested in the record; the DSIT Code of Practice mapping can be added if the CISO asks | n/a | docs/discovery/service-assistant.md §5 |
| Government security policy | Which government security policy does the system meet? | n/a: private client | n/a | docs/discovery/service-assistant.md §1 |
| Certifications | Which certifications apply? | gap: Google Cloud's reports were not read and are not recalled from memory; the application holds none | gap | D1 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Group CISO (Rachel Adeyemi) | this document | pending | pending |
| UK DPO (Oliver Grant) | Overseas access and Incident response rows | pending | pending |
| Ireland DPO (Siobhán Kelly) | Overseas access and Incident response rows | pending | pending |
