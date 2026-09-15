# Agent Runtime optimisation

Use this mode when a Python ADK application needs less orchestration work,
controlled conversation growth or a measured managed-runtime capacity change.
For deployment packaging, receipts and cleanup, read
[runtime-lifecycle.md](runtime-lifecycle.md). Read
[state and streams](runtime-state-and-streams.md) only when changing streaming,
memory ingestion, buffered persistence or deferred jobs.

## Locate execution and the actual configuration

Trace one real request before editing. A remote
`agent_engines.get(...).async_stream_query(...)` call runs the deployed agent.
A local `Runner` with `VertexAiSessionService` executes agent code locally while
using remote session storage. Verify these as separate paths. Importing an SDK
or substituting only a database client does not make a model-bearing run offline.

Inspect declared and resolved Python/ADK/Vertex/GenAI versions, selected extras,
profile and environment loading before importing agent definitions. The runtime
baseline is ADK 2.8.0, AI Platform SDK 1.153.1 and GenAI 2.19.0; preserve target
pins and verify differences. With SDK 1.153.1, its `adk` extra constrains ADK
below 2.0. The historical requirements use `agent_engines` with a separate ADK
pin. See [compatibility.md](compatibility.md); a pin check is not a resolver.

Locate the constructed Runner and deployed export. For the 2.8.0 App interface:

```python
from google.adk import Runner

# app and session_service are the target's configured, validated objects.
runner = Runner(app=app, session_service=session_service)
```

Passing only `agent=app.root_agent` drops App settings such as compaction. Verify
which constructor the actual entrypoint uses and that source staging includes
the changed files. A neighbouring example or an imported App alone proves no
integration. Close runners and transports through supported lifecycle methods.

## Reuse the conversation with its authorised owner

Create a session once, retain its returned ID, and use the same ID and trusted
owner on subsequent turns. Omitting the ID on a remote query can create a new
conversation despite an unchanged browser window. Derive identity from the
authenticated application boundary and authorise agent/session access there;
a session ID or caller-supplied `user_id` is not an access grant.

Distinguish the full runtime resource name from its engine ID and validate the
project/region expected by each installed API. Record runtime, session, model and
data locations separately. A global model client does not promise regional
processing merely because the runtime is regional.

Choose retention explicitly. For the managed-session adapter, verify support for
`ttl` or `expire_time`, and supply one retention mechanism rather than both.
Bound session create, get, query and delete inside the full operation budget.
Record create intent before dispatch, retain the returned ID, reconcile uncertain
creation and reserve separate cleanup time. Session and memory deletion are
separate operations; provider failure or permission denial cannot prove absence.

Test continuity by using a unique synthetic fact in turn one, requesting it in
turn two, and inspecting stored events after the client exits. Test wrong-user,
missing-session and unauthenticated paths with expected outcomes. Checks using
different `user_id` values under one credential establish that API boundary,
not isolation between separate IAM principals. Test the latter separately when
it is part of the product's claim.

## Compact history without confusing context selection with deletion

Use bounded previews and durable result references before adding compaction.
Choose the smallest change that addresses measured input growth:

| Need | Candidate | Verification |
| --- | --- | --- |
| Reuse stable instructions | Context caching | Positive provider cached-input usage; separate cache lifecycle |
| Reduce older conversation input | App event compaction | Actual compaction event and next outgoing request; retained facts |
| Retrieve selected facts across sessions | Narrow memory retrieval | Authorised relevant results and measured added round trips |
| Store large results | Durable object/result store | Exact authorised result reference, retrieval and expiry |

In ADK 2.8.0, `EventsCompactionConfig` pairs `token_threshold` with
`event_retention_size`, and `compaction_interval` with `overlap_size`. The token
path uses observed prompt usage when available and estimates effective context
when it is absent. It takes priority when triggered; otherwise sliding-window
processing can apply. These settings are triggers, not hard limits on the next
message or tool result. Retention size counts **events**, not user turns.

Configure compaction on the executing App with a supported summariser. Keep
domain facts, decisions, amounts and unresolved questions needed by later tasks;
tool output and pasted logs retain their original untrusted status. Count
summarisation calls, failed summaries and their cost as part of the conversation.

A meaningful test triggers compaction, observes `event.actions.compaction`,
inspects the summariser input and verifies the next actual model request contains
the intended summary while excluding selected old raw content. Separately test
retained-fact quality using follow-up questions. Compaction appends metadata and
changes request context; it does not prove original storage records were erased.
Verify retention/deletion through the storage lifecycle instead.

The bundled [runtime contract test](../tests/test_runtime_contract.py) uses real
ADK orchestration with deterministic model boundaries to check App propagation,
context selection and retained raw events. It proves neither model summarisation
quality nor hosted managed-session behaviour. Copying a fixed mock summary or
splicing a Python list is weaker evidence and cannot substitute for this boundary.

## Remove decisions the application already knows

Trace logical generations, transport attempts, tools and child handoffs. A
deterministic tool can still require a model request to select it and another
to present its result. One root agent or `mode="single_turn"` does not imply
one provider request. Preserve routing quality and required context when reducing
hops; returning a queue name does not submit a ticket.

Use a deterministic graph when the business process is known, leaving language
agents to interpret genuinely ambiguous input or explain a checked decision.
For ADK 2.8 Workflow functions, ordinary parameters bind from state and
`node_input` receives upstream output. Seed authorised identifiers through
trusted application code. Validate policy in code; a schema or instruction cannot
guarantee the model preserved a refund decision or amount.

If every request needs the same small set of independent records, one bounded
context-loading tool can avoid repeated model selections. Keep model-selected
tool batches, graph branches and concurrency inside a tool distinct. Await real
dependencies, enforce a service-wide capacity policy and distinguish unavailable
optional data from an empty successful result. An isolated per-call semaphore
multiplies across concurrent requests and instances. Use the shared
[application guidance](application.md) for asynchronous clients, bounded offload
and failure policy. Parallel reads do not create a transactional snapshot.

## Tune capacity and model work from observations

Record first event, first nonblank eligible partial text and completed answer
separately. Correlate client/platform/application measurements; application spans
miss delay before process execution. Compare equivalent workloads and retain
errors. A small sample or a faster failed answer cannot establish a tail-latency
improvement.

Inspect effective minimum/maximum instances, `container_concurrency`, CPU, memory
and serving process count. Measure cold/warm state, event-loop lag, throughput,
whole-container memory and downstream throttling. A published nine-worker layout
is not universal; a `2 * cpu + 1` starting recommendation is not an equation for
required CPU. Do not invert it into a CPU ceiling. Validate resource combinations
against current provider limits and the chosen deployment form.

Estimate memory from measured standing **container** usage plus incremental
in-flight work, buffers and headroom. Per-process client caches multiply across
workers. CPU will not accelerate time spent waiting on a remote model; increasing
concurrency can overload memory or downstream services. Warm instances remain
replaceable, and maximum instances do not bound model/tool/storage spending.
Recheck the current minimum-instance billing policy before proposing a cost.

When a model span dominates, evaluate the model, thinking level and output size
for that stage. Verify the actual model ID, lifecycle, supported endpoint and
thinking controls; a mock accepting a model string proves none of those. Keep
thought text out of the UI while preserving required thought signatures and tool
protocol fields. A lower thinking level is not necessarily disabled thinking.
Accept structured output only after both semantic checks and valid completion.

Own retries at one layer. Separate logical model calls from SDK attempts; if an
application wrapper owns retries, configure the SDK accordingly and verify that
boundary. In the recorded GenAI SDK, `HttpRetryOptions(attempts=1)` means one
attempt. Bound retryable failures, jitter/backoff, admission and the total time
including each in-flight call. A timeout checked only between synchronous calls
does not bound a blocked call. Propagate cancellation and do not replay an entire
turn that may already have executed a consequential tool.

Evaluate Standard/Priority PayGo or reserved throughput only after application
work and demand are understood. Deferrable Flex or batch requests need durable
completion handling. Check current eligibility, endpoint and request-header
rules, spillover, pricing and commitment terms before recommending a purchase.
Reserved capacity is a commercial commitment requiring explicit approval; none
of these options is a universal optimisation or was benchmarked by the lab.

Use the official [optimisation guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/optimize-and-scale),
[deployment controls](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent)
and [consumption options](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/deploy/consumption-options)
for current service choices. Keep their examples separate from target measurements.
