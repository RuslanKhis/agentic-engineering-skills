# Implementation plan: customer agent pilot

Status: in progress
Architecture: [docs/architecture/customer-agent.md](../architecture/customer-agent.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Own orders and returns answers | 1 | implementation | 5-7 | none | adk-tool-auth-and-secrets | verified_local |
| G02 Store credit within limits | 1 | implementation | 4-6 | G01 | safe-api-tool-calls | verified_local |
| G03 Handover by country | 1 | implementation | 2-3 | G01 | adk-workflow-design | verified_local |
| G04 Pilot journey | 1 | journey | 3-4 | G02, G03 | adk-agent-evaluation | verified_local |
| G05 Governance papers | 1 | governance | 5-7 | G04 | adk-governance-pack | ready |

## Calendar waits

- W1: Salesforce integration user with the credit permission, granted 2026-09-30.
- W2: Privacy officer (Aroha Ngata, Kowhai Retail Limited) reviews the G05 drafts and decides whether a New Zealand privacy impact assessment is required; duration assumption: 10 working days from the day the drafts are sent; needed by 2026-11-26. Blocks the pilot decision (no pilot-approval goal exists in this plan yet; gap).
- W3: Singapore Data Protection Officer (Daniel Tan, Kowhai Retail (Singapore) Pte. Ltd.) reviews the G05 drafts, decides on a DPIA and the PDPA assessments for the purposes listed in the input pack; duration assumption: 10 working days from the day the drafts are sent; needed by 2026-11-26. Blocks the pilot decision (same gap).
- W4: Counsel review of the questions in `docs/governance/customer-agent/regulatory-memo.md`; counsel for Kowhai Retail is not named in the record (gap), so Mere Walker names counsel; duration unknown; needed by 2026-11-26. Blocks the pilot decision (same gap).

## Measurement records

- M1: metric correct order status answers; value 93%; window 2026-10-06 to 2026-10-17; sample 300 test chats; method comparison with CRM; owner Southgate Labs; build v0.6.1
- M2: metric credits above the limit or for ineligible returns; value 0; window 2026-10-06 to 2026-10-17; sample 200 scripted conversations; method scripted tests; owner Southgate Labs; build v0.6.1
- M3: metric CRM addresses older than 24 months among test customers; value 27%; window 2026-10-06 to 2026-10-17; sample 300; method CRM export; owner Kowhai customer data team; build n/a

## Evidence

- G05: drafted, not sent. Documents in `docs/governance/customer-agent/`: regulatory-memo, privacy-impact-input-pack, transfer-assessment, impact-assessment, system-card, security-questionnaire. Regimes in scope: au (consultancy handling only), nz, sg. Waits W2 to W4 are requested the day the drafts are sent to the reviewers.

## Resume here

Next: G05 Governance papers.
