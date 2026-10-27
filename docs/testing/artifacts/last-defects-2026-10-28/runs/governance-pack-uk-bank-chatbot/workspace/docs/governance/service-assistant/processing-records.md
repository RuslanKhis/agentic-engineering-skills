---
document: processing-records
system: Thamesbridge customer service assistant
status: draft
jurisdictions: [eu, uk]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: UK DPO (Oliver Grant) and Ireland DPO (Siobhán Kelly)
role: the banks are controllers (Bank plc under UK GDPR, Bank Ireland DAC under GDPR); Southgate Labs is processor during build and support
sources: docs/architecture/service-assistant.md, docs/governance/service-assistant/privacy-impact-input-pack.md
---

# Records of processing rows: Thamesbridge customer service assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Rows for Thamesbridge's existing registers under GDPR Article 30(1) and UK GDPR Article 30(1), as the jurisdiction screen found them in scope; the DPOs merge them. One row per purpose, not per component. Each row is written once per regime; the DPOs enter it in their own register. Not legal advice. Australia has no Article 30 register: the input pack's inventory section does this job for the consultancy's own handling.

## Processing activities

| Regime | Activity and purpose | Data subjects | Personal data categories | Recipients and processors | Third-country transfers and safeguard | Automated decision with legal or similar effect, and its safeguards | Erasure time limit | Security measures | Legal basis | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UK GDPR | Answer balance and transaction questions for the signed-in customer | UK pilot customers (5,000) | Balances, transactions with merchant names (special categories flagged: health, religion, union payments), chat text | Google Cloud London; Southgate Labs, Sydney | Southgate Labs access from Australia: IDTA or Addendum and data protection test, gap: not executed (transfer-assessment.md, W4; counsel:) | No: the assistant makes no decision (R4) | gap: not recorded | Own-account scope (C1), SB01 | counsel: Article 6(1)(b) or (f); Article 9 condition | R1, C1, D2, docs/discovery/service-assistant.md §3 |
| GDPR | Answer balance and transaction questions for the signed-in customer | Irish and EU pilot customers (1,000) | As above | Google Cloud Belgium; Southgate Labs, Sydney | SCC module and transfer impact assessment, gap: not executed (transfer-assessment.md, W4; counsel: exporter) | No (R4) | gap: not recorded | C1, SB01 | counsel: Article 6(1)(b) or (f); Article 9 condition | R1, C1, D2 |
| UK GDPR | Freeze a card after the customer confirms | UK pilot customers | Card status, card ID, confirmation | Card platform; Google Cloud London | As above for support access | No: freeze needs explicit customer confirmation (C2) | gap: card platform retention not recorded | Confirmation bound to the card ID (C2), SB03 | counsel: Article 6(1)(b) | R2, C2, D5 |
| GDPR | Freeze a card after the customer confirms | Irish and EU pilot customers | As above | Card platform; Google Cloud Belgium | As above | No (C2) | gap: not recorded | C2, SB03 | counsel: Article 6(1)(b) | R2, C2, D5 |
| UK GDPR | Explain a declined overdraft from the decision engine's reason codes | UK pilot customers who applied | Overdraft decision, reason codes, application link | CreditLens; Google Cloud London | As above | The engine's decline may be solely automated and significant; the assistant only explains; Article 22C safeguards gap (D3, C3; counsel:) | gap: not recorded | Reason-code-only tool and validator (C3, C4) | counsel: Article 6(1)(b) or (f); Article 9 if special categories feed the engine | R3, C3, D3 |
| GDPR | Explain a declined overdraft from the decision engine's reason codes | Irish and EU pilot customers who applied | As above | CreditLens; Google Cloud Belgium | As above | Article 22 for the engine's decision, safeguards gap; the assistant only explains (D3; counsel:) | gap: not recorded | C3, C4 | counsel: Article 6(1)(b) or (f) | R3, C3, D3 |
| UK GDPR | Support the service from pseudonymised transcripts, logs and traces | UK pilot customers | Pseudonymised chat text; logs and traces (content gap) | Southgate Labs, Sydney | IDTA or Addendum, gap: not executed (W4; counsel:) | No | gap: not recorded | Pseudonymisation job (C5); gap: logs and traces not pseudonymised on the record | counsel: Article 6(1)(f) | C5, D4 |
| GDPR | Support the service from pseudonymised transcripts, logs and traces | Irish and EU pilot customers | As above | Southgate Labs, Sydney | SCCs, gap: not executed (W4; counsel:) | No | gap: not recorded | C5; gap: logs and traces | counsel: Article 6(1)(f) | C5, D4 |

## Processor record (Article 30(2), only while the agency processes personal data for the client)

| Processor | Controller | Categories of processing | Transfers | Security measures | Evidence |
| --- | --- | --- | --- | --- | --- |
| Southgate Labs | Thamesbridge Bank plc (UK) and Thamesbridge Bank Ireland DAC (EU) | Support: viewing logs, traces and pseudonymised transcripts for six months | Sydney, Australia; instruments not yet executed (W4) | SB05, C5; gap: engineer access controls and download restrictions | D4, SB05 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| UK DPO (Oliver Grant) | UK GDPR rows | pending | pending |
| Ireland DPO (Siobhán Kelly) | GDPR rows | pending | pending |
