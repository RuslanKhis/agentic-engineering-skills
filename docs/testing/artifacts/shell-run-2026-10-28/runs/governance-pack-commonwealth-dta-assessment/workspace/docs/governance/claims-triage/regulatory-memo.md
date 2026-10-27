---
document: regulatory-memo
system: Claims triage assistant (Compensation Claims Office)
version: design accepted 2026-09-19, build v0.6.3
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CCO legal counsel or AI accountable official (Helen Park)
sources: docs/discovery/claims-triage.md, docs/architecture/claims-triage.md, docs/plans/claims-triage.md
---

# Regulatory memo: Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for the Compensation Claims Office's (CCO) counsel. It records which regimes the jurisdiction screen found in scope, the facts the design records, and the provisions that appear relevant in Australia, which has no AI Act and assigns no risk tier. Conclusions are proposals for counsel; not legal advice.

## Summary

- **Regimes in scope:** Australia only, through the client (a non-corporate Commonwealth entity) and the claimants (docs/discovery/claims-triage.md §1, §3). counsel: confirm the screen, in particular that no claimant lives outside Australia.
- **Main obligations in Australia:** (1) APP 1.7 to 1.9 automated-decision entries in the CCO's APP privacy policy apply from 10 December 2026 (checked 2026-10-26), two days after the pilot decision on 2026-12-08 (docs/discovery/claims-triage.md §6); (2) a PIA is required for a high privacy risk project under the Agencies Privacy Code (checked 2026-10-26), already a wait, W2; (3) the DTA AI impact assessment for in-scope use cases is due to begin by 15 December 2026 and must be finished with treatments applied before deployment (checked 2026-10-26); (4) APP 11 and APP 8 on sensitive health information and the Gemini endpoint (D1, D2). All carry counsel: confirm.
- **Proposed roles:** the CCO is the APP entity and the deployer; Southgate Labs is a contracted service provider and system developer; Google is model and cloud provider (D1, D4; counsel: confirm).
- **Direct question from the requester (what the department's privacy officer needs):** the pack answers it with the input pack, the system card and the security questionnaire in this folder (source: engagement lead brief, 2026-10-28).
- **Blocking questions:** counsel: 9 questions under Questions for counsel; those needed before the pilot decision of 2026-12-08 are marked.
- **Proposed EU classification:** n/a: the EU is not in scope (Jurisdiction screen).

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes | CCO is a non-corporate Commonwealth entity (docs/discovery/claims-triage.md §1); claimants are Australian residents (docs/discovery/claims-triage.md §3); Southgate Labs staff in Sydney access logs and the evaluation set (D4) | Client establishment and data subjects; consultancy handling too. counsel: confirm |
| United States | no | Canberra and Adelaide officers, Australian claimants (docs/discovery/claims-triage.md §1, §3) | n/a: no US client, data subjects or processing purpose |
| EU | no | No EU client or people in the EU in the record (docs/discovery/claims-triage.md §3) | n/a: no EU establishment, offer or monitoring. assumption: no claimant is resident in the EU; counsel: confirm |
| United Kingdom | no | As for the EU | n/a: no UK establishment or people in the UK in the record. assumption: no claimant is resident in the UK; counsel: confirm |
| New Zealand | no | No NZ client or people in the record (docs/discovery/claims-triage.md §3) | n/a: assumption: former Commonwealth contractors resident in New Zealand are not in the claimant population; gap: residence of claimants is not recorded, so a CCO check is needed |
| Singapore | no | As for New Zealand | n/a: assumption: no claimant resident in Singapore; gap: as above |
| Canada | no | As for New Zealand | n/a: assumption: no claimant resident in Canada; gap: as above |

- **Processing locations:** Cloud Run, Cloud SQL and logs in australia-southeast1 (D2); Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` on Vertex AI in australia-southeast1 (D1); gap: the model's machine-learning processing region and retirement date were not read on the provider's model page (no network in this session), proposed as a goal for adk-model-and-output-contracts; Southgate Labs staff access from Sydney (D4).
- **Government client:** Commonwealth agency, non-corporate Commonwealth entity under the PGPA Act (docs/discovery/claims-triage.md §1).
- **Consultancy home:** assumption: Australia (default; Sydney per D4).

## System and intended purpose

- **What it does:** reads a new claim and drafts a triage recommendation (category, priority, missing evidence) that a claims officer accepts or changes (R1; README.md).
- **Who uses it and who it affects:** 20 claims officers in Canberra for an 8-week pilot (docs/discovery/claims-triage.md §6); it affects claimants, former Commonwealth contractors injured at work, about 1,900 new claims a month across 120 officers (docs/discovery/claims-triage.md §1, §3).
- **What the model decides and what code or people decide:** the model drafts; the officer accepts or changes every draft; the assistant records nothing in the case system (R4, C3); determining liability or payment and contacting claimants are out of scope (docs/architecture/claims-triage.md Scope gate).
- **Effects it can cause:** reads claims in the officer's team queue (R3, C1); drafts cite claim passages, otherwise the draft is withheld (R2, C2); the officer's accept or change is recorded with the draft (C4).
- **Human review of decisions about people:** every draft passes an officer (R4, C4); override rate during the pilot is not yet measured (gap: the baseline is 11% of triage decisions changed at assessment, docs/discovery/claims-triage.md §2; no pilot figure exists). Offline agreement with officer decisions: category 88% (M1), priority 79% (M2), 900 past claims, build v0.6.3.
- **Harms the brief names:** a wrong low priority delays payment to an injured person; a wrong category adds weeks; officers may rely on the draft without reading the notes (docs/discovery/claims-triage.md §4).

## Roles

- **Facts:** the CCO commissions it and its Assistant Secretary is sponsor and decider (docs/discovery/claims-triage.md §5); Southgate Labs builds it and supports the pilot from Sydney with access to logs and the evaluation set (D4); Google supplies Gemini and the cloud (D1, D2). gap: the contract (clauses on privacy, s 95B, AI model clauses) was not provided.
- **Australia, Privacy Act:** the CCO is an agency bound by the Privacy Act and the Agencies Privacy Code. Southgate Labs is a contracted service provider if the contract carries s 95B terms; there is no processor category in Australian law today (counsel: confirm roles, and whether Southgate Labs is an APP entity in its own right).
- **Supply chain in Guidance for AI Adoption terms:** Southgate Labs as system developer, Google as model developer, the CCO as deployer (source: adk-governance-pack reference, read 2026-10-28; not re-read at the source).

## Australia: Privacy Act and APPs

- **No AI-specific regime:** Australia has no AI Act; the 2024 mandatory guardrails proposal will not proceed (checked 2026-10-26).
- **APPs engaged:** APP 3 and 3.3 (claim notes carry injury, medical, mental-health and family-violence information, docs/discovery/claims-triage.md §3; drafts are generated information); APP 5 notice to claimants; APP 6 (use of existing claim data for triage and for evaluation, D5); APP 8 (D1, D2); APP 10 (M1, M2); APP 11 (SB01, SB03, D2, D3); APP 12 and 13 (decisions table C4, logs D3, evaluation set D5). Detail in privacy-impact-input-pack.md.
- **Overseas disclosure (APP 8, s 16C):** the design records hosting and the endpoint in australia-southeast1 (D1, D2). gap: whether the model's processing, abuse monitoring or support access sits outside Australia was not read at the provider's page; counsel: use or disclosure if any step is offshore.
- **Notifiable data breaches:** gap: no incident procedure is recorded in the design; which entity assesses within 30 days and notifies (the CCO, Southgate Labs, Google) is counsel: confirm; see security-questionnaire.md.
- **Pending, not law:** the tranche 2 privacy reform exposure draft (consultation closed 18 September 2026, checked 2026-10-26).

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| Triage of a new compensation claim: category, priority, missing evidence | Proposed: substantially and directly related (a key factor in the officer's triage); not solely automated | Every draft goes to an officer who accepts or changes it (R4, C4); share changed in the pilot: gap: not yet measured; baseline 11% (docs/discovery/claims-triage.md §2) | Priority governs how fast an injured person is paid; category governs routing (docs/discovery/claims-triage.md §4) | Claim form and notes, medical reports, including health and mental-health information (docs/discovery/claims-triage.md §3) | C2, C4, M1, M2; counsel: does it significantly affect rights or interests; is review "extensive human oversight and control"; is triage a decision under an Act |

- **Privacy policy inputs (APP 1.8):** system-card.md, Automated-decision disclosure (C4). The duty rests with the CCO; the entries apply from 10 December 2026 (checked 2026-10-26).

## Australia: Sector, state and government AI policy

- **Sector laws:** the CCO's governing compensation legislation and records obligations are not recorded; agency: name the Act under which claims are handled and whether it constrains use of automated tools or overseas processing. n/a: no consumer, APRA, My Health Record or telemarketing trigger in the record (docs/discovery/claims-triage.md §2). counsel: the Archives Act and Freedom of Information Act treatment of prompts, drafts and logs (D3).
- **Government AI policy:** DTA Policy for the responsible use of AI in government v2.1 (published 21 October 2026, checked 2026-10-26); the CCO must apply it as a non-corporate Commonwealth entity.

## Australia: Government client (Commonwealth or NSW agency)

- **Client and policy:** non-corporate Commonwealth entity under the DTA Policy v2.1 (docs/discovery/claims-triage.md §1; checked 2026-10-26).
- **Official forms and where the pack's answers are:** DTA AI impact assessment tool (government-form-answers-dta-impact-assessment.md), AI transparency statement inputs (government-form-answers-dta-transparency-statement.md), use case register row (government-form-answers-dta-use-case-register.md) and Agentic AI addendum (government-form-answers-dta-agentic-addendum.md). agency: the assessing and approving officers complete and approve them in the official tool; Southgate Labs is not the form-filler.
- **Review committee:** the Commonwealth AI Review Committee gives advice on use cases rated residual high risk or identified as highly sensitive, novel or complex (checked 2026-10-26). agency: whether to refer; the use case handles sensitive health information (docs/discovery/claims-triage.md §3); wait W4 (conditional).
- **Privacy Act roles:** s 95B contract terms and the Agencies Privacy Code PIA (checked 2026-10-26); the PIA is W2. counsel: does the contract flow the APPs down to Southgate Labs and any subcontractor, and does s 95B cover every act?
- **Security:** the environment is assessed against PROTECTED by the CCO's security team (D2); IRAP assessment booked 2026-11-16 (W1). gap: the information classification of claim data and the ISM and PSPF direction were not recorded; agency: Chief Security Officer.

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| Australia | APP 1.7 to 1.9 privacy policy entries for automated decisions | 10 December 2026 (Privacy and Other Legislation Amendment Act 2024, checked 2026-10-26) | The pilot decision is 2026-12-08 and the pilot runs 8 weeks after it (docs/discovery/claims-triage.md §6); the CCO's policy needs the entries before decisions made after that day; counsel: confirm |
| Australia | DTA AI impact assessment for in-scope use cases | by 15 December 2026 (DTA Policy v2.1, checked 2026-10-26) | Must be finalised with treatments before deployment; W3 |
| Australia | Existing in-scope use cases not yet assessed | by 30 April 2027 (DTA Policy v2.1, checked 2026-10-26) | n/a: this is a new use case |
| Australia | DTA Policy v2.1 and the transparency standard v2.1 | published 21 October 2026 and updated 20 October 2026 (DTA, checked 2026-10-26) | Re-read the forms before the agency completes them; gap: official pages not re-read in this session |

- **AI literacy and staff training:** gap: no officer training goal exists in the plan; propose a goal for the handover (DTA tool 6.8).
- **Documents the client's own process produces:** the DTA AI impact assessment (assessing and approving officers; W3); the AI transparency statement and register row (agency owner; agency: dates); the Commonwealth AI Review Committee referral if required (W4, conditional); the PIA under the Agencies Privacy Code (privacy officer; W2); the APP privacy policy update (privacy officer; W5); IRAP assessment (W1).

## Questions for counsel

- counsel: does a triage recommendation that sets category and priority amount to a computer program doing a thing "substantially and directly related" to a decision that "significantly affects" claimants (APP 1.7)? Needed before the pilot decision of 2026-12-08 (W5).
- counsel: is officer review of every draft "extensive human oversight and control", given automation bias is a named harm (docs/discovery/claims-triage.md §4) and no pilot override figure exists? Needed before W5.
- counsel: does the CCO's governing legislation authorise the use of an automated tool in triage (DTA tool 1.8)? Needed before W3.
- counsel: is the PIA required as a high privacy risk project under the Agencies Privacy Code? Needed before W2.
- counsel: is sending claim notes to Gemini a use or a disclosure (APP 8, s 16C), once the model's processing region is read at the source? Needed before W2.
- counsel: does the contract with Southgate Labs carry s 95B terms and flow-down, and who notifies an eligible data breach? Needed before W2.
- counsel: collection of sensitive information in free-text notes and in generated drafts (APP 3.3), and the APP 5 notice to claimants. Needed before W2.
- counsel: how do the Archives Act and the Freedom of Information Act treat prompts, drafts and 30-day logs (D3)? Needed before the pilot.
- counsel: human rights alignment (DTA tool 10.2) and whether an AI Review Committee referral is warranted given sensitive health data. Needed before W3 and W4.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO counsel or AI accountable official (Helen Park) | this document | pending | pending |
