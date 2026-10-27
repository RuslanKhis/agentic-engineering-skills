---
document: security-questionnaire
system: Public enquiries assistant
version: build v0.7.0
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CISO (Nikhil Rao)
sources: docs/discovery/enquiries.md, docs/architecture/enquiries.md, docs/plans/enquiries.md, docs/contract/order-form-summary.md
---

# Security questionnaire answer bank: Public enquiries assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Answers to paste into the Office's security assessment (W2). Each answer states what holds for build v0.7.0, with its status: `in place` (evidence recorded; tested locally unless said), `planned` (goal ID), `deferred` (trigger) or `n/a` (reason). The design's baseline table lists only SB01, SB03 and SB05; every other baseline rule is answered `gap:` with its area. Nothing here is a statement about production.

## Answer bank

| Area | Typical question | Answer | Status | Evidence |
| --- | --- | --- | --- | --- |
| Hosting and region | Where is data stored and processed? | Cloud Run, Firestore and Cloud Logging in australia-southeast1, Sydney; model endpoint in australia-southeast1; gap: the model's processing region is not recorded | in place for hosting; gap for the model | D1, D2 |
| Overseas access | Who can access our data from outside our country, and under what mechanism? | Southgate support from Sydney and one engineer in Brisbane, with access to transcripts and logs; Brisbane is outside NSW; Google abuse monitoring location not recorded; counsel: NSW s 19(2) and the contract mechanism; agency: Order Form item 14 says Australia | gap | D4, D5, `docs/contract/order-form-summary.md` |
| Identity and access | How are users authenticated and authorised? | Callers are anonymous; status is returned only when application number and date of birth match; routes and the licensing credential are under SB01 and SB03; gap: staff access roles | in place, tested locally, for C2, C3, SB01, SB03; gap for staff | C2, C3, SB01, SB03 |
| Encryption | Is data encrypted in transit and at rest? | gap: not recorded; provider default has not been read; proposed check by adk-agent-security | gap | D2 |
| Secrets | How are credentials managed? | The licensing system credential is covered by SB03, evidenced locally | in place, tested locally | SB03 |
| Logging and retention | What is logged, for how long, who can read it? | Transcripts 90 days in Firestore, then deleted; gap: log content, retention and readers | in place for transcripts as designed; gap for logs | D3, D2 |
| Model provider data use | Is our data used to train models? Is it retained? | gap: not recorded; see privacy-impact-input-pack.md Model provider data use; abuse monitoring applies with default settings | gap | D1, D4 |
| Sub-processors | Which third parties process our data? | Google Cloud (hosting and model) | in place as contracted | `docs/contract/order-form-summary.md`, D1 |
| Prompt injection and agency | How is the agent prevented from taking unintended actions? | It has a read-only status tool and a handover tool and cannot change applications; the runtime baseline is SB05; gap: no adversarial results recorded | in place, tested locally, for the tool limits; gap for adversarial testing | C2, C4, SB05 |
| Output handling | How is model output rendered safely? | gap: SB10 is not in the design's baseline table | gap | docs/architecture/enquiries.md Security baseline |
| Sensitive data screening | How is personal data kept out of prompts, logs and replies? | gap: no screening of free text recorded; protect-adk-sensitive-data evidence absent | gap | D3 |
| Abuse and cost limits | What limits runaway use? | Three failed lookups block further lookups in a session (C3); gap: call caps, rate limits and spend stop | in place for lookups; gap otherwise | C3 |
| Human oversight | Who reviews or approves outputs and actions? | No review step; it takes no action beyond reading status and handing over | n/a: no approval point in the design | C4 |
| Vulnerability management | Dependency audits, scans, penetration test? | gap: not recorded | gap | docs/architecture/enquiries.md Security baseline |
| Secure development | Code review, CI gates, release and rollback? | gap: release and rollback not recorded; pinned model retiring 2027-02-26 needs a release path | gap | D1 |
| Incident response | How are incidents detected, reported and handled? | No incident process or record is in the plan. Clocks that apply to the Office: Part 6A, containment immediately, assessment within 30 days and the Privacy Commissioner notified immediately; cyber incidents to Cyber Security NSW within 24 hours of detection and classification; ICTA default asks the supplier for immediate notice then details within 48 hours (checked 2026-10-26, source: adk-governance-pack reference australia.md, read 2026-10-26); counsel: which entity notifies; gap: Southgate's incident procedure and contact | gap | W2, docs/architecture/enquiries.md Security baseline |
| Deletion | How is data deleted at end of contract or on request? | Transcripts deleted after 90 days (D3); gap: end-of-contract return or destruction, and request path; the contract ends 2027-09-14 | planned: the 90-day deletion is designed, not evidenced; gap otherwise | D3, `docs/contract/order-form-summary.md` |
| Availability and recovery | What are the availability target and recovery plan? | gap: not recorded; handover to the contact centre is the fallback (C4) | gap | C4 |
| AI security baseline | Which AI security code or standard do you follow? | n/a: not requested | n/a | docs/architecture/enquiries.md Security baseline |
| Government security policy | Which government security policy does the system meet? | NSW Cyber Security Policy 2026-2027, Essential Eight Maturity Level One baseline and the supplier clauses (checked 2026-10-26, source: adk-governance-pack reference australia.md, read 2026-10-26); gap: no Maturity Level One evidence for the delivered environment; agency: CISO assessment | gap | W2, SB01, SB03, SB05 |
| Certifications | Which certifications apply? | gap: Google Cloud's reports were not read for this draft; the application holds none | gap | D2 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CISO (Nikhil Rao) | this document | pending | pending |
