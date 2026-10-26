---
topic: <topic>
design: docs/architecture/<topic>.md
plan: docs/plans/<topic>.md
goal: <G-ID or none>
primary_build: GCP + Google ADK (unchanged)
concern: <one line: who raised it and what they fear>
targets: [aws, azure]
frameworks: [langgraph, openai-agents, microsoft-agent-framework, pydantic-ai]
sources_checked: <YYYY-MM-DD>
status: draft
---

# Portability assessment: <application>

## Summary for the reader

<One page for the person who decides, citing IDs rather than restating them:>

- **Recommendation:** <the strategy in one sentence, for example "keep GCP and ADK; hold an exit plan; no second provider now">
- **Google-specific on purpose:** <components kept provider-specific by choice or as expensive dependencies, each with its design ID and the value it buys>
- **Boundaries kept:** <the few seams worth having, naming ADK's existing seam where there is one>
- **What a move would involve:** <the largest drivers: model change and re-evaluation, data rebuilds, identity and policy re-mapping>

## Concern and scope

- **Question asked:** <the stakeholder's question in their words, with who asked and when>
- **Move later or run on several now:** <exit plan at a known cost, or multicloud now on a stated need with its date or trigger>
- **Targets:** <clouds and frameworks assessed, and whether the ticket named them or the default was used>
- **In and out of scope:** <dimensions covered; what this assessment does not decide>

## Baseline architecture

<The GCP and ADK components the design records, one line each with its D, C or R ID; read the design rather than restating it. Mark facts taken from the design only, without inspected code, as design-only.>

## Component classification

| Component | Design IDs | Class | Why | Exit path |
| --- | --- | --- | --- | --- |
| <component> | <D1> | <shared logic / replaceable adapter / provider-specific by choice / expensive dependency> | <the decision criterion that placed it> | <what a move would rewrite, regenerate or re-evaluate> |

## Dimensions

| Dimension | Assessment |
| --- | --- |
| Cloud | <assessed, or not a concern: reason> |
| Agent framework | <assessed, or not a concern: reason> |
| Model | <assessed, or not a concern: reason; a model swap is not a system move> |
| Service | <assessed, or not a concern: reason> |
| Deployment | <assessed, or not a concern: reason> |

## Cloud alternatives

| Responsibility | GCP (design ID) | AWS | Azure | Difference | Portability |
| --- | --- | --- | --- | --- | --- |
| <hosting, model, sessions, data, retrieval, identity, observability, safety> | <service (D1)> | <option and status> | <option and status> | <what changes that matters> | <straightforward / moderate / expensive> |

## Agent framework alternatives

| Concern | ADK (baseline) | <framework> | <framework> |
| --- | --- | --- | --- |
| <the features this design relies on: workflow, approval, sessions, streaming, evaluation, hosting> | <how the design uses it> | <yes / partial / no / unverified, with the difference> | <...> |

<One line: what a framework switch would rewrite here and what survives.>

## Boundaries worth having

| Boundary | What it isolates | Reason (a, b, c or d) | Cost now | Existing ADK seam |
| --- | --- | --- | --- | --- |
| <boundary> | <dependency> | <second implementation now / stated switch / framework seam / volatile API> | <none, or the work> | <BaseSessionService, model connector, MCP, OTLP, or none> |

## Feature differences and migration risks

- <risk: what differs on the target, the component and design ID it affects, and its switching cost and likelihood>

## Recommended strategy

<The simplest strategy that answers the concern, its trade-offs, and why it is not multicloud now unless a stated need requires it.>

## Phased outline

1. **<phase>:** <strangler or parallel run, data backfill and change capture, re-running evaluation sets, cutover and rollback>

## Relative effort

| Item | Relative effort (small / medium / large / very large / unknown) | Drivers | Assumptions |
| --- | --- | --- | --- |
| <item> | <size by the largest driver> | <data, re-evaluation, identity, integration points, operations> | <what the size assumes; figures only with M<n> or the word assumption> |

Schedule risks outside the team's control: <contract, compliance or client re-approval, or none>.

## Optional recommendations for the current build

<None, or one block per recommendation. None of these is a ticket until a designer checkpoint approves it.>

### <recommendation>

- **What:** <the change to the current GCP build>
- **Rationale:** <why it lowers a switching cost cheaply now>
- **Acceptance criteria:** <observable checks>
- **Specialist:** <an existing sibling skill, in backticks>
- **Status:** proposed; needs a designer checkpoint

## Open questions

- <question for stakeholders or platform teams, who can answer it, and what it changes>

## Sources

| Claim or topic | URL | Read on |
| --- | --- | --- |
| <claim that drives a classification or risk> | <https URL> | <YYYY-MM-DD> |
