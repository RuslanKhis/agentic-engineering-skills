# Agent frameworks and model portability

<!-- verified: 2026-10-26; re-check every 90 days -->

Read when the assessment covers the framework or model dimension, to fill
"Agent framework alternatives" and the framework and model risks. ADK stays
the primary framework; this answers "could another framework implement the
same business workflow, and what would change". Read, never run: "yes" below
means documented, not proven for this toolkit's workflows. Release numbers
are PyPI snapshots on 2026-10-26; LangGraph, Pydantic AI and Microsoft Agent
Framework ship weekly or faster.

## The framework set

| Framework | Package (Python) | Latest release | Licence | Status | Role in an assessment |
| --- | --- | --- | --- | --- | --- |
| Google ADK (baseline) | `google-adk` | 2.13.0, 2026-10-23 | Apache-2.0 | GA since 1.0.0 (2025-05-20); 2.0.0 on 2026-05-19 | The primary build |
| LangGraph | `langgraph` (+ `langchain` for `create_agent`) | 1.2.17, 2026-10-24 | MIT; the Agent Server runtime (`langgraph-api`) is Elastic-2.0 | GA since 1.0.0 (2025-10-17) | Most direct graph-and-checkpoint alternative; managed hosting via LangSmith on GCP or AWS |
| OpenAI Agents SDK | `openai-agents` | 0.24.0, 2026-10-15 | MIT | 0.x: minor versions may break public APIs | Handoff-centred, OpenAI-first; strongest durable-engine coverage |
| Microsoft Agent Framework (MAF) | `agent-framework` | 1.23.0, 2026-10-22 | MIT | Core GA 1.0.0 on 2026-04-02; many connectors beta | Azure counterpart; successor to Semantic Kernel and AutoGen |
| Pydantic AI | `pydantic-ai` | 2.61.0, 2026-10-24 | MIT | GA; V2 since 2026-06-23; V1 gets security fixes for at least six months | Provider-neutral plain Python; most durable-engine integrations |
| AWS Strands Agents (short row) | `strands-agents` | 1.62.0, 2026-10-21 | Apache-2.0 | GA since 1.0.0 (2025-07-15) | Answers "could this run on AWS"; no new feature shape |

**Why these.** LangGraph, the OpenAI Agents SDK, MAF and Pydantic AI cover
the distinct shapes a stakeholder is likely to name; Strands is a short row
because AgentCore otherwise lacks an answer. Left out: CrewAI, LlamaIndex
and AG2 (no feature this toolkit relies on that the five lack); Semantic
Kernel and AutoGen (superseded by MAF, which ships migration guides); the
Claude Agent SDK (a coding-agent harness, not a workflow framework); Mastra
and the Vercel AI SDK (TypeScript only). Add a framework only when the
ticket names it, and research it at its source first.

**MAF status detail.** At 1.23.0, `agent-framework-core`, `-openai`,
`-foundry`, `-orchestrations`, `-declarative`, `-ag-ui` and
`-github-copilot` are Production/Stable on PyPI. Still beta: `-a2a`,
`-gemini`, `-anthropic`, `-redis`, `-azure-cosmos`, `-mem0`, `-devui`,
`-lab`, `-durabletask`, `-azurefunctions`, `-foundry-hosting`; `-hosting` is
alpha. A GA core with a beta Gemini connector matters for a GCP client.

**Bottom line.** All five can implement an LLM agent with function tools,
MCP, structured output and human approval. They differ on what is hard to
move: how a paused run is stored and resumed, how session history is
stored, what streams to the browser, and what the managed runtime is.
LangGraph and MAF have graph engines with checkpointing comparable to ADK
2.x workflows; the OpenAI SDK and Pydantic AI orchestrate in plain code and
rely on external engines for durability.

## Feature comparison

**yes** first-party and documented; **partial** works differently or via an
add-on or beta package; **no**; **unverified**.

| Feature | ADK | LangGraph | OpenAI Agents SDK | MAF | Pydantic AI |
| --- | --- | --- | --- | --- | --- |
| LLM agent with tools | yes (`LlmAgent`) | yes (`create_agent` or a graph) | yes (`Agent`) | yes (`Agent`) | yes (`Agent`) |
| Sequential / parallel / loop | yes: workflow agents, 2.x graph | yes: edges, fan-out, cycles | partial: in code, no primitives | yes: Sequential, Concurrent; loops as cycles | partial: code or `pydantic-graph`; no parallel primitive found |
| Graph workflows | yes (2.x) | yes (core model) | no | yes (`WorkflowBuilder`) | yes (`pydantic-graph`) |
| Sub-agents and handoffs | yes: `sub_agents`, `AgentTool` | yes: subgraphs; handoffs as routed tool calls | yes: handoffs are core; `Agent.as_tool()` | yes: Handoff, Group Chat, Magentic | partial: delegation via tools |
| MCP client | yes (`McpToolset`) | yes (`langchain-mcp-adapters`) | yes | yes | yes |
| OpenAPI tools | yes (`OpenAPIToolset`) | partial: community toolkit, unverified on 1.x | no first-party local tool found | unverified for Python | no first-party tool found |
| In-run state | yes (`session.state`, `{key}` templating) | yes (typed state with reducers) | partial: run context, not persisted | yes (workflow state, `AgentSession`) | partial: `deps` and history |
| Session persistence | yes: in-memory, database, Agent Platform Sessions, Firestore, Redis | yes, as checkpointers: Postgres, SQLite, MongoDB, Redis, Cosmos DB | yes: SQLite, Redis, SQLAlchemy, MongoDB, Dapr, OpenAI Conversations | partial: history providers; `SessionStore` experimental | partial: none built in |
| Checkpointing and crash resume | partial: resumability (1.16.0+) is at-least-once and needs a caller | yes: per super-step; modes `sync`, `async`, `exit` (only `sync` writes before the next step) | partial: `RunState` for approvals, no crash checkpoint | yes: workflow checkpoints with resume | partial: via engines |
| Durable engines | partial: Temporal plugin alpha, DBOS beta, Restate, Dapr | partial: `temporalio-langgraph` beta | yes: `temporalio-openai-agents` Stable, DBOS beta, Restate, Dapr | partial: Durable Task extension, beta | yes: Temporal, DBOS, Prefect, Restate, Airflow |
| Tool confirmation | yes: `require_confirmation` | yes: `HumanInTheLoopMiddleware` | yes: `needs_approval` | yes: `approval_mode="always_require"` | yes: deferred tools |
| Event and token streaming | yes | yes | yes | yes | yes |
| AG-UI | yes (`ag-ui-adk`) | yes (`ag-ui-langgraph`) | partial: community, in progress | yes (`agent-framework-ag-ui`) | yes |
| Structured output | yes (`output_schema`) | yes (`response_format`) | yes (`output_type`) | yes (`response_format`) | yes (`output_type`) |
| Gemini and Vertex | yes, native | yes: `langchain-google-genai`, `langchain-google-vertexai` | partial: compatible endpoint or LiteLLM / Any-LLM adapters ("best-effort, beta") | partial: `agent-framework-gemini` beta | yes: `GoogleModel` on Vertex with ADC |
| Evaluation tooling | yes: `adk eval`, eval sets, user simulation | partial: LangSmith plus `openevals` | partial: test recipes; platform evals unverified | partial: local checks plus Foundry evaluation | yes: Pydantic Evals |
| OTel GenAI spans | yes (`gen_ai.*`) | partial: LangSmith OTel export; native semconv unverified | partial: own tracing, exported to OpenAI by default | yes (`gen_ai.*`) | yes |
| A2A | partial: expose and consume, experimental in Python | yes: Agent Server (v1.0, accepts v0.3) | none found; unverified | partial: client beta; Foundry A2A v1.0 GA | partial: `fasta2a` |
| GCP managed hosting | yes: Agent Runtime; Cloud Run, GKE | yes: Agent Runtime LangGraph template; LangSmith on GCP | partial: custom template or container | partial: same | partial: same |
| AWS managed hosting | yes: AgentCore names ADK | yes: named | yes: named | partial: framework-agnostic, not named | partial: same |
| Azure managed hosting | partial: hosted agents run custom code | yes: hosted agents name LangGraph | partial: custom code; named by one search result, unverified | yes: `agent-framework-foundry-hosting` (beta) on GA hosted agents | partial: custom code |

**Not the same mechanism.** Tell stakeholders:

- **Approval.** An ADK confirmation is a tool-level request answered by a
  function response on the next run. A LangGraph interrupt pauses a node and
  re-runs it from its start on resume, so side effects before the pause must
  be idempotent. OpenAI's `RunState` and Pydantic AI's deferred calls bubble
  up to the caller, keyed by tool call id.
- **Durability.** LangGraph `exit` mode saves nothing if a run crashes part
  way. MAF hosted workflows replay work done after the last checkpoint, so
  external writes still need idempotency keys.
- **Sessions.** ADK stores an event log with state deltas; LangGraph stores
  channel snapshots; OpenAI and Pydantic AI store message lists; MAF stores
  `AgentSession` provider state. None reads the others' records.

**Host without switching.** LangSmith Deployment can host an ADK `Runner`
through `deployments-wrap-sdk` 0.0.2 (import `saf_sdk`), bridging ADK
sessions to Agent Server checkpoints. Changing the host does not require
changing the framework; the package is very early.

**Vendor-authored material.** Pydantic AI publishes a `vs-google-adk`
comparison and a `migrating-google-adk-to-pydantic-ai` skill; AWS and
Microsoft hosting pages describe their own products. Cite them as
vendor-authored, for their own products' facts only, never as a neutral
comparison.

## What a framework switch rewrites

| Area | Why it is rewritten |
| --- | --- |
| Orchestration | `SequentialAgent`, `ParallelAgent`, `LoopAgent`, 2.x graph nodes and `sub_agents` transfer become graph edges, plain code or handoffs. Model routing by `description` needs re-testing even where a handoff exists. |
| Callbacks and plugins | ADK's callback seams and `BasePlugin` become middleware, guardrails with hooks, or capabilities. Order, short-circuit rules and where a guard can block a tool differ: re-prove every guard (budget, PII screen, approval) with its forbidden-action test. |
| Sessions and stored history | ADK `Event` rows (content, actions, `state_delta`, `invocation_id`) are unreadable elsewhere: export to a new store or freeze the old one read-only. `user:`, `app:` and `temp:` state prefixes have no equivalent. |
| Evaluation harness | `.evalset.json`, `adk eval` criteria, user-simulation configs and offline Runner tests are ADK-bound. Keep the cases as data; re-implement the runner and trajectory matcher. |
| Instruction templating | `{key}`, `{key?}` and `{artifact.name}` are ADK syntax; a missing key fails differently elsewhere. |
| Tool declarations | Decorators change and `ToolContext` access to state, artifacts and confirmation is re-plumbed; docstrings and type hints usually survive. |
| Streaming to the frontend | ADK events map differently from other stream shapes. AG-UI on both ends cuts this to an adapter swap (event coverage per adapter `unverified`); a custom JSON API is rewritten. |
| Hosting, identity, telemetry | Agent Runtime, Agent Platform Sessions, Memory Bank, `adk deploy` and exporter settings are ADK- and GCP-specific; span names change, so dashboards and alerts change. |

**What usually survives:** tool bodies and business logic; Pydantic
schemas; prompt text once templating is converted; MCP servers; A2A peers
speaking the same version (v0.3 or v1.0); external stores and idempotency
keys held in the business system.

## Model portability within ADK

Checked against the `google-adk` 2.13.0 source and adk-docs `cc53b6c`:

- **Native connectors.** `gemini-*`, `gemma-4*` and Agent Platform endpoint
  names resolve to `Gemini`; `claude-.*` to `Claude` (Anthropic on Vertex),
  with `AnthropicLlm` for the Anthropic API; `gpt-*` and `o<n>-*` to
  `OpenAILlm` in `google.adk.integrations.openai` (extra
  `google-adk[openai]`; moved from `labs.openai` in 2.10.0), alongside
  `OpenAIResponsesLlm` and `AzureOpenAIResponsesLlm`. OCI Generative AI has
  its own connector. Docs lag the code: cite the source.
- **Claude thinking.** Claude's effort levels do not map onto
  `thinking_level`; use `AnthropicGenerateContentConfig.effort`.
- **`LiteLlm`.** `openai/`, `azure/`, `anthropic/`, `bedrock/`, `vertex_ai/`,
  `ollama_chat/`, `mistral/` and similar strings route to `LiteLlm`. ADK
  requires `litellm>=1.84`, and 2.13.0 caps it below 1.106.3. **The adk-docs
  page carries an advisory about the compromised LiteLLM 1.82.7 and 1.82.8
  releases (2026-03-24): pin and verify the package.** Known accounting gaps:
  reasoning tokens counted twice, a changed `num_retries` meaning.
- **Local models.** Ollama (`ollama_chat/…`, never `ollama/…`) and vLLM
  (`hosted_vllm/…`) run through `LiteLlm` with tool calling enabled on the
  server.
- **Apigee.** `ApigeeLlm` targets Gemini through an Apigee proxy.
- **Failover.** `FallbackModel` (2.9.0) fails over on errors. Configuring it
  belongs to `adk-model-and-output-contracts`; here it is only evidence that
  a second model can sit behind the same agent.

**A model swap is not a system move.** These connectors change the model
behind one `LlmAgent`; orchestration, callbacks, sessions, eval sets,
deployment and telemetry stay on ADK and GCP. The connectors are not equal:
built-in tools (Google Search, code execution) are Gemini-side;
`thinking_level` and output-schema handling differ by connector; usage
accounting differs on `LiteLlm`. When the concern is model lock-in, assess
the model swap first; switch the framework only when the concern is the
runtime, the cloud or the team's skills.

**Every model or framework change re-baselines the evaluations.** Scores
belong to a model and judge pair. Run the frozen evaluation set on the
candidate per category before any claim of equivalence; this is why such an
item is at least medium effort ([principles](principles.md#effort-and-risk-without-invented-numbers)).

## Unverified

- MAF Python OpenAPI tool; OpenAI Agents SDK A2A and first-party
  evaluation; LangGraph native GenAI semconv; LangChain's OpenAPI toolkit on
  1.x; Foundry naming the OpenAI Agents SDK; AG-UI event coverage per adapter.
- Hosting cells cover whether a runtime accepts a framework, not parity:
  Sessions, Memory Bank or the playground for non-ADK code on Agent Runtime
  are not stated.

## Sources

All read 2026-10-26.

| Topic | URL (pin) |
| --- | --- |
| ADK source | https://github.com/google/adk-python (tag v2.13.0, `d68ca85`) |
| ADK docs | https://github.com/google/adk-docs (`cc53b6c`); published at https://adk.dev/agents/models/ |
| LangChain and LangGraph docs | https://github.com/langchain-ai/docs (`4506df5`) |
| LangGraph release | https://github.com/langchain-ai/langgraph (1.2.17, `4c52e12`) |
| OpenAI Agents SDK | https://github.com/openai/openai-agents-python (tag v0.24.0, `17d994b`) |
| Microsoft Agent Framework | https://github.com/microsoft/agent-framework (tag python-1.23.0, `a8e284c`) |
| Pydantic AI, incl. vendor-authored `comparisons/vs-google-adk.md` | https://github.com/pydantic/pydantic-ai (tag v2.61.0, `dd82a00`) |
| Strands harness SDK | https://github.com/strands-agents/harness-sdk (`10b9393`) |
| Temporal SDK and AI integrations | https://github.com/temporalio/sdk-python (`df8caec`) ; https://github.com/temporalio/ai-integrations (`7eea646`) |
| PyPI versions, dates, status | https://pypi.org/pypi/{package}/json |
| Agent Runtime and LangGraph template | https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime |
| AgentCore Runtime; FAQ | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html ; https://aws.amazon.com/bedrock/agentcore/faqs/ |
| Foundry hosted agents | https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents |
| MAF on Foundry hosted agents | https://learn.microsoft.com/en-us/agent-framework/hosting/foundry-hosted-agent |
| AG-UI integrations | https://docs.ag-ui.com/introduction |
