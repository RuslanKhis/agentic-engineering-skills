---
document: processing-records
system: Shortlisting assistant (Kestrel Logistics)
status: draft
jurisdictions: [au, eu]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Matthias Brandt, DPO, Kestrel Logistics
role: Kestrel is controller (counsel: which entity); Southgate Labs is processor while it reads logs and the evaluation set (D5)
sources: docs/architecture/shortlisting.md, privacy-impact-input-pack.md
---

# Records of processing rows: Shortlisting assistant (Kestrel Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Rows for Kestrel's existing register under GDPR Article 30(1); the DPO merges
them. One row per purpose. Not legal advice. Australia has no Article 30
register: the privacy impact input pack's "Australia: Inventory and notice
inputs" section does this job for Southgate Labs' own handling.

## Processing activities

| Regime | Activity and purpose | Data subjects | Personal data categories | Recipients and processors | Third-country transfers and safeguard | Automated decision with legal or similar effect, and its safeguards | Erasure time limit | Security measures | Legal basis | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EU GDPR | Rank applicants for warehouse and driver vacancies and give cited rationales so a recruiter can shortlist | Applicants in the Netherlands, Germany, Poland and Romania | Name, contact details, work history, education, photos and dates of birth on some CVs (removed before the model), free text that may reveal age, nationality, health, family status (special categories flagged, counsel:) | Google Cloud, europe-west4; Southgate Labs, Sydney | Sydney access: none recorded, counsel: SCC Module 2 and transfer impact assessment (W4), see transfer-assessment.md | counsel: Article 22 applies; recruiter decides, no automatic rejection (D1, R4); review share not measured (gap) | gap: no retention decision for stores other than logs; logs 14 days (D4) | Read-only ATS credential, per-recruiter scope, redaction before the model, citation validator (C1, C3, C4, C2) | counsel: Article 6(1)(f) or (b) to confirm | D1, D4, D5, C1 |
| EU GDPR | Build the evaluation set and measure agreement and adverse impact by age band and gender before each pilot phase | Past applicants 2024 to 2026 (1,400) | Pseudonymised CV content and recruiter decisions; age band and gender as derived for M3 (source gap) | Southgate Labs, Sydney, read access | Sydney access: counsel: as above (W4) | n/a: evaluation only | gap: no retention decision | Names and contact details removed (D6) | counsel: basis and Article 6(4) compatibility; AI Act Article 4a reasons if any special category is used for bias detection, why strictly necessary: gap | D6, M3, C7 |
| EU GDPR | Debug the assistant using 14 days of prompt and response logs | Applicants whose CVs were ranked | CV text and rationales | Google Cloud (sink and region gap); Southgate Labs, Sydney | Sydney access: counsel (W4) | n/a: debugging only | 14 days (D4) | Traces keep no CV text (D4); gap: access controls on logs | counsel: Article 6(1)(f) to confirm | D4, D5 |

## Processor record (Article 30(2), only while the agency processes personal data for the client)

| Processor | Controller | Categories of processing | Transfers | Security measures | Evidence |
| --- | --- | --- | --- | --- | --- |
| Southgate Labs | Kestrel Logistics B.V. and Kestrel Logistik GmbH (counsel: which) | Read access to logs and the evaluation set for debugging, evaluation and support during the pilot and six weeks after | Access from Sydney, Australia; mechanism gap (W4) | gap: no security baseline row covers staff access; SB01 and SB03 cover routes and the ATS credential only | D5, SB01, SB03 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Matthias Brandt, DPO | This document | pending | pending |
| Anouk de Vries, counsel | Every counsel: item | pending | pending |
