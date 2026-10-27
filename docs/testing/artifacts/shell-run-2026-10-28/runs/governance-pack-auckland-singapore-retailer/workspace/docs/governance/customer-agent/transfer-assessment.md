---
document: transfer-assessment
system: Kowhai Retail customer agent
status: draft
jurisdictions: [au, nz, sg]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: privacy officer (Aroha Ngata) and Data Protection Officer (Daniel Tan)
exporter: Kowhai Retail Limited for New Zealand customers; Kowhai Retail (Singapore) Pte. Ltd. for Singapore customers; counsel: which entity exports where the New Zealand company's systems or staff handle Singapore data
sources: docs/architecture/customer-agent.md, privacy-impact-input-pack.md
---

# Transfer assessment annex: Kowhai Retail customer agent

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Facts for the transfer assessments the exporter completes for each transfer
the jurisdiction screen found: the s 11 agent facts and, for a disclosure,
the IPP 12 ground (New Zealand); and the Transfer Limitation Obligation
(Singapore). The conclusion that protection is comparable is counsel's.
Australian APP 8 facts stay in the privacy impact input pack. Not legal
advice.

## Transfers

| Transfer | From (regime) | To (recipient, country) | Data categories and volume | Access mode | Mechanism | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Hosting, Firestore transcripts and logs | New Zealand | Google Cloud, Sydney, Australia | Profile, orders, returns, transcripts; volume not recorded (gap) | Running service | s 11 agent contract; gap: Cloud agreement terms; counsel | D2, D3 |
| Hosting, Firestore transcripts and logs | Singapore | Google Cloud, Sydney, Australia | Same | Running service | Contract naming the countries or certification; gap; counsel | D2, D3 |
| Model endpoint | New Zealand | Google, Gemini in australia-southeast1; processing region unread (gap) | Prompt and CRM fields returned by tools | API call | s 11 agent contract; gap: abuse monitoring and caching terms; counsel | D1 |
| Model endpoint | Singapore | Google, Gemini in australia-southeast1; processing region unread (gap) | Same | API call | Contract naming the countries; gap; counsel | D1 |
| Consultancy access from Australia | New Zealand | Southgate Labs, Sydney, Australia | Traces that include CRM fields; evaluation sets | Remote reading of traces by three engineers | s 11 agent contract; gap: no written contract in the record; counsel | D4 |
| Consultancy access from Australia | Singapore | Southgate Labs, Sydney, Australia | Same | Same | Contract naming Australia; gap; counsel | D4 |
| Salesforce CRM | New Zealand and Singapore | Salesforce; region not recorded (gap) | Profile, orders, returns, ledger | API read and credit write | gap | D5, W1 |
| Singapore data in New Zealand head-office systems or service queue | Singapore | Kowhai Retail Limited, New Zealand; assumption: only if the Singapore queue or CRM is run from Auckland; not recorded | Handover context | Service queue | gap | C4 |

## Destination and access facts

- Australia: laws and practices bearing on the assessment (the Privacy Act 1988 as a possible "any law" binding the consultancy) are counsel's (counsel: question 2 in Questions for counsel).
- Onward transfers and sub-processors: Google's sub-processor list and any Salesforce hosting are not recorded (D1, D5; gap).
- Who can access: three Southgate Labs engineers in Sydney read traces during the pilot and a six-month support period, for support and troubleshooting (D4); gap: whether access is role-limited, logged or time-limited.
- New Zealand has prescribed no country or binding scheme and Singapore has no adequacy list, so Australia is not whitelisted for either (source: adk-governance-pack reference privacy-and-records.md, read 2026-10-26; checked 2026-10-26).

## Supplementary measures

| Measure | Status | Evidence |
| --- | --- | --- |
| Pseudonymised or masked evaluation sets and traces | gap: no screening evidence; proposed goal for protect-adk-sensitive-data | D3, D4 |
| Per-customer scope on the CRM tool | in place, tested locally | C1, G01/A2 |
| Region pinning to australia-southeast1 for hosting and endpoint | in place by design decision; not re-verified in this session | D1, D2 |
| Role-limited and logged engineer access to traces | gap: proposed goal for adk-agent-security | D4 |

## New Zealand: s 11 agents and IPP 12

| Offshore party | Country | Holds only for the client (s 11)? | Any own-purpose use (abuse monitoring, service improvement, training) | If a disclosure: IPP 12(1) ground proposed | Evidence |
| --- | --- | --- | --- | --- | --- |
| Southgate Labs | Australia | assumption: yes while it only builds, evaluates and supports Kowhai's agent; gap: contract reference | Evaluation sets reused for other clients would be own-purpose; gap: not recorded | n/a: agent only; counsel | D3, D4 |
| Google (Gemini endpoint, Cloud Run, Firestore, logs) | Australia, processing region unread | assumption: yes; gap: agreement terms | Abuse review of flagged prompts could be own-purpose (source: adk-governance-pack reference privacy-and-records.md, read 2026-10-25; not re-read); counsel | n/a: agent only; counsel | D1, D2 |

- **Public sector client:** n/a: private client (docs/discovery/customer-agent.md §1).

## Singapore: Transfer Limitation Obligation

| Transfer | Recipient role (organisation or data intermediary) | Legally enforceable obligation or specified certification | Contract clause naming the countries | Deemed satisfaction relied on | Evidence |
| --- | --- | --- | --- | --- | --- |
| Consultancy access from Australia | Data intermediary proposed | gap: no contract in the record; certification none known | gap | none | D4 |
| Hosting in Sydney | Data intermediary proposed (Google) | gap: Cloud agreement terms | gap | none | D2 |
| Model endpoint | Data intermediary proposed (Google); an organisation if prompts are used for Google's own model development, which the provider page says is not the case without permission (source: adk-governance-pack reference privacy-and-records.md, read 2026-10-25) | gap | gap | none | D1 |

- **The client's responsibility:** Kowhai Retail (Singapore) Pte. Ltd., as the transferring organisation, covers transfers its intermediaries make; contract reference gap; counsel: is the Privacy Act 1988 "any law" binding the consultancy to a comparable standard, or is a contract needed (D4; treat the contract as required until counsel says otherwise).

## Questions for counsel

- counsel: Is Sydney access by Southgate Labs an IPP 12 disclosure or an s 11 use, and does evaluation reuse change it; regime New Zealand; needed before W4.
- counsel: Which mechanism covers Singapore data in Sydney and does the contract name Australia; regime Singapore; needed before W3 and W4.
- counsel: Who exports where the New Zealand company supports the Singapore queue; facts at C4; needed before W4.
- counsel: Does Google's abuse monitoring or caching count as own-purpose use; facts at D1; needed before W4.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Privacy officer, Kowhai Retail Limited (Aroha Ngata) | New Zealand section | pending | pending |
| Data Protection Officer, Kowhai Retail (Singapore) Pte. Ltd. (Daniel Tan) | Singapore section | pending | pending |
