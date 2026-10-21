# Google's skills collection compared with this toolkit — 21 October 2026

## Scope and conclusion

This is a file-level review of a local snapshot of
[google/skills](https://github.com/google/skills) (Apache-2.0; 167 skills
under `skills/cloud`, `skills/developers`, `skills/analytics`, `skills/ads`
and `skills/identity`, downloaded 21 October 2026, no commit recorded)
against the 22 packages in this repository. Six readers each compared one
cluster of Google skills with the specialists they overlap. Facts that
changed a specialist's text were checked against Google's current
documentation where the specialist records a URL; everything else is cited
as "Google's `<skill>` skill, read 21 October 2026" and labelled vendor
guidance. No Google skill was executed and no cloud resource was touched.

**Conclusion.** The collection is product operations: gcloud recipes, IAM
and deny policies, Cloud Run and GKE administration, Terraform alert
policies, PromQL, trace and log queries, database administration, and the
Agent Platform services. About ten skills are agent-specific
(`agent-platform-*`, `google-cloud-solution-build-deploy-agents`,
`google-cloud-solution-multi-agent-security`,
`apigee-agent-gateway-governance`, `api-gateway-mcp-server`,
`google-cloud-solution-agentic-ai-bidirectional-streaming`); none is about
building an ADK application. Google's ADK lifecycle skills live in
[Agents CLI](agents-cli-comparison-2026-09-23.md). So the right relation is a
division of labour: this toolkit's specialist decides what the application
needs, Google's skill operates the product. Routing is the default; a
bounded set of facts was imported because they change an ADK decision.

## How the collections connect

- `finding-google-skills` fetches
  `https://raw.githubusercontent.com/google/skills/main/index.json`
  (a generated list of `name`, `description`, `entrypoint`) and then at most
  three matching `SKILL.md` files, once per session, never persisted. It does
  not detect installed skills. A plan can therefore name a product skill
  without the user installing all 167.
- The engineer's composition reference now carries a specialist-to-product-skill
  table; the designer's handoff carries the same by implementation route; a
  goal's supporting skills may read `google/skills:<name> (purpose)`;
  `adk-engineer` treats a missing one like a missing specialist (install
  command or router, continue local work, product step recorded as a
  prerequisite). Two scenario cases in `evals/scenarios.json` describe the
  expected behaviour.
- Packaging: Google's frontmatter (`name`, `description`, `metadata.version`,
  `metadata.category`, occasionally `compatibility` and `allowed-tools`)
  passes this repository's validator unchanged. Their only CI is a weekly
  lychee link check. Two marketplace manifests (`.claude-plugin`,
  `.agents/plugins`) and a bundled `google-cloud-developer` plugin exist; not
  adopted here.

## What each cluster found

### Deployment, platform and optimisation

Read: `google-cloud-solution-build-deploy-agents`, `agent-platform-deploy`,
`agent-platform-endpoint-management`, `agent-platform-troubleshooting`,
`agent-platform-inference`, `cloud-run-basics`, `cloud-run-alert-configuration`,
`google-agents-cli-onboarding`, `gcloud`, `cloud-build-basics`.

Imported into `deploy-adk-on-google-cloud` and `optimise-adk-on-google-cloud`:
the Agent Identity mechanism for Agent Runtime (`.agent_engine_config.json`,
principal format, auto-granted and baseline roles, the 401 token-sharing
failure behind a gateway), which replaces the sentence that a dedicated
runtime identity was "not implemented"; deployer and build role lists for
Cloud Run; Direct VPC egress over the connector and the Cloud NAT
requirement; the one-flag IAP deploy; the Reasoning Engine stderr log name
and crash signatures; the n-tier ingress settings; Cloud Run capacity metric
names; the thinking-token `MAX_TOKENS` gotcha and Dynamic Shared Quota fact;
Cloud Build trigger immutability facts for `adk-release-engineering`.

Routed: Agent Gateway and egress-policy diagnosis
(`agent-platform-troubleshooting`), Cloud Run alert Terraform, self-hosted
open models and endpoints, raw model-call SDK shapes, any new `gcloud`
command (`gcloud` skill's leaf-help rule), Cloud Build triggers.

Left out: global `gcloud config set` and `gcloud auth login` boilerplate,
public-by-default deploy examples, Google-internal tooling that leaked into
the troubleshooting skill, eval-harness directives, a sample requirement
string that pins ADK below 2.0.

### Observability

Read: the `cloud-monitoring-*` set, `cloud-trace-querying`, the
`cloud-logging-*` set, `google-cloud-slo-alert-configuration`,
`agent-platform-alert-configuration`, `cloud-run-alert-configuration`.

Imported into `adk-agent-observability`: Cloud Monitoring names of the ADK
metrics and their PromQL forms; the fast and slow burn-rate queries for the
invocation SLI; the trace-SQL tool and model error-rate query over
`_AllSpans` with its linked-dataset prerequisite; the three Online Monitor
metric IDs and the `ALIGN_PERCENTILE_50` rule; the Reasoning Engine
availability SLI; Cloud Run host-level saturation and OOM metrics; trace
filter grammar; Cloud Run log IDs; notification-channel and sink gotchas.

Routed: Terraform alert policies, SLO wizards, PromQL validation, dashboard
widgets, notification channels, trace search, log queries, sinks and buckets.

Left out: a content-capture value Google's own ADK page contradicts, the
legacy Cloud Trace path (kept, labelled legacy), content capture without
redaction, a p95 token-size alert presented as spend, invented OTel GenAI
attributes, unsourced thresholds.

### Security, identity, gateways and interoperability

Read: `google-cloud-recipe-auth`, the four `iam-helper-*` skills,
`google-cloud-solution-multi-agent-security`,
`apigee-agent-gateway-governance`, `api-gateway-mcp-server`,
`api-gateway-backend-security-and-rate-limiting`, `google-cloud-scc-query`,
`google-cloud-scc-remediation`, `google-cloud-waf-security`.

Imported into `adk-agent-security`, `adk-tool-auth-and-secrets`,
`adk-agent-interoperability` and `protect-adk-sensitive-data`: Agent Gateway
as an enforcement point whose egress policy gates MCP calls per tool name and
read-only hint outside the model, with its limits; the Agent Identity
principal format and the viewer role the service agent needs; the 401
token-sharing diagnosis as a trade-off; the remote-MCP-on-API-Gateway
contract facts (unauthenticated `tools/list`, header parameters becoming
model-controlled arguments, HTTP 200 with a JSON-RPC error); the
`X-Apigateway-Api-Userinfo` assertion and the undisableable gateway
hostname; IAM deny policies as a model-proof boundary; gateway-level Model
Armor and semantic-cache caveats; Security Command Center finding classes;
the `agentplatform` client rename.

Routed: writing or replaying IAM bindings, 403 diagnosis, break-glass
access, Agent Gateway provisioning, Apigee metering, hosting REST as MCP,
SCC triage.

Left out: a fail-open authorization extension, confirmation-free delivery,
a static user JWT in MCP connection headers, a script that enables an API
without approval, an ADK pin below our CVE floor.

### Evaluation, prompts and models

Read: `agent-platform-eval-flywheel`, `agent-platform-prompt-management`,
`agent-platform-model-registry`, `agent-platform-tuning`,
`agent-platform-tuning-management`, `agent-platform-migrate-from-ai-studio`,
`gemini-api`, `gemini-interactions-api`, `gemini-agents-api`,
`gemini-live-api`.

Imported into `adk-agent-evaluation`, `adk-model-and-output-contracts`,
`adk-agent-instructions` and `adk-release-engineering`: the managed scorer's
export and judge-pinning contract (full resource name or HTTP 400, sampling
count bounds, the superseded import path's failure mode); unversioned metric
names resolving to the latest version; the rubric builder shape and a
custom-metric gotcha; a metric-by-agent-type starting table; the ADK
session-to-dataset mapping; Live API constraints on output schemas and
session resumption; the non-text model families the lifecycle table does not
cover; the tunable-model lag; the `{{var}}` placeholder clash between
managed prompts and ADK templating.

Routed: fine-tuning and tuning jobs, evaluating non-ADK models, direct
Gemini calls from tools, server-side conversations and managed agents, raw
Live API clients, the prompt registry, the API-key-to-enterprise migration.

Left out: temperature 0 as a flakiness fix, a judge default that retires on
Vertex this month, prompt-shouting fixes, summary-only comparisons without
holdout or calibration, stale Live model IDs, a deprecated prompt SDK.

### Data, memory, retrieval and SQL

Read: `agent-platform-rag-engine-management`, `alloydb-basics`,
`cloud-sql-basics`, `bigquery-basics`, `bigquery-ai-ml`, `bigquery-bigframes`,
`bigquery-optimization`, `bigquery-troubleshooting`, `spanner-basics`,
`bigtable-basics`, `firebase-basics`, `cloud-databases-onboarding`,
`google-cloud-storage-basics`, `google-cloud-storage-bucket-architect`,
`google-cloud-solution-hybrid-search-alloydb`,
`google-cloud-solution-rag-enterprise-search-gke-sqldb`.

Imported into `adk-sql-agent-engineering` and `adk-memory-architecture`: the
named BigQuery cost controls (`maximum_bytes_billed`, dry run, per-user
quota, the 10 MiB per-table minimum, row-level security hiding bytes
billed); `require_partition_filter` DDL and the partition-column lookup; the
full `AI.*`, `ML.*`, `VECTOR_SEARCH` and `OBJ.GET_ACCESS_URL` surface for
the SQL guard; change history as a completeness watermark; remote MCP
facts (`roles/mcp.toolUser`, read-only endpoint, cost attribution label);
managed hybrid search and the embedding task-type asymmetry; RAG Engine
call shapes; Cloud SQL and AlloyDB IAM roles and the control-plane user
step for a database-backed session service; backup and PITR windows that
outlive an erasure; the Cloud Storage bucket contract; the Model Armor
floor-setting side effect; Spanner Queues as an outbox option.

Routed: partitioning and reservations, slow or expensive jobs, dataset and
instance provisioning, IAM database users, corpus discovery, bucket IAM
and signed URLs.

Left out: a deprecated RAG SDK path with in-line `pip install`, key files
and global config in prerequisites, passwords on the command line,
marketing comparisons, raw SQL and user-ID logging, LangChain stores
presented as session services.

### Architecture, foundations and meta

Read: `google-cloud-solution-architecture`, `google-cloud-recipe-onboarding`,
`google-cloud-recipe-foundation-builder`, the five `google-cloud-waf-*`
pillars, `application-design-center-design-deploy`, `finding-google-skills`,
`retrieving-developer-knowledge`, `agent-platform-skill-registry`,
`google-cloud-solution-agentic-ai-bidirectional-streaming`,
`google-cloud-solution-n-tier-serverless-web-app`, `assuredworkloads-*`,
`workload-manager-basics`, and the repository's packaging.

Imported into `adk-system-designer` and `adk-frontend-integration`: the
Well-Architected validation checklists rewritten as design checks; RTO and
RPO, game-day, HA-per-environment and committed-use questions; a project
foundation section (organisation-managed account test, org policies that
break an ADK deployment, billing check, per-goal API enablement, VPC
Service Controls as a design input); the deprecation check and
alternatives-considered columns; the bidirectional streaming reference
architecture; the Developer Knowledge lookup discipline; a one-line
Application Design Center pointer.

Routed: pillar reviews, multi-product solution architecture, onboarding and
foundations, assured workloads.

Left out: a remediation routine that grants whole admin groups on any
permission error, a connector-first networking recommendation the n-tier
skill contradicts, eval-harness meta-instructions, survey-style questions.

## Limits

A local snapshot without a recorded commit; Google's catalogue changes
weekly. Facts marked vendor guidance were not exercised against a project.
Routing was described in two scenario cases and one fresh-agent trial (see
the testing record named in the README entry for this date); it was not
measured across clients. The duplicated mapping (engineer by specialist,
designer by route) is deliberate, because packages must stay portable, and
both must change together.
