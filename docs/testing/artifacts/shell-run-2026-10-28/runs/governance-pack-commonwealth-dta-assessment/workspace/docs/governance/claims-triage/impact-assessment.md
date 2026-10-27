---
document: impact-assessment
system: Claims triage assistant (Compensation Claims Office)
version: design accepted 2026-09-19, build v0.6.3
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: CCO AI accountable official (Helen Park)
trigger: pilot decision on 2026-12-08 and the DTA AI impact assessment
sources: docs/discovery/claims-triage.md, docs/architecture/claims-triage.md, docs/plans/claims-triage.md, regulatory-memo.md
---

# AI system impact assessment: Claims triage assistant

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 and mapped to NIST AI RMF 1.0 and NIST AI 600-1. Draft for the CCO's risk owner; scores are provisional until they set them. Not legal advice.

## Scope and intended use

- **System and functions:** drafts category, priority and missing evidence for a new claim; the model drafts, code scopes access and validates citations, an officer decides (R1, R2, R3, R4, C1, C2, C3, C4).
- **Intended use:** triage of new claims by officers in a pilot (R1; docs/discovery/claims-triage.md §6); **unintended or foreseeable misuse:** using the draft to determine liability or payment, or to contact claimants, both out of scope (docs/architecture/claims-triage.md Scope gate); officers accepting drafts without reading the notes (docs/discovery/claims-triage.md §4; control C2 only shows the passages).
- **Organisation's role:** the CCO is deployer; Southgate Labs developer; Google model and cloud provider (regulatory-memo.md Roles; counsel: confirm).
- **Lifecycle stage and trigger:** pilot design, evaluated offline (G04, M1, M2); the pilot decision is on 2026-12-08 (docs/discovery/claims-triage.md §6).

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| Claims officers (20 in the pilot) | Use the draft; accountable for the decision | no; training gap: none recorded | docs/discovery/claims-triage.md §6 |
| Claimants | Speed and routing of their claim; their health information is processed | yes: injured people, mental-health history and family violence disclosures (docs/discovery/claims-triage.md §3); accessibility needs not recorded | docs/discovery/claims-triage.md §3, §4 |
| CCO executive and AI accountable official | Decide the pilot; accountable | no | docs/discovery/claims-triage.md §5 |
| Privacy Officer and Chief Security Officer | Review privacy and security | no | docs/discovery/claims-triage.md §5 |
| Southgate Labs and Google | Build, support and host | no | D1, D4 |
| Unions, claimant representatives, other stakeholders | Not consulted on the record | gap: agency: consultation not recorded | docs/discovery/claims-triage.md §5 |

## System information

- **Data:** claim form and notes, medical reports from the case system; 900 past claims with officer decisions, names and identifiers removed, for evaluation (docs/discovery/claims-triage.md §3; D5).
- **Model and logic:** Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` (D1); retirement date: gap: not read from the lifecycle page (no network); citation validator and team scoping are deterministic (C1, C2).
- **Deployment environment:** Cloud Run and Cloud SQL in australia-southeast1, assessed against PROTECTED by the CCO's security team (D2); officer sign-in through the CCO's identity provider (docs/architecture/claims-triage.md Scope gate); IRAP assessment W1; support from Sydney (D4).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | Claimants | harm | Wrong low priority delays payment to an injured person | assumption: medium; priority agreement is 79% offline | assumption: high; payment delay for an injured person | docs/discovery/claims-triage.md §4, M2 |
| H2 | Claimants | harm | Wrong category routes a claim to the wrong team and adds weeks | assumption: medium; category agreement 88% offline | assumption: medium | docs/discovery/claims-triage.md §4, M1 |
| H3 | Claimants | harm | Officers rely on the draft without reading the notes | assumption: medium; no review-depth measure | assumption: high | docs/discovery/claims-triage.md §4 |
| H4 | Claimants | harm | Sensitive information exposed through prompts, logs, staff access or a provider | assumption: low to medium; no screening evidence | assumption: high | D3, D4 |
| H5 | Claimants | harm | Unfair or discriminatory triage for groups (for example mental-health claims, people with limited English) | assumption: unknown; not measured | assumption: high | gap: no group-level measure exists |
| H6 | CCO | harm | Public confidence loss if AI use in claims handling is not disclosed | assumption: medium | assumption: medium | gap: agency: risk appetite not recorded |
| B1 | CCO and claimants | benefit | Shorter time from lodgement to triage decision (median 6 working days at baseline) | hypothesis: no pilot figure yet | n/a: benefit | docs/discovery/claims-triage.md §2 |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1, H2 | Officer accepts or changes every draft; drafts cite claim passages or are withheld; decisions recorded | in place, tested locally | R4, C2, C4, G01/A2, G03/A1 |
| H1 | Test for under-prioritising errors separately from overall agreement | gap: only overall agreement is reported (M2); goal for adk-agent-evaluation | M2 |
| H3 | Show passages; measure change rate against the baseline 11% and review time in the pilot | planned: gap: no goal yet; propose a goal for adk-agent-evaluation | R2, docs/discovery/claims-triage.md §2 |
| H4 | Team-scoped, read-only access; hosting in Australia; logs kept 30 days | in place, tested locally (C1, C3); logs D3; screening gap: goal for protect-adk-sensitive-data | C1, C3, D2, D3 |
| H4 | Environment assessment against PROTECTED | planned: W1 | D2, W1 |
| H5 | Group-level agreement and change rates | gap: no measure; goal for adk-agent-evaluation | M1, M2 |
| H6 | Transparency statement and notice to claimants | planned: agency: W3, W5 | W3, W5 |
| All | ADK runtime hardening | deferred: production | SB05 |

## Residual risk and decision

- H1 and H3 remain material after the measures: the officer is the main control and its effectiveness is unmeasured (H1, H3, C4). H4 is unresolved until screening and provider facts exist (H4). H5 is unmeasured (H5).
- **Accepted by:** gap: acceptance by the CCO's Assistant Secretary (the decider, docs/discovery/claims-triage.md §5) is not recorded; no residual rating is proposed in this draft beyond the provisional scores above.
- **Conditions that end acceptance:** a pilot override rate or review-time result that shows officers are not reviewing; a priority agreement below the agreed threshold (gap: no threshold set; M2 is 79%); any incident (C4, M2).

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | Accountable official, privacy officer and security officer named; AI literacy and training gap | docs/discovery/claims-triage.md §5; gap: training |
| Map | Scope, parties, Australia as the only regime, APP 1.7 question | regulatory-memo.md; R1 |
| Measure | Offline agreement 88% category and 79% priority; unmeasured: fairness, review depth, pilot override | M1, M2; gap: no evaluation report path is recorded in the plan |
| Manage | Measures above; incidents: none recorded; monitoring planned | C1, C2, C3, C4; gap: no incident records I |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| Confabulation | yes | Cited passages or the draft is withheld; hallucination rate not measured separately | C2, M1 |
| Data privacy | yes | Team scope, read-only, hosting in Australia; screening gap | C1, C3, D2 |
| Harmful bias or homogenisation | yes | No group measures; gap | gap: H5 |
| Human-AI configuration | yes | Officer decides every draft; automation bias not measured | R4, C4 |
| Information security | yes | SB01 and SB03 built; adversarial testing not recorded; ADK runtime deferred | SB01, SB03, SB05 |
| Value chain and component integration | yes | Single pinned model; provider facts gap | D1 |
| CBRN, dangerous or violent content, obscene or abusive content, intellectual property, information integrity, environmental impacts | n/a: internal officer tool on claim text, no public generation of such content; not assessed in detail (assumption: low relevance) | assumption: scope of the use case | R1 |

## Monitoring and review

- Watch in the pilot: share of drafts changed by officers against the baseline 11%, time to triage against the baseline 6 working days (docs/discovery/claims-triage.md §2); owner and thresholds: gap: not set.
- **Review triggers:** a change of model (D1), a new user group, a new data type, an incident, a change in law or DTA guidance, and at least every 12 months if the inherent rating is high (DTA Policy v2.1, checked 2026-10-26).

## Adverse impact and equality (if the system ranks, scores or decides about people)

| Group or characteristic | Selection or outcome rate | Ratio to the highest group | Test and sample | Proxies removed | Evidence |
| --- | --- | --- | --- | --- | --- |
| Not measured | gap: none | gap: none | gap: 900 past claims exist (D5) but no group breakdown is reported | gap: not recorded | M1, M2 |

- **Less discriminatory alternatives considered and accessibility route:** gap: none recorded; counsel: is any disparity justified; the Australian anti-discrimination Acts are screened as counsel questions, not described here.

## Australia: Guidance for AI Adoption mapping

n/a: the guidance is voluntary and for private clients; the CCO follows the DTA policy below (regulatory-memo.md).

## Australia: DTA AI impact assessment inputs (Commonwealth clients)

- **Threshold (DTA tool sections 1 to 4):** a triage assistant using sensitive health information and informing an administrative process (R1; docs/discovery/claims-triage.md §3). Proposed inherent risk: assumption: at least medium on privacy, because of health and family violence information, so the full assessment sections 5 to 12 follow; agency: sets the ratings; counsel: in scope under Appendix C.
- **Use-case owner, assessing and approving officers:** gap: not named (agency:). The AI accountable official is Helen Park (docs/discovery/claims-triage.md §5).
- **Transparency statement inputs:** usage pattern proposed as decision-making and administrative action, with workflow automation (assumption: agency: confirm the list); the public does not interact with the system; every output is reviewed by an officer (R4, C4); monitoring plan: gap (system-card.md).
- **Agentic AI addendum (AGT.1 to AGT.8):** the design has bounded tools, a read-only account and no write actions (C1, C3); memory scope, kill switch, adversarial evaluation and monitoring are not recorded (gap); see government-form-answers-dta-agentic-addendum.md.
- **Draft form answers:** government-form-answers-dta-impact-assessment.md, government-form-answers-dta-transparency-statement.md, government-form-answers-dta-use-case-register.md and government-form-answers-dta-agentic-addendum.md (agency: the assessing and approving officers complete and approve in the official tool; W3).

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| CCO AI accountable official (Helen Park) | this document | pending | pending |
