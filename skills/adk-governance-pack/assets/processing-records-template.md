---
document: processing-records
system: <system name>
status: draft
jurisdictions: [<codes in scope; must include eu or uk>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <the reviewer who relies on it: counsel, DPO or privacy officer, CISO, risk owner>
role: <the client is controller; the agency is processor during the build / not processing>
sources: <docs/architecture/<topic>.md, privacy-impact-input-pack.md>
---

# Records of processing rows: <system name>

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Rows for <client>'s existing register under GDPR Article 30(1) or UK GDPR
Article 30(1), as the jurisdiction screen found them in scope; the DPO
merges them. One row per purpose, not per component. Not legal advice.
Australia has no Article 30 register: for Australian personal information
the privacy impact input pack's "Australia: Inventory and notice inputs"
section does this job and feeds the APP privacy policy and collection notice.

## Processing activities

| Regime | Activity and purpose | Data subjects | Personal data categories | Recipients and processors | Third-country transfers and safeguard | Automated decision with legal or similar effect, and its safeguards | Erasure time limit | Security measures | Legal basis | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <EU GDPR / UK GDPR> | <purpose in the client's words> | <who> | <categories; special categories flagged> | <processor and region> | <none / country and mechanism (adequacy, DPF, SCC module, IDTA or Addendum) with transfer-assessment.md, counsel:> | <no / yes, safeguards reference> | <period, from which design decision> | <SB and C IDs, one phrase each> | counsel: <basis to confirm; AI Act Art 4a reasons if special categories are used for bias detection> | <C/D IDs> |

## Processor record (Article 30(2), only while the agency processes personal data for the client)

| Processor | Controller | Categories of processing | Transfers | Security measures | Evidence |
| --- | --- | --- | --- | --- | --- |
| <agency> | <client> | <build, test, support> | <none / where staff access from, mechanism> | <SB IDs> | <D ID or contract reference> |

## Review and sign-off

<!-- Only the reviewer fills Decision and Date. Leave both `pending` while
status is draft; the reviewer sets status: reviewed when they sign. One row
per reviewer: the role from `for:` first, then any other reviewer. -->

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| <the reviewer named in for:> | <this document, or the sections reviewed> | pending | pending |
