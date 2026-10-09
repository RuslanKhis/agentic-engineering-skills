# From architecture to work someone can carry out

Use when explaining how a design choice can be implemented or preparing the
final handoff. The output must let another session identify the next useful
goal, its integration points, relevant skills and evidence of completion.

## Ground each implementation route

Inspect the target's entrypoint, dependencies, public interfaces and tests when
available. Connect **decision → component/API → integration point → skill →
acceptance**. Identify what exists and what is proposed. For greenfield work,
propose a small module/interface layout and label it as such. Verify SDK names
and provider constraints against the target version before offering executable
code. Unknown interfaces become explicit investigation tasks with a deciding
question and bounded evidence needed.

These are starting points, not a stack to install in every application:

| Need | Concrete implementation route to assess | Infrastructure responsibility | Primary skill |
| --- | --- | --- | --- |
| Bounded language/tool orchestration | `LlmAgent` with narrow tools, invoked through the application's `App`/`Runner`; use ordinary code or a workflow agent for known ordering. Locate the agent factory and serving invocation. | Selected model endpoint; application host chosen separately | `adk-workflow-design` |
| Agent instructions and sub-agent descriptions | Instruction text at the right altitude with session-state templating; tool-use guidance in prose; each sub-agent `description` written as the routing contract the parent reads verbatim; the prompt kept as versioned code with a rendered-request test. Anything the application already knows moves to code. | None beyond the model endpoint | `adk-agent-instructions` |
| Model-facing tool interfaces and tool budgets | One declaration per tool as the model sees it: name, docstring, primitive parameters, bounded result dict with a status and actionable errors; per-agent tool count and toolset filtering; the delegation interface (`AgentTool` versus sub-agent modes). | None; server-supplied toolsets bring their own hosting | `adk-tool-interface-design` |
| Output contracts, model and backend selection | `output_schema` with a first-class refusal shape; validation failure handled at a boundary the application owns with a bounded repair budget; pinned model ID with its lifecycle date; thinking and sampling settings; failover as a decision. | The chosen backend (Gemini API or Vertex) decides how a schema is enforced | `adk-model-and-output-contracts` |
| Tools or agents across a process boundary | Tool source per capability (function tool, OpenAPI, MCP, managed toolset); `McpToolset` with an allow-list and recorded definitions; `RemoteA2aAgent` with a deliberate timeout, task-state handling and peer output treated as data; an agent card that declares capability and security schemes when exposing. | Server or peer hosting, identity between the parties, registry entries | `adk-agent-interoperability` |
| Persistent conversation or exact preferences | Assess `DatabaseSessionService` for ADK events; use application-owned profile records for exact user settings. Load a trusted user's profile at the invocation boundary. | Reuse the existing database where compatible; Cloud SQL is a candidate when a new managed PostgreSQL service is justified | `adk-memory-architecture` |
| Context-window shaping | Decide what enters each model request: a stable instruction and tool prefix for caching, tool results bounded at the tool boundary, compaction or filtering of retained history, and an overflow rule per slice. Measure on captured requests, not configuration. | Provider caching minimums and billing | `optimise-adk-on-google-cloud` |
| Browser replies and progress | Authenticated API around the Runner or remote runtime; custom JSON or AG-UI adapter; application-owned text, tool-result and completion schema connected to the existing UI. | Gateway hosting, streaming transport and session access | `adk-frontend-integration` |
| Reliable external writes | Python tool/service adapter plus a durable operation record, canonical payload and provider-backed replay/reconciliation. An asynchronous path also needs durable dispatch ownership. | Existing transactional store and approved external API; durable worker only if required | `safe-api-tool-calls` |
| Caller authority and delegated access | Verify caller/session ownership before invocation; supply trusted scope to tools; choose credentials in backend code and maintain connection lifecycle metadata. | Workload identity and Secret Manager or the existing credential store | `adk-tool-auth-and-secrets` |
| Budgets and human review | Assess `RunConfig.max_llm_calls` plus application admission/reservations for shared allowances and transport attempts; durable approval and executor records for cross-request review. Check native confirmation compatibility before using it. | Shared control store and separately owned recovery/notification work | `adk-operational-guardrails` |
| Sensitive-data boundaries | Place protection at actual ingress, persistence, tool and public-release seams; define typed projections and failure behavior. | Approved inspection services when required, with scoped identity, region and capacity | `protect-adk-sensitive-data` |
| Security posture and adversarial suite | Per-agent trifecta check (private data, untrusted content, egress or write); readers split from writers with structured state between them; capability checks in `before_tool_callback` keyed on trusted state; tool tiers with confirmation on irreversible actions; a sandboxed code executor; scripted-model tests asserting the forbidden action never runs. | Executor sandbox; egress controls of the test environment | `adk-agent-security` |
| Governed analytical answers | Reviewed SQL or constrained authoring, selective schemas, deterministic validation/execution and evidence-backed results. | Restricted database/BigQuery access with query-cost limits | `adk-sql-agent-engineering` |
| Runtime and release | Package the actual serving entrypoint and dependencies; configure identity, state and lifecycle; define deployment readback and recovery checks. | Cloud Run, managed Agent Runtime or GKE according to the accepted design | `deploy-adk-on-google-cloud` |
| Telemetry, SLOs and production-to-evaluation hand-off | One telemetry provider owner per process; content-capture gates set deliberately with the sensitive-data policy; usage counted once per logical model call; good/total SLIs from measured baselines with error-budget alerts; trace, invocation and session identifiers preserved at every hop; sampled production sessions redacted into evaluation cases. | Trace, monitoring, logging and analytics sinks with their own access and retention | `adk-agent-observability` |
| Release lifecycle, pinning, CI gates, canary and rollback | One release unit (image or revision, prompt version, model and judge IDs, tool schema hash, eval-set hash, secret versions) recorded in a manifest; a deterministic evaluation gate that fails by exit code; model retirement handled as a planned re-baseline; staged traffic with the previous revision kept ready. | CI runner; traffic split and revision retention on the chosen host | `adk-release-engineering` |

Every implementation goal includes relevant local regression checks. Add
`adk-agent-evaluation` when agent behavior or evaluation design is a substantial
part of that goal, and `optimise-adk-on-google-cloud` for measured performance
work. Choose supporting skills from the boundaries a goal touches: a goal that
adds or changes a tool gets `adk-tool-interface-design`; one that changes
instruction text or sub-agent routing gets `adk-agent-instructions`; one that
reads untrusted content (documents, retrieved passages, server-supplied tool
results, peer messages) and holds a write or egress tool gets
`adk-agent-security`; one that promises structured output or changes the model
gets `adk-model-and-output-contracts`; one that crosses a process boundary gets
`adk-agent-interoperability`; the first goal that reaches a shared environment
gets `adk-agent-observability` and `adk-release-engineering`. Name one primary
skill and only the supporting skills the slice needs.
Verify availability through the host catalogue or sibling packages; a missing
skill is a setup prerequisite, not a claim that its guidance was applied.

Official lookup points for the named interfaces:
[agents](https://adk.dev/agents/llm-agents/), [App](https://adk.dev/apps/),
[sessions](https://adk.dev/sessions/session/),
[RunConfig](https://adk.dev/runtime/runconfig/),
[confirmation limitations](https://adk.dev/tools-custom/confirmation/#known-limitations),
[Cloud Run deployment](https://adk.dev/deploy/cloud-run/).
Each specialist's `references/compatibility.md` records the ADK version its
building blocks were read against; constructors and behavior still need
verification against the project's chosen version.

## Write goals that preserve the reasoning

Use the [plan template](../assets/implementation-plan-template.md), adapting the
project's existing convention. Link architecture decisions instead of copying
their rationale into a competing document. Give goals stable IDs and names.
Each goal delivers a testable user behavior or resolves a named uncertainty.

For each goal record outcome, scope, integration points, ADK/GCP choices,
prerequisites and dependency IDs, skills, acceptance cases and evidence tier.
Distinguish decision readiness from authorization: a goal can be ready in design
while its cloud execution awaits an identified target or permission. Record
verified facts and assumptions separately; completion needs actual evidence.

For example, **“A signed-in user saves a language preference and gets it next
session”** is a useful slice. Its route is an owner-scoped profile API/store,
profile loading before agent execution and the existing preferences UI. Its
primary skill is `adk-memory-architecture`; auth or frontend guidance is added
only for boundaries being changed. Acceptance exercises saving, restart, use
in a new session, cross-user denial and forgetting. This can run locally with
controlled external dependencies before selecting or provisioning cloud storage.

Group goals into the phases of [delivery profiles](delivery-profiles.md#split-the-plan-into-phases):
phase 1 fits the stated capacity, phase 2 graduates or hardens, and the later
list keeps each deferred item with its trigger. A goal records its depth, so
the agent that carries it out builds the floor and the profile's depth, not
every control its specialist describes.

Separate precise unresolved questions from build goals they block. A discovery
goal should yield a decision or evidence artifact, with a stopping condition.
Keep later work coarse when it depends on that answer. Choose the smallest
ready implementation slice; independent local progress remains possible while
provider or deployment checks are pending.

## Continue the work

The default needs nothing else installed. Each goal in the plan carries its own
run prompt, and `adk-engineer` reads the goal's `Primary skill` and
`Supporting skills` lines, loads them and performs the authorized work:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
/adk-engineer Continue the next ready goal in docs/plans/<topic>.md.
```

When the user wants one file per unit of work, for a tracker or for parallel
sessions, copy each ready goal into the [ticket template](../assets/ticket-template.md)
under `docs/tickets/<topic>/`. Each ticket ends with its own run prompt, and the
agent that carries it out fills in its Evidence section.

### Other planning workflows (skip unless the user chose one)

The Markdown plan is portable input; it is not automatically a native tracker
map or an imported set of issues. Inspect the selected workflow's installed
instructions and project conventions before adapting it.
- **Large unresolved effort:** when the user chooses Matt Pocock's `wayfinder`,
  carry destination, accepted decisions, unresolved questions, dependencies and
  relevant skill names into its decision-planning workflow. Precisely stated
  questions can become decision tickets; later uncertainty stays unspecified.
  Implementation goals remain the downstream handoff. Use an existing map where
  present and link canonical decisions rather than restating them.
- **Ready multi-session build:** Matt's `to-spec` can turn the agreed design and
  plan into the project spec; `to-tickets` can split it into dependency-aware
  implementation slices; `implement` can work those tickets. Small settled work
  can go directly to `implement` or the requested specialist. `tdd` is an optional
  development method; preserve already-agreed public test boundaries.

Adapt to the destination's format: for example, `to-spec` keeps implementation
decisions at module/interface level. Keep concrete file-path and API observations
in the linked handoff when its spec format excludes them. Preserve agreed versus
proposed test boundaries when the destination checks that agreement.

These optional workflows may publish tracker items or perform repository actions.
A design handoff proposes the continuation; execute it only when requested and
within existing authorization. Keep the active tracker/spec as the source of truth
after adoption and turn the old plan into a pointer where necessary. Missing
optional workflows leave the portable plan usable directly.

Upstream references:
[Wayfinder](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md),
[workflow router](https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md).
Installed instructions govern actual invocation and tracker layout.
