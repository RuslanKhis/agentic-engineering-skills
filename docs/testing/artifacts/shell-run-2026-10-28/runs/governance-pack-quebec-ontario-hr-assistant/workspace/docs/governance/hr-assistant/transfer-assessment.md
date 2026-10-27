---
document: transfer-assessment
system: HR assistant (Érable Logistics)
status: draft
jurisdictions: [au, ca]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Me Geneviève Roy, counsel, Érable Logistics Inc.
exporter: Érable Logistics Inc. for each flow (counsel: confirm)
sources: docs/architecture/hr-assistant.md, docs/governance/hr-assistant/privacy-impact-input-pack.md
---

# Transfer assessment annex: HR assistant (Érable Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Facts for the s 17 assessment Érable completes before personal information of Quebec staff leaves Quebec, and for Alberta's service-provider country list where relevant (checked 2026-10-26). The conclusion that protection is adequate is counsel's (counsel: each row). Australian APP 8 facts stay in the privacy impact input pack. Not legal advice.

## Transfers

| Transfer | From (regime) | To (recipient, country) | Data categories and volume | Access mode | Mechanism | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Hosting: Cloud Run, Cloud SQL and logs | Quebec (Montréal staff) | Google Cloud, Toronto, Canada | prompts, answers, employee ID, leave details; 1,150 Montréal staff, pilot shift only (gap: pilot headcount) | service hosting; logs kept 60 days | s 17 assessment and written agreement; gap: Google Cloud agreement not in the record; counsel: adequate protection | D2, D3 |
| Model request to Gemini 3.5 Flash | Quebec | Google, United States | prompt text, including any leave reason typed; employee ID if included (gap: not recorded) | API call through the Vertex AI global endpoint | s 17 assessment and written agreement; gap: contract not in the record; counsel | D1 (page read 2026-09-10, not re-read) |
| Consultancy access from Sydney | Quebec | Southgate Labs, Australia | log content with employee IDs; same population | remote reading of logs during the pilot and a three-month support period | s 17 assessment and written agreement; gap: Southgate contract not in the record; counsel | D3, D4 |
| UKG HRIS read and write | Quebec | UKG, country not recorded | profile, balances, leave requests and decisions | integration user granted 2026-09-29 | gap: hosting location and contract not recorded; counsel | R2, W1 |

## Destination and access facts

- Destination law bearing on s 17: Canada (Ontario), the United States and Australia; counsel needs the laws and practices of each for the assessment, including foreign-authority access (counsel: the assessment of each destination's legal framework; the references do not state them).
- Onward transfers and sub-processors: Google's sub-processor list and the cloud data processing addendum are the places to read (source: adk-governance-pack reference privacy-and-records.md, read 2026-10-25, not re-read); gap: no record of sub-processors the project relies on.
- Who can access and why: two Sydney engineers on the project (docs/discovery/hr-assistant.md §5), to run and support the pilot (D4); gap: how they connect, from where, with which roles, and whether they can copy log content.
- Region note: a Toronto region is outside Quebec, so hosting itself triggers s 17 (checked 2026-10-26). Whether a Montréal region exists for the services used is reported; not confirmed at the source on 2026-10-26 (gap: owner of D2 to check; counsel: whether staying in Quebec would be preferred).

## Supplementary measures

| Measure | Status | Evidence |
| --- | --- | --- |
| Pseudonymise employee IDs in logs | gap: not designed; proposed goal for protect-adk-sensitive-data | D3 |
| Screen leave reasons before the model call | gap: no screening evidence recorded; proposed goal for protect-adk-sensitive-data | D1 |
| Restrict and audit Sydney log access, with no copying | gap: not recorded | D4 |
| Regional endpoint instead of global for the model | gap: design uses the global endpoint; proposed goal for adk-model-and-output-contracts | D1 |
| Per-user scoping of tool calls | in place, tested locally | C2 |

## Canada: Quebec s 17 and Alberta service providers

| Flow leaving Quebec, or Alberta data to a provider outside Canada | Destination | Sensitivity and purpose | Contractual measures | Destination's legal framework | Written agreement (Quebec) or country list entry (Alberta) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Hosting and logs | Toronto, Ontario | employment data, health details possible; run the service | gap: not in the record | counsel | gap: no written agreement recorded | D2 |
| Model processing | United States | same; extract dates and leave type | gap: not in the record | counsel | gap | D1 |
| Log access | Sydney, Australia | same; support | gap: not in the record | counsel | gap | D4 |
| Alberta data | n/a: no Alberta staff | n/a | n/a | n/a | n/a: no Alberta flow | docs/discovery/hr-assistant.md §1 |

- **Result of the s 17 assessment:** counsel: does the information receive adequate protection in each destination; if not, Érable refuses to communicate it or entrust it (checked 2026-10-26). No assessment exists yet (wait W4).

## Questions for counsel

- counsel: is the assessment of adequate protection met for Toronto, the United States and Australia, and what must the written agreement contain; regime Canada, Quebec; needed before the pilot, wait W4.
- counsel: is Google's cloud agreement the written agreement for hosting and model processing, and is a separate Southgate Labs contract needed for the Sydney access; regime Canada, Quebec; facts at D1, D2, D4.
- counsel: does the Toronto staff data held by a Quebec enterprise also need s 17 treatment; regime Canada; facts at D2.
- counsel: is Érable the exporter for each flow, and does Southgate's own access make it a recipient with duties of its own; regime Canada, Australia; facts at D4.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Me Geneviève Roy, counsel, Érable Logistics Inc. | this document | pending | pending |
