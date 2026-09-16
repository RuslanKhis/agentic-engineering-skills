# Select and adapt orchestration

Use the installed SDK contract and existing tests. ADK 2.8.0 contains both
deprecated compatibility agents and `Workflow`; replacing one with another is a
behavioural migration, not a spelling correction. Newer APIs require their own
version check and acceptance evidence. See [compatibility.md](compatibility.md).

| Pattern | Choose it when | Acceptance contract |
| --- | --- | --- |
| Ordinary code | Rules are known and testable | Deterministic input/output and failures; no model merely for coordination. |
| Sequential | A later step requires an earlier result | The reviewer receives the actual writer output; a failed reviewer preserves only completed work and propagates failure. |
| Parallel | Work is independent and useful concurrently | Branches overlap at an observable barrier and preserve separate outputs. Identify an explicit fan-in consumer if one is required. |
| Bounded loop | Refinement has a review decision | Both early approval and exhaustion work; result includes the final artefact and, when required, termination reason. |
| Graph | Edges and typed handoffs make dependencies clear | Assert the actual Python/node output reaches the next node, not a reconstructed plausible answer. |
| Dynamic | Number/order of steps depends on runtime input | Thin coordinating parent calls children through `ctx.run_node`; tests cover input contracts, empty work and repeated IDs. |

## State and result ownership

In a compatibility sequence, `output_key="draft"` stores completed output in
session state; `{draft}` in a downstream instruction consumes it. Use distinct
keys for concurrent writers. A post-join merge can intentionally reconcile
results, but two parallel agents silently overwriting the same key is not a merge.
The inspection helper finds only simple, same-file, directly assigned siblings;
factories, nested branches and runtime keys require manual tracing.

`Workflow` can pass typed node outputs without using session-global keys for
intermediate values. In ADK 2.8.0, it cannot be placed directly in an
`LlmAgent.sub_agents` list. Verify composition rather than guessing from another
release. A graph fan-in using `JoinNode` plus a summariser adds a dependency and
often a model call; it is not implicit in `ParallelAgent`.

Define the final result before implementing the UI. “Last final text” can discard
one parallel branch or return a critic's acknowledgement instead of the draft.
Structured node output may not be chat text at all. Preserve consumer contracts
when adapting an existing project, including whether scalar JSON is decoded or
retained as a literal string. A cleaner parser can still be a breaking change.

## Bounds and side effects

For `LoopAgent`, set a finite positive `max_iterations`; treat dynamic/configured
limits as unproven until validated. The critic may call a tool that sets
`tool_context.actions.escalate = True` to stop the enclosing loop. Model approval
is probabilistic; escalation and the iteration bound are deterministic mechanisms.

Count actual sends, including tool continuations and SDK retries. A controlled
writer/critic/exit-tool path needed three model requests; the five-pass exhaustion
path needed eleven. These explain cost multiplication, not reusable universal
caps. For a requested budget, reserve an attempt before sending, persist counts
and the original deadline if restart/resume is supported, and fail closed on
uncertain in-flight operations. Choose one retry-owning layer; bounded transient
retries must not repeat a non-idempotent action blindly.
Use [model-call-controls.md](model-call-controls.md) when implementing a strict
attempt/deadline boundary; it explains transport enforcement and safe restart.

Keep synchronously blocking I/O out of concurrent async branches or use an
explicit appropriate execution strategy. Measure overlap rather than comparing
two unreliable wall-clock thresholds. More agents can add latency and duplicate
context; add each one for a concrete responsibility or authority boundary.

## Truthfulness of the task boundary

If no live lookup tool exists, outputs must be labelled illustrative and request
missing inputs rather than invent dates, prices, availability or completed
research. The prior travel example needed a live prompt repair for precisely
this failure. Assert the outbound prompt offline; assess actual compliance in
separately approved live samples. Neither turns a prompt into a security control.

A deterministic lookup inside two model steps makes only that node offline.
Fixed clock values are simulated even if a legacy prompt says “right now”. Prefer
plain code when it meets the real task, but account for its own I/O, failure and
compute costs. Never copy a simulated service into a production feature as though
it were authoritative.

## Turn the selection into an implementation

Write a small contract table before wiring nodes: input type, output type/key,
authoritative source, side effects, failure result and next consumer. Separate
model judgement from known calculations and policy checks. Agent separation only
creates a code boundary; shared credentials, tools and state can still give every
agent the same authority. Record which checks need enforcement outside prompts.

For the checked compatibility API, import `LlmAgent`, `SequentialAgent`,
`ParallelAgent` and `LoopAgent` from `google.adk.agents`, configure named children,
and export the chosen root through the project's existing entry point. Preserve
the existing API even though compatibility agents emit deprecation warnings;
migration requires its own behavioural comparison. For a sequential repair,
trace both the writer's `output_key` and the consumer's `{key}` placeholder. For
parallel work, trace every branch and its post-join consumer in both completion
orders. A correct scheduler cannot fix a missing result key or implicit merge.

For ADK 2.8.0 graph code, `from google.adk import Agent, Workflow` supplies nodes
and orchestration. A tuple such as `("START", producer, transform, consumer)` in
`Workflow(edges=[...])` expresses order. Declare the producer's `output_schema`,
the Python function's input/return annotations, and the consumer's `input_schema`
to agree. A Pydantic input named `Record` is addressed as `{Record.field}` in the
consumer instruction, while `{draft}` above is a session-state placeholder.
Inspect the rendered request in an offline boundary test: an import or type
annotation alone does not prove the actual value crossed the edge. Serialise
Pydantic output using the model's JSON-capable methods at the HTTP boundary,
and preserve structured lists/dictionaries rather than stringifying them for UI
convenience. See [runtime.md](runtime.md) for output-event selection.
When substituting a schema-constrained model, preserve its wire contract too:
the checked `output_schema=str` model response is JSON string text (for example
`json.dumps("synthetic value")`), not an arbitrary unquoted chat response.

For dynamic work, use `@node` from `google.adk.workflow`, keep the coordinating
parent thin, and `await ctx.run_node(child, value)` instead of bypassing child
orchestration with a direct Python call. Decide whether order and duplicates are
meaningful before introducing parallelism or deduplication. One historical
contract preserved an empty list, converted each list element with `str(...)`,
and retained non-list JSON as the original input text (including quotes around a
JSON string). That is a compatibility lesson, not a parser to impose on a new
product. Test the target's chosen scalar/list, empty and duplicate-ID behaviour
explicitly. A sequential loop over runtime items is dynamic, but not concurrent.
In the checked SDK, wrapping `ctx.run_node(...)` in an unsupervised
`asyncio.create_task(...)` bypasses supported child error/cancellation handling.
Use its supervised invocation path; design concurrency through the version's
supported workflow mechanism. Data IDs need not be unique execution IDs. Verify
the SDK's child-ID constraints before supplying custom IDs, particularly when
duplicate inputs or replay are possible.

## Prepare a production handoff only when requested

Separate hosting from inference and state. Record the application host and
startup command, model backend/location, operator and runtime identities, caller
authentication, authorised tool/data access, session and artefact stores, and
shutdown/cleanup owner. A local SQLite file is not a shared multi-instance state
design. A managed model does not deploy the application or authenticate its users.

For an architecture recommendation, explain which missing capability motivates
each service: application hosting, persisted conversation history, selected
long-term memory, document retrieval or analytical queries. They are distinct
jobs; neither an analytical warehouse nor a memory service automatically replaces
session storage. Installing ADK does not configure a build trigger, runtime IAM
or an identity proxy. Produce concrete deployment requirements and acceptance
gates for the selected platform; actual platform implementation is a separate
task. This skill remains usable without other chapter skills installed.

## Evidence and implementation boundary

State handoffs, branch overlap, bounded exit and typed output are grounded in
offline tests of real ADK orchestration. The historical live samples used real
models but no travel/time API. Rich termination objects, extra normalisation/
summarisation nodes and external idempotency services are production principles
to implement and test when required, not features already proved by those demos.
