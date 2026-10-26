---
topic: claims-triage
design: docs/architecture/claims-triage.md
plan: docs/plans/claims-triage.md
goal: G05
primary_build: GCP + Google ADK (unchanged)
concern: The insurer's CTO fears group IT will standardise on Azure and the assistant would have to be rebuilt; the board also asked about AWS
targets: [aws, azure]
frameworks: [langgraph, microsoft-agent-framework, pydantic-ai]
sources_checked: 2026-10-26
status: draft
---

# Portability assessment: claims triage assistant

## Summary for the reader

- **Recommendation:** keep the GCP and ADK build as designed and hold an exit plan. Nothing in the concern needs a second provider now: the CTO asked what a later move would cost, not for the assistant to run on two clouds.
- **Google-specific on purpose:** Gemini with `output_schema` (D2), RAG Engine retrieval (D4), IAP with Workspace sign-in (D7), Model Armor (D9) and Cloud Trace dashboards (D8). Each was chosen for its value, and none is wrapped in a home-made interface.
- **Boundaries kept:** the ones ADK and the design already have: `DatabaseSessionService` on standard PostgreSQL (D3), the claims client passed into the write tool (D5), and OpenTelemetry instrumentation (D8). One cheap improvement is proposed below, pending a designer checkpoint.
- **What a move would involve:** a model change with a full re-baseline of the evaluation set (M1), because Gemini is not offered on Bedrock and was not found in the Foundry catalogue; re-chunking and re-embedding the policy corpus with retrieval re-evaluated; re-mapping identity and access; and rebuilding dashboards and safety screening. The containers, Postgres data and tool code move with little change. A move is not cheap, and the assessment does not claim the assistant is fully portable.

## Concern and scope

- **Question asked:** "If group IT standardises on Azure, do we have to rebuild this? And what would AWS involve?" (design scope gate, source: CTO, 2026-10-20).
- **Move later or run on several now:** move later at a known cost. No date or trigger for a move exists, so multicloud now is out of scope.
- **Targets:** AWS and Azure, both named by the ticket's scope-gate answer; LangGraph, Microsoft Agent Framework and Pydantic AI as framework alternatives from the reference set, because Azure pulls towards Agent Framework.
- **In and out of scope:** cloud, framework, model, service and deployment are assessed below. Data residency and legal transfer questions belong to the governance screen and are not decided here.

## Baseline architecture

Design-only facts unless marked; the repository holds G01 to G03 code, and its imports were inspected for the components marked "inspected".

- ADK 2.x `SequentialAgent` of classify, retrieve and draft steps behind FastAPI on Cloud Run (D1; inspected).
- Pinned Gemini Flash model on Agent Platform with `output_schema` TriageResult (D2, C4; inspected).
- Sessions in `DatabaseSessionService` on Cloud SQL for PostgreSQL with IAM database authentication (D3; inspected).
- Policy corpus in RAG Engine with Gemini embeddings via `VertexAiRagRetrieval` (D4, C1; inspected).
- Claims platform write through one confirmed `FunctionTool`, client passed in (D5, C2; inspected).
- Attachments in Cloud Storage via `GcsArtifactService` (D6; design-only).
- IAP with Workspace accounts, service account identity, Secret Manager (D7, C3; design-only).
- OpenTelemetry to Cloud Trace and Cloud Logging; `adk eval` with a Gemini judge (D8).
- Model Armor screening of claim free text (D9; design-only).

## Component classification

| Component | Design IDs | Class | Why | Exit path |
| --- | --- | --- | --- | --- |
| Triage rules, TriageResult schema, prompts as text | C4, D1 | shared logic | Plain Python and Pydantic with no provider imports in the inspected modules | None beyond re-running tests; prompt text is re-evaluated with any model change |
| Claims platform client and write tool | D5, C2 | shared logic | The insurer's own REST API; the client is passed into the tool body | Unchanged on any cloud; network path and secret source change |
| ADK workflow and confirmation | D1, C2 | provider-specific by choice | ADK is the chosen framework; the workflow is small | Kept on any cloud; a framework switch rewrites orchestration, confirmation and the eval harness |
| Sessions | D3 | replaceable adapter | `DatabaseSessionService` on standard PostgreSQL; ADK's `BaseSessionService` is the port | Dump and restore to RDS, Aurora or Azure PostgreSQL; contract test the session service on the target |
| Gemini model and output schema | D2, C4 | expensive dependency | Cheap seam, expensive switch: ADK has connectors, but a move off Gemini changes behaviour and needs the evaluation set re-baselined | Candidate model through ADK's native or LiteLLM connector; re-run the frozen eval set (M1) and schema-repair tests |
| Policy corpus retrieval | D4, C1 | expensive dependency | Index and embeddings are Gemini- and RAG Engine-specific | Keep source documents; re-chunk and re-embed into Bedrock Knowledge Bases or Azure AI Search; re-run retrieval evaluation |
| Attachments | D6 | replaceable adapter | Objects move by bulk copy; ADK's `BaseArtifactService` is the port | S3 or Blob Storage; a custom artifact service over Blob on Azure |
| Identity and access | D7, C3 | provider-specific by choice | IAP and service accounts are not wrapped | Re-map to ALB OIDC or Entra built-in auth and managed identities; rewrite token verification; repeat the security review |
| Hosting | D1 | provider-specific by choice | A Cloud Run container | Rehost on ECS on Fargate or Azure Container Apps; ARM64 build only for AgentCore |
| Telemetry and evaluation judge | D8 | replaceable adapter | OTel spans with an exporter set by configuration; the Gemini judge is a dependency of its own | Change the exporter; rebuild dashboards and alerts; re-baseline the judge |
| Safety screening | D9 | provider-specific by choice | Model Armor templates are not portable | Bedrock Guardrails or Azure AI Content Safety; re-run the adversarial suite |

## Dimensions

| Dimension | Assessment |
| --- | --- |
| Cloud | Assessed for AWS and Azure below; containers, Postgres and objects move, model and retrieval are the cost. |
| Agent framework | Assessed: keep ADK on any cloud; Azure pulls towards Agent Framework, which is a separate decision. |
| Model | Assessed: a model swap within ADK is a model change, not a system move, and it is the largest single driver. |
| Service | Assessed: the managed services the design relies on are RAG Engine (D4), Model Armor (D9) and IAP (D7). |
| Deployment | Not a concern: one Cloud Run container with no Agent Runtime features, so the deployment rehosts as a container. |

## Cloud alternatives

| Responsibility | GCP (design ID) | AWS | Azure | Difference | Portability |
| --- | --- | --- | --- | --- | --- |
| Hosting | Cloud Run (D1) | ECS on Fargate; AgentCore Runtime documents ADK | Container Apps; Foundry hosted agents do not name ADK | AgentCore needs ARM64 and its own entrypoint; Container Apps runs the image as is | moderate |
| Model | Gemini on Agent Platform (D2) | Bedrock models via LiteLLM (Gemini not offered); or call Gemini cross-cloud | Foundry Models (Gemini not found in the catalogue, unverified) | A model change, or cross-cloud identity, egress and residency | expensive |
| Sessions | Cloud SQL PostgreSQL (D3) | RDS or Aurora PostgreSQL | Azure Database for PostgreSQL flexible server | Same engine; check extensions | straightforward |
| Retrieval | RAG Engine (D4) | Bedrock Knowledge Bases or AgentCore Managed Knowledge Base | Azure AI Search or Foundry IQ | Re-embed with a new model; ADK retrieval tools become custom tools | expensive |
| Attachments | Cloud Storage (D6) | S3 | Blob Storage | No ADK artifact service for Blob | straightforward on AWS, moderate on Azure |
| Identity | IAP, service accounts (D7) | ALB OIDC auth, IAM task roles | Entra built-in auth, managed identity | Signed-header formats and grants differ | moderate |
| Safety | Model Armor (D9) | Bedrock Guardrails | Azure AI Content Safety, Prompt Shields | Detectors and thresholds do not map one to one | moderate |
| Observability | Cloud Trace, Cloud Logging (D8) | CloudWatch, ADOT | Azure Monitor via the OpenTelemetry distro | Spans travel; dashboards rebuilt | moderate |

## Agent framework alternatives

| Concern | ADK (baseline) | LangGraph | Microsoft Agent Framework | Pydantic AI |
| --- | --- | --- | --- | --- |
| Ordered steps (D1) | `SequentialAgent` | Graph edges | Sequential orchestration | Plain code or `pydantic-graph` |
| Approval before write (C2) | `require_confirmation` | Interrupt; the node re-runs on resume, so the write must stay idempotent | `approval_mode="always_require"` | Deferred tools |
| Sessions (D3) | Event log with state deltas | Checkpointers on Postgres | History providers; session store experimental | None built in |
| Gemini (D2) | Native | Native packages | Gemini connector still beta | Native on Vertex |
| Evaluation (D8) | `adk eval` | LangSmith or `openevals` | Local checks plus Foundry evaluation | Pydantic Evals |
| Azure hosting | Custom container on hosted agents | Named by hosted agents | First-class, hosting package beta | Custom container |

A framework switch would rewrite orchestration, the confirmation flow, the session store and the evaluation harness; tool bodies, the TriageResult schema, prompt text and the claims client survive. Pydantic AI's own ADK comparison is vendor-authored and was not used for ADK facts.

## Boundaries worth having

| Boundary | What it isolates | Reason (a, b, c or d) | Cost now | Existing ADK seam |
| --- | --- | --- | --- | --- |
| Session service | Session store (D3) | c: the framework already has the seam | None; already in place | `BaseSessionService` |
| Claims client passed into the tool | Claims platform API (D5) | a: the CI fake already exercises it | None; already in place | `FunctionTool` |
| Model behind the agent | Gemini (D2) | c: ADK's model connectors | None; no wrapper is added | ADK model registry and connectors |
| Telemetry exporter by configuration | Cloud Trace (D8) | c: OTLP is the standard seam | Small; see the optional recommendation | OpenTelemetry exporter |

No new interface is proposed over RAG Engine, Model Armor or IAP: each would force a lowest common denominator over a managed feature the design relies on.

## Feature differences and migration risks

- Model change (D2): Gemini is not on Bedrock and was not found in Foundry's catalogue, so either the model changes and the evaluation set (M1) is re-baselined, or Gemini is called across clouds, which brings identity, egress and residency questions. High switching cost, likelihood unknown.
- Structured output (C4): Bedrock structured outputs cover only some model families and a subset of JSON Schema; the TriageResult repair loop needs retesting on any target model.
- Retrieval (D4, C1): re-embedding changes which clauses are retrieved, so C1 must be proved again on the target.
- Approval semantics (C2): on a framework switch to LangGraph, the interrupted node re-runs on resume; the write key from D5 keeps the write idempotent, but the test must be repeated.
- Identity (D7, C3): the ownership check reads IAP headers today; ALB and Entra pass identity differently, so C3 is re-proved.
- Safety (D9): Model Armor templates do not copy; the adversarial suite is re-run against the target's detectors.
- Evaluation judge (D8): the Gemini judge is itself a dependency; changing it changes the scores even with the same cases.

## Recommended strategy

Keep the current build and record this exit plan; revisit it when group IT sets a date or names a target. The trade-off is accepted dependency on Gemini and RAG Engine, the two expensive items, in exchange for a simpler build now. A model swap within ADK on GCP is the cheapest first step if the concern turns out to be model lock-in rather than the cloud. Running on two clouds now would double evaluation, operations and identity work for a move that has no date.

## Phased outline

1. **Prepare on GCP:** keep evaluation cases as framework-neutral data and the exporter in configuration (optional recommendations).
2. **Model candidate:** run the frozen evaluation set on a candidate model available on the target through ADK's connectors, per category, before any infrastructure work.
3. **Rehost:** run the unchanged container on the target behind its identity front end; contract-test the session service on the target PostgreSQL.
4. **Data:** backfill sessions and attachments with change capture and checksums; rebuild the corpus index from source documents and re-run retrieval evaluation.
5. **Parallel run:** shadow a sample of claims offline through the evaluation harness; shadow traffic never calls the write tool.
6. **Cutover and rollback:** pause writes, finish the sync, switch, and keep the GCP environment ready as the fallback until the owner removes it as a deliberate final step.

## Relative effort

| Item | Relative effort (small / medium / large / very large / unknown) | Drivers | Assumptions |
| --- | --- | --- | --- |
| Model change and re-baseline | large | Behaviour re-evaluation of every eval category; output-schema retesting | Candidate model chosen by the client; M1 is the baseline to match |
| Policy corpus rebuild | medium | Re-embedding and retrieval re-evaluation | Source documents are complete; G02 code took 14 hands-on hours (M2), which bounds only the code part |
| Rehost container and sessions | small | One adapter contract test; dump and restore | Pilot volume stays small (assumption) |
| Identity and access | medium | Re-mapping principals; rewriting token verification; security review | Staff accounts federate into the target directory |
| Safety screening | medium | Re-running the adversarial suite against new detectors | Same adversarial cases are reused |
| Framework switch | unknown; needs a spike | Orchestration, confirmation and eval harness rewrite | Only if group IT mandates Agent Framework |

Schedule risks outside the team's control: the insurer's security review and any client re-approval of the model provider.

## Optional recommendations for the current build

None of these is a ticket until a designer checkpoint approves it.

### Keep evaluation cases as framework-neutral data

- **What:** store the labelled triage cases behind M1 as plain JSON beside the ADK eval set.
- **Rationale:** the cases are the asset that survives any model or framework change; the scores do not.
- **Acceptance criteria:** the eval set is generated from the plain cases, and a test fails when they diverge.
- **Specialist:** `adk-agent-evaluation`
- **Status:** proposed; needs a designer checkpoint

### Set the telemetry exporter by configuration

- **What:** select the OTLP exporter and endpoint from environment configuration rather than code.
- **Rationale:** a target's exporter then changes without a code change (D8).
- **Acceptance criteria:** a local run exports spans to a test OTLP collector with no code edit.
- **Specialist:** `adk-agent-observability`
- **Status:** proposed; needs a designer checkpoint

## Open questions

- Does group IT have a date or trigger for an Azure standard? (CTO; it decides whether this plan stays insurance.)
- Would the insurer accept calling Gemini from another cloud, or must the model move with the hosting? (CTO and security; it decides the largest effort item.)
- Which candidate models would procurement approve on each target? (Procurement; it scopes the model spike.)

## Sources

| Claim or topic | URL | Read on |
| --- | --- | --- |
| Gemini not offered on Bedrock (Gemma only) | https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html | 2026-10-26 |
| AgentCore Runtime runs ADK; ARM64 contract | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-any-agent-framework.html | 2026-10-26 |
| Bedrock Knowledge Bases vector stores | https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html | 2026-10-26 |
| Foundry Models catalogue | https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview | 2026-10-26 |
| Foundry hosted agents | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents | 2026-10-26 |
| Azure AI Search vectors | https://learn.microsoft.com/en-us/azure/search/vector-search-overview | 2026-10-26 |
| ADK sessions and database service | https://adk.dev/sessions/session/ | 2026-10-26 |
| ADK model connectors and LiteLLM advisory | https://adk.dev/agents/models/litellm/ | 2026-10-26 |
| LangGraph interrupts and checkpointers | https://github.com/langchain-ai/docs | 2026-10-26 |
| Microsoft Agent Framework package status | https://github.com/microsoft/agent-framework | 2026-10-26 |
| Pydantic AI ADK comparison (vendor-authored) | https://github.com/pydantic/pydantic-ai | 2026-10-26 |
| Cost of avoiding lock-in | https://martinfowler.com/articles/oss-lockin.html | 2026-10-26 |
