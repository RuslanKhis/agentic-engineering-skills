# governance-pack-auckland-singapore-retailer: what the fixture holds

Context unchanged. Standalone record for Kowhai Retail Limited (Auckland) and Kowhai Retail
(Singapore) Pte. Ltd.; consultancy Southgate Labs in Sydney. Topic `customer-agent`.

| Fact | Where |
| --- | --- |
| Answers order and returns questions; reads CRM order history | design R1, C1, D5; brief §3 |
| Issues store credit up to NZD 150 / SGD 130 | design R2, C2, C3 |
| Gemini, hosting and logs in australia-southeast1 for both countries | design D1, D2 |
| Sydney engineers read traces with CRM fields | design D4 |
| Transcripts kept 12 months and reused for evaluation | design D3; brief §3 |
| CRM data collected by Kowhai through shops and loyalty (indirect for the agent) | brief §3 |
| Old CRM addresses (accuracy before use) | plan M3: 27% older than 24 months |

Expected jurisdictions [au, nz, sg]; US, EU, UK, Canada out with reasons. Consultancy and Google
as s 11 agents (NZ) and data intermediaries (SG), as `counsel:`. Transfer annex with NZ and SG
rows for Sydney access and the Australian endpoint. A6 needs a shell; credit naming
`check_governance.py` and saying it was not run.
