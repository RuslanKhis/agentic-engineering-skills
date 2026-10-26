# Alternative agent frameworks to Google ADK, for portability planning — 26 October 2026

Input for the `adk-portability-planning` framework reference. ADK stays the
primary framework; this note answers "could another framework implement the
same business workflow, and what would change". Read, never run. Source IDs in
brackets resolve in [Sources](#sources).

## Summary

| Framework | Package (Python) | Latest release | Licence | Status | Python | Role in an assessment |
| --- | --- | --- | --- | --- | --- | --- |
| Google ADK (baseline) | `google-adk` | 2.13.0, 2026-10-23 [A1][PyPI] | Apache-2.0 | GA since 1.0.0 (2025-05-20); 2.0.0 on 2026-05-19; roughly weekly to fortnightly minors | >=3.11 | Toolkit baseline; skills record 2.8.0 and read 2.12.0 |
| LangGraph | `langgraph` (+ `langchain` 1.4.7 for `create_agent`) | 1.2.17, 2026-10-24 [L2][PyPI] | MIT; the Agent Server (`langgraph-api`) is Elastic-2.0 | GA since 1.0.0 (2025-10-17); about weekly patches | >=3.10 | The most direct graph-and-checkpoint alternative; managed hosting on GCP or AWS through LangSmith |
| OpenAI Agents SDK | `openai-agents` | 0.24.0, 2026-10-15 [O1][PyPI] | MIT | Still 0.x: minor versions may break public APIs [O1 `release.md`]; about fortnightly | >=3.10 | Handoff-centred, OpenAI-first; strongest third-party durable-engine coverage |
| Microsoft Agent Framework (MAF) | `agent-framework` (`agent-framework-core`) | 1.23.0, 2026-10-22 [M1][PyPI] | MIT | Core GA: 1.0.0 on 2026-04-02 after rc1–rc6 (Feb–Mar 2026). Many connectors are still beta (see note) | 3.10–3.15 (3.10 deprecated) | Azure counterpart; successor to Semantic Kernel and AutoGen [M1 README] |
| Pydantic AI | `pydantic-ai` / `pydantic-ai-slim` | 2.61.0, 2026-10-24 [P1][PyPI] | MIT | GA; V2.0 on 2026-06-23; V1 (1.107.9, 2026-10-21) gets security fixes for at least 6 months [P1 `version-policy.md`]; near-daily releases | >=3.11 | Provider-neutral, plain Python; the most durable-engine integrations; ships an ADK migration skill |
| AWS Strands Agents (short row) | `strands-agents` | 1.62.0, 2026-10-21 [S1][PyPI] | Apache-2.0 | GA since 1.0.0 (2025-07-15); semver policy [S1] | >=3.10 | AWS counterpart. Covered by the [Strands note](strands-comparison-2026-10-25.md); included only to answer "could this run on AWS" |

**Note on MAF status.** At 1.23.0 these are Production/Stable on PyPI: `agent-framework-core`, `-openai` (1.17.0),
`-foundry` (1.15.0), `-orchestrations` (1.4.0), `-declarative` (1.4.0), `-ag-ui` (1.7.0) and `-github-copilot` (2.1.0).
These are still beta (`1.0.0b2610xx`): `-a2a`, `-gemini`, `-anthropic`, `-redis`, `-azure-cosmos`, `-mem0`, `-devui`, `-lab`, `-durabletask`,
`-azurefunctions` and `-foundry-hosting`. `-hosting` is alpha. A GA core with a beta Gemini connector matters for a GCP client.

**Selection.** The four requested frameworks stay. Strands is kept as a short row because the AgentCore hosting answer is otherwise
missing. It adds no new feature shape. Dropped, one line each:
- CrewAI, LlamaIndex and AG2: no feature this toolkit relies on that the five lack, and Agent Runtime already lists them as templates.
- Semantic Kernel and AutoGen: superseded by MAF, which ships migration guides from both [M1 README].
- Claude Agent SDK: a coding-agent harness, not a workflow framework.
- Mastra and the Vercel AI SDK: TypeScript only, outside this Python toolkit.

**Bottom line.** All five can implement an LLM agent with function tools, MCP, structured output and human approval. They differ on
the things that are hard to move:
- how a paused run is stored and resumed;
- how session history is stored;
- what streams to the browser;
- what the managed runtime is.

LangGraph and MAF have graph engines with checkpointing comparable to ADK 2.x workflows. The OpenAI SDK and Pydantic AI orchestrate in
plain code and rely on external engines for durability.

## Feature comparison

Legend: **yes** (first-party, documented), **partial** (works differently, or through an add-on or beta package), **no**, **unverified**.
ADK is the 2.13.0 source with the adk-docs `cc53b6c` pages [A1][A2]; ADK facts the toolkit already holds are not re-cited.

| Feature | ADK | LangGraph | OpenAI Agents SDK | MAF | Pydantic AI |
| --- | --- | --- | --- | --- | --- |
| LLM agent with tools | yes (`LlmAgent`) | yes (`create_agent` in `langchain` 1.x, or a hand-built graph) [L1] | yes (`Agent`) | yes (`Agent`) | yes (`Agent`) |
| Sequential / parallel / loop | yes: workflow agents and 2.x graph nodes | yes: graph edges, fan-out, cycles | partial: in code (`asyncio.gather`, loops); no workflow primitives [O1 `multi_agent.md`] | yes: Sequential and Concurrent orchestrations; loops as cycles (`control-flow/simple_loop.py`) [M1] | partial: plain code or `pydantic-graph`; no parallel primitive found in `graph.md` [P1] |
| Graph workflows | yes (2.x graph API) | yes (core model) | no | yes (`WorkflowBuilder`, executors and edges) | yes (`pydantic-graph`, separate package) |
| Sub-agents and handoffs | yes: `sub_agents` transfer, `AgentTool` | yes: subgraphs; handoffs as state-routed tool calls [L1 `multi-agent/index.mdx`] | yes: handoffs are the core primitive; `Agent.as_tool()` | yes: Handoff, Group Chat and Magentic orchestrations [M1] | partial: delegation through tools and programmatic hand-off; no transfer primitive [P1 `multi-agent-applications.md`] |
| Function tools | yes | yes | yes (`@function_tool`) | yes (`@tool`) | yes |
| MCP client | yes (`McpToolset`) | yes (`langchain-mcp-adapters` 0.3.2) | yes (stdio, SSE, Streamable HTTP; also hosted MCP) [O1 `mcp.md`] | yes (`MCPStdioTool` and others in core `_mcp.py`) [M1] | yes [P1 `mcp/`] |
| OpenAPI tools | yes (`OpenAPIToolset`) | partial: LangChain community toolkit, not checked on 1.x | no first-party local tool found; hosted tools only | unverified for Python: the core README claims it, but no OpenAPI module at python-1.23.0. Foundry Toolbox has it server-side [W4] | no first-party tool found |
| In-run state | yes (`session.state`, `{key}` templating) | yes (typed graph state with reducers) | partial: a run context object, not persisted state | yes (workflow shared state; `AgentSession`) | partial: `deps` and message history; graph state in `pydantic-graph` |
| Session persistence | yes: in-memory, database, Agent Platform Sessions, Firestore, Redis and others [A2] | yes, as checkpointers: Postgres, SQLite, MongoDB, Redis, Cosmos DB; Firestore only as a community package [L1] | yes: SQLite, Redis, SQLAlchemy, MongoDB, Dapr, OpenAI Conversations, encrypted wrapper [O1 `sessions/index.md`] | partial: history providers (file, Redis beta, Cosmos beta, custom); `SessionStore` is experimental [M1] | partial: none built in; "store its `Conversation`" in your own column; `StepPersistence` in the Harness [P1 `persistence.md`] |
| Checkpointing and crash resume | partial: resumability (Python 1.16.0+) is at-least-once and needs a caller [A2 `resume.md`] | yes: a checkpoint per super-step; durability modes `sync`, `async` and `exit` (only `sync` guarantees a write before the next step) [L1 `checkpointers.mdx`] | partial: `RunState` serialises a paused run for approvals; no crash checkpoint [O1] | yes: workflow checkpoints (file, Cosmos) with resume [M1 samples] | partial: core has no checkpointer; durability comes from engines |
| Durable engines | partial: Temporal `temporalio-google-adk` 0.0.1 alpha; DBOS 0.1.0 beta; Restate; Dapr, with conditions ([durable](durable-execution-comparison-2026-10-23.md), [Restate/Dapr](restate-dapr-comparison-2026-10-25.md)) | partial: `temporalio-langgraph` 0.1.0 beta (moved out of `temporalio` contrib) [T1] | yes: `temporalio-openai-agents` 1.1.0 (Stable), DBOS 0.3.0 beta, Restate, Dapr [O1 `running_agents.md`] | partial: Durable Task and Azure Functions moved to `microsoft/agent-framework-durable-extension` (ADR-0032, 2026-07-21), beta [M1] | yes: Temporal, DBOS, Prefect, Restate, Airflow; Lambda and others in the Harness [P1] |
| Interrupt and resume | yes: tool confirmation, long-running tools, workflow-node confirmation (2.12) | yes: `interrupt()` with `Command(resume=…)`. The node re-runs from its start on resume ([interrupts note](langgraph-interrupts-comparison-2026-10-23.md)) | yes: interruptions on the result; resume from `RunState` [O1] | yes: workflow request/response; `user_input_requests` on the agent [M1] | yes: deferred tools return `DeferredToolRequests`, resumed with results [P1] |
| Tool confirmation | yes: `require_confirmation` per tool | yes: `HumanInTheLoopMiddleware(interrupt_on=…)` with approve, edit and reject, built on graph interrupts [L1] | yes: `needs_approval=True` or a callable; also on MCP servers [O1] | yes: `@tool(approval_mode="always_require")` [M1 samples] | yes: approval-required deferred tools |
| Event and token streaming | yes: event stream, SSE, live bidi | yes: stream modes including token `messages` | yes: raw response events plus `RunItemStreamEvent` [O1 `streaming.md`] | yes | yes |
| AG-UI | yes: `ag-ui-adk` 0.11.0; AG-UI lists it first-party [W6] | yes: `ag-ui-langgraph` 0.0.47; listed as a partnership [W6] | partial: listed "In Progress, Community" [W6] | yes: `agent-framework-ag-ui` 1.7.0 (Stable); first-party [W6] | yes: [P1 `ui/ag-ui.md`]; first-party [W6] |
| Structured output | yes (`output_schema`) | yes (`response_format`: tool or provider strategy) [L1] | yes (`output_type`) [O1] | yes (`response_format`) | yes (`output_type`) |
| Gemini and Vertex | yes, native | yes: `langchain-google-genai` 4.4.2 and `langchain-google-vertexai` 3.2.5 | partial: OpenAI-compatible endpoint, or the LiteLLM and Any-LLM adapters, both "best-effort, beta" [O1 `models/index.md`] | partial: `agent-framework-gemini` beta; Developer API or Agent Platform [M1] | yes: `GoogleModel` on Vertex with ADC, and Claude on Vertex [P1 `models/google-cloud.md`] |
| Other model providers | partial: native Claude and OpenAI; the rest through LiteLLM (see below) | yes: many native packages; `langchain-litellm` is beta | partial: native OpenAI; others through compatible endpoints or adapters | yes: OpenAI, Azure, Foundry (GA); Anthropic, Bedrock, Ollama, Mistral (beta) | yes: about 25 native providers |
| Evaluation tooling | yes: `adk eval`, eval sets, user simulation, environment simulation | partial: LangSmith (SaaS or self-hosted) plus OSS `openevals` 0.2.2 | partial: the SDK offers test recipes (scripted model, injected failures); evals live on the OpenAI platform, unverified | partial: local `evaluate_agent` checks plus Foundry evaluation [M1 samples] | yes: Pydantic Evals 2.61.0 |
| OpenTelemetry GenAI spans | yes: `gen_ai.*` spans and metrics [A2] | partial: LangSmith tracing; OTel export via `LANGSMITH_OTEL_ENABLED`; native `gen_ai` semconv not confirmed [L1] | partial: own tracing, exported to OpenAI by default; third parties through processors [O1 `tracing.md`] | yes: `gen_ai.*` attributes in core `observability.py` [M1] | yes: follows GenAI semconv; version configurable [P1 `logfire.md`] |
| A2A | partial: expose and consume, marked experimental in Python [A2] | yes: `/a2a/{assistant_id}` on Agent Server (A2A v1.0, still accepts v0.3) [L1 `server-a2a.mdx`] | no first-party support found; unverified | partial: `A2AAgent` client (beta), `hosting-a2a`; Foundry A2A v1.0 endpoint is GA [M1][W4] | partial: through the separate `fasta2a` package [P1 `interfaces.md`] |
| GCP managed hosting | yes: Agent Runtime "full integration"; also Cloud Run and GKE [W1] | yes: Agent Runtime `LanggraphAgent` template with Cloud SQL or AlloyDB checkpointer [W1]; LangSmith Cloud runs on GCP [L1 `cloud.mdx`] | partial: Agent Runtime custom template or container [W1] | partial: same as OpenAI SDK | partial: same as OpenAI SDK |
| AWS managed hosting | yes: AgentCore Runtime names Google ADK [W3] | yes: named [W2][W3]; LangSmith also runs on AWS | yes: named [W3] | partial: framework-agnostic, not named [W2] | partial: same as MAF |
| Azure managed hosting | partial: Foundry hosted agents run custom code [W4] | yes: hosted agents name LangGraph [W4] | partial: custom code; named by one search result, unverified | yes: `agent-framework-foundry-hosting` (beta) on GA hosted agents [W5] | partial: custom code |

**Not the same mechanism** — what to tell a stakeholder:

- **Approval.** An ADK confirmation is a tool-level request answered by a function response on the next run. A LangGraph interrupt
  pauses a node and re-runs it from its start on resume, so side effects before the pause must be idempotent. OpenAI's `RunState`
  and Pydantic AI's deferred calls both bubble up to the caller, keyed by the tool call id.
- **Durability.** LangGraph `exit` mode saves nothing if a run crashes part-way, so ask which mode is configured. MAF hosted
  workflows resume from the last checkpoint and replay any work done after it, so external writes still need idempotency keys [W5].
- **Sessions.** ADK stores an event log with state deltas. LangGraph stores channel snapshots per super-step. OpenAI and Pydantic
  AI store message lists. MAF stores `AgentSession` provider state. None of these reads the others' records.

**Hosting note.** LangSmith Deployment can host an ADK `Runner` through `deployments-wrap-sdk` 0.0.2 (2026-08-07, import
`saf_sdk`). It bridges ADK sessions to Agent Server checkpoints [L1 `deploy-google-adk.mdx`]. Changing the host does not require
changing the framework. The package is very early.

## What a framework switch actually rewrites

| Area | Why it is rewritten |
| --- | --- |
| Orchestration code | `SequentialAgent`, `ParallelAgent`, `LoopAgent`, 2.x graph nodes and `sub_agents` transfer become graph edges (LangGraph, MAF), plain code (OpenAI, Pydantic AI) or handoffs. Routing by the model reading `description` needs re-testing even where a handoff exists. |
| Callbacks and plugins | ADK's six callback seams and `BasePlugin` become LangChain middleware, OpenAI guardrails with `RunHooks`, MAF middleware, Pydantic AI capabilities and hooks, or Strands hooks. Order, short-circuit rules and the place where a guard can block a tool all differ. Re-prove every guard (budget, PII screen, approval) with its forbidden-action test. |
| Session schema and stored history | ADK `Event` rows (content, actions, `state_delta`, `invocation_id`) cannot be read by another framework. Migrate to a new store with an export job, or freeze the old store read-only. State-key prefixes (`user:`, `app:`, `temp:`) have no equivalent elsewhere. |
| Evaluation sets and harness | `.evalset.json` files, `adk eval` criteria, user-simulation configs and the toolkit's offline Runner tests are tied to ADK. Keep the cases (inputs, expected tool calls, rubric) as data. Re-implement the runner and the trajectory matcher. |
| Instruction templating | `{key}`, `{key?}` and `{artifact.name}` injection is ADK syntax. Elsewhere it becomes f-strings, dynamic instruction callables (OpenAI, Pydantic AI), `ChatPromptTemplate` or middleware. A missing key fails differently in each. |
| Tool declarations | Decorators and wrappers change (`FunctionTool`, `@function_tool`, `@tool`). `ToolContext` access to state, artifacts and confirmation must be re-plumbed. Docstrings and type hints usually survive as the model-facing schema. |
| Streaming event mapping in the frontend | ADK events (`partial`, `function_call`, `actions.state_delta`) map onto the UI differently from LangGraph stream modes or OpenAI `RunItemStreamEvent`s. AG-UI on both ends cuts this to an adapter swap, though event coverage per adapter is unverified. A custom JSON API is rewritten. |
| Hosting, identity and telemetry wiring | Agent Runtime deployment, Agent Platform Sessions, Memory Bank, `adk deploy` and Cloud Trace exporter settings are ADK- and GCP-specific. Span names and attributes change, so dashboards and alerts change too. |

**What usually survives:**
- tool function bodies and the business logic behind them;
- Pydantic input and output schemas;
- prompts as text, once the templating syntax is converted;
- MCP servers (every candidate has a client);
- A2A peers, if the new framework speaks the same A2A version (v0.3 or v1.0);
- external stores (BigQuery, RAG indexes, Secret Manager) and idempotency keys held in the business system.

## Model portability within ADK

Verified against adk-docs `cc53b6c` [A2] and the 2.13.0 source [A1]:

- **Registry strings (native).** ADK resolves these strings to native classes:
  - `gemini-*`, `gemma-4*` and Agent Platform endpoint resource names go to `Gemini`;
  - `claude-.*` goes to `Claude`, Anthropic on Vertex through `AsyncAnthropicVertex`; `AnthropicLlm` calls the Anthropic API directly;
  - `gpt-*` and `o<n>-*` go to `OpenAILlm` in `google.adk.integrations.openai` (extra `google-adk[openai]`; moved from `labs.openai`,
    changelog 2.10.0 section). `OpenAIResponsesLlm` and `AzureOpenAIResponsesLlm` are also there.
  - OCI Generative AI has its own connector (`google-adk[oci]`).
- **Docs lag the code.** adk-docs `openai.md` says Python reaches OpenAI only through LiteLLM. The Claude page still quotes the narrower
  `claude-3-*` / `claude-*-4*` patterns and a 2024 model id. Cite the source, not the page.
- **Claude thinking.** Claude's five effort levels do not map onto `thinking_level`. Use `AnthropicGenerateContentConfig.effort` [A1].
- **`LiteLlm` connector.** Strings such as `openai/`, `azure/`, `anthropic/`, `bedrock/`, `vertex_ai/`, `ollama_chat/` and `mistral/`
  are registered to `LiteLlm`. ADK requires `litellm>=1.84`. The adk-docs page carries an advisory about the compromised LiteLLM
  1.82.7 and 1.82.8 releases (2026-03-24). 2.13.0 caps litellm below 1.106.3 [A1 CHANGELOG]. Known accounting gaps are in the
  [LiteLLM note](litellm-comparison-2026-10-25.md).
- **Apigee.** `ApigeeLlm` (Python v1.18.0) targets Gemini `generateContent` through an Apigee proxy. Its `CompletionsHTTPClient` covers
  OpenAI-style routes.
- **Ollama and vLLM.** Both run through `LiteLlm`: `ollama_chat/…`, never `ollama/…`, and `hosted_vllm/…`. Tool calling must be
  enabled on the server. LiteRT-LM serves Gemma locally through a `Gemini` client.
- **Failover.** `FallbackModel` (2.9.0) fails over on errors. adk-docs documents router-based routing for TypeScript only, as
  experimental.

**Interchangeable model calls are not a portable agent.** These connectors change the model behind one `LlmAgent`. The orchestration,
callbacks, sessions, eval sets, deployment and telemetry all stay on ADK. The connectors are not equal either:
- built-in tools (Google Search, code execution) are Gemini-side;
- `thinking_level` and output-schema handling differ by connector;
- usage accounting differs on `LiteLlm`.

A model swap therefore needs its own eval run, but not a framework migration. Swap the model first when the client's concern is model
lock-in. Switch the framework only when the concern is the runtime, the cloud or the team's skills.

## Status surprises found on 26 October 2026

- MAF reached 1.0 GA on 2026-04-02, but its Gemini, A2A, Anthropic, Redis, Cosmos and Foundry-hosting packages are still beta.
  Durable Task hosting moved to a separate repository.
- Pydantic AI is on V2 (since 2026-06-23) and still patches V1. It publishes a `vs-google-adk` comparison and a
  `migrating-google-adk-to-pydantic-ai` skill. Treat both as vendor-authored.
- Strands now calls itself the "Strands Harness SDK". `strands-agents/sdk-python` redirects to `strands-agents/harness-sdk`, and
  `strands-agents/docs` is archived (docs moved to `site/`). The PyPI name is unchanged.
- "LangGraph Platform" is now LangSmith Deployment, with Agent Server as its runtime. The runtime package is Elastic-2.0, not MIT.
- Temporal's LangGraph plugin left `temporalio` contrib for `temporalio-langgraph`. `temporalio-openai-agents` is Stable while the ADK
  plugin is alpha.
- Foundry hosted agents are GA; their old backend was supported only until 2026-08-20 [W4 search summary].
- ADK 2.13.0 (2026-10-23) is newer than the toolkit's 2.12.0 reads.

## Sources

All read 2026-10-26.

- [A1] [google/adk-python](https://github.com/google/adk-python) tag `v2.13.0` (`d68ca85`). Files: `src/google/adk/models/__init__.py`,
  `anthropic_llm.py`, `integrations/openai/README.md`, `integrations/oci/__init__.py`, `CHANGELOG.md`.
- [A2] [google/adk-docs](https://github.com/google/adk-docs) `main` (`cc53b6c`, 2026-10-23). Files: `docs/agents/models/*.md`,
  `docs/a2a/quickstart-exposing.md`, `docs/runtime/resume.md`, `docs/observability/metrics.md`, `docs/integrations/ag-ui.md`.
  Published at https://google.github.io/adk-docs/agents/models/.
- [L1] [langchain-ai/docs](https://github.com/langchain-ai/docs) `main` (`4506df5`, 2026-10-23). Files:
  - `src/oss/langgraph/{checkpointers,interrupts,fault-tolerance}.mdx`;
  - `src/oss/langchain/{human-in-the-loop,structured-output}.mdx`, `multi-agent/index.mdx`;
  - `src/oss/python/integrations/checkpointers/index.mdx`;
  - `src/langsmith/{deployment,cloud,deploy-to-cloud-overview,self-hosted,server-a2a,deploy-google-adk,trace-with-opentelemetry}.mdx`.
- [L2] [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) release `1.2.17` (`4c52e12`). Release metadata only.
- [O1] [openai/openai-agents-python](https://github.com/openai/openai-agents-python) tag `v0.24.0` (`17d994b`). Files:
  `docs/{models/index,sessions/index,running_agents,human_in_the_loop,multi_agent,tracing,streaming,agents,tools,mcp,testing,release}.md`.
- [M1] [microsoft/agent-framework](https://github.com/microsoft/agent-framework) tag `python-1.23.0` (`a8e284c`). Files:
  - `README.md`, `python/README.md`;
  - `python/packages/{a2a,ag-ui,gemini,hosting,foundry_hosting,core}/README.md`;
  - `docs/decisions/0032-durable-azure-functions-extraction.md`;
  - the `python/samples` tree, `core/_mcp.py`, `core/observability.py`.
- [P1] [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) tag `v2.61.0` (`dd82a00`). Files:
  `docs/{version-policy,persistence,framework-migration,interfaces,graph,multi-agent-applications,logfire}.md`,
  `comparisons/vs-google-adk.md`, `durable_execution/overview.md`, `models/google-cloud.md`, `ui/`.
- [S1] [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk) `main` (`10b9393`). Files:
  `site/src/content/docs/user-guide/sdk/{versioning-and-support,model-providers/google,storage/index}.mdx`,
  `integrations/integrations/ag-ui.mdx`. Also the archived [strands-agents/docs](https://github.com/strands-agents/docs) (`658b6f0`).
- [T1] [temporalio/sdk-python](https://github.com/temporalio/sdk-python) `main` (`df8caec`): `temporalio/contrib` listing and
  `contrib/langgraph/README.md`. [temporalio/ai-integrations](https://github.com/temporalio/ai-integrations) (`7eea646`): `python/` listing.
- [PyPI] https://pypi.org/pypi/{package}/json for every version, date, status classifier and `requires_python` quoted above.
- [W1] https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime (updated 2026-10-23) and
  `…/build/runtime/create-a-langgraph-agent` (updated 2026-10-22).
- [W2] https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- [W3] https://aws.amazon.com/bedrock/agentcore/faqs/
- [W4] https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents (ms.date 2026-10-19).
- [W5] https://learn.microsoft.com/en-us/agent-framework/hosting/foundry-hosted-agent (ms.date 2026-10-08).
- [W6] https://docs.ag-ui.com/introduction (integration table).

## Source register rows

| id | repo | pinned | read | licence | note |
| --- | --- | --- | --- | --- | --- |
| adk-python (update) | google/adk-python | d68ca85 (v2.13.0) | 2026-10-26 | Apache-2.0 | models registry, OpenAI and OCI integrations, CHANGELOG |
| adk-docs (update) | google/adk-docs | cc53b6c | 2026-10-26 | Apache-2.0 | model pages, A2A, resume, metrics |
| langchain-docs (update) | langchain-ai/docs | 4506df5 | 2026-10-26 | MIT | LangGraph persistence and interrupts; LangSmith Deployment, A2A, ADK wrapper |
| langgraph (new) | langchain-ai/langgraph | 4c52e12 (1.2.17) | 2026-10-26 | MIT | release metadata only |
| openai-agents-python (update) | openai/openai-agents-python | 17d994b (v0.24.0) | 2026-10-26 | MIT | models, sessions, durable integrations, HITL, tracing |
| ms-agent-framework (update) | microsoft/agent-framework | a8e284c (python-1.23.0) | 2026-10-26 | MIT | package status, hosting, ADR-0032 |
| pydantic-ai (update) | pydantic/pydantic-ai | dd82a00 (v2.61.0) | 2026-10-26 | MIT | version policy, persistence, vs-google-adk, migration |
| strands-harness-sdk (update) | strands-agents/harness-sdk | 10b9393 | 2026-10-26 | Apache-2.0 | docs site, versioning policy, providers |
| strands-docs (new) | strands-agents/docs | 658b6f0 (archived) | 2026-10-26 | unverified | archived; not used for facts |
| temporal-sdk-python (new) | temporalio/sdk-python | df8caec | 2026-10-26 | MIT | contrib listing; LangGraph plugin moved |
| temporal-ai-integrations (update) | temporalio/ai-integrations | 7eea646 | 2026-10-26 | MIT | `python/` listing only |

All rows: `note` → `docs/research/portability-agent-frameworks-2026-10-26.md`; `used_by` → `adk-portability-planning`.

## Limits of this note

- **Read, not run.** No candidate framework was installed or run. "yes" means documented, not proven for this toolkit's workflows.
- **Unverified cells:**
  - MAF Python OpenAPI tool;
  - OpenAI Agents SDK A2A and first-party evaluation;
  - LangGraph native GenAI semconv;
  - LangChain's OpenAPI toolkit on 1.x;
  - Foundry naming the OpenAI SDK;
  - AG-UI event coverage per adapter;
  - the licence of the archived Strands docs repo.
- **Search-only facts.** Two Foundry facts came from search summaries of Microsoft Learn: the 2026-08-20 backend deadline and the
  `azure-ai-projects` 2.3.0 GA marker. Of those, only GA status was confirmed on a page opened [W5].
- **Snapshots age fast.** Release numbers are PyPI snapshots on 2026-10-26. LangGraph, Pydantic AI and MAF ship weekly or faster.
- **Vendor material is not a neutral comparison.** Pydantic AI's ADK comparison and AWS and Microsoft hosting pages were used for
  their own products' facts only.
- **Hosting cells cover listing, not parity.** They say whether a runtime accepts a framework. They do not cover Sessions, Memory
  Bank or the playground for non-ADK code on Agent Runtime, which [W1] does not state.
