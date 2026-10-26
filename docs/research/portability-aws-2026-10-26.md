# Portability of a GCP + ADK design to AWS — 26 October 2026

## Scope and snapshot

How each Google Cloud responsibility in
[gcp-decisions.md](../../skills/adk-system-designer/references/gcp-decisions.md)
would map to AWS, for the `adk-portability-planning` AWS reference. This covers
differences that matter to architecture and migration only. It contains no
implementation, IaC, IAM policy or price figures. Facts come from AWS, Google
Cloud, ADK (now served at `adk.dev`) and LiteLLM documentation, all read on
26 October 2026. Nothing was deployed or run. GCP + ADK stays the primary path.

**Conclusion.** An ADK application is portable: AWS documents ADK on
AgentCore Runtime, and containers, tool functions, Postgres and OTel move with
little change. The expensive parts are the ones Google manages for ADK: Gemini
itself (it is not offered on Bedrock), Memory Bank, RAG and Agent Search
retrieval, Google Search grounding, Firestore and BigQuery. Each one needs a
rewrite or a data rebuild, then re-evaluation. A middle path is AWS hosting
that keeps calling Gemini across clouds. It defers the model cost but adds
cross-cloud identity, egress and residency questions.

## Summary

| # | GCP responsibility | Plausible AWS option(s) | AWS status (26 Oct 2026) | Rating |
| --- | --- | --- | --- | --- |
| 1 | Cloud Run, GKE, Agent Runtime | ECS on Fargate, EKS, AgentCore Runtime; Lambda for short turns only | GA (AgentCore GA Oct 2025) | moderate |
| 2 | Gemini on Agent Platform / Gemini API | Bedrock models (Claude, Nova, Gemma, others) via LiteLlm; or keep Gemini cross-cloud | GA; Gemini not on Bedrock | expensive (model switch) / moderate (keep Gemini) |
| 3 | Sessions, Memory Bank, Agent Registry, Gemini Enterprise, A2A hosting | DatabaseSessionService on Aurora PG; AgentCore Memory; AWS Agent Registry; AgentCore Runtime A2A | GA; Registry GA Aug 2026 in 5 regions | expensive |
| 4 | Service accounts, Identity Platform, IAP | IAM roles (task role, EKS Pod Identity, AgentCore execution role), Cognito, ALB OIDC auth, AgentCore Identity; Verified Permissions | GA | moderate |
| 5 | Secret Manager | AWS Secrets Manager | GA | straightforward |
| 6 | Cloud SQL / AlloyDB, Firestore, BigQuery | RDS/Aurora PostgreSQL; DynamoDB; Redshift or Athena | GA | straightforward (PG) / expensive (Firestore, BigQuery) |
| 7 | Cloud Storage | S3 | GA | straightforward |
| 8 | RAG Engine, Agent Search, vector search | Bedrock Knowledge Bases, AgentCore Managed Knowledge Base, OpenSearch, S3 Vectors, Aurora pgvector | GA (S3 Vectors Dec 2025; Managed KB Jul 2026) | expensive |
| 9 | Cloud Tasks, Pub/Sub | SQS, SNS, EventBridge (+ Scheduler), Step Functions | GA | moderate |
| 10 | Cloud Logging/Trace/Monitoring + OTel | CloudWatch, X-Ray, ADOT, AgentCore Observability | GA | moderate |
| 11 | Model Armor, Sensitive Data Protection | Bedrock Guardrails (ApplyGuardrail), AgentCore Policy, Comprehend PII, Macie | GA | moderate |
| 12 | Cloud Build, Artifact Registry | CodeBuild (or existing CI), ECR | GA | straightforward |

## Row detail

**1. Hosting (moderate).** Cloud Run → ECS on Fargate; GKE → EKS; Agent
Runtime (now under "Gemini Enterprise Agent Platform", formerly Vertex AI Agent
Engine) → AgentCore Runtime. AgentCore runs each user session in its own microVM
for up to 8 hours (14 days on the newer Instances type), bills by consumption
with I/O wait free, takes 100 MB payloads and supports HTTP, MCP, A2A and AG-UI.
The container must be **ARM64** and serve `/invocations` and `/ping` on port
8080, with the session ID in `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id`. The
microVM is wiped when the session ends, so in-process state is lost. Lambda's
900-second limit rules it out for long or streaming turns. *Migration:* an
AgentCore entrypoint adapter, an ARM64 build, retests of streaming, cold start
and concurrency, and Cloud Run ingress/IAP mapped to ALB and security groups.

**2. Model inference (expensive if the model changes).** On Bedrock, Google
offers only Gemma; there is no Gemini model. Moving off Gemini means new prompts,
model settings, output-schema checks and a full evaluation re-baseline. The other
path keeps Gemini and calls the Gemini API or Agent Platform from AWS. AgentCore
Runtime says it is model-agnostic and names Gemini. That path brings cross-cloud
credentials, egress and data residency into scope. AgentCore Gateway inference
targets (October 2026) can front model providers, translate between API dialects
and fall back to another model. *Migration:* re-evaluate everything if the model
changes. If Gemini stays, record a residency decision and a credential decision.

**3. Managed agent capabilities (expensive).**
- *Sessions:* ADK's `DatabaseSessionService` (PostgreSQL, MySQL, SQLite) runs on
  Aurora or RDS PostgreSQL, which makes this part straightforward. Existing
  `VertexAiSessionService` history needs an export and import that nobody has
  written yet.
- *Memory Bank → AgentCore Memory:* short-term events plus long-term records
  extracted by strategies (semantic, summary, preference, episodic, custom) into
  namespaces, with a TTL since October 2026. AWS examples cover LangChain/
  LangGraph, Strands and AWS SDKs, not ADK, and ADK ships only in-memory, Memory
  Bank and RAG memory services, so a custom `BaseMemoryService` is required.
  Extraction differs: re-extract memories rather than copy them, and retest
  recall, scoping and erasure.
- *Agent Registry / Gemini Enterprise:* AWS Agent Registry (GA August 2026, five
  regions) catalogues agents, tools, MCP servers and skills. No AWS replacement
  for Gemini Enterprise as the end-user surface was researched.
- *A2A hosting:* AgentCore Runtime serves A2A on port 9000 at the root path,
  with SigV4 or OAuth. The agent card and auth wiring change.
- *Bedrock Agents* is now "Bedrock Agents Classic". It is closed to new
  customers and in maintenance mode, so it is not a target. The *AgentCore
  harness* (GA July 2026) defines agents as configuration and exports them to
  Strands code. *Strands Agents* is AWS's own framework and supports Gemini.
  Either one means rewriting the agent: a framework change, not a port.

**4. Identity (moderate).** Service accounts become IAM roles: an ECS task role,
an EKS Pod Identity association, or the AgentCore execution role. Pod Identity
is not supported for pods on Fargate. AgentCore Identity adds agent workload
identities, inbound JWT from Cognito, Entra ID or Okta, an outbound OAuth/API-key
token vault and on-behalf-of exchange. Identity Platform maps to Cognito user
pools. IAP's closest equivalent is ALB `authenticate-oidc` or
`authenticate-cognito`. The ALB passes user claims in a signed `x-amzn-oidc-data`
JWT (ES256), and the app must verify that signature and the `signer` ARN. IAP's
headers and audience differ. Cedar authorisation is available as Verified
Permissions or AgentCore Policy, which applies only at Gateway. *Migration:*
rewrite token verification and the ownership checks keyed on it. Moving existing
users between identity providers is a project of its own (not researched).

**5. Secrets (straightforward).** Secrets Manager is billed by usage and offers
scheduled rotation, through managed rotation or a Lambda rotation function.
AgentCore Identity can reference existing Secrets Manager secrets. *Migration:*
copy the values, change the client calls and re-grant access by role. Retest
anything that pins a secret version.

**6. Databases (straightforward to expensive).** Cloud SQL PostgreSQL to RDS or
Aurora PostgreSQL is a dump-and-restore. Check extension parity, including
pgvector. AlloyDB-only features would not carry over (not itemised here).
Firestore to DynamoDB changes the data model, the query and transaction patterns
and the security rules, so the data layer must be rewritten. Analytics on
BigQuery would go to Redshift or Athena. Athena runs SQL over S3 and bills per
query. The SQL dialect, partitioning, reviewed SQL-agent templates, schema
descriptions and the cost guards built on BigQuery's bytes-billed model all need
rework and re-evaluation. *Migration:* moving the data and validating it, plus
retesting every SQL-agent case.

**7. Object storage (straightforward).** S3 covers buckets, presigned URLs,
lifecycle and encryption. *Migration:* bulk copy, which carries cross-cloud
egress charges. Rewrite the signed-URL and retention or lock settings, and
re-grant access through IAM.

**8. Retrieval (expensive).** RAG Engine (which ADK's docs now call
"Knowledge Engine") maps to Bedrock Knowledge Bases or to the AgentCore Managed
Knowledge Base, which is queried through Gateway. Knowledge Bases supports these
vector stores: OpenSearch Serverless, OpenSearch Managed (public-access domains
only, VPC domains are not supported), S3 Vectors, Aurora PostgreSQL pgvector,
Neptune Analytics, Pinecone, Redis and MongoDB Atlas. S3 Vectors has been GA
since December 2025. It stores float embeddings only, allows 1 KB of metadata
and 35 keys per vector under a knowledge base, and is suited to infrequent
queries. Agent Search (formerly Vertex AI Search) has no direct equivalent
identified here. *Migration:* Gemini embeddings are not on Bedrock, so the corpus
must be re-chunked and re-embedded. Metadata filters, access scoping and
retrieval quality all need re-evaluation. ADK's built-in retrieval tools become
custom tools.

**9. Async work (moderate).** Cloud Tasks pushes over HTTP. SQS is pull-based:
a standard queue gives at-least-once delivery with best-effort ordering, and a
FIFO queue gives exactly-once processing within message groups through
deduplication IDs. EventBridge Scheduler covers one-off scheduled invocations,
delivered at least once. Pub/Sub maps to SNS or EventBridge. Durable multi-step
work maps to Step Functions. Standard workflows run exactly once for up to a
year. Express workflows run for up to five minutes, at least once when
asynchronous. *Migration:* switch push to pull, or wire an event-source mapping.
Re-derive idempotency keys, replace OIDC push auth with IAM, and retest retries.

**10. Observability (moderate).** Manual OTel spans and attributes carry over.
Exporters change to ADOT with CloudWatch Transaction Search. AgentCore
Observability also accepts agents hosted outside AgentCore through ADOT
environment variables. AWS names auto-instrumentation only for Strands, LangChain
and CrewAI, so how ADK's spans render in AWS dashboards is unverified. Setting
`AWS_GENAI_CONTENT_EXTRACTION_OPT_OUT=true` *keeps* model and tool payloads on
spans, so the redaction policy needs a fresh review. *Migration:* rebuild log
metrics, alerts and dashboards as CloudWatch alarms. The BigQuery Agent Analytics
pipeline has no counterpart and must be rebuilt.

**11. Safety screening (moderate).** Bedrock Guardrails can screen through
`ApplyGuardrail` without invoking a model. Its filters cover harmful content
(including Prompt Attack), denied topics, words, sensitive information
(probabilistic plus regex), contextual grounding and Automated Reasoning.
AgentCore Policy can run Guardrails at Gateway. Comprehend PII detection supports
English and Spanish text only, real-time calls take up to 100 KB, and redaction
runs as an asynchronous batch job. Macie only discovers sensitive data in S3; it
cannot screen inline. *Migration:* detectors, thresholds and language coverage
differ, so Model Armor templates and SDP info types cannot be copied over. Re-run
the PII and adversarial suites.

**12. CI and registry (straightforward).** Cloud Build maps to CodeBuild (or the
team's existing CI) and Artifact Registry to ECR. Builds must add ARM64 for
AgentCore Runtime.

## Can ADK run on AWS?

Yes, as an ordinary container on ECS/Fargate or EKS, and on AgentCore Runtime.
AWS's "Use any agent framework" page includes a Google ADK example. That example
uses a Gemini API key, `InMemorySessionService` and `google_search`, so it keeps
Gemini and loses sessions when the microVM ends. ADK's model docs list a
`LiteLlm` connector, but no ADK page mentions Bedrock. LiteLLM's own docs cover
`bedrock/` and `bedrock/converse/` routes, tool calling and `response_format`;
for some models LiteLLM emulates the schema with a forced tool call. ADK on
Bedrock through LiteLlm is therefore plausible but **not documented by ADK and
not tested here**. The
[LiteLLM note](litellm-comparison-2026-10-25.md) already found two problems on
`LiteLlm` routes: reasoning tokens counted twice, and a changed `num_retries`
meaning. Lambda fits only short, non-streaming turns.

What is lost or must be replaced:
- `VertexAiSessionService` → `DatabaseSessionService` on Aurora/RDS PostgreSQL.
- Memory Bank (`VertexAiMemoryBankService`) → custom `BaseMemoryService` over
  AgentCore Memory or Postgres.
- RAG (`VertexAiRagRetrieval`, Knowledge Engine) and the Agent Search tool →
  custom tools over the Bedrock KB Retrieve API or a vector store.
- `google_search` (Gemini 2+ only) → off Gemini, the AgentCore Web Search tool
  (GA July 2026, MCP via Gateway, 7 of 22 listed regions) or another search API.
- BigQuery tools, Agent Analytics, Online Monitors and Gemini Enterprise
  registration: re-platform each one or drop it.

## Gemini-specific features that do not carry over

Google Search grounding (Gemini 2+ only, the sole tool on its agent, with
search suggestions that must be rendered) has no Bedrock equivalent, so citation
UX and grounding evidence change. Context caching differs: Agent Platform caches
implicitly by default and also offers explicit cache resources with a TTL (60
minutes by default) billed for storage, while Bedrock has best-effort implicit
caching and per-request cache checkpoints (model minimums of 512 to 4,096 tokens,
mostly a 5-minute TTL, 1 hour on some models) chained tools → system → messages,
so editing a tool invalidates the rest. Bedrock structured outputs (GA February
2026) cover only some model families (Claude 4.5+, select open-weight), accept a
subset of JSON Schema Draft 2020-12, return a 400 for unsupported features, and
can take minutes to compile a new schema (cached 24 hours). Gemini
`response_schema` behaviour, ADK `output_schema` repair loops and thinking
settings all need retesting on the target model.

## What stays the same

- Business logic and tool-function bodies (only cloud SDK calls change); ADK
  agents, workflows, callbacks and guardrail code, if ADK stays.
- PostgreSQL schemas and migrations; container images (plus an ARM64 build).
- OTel instrumentation (only exporters change); evaluation sets and
  deterministic tests (baselines re-run); custom JSON or AG-UI frontend contracts.

## Name and status surprises

- ADK docs moved from `google.github.io/adk-docs` to `adk.dev` (301 redirect).
  ADK's integrations page now says "Knowledge Engine" and "Agent Search", while
  Google Cloud docs still say "RAG Engine".
- "Bedrock Agents Classic" is closed to new customers; Bedrock lists Gemma, not
  Gemini; AgentCore Runtime requires ARM64.
- AgentCore GA: core October 2025; Policy and Evaluations March 2026; Harness,
  Managed Knowledge Base, Web Search, A/B testing July 2026; AWS Agent Registry
  August 2026 (new `agent-registry` namespace). Still preview: Runtime managed
  session storage, Payments, Failure Insights.
- Policy accepts Cedar, natural language or Dogwood, a new open-source language
  with session-history ("temporal") conditions.

## Unverified

- A maintained ADK memory or session service for AgentCore, outside official docs.
- ADK → Bedrock via `LiteLlm` end to end (tools, streaming, `output_schema`,
  usage); how ADK's own spans render in CloudWatch GenAI Observability.
- An AWS counterpart to Agent Search or to Gemini Enterprise's end-user surface.
- Cross-cloud credentials for Gemini from AWS (for example, Google workload
  identity federation); moving Identity Platform users into Cognito.
- Google-side GA or Preview status of Memory Bank and Agent Registry.

## Sources (all read 2026-10-26)

- AgentCore: [FAQ](https://aws.amazon.com/bedrock/agentcore/faqs/); [release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html); [Runtime](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html); [service contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-service-contract.html); [HTTP contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-http-protocol-contract.html); [any framework](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-any-agent-framework.html); [Memory](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html); [Memory examples](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-examples.html); [Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html); [Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html); [Observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html); [configure observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html); [regions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html).
- Bedrock: [Agents (Classic)](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html); [models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html); [Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html); [KB vector stores](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html); [prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html); [structured output](https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html) and [What's New, Feb 2026](https://aws.amazon.com/about-aws/whats-new/2026/02/structured-outputs-available-amazon-bedrock) (search-result summaries only).
- Other AWS: [S3 Vectors GA](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-s3-vectors-generally-available/) (search summary); [Lambda timeout](https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html); [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html); [ALB authentication](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html); [Verified Permissions](https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html); [Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html); [Athena](https://docs.aws.amazon.com/athena/latest/ug/what-is.html); [SQS queue types](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html); [EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html); [Step Functions types](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html); [Comprehend PII](https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html); [Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html).
- Google / ADK: [ADK models](https://adk.dev/agents/models/); [LiteLLM connector](https://adk.dev/agents/models/litellm/); [sessions](https://adk.dev/sessions/session/); [memory](https://adk.dev/sessions/memory/); [integrations](https://adk.dev/integrations/); [Google Search tool](https://adk.dev/integrations/google-search/); [Agent Runtime quickstart](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/quickstart-adk); [context cache](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview) (search summary).
- Third party: [LiteLLM Bedrock provider](https://docs.litellm.ai/docs/providers/bedrock); [Strands model providers](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/).

## Limits of this note

Desk research only: nothing was deployed, invoked or measured. Ratings are
qualitative, not effort estimates, and no prices are given. AgentCore shipped
monthly through 2026, so recheck its release notes before quoting a status. The
source list marks claims that rest on search summaries. Google-side status comes
from the toolkit's references and was not re-verified. Azure is out of scope.
