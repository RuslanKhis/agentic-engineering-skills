# Working with other skill collections

Read this when another collection supplies the project's lifecycle, a goal
names a `google/skills:<name>` supporting skill, or the user asks to combine
skills. Keep one development workflow for the task and use the selected ADK
specialist for the application decisions. Additional collections are
optional; their presence does not expand the user's request.

## Establish the project and scope

Read the relevant project instructions and existing design before choosing a
workflow. An `agents-cli-manifest.yaml` identifies an Agents CLI project; inspect
its declared agent directory, framework, version and deployment target alongside
the actual code. Read `.agents-cli-spec.md` when present and relevant. A manifest
is evidence of project conventions, not permission to execute platform commands.

Google's own page on coding ADK with an AI assistant names three ways to
give a coding agent ADK context (google/adk-docs `docs/tutorials/coding-with-ai.md`,
commit 0ac7ec6, read 2026-10-23): the Agents CLI skills installed by
`uvx google-agents-cli setup` (lifecycle and coding guidelines,
scaffolding, evaluation, deployment, publishing, tracing, an API quick
reference and docs index), the ADK Docs MCP server a coding tool can
query, and the machine-readable docs index in the `llms.txt` convention.
This collection sits above them as the decision layer: when a project has
them installed, route the mechanism to them and keep the decision here. A
project's own standing instructions for coding agents belong in an
`AGENTS.md` at the repository root, the open plain-Markdown format most
coding tools read (agentsmd/agents.md commit d001185, MIT, read
2026-10-23: a "README for agents" with sections such as environment tips,
test commands and pull-request rules), paired with a one-line `CLAUDE.md`
that includes it for tools that read only that file; `adk-system-designer`
decides what goes in it.

| Situation | How to proceed |
| --- | --- |
| User chose the Agents CLI lifecycle for a new project | Use the installed `google-agents-cli-workflow` for the requested lifecycle phases (understand with its spec gate, study recipes, scaffold, build, evaluate, deploy, publish, observe) and this toolkit's specialist for the feature. Reuse the agreed design; a design from `adk-system-designer` answers its spec phase. |
| Focused change in an existing Agents CLI project | Select the primary ADK specialist. Preserve the manifest, generated server/transport, dependency pins, model and infrastructure ownership. Consult the relevant installed Google skill for the specific interface or command needed. |
| Existing ADK application without Agents CLI | Work in its current layout and environment. Adopting a scaffold is a separate requested change; a downloaded recipe can be studied without converting the application. |
| User chose Matt Pocock's `tdd`, `diagnosing-bugs` or another process skill | Follow that installed process and use the ADK specialist's domain guidance. Keep the existing task and design instead of starting another interview or ticketing workflow. |
| User hands over a ticket or plan goal written by `adk-system-designer` | Read the ticket or goal, use its named primary and supporting skills, verify its acceptance cases and write the Evidence section. No other collection is needed unless it names companion skills (next row). |
| A ticket or goal names companion skills (FastAPI's bundled skill, `shadcn`, Vercel's React rules, `playwright-cli` and others) | Load each at the pin in the project's `AGENTS.md` for library syntax and UI craft inside the ticket's constraints; a missing one is a setup step with its install line, not applied guidance. This toolkit's specialist decides identity, ownership, security rules and the stream contract; a companion decides library syntax for its pinned version; the ticket's DESIGN.md decides between UI companions, including copy case. A companion's advice that conflicts with a constraint or rule loses and is noted in Evidence. |
| User continues a system-design handoff | Read its canonical design and goal plan. Use Wayfinder for substantial unresolved decisions when chosen; use the adopted spec/ticket workflow or a specialist for ready build goals. Keep one authoritative record of decisions and progress. |

State the division of work briefly. For example: “I’ll use the memory specialist
for storage and user isolation, and the existing Agents CLI conventions for
integration.” Load only the optional skills relevant to that division.

## Select optional guidance

- `google-agents-cli-adk-code`: ADK API cheatsheets (agents, tools, callbacks,
  state, the graph Workflow API, Live, managed agents) and the recipe
  catalogue in `google/adk-recipes` (memory, approval, RAG, safety plugins,
  ambient triggers, a scheduled production-trace evaluator). That
  repository's README says recipes are "for demonstration and as starting
  points, not production use" (google/adk-recipes be63596, `README.md`, read
  2026-10-22): `core/` holds the curated patterns, `contrib/` deployable
  vertical agents, `plugins/` installable skills with an `EVAL.yaml`. A change
  that lifts a recipe pattern repeats that disclaimer in its Evidence section
  and names the controls the recipe lacks. Two recipes carry their own Apache
  LICENSE (`core/python/cross-session-memory`,
  `contrib/python/brand-aligned-presentations`); check the folder before
  copying code.
- google/adk-python's own `.agents/skills/` (`adk-agent-builder`,
  `adk-architecture`, `adk-debug`, `adk-review`, `adk-unit-design` and
  others; main ed76f94, read 2026-10-22) are the ADK maintainers' skills for
  building and testing agents against the SDK's current API; they are not
  installed with the package. When a project has adopted them, they operate
  the SDK's shapes and this toolkit's specialist still decides the contracts
  and the evidence; the flake habits in `adk-agent-builder`'s testing
  reference are already carried in adk-agent-evaluation.
- `agents-cli-aqua`: shipped into `.agents/skills/` by the Ambient Quality
  Agent extension from `google/adk-recipes`
  (`agents-cli extension add google/adk-recipes#core/python/ambient-quality-agent
  --ref ambient-quality-agent/v0.1.0`), not by `google/skills`; operates the
  scheduled evaluator over production traces that `adk-release-engineering`
  decides how to use (its production-feedback reference).
- `google-agents-cli-scaffold`: a requested project creation, enhancement or
  upgrade; its own text says to run the workflow's spec phase first.
- `google-agents-cli-eval`: Agents CLI dataset, trace, metric and result
  formats, user simulation, Live mode, `compare`, `analyze`, `submit`.
- `google-agents-cli-deploy`: the adopted delivery mechanism, `deploy` flags
  and the generated Terraform's ownership.
- `google-agents-cli-observability`: telemetry environment, completion
  uploads and BigQuery analytics infrastructure.
- `google-agents-cli-publish`: requested registration in Gemini (formerly
  Gemini Enterprise) with `agents-cli publish gemini`, and Agent Registry
  commands.

Discover these through the coding agent's available-skills catalogue. Read the
selected skill's instructions before relying on it. Google's
`google-agents-cli-onboarding` skill, published in the `google/skills`
collection, installs the CLI (`uvx google-agents-cli setup`) and points at
these same skills; it is an entry to them, not a seventh workflow. If an optional collection
is absent, report that limitation and continue work supported by this toolkit;
offer installation only when its capability is needed. This differs from a
missing primary specialist, which the entry skill handles explicitly.

Three of this toolkit's specialists overlap with Google's lifecycle skills in
scope but not in role. `adk-agent-observability` decides which signals, gates,
SLIs and exporters the application needs; `google-agents-cli-observability`
provisions the generated telemetry infrastructure. `adk-release-engineering`
designs the eval gate, pinning, migration and rollback bundle;
`google-agents-cli-deploy` and `google-agents-cli-eval` run the generated
pipeline and the Agents CLI evaluation commands. `adk-agent-interoperability`
owns the agent card and MCP or A2A contracts; `google-agents-cli-publish`
performs the requested Gemini Enterprise registration. When both are installed,
this toolkit's skill decides and Google's skill operates the adopted mechanism;
neither replaces the other.

Google's code skill points to its full workflow, including scaffolding and live
evaluation. Honour the user's actual task when combining those instructions.
Studying a recipe means reading its files; cloning it is a network action
under the same authorisation as any fetch, and the installed skill's copy of
the catalogue often answers the question without a clone. Google's rule to run
everything through `uv` governs its generated project's commands; running the
project's own test command with the interpreter at hand, and saying which one
ran, is not a conflict.
For a local feature request, complete the local change and report any separate
platform prerequisite. A skill's command example is not authorisation to install
tools, change cloud resources or run paid evaluations.

## Use Google's product skills for the mechanism

Google's [skills collection](https://github.com/google/skills) (`google/skills`,
Apache-2.0) holds about 170 skills for Google products: gcloud recipes, IAM
and deny policies, Cloud Run and GKE operations, Terraform alert policies,
PromQL, trace and log queries, database administration, Agent Platform
services. About ten are agent-specific; none covers building an ADK
application. The division is the same as with Agents CLI: this toolkit's
specialist decides what the application needs, and Google's skill operates
the product that provides it.

A goal or ticket names such a skill in its supporting skills as
`google/skills:<name>` with its purpose, for example
`google/skills:cloud-run-basics (service and ingress provisioning)`. Treat it
like a missing specialist, not a blocker: look for `<name>` in the host's
catalogue or the sibling directory; if it is absent, show

```bash
npx skills@latest add google/skills --skill <name>
```

or, when Google's `finding-google-skills` router is installed, ask it for the
product by name (it fetches the published catalogue and that one skill on
demand). Continue the local work meanwhile and record the product step as a
prerequisite in the Evidence section. Its command examples are not
authorisation: provisioning, IAM changes, API enablement and paid runs still
need the user's approval for that scope.

| Our specialist | Google skills to pull in | When |
| --- | --- | --- |
| `adk-system-designer` | `google-cloud-waf-reliability`, `-security`, `-cost-optimization`, `-operational-excellence`, `-performance-optimization`; `google-cloud-solution-architecture`, `google-cloud-solution-build-deploy-agents` | Production or MVP profile review per pillar; the agent is one component of a larger multi-product system |
| `adk-system-designer`, `deploy-adk-on-google-cloud` | `google-cloud-recipe-onboarding`, `google-cloud-recipe-auth`, `gcloud`; `google-cloud-recipe-foundation-builder`, `assuredworkloads-*` | First goal that touches a project with no project or billing yet; any new `gcloud` command; a new organisation or regulated data residency |
| `deploy-adk-on-google-cloud` | `cloud-run-basics`, `gke-basics`, `gke-app-onboarding`, `google-cloud-global-frontend-configuration`, `google-cloud-solution-n-tier-serverless-web-app`, `cloud-build-basics`, `agent-platform-troubleshooting` | The chosen host; a public load balancer or Cloud Armor in front; private tiers; CI on Cloud Build; a 403 or startup failure behind an Agent Gateway |
| `adk-agent-observability` | `agent-platform-alert-configuration`, `cloud-run-alert-configuration`, `google-cloud-slo-alert-configuration`, `cloud-monitoring-*`, `cloud-trace-querying`, `cloud-logging-*` | SLIs decided and the alert policy, dashboard, query, sink or notification channel must now be built |
| `adk-tool-auth-and-secrets`, `adk-agent-security` | `iam-helper-for-policy-management`, `-policy-simulator`, `-troubleshooting`, `-privileged-access-management`; `google-cloud-solution-multi-agent-security`, `apigee-agent-gateway-governance`; `google-cloud-scc-query`, `google-cloud-scc-remediation` | An IAM binding or deny policy to write or replay; a 403 on the runtime identity; break-glass access; Agent Gateway or Model Armor at the perimeter; Security Command Center findings |
| `adk-agent-interoperability` | `api-gateway-mcp-server`, `api-gateway-backend-security-and-rate-limiting`, `gemini-agents-api`, `agent-platform-skill-registry`; `google-agents-cli-publish` from Agents CLI | Hosting a REST API as a remote MCP server; registering agents or skills on Agent Platform; `agents-cli publish gemini` and Agent Registry commands in an Agents CLI project |
| `adk-memory-architecture`, `adk-sql-agent-engineering` | `cloud-sql-basics`, `alloydb-basics`, `bigquery-basics`, `bigquery-optimization`, `bigquery-troubleshooting`, `bigquery-ai-ml`, `agent-platform-rag-engine-management`, `google-cloud-storage-basics` | The chosen store needs provisioning, IAM database users, partitioning, cost diagnosis, a corpus smoke test or a bucket |
| `adk-agent-evaluation`, `adk-release-engineering` | `agent-platform-eval-flywheel`, `cloud-build-basics` | The managed scorer or Cloud Build is the adopted mechanism |
| `adk-model-and-output-contracts` | `gemini-api`, `agent-platform-tuning`, `agent-platform-inference` | A tool calls Gemini directly; fine-tuning; a self-hosted open model endpoint |
| `adk-frontend-integration` | `google-cloud-solution-agentic-ai-bidirectional-streaming`, `gemini-live-api` | Audio or video streaming in the journey |
| `optimise-adk-on-google-cloud` | `gke-cost-optimization`, `gke-workload-scaling`, `google-cloud-networking-observability` | A GKE host; packet loss or Private Service Connect latency |
| `adk-release-engineering`, `adk-agent-evaluation` | `agents-cli-aqua` (from the AQuA extension in `google/adk-recipes`, named in a goal as `google/adk-recipes:agents-cli-aqua`) | A scheduled evaluator over production traces is adopted after launch; the specialist decides whether its insights gate a release |

When Google's sources disagree with each other, settle it in this order: the
official product documentation decides a platform fact; the CLI's release
notes and source decide what a command does, over the skill text that
describes it; and this toolkit records the divergence beside the fact, so the
next reader does not repeat the tie-break. The deploy and interoperability
references carry three such records at 1.11.0 (the Agent Identity baseline
role, the invoker role for Gemini registration, the dry-run semantics).

Google's skills were written for an operator at a terminal. Keep this
toolkit's rules where they differ: pass `--project` and `--region` on each
command instead of `gcloud config set`, use platform identity instead of
downloaded keys, deploy private (`--no-allow-unauthenticated`) by default, and
enable an API or grant a role only within an approval the user gave for that
scope. The `CLOUDSDK_METRICS_REQUEST_ATTRIBUTION` prefix in their examples is
optional telemetry attribution, not a requirement.

## Check the combined result

Keep deterministic application checks and real-model evaluations distinct.
Google's workflow says not to write behavioural unit tests; this toolkit's
scripted-model Runner tests assert application effects (a forbidden action
never runs, a record stays owner-scoped), not response wording, and remain
part of the change.
Scripted-model Runner tests can verify identity, consent and stored effects;
live evaluations measure model-dependent choices. Agents CLI results
(`artifacts/grade_results/results_<timestamp>.json`) and
native ADK evaluation artifacts have different contracts, so verify the producer
and schema before choosing a checker.

Use the existing deployment path and account for each telemetry destination when
those concerns are in scope. Preserve ownership and configuration that the
feature does not need to change. Finish with the actual checks, any workflow
conflict that remains, and the precise prerequisite for unverified work.
