---
document: impact-assessment
system: <system name>
version: <build or design revision assessed>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk, nz, sg, ca>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <the reviewer who relies on it: counsel, DPO or privacy officer, CISO, risk owner>
trigger: <why this assessment now: design, production decision, significant change>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md, regulatory-memo.md>
---

# AI system impact assessment: <system name>

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 and mapped to NIST AI RMF
1.0 and NIST AI 600-1. Draft for <client>'s risk owner; scores are
provisional until they set them. Not legal advice.

<!-- The sections after "Monitoring and review" are optional: keep each one
whose condition holds and delete the rest, with this comment. -->

## Scope and intended use

- **System and functions:** <what it does; what the model decides; what code decides> (<C/D IDs>).
- **Intended use:** <workflow and users> (<R IDs>); **unintended or foreseeable misuse:** <uses> (<C/SB IDs or assumption:>).
- **Organisation's role:** <provider / deployer / both; agency's role> (regulatory memo, <D ID or counsel:>).
- **Lifecycle stage and trigger:** <stage; why now> (<goal ID>).

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| <users> | <direct use> | <yes / no, why> | <docs/discovery/<topic>.md §n or R ID> |
| <people the system's outputs are about> | <decisions, data> | <yes / no, why> | <R/C IDs> |

## System information

- **Data:** <sources, quality, provenance, personal data> (<data register, D IDs>).
- **Model and logic:** <pinned model and retirement date; deterministic parts> (<D IDs>).
- **Deployment environment:** <hosting, region, integrations, who operates it> (<D IDs>).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | <party> | harm | <what could happen> | <assumption: basis> | <assumption: basis> | <brief harm, I or M ID> |
| B1 | <party> | benefit | <measured or hypothesised benefit> | <measured / hypothesis> | <n/a:> | <M ID or hypothesis: brief §4> |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1 | <contract or rule that limits it> | <in place / planned G ID / deferred: trigger / gap:> | <C/SB IDs, G/A> |

## Residual risk and decision

- <what remains after the measures, per impact> (<H IDs, C IDs>).
- **Accepted by:** <role> on <date> (source: <who>, <YYYY-MM-DD>) / gap: acceptance by <role>.
- **Conditions that end acceptance:** <measure falls below threshold; new use> (<C ID>).

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | <roles, acceptance, literacy> | <IDs> |
| Map | <scope, parties, regimes and classification> | <IDs> |
| Measure | <evaluations and what is unmeasured> | <M IDs, reports> |
| Manage | <measures, incidents, monitoring> | <C/SB/I IDs> |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| Confabulation | <yes / n/a: reason> | <measure; action IDs such as MS-2.5-001> | <IDs> |
| Data privacy | <yes / n/a: reason> | <measure> | <IDs> |
| Harmful bias or homogenisation | <yes / n/a: reason> | <measure> | <IDs> |
| Human-AI configuration | <yes / n/a: reason> | <measure> | <IDs> |
| Information security | <yes / n/a: reason> | <measure; red-team results> | <IDs> |
| Value chain and component integration | <yes / n/a: reason> | <measure> | <IDs> |
| <each remaining risk of the twelve> | <yes / n/a: reason> | <measure> | <IDs> |

## Monitoring and review

- <measure watched in operation, owner and threshold> (<C/M IDs>).
- **Review triggers:** model change, new user group or data, incident, change in law or regulator guidance (<D/G IDs>).

## Adverse impact and equality (if the system ranks, scores or decides about people)

| Group or characteristic | Selection or outcome rate | Ratio to the highest group | Test and sample | Proxies removed | Evidence |
| --- | --- | --- | --- | --- | --- |
| <group> | <rate> | <ratio> | <test, n, window> | <postcode, name, age signals> | <M ID or gap:> |

- **Less discriminatory alternatives considered and accessibility route:** <what and why> (<D IDs>; counsel: <is any disparity justified?>).

## Australia: Guidance for AI Adoption mapping

| Practice | Content in this assessment | Evidence |
| --- | --- | --- |
| 1 Decide who is accountable | <owners across client, agency and model provider> | <IDs> |
| 2 Understand impacts and plan accordingly | <impacts, contestability> | <H IDs> |
| 3 Measure and manage risks | <measures> | <C/M IDs> |

## Australia: DTA AI impact assessment inputs (Commonwealth clients)

- **Threshold (DTA tool sections 1 to 4):** <use case, inherent risk facts> (<IDs>; counsel: <in scope under Appendix C?>).
- **Use-case owner, assessing and approving officers:** <names or roles> (source: <who>, <YYYY-MM-DD> / gap:).
- **Transparency statement inputs:** <usage pattern and domain, public interaction without human review, monitoring> (system-card.md; <IDs>).
- **Agentic AI addendum (AGT.1 to AGT.8):** <memory scope, bounded workflows and approvals, typed tools, adversarial evaluation, monitoring, kill switch, decommissioning> (<C/SB IDs>).
- **Draft form answers:** <the DTA tool, transparency statement and register answers, or the NSW AIAF registration and assessment answers, for the agency's officers> (government-form-answers-<form>.md; agency: <who completes and approves>).

## New Zealand: Responsible AI Guidance mapping and Māori impact

| Item | Content in this assessment | Evidence |
| --- | --- | --- |
| MBIE Responsible AI Guidance (private clients): inventory, PIA at design, security and jurisdictional risk, transparency | <content> | <IDs> |
| Algorithm Charter (signatory agencies): likelihood and impact rating, role of humans, contact point, appeal channel | <content, or n/a: not a signatory> | <IDs; agency:> |
| Māori impact and engagement: data about Māori, noa or tapu classification, offshore storage rationale, engagement owner | <content> | <IDs or gap:> |
| Senior leadership approval (OPC expectation) | <who and when> | <source: or gap:> |

## Singapore: Agentic MGF mapping

| Dimension (Model AI Governance Framework for Agentic AI v1.5) | Content in this assessment | Evidence |
| --- | --- | --- |
| 1 Assess and bound the risks up front (error tolerance, sensitive data and memory, external systems, write actions, reversibility, autonomy) | <content> | <D/C IDs> |
| 2 Make humans meaningfully accountable (value-chain roles, approval checkpoints, override rate and review time) | <content> | <C IDs, M IDs> |
| 3 Technical controls and processes (change management on model updates, pre-deployment testing, gradual roll-out) | <content> | <C/SB/G IDs> |
| 4 End-user responsibility (disclosure at the point of interaction, range of actions, escalation contacts) | <content> | <C IDs> |

- **Financial clients:** <MAS materiality inputs (impact, complexity, reliance), FEAT fairness definition and metrics, kill switch, independent review; or n/a: not MAS-regulated> (<IDs>).

## Canada: AIA inputs (federal clients)

- **Administrative decision and impact level:** <whether the output makes or informs an administrative decision; the proposed level as the department will score it> (<C IDs>; counsel: <decision?>; agency: <level and approver>).
- **Appendix C requirements as waits:** <peer review, notice, human involvement, explanation, approval to operate> (<W IDs or gap:>).
- **Ontario human rights checklist:** <the OHRC Human Rights AI Impact Assessment questions for an agent that screens or ranks people, or n/a:> (<M IDs>).

## EU: FRIA crosswalk (AI Act Article 27, if required)

| Article 27(1) | Pack section | Evidence |
| --- | --- | --- |
| (a) deployer's processes using the system | Scope and intended use; privacy-impact-input-pack.md Processing description | <IDs> |
| (b) period and frequency of use | privacy-impact-input-pack.md Processing description | <IDs> |
| (c) categories of persons and groups affected | Interested parties | <IDs> |
| (d) specific risks of harm | Impacts; privacy-impact-input-pack.md Risks and measures | <IDs> |
| (e) human oversight measures | system-card.md Human oversight | <IDs> |
| (f) measures if risks materialise, governance, complaints | Measures; Residual risk and decision | <IDs; counsel: required under Article 27?> |

## Review and sign-off

<!-- Only the reviewer fills Decision and Date. Leave both `pending` while
status is draft; the reviewer sets status: reviewed when they sign. One row
per reviewer: the role from `for:` first, then any other reviewer. -->

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| <the reviewer named in for:> | <this document, or the sections reviewed> | pending | pending |
