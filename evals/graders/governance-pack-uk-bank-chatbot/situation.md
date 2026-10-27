# governance-pack-uk-bank-chatbot: what the fixture holds

Context unchanged. Standalone record for Thamesbridge Bank plc (UK) and Thamesbridge Bank
Ireland DAC; consultancy Southgate Labs in Sydney. Topic `service-assistant`.

| Fact | Where |
| --- | --- |
| Reads balances and transactions | design R1, C1 |
| Freezes cards on confirmation | design R2, C2, D5 |
| Explains declined overdraft decisions from the decision engine's reason codes | design R3, C3, C4, D3 |
| Hosting London (europe-west2) and Belgium (europe-west1) | design D2 |
| Sydney support for six months with logs, traces, pseudonymised transcripts | design D4; C5 |
| Customers in the UK, Ireland and other EU countries | brief §1, §3 |
| Chat header says the customer is talking to the bank's assistant | design D6 |
| Waits W1 model risk review, W2 DPIA sign-off | plan |

Expected jurisdictions [au, eu, uk]; US out with a reason. Transfer annex rows for EU and UK
data accessed from Australia. counsel_required: yes (credit decision explanations). A5 needs a
shell for `check_governance.py`; credit naming it and saying it was not run.

Changed on 28 October 2026 (Phase 12): the check_governance.py assertion now carries the "reported as not run" escape in its own text, because Phase 11 judges failed it on the literal "runs" even where this note allowed naming the command.
