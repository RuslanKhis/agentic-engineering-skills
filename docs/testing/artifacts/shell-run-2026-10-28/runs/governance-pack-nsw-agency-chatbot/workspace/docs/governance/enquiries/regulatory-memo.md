---
document: regulatory-memo
system: Public enquiries assistant
version: design accepted 2026-09-15, build v0.7.0
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Accountable Official for AI (Ruth Abbott), with the agency's counsel
sources: docs/discovery/enquiries.md, docs/architecture/enquiries.md, docs/plans/enquiries.md, docs/contract/order-form-summary.md
---

# Regulatory memo: Public enquiries assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for the NSW Trades Licensing Office's counsel. It records which regimes the jurisdiction screen found in scope, the facts the design records, and the provisions that appear relevant. Australia has no AI Act and assigns no risk tier; the NSW material sits inside the Australia sections. Conclusions are proposals for counsel; not legal advice.

## Summary

- **Regimes in scope:** Australia, through a NSW public sector agency client and NSW applicants (docs/discovery/enquiries.md §1, §3); counsel: confirm the screen.
- **Main obligations in Australia:** the agency's own handling runs under the PPIP and HRIP Acts (IPPs, s 19(2) for recipients outside NSW, HPP 14, Part 6A breach notification); the agency registers the use case on the AIAF Platform under DCS-2026-02, mandatory since 30 September 2026 (checked 2026-10-26, source: adk-governance-pack reference australia.md, read 2026-10-26); the contract's ICTA clause 6.11 model-change notice conflicts with the pinned model's retirement (D1, `docs/contract/order-form-summary.md`).
- **Proposed roles:** the agency is the public sector agency; Southgate Labs is a contracted service provider under a State contract; Google Cloud is a subcontractor (Roles below; counsel: confirm).
- **Direct question: does the six-month model-change notice fit the pinned model?** Proposed answer, counsel: no. D1 records retirement of `gemini-3.5-flash-001` on 2027-02-26 (model page read 2026-10-20; not re-read on 2026-10-28, no web access). Six months before that date was 2026-08-26, which is before the Order Form was signed on 2026-09-08 (`docs/contract/order-form-summary.md`). Even a notice given on 2026-10-28 would run to 2027-04-28, after retirement. The contract term runs to 2027-09-14, so the pilot and any production period will need a different model inside the term. Options for counsel and the agency: written agreement to a shorter notice or approval of a named replacement model now (W7), or an Order Form variation.
- **Blocking questions:** counsel: 10 questions, listed under Questions for counsel.

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes | NSW agency client (docs/discovery/enquiries.md §1); NSW licence applicants (§3); Southgate staff in Sydney and Brisbane see transcripts and logs (D5) | Client establishment and data subjects; the consultancy's own handling; counsel: whether s 7B(5) covers every act |
| United States | no | Applicants for NSW trade licences (docs/discovery/enquiries.md §3); no US client | n/a: no US client, data subjects or purpose; assumption: visitors from the US are incidental; counsel: confirm |
| EU | no | NSW applicants only (docs/discovery/enquiries.md §3); the chat sits on the Office's licensing pages (§6) | n/a: no offer to, or monitoring of, people in the EU; assumption: incidental visitors only; counsel: confirm |
| United Kingdom | no | As for the EU; the client is not UK government (docs/discovery/enquiries.md §1) | n/a: no UK establishment or offer to people in the UK; assumption: incidental visitors only; counsel: confirm |
| New Zealand | no | No New Zealand client; applicants are NSW licence applicants (docs/discovery/enquiries.md §3) | n/a: no New Zealand data held or accessed on the record; assumption: none; counsel: confirm |
| Singapore | no | No Singapore client or data subjects on the record (docs/discovery/enquiries.md §3) | n/a: none; assumption: none |
| Canada | no | No Canadian client or data subjects on the record (docs/discovery/enquiries.md §3) | n/a: none; assumption: none |

- **Processing locations:** hosting, Firestore and logs in australia-southeast1, Sydney (D2); the model endpoint is in australia-southeast1 (D1), but the model's processing region is not recorded: gap: the model page's processing region, to be read by adk-model-and-output-contracts; abuse-monitoring processing location not recorded (D4); Southgate support access from Sydney and Brisbane (D5). Order Form item 14 says Australia (`docs/contract/order-form-summary.md`).
- **Government client:** NSW public sector agency, an executive agency (docs/discovery/enquiries.md §1), so DCS-2026-02 applies (checked 2026-10-26, source: adk-governance-pack reference australia.md, read 2026-10-26).

## System and intended purpose

- **What it does:** answers licensing enquiries from the Office's published guidance with a link, and gives a caller their application's status (R1, R2).
- **Who uses it and who it affects:** members of the public on the "Apply for a licence" pages; applicants for trade licences whose status is looked up (docs/discovery/enquiries.md §3, §6).
- **What the model decides and what code decides:** the model drafts answers; an output validator requires a guidance citation (C1); the lookup tool, not the model, matches number and date of birth (C2) and counts failures (C3).
- **Effects it can cause:** reads guidance and the licensing system; creates a handover to the contact-centre queue (C4); it cannot decide or change applications (docs/architecture/enquiries.md Scope gate, out of scope).
- **Human review of decisions about people:** n/a: it makes no decision about a person; the status read-out is a lookup (C2, M2).

## Roles

- **Facts:** the Office commissions and runs it under its name and sets its purpose (docs/discovery/enquiries.md §1, §5); Southgate Labs builds and supports it (D5, D6); Google Cloud hosts and supplies the model as a subcontractor (`docs/contract/order-form-summary.md`, D1, D2).
- **Australia, Privacy Act:** the consultancy's acts for the State contract are proposed to fall outside the APPs under s 7B(5); its other handling, such as reuse of transcripts for its own purposes, stays under the APPs (source: adk-governance-pack reference australia.md, read 2026-10-26); counsel: does s 7B(5) cover support access and abuse-monitoring flows (D4, D5); gap: the contract's privacy schedule is not in the record.
- **NSW, PPIP Act:** the Act binds the agency, and binds the contractor only if the contract says so (source: adk-governance-pack reference australia.md, read 2026-10-26); gap: contract terms on IPP compliance, breach notice and flow-down are not in `docs/contract/order-form-summary.md`; counsel: confirm.
- **NSW, HRIP Act:** transcripts may hold health information typed by callers (docs/discovery/enquiries.md §3), so the HRIP Act can bind Southgate directly (source: adk-governance-pack reference australia.md, read 2026-10-26); counsel: is Southgate an organisation bound in its own right.

## Australia: Privacy Act and APPs

- **No AI-specific regime:** Australia has no AI Act (checked 2026-10-26, source: adk-governance-pack reference australia.md, read 2026-10-26).
- **APPs engaged:** only for the consultancy's handling outside s 7B(5); the agency's own handling is under the IPPs in privacy-impact-input-pack.md; counsel: which of Southgate's acts, if any, fall outside s 7B(5) (D5, D3).
- **Overseas disclosure (APP 8, s 16C):** n/a: all recorded processing is in Australia (D2, `docs/contract/order-form-summary.md`); gap: the model's processing region and abuse-monitoring location (D1, D4) could be outside Australia; counsel: use or disclosure if they are.
- **Notifiable data breaches:** the Commonwealth scheme is said not to apply to State-contract acts (source: adk-governance-pack reference australia.md, read 2026-10-26); the agency's Part 6A duties are in security-questionnaire.md; counsel: which entity notifies.

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| n/a: no decision about a person; the agent reads status and cannot decide or change an application | n/a: not a decision | n/a: no decision to review; handover on request (C4) | n/a | application number, date of birth, stage, missing documents (docs/discovery/enquiries.md §3) | R2, C2, M2; counsel: confirm that guidance answers and status read-outs do not significantly affect rights or interests |

- **Privacy policy inputs (APP 1.8):** system-card.md, Automated-decision disclosure (C2).

## Australia: Sector, state and government AI policy

- **Sector laws:** health information in free text is screened under the HRIP Act (privacy-impact-input-pack.md); Australian Consumer Law n/a: a government licensing service gives no consumer offer (docs/discovery/enquiries.md §1); counsel: confirm. Workplace Surveillance Act n/a: the users are the public, not agency staff (R1, R2); counsel: confirm that Southgate staff reading transcripts is not surveillance of agency staff.
- **Government AI policy:** DCS-2026-02 and the NSW AI Operational Policy v1.1 (checked 2026-10-26, source: adk-governance-pack reference australia.md, read 2026-10-26); the Operational Policy is not mandatory for suppliers, so the agency registers the use case.

## Australia: Government client (Commonwealth or NSW agency)

- **Client and policy:** NSW agency under DCS-2026-02 and the NSW AI Operational Policy v1.1 (docs/discovery/enquiries.md §1; checked 2026-10-26, source: adk-governance-pack reference au-government-crosswalks.md, read 2026-10-26). The Accountable Official is also the sponsor and decider (docs/discovery/enquiries.md §5); agency: confirm that is intended.
- **Official forms and where the pack's answers are:** `government-form-answers-nsw-aiaf-registration.md` and `government-form-answers-nsw-aiaf-assessment.md`; the IPC AI PIA guide rows are in privacy-impact-input-pack.md; agency: the Accountable Owner and assessing officers complete them (W5).
- **Review committee:** NSW AI Review Committee referral within 5 business days of completing the AIAF applies if the band is high or critical (checked 2026-10-26); agency: sets the band, with a proposal in impact-assessment.md; counsel: referral needed; wait W6, conditional.
- **Privacy Act roles:** the consultancy's acts for a State contract fall under s 7B(5), its other handling stays under the APPs; counsel: does s 7B(5) cover every act (D5, D4).
- **NSW privacy:** IPPs and s 19(2) apply to any recipient outside NSW, including another Australian state (checked 2026-10-26); Brisbane support access with transcripts and logs (D5) is outside NSW, and so may be abuse-monitoring storage (D4) and the model's processing (D1, gap); HRIP Act and HPP 14 for health information in transcripts; Part 6A for eligible data breaches (privacy-impact-input-pack.md); counsel: use or disclosure and which s 19(2) ground.
- **NSW access and records:** the contract, valued at $420,000 including GST, is over the $150,000 threshold for the agency's GIPA contracts register (`docs/contract/order-form-summary.md`; checked 2026-10-26); agency: register entry; counsel: whether GIPA s 121 applies to a public-facing service run for the agency. Transcripts, prompts and outputs are State records; gap: no export of transcripts, model ID and timestamps to the agency's recordkeeping system is recorded (D3), and the 90-day deletion (D3) must fit the agency's disposal authority (agency: the records manager, W4).
- **NSW security:** NSW Cyber Security Policy, Essential Eight Maturity Level One baseline and 24-hour cyber incident reporting (checked 2026-10-26); security-questionnaire.md; the design's baseline table lists only SB01, SB03 and SB05 (docs/architecture/enquiries.md Security baseline); CISO assessment W2.
- **NSW contract AI clauses:** the AI module is selected and clause 6.11 is at the default (`docs/contract/order-form-summary.md`). By default that means six months' notice of a change to the underlying model and Customer Data kept in NSW unless the Order Form permits otherwise (checked 2026-10-26, source: adk-governance-pack reference australia.md, read 2026-10-26). Gaps: the summary does not list the model IDs the Order Form names as AI systems; Order Form item 14 says Australia, not NSW, so Brisbane access needs the agency's view. Retirement of the pinned model on 2027-02-26 (D1, model page read 2026-10-20, not re-read) falls inside any six-month notice window; gap for adk-model-and-output-contracts and adk-release-engineering; counsel: the notice period and the Order Form terms (W7).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| Australia, NSW | DCS-2026-02, AIAF Platform for registering and assessing AI use cases | 30 September 2026 (checked 2026-10-26) | The agency registers before the 2026-12-10 pilot decision (W5) |
| Australia, NSW | First annual AI attestation by the agency | 31 October 2027 (checked 2026-10-26) | After the contract term ends 2027-09-14 (`docs/contract/order-form-summary.md`); agency: owner |
| Australia, NSW | PPIP Act Part 6A mandatory data breach notification | 28 November 2023 (checked 2026-10-26) | The agency's breach policy and register cover this service (security-questionnaire.md) |
| Australia | APP 1.7 to 1.9 automated-decision privacy-policy entries | 10 December 2026 (checked 2026-10-26) | n/a: no decision about a person (C2); same day as the pilot decision (docs/discovery/enquiries.md §6) |
| Contract | Pinned model retirement | 2027-02-26 (D1, model page read 2026-10-20, not re-read) | Inside the six-month model-change notice window; W7 |

- **AI literacy and staff training:** the Operational Policy asks agencies to offer AI training; gap: no training goal for contact-centre staff in the plan; proposed goal for adk-presenter's rollout pack.
- **Documents the client's own process produces:** AIAF registration and assessment (agency: Accountable Owner, W5); AI Review Committee referral if high or critical (W6); the agency's PIA under the IPC guide (agency: privacy officer, W4); privacy management plan update (agency, W4); Part 6A breach policy and register entry (agency, W2); GIPA contracts register entry (agency); Digital Assurance Framework gateway n/a: the $420,000 value is below the $5 million trigger (`docs/contract/order-form-summary.md`) unless Digital Restart Fund money funds it (agency: confirm).

## Questions for counsel

- counsel: does the six-month model-change notice in clause 6.11 apply to the replacement of `gemini-3.5-flash-001` retiring 2027-02-26, can it be waived or shortened, and does the Order Form list the model; regime Australia, NSW; facts at D1 and `docs/contract/order-form-summary.md`; needed before W7 and the 2026-12-10 pilot decision.
- counsel: is the model's processing region, and Google's abuse-monitoring processing (D4), outside NSW or Australia, and is that a use or a disclosure under s 19(2); needed before W3.
- counsel: is Brisbane support access to transcripts and logs (D5) a use or a disclosure outside NSW, and does Order Form item 14 (Australia) permit it; needed before W3.
- counsel: does s 7B(5) cover every act Southgate does, including support access and abuse-monitoring flows; needed before W3.
- counsel: is Southgate bound by the HRIP Act in its own right, and is HPP 14 met for health information in transcripts; needed before W3.
- counsel: does the Order Form give the agency IPP-compliant handling, breach notice and flow-down to Google (the IPC reasonable-steps minimum); gap: the contract text is not in the record; needed before W3.
- counsel: does the agency hold, under s 59C, data in Southgate's environments, and who notifies a Part 6A breach; needed before W2.
- counsel: does GIPA s 121 apply to a service for the public run on the agency's behalf; needed before W3.
- counsel: which AIAF band applies and is an AI Review Committee referral needed; needed before W5 and W6.
- counsel: does a guidance answer or status read-out ever feed an administrative decision under an Act; facts at R1, R2, C2; needed before W3.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Accountable Official for AI (Ruth Abbott) | this document | pending | pending |
| Agency counsel | this document, every counsel: item | pending | pending |
