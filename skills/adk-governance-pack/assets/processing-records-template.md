---
document: processing-records
system: <system name>
status: draft
jurisdictions: [<codes in scope; must include eu or uk>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
role: <the client is controller; the agency is processor during the build / not processing>
sources: <docs/architecture/<topic>.md, privacy-impact-input-pack.md>
---

# Records of processing rows: <system name>

Rows for <client>'s existing register under GDPR Article 30(1) or UK GDPR
Article 30(1), as the jurisdiction screen found them in scope; the DPO
merges them. One row per purpose, not per component. Not legal advice.
Australia has no Article 30 register: for Australian personal information
the privacy impact input pack's "Australia: Inventory and notice inputs"
section does this job and feeds the APP privacy policy and collection notice.

## Processing activities

| Regime | Activity and purpose | Data subjects | Personal data categories | Recipients and processors | Third-country transfers and safeguard | Solely automated significant decision | Erasure time limit | Security measures | Legal basis | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <EU GDPR / UK GDPR> | <purpose in the client's words> | <who> | <categories; special categories flagged> | <processor and region> | <none / country and mechanism (adequacy, DPF, SCC module, IDTA or Addendum) with transfer-assessment.md, counsel:> | <no / yes, safeguards reference> | <period, from which design decision> | <SB and C IDs, one phrase each> | counsel: <basis to confirm; AI Act Art 4a reasons if special categories are used for bias detection> | <C/D IDs> |

## Processor record (Article 30(2), only while the agency processes personal data for the client)

| Processor | Controller | Categories of processing | Transfers | Security measures | Evidence |
| --- | --- | --- | --- | --- | --- |
| <agency> | <client> | <build, test, support> | <none / where staff access from, mechanism> | <SB IDs> | <D ID or contract reference> |
