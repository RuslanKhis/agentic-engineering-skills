# System design: <application or change>

Status: draft / user-reviewed decisions recorded below

## Purpose and constraints

Summarize users, one concrete journey, its current friction, useful result,
non-goals and existing systems. Name the outcome to improve and any known baseline.
Separate confirmed requirements, observed repository facts and proposed assumptions.
State what the model contributes and what ordinary code controls.

## Guarantees and acceptance

| Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |

Include only meaningful promises. Quantified targets need an owner/source or an
explicit provisional assumption; unresolved guarantees remain visible.

## Architecture and decisions

Show a component diagram and the important request/operation sequence when useful.
Label trust boundaries, user/workload identities, stores, public output and effects.

| Requirement | Design choice | Reason | Tradeoff / alternative | Verification and expected result |
| --- | --- | --- | --- | --- |

Record decision IDs and their status (proposed, user-accepted or superseded)
with assumptions and revisit conditions. Update dependent choices and checks
when a requirement changes. Reference detailed contracts and tests below rather
than repeating them; keep this record proportionate to the design.

Distinguish application runtime, model backend and data services. Record relevant
versions, current provider sources and any capability still needing verification.

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |

Capture session/invocation/business-operation identities, tool schemas, approval
binding, credential ownership and public-output policy where relevant.

## Budgets and capacity

Record workload assumptions, complete-request latency and first meaningful output,
model/tool/retry fan-out, concurrent demand, usage units and enforcement points.
State restart behavior, exhaustion outcomes and dated/symbolic cost assumptions.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |

Trace successful completion and the applicable denial, partial failure, timeout,
duplicate/restart and erasure scenarios. Include rollout, rollback and owned-resource
cleanup at the depth the task needs.

## Verification and implementation handoff

Separate planned offline, local integration, live-provider and hosted checks.
Identify existing evidence without presenting it as a fresh test.
Where a design claims improved user or business outcomes, state the baseline,
measurement and guardrails separately from technical correctness and model quality.
Keep unmeasured benefits explicit as hypotheses.

Link the implementation plan, or include its goals here for a small effort.
Map consequential choices to ADK/application components, concrete integration
points, GCP responsibilities and relevant specialists. Label proposed modules
and unresolved version/provider checks. Define dependency-ordered goals with
acceptance evidence, then identify the next ready goal and continuation prompt.

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |

Record which decisions the user accepted. Design completion and implementation
authorization are separate facts; preserve implementation already requested.
