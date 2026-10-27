---
document: transfer-assessment
system: Shortlisting assistant (Kestrel Logistics)
status: draft
jurisdictions: [au, eu]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Anouk de Vries, counsel, Kestrel Logistics
exporter: counsel: Kestrel Logistics B.V. or Kestrel Logistik GmbH, or each for its own applicants
sources: docs/architecture/shortlisting.md, privacy-impact-input-pack.md
---

# Transfer assessment annex: Shortlisting assistant (Kestrel Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Facts for the transfer impact assessment Kestrel completes (EDPB
Recommendations 01/2020) for each transfer found by the jurisdiction screen.
The conclusion that protection is essentially equivalent is counsel's. Australian
APP 8 facts stay in privacy-impact-input-pack.md. Not legal advice.

## Transfers

| Transfer | From (regime) | To (recipient, country) | Data categories and volume | Access mode | Mechanism | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Southgate Labs access from Sydney | EU | Southgate Labs, Australia | Prompt and response logs (CV text) and the 1,400-application evaluation set; volume of logs gap | Remote read access during the pilot and six weeks after | No adequacy decision for Australia (source: adk-governance-pack reference privacy-and-records.md, read 2026-10-26); counsel: SCC Module 2 (Decision (EU) 2021/914) and a transfer impact assessment; gap: none recorded (W4) | D5, D6 |
| Model endpoint | EU | Google, region gap | Redacted CV text and vacancy requirements | API call | counsel: none needed if processing stays in the EU; gap: the model's processing region and any abuse-monitoring storage were not read from the provider's page | D2 |
| Group company data in shared systems | EU | Kestrel Logistik GmbH, Germany, with Kestrel Logistics B.V., Netherlands | Applicants in Germany processed in a project of the Dutch entity | Shared project `kestrel-talent-pilot` | n/a: both inside the EU; counsel: who is exporter and controller | D3, docs/discovery/shortlisting.md §1 |

## Destination and access facts

- Laws and practices of Australia that bear on the assessment, for counsel: counsel: which Australian law could compel access to data Southgate staff read from Sydney, and whether the Privacy Act binds Southgate to a comparable standard (source: adk-governance-pack reference australia.md, checked 2026-10-26).
- Onward transfers and sub-processors: Google Cloud as the hosting and model provider (D2, D3); gap: Google's sub-processor list was not read (no network access).
- Who can access, from where, and why: two Southgate engineers in Sydney, for debugging and evaluation; the brief names the engineers (docs/discovery/shortlisting.md §6, D5). gap: access is per named person or per team, and whether staff access is logged.

## Supplementary measures

| Measure | Status | Evidence |
| --- | --- | --- |
| Evaluation set pseudonymised by removing names and contact details | in place as a design decision; counsel: pseudonymised, not anonymous, data remains personal data (D6) | D6 |
| Logs kept 14 days only | in place as a retention period; gap: enforcement evidence | D4 |
| Dates of birth, photos, nationality and marital status removed before the model, so they are absent from model-bound logs | in place, tested locally (C4); gap: the evaluation set is built from exports that may still carry them, since D6 removes names and contact details only | C4, D6 |
| EU-only access to logs, or access through a Kestrel-controlled jump host with logging | gap: not planned; proposed goal for adk-agent-security | D5 |
| Reading the evaluation set inside Kestrel's project without copying out | gap: not recorded | D3, D5 |

## Questions for counsel

- counsel: is Sydney read access a restricted transfer, who is the exporter, which SCC module applies, and is the transfer impact assessment met; needed before W4.
- counsel: may Southgate's access to live applicant data wait until W4 is complete, with access in the pilot limited to synthetic or redacted data meanwhile; needed before W2.
- counsel: does Google's processing for the pinned model stay in the EU, and is abuse-monitoring storage or review by people acceptable; needed before W2.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Anouk de Vries, counsel | This document | pending | pending |
| Matthias Brandt, DPO | Facts and supplementary measures | pending | pending |
