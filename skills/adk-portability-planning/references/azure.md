# Azure alternatives for a GCP and ADK design

<!-- verified: 2026-10-26; re-check every 90 days -->

Read when `targets` includes `azure`, to fill the Azure column of "Cloud
alternatives" and the Azure risks. Desk research only, from Microsoft Learn,
Azure and Foundry announcements and the ADK docs: nothing was deployed and no
ADK-on-Azure path was run. No prices are given; "pricing shape" means what is
metered. Foundry status labels change quickly and several Learn pages
contradict each other; both are flagged below. Regional availability was
checked only for hosted agents and Memory; check every other service against
the client's residency needs.

**Conclusion.** Containers, PostgreSQL, secrets, object storage and CI move
cheaply. The expensive parts are the ones that make the design an ADK-on-GCP
design: Gemini itself, the managed session, memory and registry layer,
BigQuery and Firestore, and managed retrieval. Each carries a re-evaluation
cost as well as engineering, because model, embeddings and retrieval change
together.

## Summary by GCP responsibility

Ratings: straightforward, moderate, expensive.

| GCP responsibility | Azure option | Status (2026-10-26) | Meaningful difference | Migration concern | Portability |
| --- | --- | --- | --- | --- | --- |
| Hosting: Cloud Run, GKE, Agent Runtime | Container Apps; AKS; App Service; Foundry Agent Service hosted agents | GA; hosted agents GA (announced 9 July 2026) | Container Apps: revisions, traffic splitting, KEDA, scale to zero (not when scaling on CPU or memory). Hosted agents: your container in a per-session VM-isolated sandbox behind a Responses, Invocations or A2A endpoint; one version serves all traffic, no splitting | Cloud Run and GKE images move as they are. Agent Runtime does not: hosted agents expect Microsoft's protocol libraries, and ADK is not a named framework | moderate (containers) / re-platform (managed runtime) |
| Model: Gemini on Agent Platform | Foundry Models: Azure OpenAI and other models sold by Azure; partner models (Anthropic, Mistral, Meta, Cohere) via Marketplace | GA; no Gemini in the catalogue pages read (`unverified` against the live catalogue) | Deployment types (Global, Data Zone, Regional; Standard or Provisioned) set where prompts are processed; partner models carry the provider's terms and per-country limits | A model change: prompts, output schemas, thinking and sampling, tool calling and evaluation baselines redone | expensive |
| Sessions, Memory Bank, Agent Registry, Gemini Enterprise, A2A | Foundry conversations and state store (state store preview); Foundry Memory (preview); publish to Microsoft 365 Copilot and Teams; Agent 365 registry (GA 1 May 2026); A2A v1.0 (GA), v0.3 (preview); MCP via toolboxes (GA) | Mixed | Foundry state belongs to Foundry's APIs, not ADK's services. Memory needs Azure OpenAI chat and embedding deployments, has no VNet support, sets quotas per scope. Incoming A2A: JSON-RPC, text only, no streaming, Entra-authenticated, v0.3 unless v1.0 requested | No ADK backend targets Foundry state or memory: custom or database-backed services. Gemini Enterprise listing becomes a Microsoft 365 publish with tenant admin approval | expensive |
| Identity: service accounts, Workload Identity, end-user sign-in | Managed Identity; Entra Workload ID on AKS; Entra Agent ID (GA); Container Apps and App Service built-in auth | GA | Azure RBAC on resource scopes replaces IAM bindings; the Entra tenant is a separate directory; hosted agents get a per-agent Entra identity and on-behalf-of flows from Microsoft 365 | Every grant re-derived; Google-account users need Entra federation or a Google provider; Agent ID licensing ties into Agent 365, not settled | moderate |
| Secrets: Secret Manager | Key Vault | GA | RBAC is the default data-plane model for new vaults from API version 2026-02-01; soft delete and purge protection | Rotation hooks, naming and reader roles (Key Vault Secrets User) change | straightforward |
| Databases: Cloud SQL or AlloyDB, Firestore, BigQuery | Azure Database for PostgreSQL flexible server; Cosmos DB for NoSQL; Fabric Data Warehouse or Synapse SQL | GA | Flexible server is community PostgreSQL with built-in PgBouncer. Cosmos DB bills request units; vector search enabled per account, new containers only. Fabric bills capacity units; Synapse SQL is T-SQL. BigQuery bills bytes scanned or slots | Postgres: dump and restore (AlloyDB-only features do not carry). Firestore to Cosmos DB is a data-model redesign. GoogleSQL rewritten as T-SQL; bytes-scanned cost guards no longer apply | straightforward (Postgres) / expensive (Firestore, BigQuery) |
| Object storage: Cloud Storage | Blob Storage | GA | Signed URLs become SAS tokens or RBAC | ADK ships `GcsArtifactService`; no Azure artifact service, so a custom `BaseArtifactService` over Blob | straightforward (data) / moderate (ADK artifacts) |
| Retrieval: RAG Engine, Agent Search, vector search | Azure AI Search; Foundry IQ knowledge bases on top (partly GA); Foundry file search; pgvector or Cosmos DB vectors | Mixed | Foundry IQ's GA scope depends on the Search REST API version; portal preview only. File search through a toolbox in a hosted agent has no user isolation: the project shares the vector stores | ADK's Vertex AI RAG and Search tools are lost; re-chunk, re-embed with a new model, re-evaluate retrieval | expensive |
| Async work: Cloud Tasks, Pub/Sub | Service Bus queues and topics; Event Grid; Storage queues; Durable Functions | GA | Service Bus is pull with long polling, duplicate detection, sessions for FIFO, dead-lettering; Storage queues cap messages at 64 KB and can reorder; Durable Functions replays orchestrators from history | Push to an HTTP target becomes a consumer or Functions trigger; idempotency design carries, delivery wiring does not | moderate |
| Observability: Cloud Logging, Trace, Monitoring with OTel | Azure Monitor and Application Insights via the Microsoft OpenTelemetry Distro (`microsoft-opentelemetry`); Foundry tracing | Azure Monitor GA; Foundry tracing for prompt and hosted agents reported GA on one page and preview in a Microsoft post (`unverified`); workflow and external agents preview | Exports to Azure Monitor, any OTLP endpoint or Agent 365; Foundry uses the OTel GenAI conventions, themselves at Development status | ADK spans travel; dashboards, alerts, log queries and BigQuery Agent Analytics rebuilt; Foundry views of ADK spans `unverified` | moderate |
| Safety: Model Armor, Sensitive Data Protection | Azure AI Content Safety (Prompt Shields GA, groundedness preview); Foundry guardrails; Azure Language PII; Purview DSPM for AI | Mixed | Content filters default-on for serverless deployments only through the Azure OpenAI SDK and v1 APIs; other paths need explicit Content Safety calls; Purview needs user-context Entra tokens | Detectors, thresholds and redaction templates do not map one to one; re-run adversarial and PII suites | moderate |
| CI and registry | GitHub Actions or Azure DevOps; Azure Container Registry | GA | Hosted agents pull from ACR; Foundry projects created before 25 June 2026 need the registry's public endpoint | Deploy steps, registry paths and CI federation to Entra (not read, `unverified`) | straightforward |

## Running ADK itself on Azure

ADK says an agent can be deployed to "any environment that supports
container images", so Container Apps or AKS can host an unchanged ADK
FastAPI app. ADK's LiteLLM connector takes
`provider/model` strings. LiteLLM's Azure provider uses
`azure/<deployment-name>` and accepts Entra tokens through
`azure_ad_token_provider` from `DefaultAzureCredential`, so keyless calls from
a managed identity look feasible. ADK's docs do not mention Azure OpenAI or
Foundry, so this path is `unverified` end to end; tool calling, streaming and
structured output need their own test. ADK 2.13.0 pins
`litellm>=1.84,<1.106.3` ("1.107.0 was a compromised release; raise only
after checking the new release is clean"), and the ADK docs also warn about
the compromised releases 1.82.7 and 1.82.8: keep the cap. ADK 2.13.0 also ships
`AzureOpenAIResponsesLlm` in `google.adk.integrations.openai` (see
[agent frameworks](agent-frameworks.md#model-portability-within-adk)).

What an ADK app on Azure loses or must replace:

- `VertexAiSessionService` → `DatabaseSessionService` on Azure PostgreSQL,
  which ADK supports.
- `VertexAiMemoryBankService` and `VertexAiRagMemoryService`: no Azure
  backend. Memory Bank does not require Agent Runtime hosting, so a
  cross-cloud call back to GCP is possible, bringing back the GCP dependency,
  egress and federated identity.
- Vertex AI RAG Engine and Agent Search tools → function tools over Azure AI
  Search.
- `google_search` grounding (Gemini 2 only) → Foundry's Bing-based web search
  or another search API, each with its own usage terms.
- `GcsArtifactService` → a custom Blob artifact service.

Packaging ADK as a Foundry hosted agent is plausible, since Microsoft calls
the protocol libraries framework-agnostic, but no ADK sample was found and
ADK's HTTP surface is not the Responses protocol: `unverified`, and adapter
work.

## The Microsoft Agent Framework pull

Microsoft Agent Framework is, on Microsoft Learn, "the direct successor" to
Semantic Kernel and AutoGen. On Azure it is the first-class path: Foundry
samples, the `FoundryToolbox` integration, Purview policy middleware and
tracing conventions target it first. Hosting on Azure does not force it
(hosted agents name LangGraph, the OpenAI Agents SDK and custom code), but
each managed feature a team adopts there pulls further towards it, as Agent
Runtime and Memory Bank pull towards ADK on GCP. Treat "move the cloud" and
"change the framework" as separate decisions with separate costs.

## What stays the same

- Agent logic, tool functions and ADK workflow structure, if ADK is kept.
- Container images and the FastAPI entry point.
- PostgreSQL schemas and operational SQL.
- OpenTelemetry instrumentation and span content rules.
- MCP servers and A2A as protocols (Foundry needs v1.0 requested; whether
  ADK's A2A version matches is `unverified`).
- Application guardrails: budgets, approval, idempotent tools, ownership
  checks and redaction seams in callbacks.
- Evaluation sets and their structure; baselines are re-run.

## Status and name notes (2026-10-26)

- "Azure AI Foundry" is now **Microsoft Foundry**; the service is **Foundry
  Agent Service** (prompt agents, voice prompt agents in preview, hosted
  agents). Its runtime is also called "Agent Runtime", like Google's.
- Foundry RBAC roles renamed: Azure AI User became **Foundry User**.
- Azure AI services are branded **Foundry Tools**; **Azure AI Search** and
  **Azure AI Content Safety** keep their names, with **Foundry IQ** and
  **Foundry guardrails** on top.
- **Entra Agent ID** is GA; the Entra Agent Registry is being folded into
  **Microsoft Agent 365**.
- The Python OpenTelemetry distro is now `microsoft-opentelemetry`.
- Hosted agents' old backend was supported only until 2026-08-20 (search
  summary).

## Unverified

- That Gemini is unavailable on Azure (absent from the catalogue pages read;
  live catalogue not browsed).
- ADK with LiteLLM against Azure OpenAI: tool calls, streaming, structured
  output and Entra token refresh.
- ADK packaged as a hosted agent; Foundry trace views for ADK spans.
- A2A version compatibility between ADK and Foundry.
- Purview DSPM coverage of Foundry agents (pages conflict).
- Whether Azure Language's synthetic-replacement redaction is GA (pages
  conflict).
- Foundry tracing status for hosted agents (GA or preview; sources conflict).
- Agent ID licensing outside Agent 365.
- Azure AI Search billing shape (provisioned tiers), not read.

## Sources

All read 2026-10-26. "(search summary)" means the claim rests on a search
summary, not a full read.

| Topic | URL |
| --- | --- |
| Hosted agents | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents |
| Agent Service overview | https://learn.microsoft.com/en-us/azure/foundry/agents/overview |
| Hosted agents GA, 9 July | https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-july-august-2026/ |
| Foundry Memory (preview) | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory |
| Incoming A2A | https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/enable-agent-to-agent-endpoint |
| Publish to Copilot and Teams | https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot |
| File search | https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search |
| Foundry tracing | https://learn.microsoft.com/en-us/azure/foundry/observability/concepts/trace-agent-concept |
| Foundry Models; partner models | https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview ; https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-from-partners |
| Foundry IQ (search summary) | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq |
| Azure AI Search vectors | https://learn.microsoft.com/en-us/azure/search/vector-search-overview |
| Entra Agent ID | https://learn.microsoft.com/en-us/entra/agent-id/whats-new-agent-id |
| Agent 365 and registry convergence (search summary) | https://learn.microsoft.com/en-us/microsoft-agent-365/overview ; https://learn.microsoft.com/en-us/entra/agent-id/agent-registry-convergence |
| AKS workload identity | https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview |
| Container Apps; authentication | https://learn.microsoft.com/en-us/azure/container-apps/overview ; https://learn.microsoft.com/en-us/azure/container-apps/authentication |
| Key Vault RBAC and soft delete (search summary) | https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide ; https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview |
| PostgreSQL flexible server | https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/overview |
| Cosmos DB vectors and serverless (search summary) | https://learn.microsoft.com/en-us/cosmos-db/index-vector-data ; https://learn.microsoft.com/en-us/azure/cosmos-db/serverless |
| Synapse; Fabric warehouse billing (search summary) | https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is ; https://learn.microsoft.com/en-us/fabric/data-warehouse/usage-reporting |
| Service Bus; Storage queues compared (search summary) | https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview ; https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-azure-and-service-bus-queues-compared-contrasted |
| Durable Functions (search summary) | https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-orchestrations |
| Azure Monitor OpenTelemetry | https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable |
| Content Safety; Language PII (search summary) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview ; https://learn.microsoft.com/en-us/azure/ai-services/language-service/whats-new |
| Purview and Foundry (search summary) | https://learn.microsoft.com/en-us/purview/ai-azure-foundry ; https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-onboarding |
| Agent Framework overview; 1.0 GA (devblog 2026-04-03; PyPI `agent-framework-core` 1.0.0 uploaded 2026-04-02) | https://learn.microsoft.com/en-us/agent-framework/overview/ ; https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/ ; https://pypi.org/pypi/agent-framework-core/1.0.0/json |
| ADK deploy, models, LiteLLM, sessions, memory, artifacts, Google Search | https://adk.dev/deploy/ ; https://adk.dev/agents/models/ ; https://adk.dev/agents/models/litellm/ ; https://adk.dev/sessions/session/ ; https://adk.dev/sessions/memory/ ; https://adk.dev/artifacts/ ; https://adk.dev/integrations/google-search/ |
| LiteLLM Azure provider | https://docs.litellm.ai/docs/providers/azure/ |
| ADK 2.13.0 LiteLLM pin and comment | https://raw.githubusercontent.com/google/adk-python/v2.13.0/pyproject.toml |
| BigQuery pricing models (search summary) | https://cloud.google.com/bigquery/pricing ; https://cloud.google.com/bigquery/docs/editions-intro |
