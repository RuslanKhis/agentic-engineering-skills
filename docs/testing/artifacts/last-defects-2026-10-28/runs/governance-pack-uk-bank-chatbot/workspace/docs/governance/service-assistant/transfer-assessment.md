---
document: transfer-assessment
system: Thamesbridge customer service assistant
status: draft
jurisdictions: [au, eu, uk]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: UK DPO (Oliver Grant) and Ireland DPO (Siobhán Kelly)
exporter: Thamesbridge Bank plc for UK customers' data; Thamesbridge Bank Ireland DAC for Irish and EU customers' data; counsel: confirm who exports for each transfer
sources: docs/architecture/service-assistant.md, docs/governance/service-assistant/privacy-impact-input-pack.md
---

# Transfer assessment annex: Thamesbridge customer service assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Facts for the transfer assessments the exporters complete: the transfer impact assessment (EU, EDPB Recommendations 01/2020) and the data protection test (UK GDPR Articles 44A to 47A). The conclusion that protection is adequate or not materially lower is counsel's. Australian APP 8 facts stay in the input pack. Not legal advice.

## Transfers

| Transfer | From (regime) | To (recipient, country) | Data categories and volume | Access mode | Mechanism | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Southgate Labs access from Sydney, UK data | UK | Southgate Labs, Australia | Logs, traces and pseudonymised transcripts of up to 5,000 UK pilot customers over 8 weeks, with support for six months | Remote access by four engineers | IDTA or Addendum plus the data protection test; no UK adequacy regulations for Australia (checked 2026-10-26); gap: not executed (W4); counsel: | D4, docs/discovery/service-assistant.md §5, §6 |
| Southgate Labs access from Sydney, EU data | EU | Southgate Labs, Australia | As above for up to 1,000 Irish and EU pilot customers | Remote access by four engineers | SCCs (Decision (EU) 2021/914) with a transfer impact assessment; module counsel: (controller to processor, or processor to sub-processor if a group company contracts); gap: not executed (W4) | D4, docs/discovery/service-assistant.md §6 |
| Irish and EU customers' data held in UK systems of the group (core banking, CreditLens) | EU | Thamesbridge Bank plc, United Kingdom | Account and decision data for Irish and EU customers | gap: location of core banking, card platform and CreditLens for Irish customers not recorded | EU adequacy decision for the UK, renewed 19 December 2025, read via a search extract of the Commission page (checked 2026-10-26); counsel: confirm applicability and which entity exports | D3, docs/discovery/service-assistant.md §1 |
| UK data to Belgium hosting | UK | Google Cloud, Belgium | Chat, logs and traces of UK customers if any is routed to europe-west1 | gap: D2 says UK traffic stays in London; none expected | UK adequacy regulations cover the EEA (checked 2026-10-26); n/a if no UK data is routed to Belgium | D2 |
| Model endpoint, caching, abuse monitoring and Google support | UK and EU | Google Cloud, country of the model's processing gap | Prompts and outputs including balances, transactions and reason codes | API calls; abuse-monitoring storage; support access | gap: processing region and Google sub-processor locations not read; Google Cloud Data Processing Addendum transfer terms (source: adk-governance-pack reference, read 2026-10-25); counsel: | D1, D2 |

## Destination and access facts

- Australia has no UK or EU adequacy decision, so the Sydney access needs an instrument and a documented assessment (source: adk-governance-pack reference, read 2026-10-26; checked 2026-10-26).
- counsel: the laws and practices of Australia that bear on the assessment, including government access powers over data held by the consultancy (D4).
- Onward transfers and sub-processors: gap: Southgate Labs' own tools, ticketing and chat used for support are not recorded; Google sub-processors list not read (D4, D1).
- Who can access: four Southgate Labs engineers in Sydney, for six months, to logs, traces and pseudonymised transcripts; Thamesbridge's own access and the engineers' device and network controls are gap: not recorded (D4, SB05).
- gap: whether engineers can download or copy data out of the Thamesbridge environment; proposed goal for adk-agent-security.

## Supplementary measures

| Measure | Status | Evidence |
| --- | --- | --- |
| Pseudonymised transcripts for engineer access | in place for transcripts, tested locally; coverage unmeasured; gap: logs and traces | C5, G04/A1 |
| Logs and traces held in the traffic's own region | decided, not evidenced; gap: configuration proof | D2 |
| Access only through a bank-controlled environment with no export, per-engineer logging and time-limited approval | gap: not recorded; proposed goals for adk-agent-security and adk-agent-observability | D4 |
| Masking of merchant names and free-text special categories before logging | gap: proposed goal for protect-adk-sensitive-data | docs/discovery/service-assistant.md §3 |
| Stop engineer access to production data at pilot end unless extended | gap: proposed decision for the sponsor | D4 |

## Questions for counsel

- counsel: is the Sydney access a restricted transfer under UK GDPR and GDPR, who exports in each regime, which module or tool applies, and is the data protection test or transfer impact assessment met; needed before W4.
- counsel: does pseudonymisation change the analysis when logs and traces are not pseudonymised; needed before W4.
- counsel: is the EU to UK flow for Irish customers' data covered by adequacy and which entity exports; needed before W3.
- counsel: which Google processing locations and sub-processors create further transfers, once the model page is read; needed before W2.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| UK DPO (Oliver Grant) | UK transfers | pending | pending |
| Ireland DPO (Siobhán Kelly) | EU transfers | pending | pending |
