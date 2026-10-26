---
document: transfer-assessment
system: <system name>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk, nz, sg, ca; must include eu, uk, nz, sg or ca>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <the reviewer who relies on it: counsel, DPO or privacy officer, CISO, risk owner>
exporter: <client legal entity per transfer; for a group, each exporting entity, or counsel: who exports>
sources: <docs/architecture/<topic>.md, privacy-impact-input-pack.md>
---

# Transfer assessment annex: <system name>

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Facts for the transfer assessments the exporter completes for each transfer
the jurisdiction screen found: the transfer impact assessment (EU, EDPB
Recommendations 01/2020); the data protection test (UK GDPR Articles 44A to
47A; the ICO still calls the record a TRA); the s 11 agent facts and, for a
disclosure, the IPP 12 ground (New Zealand); the Transfer Limitation
Obligation (Singapore); the s 17 assessment before personal information
leaves Quebec, and Alberta's service-provider country list (Canada). The
conclusion that the protection is adequate, comparable or not materially
lower is counsel's. Not legal advice.

<!-- Keep only the regime sections, and the rows, whose code is in
jurisdictions, and list the same codes as the pack's other drafts (au
included when the consultancy brings it in). Australian APP 8 and NSW
s 19(2) facts stay in the privacy impact input pack. Delete this comment. -->

## Transfers

| Transfer | From (regime) | To (recipient, country) | Data categories and volume | Access mode | Mechanism | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| <consultancy access from Australia> | <EU / UK / New Zealand / Singapore / Quebec> | <agency, Australia> | <categories; approximate volume> | <remote access to logs, traces, evaluation sets, support tickets> | <SCC Module 2 / IDTA / Addendum / s 11 agent contract / contract specifying the countries / s 17 written agreement; counsel:> | <D ID or gap:> |
| <group company: a subsidiary's data in the parent's systems in another country> | <the subsidiary's regime> | <parent, country> | <categories> | <shared system of record> | <contract or binding corporate rules; counsel: who exports> | <D ID or gap:> |
| <model endpoint or telemetry outside the region> | <EU / UK / New Zealand / Singapore / Quebec> | <provider, country> | <categories> | <API call, storage> | <adequacy, DPF or UK Extension with check date, SCCs, contract or certification; counsel:> | <D ID, source:> |

## Destination and access facts

- <laws and practices of the destination country that bear on the assessment, as counsel will need them> (counsel: <question>).
- <onward transfers and sub-processors> (<D IDs, source:>).
- <who at the recipient can access the data, from where, and why> (<D/SB IDs>).

## Supplementary measures

| Measure | Status | Evidence |
| --- | --- | --- |
| <pseudonymised evaluation sets; EU- or UK-only log access; encryption with client-held keys> | <in place / planned G ID / gap:> | <C/SB IDs> |

## New Zealand: s 11 agents and IPP 12

| Offshore party | Country | Holds only for the client (s 11)? | Any own-purpose use (abuse monitoring, service improvement, training) | If a disclosure: IPP 12(1) ground proposed | Evidence |
| --- | --- | --- | --- | --- | --- |
| <consultancy; Google model endpoint> | <Australia; processing region> | <yes / no; contract reference> | <none / what; counsel:> | <n/a: agent only / ground; counsel:> | <D ID, source:> |

- **Public sector client:** <jurisdictional risk assessment inputs: hosting region, model processing region, provider jurisdiction, foreign-law access, consultancy access from Sydney; data classification against the RESTRICTED ceiling; or n/a: private client> (<D IDs; agency:>).

## Singapore: Transfer Limitation Obligation

| Transfer | Recipient role (organisation or data intermediary) | Legally enforceable obligation or specified certification | Contract clause naming the countries | Deemed satisfaction relied on | Evidence |
| --- | --- | --- | --- | --- | --- |
| <consultancy access from Australia> | <data intermediary> | <contract; Global or APEC CBPR or PRP with its check date; counsel:> | <clause reference or gap:> | <none / which> | <D ID or gap:> |

- **The client's responsibility:** <the client, as the transferring organisation, covers transfers its data intermediaries make> (<contract reference or gap:>; counsel: <is the Privacy Act 1988 "any law" binding the consultancy to a comparable standard, or is a contract needed>).

## Canada: Quebec s 17 and Alberta service providers

| Flow leaving Quebec, or Alberta data to a provider outside Canada | Destination | Sensitivity and purpose | Contractual measures | Destination's legal framework | Written agreement (Quebec) or country list entry (Alberta) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| <model endpoint in Ontario, the US or elsewhere; logs; consultancy access from Sydney> | <region, country> | <facts> | <terms> | <counsel:> | <reference or gap:> | <D ID, source:> |

- **Result of the s 17 assessment:** counsel: <does the information receive adequate protection; if not, the enterprise refuses to communicate it or entrust it>.

## Questions for counsel

- counsel: <is the access a restricted transfer, who is the exporter, which module or tool applies, is the test met; for New Zealand, agent or foreign recipient; for Singapore, which mechanism; for Quebec, adequate protection>, needed by <goal or wait ID>.

## Review and sign-off

<!-- Only the reviewer fills Decision and Date. Leave both `pending` while
status is draft; the reviewer sets status: reviewed when they sign. One row
per reviewer: the role from `for:` first, then any other reviewer. -->

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| <the reviewer named in for:> | <this document, or the sections reviewed> | pending | pending |
