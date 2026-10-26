---
document: transfer-assessment
system: <system name>
status: draft
jurisdictions: [<codes in scope; must include eu or uk>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
exporter: <client legal entity, or counsel: who exports>
sources: <docs/architecture/<topic>.md, privacy-impact-input-pack.md>
---

# Transfer assessment annex: <system name>

Facts for the transfer impact assessment (EU, EDPB Recommendations 01/2020)
and the data protection test (UK GDPR Articles 44A to 47A; the ICO still
calls the record a TRA) that the exporter completes for each restricted
transfer. The conclusion that the protection is adequate, or not materially
lower, is counsel's. Not legal advice.

## Transfers

| Transfer | From (regime) | To (recipient, country) | Data categories and volume | Access mode | Mechanism | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| <consultancy access from Australia> | <EU / UK> | <agency, Australia> | <categories; approximate volume> | <remote access to logs, traces, evaluation sets, support tickets> | <SCC Module 2 / IDTA / Addendum; counsel:> | <D ID or gap:> |
| <model endpoint or telemetry outside the region> | <EU / UK> | <provider, country> | <categories> | <API call, storage> | <adequacy, DPF or UK Extension with check date, SCCs; counsel:> | <D ID, source:> |

## Destination and access facts

- <laws and practices of the destination country that bear on the assessment, as counsel will need them> (counsel: <question>).
- <onward transfers and sub-processors> (<D IDs, source:>).
- <who at the recipient can access the data, from where, and why> (<D/SB IDs>).

## Supplementary measures

| Measure | Status | Evidence |
| --- | --- | --- |
| <pseudonymised evaluation sets; EU- or UK-only log access; encryption with client-held keys> | <in place / planned G ID / gap:> | <C/SB IDs> |

## Questions for counsel

- counsel: <is the access a restricted transfer, who is the exporter, which module or tool applies, is the test met>, needed by <goal or wait ID>.
