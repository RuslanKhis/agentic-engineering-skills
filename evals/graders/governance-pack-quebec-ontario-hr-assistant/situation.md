# governance-pack-quebec-ontario-hr-assistant: what the fixture holds

Context unchanged. Standalone record for Érable Logistics Inc. (CBCA company, head office
Montréal; centres in Montréal and Toronto; provincially regulated employer); consultancy
Southgate Labs in Sydney. Topic `hr-assistant`.

| Fact | Where |
| --- | --- |
| Answers HR policy questions in French and English | design R1, C1 |
| Auto-approves routine leave under two days with no human review | design R3, C3, C4, D5; plan M2 (64% of requests) |
| Hosting Toronto (northamerica-northeast2) | design D2 |
| Gemini processing in the United States (global endpoint) | design D1 |
| Sydney engineers read logs | design D4 |
| Prompts logged 60 days with employee IDs | design D3; brief §3 |
| Montréal unionised (collective agreement); Toronto not | brief §5 |
| Person in charge of the protection of personal information named | brief §5 |

Expected jurisdictions [au, ca] (Canada named "Canada", never "CA"); s 12.1 facts for the
auto-approval; s 3.3 PIA and s 17 rows for Toronto, US model processing and Sydney access;
Ontario electronic monitoring policy for logged prompts as a wait; counsel_required: yes. A6
needs a shell; credit naming `check_governance.py` and saying it was not run.
