---
document: impact-assessment
system: HR assistant (Érable Logistics)
version: design accepted 2026-09-11, build v0.5.0
status: draft
jurisdictions: [au, ca]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Luc Tremblay, Vice-President, People, Érable Logistics Inc. (risk owner and decider)
trigger: pilot decision on 2026-11-24
sources: docs/discovery/hr-assistant.md, docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md, docs/governance/hr-assistant/regulatory-memo.md
---

# AI system impact assessment: HR assistant (Érable Logistics)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 and mapped to NIST AI RMF 1.0 and NIST AI 600-1 (source: adk-governance-pack reference impact-assessment.md, read 2026-10-28). Draft for Érable's risk owner; scores are provisional until they set them (counsel: legal conclusions stay with Me Roy). Not legal advice.

## Scope and intended use

- **System and functions:** answers HR policy questions in French and English, takes leave requests into UKG, auto-approves routine ones by a rule and routes the rest to the manager (R1 to R4, C3, C5). The model extracts dates and leave type only; the rule decides (D5).
- **Intended use:** staff HR questions and routine leave requests under two days at the Montréal and Toronto centres (docs/discovery/hr-assistant.md §2). **Foreseeable misuse:** an employee asking for another employee's data (C2); splitting a long leave into requests under two days to avoid manager review (assumption: possible; gap: no control recorded against repeated requests); pasting health details into a prompt (gap: no screening recorded).
- **Organisation's role:** Érable is the deployer and the organisation responsible for the information; Southgate Labs built it (regulatory memo Roles; counsel: confirm).
- **Lifecycle stage and trigger:** pilot, one shift per centre for 6 weeks, decision 2026-11-24 (docs/discovery/hr-assistant.md §6; G05).

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| Distribution-centre staff, Montréal (1,150) and Toronto (640) | use the assistant; their leave decisions and data are processed | yes in part: employees depend on their employer for pay and attendance records; assumption: no minors | docs/discovery/hr-assistant.md §1 |
| Managers | receive non-routine requests | no | R4, C5 |
| HR (about 2,300 questions and 900 leave requests a month today) | receive handovers and complaints | no | docs/discovery/hr-assistant.md §1, C1 |
| Montréal Teamsters local | represents Montréal staff under a collective agreement | assumption: has consultation rights; counsel: what the agreement requires (wait W5) | docs/discovery/hr-assistant.md §5 |
| Southgate Labs engineers | read logs from Sydney | no | D4 |

## System information

- **Data:** UKG profile and leave balances, leave requests and reasons that may mention health or family matters, HR policies in French and English, prompts and answers logged with employee ID (docs/discovery/hr-assistant.md §3, D3).
- **Model and logic:** `gemini-3.5-flash-001` for extraction and policy answers; a deterministic rule for approval (D1, D5, C3). gap: retirement date and current processing region not re-read.
- **Deployment environment:** Cloud Run and Cloud SQL in Toronto, Gemini through the global endpoint with US processing, Sydney engineers reading logs (D1, D2, D4). Operated by Southgate during the pilot and a three-month support period (D4).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | staff | harm | a wrong approval or an extraction error enters pay, scheduling and attendance records | assumption: low; 1.6% extraction errors in replay | assumption: moderate | docs/discovery/hr-assistant.md §4, M3 |
| H2 | staff | harm | an employee does not know a decision was made without a person and cannot ask for review | assumption: high without a notice | assumption: moderate | docs/discovery/hr-assistant.md §4, C4 |
| H3 | staff | harm | leave reasons with health or family details reach Gemini in the US and logs read in Sydney | assumption: moderate | assumption: high | D1, D3, D4 |
| H4 | staff | harm | the assistant approves less often, or extracts less accurately, for one language group or site | assumption: unknown; gap: no bias measure | assumption: moderate | M1, M3 |
| H5 | staff | harm | a policy answer cites the wrong section and misleads | assumption: moderate (8% in evaluation) | assumption: moderate | C1, M1 |
| B1 | staff, HR | benefit | faster decisions than the 31-hour median | hypothesis: the rule approves 64% of pilot-shape requests (M2) so a large share could be decided in seconds | n/a: benefit | hypothesis: docs/discovery/hr-assistant.md §2, M2 |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1 | rule conditions in code before the UKG write; non-routine requests to the manager | in place, tested locally | C3, C5 |
| H1 | employee confirms extracted dates before submission | gap: not in the contracts | C3 |
| H2 | s 12.1 notice, explanation and a route to a staff member | gap: proposed goal for adk-operational-guardrails | C4 |
| H2 | counter-metric: decisions reversed after complaint, baseline 1.2% | planned: pilot measure not yet defined (gap) | docs/discovery/hr-assistant.md §2 |
| H3 | employee-scoped tools; no screening or pseudonymisation | in place for scoping (C2); gap for screening, proposed goal for protect-adk-sensitive-data | C2, SB01 |
| H4 | none | gap: proposed goal for adk-agent-evaluation | M3 |
| H5 | every answer cites a policy section; handover to HR | in place, tested locally | C1, M1 |

## Residual risk and decision

- H2 and H3 remain high without the gaps above; H1 and H5 remain low to moderate (H1, H2, H3, H5, C1, C3).
- **Accepted by:** gap: acceptance by Luc Tremblay, the decider, not recorded; pending until the counsel questions are answered.
- **Conditions that end acceptance:** a reversal rate after complaint above the 1.2% baseline (docs/discovery/hr-assistant.md §2); a model change or retirement; a new leave type or a leave of two days or more entering scope (docs/architecture/hr-assistant.md Scope gate).

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | decider Luc Tremblay; person in charge Marie-Claude Gagnon; counsel Me Roy; no named incident owner (gap) | docs/discovery/hr-assistant.md §5 |
| Map | scope, parties, regimes: Quebec and Ontario, with Australia for the consultancy | regulatory-memo.md, D1, D2, D4 |
| Measure | M1 92% right section, M2 64% auto-approved, M3 98.4% extraction; not measured: bias, review share, pilot overrides | M1, M2, M3 |
| Manage | C1 to C5 contracts; no incident record yet; kill switch not recorded (gap) | C1, C5 |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| Confabulation | yes | answers cite the policy section; 92% right (M1); action IDs not mapped (gap) | C1, M1 |
| CBRN information | n/a: HR assistant with no such topic or tools | n/a | R1 |
| Dangerous, violent or hateful content | n/a: policy answers from published HR policies only | n/a | R1 |
| Data privacy | yes | employee scoping; screening and pseudonymisation are gaps | C2, D3 |
| Environmental impacts | n/a: not assessed for a pilot of one shift per centre (assumption) | n/a | docs/discovery/hr-assistant.md §6 |
| Harmful bias or homogenisation | yes | not measured (gap) | M3 |
| Human-AI configuration | yes | no human review of auto-approvals (C4); manager review for the rest | C4, C5 |
| Information integrity | yes | answers from published policies only; no disinformation use | C1 |
| Information security | yes | SB01 and SB03 at Build depth, SB05 deferred; no red-team result recorded (gap) | SB01, SB03, SB05 |
| Intellectual property | n/a: answers draw on Érable's own policies | n/a | R1 |
| Obscene, degrading or abusive content | n/a: no generation of such content is a design purpose | n/a | R1 |
| Value chain and component integration | yes | Google model and UKG integration; model retirement date unknown (gap) | D1, W1 |

## Monitoring and review

- Watch during the pilot: reversal rate after complaint against the 1.2% baseline, share of requests auto-approved against 64% in replay, citation accuracy against 92% (owner: Southgate Labs with Érable HR; gap: no thresholds or owner agreed) (M1, M2, docs/discovery/hr-assistant.md §2).
- **Review triggers:** model change or retirement, a new user group or data, an incident, a change in Quebec or Ontario law or guidance (D1, G05).

## Adverse impact and equality (if the system ranks, scores or decides about people)

| Group or characteristic | Selection or outcome rate | Ratio to the highest group | Test and sample | Proxies removed | Evidence |
| --- | --- | --- | --- | --- | --- |
| language (French, English), site, leave type | gap: not measured; M1 sampled 150 French and 150 English questions but M3 does not record the language split | gap | gap | gap: none recorded | M1, M3 |

- **Less discriminatory alternatives considered and accessibility route:** none recorded; manager review is the alternative route for non-routine requests (C5; counsel: whether any disparity would be justified).
- **Regime checklists:** for Ontario, use the OHRC and Law Commission of Ontario Human Rights AI Impact Assessment (6 November 2024, checked 2026-10-26) as the adverse-impact checklist (gap: not completed); counsel: Quebec's Charter of human rights is not covered by the references.

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Luc Tremblay, Vice-President, People, Érable Logistics Inc. | this document | pending | pending |
| Me Geneviève Roy, counsel, Érable Logistics Inc. | this document | pending | pending |
