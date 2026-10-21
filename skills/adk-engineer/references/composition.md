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

| Situation | How to proceed |
| --- | --- |
| User chose the Agents CLI lifecycle for a new project | Use the installed `google-agents-cli-workflow` for the requested lifecycle phases and this toolkit's specialist for the feature. Reuse the agreed design. |
| Focused change in an existing Agents CLI project | Select the primary ADK specialist. Preserve the manifest, generated server/transport, dependency pins, model and infrastructure ownership. Consult the relevant installed Google skill for the specific interface or command needed. |
| Existing ADK application without Agents CLI | Work in its current layout and environment. Adopting a scaffold is a separate requested change; a downloaded recipe can be studied without converting the application. |
| User chose Matt Pocock's `tdd`, `diagnosing-bugs` or another process skill | Follow that installed process and use the ADK specialist's domain guidance. Keep the existing task and design instead of starting another interview or ticketing workflow. |
| User hands over a ticket or plan goal written by `adk-system-designer` | Read the ticket or goal, use its named primary and supporting skills, verify its acceptance cases and write the Evidence section. No other collection is needed. |
| User continues a system-design handoff | Read its canonical design and goal plan. Use Wayfinder for substantial unresolved decisions when chosen; use the adopted spec/ticket workflow or a specialist for ready build goals. Keep one authoritative record of decisions and progress. |

State the division of work briefly. For example: “I’ll use the memory specialist
for storage and user isolation, and the existing Agents CLI conventions for
integration.” Load only the optional skills relevant to that division.

## Select optional guidance

- `google-agents-cli-adk-code`: installed ADK interfaces and reference recipes.
- `google-agents-cli-scaffold`: a requested project creation or scaffold change.
- `google-agents-cli-eval`: Agents CLI dataset, trace, metric and result formats.
- `google-agents-cli-deploy`: the adopted delivery mechanism and generated infrastructure.
- `google-agents-cli-observability`: telemetry setup and export destinations.
- `google-agents-cli-publish`: requested Gemini Enterprise registration.

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
| `adk-agent-interoperability` | `api-gateway-mcp-server`, `api-gateway-backend-security-and-rate-limiting`, `gemini-agents-api`, `agent-platform-skill-registry` | Hosting a REST API as a remote MCP server; registering agents or skills on Agent Platform |
| `adk-memory-architecture`, `adk-sql-agent-engineering` | `cloud-sql-basics`, `alloydb-basics`, `bigquery-basics`, `bigquery-optimization`, `bigquery-troubleshooting`, `bigquery-ai-ml`, `agent-platform-rag-engine-management`, `google-cloud-storage-basics` | The chosen store needs provisioning, IAM database users, partitioning, cost diagnosis, a corpus smoke test or a bucket |
| `adk-agent-evaluation`, `adk-release-engineering` | `agent-platform-eval-flywheel`, `cloud-build-basics` | The managed scorer or Cloud Build is the adopted mechanism |
| `adk-model-and-output-contracts` | `gemini-api`, `agent-platform-tuning`, `agent-platform-inference` | A tool calls Gemini directly; fine-tuning; a self-hosted open model endpoint |
| `adk-frontend-integration` | `google-cloud-solution-agentic-ai-bidirectional-streaming`, `gemini-live-api` | Audio or video streaming in the journey |
| `optimise-adk-on-google-cloud` | `gke-cost-optimization`, `gke-workload-scaling`, `google-cloud-networking-observability` | A GKE host; packet loss or Private Service Connect latency |

Google's skills were written for an operator at a terminal. Keep this
toolkit's rules where they differ: pass `--project` and `--region` on each
command instead of `gcloud config set`, use platform identity instead of
downloaded keys, deploy private (`--no-allow-unauthenticated`) by default, and
enable an API or grant a role only within an approval the user gave for that
scope. The `CLOUDSDK_METRICS_REQUEST_ATTRIBUTION` prefix in their examples is
optional telemetry attribution, not a requirement.

## Check the combined result

Keep deterministic application checks and real-model evaluations distinct.
Scripted-model Runner tests can verify identity, consent and stored effects;
live evaluations measure model-dependent choices. Agents CLI JSON results and
native ADK evaluation artifacts have different contracts, so verify the producer
and schema before choosing a checker.

Use the existing deployment path and account for each telemetry destination when
those concerns are in scope. Preserve ownership and configuration that the
feature does not need to change. Finish with the actual checks, any workflow
conflict that remains, and the precise prerequisite for unverified work.
