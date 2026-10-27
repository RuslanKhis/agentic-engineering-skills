---
document: regulatory-memo
system: HR assistant (Érable Logistics)
version: design accepted 2026-09-11, build v0.5.0
status: draft
jurisdictions: [au, ca]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Me Geneviève Roy, counsel, Érable Logistics Inc.
sources: docs/discovery/hr-assistant.md, docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md
---

# Regulatory memo: HR assistant (Érable Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Érable Logistics' counsel (counsel: this memo records facts and proposed conclusions only). It records which regimes the jurisdiction screen found in scope, the facts the design records and the provisions that appear relevant. Canada has no AI Act and assigns no risk tier (checked 2026-10-26). The law was taken from the skill's references, last read at the source on 2026-10-26; it was not re-read at the source for this draft (no network access in this session).

## Summary

- **Regimes in scope:** Australia (the consultancy's own handling only) and Canada (Quebec and Ontario); the United States, EU, United Kingdom, New Zealand and Singapore are out, with reasons in the Jurisdiction screen (counsel: confirm the screen).
- **Direct question, does Law 25 apply to the leave decisions?** Proposed answer: yes for Montréal staff. Érable is a Montréal-headquartered enterprise with 1,150 Montréal staff (docs/discovery/hr-assistant.md §1), and Quebec's private sector Act as amended by Law 25 covers an enterprise's Quebec employees (CAI aide-mémoire, checked 2026-10-26). The leave approval is made by a rule with no human review (C3, C4, D5), which is the fact pattern s 12.1 (decisions based exclusively on automated processing) addresses. The same Act also brings in s 3.3 (a PIA for the system project), s 17 (every flow leaving Quebec) and s 3.1 (person in charge). counsel: confirm that s 12.1 applies, because the reference records the section's wording as reported, not confirmed at the source on 2026-10-26, and does not settle whether it reaches a favourable decision such as an approval.
- **Open on the same question:** whether the Quebec Act reaches Toronto staff data held by a Quebec enterprise, or PIPEDA or no statute governs it, is not settled by the reference (counsel: Canada: Privacy laws and roles below). Ontario has no general private sector privacy statute for a provincially regulated employer's staff (checked 2026-10-26).
- **Main obligations in the other regime:** Australia, for Southgate Labs only: the Privacy Act's reach over its Sydney log access to Canadian staff data, and eligible data breach duties (D4; counsel: whether the Act reaches it).
- **Proposed roles:** Érable is the organisation responsible for the information under its control; Southgate Labs and Google act for it; whether either has an own purpose is open (Roles below; counsel: confirm).
- **Blocking questions:** counsel: 14 questions, listed under Questions for counsel; the pilot decision is due 2026-11-24 (docs/discovery/hr-assistant.md §6).

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes | Southgate Labs engineers in Sydney read logs during the pilot and a three-month support period (D4); consultancy home Sydney (docs/discovery/hr-assistant.md §5; assumption: consultancy home Australia) | Consultancy's own handling only; counsel: whether the Privacy Act reaches Canadian employees' data read from Australia. The client's own APP rows are n/a: client and data subjects are in Canada |
| United States | no | Staff in Montréal and Toronto only (docs/discovery/hr-assistant.md §1); Gemini processing in the US is a transfer fact (D1) | n/a: no US client or US data subjects; data processed in the US does not bring state privacy laws in |
| EU | no | No EU establishment, staff or output use (docs/discovery/hr-assistant.md §1) | n/a: no EU nexus in the record; assumption: none exists |
| United Kingdom | no | No UK establishment or staff (docs/discovery/hr-assistant.md §1) | n/a: no UK nexus in the record; assumption: none exists |
| New Zealand | no | No New Zealand client or staff (docs/discovery/hr-assistant.md §1) | n/a: no New Zealand nexus; the Sydney access is to Canadian data |
| Singapore | no | No Singapore client or staff (docs/discovery/hr-assistant.md §1) | n/a: no Singapore nexus |
| Canada | yes | Federally incorporated employer, head office Montréal; 1,150 Montréal and 640 Toronto staff (docs/discovery/hr-assistant.md §1) | People in Quebec and Ontario; Quebec Act applies to the Montréal staff (checked 2026-10-26); counsel: which law governs each flow |

- **Processing locations:** Cloud Run, Cloud SQL and logs in northamerica-northeast2 (Toronto) (D2); Gemini 3.5 Flash through the Vertex AI global endpoint, processing in the United States per the model page read 2026-09-10 (D1; not re-read); Sydney engineers read the logs (D4). gap: the model's retirement date and current processing region were not re-read (no network); proposed goal for adk-model-and-output-contracts.
- **Government client:** private client; Érable is a private logistics employer (docs/discovery/hr-assistant.md §1). n/a: no Commonwealth, NSW, federal or Ontario public body.

## System and intended purpose

- **What it does:** answers HR policy questions in French or English from published policies and takes leave requests, recording them in UKG (R1, R2); it auto-approves routine requests (R3).
- **Who uses it and who it affects:** distribution-centre staff in Montréal (1,150) and Toronto (640); the pilot is one shift at each centre for 6 weeks (docs/discovery/hr-assistant.md §1, §6). gap: the number of staff on the pilot shifts.
- **What the model decides and what code or people decide:** the model only extracts dates and leave type; the rule in C3 decides (D5); other requests go to the manager (R4, C5).
- **Effects it can cause:** writes an approval to UKG with approver "HR assistant" and no human review (C4); affects pay, scheduling and attendance records (docs/discovery/hr-assistant.md §4).
- **Human review of decisions about people:** none for auto-approved requests (C4). The share is measured: the rule approves 64% of pilot-shape requests without review (M2, replay of 500 July 2026 requests). gap: no measured pilot share, override rate or complaint rate; the 1.2% reversal baseline predates the assistant (docs/discovery/hr-assistant.md §2).
- **Out of scope:** pay, discipline and leave of two days or more (docs/architecture/hr-assistant.md Scope gate).

## Roles

- **Facts:** Érable commissions it and the staff use it under Érable's name (docs/discovery/hr-assistant.md §1). Southgate Labs built it and its Sydney engineers read logs (D4). Google processes prompts through Gemini (D1). gap: whose Google Cloud project and agreement hosts D2, and which contract binds Southgate and Google.
- **Australia, Privacy Act:** Southgate Labs may be an APP entity in its own right (gap: annual turnover not recorded); the employee records exemption does not cover a contractor handling another organisation's employee information (source: adk-governance-pack reference australia.md, read 2026-10-28). Australian law has no processor category (counsel: confirm whether the Act reaches the Sydney access).
- **Canada:** the statutes have no controller and processor. Érable is the organisation responsible for personal information under its control, including information passed to a third party for processing (PIPEDA Schedule 1, 4.1.3, checked 2026-10-26; Quebec speaks of mandates and service contracts). counsel: whether Southgate Labs acts only for Érable or also for its own purposes (for example evaluation or product improvement, no record either way: gap).
- **Quebec person in charge (s 3.1):** Marie-Claude Gagnon, Director, HR Operations (docs/discovery/hr-assistant.md §5). gap: whether title and contact details are published on Érable's website.

## Australia: Privacy Act and APPs

- **No AI-specific regime:** Australia has no AI Act; the mandatory guardrails proposal will not proceed (checked 2026-10-26).
- **APPs engaged:** the consultancy's own handling only: reading log content (prompts with employee IDs, D3, D4) is a use of personal information; APP 11 security and destruction apply to what Southgate holds or can see (gap: how and where staff access logs, what they copy). Client-side APP 3, 5, 6, 10, 12 and 13 rows are n/a: client and data subjects are in Canada.
- **Overseas disclosure (APP 8, s 16C):** n/a: the data originates in Canada and Southgate does not send it onward from Australia on the record (D4); gap: confirm no copy, export or evaluation set leaves Sydney (counsel: use or disclosure if one does).
- **Notifiable data breaches:** an eligible data breach is assessed within 30 days and notified as soon as practicable (checked 2026-10-26); gap: no contract term says which entity notifies (counsel: which entity notifies).
- **Pending, not law:** n/a: the tranche 2 and children's code items do not touch this system.

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| n/a: Southgate Labs makes no decision about a person; Érable's leave approval concerns Canadian staff, so APP 1.7 is not the client's rule | n/a: client-side APP 1.7 row | n/a | n/a | n/a | C3, C4; counsel: confirm APP 1.7 is out for Southgate |

- **Privacy policy inputs (APP 1.8):** n/a: no Australian client; the system card's disclosure block serves Canada (system-card.md).

## Australia: Sector, state and government AI policy

- **Sector laws:** n/a: no Australian staff or customers, so no NSW workplace surveillance notice and no sector regulator (docs/discovery/hr-assistant.md §1).
- **Government AI policy:** n/a: private client, no DTA or NSW AIAF duty (docs/discovery/hr-assistant.md §1).

## Canada: Privacy laws and roles

- **No AI-specific statute:** Canada has no AI Act; the Artificial Intelligence and Data Act died with Bill C-27, and Bill C-36 is not law (checked 2026-10-26).
- **Which law governs each flow:** Quebec's private sector Act (Law 25) for Montréal staff; for Toronto staff PIPEDA reaches employee information only at a federal work, undertaking or business (checked 2026-10-26), and Érable is described as provincially regulated (docs/discovery/hr-assistant.md §1). counsel: which law governs each flow.

| Flow (input pack Data flows) | People and province | Law proposed | Evidence |
| --- | --- | --- | --- |
| Policy questions and prompts, logged with employee ID for 60 days | Montréal staff, Quebec | Quebec Act | D3; counsel: confirm |
| Policy questions and prompts, logged with employee ID for 60 days | Toronto staff, Ontario | n/a: no general private sector statute for Ontario staff of a provincially regulated employer (checked 2026-10-26); counsel: does the Quebec Act reach it because the enterprise is in Quebec | D3 |
| Leave requests and reasons, written to UKG; reasons may mention health or family matters | Montréal staff | Quebec Act, sensitive information | docs/discovery/hr-assistant.md §3; counsel: confirm |
| Leave requests and reasons | Toronto staff | as the Toronto row above | docs/discovery/hr-assistant.md §3; counsel: confirm |
| Sydney engineers read logs | both | Quebec s 17 for Montréal data; Toronto per counsel | D4; counsel: confirm |

- **Consent and appropriate purposes:** meaningful consent and the s 5(3) reasonable-person test are PIPEDA terms; for Quebec staff the Act's own consent rules apply. The record has no notice or consent text (gap: employee notice naming Google and the foreign processing; counsel: express or implied consent, since leave reasons may be sensitive).
- **Cross-border and out-of-Quebec flows:** Toronto hosting is already outside Quebec (D2), as are US model processing (D1) and Sydney access (D4); each needs a s 17 assessment and a written agreement before it runs (transfer-assessment.md; checked 2026-10-26; counsel: adequate protection).
- **Breach clocks and records:** Quebec: notify the CAI and the person on a risk of serious injury and keep an incident register; PIPEDA, where it applies: as soon as feasible and a 24-month record of every breach (checked 2026-10-26; security-questionnaire.md; counsel: which entity reports to which commissioner).
- **Quebec obligations the pilot meets:** s 3.3 PIA for an information system project, which an AI system is (checked 2026-10-26); the input pack is input to Érable's EFVP (wait W3). The Charter of the French Language and the collective agreement are not covered by this pack (counsel: do they require French notices or interfaces, or union notice, for this system; wait W5).

## Canada: Automated decisions

| Decision the agent touches | Exclusive automation (Quebec s 12.1) | Review route and measured share | Explanation the design can produce | Evidence |
| --- | --- | --- | --- | --- |
| Approval of leave under two days for Montréal staff | Proposed: yes in operation, the rule decides and writes approver "HR assistant" with no human review (the model only extracts dates and leave type) | none designed for an approved request; 64% of pilot-shape requests are approved this way (M2); gap: no route to submit observations to a staff member | The three conditions in C3 (under two days, balance covers it, no blackout date) are the principal factors; gap: no mechanism returns them to the employee | C3, C4, D5, M2; counsel: does s 12.1 apply to a favourable decision |
| Referral of any other request to the manager | n/a: a person decides, nothing is refused by the assistant | manager's UKG queue | n/a | C3, C5 |

- **Notice:** s 12.1 requires telling the person no later than when they are informed of the decision (checked 2026-10-26; wording reported; not confirmed at the source on 2026-10-26). The brief records staff may not know a request was decided without a person (docs/discovery/hr-assistant.md §4); gap: no notice in the design.
- **Extraction risk:** dates and leave type were extracted correctly in 98.4% of 500 replayed requests (M3), so about 1.6% could feed the rule wrongly; gap: no employee confirmation of extracted dates in the contracts (C3).
- **Federal client:** n/a: not a federal institution (docs/discovery/hr-assistant.md §1).

## Canada: Employment, sector and government AI policy

- **Employment:** Toronto has 640 staff, so an Ontario employer with 25 or more employees must have a written electronic monitoring policy (checked 2026-10-26); whether prompt logging tied to employee IDs (D3) needs it updated now is open (counsel: update now or at the next cycle; wait W6). Ontario job-posting AI disclosure is n/a: the assistant does not screen applicants (R1 to R4). Human rights codes apply to decisions about people (checked 2026-10-26; impact-assessment.md Adverse impact and equality); counsel: any disparity in auto-approval by group or language.
- **Sector and consumer:** CASL is n/a: no outbound commercial messages (R1 to R4). PHIPA is n/a: Érable is not a health information custodian (docs/discovery/hr-assistant.md §1); counsel: whether health details in leave reasons raise a separate duty.
- **Government client:** n/a: private client (docs/discovery/hr-assistant.md §1).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| Canada, Quebec | s 3.3 PIA for system projects and s 17 PIA before communication outside Quebec | 22 September 2023 (CAI aide-mémoire, checked 2026-10-26) | In force now; W3 and W4 before the pilot |
| Canada, Quebec | s 12.1 decisions based exclusively on automated processing | 22 September 2023 (CAI aide-mémoire, checked 2026-10-26; wording reported; not confirmed at the source on 2026-10-26) | In force now; the leave approval rule (C3, C4) |
| Canada, Quebec | s 27 portability and the final phase of Law 25 | 22 September 2024 (CAI aide-mémoire, checked 2026-10-26) | In force now; an access or portability request reaches logs and UKG records (D3) |
| Canada, Ontario | Written electronic monitoring policy for employers of 25 or more | the policy must exist before March 1 each year after January 1 headcount (ontario.ca guide, checked 2026-10-26) | Toronto has 640 staff; wait W6 |

- **AI literacy and staff training:** n/a: no EU AI Act duty; gap: no plan goal trains staff or managers on the assistant or on the s 12.1 notice.
- **Documents the client's own process produces:** the Quebec EFVP (owner: Érable person in charge, wait W3) and the s 17 assessments and written agreements (owner: Érable, wait W4); counsel's review (W2); union notice if required (W5); monitoring policy update if required (W6).

## Questions for counsel

- counsel: does Quebec s 12.1 apply to the auto-approval of leave under two days, given a rule and not the model decides and no person reviews it (C3, C4, D5); regime Canada, Quebec; needed before W2 closes and the 2026-11-24 pilot decision.
- counsel: does s 12.1 cover a favourable decision such as an approval, as the reference's reported text is silent; regime Canada, Quebec; facts at C3.
- counsel: what does a compliant s 12.1 notice, explanation and review route look like for a request approved in seconds; regime Canada, Quebec; facts at C4, M2; needed before the pilot starts.
- counsel: does the Quebec Act reach Toronto staff data held by a Quebec enterprise, or does PIPEDA or no statute; regime Canada; facts at docs/discovery/hr-assistant.md §1, D2.
- counsel: does each flow (Toronto hosting D2, US model processing D1, Sydney access D4) receive adequate protection under s 17, and is Google's cloud agreement plus a Southgate contract the written agreement; regime Canada, Quebec; wait W4.
- counsel: is express consent needed for leave reasons that may mention health or family matters, and for sending them to Gemini in the US; regime Canada, Quebec; facts at docs/discovery/hr-assistant.md §3, D1.
- counsel: does a Quebec s 3.3 PIA (EFVP) need to be finished before the pilot, and who signs it; regime Canada, Quebec; wait W3.
- counsel: does the collective agreement at the Montréal centre require notice to or consultation with the union about auto-approval or logging; regime Canada; wait W5 (the reference does not cover it).
- counsel: does the Charter of the French Language require French notices, interface or documents; regime Canada, Quebec (the reference does not cover it).
- counsel: does prompt logging with employee IDs need the Ontario electronic monitoring policy updated now; regime Canada, Ontario; facts at D3; wait W6.
- counsel: are there Ontario employment-law duties (human rights code adverse-impact, collective agreements, common-law torts) for Toronto staff data that this pack has not screened (reference records the statutes as not re-read).
- counsel: does Southgate Labs act only for Érable, and does its Sydney access need anything more than a contract; regime Canada, Australia; facts at D4.
- counsel: is Southgate Labs an APP entity and does the Privacy Act reach its Sydney reading of Canadian employees' logs; regime Australia; facts at D4.
- counsel: which entity notifies which commissioner (CAI, OPC, OAIC) after a breach in logs read from Sydney; regime Canada, Australia; facts at D3, D4.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Me Geneviève Roy, counsel, Érable Logistics Inc. | this document | pending | pending |
