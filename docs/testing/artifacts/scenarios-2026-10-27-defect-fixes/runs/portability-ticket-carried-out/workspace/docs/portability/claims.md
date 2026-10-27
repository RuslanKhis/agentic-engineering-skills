---
topic: claims
design: docs/architecture/claims.md
plan: docs/plans/claims.md
goal: G07
primary_build: GCP + Google ADK (unchanged)
concern: Martin Cole (CTO) wants to know what a later move to AWS would involve; Azure and LangGraph to be compared
targets: [aws, azure]
frameworks: [langgraph]
sources_checked: 2026-10-26
status: draft
---

# Portability assessment: Tidewater claims assistant

## Summary for the reader

- **Recommendation:** keep GCP and ADK as the build; hold this exit plan; run no second provider now. Reopen the question only when a trigger in "Recommended strategy" fires.
- **Google-specific on purpose:** Gemini on Vertex AI (D5), Agent Platform Memory Bank (D1), Vertex AI Search over policy wordings (D3), Firestore (D4) and Identity Platform (D6). The first four hold data or behaviour that must be regenerated or re-evaluated elsewhere, so they are expensive dependencies, not just provider choices. They buy managed recall (R2), clause-cited answers (R3, C3), owner-checked claims (R1, C1) and a quota-based spend stop (R6, C6) with little code.
- **Boundaries kept:** ADK's own seams only: the model string (already read from `MODEL_ID` in `claims/agent.py`), `BaseSessionService` and `BaseMemoryService`. No home-made wrapper layers are proposed.
- **What a move would involve:** a model change with a full re-evaluation, a rebuilt memory and retrieval layer, a Firestore data-model redesign, and identity re-mapping. The user ID is the verified `sub` (D6), and it keys claim ownership (C1) and memory scope (C2), so a change of identity provider must preserve it or remap both. Containers, tool logic and the React front end move cheaply. Overall this is a very large project with its own plan, not a configuration change; the stack is not cloud-agnostic and this document does not claim otherwise.

## Concern and scope

- **Question asked:** "what would it take to move this to AWS later?" (G07 ticket), raised by Martin Cole, CTO, recorded in the design's scope gate on 2026-09-18 as "what a later move to AWS would involve".
- **Move later or run on several now:** an exit plan at a known cost. The scope gate states the build stays on GCP and ADK, and no date or trigger for running on two providers is recorded, so multicloud now is not assessed as a goal.
- **Targets:** AWS and Azure as clouds, LangGraph as the framework to compare. All three are named in the design scope gate; the default framework set was not used, so OpenAI Agents SDK, Microsoft Agent Framework and Pydantic AI are left out because nobody asked for them.
- **In and out of scope:** the five dimensions (cloud, agent framework, model, service, deployment). Out: any change to the design, code or other goals; implementation on a target; claim decisions and payments (design scope gate). Model swap and whole-system move are kept apart below.

## Baseline architecture

Facts marked inspected were read in `claims/agent.py` and `claims/tools.py`; the rest is design-only. No tests directory and no infrastructure files exist in the workspace, so G01 and G02 evidence is taken from the plan.

- Web chat in the customer portal (React) served by the FastAPI service on Cloud Run behind the existing external load balancer (D6); design-only.
- ADK `LlmAgent` `claims_assistant` with tools `get_claim`, `add_note` and `PreloadMemoryTool`; model read from `MODEL_ID`, default `gemini-3.5-flash-001` (D5); inspected. The design also lists `upload_photo` and `search_wording`, not yet in code (G03, G04).
- Claim tools call `google.cloud.firestore` directly inside the tool bodies, with the owner check against `tool_context.user_id` and `firestore.ArrayUnion` for notes (D4, C1); inspected.
- `VertexAiSessionService` (D2) and `VertexAiMemoryBankService`, scope `{user_id}` (D1, C2); design-only: the code wires neither, so session and memory services are not yet set in the inspected files.
- Vertex AI Search data store over policy wordings, filtered by product version (D3, C3); design-only, planned G03.
- Cloud Storage for photos, path from claim ID (D4, C4); design-only, planned G04.
- Identity Platform sign-in, verified `sub` as user ID (D6, R1); design-only.
- After-model callback for payout promises (C5, G05) and the daily model quota cap (C6, G06); design-only, planned.
- The design records no observability, secrets or async components, so they are not classified.

## Component classification

| Component | Design IDs | Class | Why | Exit path |
| --- | --- | --- | --- | --- |
| React web chat | D6 | shared logic | No provider imports in the design; it talks to the FastAPI service | Re-point at the new backend URL and sign-in flow; re-run front-end tests |
| FastAPI service and container image | D6 | shared logic | Plain Python and a container; no cloud SDK in the service itself (design-only) | Rebuild image for the target (ARM64 if AgentCore is chosen); entrypoint adapter only if a managed agent runtime is used |
| Agent definition and instruction text (`claims/agent.py`) | D5, R5 | shared logic | Imports only ADK; model is a string from `MODEL_ID`; prompt is data. Moves across clouds with a test run, but a framework move rewrites it and a model move re-evaluates it | Cloud move: none. LangGraph: rewrite as a graph or `create_agent` call. Model: see the Gemini row |
| Claim tool bodies (`get_claim`, `add_note`) and owner check | D4, C1, R1 | provider-specific by choice | Inspected: Firestore client and `ArrayUnion` are called inline, so the logic is not free of provider imports. Bounded rewrite of two functions, no data conversion in the code itself | Rewrite the store calls on the target store; re-prove C1 (not found for another user's claim) with the forbidden-access test |
| Firestore claims, notes and photo metadata | D4, C1 | expensive dependency | Data to move; document model, array-union updates and security semantics differ from DynamoDB or Cosmos DB, so it is a data-model redesign | Redesign the model on the target, backfill with change capture, validate with checksums, re-prove C1. Volume is not recorded in the design |
| Cloud Storage photos | D4, C4, R4 | replaceable adapter | Plain objects under a path derived from the claim ID; bulk copy, no conversion (design-only; assumption: no signed-URL clients yet) | Bulk copy with egress; rewrite signed-URL and retention settings; re-run the C4 path-check test |
| ADK sessions (`VertexAiSessionService`) | D2 | replaceable adapter | `BaseSessionService` is ADK's seam and `DatabaseSessionService` runs on PostgreSQL. Holds only if history of open sessions need not move (assumption; see Open questions) | Swap the service in configuration. If history must carry over, the export path is `unverified` and the row becomes an expensive dependency |
| Memory Bank and `PreloadMemoryTool` | D1, C2, R2 | expensive dependency | Google generates the memories; another store extracts different ones. `BaseMemoryService` is the seam, so the code is cheap but the switch is not | Custom `BaseMemoryService` on the target; regenerate or discard memories; re-test recall and the `{user_id}` scope (C2); carry consent and erasure records |
| Vertex AI Search wordings index | D3, C3, R3 | expensive dependency | The index and embeddings do not move; source documents do. Clause citation and product-version filtering (C3) depend on its behaviour | Re-chunk, re-embed, rebuild the version filter, re-run retrieval evaluation; `search_wording` becomes a custom tool. No Agent Search counterpart identified on AWS |
| Gemini 3.5 Flash on Vertex AI (`gemini-3.5-flash-001`) | D5, R5 | expensive dependency | Cheap seam, expensive switch: the model string and ADK connectors make the code easy to change, but prompts, settings and the no-payout-promise behaviour (R5) need a full re-evaluation | Model candidate on the frozen evaluation set first; re-baseline per category. Gemini is not offered on Bedrock |
| Identity Platform sign-in and verified `sub` | D6, R1, C1, C2 | expensive dependency | Users and their `sub` values would have to move or be remapped; the same ID keys Firestore owner (C1) and Memory Bank scope (C2). Moving users between identity providers was not researched | Spike first. Preserve or map `sub`; rewrite token verification; repeat the security review |
| Cloud Run and the external load balancer | D6 | provider-specific by choice | Value: little to operate. A container rehosts; ingress, scaling and identity bindings are configuration, with no data and nothing to re-evaluate | Rebuild ingress and service identity on ECS or Container Apps; retest streaming and cold start |
| Spend cap on Vertex AI quota | D5, C6, R6 | provider-specific by choice | The enforcement is a Vertex AI quota (planned, G06), which has no like-for-like counterpart; bounded rewrite of the control | Re-implement the cap on the target's quotas or in an ADK plugin; repeat the C6 refusal test |
| No-payout-promise callback | C5, R5 | shared logic | An ADK after-model callback with no provider imports (planned, G05) | Cloud move: none. Model move: re-run the forbidden-phrase suite. Framework move: re-plumb as middleware |

## Dimensions

| Dimension | Assessment |
| --- | --- |
| Cloud | Assessed. Hosting, tool logic and photos move cheaply; Firestore, Memory Bank, Vertex AI Search and Identity Platform do not (D1, D3, D4, D6). |
| Agent framework | Assessed against LangGraph. The design is one `LlmAgent` with three tools and callbacks, so orchestration is small; sessions, callbacks, tests and re-evaluation carry the cost. |
| Model | Assessed. A model behind the same ADK agent is a model change with re-evaluation (D5), not a system move. Claude on Vertex AI is a native ADK connector and stays on GCP. |
| Service | Assessed. Managed services (D1, D2, D3, D4, D6) carry the lock-in; the application code is thin. |
| Deployment | Not a concern: one Cloud Run container behind the existing load balancer, no Agent Runtime features used (D6), so the image rehosts. |

## Cloud alternatives

Both targets are in scope because the scope gate names them. Statuses come from the reference notes read on 2026-10-26; nothing was deployed.

| Responsibility | GCP (design ID) | AWS | Azure | Difference | Portability |
| --- | --- | --- | --- | --- | --- |
| Hosting | Cloud Run behind an external load balancer (D6) | ECS on Fargate or EKS (GA); AgentCore Runtime (GA) | Container Apps or AKS (GA); Foundry hosted agents (GA) | Image rehosts. AgentCore needs ARM64 and an `/invocations` contract; hosted agents expect Microsoft's protocol libraries and ADK is not a named framework (`unverified` as packaged) | straightforward (containers) |
| Model | Gemini on Vertex AI (D5) | Bedrock models through `LiteLlm` (GA; ADK on Bedrock `unverified`); or call Gemini across clouds | Foundry Models; no Gemini found in the catalogue pages read (`unverified`) | A model change or a cross-cloud call; prompts, schemas and evaluation baselines redone | expensive (switch) / moderate (keep Gemini) |
| Sessions | Agent Platform sessions (D2) | `DatabaseSessionService` on Aurora or RDS PostgreSQL (GA) | `DatabaseSessionService` on Azure PostgreSQL (GA) | ADK supports PostgreSQL; `VertexAiSessionService` history has no written export | moderate |
| Memory | Memory Bank (D1) | AgentCore Memory (GA); no ADK memory service targets it (`unverified` that none is maintained) | Foundry Memory (preview); no ADK backend | Different extraction; custom `BaseMemoryService`; regenerate and retest | expensive |
| Retrieval | Vertex AI Search (D3) | Bedrock Knowledge Bases, OpenSearch, S3 Vectors, Aurora pgvector (GA) | Azure AI Search; Foundry IQ (partly GA) | No Agent Search equivalent identified on AWS; Gemini embeddings are not on Bedrock; re-chunk and re-embed | expensive |
| Claims data | Firestore (D4) | DynamoDB (GA) | Cosmos DB for NoSQL (GA) | Data model, queries, transactions and rules change | expensive |
| Photos | Cloud Storage (D4) | S3 (GA) | Blob Storage (GA) | Signed URLs become presigned URLs or SAS tokens; bulk copy with egress | straightforward |
| Identity | Identity Platform (D6) | Cognito with ALB `authenticate-cognito` or `authenticate-oidc` (GA) | Entra with Container Apps built-in auth (GA) | ALB passes a signed JWT the app must verify; user migration not researched; `sub` must be preserved or remapped | moderate (code) / expensive (users) |
| Spend cap | Vertex AI quota (C6, D5) | Bedrock service quotas and budgets; model dependent | Foundry deployment quotas | Quota semantics and refusal behaviour differ; not mapped one to one | moderate |

## Agent framework alternatives

| Concern | ADK (baseline) | LangGraph |
| --- | --- | --- |
| Agent with tools | `LlmAgent` with `get_claim`, `add_note`, `PreloadMemoryTool` | yes: `create_agent` or a graph |
| Sessions and history | `VertexAiSessionService` event log with state deltas (D2) | yes, as checkpointers (Postgres, SQLite, MongoDB, Redis, Cosmos DB); channel snapshots, so ADK records are unreadable |
| Cross-session memory | Memory Bank through `BaseMemoryService` and `PreloadMemoryTool` (D1) | partial: a store you choose and wire; Memory Bank has no first-party LangGraph path found in the reference (`unverified`) |
| Callbacks and guards | after-model callback for C5; owner checks in tools (C1) | partial: middleware and node logic; ordering and short-circuit rules differ, so every guard is re-proved |
| Structured output | `output_schema` | yes: `response_format` |
| Gemini on Vertex | native (D5) | yes: `langchain-google-vertexai` |
| Evaluation | scripted-model Runner tests, `adk eval` | partial: LangSmith plus `openevals`; cases move, runner is rewritten |
| Hosting | Cloud Run (D6) | yes: container anywhere; Agent Runtime template on GCP; hosted agents name it on Azure; named on AWS |
| Licence and status | Apache-2.0, GA | MIT, GA since 1.0.0; the Agent Server runtime is Elastic-2.0 |

A switch to LangGraph rewrites the agent wiring, callbacks, session storage and test runner; it does not remove any Google service by itself. What survives: tool bodies and the owner-check logic, instruction text once templating is converted, Pydantic schemas and the evaluation cases as data. LangGraph is not needed for any AWS or Azure move: ADK runs as a container on both, and the framework is a separate decision.

## Boundaries worth having

| Boundary | What it isolates | Reason (a, b, c or d) | Cost now | Existing ADK seam |
| --- | --- | --- | --- | --- |
| Model chosen by configuration (`MODEL_ID`) | The Gemini model name (D5) | (c) the framework already has the seam | none; already in `claims/agent.py` (inspected) | model connectors (native Claude and OpenAI, `LiteLlm`) |
| Session service by ADK interface | Agent Platform sessions (D2) | (c) the framework already has the seam | none; do not wrap it | `BaseSessionService`, `DatabaseSessionService` |
| Memory service by ADK interface | Memory Bank (D1) | (c) the framework already has the seam | none; do not wrap it, and do not put a common interface over memory extraction | `BaseMemoryService` |

Not proposed: a repository or port over Firestore. No second implementation is needed now (rule a is unconfirmed: how G01's tests fake Firestore is not visible), no switch has a date or trigger (rule b), and a store-neutral interface would hide the transaction and array-update semantics that differ on DynamoDB or Cosmos DB. The exit path is recorded in the classification instead. Also not proposed: a wrapper over Vertex AI Search or Memory Bank, which would reduce them to a common denominator.

## Feature differences and migration risks

- **Model behaviour (D5, R5, C5).** Likelihood moderate if a move happens; switching cost high. Prompts, output checks and the payout-promise suite must be re-run on the new model; Bedrock structured output accepts a subset of JSON Schema and Gemini features such as grounding have no counterpart (not used by this design).
- **Memory (D1, C2, R2).** Generated memories do not transfer; another extractor yields different recall. Consent and erasure records must be carried across. Switching cost high.
- **Retrieval (D3, C3, R3).** Re-embedding and a new filter change which clause is cited; the evaluation must be rebuilt. Switching cost high; AWS has no identified Agent Search counterpart.
- **Firestore (D4, C1).** Redesign, not a copy. Owner-check semantics must be re-proved after the move. Switching cost high; data volume unknown.
- **Identity (D6, R1, C1, C2).** The `sub` keys ownership and memory scope. A new identity provider that issues different IDs silently breaks R1 and R2 unless remapped. Switching cost high; user migration was not researched.
- **Cross-cloud Gemini.** A middle path hosts on AWS and keeps Gemini on Vertex AI; it defers the model cost but adds cross-cloud credentials, egress and residency questions. Credentials for this are `unverified`.
- **ADK on Bedrock or Azure OpenAI through `LiteLlm`** is plausible but not documented by ADK and not tested (`unverified`). ADK's pin on `litellm` caps the version because of compromised releases; keep that cap.
- **Policy facet.** IAM and retention rules do not migrate themselves; the security review and data-processing approvals repeat.
- **Likelihood.** Costly and not currently planned: the guidance for that quadrant is insurance, meaning an exit path and a trigger, which this document supplies.

## Recommended strategy

Keep the GCP and ADK build. Do not build for two providers now: no stated need, date or trigger exists, a second implementation would need its own contract tests, evaluation runs and on-call knowledge, and a lowest-common-denominator layer would remove the managed features (Memory Bank, Vertex AI Search) that the requirements rely on. The cost is accepted lock-in on five Google services, all listed above.

Hold this plan as the exit path. Reopen it when one of these happens: a dated decision to leave GCP, a client or regulator requirement on where claims data or model calls run, a model quality or price change that makes Gemini unsuitable, or a platform decision that makes AWS or Azure the corporate default. If the fear is model lock-in only, the model swap alone (for example Claude on Vertex AI behind the same agent) answers it at medium effort without leaving GCP.

If a move is ever approved, the least bad shape is: host the unchanged container on the target, keep ADK, use `DatabaseSessionService` on PostgreSQL, accept a model change and rebuild memory, retrieval and claims data deliberately. LangGraph adds a second rewrite and is not required for either cloud.

## Phased outline

1. **Decision and spike:** confirm the trigger, residency and approvals; spike identity migration and the `sub` mapping, and the ADK-on-target model connector, since both are `unverified`.
2. **Model candidate:** run the frozen evaluation set (cases kept as data, same judge) on the candidate model per category, including the payout-promise suite; stay on GCP.
3. **Strangler façade:** place a thin routing layer in front of the existing service; move the container first, with GCP still serving traffic.
4. **Data backfill:** load Firestore claims and photos by ETL with change capture, not dual-write; validate with checksums and replayed reads through the new tools; rebuild the wording index and re-run retrieval evaluation; regenerate or discard memories and re-test recall and scope.
5. **Parallel run:** shadow a sample of sessions offline through the evaluation harness; shadow traffic never executes write tools such as `add_note`.
6. **Cutover with rollback:** pause writes, finish the sync, validate, switch; keep GCP as the rollback until a deliberate decommission step.

## Relative effort

| Item | Relative effort (small / medium / large / very large / unknown) | Drivers | Assumptions |
| --- | --- | --- | --- |
| Container, ingress and hosting on AWS or Azure | small | Image rebuild, ingress and service identity configuration; no data | No managed agent runtime is used; ARM64 build only for AgentCore |
| Photos to S3 or Blob | small | Bulk copy, egress, signed-URL settings | assumption: photo volume is modest; not recorded in the design |
| Sessions to PostgreSQL | small | One service swap through ADK's seam; contract test | assumption: history of open sessions need not move; otherwise unknown; needs a spike |
| Model swap on GCP (for example Claude on Vertex AI) | medium | Re-evaluation of prompts, settings and R5 behaviour on the frozen set | Native ADK connector exists; effort sized by re-evaluation |
| Model on AWS or Azure | large | Re-evaluation, new connector path (`unverified`), output-schema checks, quota mapping for C6 | Gemini kept off the table; cross-cloud Gemini would be medium plus egress and residency work |
| Memory Bank replacement | large | Regenerated memories, custom `BaseMemoryService`, recall re-evaluation, erasure records | Memories may be discarded if the business accepts it (open question) |
| Vertex AI Search replacement | large | Re-chunk, re-embed, version filter, retrieval re-evaluation | One document per product version, volume small |
| Firestore to DynamoDB or Cosmos DB | large | Data-model redesign, backfill, re-proving C1 | Data volume unknown |
| Identity Platform migration | unknown; needs a spike | User migration, `sub` preservation, token verification, security review | Not researched in the references |
| Framework switch to LangGraph | large | Re-evaluation, sessions, callbacks (C5), test runner rewrite | Single agent, three tools; orchestration itself is small |
| Whole-system move to AWS | very large | Model, memory, retrieval, data and identity all change together; needs its own plan | Sized by the combined drivers, with re-evaluation per category |

Schedule risks outside the team's control: data-processing agreements and residency terms for policyholder data and photos, the insurer's AI governance sign-off, and sponsor re-approval of the spend ceiling (R6) on a new provider's pricing. None is dated in the plan.

## Optional recommendations for the current build

None.

## Open questions

- **Is there a date or trigger for leaving GCP?** Answerable by Martin Cole. Assumption used: none, so the strategy is an exit plan, not multicloud.
- **Would a move keep calling Gemini across clouds?** Answerable by Martin Cole and the platform team. Assumption used: not assumed; both shapes are shown. It changes the model row from expensive to moderate and adds residency and egress work.
- **Must in-flight session history carry over?** Answerable by Joanne Price. Assumption used: no, so sessions are a replaceable adapter.
- **May Memory Bank memories be discarded and rebuilt after a move?** Answerable by Joanne Price and the privacy owner. Assumption used: yes, with consent and erasure records carried across; otherwise the cost is higher.
- **How many claims, photos and policy versions exist?** Answerable by the engagement lead. Assumption used: modest volumes; sizes for Firestore, photos and retrieval depend on it.
- **Can the identity provider's `sub` values be preserved or mapped?** Answerable by the platform and identity team. Assumption used: unknown; identity effort stays "unknown; needs a spike".
- **How does G01's test suite fake Firestore?** Answerable by Tom Reid. The tests were not in the workspace. It decides whether a claim-store contract test already exists (boundary rule a) and was not assumed.
- **Is a frozen evaluation set planned?** Answerable by the designer. No plan goal builds one; model and framework re-baselines assume it. A specialist for it (`adk-agent-evaluation`) is not installed in this workspace, so no recommendation is made; the designer may add a goal.
- **Which cross-cloud claims are `unverified`?** ADK on Bedrock or Azure through `LiteLlm`, a maintained ADK memory service for AgentCore, Gemini absent from the live Azure catalogue, and Google-side GA status of Memory Bank. Platform teams can confirm with a spike.

## Sources

No web access was available in this session, so no source was re-verified. Each URL below is taken from the skill's reference notes, which record the read date shown.

| Claim or topic | URL | Read on |
| --- | --- | --- |
| Portability terms, exit-plan versus multicloud, abstraction costs (NIST SP 500-291r2; Hohpe, "Don't get locked up into avoiding lock-in") | https://doi.org/10.6028/NIST.SP.500-291r2 ; https://martinfowler.com/articles/oss-lockin.html | 2026-10-26 |
| Strangler fig, contract tests, parallel change | https://martinfowler.com/bliki/StranglerFigApplication.html ; https://martinfowler.com/bliki/ContractTest.html | 2026-10-26 |
| ADK sessions, models, LiteLLM connector | https://adk.dev/sessions/session/ ; https://adk.dev/agents/models/ ; https://adk.dev/agents/models/litellm/ | 2026-10-26 |
| ADK memory and Google Search grounding limits | https://adk.dev/sessions/memory/ ; https://adk.dev/integrations/google-search/ | 2026-10-26 |
| ADK 2.13.0 LiteLLM version cap | https://raw.githubusercontent.com/google/adk-python/v2.13.0/pyproject.toml | 2026-10-26 |
| Google model migration guide (re-testing between model versions) | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate | 2026-10-26 |
| AWS AgentCore Runtime, Memory, Identity, release notes | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html ; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html | 2026-10-26 |
| Any agent framework on AgentCore (ADK example) | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-any-agent-framework.html | 2026-10-26 |
| Bedrock models, Knowledge Bases, structured output (search summary) | https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html ; https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html ; https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html | 2026-10-26 |
| ALB authentication (signed JWT) | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html | 2026-10-26 |
| LiteLLM Bedrock and Azure providers | https://docs.litellm.ai/docs/providers/bedrock ; https://docs.litellm.ai/docs/providers/azure/ | 2026-10-26 |
| Azure Foundry hosted agents, Foundry Memory (preview), Foundry Models | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents ; https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory ; https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview | 2026-10-26 |
| Azure Container Apps and authentication; Azure AI Search vectors; Cosmos DB vectors (search summary) | https://learn.microsoft.com/en-us/azure/container-apps/overview ; https://learn.microsoft.com/en-us/azure/search/vector-search-overview ; https://learn.microsoft.com/en-us/cosmos-db/index-vector-data | 2026-10-26 |
| LangGraph release, checkpointing, licence (vendor-authored for its own product) | https://github.com/langchain-ai/langgraph | 2026-10-26 |
| LangChain and LangGraph docs | https://github.com/langchain-ai/docs | 2026-10-26 |
| Agent Runtime and LangGraph template on GCP | https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime | 2026-10-26 |
