# From architecture to work someone can carry out

Use when explaining how a design choice can be implemented or preparing the
final handoff. The output must let another session identify the next useful
goal, its integration points, relevant skills and evidence of completion.

## Ground each implementation route

Inspect the target's entrypoint, dependencies, public interfaces and tests when
available. Connect **contract → decision → component/API → integration point →
skill → acceptance**. Identify what exists and what is proposed. For greenfield
work, propose a small module/interface layout and label it as such. Verify SDK names
and provider constraints against the target version before offering executable
code. Unknown interfaces become explicit investigation tasks with a deciding
question and bounded evidence needed. A route that lifts a pattern from
`google/adk-recipes` names the recipe and the file, carries the repository's
"not production use" disclaimer into the goal, and lists the controls the
recipe omits as acceptance items; the design never copies recipe code.

These are starting points, not a stack to install in every application:

| Need | Concrete implementation route to assess | Infrastructure responsibility | Primary skill |
| --- | --- | --- | --- |
| Bounded language/tool orchestration | `LlmAgent` with narrow tools, invoked through the application's `App`/`Runner`; use ordinary code or a workflow agent for known ordering. Locate the agent factory and serving invocation. | Selected model endpoint; application host chosen separately | `adk-workflow-design` |
| Agent instructions and sub-agent descriptions | Instruction text at the right altitude with session-state templating; tool-use guidance in prose; each sub-agent `description` written as the routing text the parent reads verbatim; the prompt kept as versioned code with a rendered-request test. Anything the application already knows moves to code. | None beyond the model endpoint | `adk-agent-instructions` |
| Model-facing tool interfaces and tool budgets | One declaration per tool as the model sees it: name, docstring, primitive parameters, bounded result dict with a status and actionable errors; per-agent tool count and toolset filtering; the delegation interface (`AgentTool` versus sub-agent modes). | None; server-supplied toolsets bring their own hosting | `adk-tool-interface-design` |
| Output schemas, model and backend selection | `output_schema` with a first-class refusal shape; validation failure handled at a boundary the application owns with a bounded repair budget; pinned model ID with its lifecycle date; thinking and sampling settings; failover as a decision. | The chosen backend (Gemini API or Vertex) decides how a schema is enforced | `adk-model-and-output-contracts` |
| Tools or agents across a process boundary | Tool source per capability (function tool, OpenAPI, MCP, managed toolset); `McpToolset` with an allow-list and recorded definitions; `RemoteA2aAgent` with a deliberate timeout, task-state handling and peer output treated as data; an agent card that declares capability and security schemes when exposing; a deterministic policy service is a valid A2A peer when a hard rule must not depend on a model. For an exposed MCP server, the acceptance check is a pinned command with a reviewed baseline: `npx -y @modelcontextprotocol/conformance@0.2.0-alpha.12 server --url http://127.0.0.1:$PORT/mcp --requirements <revision> --expected-failures conformance-baseline.yml` exits 0, every baseline entry names a scenario or check and the fixture it depends on (proven on google-adk 2.12.0 on 2026-10-22; the interoperability skill's validation reference has the results). For an exposed A2A agent, the acceptance item is a planned verification whose first step is the spike: `./run_tck.py --sut-host http://127.0.0.1:$PORT --level must -- -k 'agent_card or versioning'` on the pinned a2a-sdk with `reports/compatibility.json` attached and the deferred requirement ids listed (the TCK was read, not run, on 2026-10-22). | Server or peer hosting, identity between the parties, registry entries | `adk-agent-interoperability` |
| Persistent conversation or exact preferences | Assess `DatabaseSessionService` for ADK events; use application-owned profile records for exact user settings. Load a trusted user's profile at the invocation boundary. | Reuse the existing database where compatible; Cloud SQL is a candidate when a new managed PostgreSQL service is justified | `adk-memory-architecture` |
| Context-window shaping | Decide what enters each model request: a stable instruction and tool prefix for caching, tool results bounded at the tool boundary, compaction or filtering of retained history, and an overflow rule per slice. Measure on captured requests, not configuration. | Provider caching minimums and billing | `optimise-adk-on-google-cloud` |
| Browser replies and progress | Authenticated API around the Runner or remote runtime; custom JSON or AG-UI adapter; application-owned text, tool-result and completion schema connected to the existing UI. | Gateway hosting, streaming transport and session access | `adk-frontend-integration` |
| HTTP API beyond the agent route | Domain routes under `/api` behind the shared verified-principal dependency; records filtered by owner; application tables and migrations kept apart from ADK's; the public OpenAPI contract and generated client; one error handler; CORS and headers; the single-process Cloud Run shape | Database for application data; Cloud Tasks for work that must outlive the response | `adk-fastapi-backend` |
| Visual design and agent UI states | shadcn components themed from DESIGN.md tokens, starting from the house design system; agent events mapped to UI states; screenshot and accessibility checks at the profile's depth | None | `adk-frontend-integration`, with companions `shadcn` and, for a new visual direction, `frontend-design` |
| Web security baseline | Rules from the [security baseline](security-baseline.md), recorded once in the design and cited in goals and acceptance | As each rule's owner needs | The rule's *Implemented by* skill |
| Reliable external writes | Python tool/service adapter plus a durable operation record, canonical payload and provider-backed replay/reconciliation. An asynchronous path also needs durable dispatch ownership. | Existing transactional store and approved external API; durable worker only if required | `safe-api-tool-calls` |
| Caller authority and delegated access | Verify caller/session ownership before invocation; supply trusted scope to tools; choose credentials in backend code and maintain connection lifecycle metadata. | Workload identity and Secret Manager or the existing credential store | `adk-tool-auth-and-secrets` |
| Budgets and human review | Assess `RunConfig.max_llm_calls` plus application admission/reservations for shared allowances and transport attempts; durable approval and executor records for cross-request review. Check native confirmation compatibility before using it. | Shared control store and separately owned recovery/notification work | `adk-operational-guardrails` |
| Sensitive-data boundaries | Place protection at actual ingress, persistence, tool and public-release seams; define typed projections and failure behavior. | Approved inspection services when required, with scoped identity, region and capacity | `protect-adk-sensitive-data` |
| Security posture and adversarial suite | Per-agent trifecta check (private data, untrusted content, egress or write); readers split from writers with structured state between them; capability checks in `before_tool_callback` keyed on trusted state; tool tiers with confirmation on irreversible actions; a sandboxed code executor; scripted-model tests asserting the forbidden action never runs. | Executor sandbox; egress controls of the test environment | `adk-agent-security` |
| Governed analytical answers | Reviewed SQL or constrained authoring, selective schemas, deterministic validation/execution and evidence-backed results. | Restricted database/BigQuery access with query-cost limits | `adk-sql-agent-engineering` |
| Choosing where AI goes, the first use case and its measure | A discovery brief: journey friction or KPI-to-process map, ranked opportunity portfolio with technology fit (agent, LLM, classical ML, rules, process change), the first use case with its outcome measure and baseline, and the hypothesis chain. Precedes design; the designer reads it as answered scope. | None | `adk-discovery` |
| Stakeholder approval or results review at a phase boundary | A deck outline with an action title and an evidence citation per slide, the spoken narrative, the questions to expect and a one-page decision memo, built from this plan's recorded evidence; one outline per audience (business, technical) and a public case study when the result is shareable. | None | `adk-presenter` |
| Monthly value report after launch | A one-page report for the sponsor: outcome against the brief's baseline, counter-metric, adoption, cost per outcome against the plan's estimate, incidents and thresholds fired, each figure citing an M or I record, ending in a stop, continue or scale call with its decider. | None | `adk-presenter` (`value-report` stage) |
| Governance papers for the client's reviewers | Drafts under `docs/governance/<topic>/`, after a jurisdiction screen (Australia, United States, EU, UK, in that order): regulatory memo (EU AI Act classification where the EU applies), privacy impact input pack (PIA, DPIA or US risk assessment), transfer assessment annex, records-of-processing rows under GDPR or UK GDPR, impact assessment, system card and security questionnaire answers, each statement citing contract, decision and evidence IDs or flagged for counsel; sized to the profile. Sign-offs are calendar waits. | None | `adk-governance-pack` |
| Portability or lock-in concern recorded in the scope gate | A separate, high-level assessment at `docs/portability/<topic>.md`: provider dependencies, AWS and Azure alternatives, a small comparison of other agent frameworks, model portability, the replacement boundaries worth having, migration risks and a phased outline with relative effort. The GCP + ADK design stays the build; nothing is implemented and the design does not change. | None | `adk-portability-planning` |
| Runtime and release | Package the actual serving entrypoint and dependencies; configure identity, state and lifecycle; define deployment readback and recovery checks. | Cloud Run, managed Agent Runtime or GKE according to the accepted design | `deploy-adk-on-google-cloud` |
| Telemetry, SLOs and production-to-evaluation hand-off | One telemetry provider owner per process; content-capture gates set deliberately with the sensitive-data policy; usage counted once per logical model call; good/total SLIs from measured baselines with error-budget alerts; trace, invocation and session identifiers preserved at every hop; sampled production sessions redacted into evaluation cases. | Trace, monitoring, logging and analytics sinks with their own access and retention | `adk-agent-observability` |
| Release lifecycle, pinning, CI gates, canary and rollback | One release unit (image or revision, prompt version, model and judge IDs, tool schema hash, eval-set hash, secret versions) recorded in a manifest; a deterministic evaluation gate that fails by exit code; model retirement handled as a planned re-baseline; staged traffic with the previous revision kept ready. | CI runner; traffic split and revision retention on the chosen host | `adk-release-engineering` |

Every implementation goal includes relevant local regression checks, including the earlier acceptance items named in the ticket's `pass_to_pass` list. Add
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

A goal that creates or changes a web component also names its companion
skills, its design system and the security rule IDs it proves (see
[web application defaults](web-app-defaults.md)). Companions install in the
application project. A missing companion is a setup step, not a claim that its
guidance was applied.

### Name the Google product skill a route needs

Google's `google/skills` collection (Apache-2.0, installed with
`npx skills@latest add google/skills --skill <name>` or fetched on demand by
its `finding-google-skills` router) operates Google Cloud products: it
provisions, queries, generates Terraform and PromQL, and administers. It does
not design the application; this toolkit's specialist does. When a route's
infrastructure responsibility must be carried out, add the product skill to
the goal's supporting skills as `google/skills:<name> (purpose)`.
`adk-engineer` checks whether it is installed, shows how to get it when not,
and treats its commands as proposals that still need the user's approval for
that scope. A goal with such a line stays ready in design; its product step
is an execution-scope prerequisite until authorised.

| Infrastructure responsibility in the route | `google/skills` name(s) |
| --- | --- |
| A project with billing, APIs and a landing zone, or an organisation-managed account | `google-cloud-recipe-onboarding`, `google-cloud-recipe-auth`, `google-cloud-recipe-foundation-builder` |
| Any `gcloud` command the goal will run | `gcloud` |
| Cloud Run service, ingress and egress, private tiers, a public load balancer | `cloud-run-basics`, `google-cloud-solution-n-tier-serverless-web-app`, `google-cloud-global-frontend-configuration` |
| GKE cluster, onboarding, scaling, cost | `gke-basics`, `gke-app-onboarding`, `gke-workload-scaling`, `gke-cost-optimization` |
| Agent Runtime behind an Agent Gateway, Agent Identity, egress policies, Agent Registry | `agent-platform-troubleshooting`, `google-cloud-solution-multi-agent-security`, `apigee-agent-gateway-governance` |
| IAM bindings and deny policies to write | `iam-helper-for-policy-management` |
| Replaying 90 days of access against a narrower policy before applying it | `iam-helper-for-policy-simulator` |
| A 403 on the runtime identity | `iam-helper-for-troubleshooting` |
| Time-bound operator or break-glass access | `iam-helper-for-privileged-access-management` |
| Model Armor templates, Sensitive Data Protection, Vertex AI quotas, any product with no skill of its own | `gcloud` (the command skill; the specialist supplies the settings) |
| A REST API exposed as a remote MCP server, with auth and quotas | `api-gateway-mcp-server`, `api-gateway-backend-security-and-rate-limiting` |
| Cloud SQL or AlloyDB instance, IAM database users, backups | `cloud-sql-basics`, `alloydb-basics` |
| BigQuery datasets, partitioning, cost diagnosis, `AI.*` syntax | `bigquery-basics`, `bigquery-optimization`, `bigquery-troubleshooting`, `bigquery-ai-ml` |
| RAG Engine corpora, Cloud Storage buckets and signed URLs | `agent-platform-rag-engine-management`, `google-cloud-storage-basics` |
| Alert policies on agent metrics (Terraform), on the Cloud Run host, or a formal SLO with burn-rate alerts | `agent-platform-alert-configuration`, `cloud-run-alert-configuration`, `google-cloud-slo-alert-configuration` |
| A PromQL query, a metric descriptor lookup, a dashboard widget, a notification channel | `cloud-monitoring-promql-query`, `cloud-monitoring-metric-selection`, `cloud-monitoring-chart-generation`, `cloud-monitoring-notification-channels-configuration` |
| A trace search; a log query; a log sink, bucket or view | `cloud-trace-querying`; `cloud-logging-query-generation`; `cloud-logging-configuration-basics` |
| A Well-Architected pillar review at MVP or production profile | `google-cloud-waf-reliability`, `-security`, `-cost-optimization`, `-operational-excellence`, `-performance-optimization` (one per pillar whose depth is "build now") |
| CI on Cloud Build; the managed evaluation scorer | `cloud-build-basics`, `agent-platform-eval-flywheel` |
| Direct Gemini calls outside ADK, fine-tuning, self-hosted open models | `gemini-api`, `agent-platform-tuning`, `agent-platform-inference` |
| Audio or video streaming | `google-cloud-solution-agentic-ai-bidirectional-streaming`, `gemini-live-api` |
| Security Command Center findings on the agent's project | `google-cloud-scc-query`, `google-cloud-scc-remediation` |
| A scheduled evaluator over production traces after launch | `google/adk-recipes:agents-cli-aqua` (installed by the Ambient Quality Agent extension from `google/adk-recipes`, pinned by `--ref`; `adk-release-engineering` decides whether its insights gate a release) |

The names above were read from the published catalogue on 21 October 2026.
When Google's router is installed, confirm a name against the current
catalogue before writing it into a goal (skills are renamed and added); the
router's own rule not to name a skill it has not seen in the catalogue applies
to it, not to this table, which is a dated reference.

Google's skills assume an operator at a terminal: several open with global
`gcloud config set`, deploy public by default or download keys. The goal's
depth and floor (scoped flags, platform identity, private by default,
approval per scope) still govern; the product skill supplies the commands.

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

For each goal record outcome, the contracts it proves (C IDs from the design),
scope, integration points, ADK/GCP choices, prerequisites and dependency IDs,
skills, acceptance cases and evidence tier, and the resources it creates that
charge while provisioned (idle cost with pricing date, cleanup command,
verification, and the teardown goal or cost contract that owns them; the
[resource cost ledger](resource-costs.md) supplies the rows). Each acceptance case names the
contract it proves, so evidence lands against a contract rather than only
against the goal; a critical contract no goal cites is a gap to record.
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

## Plan a portability goal when the scope gate asks for one

Only when the scope gate's lock-in question was answered yes. When it was no,
the plan has no portability goal, no ticket and no load of
`adk-portability-planning`. A yes changes no architecture: the design stays
GCP + Google ADK, and the assessment is a separate document beside it. Data
residency is not this question; the governance jurisdiction screen owns it.

- **Placement:** phase 1 by default, independent of the build goals:
  `blocked_by: []`, because it depends only on the design (a draft is
  enough; the assessment carries its open decisions), and no build goal
  waits for it, not even to order one person's work: `check_schedule.py`
  reports a goal other than a presentation that lists it in `blocked_by`.
  `plan_status.py --gate` skips it, like a review or teardown, so an
  unfinished assessment never holds the phase. A presentation goal depends
  on it only when that review must answer the concern; otherwise the review
  lists it under `mentions_only`. The journey check is transitive: a review
  that depends on the portability goal and on built work still needs its
  journey goal; one that depends only on the portability goal needs none.
- **Estimate:** human hours, hands-on and review, like other document goals:
  reading the design and plan, checking provider sources, and the stakeholder
  read-through. In a statement of work it belongs to a deliverable like any
  goal in a priced phase.
- **Fields:** `type: portability`, `primary_skill: adk-portability-planning`,
  `contracts: []`, `security: []`, `touches: [docs/portability/<topic>.md]`
  (the gate flags changed files no ticket lists), and `docs:`
  `adk-portability-planning/references/principles.md` plus the reference for
  each target the scope gate named: `aws.md`, `azure.md`, and
  `agent-frameworks.md` for another agent framework or model portability.
- **Ticket:** written even when the other goals stay goals-only, so the
  session that runs it has the acceptance and the no-code boundary in one
  file. In the compact form (a one-person proof of concept with no plan file)
  the portability goal is a goal line in the design file, and the ticket's
  `plan` field, like `--plan` in its verification, points at the design file.
- **Outcome:** "Read the accepted GCP + Google ADK architecture and plan.
  Produce a high-level portability assessment for <the targets and dimensions
  the scope gate recorded>, for <who raised the concern>, at
  `docs/portability/<topic>.md`. Keep it separate from the baseline. Do not
  implement an alternative application or change the approved GCP
  implementation."
- **Recommendations:** the assessment's optional recommendations for the
  current build (a boundary worth adding now, for example) are proposals.
  Each becomes a ticket only after a designer checkpoint approves it, with
  the specialist the assessment names as primary skill and the design's
  contracts in its acceptance; the portability ticket writes neither tickets
  nor code.

Acceptance, each item tagged `(deliverable)`, which `check_tickets.py`
accepts on portability tickets in place of a contract ID:

- [ ] A1 THE assessment docs/portability/<topic>.md SHALL exist and check_portability.py SHALL exit 0 with --design and --plan (deliverable)
- [ ] A2 THE assessment SHALL cover the targets recorded in the scope gate and each of the five dimensions, assessed or marked not a concern with a reason (deliverable)
- [ ] A3 EVERY provider or framework claim that drives a classification or risk SHALL cite an official source with its read date (deliverable)
- [ ] A4 THE design document SHALL NOT change and no other goal's scope SHALL change; `git hash-object docs/architecture/<topic>.md` prints the value recorded in Evidence before the assessment was written (deliverable)
- [ ] A5 THE skill SHALL NOT write application code, infrastructure code or new tickets; improvements to the current build appear only under Optional recommendations with their specialist (deliverable)

Verification, automated, with `SKILL_DIR` resolved to the
`adk-portability-planning` directory (exit 0 expected):

```bash
python3 "$SKILL_DIR/scripts/check_portability.py" docs/portability/<topic>.md \
  --design docs/architecture/<topic>.md --plan docs/plans/<topic>.md
git hash-object docs/architecture/<topic>.md   # equals the value in Evidence
```

Fill `<topic>` when writing the ticket, or `check_tickets.py` reports it as
an unfilled placeholder. `git hash-object` works whether or not the design is
committed, so the ticket is `ready` from the start. Verification, manual:
none.

The ticket's front matter, for a design whose scope gate named AWS and
another agent framework:

```yaml
---
goal: G02
title: Portability assessment for the support assistant
design: docs/architecture/support.md
plan: docs/plans/support.md
primary_skill: adk-portability-planning
supporting_skills: []
docs: [adk-portability-planning/references/principles.md, adk-portability-planning/references/aws.md, adk-portability-planning/references/agent-frameworks.md]
blocked_by: []
touches: [docs/portability/support.md]
parallel_safe: yes
contracts: []
companion_skills: []
security: []
design_system: none
contract_deltas: []
pass_to_pass: []
phase: 1
type: portability
profile: MVP or pilot
estimate:
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  handoff: none
  calendar_waits: none
owner: Ana
status: ready
---
```

## Continue the work

The default needs nothing else installed. Each goal in the plan carries its own
run prompt, and `adk-engineer` reads the goal's `Primary skill` and
`Supporting skills` lines, loads them and performs the authorized work. It
also reads a goal's companion skills, design system and security rules:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
/adk-engineer Continue the next ready goal in docs/plans/<topic>.md.
```

When the user wants one file per unit of work, for a tracker or for parallel
sessions, copy each ready goal into the [ticket template](../assets/ticket-template.md)
under `docs/tickets/<topic>/`. Each ticket ends with its own run prompt, and the
agent that carries it out fills in its Evidence section.
Write one ticket per goal of the phase, not only for the first: `blocked_by`
carries the sibling goals it waits for, and `status: ready` means nothing
outside the phase blocks it. `touches` lists the paths a ticket expects to
write, so tickets whose lists do not overlap can run at the same time, each in
its own worktree; `plan_status.py` names those groups from actual statuses and
`adk-engineer`'s ticket lifecycle reference gives the worktree and merge
procedure. Statuses and evidence live in the tickets, never in a shared plan
table that every parallel session would edit. One lead method runs a ticket: `adk-engineer` in
this session, or an installed alternative such as Superpowers'
subagent-driven-development, which replaces it rather than joining it;
companions such as an installed `wizard` skill take the steps only a person
can do (IAM grants, secret values, consent screens). A project's standing
instructions for coding agents (pins, test commands, the evidence directory,
the design's invariants) belong in a root `AGENTS.md` with a one-line
`CLAUDE.md` include, written when the project first needs them rather than as
a goal of every plan; `adk-engineer`'s composition reference names the
convention.

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
