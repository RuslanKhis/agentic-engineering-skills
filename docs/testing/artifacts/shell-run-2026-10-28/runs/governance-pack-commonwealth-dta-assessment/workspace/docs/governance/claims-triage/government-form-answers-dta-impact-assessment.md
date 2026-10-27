---
document: government-form-answers
system: Claims triage assistant (Compensation Claims Office)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CCO officer who completes the form (assessing officer or accountable use case owner; agency: to be named)
form: DTA AI impact assessment tool
form_version: v1.0, published 1 December 2025
form_url: https://www.digital.gov.au/ai/impact-assessment-tool
form_checked: 2026-10-26
sources: docs/discovery/claims-triage.md, docs/architecture/claims-triage.md, docs/plans/claims-triage.md, regulatory-memo.md, impact-assessment.md, privacy-impact-input-pack.md, system-card.md
---

# Draft answers for DTA AI impact assessment tool: Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

This is not the official form. It drafts answers, in the official form's own order, for the Compensation Claims Office's officers to check and paste into the official tool, where they complete, rate and approve the assessment. Each answer cites the project record, or says who must answer it: `agency:` for what only the agency can answer, `counsel:` for a legal question. Not legal advice.

## Form and version

- **Form:** DTA AI impact assessment tool v1.0, https://www.digital.gov.au/ai/impact-assessment-tool (checked 2026-10-26).
- **Crosswalk used:** references/au-government-crosswalks.md, verified 2026-10-26 (source: adk-governance-pack reference, read 2026-10-28).
- **Version match:** gap: official page not re-read in this session (no network); the version and date are the crosswalk's. Re-read the page and the Appendix D v2.1 usage-pattern list before the officers paste (the form lists four patterns, the policy seven; agency: which list the CCO's copy uses).
- **Rating basis the form uses:** DTA: inherent risk at section 3, residual at section 12 (assumption: every rating below is a proposal, inherent unless marked residual).

## Who completes and approves

| Role in the form | Who | Evidence |
| --- | --- | --- |
| Assessing officer | agency: name and position once the agency names them | gap: not named |
| Approving officer | agency: name and position | gap: not named |
| Accountable use case owner | agency: AI accountable official is Helen Park (docs/discovery/claims-triage.md §5); confirm whether she is the owner | docs/discovery/claims-triage.md §5 |
| External suppliers with responsibilities | Southgate Labs as developer and supporter; Google as model and cloud provider | regulatory-memo.md Roles; D1, D4 |

## Draft answers

| # | Question (paraphrase) | Draft answer | Evidence | Who decides |
| --- | --- | --- | --- | --- |
| 1.1 | Use case name, reference, lead agency | Claims triage assistant; lead agency Compensation Claims Office; reference: agency: | README.md | agency: |
| 1.2 | Officers | agency: all three names | gap: not named | agency: |
| 1.3 | Others with responsibilities | Southgate Labs (developer, pilot support from Sydney); Google (model and cloud provider) | D1, D4 | the record |
| 1.4 | Plain-language description | Reads a new claim and drafts a category, priority and list of missing evidence that a claims officer accepts or changes | R1, R4, system-card.md | the record |
| 1.5 | Which in-scope criteria apply | Uses personal and sensitive data; informs an administrative process; no public interaction. Proposed: in scope | docs/discovery/claims-triage.md §3, §4 | counsel: in scope; agency: DTA direction |
| 1.6 | Type of AI technology | Generative language model, Gemini 3.5 Flash pinned as `gemini-3.5-flash-001`, via Vertex AI | D1 | the record |
| 1.7 | Usage pattern | Proposed: decision-making and administrative action; workflow automation | R1, R4 | agency: which list and pattern |
| 1.8 | Legislative authority for automating an administrative decision | Facts: the officer decides; the assistant only drafts and writes nothing to the case system | R4, C3, C4 | counsel: always; agency: governing Act |
| 1.9 | Domain | Compensation claims for injured former Commonwealth contractors | docs/discovery/claims-triage.md §1 | agency: confirms |
| 1.10 | Expert contributions | Privacy officer and Chief Security Officer named as stakeholders; IRAP assessor | docs/discovery/claims-triage.md §5, W1 | agency: |
| 1.11 | Review log | First assessment; re-validate on a material change including model change | D1 | agency: |
| 2.1 | Problem | 6 working days median from lodgement to triage decision; 1,900 new claims a month | docs/discovery/claims-triage.md §1, §2 | the record |
| 2.2 | Purpose and how AI addresses it | Draft triage to shorten time to triage while officers decide | R1, docs/discovery/claims-triage.md §2 | the record |
| 2.3 | Non-AI alternatives | gap: no non-AI alternative recorded as considered; baseline is unaided officer triage | docs/discovery/claims-triage.md §2 | agency: |
| 2.4 | Stakeholders | Officers, claimants, privacy and security officers; claimant representatives and unions not consulted on the record | docs/discovery/claims-triage.md §5; gap: consultation | agency: |
| 2.5 | Expected benefits with analysis | hypothesis: shorter time to triage; no pilot figure yet; counter-metric share of decisions changed, baseline 11% | docs/discovery/claims-triage.md §2 | agency: |
| 3.1 | Accessibility and inclusion | Not applicable to claimants directly (staff tool); languages and accessibility of claim content not evaluated | gap: system-card.md Limits | assessing officer |
| 3.2 | Unfair discrimination | Proposed rating: assumption: medium, because group results are not measured; gap: no fairness measure | impact-assessment.md H5; M1, M2 | agency: sets rating |
| 3.3 | Stereotyping, demeaning content, defamation | assumption: low to medium; drafts about claimants with mental-health history could use stigmatising words; not tested | impact-assessment.md; C2 | agency: |
| 3.4 | Harm | Proposed rating: assumption: high consequence for H1 (delayed payment to an injured person), likelihood medium | docs/discovery/claims-triage.md §4, M2 | agency: |
| 3.5 | Privacy concerns | Proposed rating: assumption: high, health, mental-health and family violence information to a generative model | privacy-impact-input-pack.md; docs/discovery/claims-triage.md §3 | agency: sets rating; counsel: high privacy risk |
| 3.6 | Security, data aspects | Data in australia-southeast1, assessed against PROTECTED; classification: agency:; model provider data use gap | D2, security-questionnaire.md | agency: |
| 3.7 | Security, system aspects | Pretrained model pinned (D1); servers in Australia (D2); shutdown and monitoring gap: no kill switch or monitoring recorded | D1, D2 | agency: |
| 3.8 | Reputation and public confidence | assumption: medium; public disclosure and notice not yet settled | impact-assessment.md H6 | agency: risk appetite |
| 3.9 | Overall inherent rating | Computed from the proposals: assumption: high (3.4 and 3.5 rated high). If high, the use case is reported to the accountable official and reviewed at least every 12 months (checked 2026-10-26) | impact-assessment.md | agency: approves |
| 4.1 | Assessing officer's recommendation | Proposed: full assessment necessary (sections 5 to 12) | impact-assessment.md | agency: |
| 4.2 | Approving officer's review | agency: only; W3 | W3 | agency: |
| 5.1 | Definition of fairness | gap: none recorded; agency: the CCO's fairness policy | impact-assessment.md | agency: |
| 5.2 | Measuring fairness | gap: no group-level measure; goal for adk-agent-evaluation | M1, M2 | the record |
| 6.1 | Data suitability, permissions and rights | Past claims 2023 to 2026 de-identified for evaluation; permission to use claim data for AI: agency: | D5 | agency:; counsel: APP 6 |
| 6.2 | Indigenous data | gap: not assessed; claimants may include Indigenous Australians | docs/discovery/claims-triage.md §3 | agency: |
| 6.3 | Suitability of a procured model; contract terms | Gemini 3.5 Flash pinned; retirement date and provider data use gap; contract with Southgate Labs and Google: agency: and counsel: | D1, privacy-impact-input-pack.md | counsel: |
| 6.4 | Testing | Offline evaluation on 900 past claims: category 88%, priority 79%, build v0.6.3 | M1, M2, G04 | the record |
| 6.5 | Pilot | 20 officers, Canberra, 8 weeks, decision on 2026-12-08 | docs/discovery/claims-triage.md §6 | agency: |
| 6.6 | Monitoring plan | gap: share changed by officers and time to triage are the named measures; thresholds and owner not set | docs/discovery/claims-triage.md §2; impact-assessment.md Monitoring | agency: |
| 6.7 | Intervening or disengaging | Officer can change any draft (R4); gap: no kill switch recorded | R4, C4 | agency: |
| 6.8 | Operator training | gap: none recorded | system-card.md | agency: |
| 7.1 | APP compliance | See the APP compliance check | privacy-impact-input-pack.md | counsel: |
| 7.2 | Where the threshold assessment and PIA are stored | agency: ; the input pack is the PIA input | W2 | agency: |
| 7.3 | Security measures; IT Security Adviser | Team scoping, read-only account, hosting in Australia, IRAP booked 2026-11-16; ITSA review agency: | C1, C3, D2, W1, security-questionnaire.md | agency: |
| 8.1 | Stakeholder consultation | gap: none on the record | docs/discovery/claims-triage.md §5 | agency: |
| 8.2 | Public visibility | The CCO's transparency statement; agency: | government-form-answers-dta-transparency-statement.md | agency: |
| 8.3 | Documentation and records | System card, input pack, decision lineage recorded with each draft; records retention agency: | C4, system-card.md | agency: |
| 8.4 | Disclosing AI interactions; non-AI alternative | No conversation with claimants; notice that AI informs triage gap | system-card.md | agency: |
| 8.5 | Explanations of factors | Each draft field cites claim passages | R2, C2 | the record |
| 9.1 | Notification when AI materially influenced an administrative action | gap: no notice recorded; APP 1.7 from 10 December 2026 (checked 2026-10-26) | regulatory-memo.md | counsel: |
| 9.2 | Challenging AI-influenced actions | agency: internal and external review routes | system-card.md | agency: |
| 10.1 | Diversity across the lifecycle | gap: evaluation set composition not reported | D5 | agency: |
| 10.2 | Human rights alignment | counsel: always; facts: vulnerable claimants, health information | regulatory-memo.md | counsel: |
| 11.1 | Accountability mechanisms | AI accountable official Helen Park; privacy and security officers named; governance board and residual risk acceptance agency: | docs/discovery/claims-triage.md §5 | agency: |
| 12.1 | Agency-specific legislation | agency: the CCO's Act | regulatory-memo.md | agency: |
| 12.2 | Legal advice: needed, and where stored | agency: only; counsel questions are in the memo | regulatory-memo.md | agency: |
| 12.3 | Risk summary: treatments and residual risk | See impact-assessment.md Measures; H1 to H5 residual material, H4 and H5 open | impact-assessment.md | agency: |
| 12.4 | Overall residual rating | Proposed: assumption: high until officer review depth, screening and fairness are measured | impact-assessment.md | agency: sets |
| 12.5 | Internal governance body review (required if inherent risk is high) | agency: required if 3.9 is high; W3 | W3 | agency: |

## Questions for the agency

- agency: name the assessing officer, approving officer and accountable use case owner; needed by W3.
- agency: the CCO's enabling legislation, records disposal authority, information classification and risk appetite; needed by W3.
- agency: whether to refer to the Commonwealth AI Review Committee (sensitive health information; the committee advises on residual high risk or highly sensitive, novel or complex use cases, checked 2026-10-26); needed by W4.

## Questions for counsel

- counsel: legislative authority for the automated tool in triage (1.8); needed by W3.
- counsel: human rights alignment (10.2); needed by W3.
- counsel: APP compliance and use or disclosure for the Gemini endpoint (7.1); needed by W2.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO officer completing the form (agency: to be named) | this document | pending | pending |
