---
document: privacy-impact-input-pack
system: HR assistant (Érable Logistics)
version: design accepted 2026-09-11, build v0.5.0
status: draft
jurisdictions: [au, ca]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
owner: Érable Logistics Inc. (organisation responsible for the information); Southgate Labs (consultancy, Sydney; legal entity name not recorded, gap)
for: Marie-Claude Gagnon, person in charge of the protection of personal information, Érable Logistics Inc.
sources: docs/discovery/hr-assistant.md, docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md
---

# Privacy impact input pack: HR assistant (Érable Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Inputs for Érable's Quebec privacy impact assessment (the EFVP) and for the Southgate Labs handling screened under Australian law (counsel: the person in charge and counsel decide what the EFVP concludes). Érable writes and signs the assessment; this pack supplies the facts the design and plan record and the questions only counsel can answer. Law as read from the skill's references on 2026-10-26 (checked 2026-10-26), not re-read at the source in this session.

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| Australia | OAIC threshold assessment: new or changed handling of personal information | yes | Sydney engineers read logs containing prompts and employee IDs (counsel: whether the Act reaches it) | D3, D4 |
| Canada | Quebec s 3.3 PIA for an information system project, and s 17 PIA before data leaves Quebec; OPC expects PIAs or AIAs for generative AI (checked 2026-10-26) | yes | New system handling Montréal employees' personal information, including possibly health details, with three flows outside Quebec | D1, D2, D4, docs/discovery/hr-assistant.md §3 |

Result: counsel: an assessment is required in Quebec under s 3.3 and s 17 (wait W3, wait W4); Australia recommended for the consultancy's handling; the person in charge decides.

## Processing description

- **Purpose:** answer HR policy questions and take and decide routine leave requests, to cut the median 31 hours from request to decision (R1, R2, R3; docs/discovery/hr-assistant.md §2).
- **Nature:** reads the employee profile from UKG, extracts dates and leave type with the model, applies a rule, and writes the decision to UKG; logs prompts and answers with the employee ID (C2, C3, C4, D3, D5).
- **Scope:** 1,150 Montréal and 640 Toronto staff, about 2,300 questions and 900 leave requests a month across HR today (docs/discovery/hr-assistant.md §1); the pilot is one shift per centre for 6 weeks (docs/discovery/hr-assistant.md §6). gap: staff on the pilot shifts.
- **Context:** an employment relationship, where staff cannot easily decline; the Montréal centre has a collective agreement in force and Toronto is non-unionised (docs/discovery/hr-assistant.md §5). gap: any prior employee notice.

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| User prompt and leave request | question text, leave dates, leave reason (may mention health or family matters) | employee | Cloud Run, northamerica-northeast2 (Toronto) | in logs, 60 days | gap: not recorded | gap: no screening evidence recorded | D2, D3, docs/discovery/hr-assistant.md §3 |
| Model request | prompt text including any reason the employee typed; employee ID not sent unless in the prompt (gap: not recorded) | Cloud Run | Gemini 3.5 Flash, Vertex AI global endpoint, processing in the United States | provider retention: see Model provider data use | n/a: not stored by the client | gap: none recorded | D1 |
| Tool call, UKG read | employee ID, site, role, manager, leave balances | agent | UKG HRIS (location not recorded, gap) | UKG's own retention (client system) | yes, in UKG | scoped to the verified employee ID | C2 |
| Tool call, UKG write | leave request, approver "HR assistant", decision | agent | UKG HRIS | UKG's own retention (client system) | yes, in UKG | rule in code before the write | C3, C4 |
| Logs and traces | prompts and answers with employee ID | Cloud Run | logs in northamerica-northeast2 (Toronto) | 60 days | gap: not recorded | gap: no redaction recorded | D2, D3 |
| Consultancy access | the log content above | Érable's Google Cloud environment (ownership not recorded, gap) | Southgate Labs engineers, Sydney, Australia | pilot plus three-month support | n/a: access, not storage | gap: access method, role scoping and copying rules not recorded | D4 |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| Montréal employees (1,150) | profile, balances, leave requests and reasons, chat prompts | leave reasons may disclose health or family circumstances; counsel: sensitivity under Quebec law | UKG, the employee, and the assistant (generated decision) | docs/discovery/hr-assistant.md §1, §3 |
| Toronto employees (640) | same | same; counsel: Ontario law applying | same | docs/discovery/hr-assistant.md §1, §3 |

## Automated decisions

- **Facts:** the rule approves a request when it is under two days, the balance covers it and no blackout date applies; the approval is written with approver "HR assistant" and no human review (C3, C4). The model only extracts dates and leave type (D5). Every other request goes to the manager's UKG queue (C5). The rule approves 64% of pilot-shape requests (M2, 500 replayed requests); dates and leave type were extracted correctly in 98.4% (M3). gap: share reviewed in the pilot, override rate and who could change an approved decision.
- **Explanation the design can produce:** the three C3 conditions; gap: no contract makes the assistant tell the employee which condition was met, nor offers correction of the personal information used.
- counsel: Quebec s 12.1: a decision made by the system alone, with notice, explanation and review for the Montréal staff; whether it covers an approval; Ontario staff per counsel. Australian APP 1.7 is n/a: no decision by Southgate Labs about a person.

## Necessity and proportionality

- Only the profile fields the rule needs (site, role, manager, leave balances) are read (docs/discovery/hr-assistant.md §3, C2); gap: whether the profile read is limited to those fields for the model's prompt.
- Less intrusive alternative: send every request to the manager, which is the pre-assistant process with a 31-hour median (docs/discovery/hr-assistant.md §2); a design that logs without the employee ID or with a pseudonym is not recorded (gap: log pseudonymisation; proposed goal for protect-adk-sensitive-data).
- Re-used datasets: n/a: no evaluation set from staff data is recorded; M2 replayed 500 July 2026 requests, so real requests were re-used (M2; gap: purpose, authority and storage of the replay set; counsel: compatible purpose).
- How people are informed and exercise rights: gap: no notice naming Google, the US processing and Sydney access; gap: no access, correction or erasure path for logs (counsel: Quebec access and correction rights reach logs held 60 days).

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| Prompt and answer logs | prompts and answers with employee ID | 60 days | gap: how a request reaches the logs before expiry | D3 |
| Cloud SQL | gap: contents not recorded in the design | gap: no retention decision | gap | D2 |
| UKG records | leave requests and decisions | client system, not decided here | n/a: client's HRIS | R2 |
| M2 replay set | 500 July 2026 requests | gap: not recorded | gap | M2 |

## Recipients and regions

| Recipient (service provider, in the regime's own word) | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| Google Cloud (Cloud Run, Cloud SQL, logs) | service provider under Érable's agreement (assumption: Érable is the customer; gap: contract not in the record) | Toronto, Ontario, Canada | outside Quebec: s 17 assessment and written agreement (transfer-assessment.md; counsel: adequate protection) | D2 |
| Google (Gemini through Vertex AI) | service provider | United States (model page read 2026-09-10, not re-read) | outside Quebec and outside Canada: s 17; foreign-access notice to staff (transfer-assessment.md; counsel) | D1 |
| Southgate Labs | service provider during build and support; APP entity in its own right in Australia (counsel: turnover and reach) | Sydney, Australia | outside Quebec and outside Canada: s 17 and a written agreement; APP 8 is n/a: Southgate reads data originating in Canada (transfer-assessment.md; counsel) | D4; gap: contract not in the record |
| UKG | system of record | gap: hosting country not recorded | gap: not covered by the design | R2 |

## Model provider data use

- Gemini 3.5 Flash is pinned as `gemini-3.5-flash-001` and called through the Vertex AI global endpoint; the model page listed US processing (D1, read 2026-09-10). gap: the model's retirement date was not recorded and could not be re-read; proposed goal for adk-model-and-output-contracts.
- Google states it does not use customer data to train or fine-tune models without permission or instruction; implicit caching is on by default and deleted within 24 hours; the global endpoint does not guarantee cached data stays in a location; prompts flagged by abuse classifiers can be stored up to 90 days in the project's region and reviewed by people (source: adk-governance-pack reference privacy-and-records.md, pages read 2026-10-25, not re-read). gap: the project's caching setting, abuse-monitoring status and whether Érable's agreement exempts it (counsel: the Google Cloud agreement terms).
- Whether Gemini was trained on personal data and what Érable relies on: counsel: a question for Google's published statements; no record (gap).

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| Wrong approval or routing of leave from a mis-extracted date or type (about 1.6% in replay) | assumption: low likelihood, moderate severity (pay, attendance) | rule in code before the UKG write; non-routine to the manager | in place, tested locally (C3, C5); no employee confirmation of extracted dates (gap) | C3, C5, M3 |
| Employee does not know the decision was made without a person | assumption: high likelihood, moderate severity | none designed | gap: s 12.1 notice and review route; proposed goal for adk-operational-guardrails | docs/discovery/hr-assistant.md §4 |
| Employee A reads or requests leave for employee B | assumption: low likelihood, high severity | tool scoped to the verified employee ID | in place, tested locally | C2, SB01 |
| Leave reasons (health, family) in prompts reach Gemini in the US and logs readable from Sydney | assumption: moderate likelihood, high severity | none recorded | gap: sensitive-data screening and log pseudonymisation; proposed goal for protect-adk-sensitive-data | D1, D3, D4 |
| Wrong policy answer given as HR's position | assumption: moderate likelihood, moderate severity | every answer cites the policy section; handover to HR | in place, tested locally; 92% cite the right section (M1), so 8% do not | C1, M1 |

## Australia: APP compliance check

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection (3.3 consent for sensitive information; generated or inferred information is collected) | n/a: Southgate collects nothing for itself; it reads logs Érable collected | counsel: whether reading log content is collection | D4 |
| APP 5 notice | n/a: no Australian individuals | n/a | D4 |
| APP 6 use and disclosure | Southgate reads logs to run the pilot and support | counsel: any use beyond support (evaluation, improvement) | D4 |
| APP 8 and s 16C overseas recipients | n/a: no onward disclosure from Australia recorded | gap: confirm no export of log content from Sydney | D4 |
| APP 10 quality; APP 11 security and destruction | Southgate holds no data on the record; gap: copies, tickets, laptops, retention after the support period | gap: Southgate's own handling and destruction rule | D4 |
| APP 12 and 13 access and correction | n/a: no Australian individuals | n/a | D4 |

- **PIA required?** Recommended, not required, for a private organisation (OAIC guidance, checked 2026-10-26; counsel: whether the Act reaches Southgate's handling).

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Canadian employees' prompts, employee IDs and leave details visible in logs | run, debug and support the pilot | Érable's logs | Southgate engineers | Australia (access) | 60 days in logs; gap: Southgate copies | D3, D4 |

- **Proposed APP 5 notice and privacy-policy additions, including APP 1.8 entries:** n/a: Southgate holds no Australian individuals' information on the record; gap: Southgate's own privacy policy entry for support access to client logs (counsel: confirm).

## Canada: Consent and notice inputs

- **The four key elements up front (what personal information, which parties, what purposes, the risk of harm):** proposed just-in-time notice at first use naming the personal information (questions, leave requests and reasons, employee ID), Google and Southgate Labs as parties, the purposes (answer, decide routine leave, support) and the risk of decisions made without a person; no text exists (gap: notice; counsel: implied or express consent, with express generally needed for sensitive information per the OPC, checked 2026-10-26).
- **Foreign processing notice:** staff must be told their information may be processed in the United States and Australia and be accessible to those countries' courts and authorities, ideally when collected (OPC 2009 guidelines, checked 2026-10-26); no text exists (gap: notice).
- **Alberta, if in scope:** n/a: no Alberta staff or flow (docs/discovery/hr-assistant.md §1).
- **BC, if in scope:** n/a: no BC staff or flow (docs/discovery/hr-assistant.md §1).

## Canada: Quebec PIA and s 17 facts

- **s 3.3 project facts:** an AI system for 1,150 Montréal employees reading and writing HR profile and leave data, with health details possible in free text, for answering policy questions and approving routine leave (R1 to R4, docs/discovery/hr-assistant.md §3); the EFVP is Érable's (wait W3).
- **Each flow leaving Quebec:** (1) Toronto hosting and logs (D2); (2) Gemini processing in the United States (D1); (3) Sydney log access (D4); (4) UKG location unknown (gap). Sensitivity, contractual measures, destination law and the written agreement per flow are in transfer-assessment.md (counsel: adequate protection; wait W4).
- **Privacy by default (s 9.1) and profiling (s 8.1):** s 9.1 targets products offered to the public, so n/a: internal employee tool (assumption: an internal tool is not offered to the public; counsel: confirm). No memory, personalisation or history sharing is designed (R1 to R4); the 60-day log is the only retained history (D3). No profiling function is designed (R1 to R4).

## Questions for counsel

- counsel: is a Quebec EFVP required before the pilot starts, and what does s 17 need per flow; regime Canada, Quebec; wait W3, wait W4.
- counsel: is express consent needed for leave reasons, and for the US and Sydney handling; regime Canada, Quebec; needed before W2 closes.
- counsel: what retention and access path is required for 60-day logs with employee IDs (D3), and does the Quebec Act's destruction rule fit; regime Canada, Quebec.
- counsel: does reading logs from Sydney make Southgate Labs subject to the Privacy Act, and what must it do beyond the contract; regime Australia; facts at D4.
- counsel: is the replay of 500 July 2026 requests (M2) a compatible re-use of leave data; regime Canada, Quebec.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Marie-Claude Gagnon, person in charge of the protection of personal information, Érable Logistics Inc. | this document | pending | pending |
| Me Geneviève Roy, counsel, Érable Logistics Inc. | this document | pending | pending |
