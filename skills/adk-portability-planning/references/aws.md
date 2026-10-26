# AWS alternatives for a GCP and ADK design

<!-- verified: 2026-10-26; re-check every 90 days -->

Read when `targets` includes `aws`, to fill the AWS column of "Cloud
alternatives" and the AWS risks. Desk research only: nothing was deployed or
run, no prices are given, and the ratings are qualitative judgements for a
stakeholder conversation, not estimates. AgentCore shipped monthly through
2026, so re-check its release notes before quoting a status.

**Conclusion.** An ADK application can run on AWS: AWS documents ADK on
AgentCore Runtime, and containers, tool functions, Postgres and OTel move
with little change. The expensive parts are the ones Google manages for ADK:
Gemini itself (not offered on Bedrock), Memory Bank, RAG and Agent Search
retrieval, Google Search grounding, Firestore and BigQuery. Each needs a
rewrite or a data rebuild, then re-evaluation. A middle path hosts on AWS and
keeps calling Gemini across clouds: it defers the model cost but brings
cross-cloud identity, egress and residency into scope.

## Summary by GCP responsibility

Ratings: straightforward, moderate, expensive.

| GCP responsibility | AWS option | Status (2026-10-26) | Meaningful difference | Migration concern | Portability |
| --- | --- | --- | --- | --- | --- |
| Hosting: Cloud Run, GKE, Agent Runtime | ECS on Fargate, EKS, AgentCore Runtime; Lambda for short turns only | GA (AgentCore core GA Oct 2025) | AgentCore runs each session in its own microVM, wiped at session end; ARM64 containers serving `/invocations` and `/ping` on port 8080; Lambda's 900-second limit | Entrypoint adapter, ARM64 build, retest streaming, cold start and concurrency; map ingress and IAP to ALB and security groups | moderate |
| Model: Gemini on Agent Platform or Gemini API | Bedrock models (Claude, Nova, Gemma, others) through `LiteLlm`; or keep calling Gemini cross-cloud | GA; Gemini is not on Bedrock (Gemma only) | A model change, or a cross-cloud call | Model change: new prompts, settings, output-schema checks and a full evaluation re-baseline. Keep Gemini: record a residency and a credential decision | expensive (switch) / moderate (keep Gemini) |
| Sessions, Memory Bank, Agent Registry, Gemini Enterprise, A2A hosting | `DatabaseSessionService` on Aurora or RDS PostgreSQL; AgentCore Memory; AWS Agent Registry; A2A on AgentCore Runtime | GA; Agent Registry GA Aug 2026 in five regions | AgentCore Memory extracts long-term records by strategy (semantic, summary, preference, episodic, custom); no ADK memory service targets it | Custom `BaseMemoryService`; re-extract memories, retest recall, scoping and erasure; `VertexAiSessionService` history needs an export nobody has written | expensive |
| Identity: service accounts, Identity Platform, IAP | IAM roles (ECS task role, EKS Pod Identity, AgentCore execution role); Cognito; ALB `authenticate-oidc` or `authenticate-cognito`; AgentCore Identity; Verified Permissions | GA | ALB passes claims in a signed `x-amzn-oidc-data` JWT (ES256) the app must verify; Pod Identity not on Fargate pods | Rewrite token verification and ownership checks; moving users between identity providers is its own project (not researched) | moderate |
| Secrets: Secret Manager | AWS Secrets Manager | GA | Managed or Lambda rotation; AgentCore Identity can reference secrets | Copy values, change client calls, re-grant by role; retest version pins | straightforward |
| Databases: Cloud SQL or AlloyDB, Firestore, BigQuery | RDS or Aurora PostgreSQL; DynamoDB; Redshift or Athena | GA | Firestore to DynamoDB changes data model, queries, transactions and rules; Athena bills per query over S3 | Postgres: dump and restore, check extensions incl. pgvector; AlloyDB-only features do not carry. BigQuery: dialect, partitioning, SQL templates and bytes-billed cost guards reworked and re-evaluated | straightforward (Postgres) / expensive (Firestore, BigQuery) |
| Object storage: Cloud Storage | S3 | GA | Presigned URLs, lifecycle, encryption all exist | Bulk copy with egress; rewrite signed-URL and retention settings; re-grant | straightforward |
| Retrieval: RAG Engine, Agent Search, vector search | Bedrock Knowledge Bases; AgentCore Managed Knowledge Base (via Gateway); OpenSearch; S3 Vectors; Aurora pgvector | GA (S3 Vectors Dec 2025; Managed KB Jul 2026) | Knowledge Bases on OpenSearch Managed supports public-access domains only; S3 Vectors stores float embeddings, 1 KB metadata and 35 keys per vector under a KB; no Agent Search equivalent identified | Gemini embeddings are not on Bedrock: re-chunk, re-embed, re-evaluate retrieval; ADK retrieval tools become custom tools | expensive |
| Async work: Cloud Tasks, Pub/Sub | SQS, SNS, EventBridge (+ Scheduler), Step Functions | GA | SQS is pull; standard queues at-least-once, FIFO exactly-once per group; Step Functions Standard exactly-once, Express at-least-once when async | Push to pull or event-source mapping; re-derive idempotency keys; IAM replaces OIDC push auth; retest retries | moderate |
| Observability: Cloud Logging, Trace, Monitoring with OTel | CloudWatch, X-Ray, ADOT, AgentCore Observability | GA | Auto-instrumentation named only for Strands, LangChain, CrewAI; `AWS_GENAI_CONTENT_EXTRACTION_OPT_OUT=true` *keeps* payloads on spans | Exporters change; rebuild alarms and dashboards; BigQuery Agent Analytics has no counterpart; review redaction policy | moderate |
| Safety: Model Armor, Sensitive Data Protection | Bedrock Guardrails (`ApplyGuardrail`), AgentCore Policy, Comprehend PII, Macie | GA | Comprehend PII: English and Spanish only, 100 KB real-time, redaction as async batch; Macie discovers in S3 only | Templates and info types do not copy; re-run PII and adversarial suites | moderate |
| CI and registry: Cloud Build, Artifact Registry | CodeBuild or existing CI; ECR | GA | ARM64 builds for AgentCore | Deploy steps and registry paths | straightforward |

## Can ADK itself run on AWS?

Yes: as an ordinary container on ECS on Fargate or EKS, and on AgentCore
Runtime, whose "use any agent framework" page includes a Google ADK example.
That example uses a Gemini API key, `InMemorySessionService` and
`google_search`, so it keeps Gemini and loses sessions when the microVM ends.
ADK's model docs list a `LiteLlm` connector but no ADK page mentions
Bedrock. LiteLLM's docs cover `bedrock/` and `bedrock/converse/` routes, tool
calling and `response_format` (emulated for some models with a forced tool
call). **ADK on Bedrock through `LiteLlm` is plausible but not documented by
ADK and not tested (`unverified`).** Known `LiteLlm` issues: reasoning tokens
counted twice and a changed `num_retries` meaning.

What ADK loses or must replace on AWS:

- `VertexAiSessionService` → `DatabaseSessionService` on Aurora or RDS
  PostgreSQL (supported by ADK).
- Memory Bank (`VertexAiMemoryBankService`) → a custom `BaseMemoryService`
  over AgentCore Memory or Postgres. AWS's memory examples cover LangChain,
  LangGraph, Strands and AWS SDKs, not ADK.
- RAG (`VertexAiRagRetrieval`) and the Agent Search tool → custom tools over
  the Bedrock Knowledge Bases Retrieve API or a vector store.
- `google_search` (Gemini 2+ only) → off Gemini, the AgentCore Web Search
  tool (GA July 2026, MCP via Gateway, 7 of 22 listed regions) or another
  search API with its own terms.
- BigQuery tools, Agent Analytics, Online Monitors and Gemini Enterprise
  registration: re-platform each or drop it.

What ADK keeps: agents, workflows, callbacks, plugins, tool declarations,
evaluation sets and the A2A and MCP protocols, if ADK stays the framework.

### Gemini features that do not carry over

- **Google Search grounding:** no Bedrock equivalent, so citation UX and
  grounding evidence change.
- **Context caching:** Agent Platform caches implicitly and also offers
  explicit cache resources with a TTL (60 minutes by default, per a search
  summary). Bedrock has best-effort implicit caching and per-request cache
  checkpoints chained tools → system → messages (model minimums of 512 to
  4,096 tokens; mostly a 5-minute TTL), so editing a tool invalidates the
  rest.
- **Structured output:** Bedrock structured outputs (GA February 2026, from
  search summaries) cover some model families, accept a subset of JSON
  Schema Draft 2020-12, return 400 for unsupported features and can take
  minutes to compile a new schema. Retest `output_schema` repair loops and
  thinking settings on the target model.

### Other AWS agent offerings

- **Bedrock Agents** is now "Bedrock Agents Classic": closed to new
  customers, maintenance mode. Not a target.
- **AgentCore harness** (GA July 2026) defines agents as configuration and
  exports them to Strands code; **Strands Agents** is AWS's framework and
  supports Gemini. Either is a framework change, not a port; see
  [agent frameworks](agent-frameworks.md).
- **AgentCore Policy** accepts Cedar, natural language or Dogwood (a new
  open-source language with session-history conditions) and applies only at
  Gateway.

## What stays the same

- Business logic and tool bodies (only cloud SDK calls change); ADK agents,
  workflows, callbacks and guardrail code if ADK stays.
- PostgreSQL schemas and migrations; container images (plus an ARM64 build).
- OTel instrumentation (exporters change); evaluation sets and deterministic
  tests (baselines re-run); custom JSON or AG-UI frontend contracts.

## Status notes (2026-10-26)

- AgentCore GA milestones: core October 2025; Policy and Evaluations March
  2026; harness, Managed Knowledge Base, Web Search and A/B testing July
  2026; AWS Agent Registry August 2026 (new `agent-registry` namespace).
  Still preview: Runtime managed session storage, Payments, Failure Insights.
- AgentCore Gateway inference targets (October 2026) can front model
  providers, translate API dialects and fall back to another model.
- ADK docs moved from `google.github.io/adk-docs` to `adk.dev`; ADK's
  integrations page says "Knowledge Engine" and "Agent Search" where Google
  Cloud docs still say "RAG Engine".

## Unverified

- A maintained ADK memory or session service for AgentCore.
- ADK → Bedrock via `LiteLlm` end to end (tools, streaming, `output_schema`,
  usage); how ADK's spans render in CloudWatch GenAI Observability.
- An AWS counterpart to Agent Search or to Gemini Enterprise's end-user
  surface.
- Cross-cloud credentials for calling Gemini from AWS (for example Google
  workload identity federation); moving Identity Platform users into Cognito.
- Google-side GA or Preview status of Memory Bank and Agent Registry.

## Sources

All read 2026-10-26. "(search summary)" means the claim rests on a search
summary, not a full read of the page.

| Topic | URL |
| --- | --- |
| AgentCore FAQ | https://aws.amazon.com/bedrock/agentcore/faqs/ |
| AgentCore release notes | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html |
| AgentCore Runtime | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html |
| Runtime service and HTTP contracts | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-service-contract.html ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-http-protocol-contract.html |
| Any agent framework on AgentCore | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-any-agent-framework.html |
| AgentCore Memory and examples | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-examples.html |
| AgentCore Identity, Policy | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html |
| AgentCore Observability | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html |
| AgentCore regions | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html |
| Bedrock Agents (Classic) | https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html |
| Bedrock models at a glance | https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html |
| Bedrock Guardrails | https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html |
| Knowledge Base vector stores | https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html |
| Bedrock prompt caching | https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html |
| Bedrock structured output (search summary) | https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html ; https://aws.amazon.com/about-aws/whats-new/2026/02/structured-outputs-available-amazon-bedrock |
| S3 Vectors GA (search summary) | https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-s3-vectors-generally-available/ |
| Lambda timeout | https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html |
| EKS Pod Identity | https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html |
| ALB authentication | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html |
| Verified Permissions | https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html |
| Secrets Manager | https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html |
| Athena | https://docs.aws.amazon.com/athena/latest/ug/what-is.html |
| SQS queue types | https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html |
| EventBridge Scheduler | https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html |
| Step Functions workflow types | https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html |
| Comprehend PII; Macie | https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html ; https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html |
| ADK models and LiteLLM connector | https://adk.dev/agents/models/ ; https://adk.dev/agents/models/litellm/ |
| ADK sessions, memory, integrations, Google Search | https://adk.dev/sessions/session/ ; https://adk.dev/sessions/memory/ ; https://adk.dev/integrations/ ; https://adk.dev/integrations/google-search/ |
| Agent Runtime quickstart | https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart-adk |
| Agent Platform context cache (search summary) | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview |
| LiteLLM Bedrock provider | https://docs.litellm.ai/docs/providers/bedrock |
| Strands model providers | https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/ |
