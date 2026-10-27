# governance-pack-nsw-agency-chatbot: what the fixture holds

Context unchanged. Standalone record for the NSW Trades Licensing Office (fictional NSW executive
agency); consultancy Southgate Labs in Sydney with a support engineer in Brisbane. Topic
`enquiries`.

| Fact | Where |
| --- | --- |
| Answers from published guidance; looks up a caller's application status | design R1, R2, C1-C3 |
| Gemini pinned; retirement 2027-02-26 (model page read 2026-10-20), about four months away | design D1 |
| Hosting australia-southeast1 | design D2 |
| Abuse monitoring location not recorded; Brisbane support access (outside NSW) | design D4, D5 |
| Transcripts kept 90 days | design D3 |
| ICTA contract, AI module, clause 6.11 model-change notice at the default (six months) | `docs/contract/order-form-summary.md`; design D6 |
| Value $420,000 including GST | order form summary |
| Accountable Official Ruth Abbott; privacy officer; CISO | brief §5 |

The retirement date (2027-02-26) falls inside a six-month notice window from now (A4). Expected
jurisdictions [au] with a seven-row screen; government form answers (AIAF) with form metadata;
counsel_required: yes. A6 needs a shell; credit naming `check_governance.py` and saying it was
not run.
