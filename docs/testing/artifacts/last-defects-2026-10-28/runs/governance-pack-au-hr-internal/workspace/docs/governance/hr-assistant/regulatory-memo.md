---
document: regulatory-memo
system: Staff HR assistant (Wattle & Co)
version: design accepted 2026-09-24; build v0.4.1 (M1 to M3)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Wattle & Co counsel (not named in the record) and Privacy Officer (Grace Nguyen)
sources: docs/discovery/hr-assistant.md, docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md
---

# Regulatory memo: Staff HR assistant (Wattle & Co)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for Wattle & Co's counsel. It records which regimes the jurisdiction
screen found in scope, the facts the design records, and the provisions that
appear relevant in Australia. Conclusions are proposals for counsel; not
legal advice.

## Summary

- **Regimes in scope:** Australia only (Jurisdiction screen below; counsel: confirm the screen).
- **Main obligations in Australia:** (1) APP 1.7 to 1.9 automated-decision entries in the privacy policy from 10 December 2026, relevant because managers are pointed to the assistant before performance conversations (D6, C5; APP 1.7, checked 2026-10-26); (2) APP 8 and s 16C for the Sentry US-region flow of request and response bodies (D4) and any Gemini processing outside Australia (D1; gap: processing region not read); (3) APP 3.3 and APP 11 for union and medical information that masking misses (C4, M2); (4) NSW workplace surveillance notice for the NSW pilot (W3).
- **Proposed roles:** Wattle & Co is the employer and the deployer; Southgate Labs builds and supports and is an APP entity in its own right for its handling (Roles below; counsel: confirm).
- **Facts the Privacy Officer and Head of Security should read first:**
  - Prompts and answers are logged for 30 days in Sydney (D3), but application error bodies, including request and response bodies, go to a US-region Sentry project (D4). The "everything stays in Sydney" reading of D2 is therefore wrong for error bodies.
  - Masking of union and medical phrases caught 82% of 150 synthetic test prompts (M2); misses include "my delegate", "SDA meeting", "physio" and "IVF appointment". The record does not say whether masking (C4) sits in front of the Sentry path (gap: C4 scope against D4).
  - Southgate Labs engineers in Sydney read logs and Sentry during the pilot and a three-month support period (D5).
- **Blocking questions:** counsel: 11 questions, listed under Questions for counsel.

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes | Wattle & Co is an Australian retailer with 4,800 staff in NSW, Victoria and Queensland (docs/discovery/hr-assistant.md §1); Southgate Labs engineers in Sydney read personal information (D5) | Client established in Australia and data subjects in Australia; the consultancy's own handling also brings it in |
| United States | no | No US client or staff (docs/discovery/hr-assistant.md §1); Sentry stores error bodies in its US region (D4) | n/a: data merely stored in the US does not bring US state privacy laws in; it is an APP 8 fact (source: adk-governance-pack reference, read 2026-10-28) |
| EU | no | No EU establishment, staff or market recorded (docs/discovery/hr-assistant.md §1) | n/a: no EU nexus; assumption: no staff are located in the EU, counsel to confirm |
| United Kingdom | no | No UK establishment or staff recorded (docs/discovery/hr-assistant.md §1) | n/a: no UK nexus; assumption: no staff are located in the UK |
| New Zealand | no | No New Zealand client, staff or data recorded (docs/discovery/hr-assistant.md §1) | n/a: no New Zealand nexus; assumption: no New Zealand staff |
| Singapore | no | No Singapore client, staff or data recorded (docs/discovery/hr-assistant.md §1) | n/a: no Singapore nexus; assumption: no Singapore staff |
| Canada | no | No Canadian client, staff or data recorded (docs/discovery/hr-assistant.md §1) | n/a: no Canadian nexus; assumption: no Canadian staff |

- **Processing locations:** Cloud Run, Cloud SQL and logs in australia-southeast1 (D2); Gemini endpoint pinned in australia-southeast1 (D1); error bodies in Sentry's US region (D4); Southgate engineers access from Sydney (D5). gap: the model page was not readable in this session, so the model's machine-learning processing region, abuse-monitoring storage and retirement date are unconfirmed; propose a check by adk-model-and-output-contracts beside D1.
- **Government client:** n/a: private retailer (docs/discovery/hr-assistant.md §1). No government form answers are drafted. Consultancy home: assumption: Australia (default).

## System and intended purpose

- **What it does:** answers staff questions on their own leave balance, roster and HR policy, and lets managers ask about the leave and attendance of people who report to them, by reading Workday (R1, R2, C3).
- **Who uses it and who it affects:** pilot of 300 staff and 25 managers in NSW stores (docs/discovery/hr-assistant.md §6); the wider design covers 4,800 staff (docs/discovery/hr-assistant.md §1). Team members whose attendance a manager asks about are affected but are not the person using it (R2, D6).
- **What the model decides and what code or people decide:** the model drafts answers and summaries; Workday reads are scoped by code to the verified employee and supervisory organisation (C1, C2, D7); the manager decides what to do with a summary (D6).
- **Effects it can cause:** read only, no write to Workday and no approval of leave (R4, C3); a summary can influence a performance conversation (docs/discovery/hr-assistant.md §4).
- **Human review of decisions about people:** the summary lists the records it is built from so the manager can check it (C5); gap: no measured share of summaries a manager checks or overrides. Summaries matched Workday in 95% of 60 (M3).

## Roles

- **Facts:** Wattle & Co commissions and decides (source: docs/discovery/hr-assistant.md §5); the assistant runs for Wattle's staff behind Entra ID sign-in (D7); Southgate Labs builds it and its engineers read logs and Sentry in Sydney during the pilot and three months of support (D5); Google supplies the model (D1); Sentry receives error bodies (D4). gap: no contract or data-processing terms with Google, Sentry or between Wattle and Southgate Labs are in the record.
- **Australia, Privacy Act:** Wattle & Co is an APP entity if its turnover exceeds $3 million (assumption: it does, as a 4,800-staff retailer; counsel: confirm s 6D). The employee records exemption (s 7B(3)) may take Wattle's own acts directly related to the employment relationship, and employee records, outside the APPs; the OAIC says it does not cover contractors handling an employer's employee information, so Southgate Labs is not covered by Wattle's exemption (source: adk-governance-pack reference australia.md, read 2026-10-28; checked 2026-10-26). gap: Southgate Labs' turnover is not recorded (counsel: is Southgate an APP entity in its own right; does the exemption reach Wattle's use of the assistant; does it reach APP 1.7). There is no processor category in Australian law today.
- **Supply-chain roles (Guidance for AI Adoption terms):** Southgate Labs as system developer, Google as model developer, Wattle & Co as deployer (source: adk-governance-pack reference australia.md, read 2026-10-28).

## Australia: Privacy Act and APPs

- **No AI-specific regime:** Australia has no AI Act; the 2024 mandatory guardrails proposal will not proceed, and obligations come from the laws screened here (checked 2026-10-26).
- **APPs engaged (if they apply, see Roles):** APP 3 and 3.3 for union membership and medical details typed into prompts and leave reasons (docs/discovery/hr-assistant.md §3, C4); APP 5 for notice to staff; APP 6 for using Workday data for the assistant; APP 8 and s 16C for Sentry and any Gemini processing outside Australia (D1, D4); APP 10 for accuracy of summaries (M1, M3); APP 11 for the masking gap and retention (D3, M2); APP 12 and 13 for logs held about a person (D3). Each is set out in privacy-impact-input-pack.md.
- **Overseas disclosure (APP 8, s 16C):** Sentry US region receives error bodies with request and response content (D4); gap: whether bodies are scrubbed, Sentry's retention and the contract. counsel: is sending bodies to Sentry a use or a disclosure; is any contract sufficient for APP 8.1. Gemini: endpoint in australia-southeast1 (D1); gap: processing region and abuse-monitoring storage unread.
- **Notifiable data breaches:** an eligible data breach is assessed within 30 days (s 26WH, checked 2026-10-26); gap: no contract term says whether Southgate Labs, Wattle or Sentry notifies (security-questionnaire.md; counsel: which entity notifies; whether the scheme reaches employee records).
- **Pending, not law:** the tranche 2 exposure draft (consultation 31 August to 18 September 2026) does not remove the employee records exemption (checked 2026-10-26).

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| Manager's performance conversation about a team member, informed by "a summary of <name>'s attendance this quarter" | Proposed: substantially and directly related (the manager guide suggests the summary before the conversation) | The manager reads the summary and its source records (C5); gap: share checked or overridden not measured | Could affect a person's employment (docs/discovery/hr-assistant.md §4) | Clock-in, lateness and absences (docs/discovery/hr-assistant.md §3) | D6, C5, M3 (95% of 60 summaries matched Workday); counsel: does it significantly affect rights or interests; is there extensive human oversight and control |
| Leave balance, roster and policy answers to staff | Proposed: not a decision about a person; staff act on the answer (R1) | n/a: no review step | A wrong balance leads someone to book leave they do not have (docs/discovery/hr-assistant.md §4) | Leave balances and rosters | R1, M1 (97% of 240 correct); counsel: confirm not in scope |

- **Privacy policy inputs (APP 1.8):** system-card.md, Automated-decision disclosure (C5).
- The OAIC fact sheet of September 2026 lists AI reports used to rank employee performance as an in-scope example and says human review is not an exemption (source: adk-governance-pack reference australia.md, read 2026-10-28; checked 2026-10-26). Whether the employee records exemption removes the duty from Wattle is counsel's question.

## Australia: Sector, state and government AI policy

- **Workplace surveillance (NSW):** the pilot is NSW staff (docs/discovery/hr-assistant.md §6) and prompts are logged for 30 days (D3). The Workplace Surveillance Act 2005 requires written notice at least 14 days before computer surveillance starts (s 10, per DPC circular C2005-37; re-read at the source; checked 2026-10-26). counsel: is identity-linked prompt logging computer surveillance; gap: whether logs carry the employee ID (D7). Victoria and Queensland staff: counsel, the reference does not cover their rules; they are outside the pilot (docs/discovery/hr-assistant.md §6). Wait W3.
- **Enterprise agreement and Fair Work Act:** the enterprise agreement requires consultation on major workplace change with SDA delegates (docs/discovery/hr-assistant.md §5); counsel: is the assistant major change; do general protections bear on union information reaching managers or engineers through logs (C4, M2). Wait W4.
- **Anti-discrimination:** illness, family and union information in prompts and leave reasons (docs/discovery/hr-assistant.md §4); counsel: indirect discrimination in attendance summaries; no bias measurement is recorded (gap).
- **Statutory tort for serious invasions of privacy (commenced 10 June 2025, checked 2026-10-26):** intentional or reckless conduct only; recorded as a risk line in privacy-impact-input-pack.md (D4, D5).
- **Australian Consumer Law:** n/a: internal staff tool, no consumers (docs/discovery/hr-assistant.md §1).
- **Government AI policy:** n/a: private client (docs/discovery/hr-assistant.md §1).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| Australia | APP 1.7 to 1.9 privacy-policy entries for automated decisions | 10 December 2026 (APP 1.7, Privacy and Other Legislation Amendment Act 2024, checked 2026-10-26) | The pilot decision is 2026-11-27 (docs/discovery/hr-assistant.md §6), so manager summaries in the pilot may fall after commencement; gap: pilot start date |
| Australia | NSW workplace surveillance notice, at least 14 days | before surveillance starts (Workplace Surveillance Act 2005 s 10, checked 2026-10-26) | NSW pilot staff; W3 |

- **Staff training and guidance:** the manager guide exists (D6); gap: no goal covers guidance that a summary is not a finding and must be checked against the records; propose to adk-agent-evaluation under G05.
- **Documents the client's own process produces:** the privacy policy update for APP 1.8 (Privacy Officer, W5); the workplace surveillance notice (Wattle & Co, W3); SDA consultation (Wattle & Co, W4). No government forms apply.

## Questions for counsel

- counsel: Does the employee records exemption (s 7B(3)) apply to Wattle's use of the assistant, and does it reach APP 1.7; regime Australia; facts at D6, docs/discovery/hr-assistant.md §3; needed before W3 and the 2026-11-27 pilot decision.
- counsel: Is Southgate Labs an APP entity in its own right and is its handling covered by the exemption; regime Australia; facts at D5; needed before W6.
- counsel: Is the manager attendance summary a decision substantially and directly related to a decision that significantly affects an individual, and is manager review extensive human oversight (APP 1.7); facts at D6, C5, M3; needed before the pilot decision.
- counsel: Is sending request and response bodies to Sentry's US region a use or a disclosure (APP 8, s 16C), and what contract is needed; facts at D4; needed before the pilot decision.
- counsel: Is union membership or medical information in logs and Sentry "sensitive information" handled without consent (APP 3.3), given masking at 82% (M2); needed before the pilot decision.
- counsel: Is identity-linked prompt logging computer surveillance under the NSW Workplace Surveillance Act 2005 and what notice is needed (W3).
- counsel: Do Victorian and Queensland rules on workplace monitoring or surveillance need review before rollout beyond the NSW pilot.
- counsel: Does the enterprise agreement require consultation with the SDA before the pilot (W4).
- counsel: Do Fair Work general protections or anti-discrimination law limit the use of attendance summaries in performance conversations.
- counsel: Which entity assesses and notifies an eligible data breach, and does the scheme reach employee records.
- counsel: Is the model's processing region, abuse-monitoring storage or support access outside Australia a use or a disclosure (APP 8); gap: model page unread (D1).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Wattle & Co counsel (name gap: not in the record) | this document | pending | pending |
| Privacy Officer (Grace Nguyen) | this document | pending | pending |
