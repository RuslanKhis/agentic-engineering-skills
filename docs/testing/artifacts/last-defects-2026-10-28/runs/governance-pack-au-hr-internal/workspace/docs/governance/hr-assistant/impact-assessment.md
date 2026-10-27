---
document: impact-assessment
system: Staff HR assistant (Wattle & Co)
version: design accepted 2026-09-24; build v0.4.1 (M1 to M3)
status: draft
jurisdictions: [au]
counsel_required: yes
prepared: 2026-10-28 by Southgate Labs
for: Head of Security (Daniel Okoro) and Privacy Officer (Grace Nguyen)
trigger: pilot decision on 2026-11-27 (docs/discovery/hr-assistant.md §6)
sources: docs/discovery/hr-assistant.md, docs/architecture/hr-assistant.md, docs/plans/hr-assistant.md, regulatory-memo.md
---

# AI system impact assessment: Staff HR assistant (Wattle & Co)

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Structured along the topics of ISO/IEC 42005:2025 and mapped to NIST AI RMF
1.0 and NIST AI 600-1. Draft for Wattle & Co's risk owner; scores are
provisional until they set them. Not legal advice.

## Scope and intended use

- **System and functions:** answers leave, roster and policy questions and summarises a team member's attendance, reading Workday only (R1, R2, R4, C3).
- **Intended use:** staff self-service and manager team questions (R1, R2); **foreseeable misuse:** a manager treats a summary as a finding in a performance conversation, which the manager guide invites (D6, C5); staff type health, family or union details (docs/discovery/hr-assistant.md §4).
- **Organisation's role:** Wattle & Co deployer; Southgate Labs developer; Google model developer (regulatory memo, Roles; counsel: confirm).
- **Lifecycle stage and trigger:** pre-pilot; governance papers are goal G06 (ready), before the 2026-11-27 decision.

## Interested parties

| Party | How affected | Vulnerable? | Evidence |
| --- | --- | --- | --- |
| Staff using the assistant (300 in the pilot) | Direct use; their prompts are logged | assumption: some are casual or young retail staff with less power than a manager; not recorded | docs/discovery/hr-assistant.md §6, D3 |
| Managers (25 in the pilot) | Direct use; accountable for what they do with a summary | no | docs/discovery/hr-assistant.md §6, D6 |
| Team members who are summarised | Their attendance is summarised for a performance conversation and they do not use the tool | yes: an employment decision about them depends on a power imbalance | R2, D6 |
| SDA delegates and members | Union information may appear in prompts; consultation is required on major change | yes: union membership is sensitive information | docs/discovery/hr-assistant.md §4 and §5 |
| HR service centre | Ticket volume changes | no | docs/discovery/hr-assistant.md §2 |

## System information

- **Data:** Workday leave, roster and time data and typed prompts; free-text leave reasons can mention illness, family or union matters (docs/discovery/hr-assistant.md §3).
- **Model and logic:** Gemini 3.5 Flash pinned as `gemini-3.5-flash-001` (D1); gap: retirement date and processing region unread, propose adk-model-and-output-contracts check; deterministic parts are the scoping tools (C1, C2, C3) and the output schema (C5).
- **Deployment environment:** Cloud Run, Cloud SQL and logs in australia-southeast1 (D2); error bodies to Sentry in the US (D4); Southgate Labs engineers in Sydney (D5).

## Impacts

| ID | Party | Benefit or harm | Description | Likelihood (provisional) | Severity (provisional) | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | Staff | harm | A wrong leave balance leads to booking leave they do not have | assumption: 3% of 240 test questions were wrong (M1) | assumption: moderate | docs/discovery/hr-assistant.md §4, M1 |
| H2 | Team member | harm | A wrong or context-free attendance summary affects a performance conversation | assumption: 5% of 60 summaries did not match (M3) | assumption: high, employment effect | docs/discovery/hr-assistant.md §4, M3, C5 |
| H3 | Staff and union members | harm | Union or medical information reaches logs, Sentry in the US and engineers | assumption: 18% of 150 synthetic prompts were not masked (M2) | assumption: high | C4, M2, D3, D4, D5 |
| H4 | Team member | harm | Leave reasons reach a manager | gap: the tool's output fields are not recorded | assumption: high | docs/discovery/hr-assistant.md §3 |
| H5 | Staff | harm | Staff are monitored without notice or consultation | assumption: possible, not recorded | assumption: moderate | docs/discovery/hr-assistant.md §5, D3 |
| H6 | Staff | harm | Another person's records are read | assumption: low | assumption: high | C1, C2 |
| B1 | HR service centre and staff | benefit | Fewer tickets than 3,900 a month | hypothesis: not yet measured | n/a: benefit | docs/discovery/hr-assistant.md §2 |

## Measures

| Impact | Measure | Status | Evidence |
| --- | --- | --- | --- |
| H1 | Measured against Workday; counter-metric under 5% marked wrong | Measured locally (97%); the counter-metric is planned under G05 | M1, docs/discovery/hr-assistant.md §2 |
| H2 | Summary lists its source records | In place, tested locally; manager guidance and measured checking are gaps | C5, G03/A1, M3 |
| H3 | Masking before logging | Partially in place: 82% on synthetic prompts; planned under G04 (in_progress); gap: coverage of the Sentry path | C4, M2, D4 |
| H4 | None recorded | gap: propose adk-model-and-output-contracts goal to confirm and restrict the summary schema | C5 |
| H5 | None recorded | gap: notice (W3) and consultation (W4) | W3, W4 |
| H6 | Verified employee ID and supervisory organisation check | In place, tested locally | C1, C2, G02/A2, G02/A3 |

## Residual risk and decision

- H2 and H3 stay high until masking, the Sentry path and manager guidance are fixed (M2, M3, D4, D6).
- **Accepted by:** gap: acceptance by Marcus Bell, who decides the pilot (docs/discovery/hr-assistant.md §2); not recorded.
- **Conditions that end acceptance:** masking falls below its accepted threshold (gap: no threshold set; M2 is 82%); counter-metric over 5%; model retirement (D1).

## NIST AI RMF mapping

| Function | Content in this assessment | Evidence |
| --- | --- | --- |
| Govern | Decider, Privacy Officer and Head of Security named; acceptance not recorded; training gap | docs/discovery/hr-assistant.md §5 |
| Map | Scope, parties, Australia-only screen | regulatory-memo.md, D6 |
| Measure | Leave accuracy, masking coverage and summary accuracy measured; no bias, no checking rate, no red-team | M1, M2, M3 |
| Manage | Contracts C1 to C5; security review W2 pending; no incident records exist | C1, C5, W2 |

| NIST AI 600-1 risk | Applies? | Measure and suggested actions performed | Evidence |
| --- | --- | --- | --- |
| CBRN information | n/a: HR assistant, no such content | none needed | R1 |
| Confabulation | yes | Source-record list and measured match; no red-team of invented records | C5, M1, M3 |
| Dangerous, violent or hateful content | n/a: internal HR scope; assumption: not tested | none recorded | R1 |
| Data privacy | yes | Scoping and masking; US error flow and engineer access open | C1, C4, D4, D5, M2 |
| Environmental impacts | n/a: not assessed at pilot scale | none | D1 |
| Harmful bias or homogenisation | yes | gap: no bias measurement of attendance summaries | C5 |
| Human-AI configuration | yes | Manager reads summary; gap: automation bias unmeasured | D6, C5 |
| Information integrity | yes | Answers cite records; policy answers unmeasured | M1 |
| Information security | yes | Read-only user and scoped tools; no red-team recorded | C3, SB01, SB03 |
| Intellectual property | n/a: no creative or third-party content generation | none | R1 |
| Obscene, degrading or abusive content | n/a: internal HR scope; assumption: not tested | none recorded | R1 |
| Value chain and component integration | yes | Gemini, Sentry, Workday and Entra ID are third parties; contracts not recorded | D1, D4, D7 |

## Monitoring and review

- Counter-metric: share of answers staff mark wrong, target under 5%; gap: not yet measured, planned under G05 (docs/discovery/hr-assistant.md §2).
- Masking coverage is re-measured per build (M2); gap: threshold not set.
- **Review triggers:** model change or retirement (D1), a rollout to Victoria and Queensland (docs/discovery/hr-assistant.md §1), any incident, a change in law (APP 1.7 from 10 December 2026, checked 2026-10-26).

## Adverse impact and equality

| Group or characteristic | Selection or outcome rate | Ratio to the highest group | Test and sample | Proxies removed | Evidence |
| --- | --- | --- | --- | --- | --- |
| Staff with illness, carer duties or union involvement (attendance summaries) | gap: not measured | gap | gap: no sample | gap | C5, docs/discovery/hr-assistant.md §4 |

- **Less discriminatory alternatives considered and accessibility route:** gap: none recorded; an alternative is to withhold summaries that include protected absences (counsel: is any disparity justified; Fair Work general protections and anti-discrimination law).

## Australia: Guidance for AI Adoption mapping

| Practice | Content in this assessment | Evidence |
| --- | --- | --- |
| 1 Decide who is accountable | Marcus Bell decides; Grace Nguyen and Daniel Okoro review; Southgate Labs engagement lead Priya Raman; Google is the model provider | docs/discovery/hr-assistant.md §5 |
| 2 Understand impacts and plan accordingly | H1 to H6; the team member has no contest route (gap) | D6 |
| 3 Measure and manage risks | M1 to M3 and C1 to C5; gaps above | M1, M2, M3 |

## Review and sign-off

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| Head of Security (Daniel Okoro) | this document | pending | pending |
| Privacy Officer (Grace Nguyen) | this document | pending | pending |
