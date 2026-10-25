---
document: impact-assessment
system: <system name>
version: <build or design revision assessed>
status: draft
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
trigger: <why this assessment now: design, production decision, significant change>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md, classification-memo.md>
---

# AI system impact assessment: <system name>

Structured along the topics of ISO/IEC 42005:2025 and mapped to NIST AI RMF
1.0 and NIST AI 600-1. Draft for <client>'s risk owner; scores are
provisional until they set them. Not legal advice.

## Scope and intended use

- **System and functions:** <what it does; what the model decides; what code decides> (<C/D IDs>).
- **Intended use:** <workflow and users> (<R IDs>); **unintended or foreseeable misuse:** <uses> (<C/SB IDs or assumption:>).
- **Organisation's role:** <provider / deployer / both; agency's role> (classification memo, <D ID or counsel:>).
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
| Map | <scope, parties, classification> | <IDs> |
| Measure | <evaluations and what is unmeasured> | <M IDs, reports> |
| Manage | <measures, incidents, monitoring> | <C/SB/I IDs> |

| NIST AI 600-1 risk | Applies? | Measure | Evidence |
| --- | --- | --- | --- |
| Confabulation | <yes / n/a: reason> | <measure> | <IDs> |
| Data privacy | <yes / n/a: reason> | <measure> | <IDs> |
| Harmful bias or homogenisation | <yes / n/a: reason> | <measure> | <IDs> |
| Human-AI configuration | <yes / n/a: reason> | <measure> | <IDs> |
| Information security | <yes / n/a: reason> | <measure> | <IDs> |
| Value chain and component integration | <yes / n/a: reason> | <measure> | <IDs> |
| <each remaining risk of the twelve> | <yes / n/a: reason> | <measure> | <IDs> |

## Monitoring and review

- <measure watched in operation, owner and threshold> (<C/M IDs>).
- **Review triggers:** model change, new user group or data, incident, change in law (<D/G IDs>).
