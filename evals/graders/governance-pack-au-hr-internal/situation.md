# governance-pack-au-hr-internal: what the fixture holds

Context unchanged. Standalone record for Wattle & Co (Australian retailer, 4,800 staff in NSW,
VIC, QLD); consultancy Southgate Labs in Sydney. Topic `hr-assistant`.

| Fact | Where |
| --- | --- |
| Workday leave, roster and attendance reads | brief §3; design C1-C3 |
| Manager attendance summary before a performance conversation | design D6, R2, C5; brief §4 |
| Gemini pinned in australia-southeast1 | design D1 |
| Prompts logged 30 days | design D3 |
| Error bodies to a US-region Sentry project | design D4 |
| Sydney engineers read logs and Sentry | design D5 |
| Masking missed union and medical phrases | plan M2 (82%, misses listed); design C4 partially evidenced |
| Union (SDA) consultation under the enterprise agreement | brief §5 |
| Pilot in NSW stores | brief §6; design scope gate |

Not in the record (the agent should raise): the NSW Workplace Surveillance Act notice for prompt
logging (a wait), and union consultation as a wait (only the stakeholder fact is recorded).
Expected jurisdictions [au]; US out (data merely routed to a US tracker is an APP 8 fact), EU
and UK out. A6 needs a shell; credit naming `check_governance.py` and saying it was not run.
