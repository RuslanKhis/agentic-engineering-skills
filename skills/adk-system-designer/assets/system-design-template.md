# System design: <application or change>

Status: draft / user-reviewed decisions recorded below

## Purpose and constraints

Summarize users, one concrete journey, its current friction, useful result,
non-goals and existing systems. Name the outcome to improve and any known baseline.
Separate confirmed requirements, observed repository facts and proposed assumptions.
State what the model contributes and what ordinary code controls.

## Scope, evaluator and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| Time and money available | <hours or days; spending allowance and its reserve for the deliverable> |
| Who judges the result and what they read | <reviewer; predictions, report, demo or running service> |
| Artifact type | exploration / assignment / pilot / production |

List, explicitly, the controls this design chooses not to build yet and why:

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |

When the artifact is judged on output quality, the first slice is the core
judgment end to end on real inputs with a measured result; deferred controls
start after that measurement exists.

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

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions and routing descriptions | <judgment each agent owns; sub-agent descriptions as routing contracts; what stays in code> | `adk-agent-instructions`; rendered-request test |
| Tool interfaces and budgets | <tool source per capability; per-agent tool count; result bound; read/write/irreversible tier> | `adk-tool-interface-design`; `adk-agent-interoperability` for MCP or A2A; declaration dump and size |
| Output contract, model and backend | <schema with refusal shape; pinned model ID and lifecycle date; backend; thinking; failover> | `adk-model-and-output-contracts`; scripted invalid-output test |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |

Capture session/invocation/business-operation identities, tool schemas, approval
binding, credential ownership and public-output policy where relevant.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution (split, remove a leg, or accepted risk) |
| --- | --- | --- | --- | --- |

Record the tool tiers (read, write, irreversible) and the confirmation each
tier needs in code, the code executor and its sandbox, and the adversarial
cases that assert the forbidden action never runs. `adk-agent-security` owns
the threat model; omit this block with a one-line reason for a read-only
product with no untrusted input.

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

Name the deliverable the evaluator will judge (predictions, exports, answers)
and the rule that it is produced by the method the report describes: when the
method changes, the deliverable is regenerated, or the report states that it
was not and why. Reserve the budget for that final run before any experiment
draws on it.

Observability and release, at the depth the artifact type needs:

- SLIs tied to the guarantees above, each with baseline, target and alert owner.
- Telemetry owner per process; content-capture gates and sinks with retention.
- Release bundle: image or revision, prompt version, model and judge IDs, tool
  schema hash, secret versions, and where it is recorded.
- Promotion gate (deterministic checks, judge schedule, cost ceiling) and the
  canary's comparable sample.
- Rollback unit and how long the previous revision stays ready.

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
