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

- **Recommendation:** keep GCP and ADK as built, hold this exit plan, and reopen it only on a named trigger (see Recommended strategy). Do not run a second provider now.
- **Google-specific on purpose:** Memory Bank (D1, C2) buys recall scoped to the verified user without us writing memory extraction. Agent Platform sessions (D2) buy managed history. Vertex AI Search (D3, C3) buys policy-wording retrieval with a version filter. Firestore (D4, C1) buys the claims store. Gemini on Vertex AI (D5) is the model. Identity Platform (D6) holds the sign-in. Each of these is an expensive dependency (data to move or regenerate, behaviour to re-evaluate), not a code problem.
- **Boundaries kept:** ADK's own seams only: `BaseSessionService`, `BaseMemoryService` and the model connectors. No home-made wrapper is proposed.
- **What a move would involve:** the largest drivers are (1) the claims data in Firestore, which has no like-for-like AWS or Azure store; (2) regenerating Memory Bank memories and re-running recall tests; (3) re-chunking and re-embedding the policy wordings and re-proving clause citation (C3); (4) a model change with a full re-evaluation, because Gemini is not on Bedrock and was not found in the Azure catalogue pages read (`unverified`); (5) moving Identity Platform users, which is not sized. The containers, tool logic and the React front end move with little change. The answer to "AWS later?" is yes, at a large and partly unsized cost, and no step is a configuration change.

## Concern and scope

- **Question asked:** the scope gate records that the CTO "wants to know what a later move to AWS would involve" (Martin Cole, 2026-09-18, design scope-gate row "Portability"); ticket G07 phrases it as "what would it take to move this to AWS later?".
- **Move later or run on several now:** an exit plan at a known cost. No date, trigger or requirement to run on several providers now was recorded, so multicloud is out. Assumption: the CTO's concern is exit cost and negotiating position, not a planned move.
- **Targets:** AWS and Azure as clouds, LangGraph as the one framework to compare. All three were named in the scope gate and G07, so the default framework set was not used. Other frameworks are left out on purpose.
- **In and out of scope:** the five dimensions (cloud, framework, model, service, deployment) are covered. A model swap is kept apart from a system move. Out of scope: any change to the design, the code or other goals; building anything on a target; prices, dates and durations (no plan measurement record exists, so sizes are relative only); claim decisions and payments (design out-of-scope row).

## Baseline architecture

Facts are marked `inspected` (read in `claims/`) or `design-only`.

- Python 3.12, `google-adk` 2.12.0 on Cloud Run in europe-west2 (D6): design-only. The README says `google-adk` is not installed here, so ADK API facts were not checked against 2.12.0; the references were checked against 2.13.0.
- ADK agent `claims_assistant` with `LlmAgent`, model from `MODEL_ID` defaulting to `gemini-3.5-flash-001` (D5), tools `get_claim` and `add_note`, and `PreloadMemoryTool` (D1): inspected in `claims/agent.py`. `upload_photo` and `search_wording` are design-only (G04 and G03 are not built).
- `get_claim` and `add_note` read and write Firestore with an owner check on the verified user ID (D4, C1): inspected in `claims/tools.py`. The only provider import in the code is `google.cloud.firestore`.
- Agent Platform `VertexAiSessionService` (D2) and `VertexAiMemoryBankService` (D1, C2): design-only; the grep found no such import. G02 evidence says recall was tested with `InMemoryMemoryService` and a scripted model, and live recall on the dev Agent Engine was not run.
- Vertex AI Search data store over policy wordings, one document per product version, filtered by product version (D3, C3): design-only (G03 planned).
- Cloud Storage for photos with the path derived from the claim ID (D4, C4): design-only (G04 planned).
- Identity Platform sign-in; the verified `sub` is the user ID (D6, R1): design-only.
- FastAPI service and React web chat on Cloud Run behind the existing external load balancer (D6): design-only; no service code exists yet.
- After-model callback blocks payout promises (C5, R5) and Vertex AI quota caps daily spend (C6, R6): design-only (G05 and G06 planned).
- Not recorded in the design: observability and alerting, service-account and IAM layout, secrets, CI and registry, async work, an evaluation set. They are listed as open questions rather than assumed.

## Component classification

| Component | Design IDs | Class | Why | Exit path |
| --- | --- | --- | --- | --- |
| Agent instruction text and tool docstrings | R5, D5 | shared logic | Plain text, no provider import (`INSTRUCTION` in `claims/agent.py`). | Moves as data; tool docstrings and wording still need re-evaluation on another model. |
| Tool logic: owner check and note handling | C1, R1 | replaceable adapter | The logic is a few lines, but `claims/tools.py` imports `google.cloud.firestore` and builds the client inside the module, so it is not shared logic. The port is `_client()` and two calls. | Rewrite the data calls against the new store behind the same function signatures; re-run the C1 owner-check tests. The data store itself is the next row. |
| ADK agent wiring, callbacks and tests (`LlmAgent`, `PreloadMemoryTool`, after-model callback for C5) | D1, C5, R5 | expensive dependency | A framework move needs re-evaluation, and ADK callbacks, state and Runner tests do not map one to one. Small today: one agent, two built tools. | Keep ADK on any cloud (it runs in a container). A switch to LangGraph rewrites orchestration and callbacks into graph nodes and middleware, and re-proves C5 with its forbidden-action test. |
| FastAPI service and React chat | D6 | replaceable adapter | Containerised web code; no provider import found because the service is not written yet (design-only). | Rehost the image; rewire the sign-in token check and the load balancer. |
| Agent Platform sessions (`VertexAiSessionService`) | D2, R2 | expensive dependency | History lives in Agent Platform and its export path is `unverified`; ADK `Event` rows are unreadable by other frameworks. | Seam: `BaseSessionService`; `DatabaseSessionService` on Postgres is ADK's supported alternative. Switch: start new sessions on the target and freeze or discard old history. Needs a retention decision (open question). |
| Memory Bank with `PreloadMemoryTool` | D1, C2, R2 | expensive dependency | Google generates the memories; another store extracts different ones. Scope `{user_id}` and erasure records have to be carried over. | Seam: `BaseMemoryService` (custom, nothing maintained was found for AgentCore or Azure). Switch: regenerate from retained conversations or let memory rebuild, and re-run the C2 recall-isolation tests. |
| Vertex AI Search over policy wordings | D3, C3, R3 | expensive dependency | Source documents move but the index does not. The product-version filter and clause citation are tied to this retrieval. | Re-chunk and re-embed with the target's embedding model, rebuild the version filter in a custom tool, re-run retrieval and citation tests (C3). |
| Firestore: claims, notes, photo metadata | D4, C1, R1, R4 | expensive dependency | Live policyholder data; DynamoDB and Cosmos DB change the data model, queries and transactions (target references). | Redesign the data model, backfill with change capture, validate with checksums, re-prove owner checks (C1) on the new store. |
| Cloud Storage for photos | D4, C4, R4 | replaceable adapter | Object storage exists on both targets; bytes copy with no conversion. Volume is unknown. | Bulk copy, rewrite signed-URL and retention settings, keep the claim-ID path rule (C4). |
| Gemini 3.5 Flash on Vertex AI (`gemini-3.5-flash-001`) | D5 | expensive dependency | Gemini is not on Bedrock; no Gemini found in the Azure catalogue pages read. Another model needs new prompts, settings and a re-baseline. | Seam: ADK model connectors and `MODEL_ID` (cheap seam, expensive switch). Switch: candidate model on a frozen evaluation set first. Alternative: keep calling Gemini across clouds, which adds identity, egress and residency decisions. |
| Vertex AI quota as the spend cap | C6, R6 | provider-specific by choice | The cap is enforced by a Google quota; no code to port. | Re-create the cap with the target's quotas or budgets and re-test the refusal outcome. |
| Cloud Run behind the external load balancer | D6 | provider-specific by choice | One container, no Agent Runtime features (design lists Cloud Run, not Agent Runtime). | Rehost the image on ECS on Fargate or EKS (AWS) or Container Apps or AKS (Azure); rebuild ingress and routing. |
| Identity Platform sign-in | D6, R1 | expensive dependency | User accounts and token verification; the verified `sub` is the user ID that every ownership check (C1, C2, C4) keys on. | Rewrite token verification; move users to Cognito or Entra (not researched), keep or remap the user IDs, repeat the security review. Whether IDs survive is an open question. |

## Dimensions

| Dimension | Assessment |
| --- | --- |
| Cloud | Assessed: AWS and Azure. Hosting and objects move easily; data stores, retrieval, memory and identity do not (see Cloud alternatives). |
| Agent framework | Assessed: LangGraph. Agent logic is small, but sessions, callbacks and tests are ADK-bound; a framework move is separate from a cloud move. |
| Model | Assessed: a model swap behind the same ADK agent is a model change with a re-evaluation, not a system move; Gemini is the open dependency on both targets. |
| Service | Assessed: Memory Bank, sessions, Vertex AI Search, Firestore and Identity Platform are the managed services in the design; each has its own row above. |
| Deployment | not a concern: one Cloud Run container behind an existing load balancer, no Agent Runtime features, so the image rehosts; only ingress and identity wiring change. |

## Cloud alternatives

Status and differences come from the skill's AWS and Azure references, read 2026-10-26; nothing was deployed or run. Ratings are qualitative.

| Responsibility | GCP (design ID) | AWS | Azure | Difference | Portability |
| --- | --- | --- | --- | --- | --- |
| Hosting | Cloud Run (D6) | ECS on Fargate or EKS; AgentCore Runtime documents ADK (GA) | Container Apps or AKS (GA); hosted agents need Microsoft protocol libraries and ADK is not a named framework (`unverified` as a host) | Image moves; AgentCore wants ARM64 and `/invocations`; ingress and auth rewired | moderate |
| Model | Gemini 3.5 Flash on Vertex AI (D5) | Bedrock models through `LiteLlm`; Gemini is not on Bedrock; or call Gemini across clouds. ADK on Bedrock via `LiteLlm` is `unverified` | Foundry Models (Azure OpenAI and partner models); no Gemini in the pages read (`unverified` against the live catalogue); ADK with Azure through `LiteLlm` is `unverified` | Model change with full re-evaluation, or a cross-cloud call | expensive |
| Sessions | Agent Platform sessions (D2) | `DatabaseSessionService` on Aurora or RDS PostgreSQL (GA) | `DatabaseSessionService` on Azure PostgreSQL (GA) | History does not export; new store | moderate |
| Memory | Memory Bank (D1) | AgentCore Memory (GA); no ADK memory service targets it | Foundry Memory (preview); no ADK backend | Different extraction; custom `BaseMemoryService`; regenerate and re-test | expensive |
| Retrieval | Vertex AI Search (D3) | Bedrock Knowledge Bases, OpenSearch, S3 Vectors or Aurora pgvector; no Agent Search equivalent identified | Azure AI Search (GA); Foundry IQ partly GA | Gemini embeddings not on Bedrock; re-chunk, re-embed, re-evaluate; ADK retrieval tools become custom tools | expensive |
| Claims data | Firestore (D4) | DynamoDB | Cosmos DB for NoSQL | Data model, queries and transactions change | expensive |
| Photos | Cloud Storage (D4) | S3 | Blob Storage; ADK has `GcsArtifactService` but no Azure artifact service (only matters if artifacts are used) | Copy with egress; signed URLs become presigned URLs or SAS tokens | straightforward |
| Identity | Identity Platform (D6) | Cognito; ALB `authenticate-oidc` passes a signed `x-amzn-oidc-data` JWT the app must verify | Entra; Container Apps built-in auth | Token verification rewritten; user migration not researched | moderate |
| Spend cap | Vertex AI quota (C6) | Bedrock and account quotas (not researched in the reference) | Foundry deployment quotas (not researched in the reference) | A different control with different semantics | unknown; needs a spike |

## Agent framework alternatives

LangGraph 1.2.17 (GA since 1.0.0; MIT, with an Elastic-2.0 Agent Server runtime) against ADK 2.12.0 as pinned by the design. The reference compared 2.13.0. Cells are documented capability, not proof for this workflow.

| Concern | ADK (baseline) | LangGraph |
| --- | --- | --- |
| Agent with function tools (R1 tools) | `LlmAgent` with `get_claim`, `add_note` (`claims/agent.py`) | yes: `create_agent` or a graph; tool bodies carry over |
| Gemini on Vertex AI (D5) | yes, native | yes: `langchain-google-vertexai` |
| Session persistence (D2) | `VertexAiSessionService`, event log with state deltas | yes, as checkpointers (Postgres, SQLite, MongoDB, Redis, Cosmos DB); stores channel snapshots, cannot read ADK events |
| Cross-session memory (D1) | Memory Bank through `PreloadMemoryTool` | not covered by the reference for Memory Bank: `unverified`; a LangGraph move would need its own memory store |
| Output check callback (C5) | after-model callback | middleware or guardrail hooks; order and short-circuit rules differ, so the forbidden-action test is re-run |
| Streaming to the chat UI | yes | yes; AG-UI available (`ag-ui-langgraph`) |
| Evaluation tooling | `adk eval`, eval sets, Runner tests | partial: LangSmith plus `openevals`; ADK evalset runners are re-implemented |
| Managed hosting | Agent Runtime, Cloud Run | Agent Runtime has a LangGraph template; hosted on AWS and Azure; LangSmith Deployment can also host an ADK `Runner` (package very early) |
| Approval or confirmation | not used in this design | not needed here; if added, an interrupt re-runs the node from its start, so earlier side effects must be idempotent |

A switch to LangGraph would rewrite orchestration, callbacks (C5), session storage (D2) and the test harness; tool bodies, prompt text, the React front end and external stores survive. LangGraph does not remove the Google dependencies (Memory Bank, Vertex AI Search, Firestore, Gemini) and solves none of the data costs above, so it answers a framework concern, not the AWS question.

## Boundaries worth having

| Boundary | What it isolates | Reason (a, b, c or d) | Cost now | Existing ADK seam |
| --- | --- | --- | --- | --- |
| Session service choice | Agent Platform sessions (D2) | (c) framework seam | none | `BaseSessionService` |
| Memory service choice | Memory Bank (D1) | (c) framework seam | none | `BaseMemoryService` |
| Model ID and connector | Gemini (D5) | (c) framework seam | none; `MODEL_ID` already read from the environment | model connectors |
| Claims data module | Firestore client in `claims/tools.py` (D4) | none holds today: no second implementation or stated switch | not proposed; exit path recorded in the classification | none |

No wrapper is proposed over Memory Bank, Vertex AI Search or Firestore: a common interface would offer only what the services share and hide the managed behaviour the design relies on.

## Feature differences and migration risks

Risk is rated on switching cost and likelihood; likelihood is unknown because no trigger is recorded.

- **Model (D5):** Gemini is absent on Bedrock and was not found on Azure (`unverified`). Costly; likelihood unknown. A model swap needs a frozen evaluation set, and the plan has none: only scripted-model tests (G02). Without it nobody can show a replacement model is equivalent. This is the main gap in the exit plan.
- **Memory (D1, C2):** regenerated memories differ, and recall isolation and erasure must be re-proven. Costly; unlikely enough to need an exit path, not a seam.
- **Retrieval (D3, C3):** different embeddings and ranking change which clause is cited, which touches R3 directly. Costly.
- **Claims data (D4, C1):** live data with writes; dual-write must be avoided, so backfill plus change capture and a pause for cutover. Costly.
- **Identity (D6):** user migration is not researched; a failed ID mapping would break every ownership check (R1, C1, C2, C4). Unknown size.
- **Cross-cloud Gemini middle path:** hosting on AWS while calling Gemini defers the model cost but adds credential federation (`unverified`), egress and a residency decision for policyholder data.
- **Memory Bank and sessions status:** Google-side GA or preview status of Memory Bank is `unverified` in the references and was not re-read; this affects how much the dependency can be relied on and priced.
- **LiteLLM:** the likely route off Gemini in ADK is `LiteLlm`, which ADK 2.13.0 caps at `litellm>=1.84,<1.106.3` after compromised releases; keep the cap and verify the package. Known accounting gaps exist.
- **Design and code:** D2 and D1 name `VertexAi...` services and the FastAPI service, none of which is in the code yet. This is recorded as design-only, not treated as a mismatch.

## Recommended strategy

Keep the build on GCP and ADK. Hold this exit plan as the answer to the CTO. Add no abstraction layer and no second provider now: nothing records a switch date or trigger (rule b), the framework already provides the seams worth using (rule c), and a wrapper over the managed services would remove the reasons they were chosen. Multicloud would mean two live, tested and operated stacks, plus the egress and identity costs, to insure against an exit nobody has scheduled. The trade-off accepted is that a move later is a project, not a switch, and the largest items are data and re-evaluation.

Suggested triggers to reopen: a stated AWS or Azure move with a date; a contract or residency change; Gemini or a Google managed service withdrawn, repriced or changed materially; a client requirement to run on another cloud. The cheapest useful step before any trigger is a frozen evaluation set (see Open questions and Optional recommendations).

If a move happens, the least disruptive path is staged: first the model (a model change on GCP), then data stores, then hosting, and last the framework if a framework concern still exists.

## Phased outline

1. **Model candidate:** run a candidate model on the frozen evaluation set, per category, behind the same ADK agent on GCP. This needs the set to exist first. Decide whether to keep calling Gemini across clouds.
2. **Parallel run on the target:** stand up the container on the target behind a façade or routing layer while GCP serves users; shadow a sample offline and never let shadow traffic run write tools.
3. **Data backfill:** copy Firestore data to the new store with change capture and checksums, not dual-write; copy photos and verify sample reads through the new code; re-index policy wordings and re-run retrieval tests.
4. **Identity and memory:** map users and IDs, then let memory regenerate and re-run the recall and erasure tests.
5. **Re-evaluation per category:** re-run the evaluation sets and the contract tests (C1 to C6) against the target.
6. **Cutover with rollback:** pause writes, finish the sync, validate with checksums, switch, keep GCP as the rollback, and decommission it only as a deliberate final step.

## Relative effort

| Item | Relative effort (small / medium / large / very large / unknown) | Drivers | Assumptions |
| --- | --- | --- | --- |
| Model swap behind the same ADK agent (D5) | medium | Re-evaluation of prompts, output checks and tool calling | A labelled evaluation set exists; if it must be built first the item grows. Gemini across clouds instead is smaller but adds decisions |
| Container rehost (D6) | small | One image; ingress and token-check rewiring | No Agent Runtime features; ARM64 build only if AgentCore is chosen |
| Sessions (D2) | medium | No known export path; new store and contract tests | Old history may be dropped; retention rules unknown |
| Memory Bank (D1, C2) | large | Regeneration, custom `BaseMemoryService`, isolation and erasure re-tests | Source conversations are retained; otherwise memories are lost |
| Retrieval over policy wordings (D3, C3) | medium | Re-embedding, custom tool, clause-citation re-evaluation | Small corpus of one document per product version |
| Claims data (D4, C1) | large | Data-model redesign, live backfill, changed transactions, owner-check re-proof | Data volume unknown |
| Photos (D4, C4) | small | Bulk copy and signed-URL changes | Volume unknown |
| Identity (D6) | unknown; needs a spike | User migration and ID mapping not researched | Whether users federate from another directory is unknown |
| Spend cap (C6) | unknown; needs a spike | Different quota semantics on each target; not researched | None |
| Framework switch to LangGraph | large | Orchestration, callbacks (C5), sessions, test harness, re-evaluation | Small agent today; each goal G03 to G06 adds ADK-bound code |
| Whole move to AWS or Azure | large | Several drivers: data plus re-evaluation plus identity | Sized by the largest items above, not their sum; no durations are given because no plan measurement exists |

Schedule risks outside the team's control: data-processing and residency approval for policyholder data on a new cloud, the insurer's compliance sign-off and the client's approval of a new model. These are not folded into the sizes above.

## Optional recommendations for the current build

None. The one gap found, a frozen evaluation set for a model swap, needs the evaluation specialist, which is not installed in this project, so it is recorded as an open question for the designer checkpoint instead of a proposed ticket.

## Open questions

- **Trigger and date for a move** (Martin Cole): none recorded. Assumption: none exists, so this is an exit plan only. A named trigger would decide whether the evaluation set and the Postgres session option should be built now.
- **Gemini across clouds** (Martin Cole, platform team): is calling Gemini from AWS or Azure acceptable for policyholder data? It decides whether the model dimension is a model change or a cross-cloud call.
- **Evaluation set** (Tom Reid, designer checkpoint): should the plan gain a goal for a frozen evaluation set and judge? Assumption: not now; flagged as the main gap.
- **Session retention** (Joanne Price): can open sessions be dropped at a move? Decides the sessions row.
- **Identity** (platform team): does Identity Platform federate from an existing directory, and are user IDs stable if users move? Decides the identity size.
- **Memory Bank status** (Google contact): GA or preview at the time of a move, and any export path for memories or sessions.
- **Items not in the design:** observability, IAM layout, secrets and CI. Assumption: standard and not a dominant cost. Each would be assessed when recorded.
- **ADK version:** design pins 2.12.0, references checked 2.13.0. Assumption: the differences do not change a class; re-check against the pinned version.

## Sources

No web access was available in this session, so each row cites the skill's reference file and its recorded read date; nothing was re-read at the source.

| Claim or topic | URL | Read on |
| --- | --- | --- |
| AWS hosting, AgentCore Runtime with ADK | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/using-any-agent-framework.html | 2026-10-26 |
| AgentCore Memory; no ADK memory service | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html | 2026-10-26 |
| Gemini not on Bedrock | https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html | 2026-10-26 |
| Bedrock Knowledge Bases vector stores | https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html | 2026-10-26 |
| ALB authentication (signed JWT) | https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html | 2026-10-26 |
| Azure Foundry hosted agents | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents | 2026-10-26 |
| Azure Foundry Models; partner models | https://learn.microsoft.com/en-us/azure/foundry/concepts/foundry-models-overview | 2026-10-26 |
| Foundry Memory (preview) | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-memory | 2026-10-26 |
| Azure AI Search vectors | https://learn.microsoft.com/en-us/azure/search/vector-search-overview | 2026-10-26 |
| ADK sessions, memory, LiteLLM, models | https://adk.dev/sessions/session/ | 2026-10-26 |
| ADK 2.13.0 LiteLLM pin | https://raw.githubusercontent.com/google/adk-python/v2.13.0/pyproject.toml | 2026-10-26 |
| LangGraph 1.2.17 release and docs | https://github.com/langchain-ai/langgraph | 2026-10-26 |
| Agent Runtime and LangGraph template | https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime | 2026-10-26 |
| Portability principles: classes, effort, phasing | https://doi.org/10.6028/NIST.SP.500-291r2 | 2026-10-26 |
