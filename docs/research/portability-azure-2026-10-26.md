# Azure alternatives for a GCP and ADK design — 26 October 2026

## Scope

How the GCP responsibilities in
[`gcp-decisions.md`](../../skills/adk-system-designer/references/gcp-decisions.md)
would map to Azure, for the optional `adk-portability-planning` skill. GCP and
ADK stay the primary build path. This is a high-level note on architectural
and operational differences, read from Microsoft Learn, Azure and Foundry
announcements, and the ADK docs on 26 October 2026. Nothing was deployed or
run. No prices or effort figures are given; "pricing shape" means what is
metered, never a rate.

## Summary

| # | GCP responsibility | Plausible Azure option and status | Meaningful difference | Migration concern | Portability |
| --- | --- | --- | --- | --- | --- |
| 1 | Hosting: Cloud Run, GKE, Agent Runtime | Container Apps (GA); AKS (GA); App Service (GA); Foundry Agent Service hosted agents (GA, announced 9 July 2026) | Container Apps has revisions, traffic splitting, KEDA scaling and scale to zero (not when scaling on CPU or memory). Hosted agents run your container in a per-session VM-isolated sandbox behind a Responses, Invocations or A2A endpoint, billed on CPU and memory across active sessions; one version serves 100% of traffic, no splitting | Cloud Run and GKE images move as they are. Agent Runtime does not: hosted agents expect Microsoft's protocol libraries (Python or C#), and ADK is not a named framework | Moderate: plain containers move cheaply; the managed-runtime path is a re-platform |
| 2 | Model inference: Gemini on Vertex AI | Foundry Models: Azure OpenAI and other "sold by Azure" models; partner models (Anthropic, Mistral, Meta, Cohere) through Azure Marketplace | No Gemini model appears in the Foundry catalog pages read. Deployment types (Global, Data Zone, Regional; Standard per token or Provisioned) set where prompts are processed. Partner models carry the provider's terms and per-country offer limits | A move means a model change, so prompts, output schemas, thinking and sampling settings, tool calling and evaluation baselines are redone | Expensive: every quality claim must be re-earned |
| 3 | Managed agent capabilities: ADK sessions, Memory Bank, Agent Registry and Gemini Enterprise, A2A | Foundry conversations and state store (state store in preview); Foundry Memory (preview); publish to Microsoft 365 Copilot and Teams; Agent 365 registry (GA 1 May 2026); A2A v1.0 (GA), v0.3 (preview); MCP via toolboxes (GA) | Foundry state belongs to Foundry's own APIs, not ADK's `SessionService` and `MemoryService`. Memory needs Azure OpenAI chat and embedding deployments, has no VNet support, and sets quotas per scope. Incoming A2A is JSON-RPC only, text only, no streaming, Entra-authenticated, and serves v0.3 unless v1.0 is requested | No ADK backend targets Foundry state or memory; each would need a custom service or a database-backed one. Gemini Enterprise listing becomes a Microsoft 365 publish with tenant admin approval | Expensive: the managed agent layer does not transfer |
| 4 | Identity: service accounts, Workload Identity, end-user sign-in | Managed Identity; Entra Workload ID on AKS (OIDC federation); Entra Agent ID (GA); Container Apps and App Service built-in auth ("Easy Auth") | Azure RBAC role assignments on resource scopes replace IAM bindings; the Entra tenant is a separate directory. Hosted agents get a per-agent Entra identity automatically and support on-behalf-of flows from Microsoft 365. Easy Auth runs as a sidecar and injects identity headers | Every grant is re-derived. Users signing in with Google accounts need Entra federation or a Google provider. Agent ID licensing ties into Agent 365, which is not settled | Moderate: concepts match, the policy has to be rewritten |
| 5 | Secrets: Secret Manager | Key Vault (GA) | RBAC is the default data-plane model for new vaults from API version 2026-02-01. Soft delete keeps deleted secrets recoverable for 7 to 90 days, and purge protection blocks early deletion | Rotation hooks and naming change, and so do the reader roles (Key Vault Secrets User) | Straightforward |
| 6 | Databases: Cloud SQL or AlloyDB PostgreSQL, Firestore, BigQuery | Azure Database for PostgreSQL flexible server (GA); Cosmos DB for NoSQL (GA; vector search must be enabled per account and only on new containers); Fabric Data Warehouse or Synapse SQL | Flexible server runs community PostgreSQL, has stop/start and built-in PgBouncer. Cosmos DB bills request units, provisioned or serverless. Fabric bills capacity units on a capacity SKU; Synapse SQL is T-SQL with serverless and dedicated pools. BigQuery bills bytes scanned (on-demand) or slots (editions) | PostgreSQL moves by dump and restore (AlloyDB-only features do not). Firestore to Cosmos DB is a data-model redesign. BigQuery SQL (GoogleSQL) must be rewritten as T-SQL, and cost guards built on bytes scanned no longer apply | Straightforward (PostgreSQL); expensive (Firestore, BigQuery) |
| 7 | Object storage: Cloud Storage | Blob Storage (GA) | Signed URLs become SAS tokens or RBAC; lifecycle policies and cooler tiers exist on both | ADK ships `GcsArtifactService`; there is no Azure artifact service in ADK, so a custom `BaseArtifactService` over Blob is needed | Straightforward for the data, moderate for ADK artifacts |
| 8 | Retrieval: Vertex AI RAG Engine, Vertex AI Search, vector search | Azure AI Search (name unchanged; vector and hybrid search on all tiers at no extra charge); Foundry IQ knowledge bases on top of it (partly GA); Foundry file search; pgvector or Cosmos DB vectors | Foundry IQ's GA scope depends on the Search REST API version, and its portal experience is preview only. File search through a toolbox in a hosted agent has no user isolation: everyone in the project shares the vector stores | ADK's Vertex AI RAG and Search tools are lost. Corpora must be re-chunked, re-embedded with a new model, and retrieval quality re-evaluated | Expensive: re-indexing and re-evaluation |
| 9 | Async work: Cloud Tasks, Pub/Sub | Service Bus queues and topics (GA); Event Grid (GA); Storage queues (GA); Durable Functions (GA) | Service Bus is pull-based with long polling, with duplicate detection, sessions for FIFO, scheduled delivery, dead-lettering and transactions. Storage queues cap messages at 64 KB and can reorder. Durable Functions replays orchestrator code from an event-sourced history | Cloud Tasks' push to an HTTP target becomes a consumer or a Functions trigger. Idempotency and retry design carry over; delivery wiring does not | Moderate |
| 10 | Observability: Cloud Logging, Trace, Monitoring with OpenTelemetry | Azure Monitor and Application Insights through the Microsoft OpenTelemetry Distro (`microsoft-opentelemetry`); Foundry tracing (GA for prompt and hosted agents; workflow and external agents preview) | The distro exports to Azure Monitor, any OTLP endpoint or Agent 365. Foundry uses the OpenTelemetry GenAI conventions, which are themselves at Development status | ADK's spans travel, but dashboards, alerts, log queries and BigQuery Agent Analytics are rebuilt. Whether Foundry's trace views render ADK spans well is `unverified` | Moderate |
| 11 | Safety screening: Model Armor, Sensitive Data Protection | Azure AI Content Safety: Prompt Shields (GA), groundedness (preview), protected material, task adherence; Foundry guardrails; Azure Language PII (text PII GA in API 2026-05-01); Purview DSPM for AI | Content filters are on by default for serverless model deployments, but only through the Azure OpenAI SDK and v1 APIs; other client paths need explicit Content Safety calls. Purview enforcement needs user-context Entra tokens, and its coverage of Foundry agents conflicts between pages | Detector categories, thresholds and redaction templates do not map one to one; adversarial and PII suites must be re-run against the new detectors | Moderate |
| 12 | CI and registry | GitHub Actions or Azure DevOps, with Azure Container Registry (GA) | Hosted agents pull from ACR; Foundry projects created before 25 June 2026 need the registry's public endpoint | Deploy steps, registry paths and CI federation to Entra change; GitHub Actions to Entra federation was not read (`unverified`) | Straightforward |

**Conclusion.** The containers, PostgreSQL, secrets, object storage and CI move
cheaply. The expensive parts are those that make the design an ADK-on-GCP
design: Gemini itself (row 2), the managed session, memory and registry layer
(row 3), BigQuery and Firestore (row 6), and managed retrieval (row 8). Each of
these carries a re-evaluation cost as well as engineering, because model,
embeddings and retrieval all change together.

## Running ADK itself on Azure

The ADK docs say an agent can be deployed to "any environment that supports
container images", so Container Apps or AKS can host an unchanged ADK FastAPI
app. ADK's LiteLLM connector (`litellm>=1.84` required; the docs warn about
compromised LiteLLM releases 1.82.7 and 1.82.8) takes `provider/model`
strings. LiteLLM's Azure provider uses `azure/<deployment-name>` and accepts
Entra tokens through `azure_ad_token_provider` built from
`DefaultAzureCredential`, so keyless calls from a managed identity look
feasible. The ADK docs do not mention Azure OpenAI or Foundry, so this path
is `unverified` end to end in official ADK material. Tool calling, streaming
and structured output through this route need their own test.

What an ADK app on Azure loses or must replace:

- `VertexAiSessionService`, which needs Agent Runtime: replace with
  `DatabaseSessionService` on Azure PostgreSQL, which the ADK docs list as
  supported.
- `VertexAiMemoryBankService` and `VertexAiRagMemoryService`: no Azure
  backend. Memory Bank does not require hosting on Agent Runtime, so a
  cross-cloud call back to GCP is possible but brings back the GCP
  dependency, egress and federated identity.
- Vertex AI RAG Engine and Vertex AI Search tools: replace with function
  tools over Azure AI Search.
- `google_search` grounding, which ADK documents as compatible only with
  Gemini 2 models: replace with Foundry's Bing-based web search or another
  search API, each with its own usage terms.
- `GcsArtifactService`: replace with a custom Blob artifact service.

Packaging ADK as a Foundry hosted agent is plausible, since Microsoft calls
the protocol libraries framework-agnostic, but no ADK sample was found and
ADK's own HTTP surface is not the Responses protocol. Treat it as
`unverified` and adapter work.

## The Microsoft Agent Framework pull

Microsoft Agent Framework is described on Microsoft Learn as "the direct
successor" to Semantic Kernel and AutoGen, "created by the same teams"
(Python and .NET; Go in public preview; 1.0 announced on Microsoft's
devblog). On Azure it is the first-class path: Foundry samples, the
`FoundryToolbox` integration for hosted agents, Purview policy middleware and
tracing conventions all target it first, while other runtimes use generic MCP
clients. Hosting on Azure does not force the framework (hosted agents name
LangGraph, the OpenAI Agents SDK and custom code), but every managed feature
a team adopts there pulls it further towards Agent Framework, just as Agent
Runtime and Memory Bank pull towards ADK on GCP. A portability assessment
should treat "move the cloud" and "change the framework" as separate
decisions with separate costs. The framework comparison is covered elsewhere.

## What stays the same

- Agent logic, tool functions and ADK workflow structure, if ADK is kept.
- Container images and the FastAPI entry point.
- PostgreSQL schemas and SQL for operational data.
- OpenTelemetry instrumentation and span content rules.
- MCP servers and A2A as protocols. Foundry needs A2A v1.0 explicitly
  requested, and whether ADK's A2A version matches is `unverified`.
- Application-level guardrails: budgets, approval, idempotent tools,
  ownership checks and redaction seams in callbacks.
- Evaluation sets and their structure, though baselines must be re-run.

## Name and status changes noticed

- "Azure AI Foundry" is now **Microsoft Foundry**; the service is **Foundry
  Agent Service**, with prompt agents, voice-based prompt agents (preview) and
  hosted agents. Its runtime component is also called "Agent Runtime", the
  same name as Google's.
- Foundry RBAC roles were renamed: Azure AI User became **Foundry User**, and
  so on.
- Azure AI services are now branded **Foundry Tools**, for example "Azure
  Language in Foundry Tools". **Azure AI Search** keeps its name, with **Foundry
  IQ** built on it. **Azure AI Content Safety** keeps its name, and **Foundry
  guardrails** sit on top of it.
- **Entra Agent ID** is GA. The Entra Agent Registry is being folded into
  **Microsoft Agent 365**: the admin blades were due to retire on 1 May 2026,
  and the Graph registry APIs are being replaced.
- Microsoft's Python OpenTelemetry distro has a new name,
  `microsoft-opentelemetry`; existing Azure Monitor distro users need not
  change.

## Unverified

- That Gemini is unavailable on Azure. It is absent from the catalog pages
  read, but the live catalog was not browsed.
- ADK with LiteLLM against Azure OpenAI: tool calls, streaming, structured
  output and Entra token refresh.
- ADK packaged as a hosted agent, and Foundry trace views for ADK spans.
- A2A version compatibility between ADK and Foundry.
- Purview DSPM coverage of Foundry agents, where Microsoft pages conflict.
- Whether Azure Language's synthetic-replacement redaction is GA, where pages
  conflict.
- The exact date of Agent Framework 1.0, and Agent ID licensing outside Agent 365.
- Azure AI Search billing shape (provisioned tiers), which was not read.

## Sources (all read 2026-10-26)

- Hosted agents: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents
- Agent Service overview: https://learn.microsoft.com/en-us/azure/foundry/agents/overview
- Hosted agents GA (9 July): https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-july-august-2026/
- Memory (preview): https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory
- Incoming A2A: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/enable-agent-to-agent-endpoint
- Publish to Copilot and Teams: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot
- File search: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search
- Foundry tracing: https://learn.microsoft.com/en-us/azure/foundry/observability/concepts/trace-agent-concept
- Foundry Models overview: https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview
- Partner models: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-from-partners
- Foundry IQ: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq (search result)
- Azure AI Search vectors: https://learn.microsoft.com/en-us/azure/search/vector-search-overview
- Entra Agent ID what's new: https://learn.microsoft.com/en-us/entra/agent-id/whats-new-agent-id
- Agent 365 and registry convergence: https://learn.microsoft.com/en-us/microsoft-agent-365/overview and https://learn.microsoft.com/en-us/entra/agent-id/agent-registry-convergence (search results)
- AKS workload identity: https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview
- Container Apps: https://learn.microsoft.com/en-us/azure/container-apps/overview and https://learn.microsoft.com/en-us/azure/container-apps/authentication
- Key Vault RBAC and soft delete: https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide and https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview (search results)
- PostgreSQL flexible server: https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/overview
- Cosmos DB vectors and serverless: https://learn.microsoft.com/en-us/cosmos-db/index-vector-data and https://learn.microsoft.com/en-us/azure/cosmos-db/serverless (search results)
- Synapse: https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is
- Fabric warehouse billing: https://learn.microsoft.com/en-us/fabric/data-warehouse/usage-reporting (search result)
- Service Bus: https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview
- Storage queues compared: https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-azure-and-service-bus-queues-compared-contrasted (search result)
- Durable Functions: https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-orchestrations (search result)
- Azure Monitor OpenTelemetry: https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable
- Content Safety: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview
- Language PII: https://learn.microsoft.com/en-us/azure/ai-services/language-service/whats-new (search result)
- Purview and Foundry: https://learn.microsoft.com/en-us/purview/ai-azure-foundry and https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-onboarding (search results)
- Agent Framework: https://learn.microsoft.com/en-us/agent-framework/overview/ and https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/ (search result)
- ADK: https://adk.dev/deploy/, https://adk.dev/agents/models/, https://adk.dev/agents/models/litellm/, https://adk.dev/sessions/session/, https://adk.dev/sessions/memory/, https://adk.dev/artifacts/, https://adk.dev/integrations/google-search/ (google.github.io/adk-docs now redirects to adk.dev)
- LiteLLM Azure provider: https://docs.litellm.ai/docs/providers/azure/
- BigQuery pricing models: https://cloud.google.com/bigquery/pricing and https://cloud.google.com/bigquery/docs/editions-intro (search results)

"Search result" means the claim rests on a search summary of that page, not
on a full read.

## Limits of this note

Desk research only: nothing was deployed on Azure, and no ADK-on-Azure path
was run. Status labels change quickly in Foundry; several Learn pages were
updated in the past month and some contradict each other, and both are
flagged above. Regional availability was checked only for hosted agents and
Memory, which have different region lists; every other service needs a
per-region check against the client's residency needs. No prices, effort
estimates or parity claims are made. The ratings are relative judgements for
a stakeholder conversation, not estimates. The framework comparison (Agent
Framework against ADK) and the AWS mapping are out of scope.
