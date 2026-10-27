# Select and adapt orchestration

Use the installed SDK contract and existing tests. ADK 2.8.0 contains both
deprecated compatibility agents and `Workflow`; replacing one with another is a
behavioural migration with its own acceptance evidence. Newer APIs require their own
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
keys for concurrent writers. Two parallel agents writing the same key need a post-join merge that
reconciles both results explicitly.
The inspection helper finds only simple, same-file, directly assigned siblings;
factories, nested branches and runtime keys require manual tracing.

`Workflow` can pass typed node outputs without using session-global keys for
intermediate values. In ADK 2.8.0, it cannot be placed directly in an
`LlmAgent.sub_agents` list. Verify composition rather than guessing from another
release. A graph fan-in using `JoinNode` plus a summariser adds a dependency and
often a model call; declare it explicitly, since `ParallelAgent` supplies none.
For example, a reviewer that receives the writer's draft through `{draft}` and
the run's last final text from a critic returns the critic's acknowledgement;
select the draft event explicitly.

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
retries repeat idempotent actions only.
Use [model-call-controls.md](model-call-controls.md) when implementing a strict
attempt/deadline boundary; it explains transport enforcement and safe restart.

Keep synchronously blocking I/O out of concurrent async branches or use an
explicit appropriate execution strategy. Measure overlap rather than comparing
two unreliable wall-clock thresholds. More agents can add latency and duplicate
context; add each one for a concrete responsibility or authority boundary.

## Truthfulness of the task boundary

Without a live lookup tool, label outputs illustrative and request the missing
dates, prices, availability or research. The prior travel example needed a live prompt repair for precisely
this failure. Assert the outbound prompt offline; assess actual compliance in
separately approved live samples. A prompt stays an instruction; security controls live in code.

A deterministic lookup inside two model steps makes only that node offline.
Fixed clock values are simulated even if a legacy prompt says “right now”. Prefer
plain code when it meets the real task, but account for its own I/O, failure and
compute costs. Keep a simulated service labelled simulated wherever it travels, including
production features.

## Turn the selection into an implementation

Write a small contract table before wiring nodes: input type, output type/key,
authoritative source, side effects, failure result, next consumer, and two
columns that stop omissions from travelling silently downstream:

| Column | What it records |
| --- | --- |
| Coverage output | What the stage looked for and did not find, as structured data the next consumer receives: unresolved references, issues with no operative text, pages not viewed, truncated searches |
| Identity and limits | How items are identified (occurrence IDs, document/version/page spans) and how each per-item limit was sized from the data, with the measurement that sized it |

A stage that emits only its results, and not its omissions, fails design
review: a reviewer weighs the policies retrieval delivered. For example, a
retrieval row reads:

```text
stage: retrieval | in: issues[] | out: units[] + sufficiency | source: FTS index v3
effects: none | failure: none_found per issue | next: reconciliation
coverage: unresolved_references[], truncated[] | identity: unit_id=doc:heading + page span; k=4 sized from gold recall
```
 A
downstream stage that detects an upstream omission may issue one bounded
request upstream (for example one more retrieval round within a stated call
budget) before failing; the request and its budget are part of the
contract. The memory skill's local-document coverage pack and the evaluation
skill's contract qualification give the detail for coverage records and
limit sizing when those packages are installed.

Separate model judgement from known calculations and policy checks. Agent
separation only creates a code boundary; shared credentials, tools and state
can still give every agent the same authority. Record which checks need
enforcement outside prompts.

When a reviewer repeatedly reconstructs known claim/source/issue IDs, consider
the optional [draft-bound review frame](review-contracts.md#optional-server-owned-frame).
Keep established identities and obligations in ordinary code; reserve model work
for evidence and disposition judgments. Use it only where the application's
contract benefits, and rebuild the frame after corrections.

For the checked compatibility API, import `LlmAgent`, `SequentialAgent`,
`ParallelAgent` and `LoopAgent` from `google.adk.agents`, configure named children,
and export the chosen root through the project's existing entry point. Preserve
the existing API even though compatibility agents emit deprecation warnings;
migration requires its own behavioural comparison. For a sequential repair,
trace both the writer's `output_key` and the consumer's `{key}` placeholder. For
parallel work, trace every branch and its post-join consumer in both completion
orders. A missing result key or implicit merge is fixed in the contract, whatever the
scheduler does.

For ADK 2.8.0 graph code, `from google.adk import Agent, Workflow` supplies nodes
and orchestration. A tuple such as `("START", producer, transform, consumer)` in
`Workflow(edges=[...])` expresses order. Declare the producer's `output_schema`,
the Python function's input/return annotations, and the consumer's `input_schema`
to agree. A Pydantic input named `Record` is addressed as `{Record.field}` in the
consumer instruction, while `{draft}` above is a session-state placeholder.
Inspect the rendered request in an offline boundary test: the rendered request
shows the value that crossed the edge, and an import or annotation shows the
declaration. Serialise
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

## Graph interrupts, state and retries

The facts below describe the graph API that Agents CLI scaffolds target
(`google-adk>=2.12.0` for new projects as of Agents CLI 1.11.0); this skill's
recorded baseline is 2.8.0, so confirm each one against the installed version
before relying on it.

- **Pausing a node for a person.** A node yields `RequestInput(message=...)`,
  optionally with `payload` and `response_schema`; on resume the reply is read
  from `ctx.resume_inputs`. With `rerun_on_resume=False` (the `FunctionNode`
  default) the reply is routed to the node's successor as its input and the
  interrupted node is bypassed; with `rerun_on_resume=True` (the `LlmAgent`
  node default) the node runs again from the top with `resume_inputs`
  populated (https://adk.dev/graphs/human-input/, read 22 October 2026;
  supported from ADK Python 2.0.0). adk.dev documents an implicit interrupt
  identifier for Python; the Agents CLI cheatsheet shows an explicit
  `RequestInput(interrupt_id=..., message=...)` keyword, keys `resume_inputs`
  by it and advises a unique identifier per loop iteration (for example
  `f"review_{count}"`) so a loop does not restart indefinitely (Agents CLI
  1.11.0, `google-agents-cli-adk-code` skill,
  `references/adk-python-workflows.md`, read 22 October 2026; vendor guidance,
  confirm the keyword exists on the installed version). Acceptance: a test
  resumes the paused run with a scripted reply and asserts which node ran
  again and what the successor received.
- **Deterministic first, the model for ambiguity.** The ambient-expense-agent
  recipe keeps the `$100` threshold in code (`config.review_threshold`), routes
  with `Event(route="AUTO_APPROVE" | "NEEDS_REVIEW", output=node_input)` so
  only the review branch reaches an `LlmAgent`, pauses that branch with
  `RequestInput` for a manager, and is driven by Pub/Sub push to the ADK
  trigger endpoint (`trigger_sources=["pubsub"]` on the FastAPI app; the
  trigger payload is base64 in production and plain JSON in local tests)
  (google/adk-recipes be63596, `core/python/ambient-expense-agent/expense_agent/{agent,fast_api_app}.py`
  and `README.md`, read 2026-10-22; vendor sample, "not production use").
  Copy the shape: business rules in function nodes, judgement in one LLM node,
  the pause on the node that needs a person. The recipe's Terraform owns
  Pub/Sub, two Cloud Run services and IAP; a redelivered Pub/Sub message is a
  repeat of the same expense, which the 2.12.0 trigger delivery id lets the
  parse node detect (`adk-operational-guardrails`).
- **Reference wiring.** ADK's repository carries twenty-four workflow
  samples under `contributing/samples/workflows/`, among them `retry`,
  `dynamic_fan_out_fan_in`, `request_input` and `request_input_rerun`, and
  `hitl/` samples for the confirmation and request-input gates (main ed76f94,
  read 2026-10-22); read one for the API shape on the installed version and
  keep this reference's acceptance contracts.
- **Confirming a node.** From ADK 2.12.0 a workflow node (`@node`,
  `FunctionNode`) takes `require_confirmation` (absent on the 2.8.0
  baseline). The gate stays code; its mechanics and the duplicate-reply rule
  are under [confirmation mechanics](#confirmation-mechanics) below, and the
  re-run on resume under [runtime](runtime.md#recovery-claims).
- **State written by a node.** An `Event` carries `output` (to the successor),
  `route` (edge selection) and `state` (a delta committed with the node's
  events). adk.dev says to write state through `ctx.state` rather than
  returning it, and that writes are committed with the node's events and
  visible to downstream nodes in the same run
  (https://adk.dev/graphs/data-handling/, read 22 October 2026). The Agents
  CLI cheatsheet prefers `return Event(output=..., state={...})` because the
  delta is persisted in event history and replayable, and calls a
  `ctx.state[...]` assignment a side effect that may be lost on replay (same
  skill, `references/adk-python-workflows.md`; vendor guidance). Choose one
  convention per project and test it under resume and rewind rather than
  trusting either description. Only the last `output` a node yields reaches
  its successor, and state is not for large payloads: use artifacts or a
  store (adk.dev, same page).
- **Typed outputs inside a graph.** Set `output_schema` on every `LlmAgent`
  node; without it the output is `types.Content`, which breaks typed function
  nodes and serialisation through `JoinNode` or a database session (the adk.dev
  data-handling page and the Agents CLI cheatsheet agree). `JoinNode` emits a
  dict keyed by predecessor names; `ctx.state.get(key)` returns a dict, so
  rebuild typed access with `MyModel(**data)`.
- **Runtime-sized fan-out and retries.** `ParallelWorker` processes a list
  concurrently, one worker per item; `state_schema` on `Workflow` or
  `FunctionNode` validates state with a Pydantic model;
  `FunctionNode(..., retry_config=RetryConfig(...))` retries a failing
  function node; an unconditional cycle is rejected, so a loop needs at least
  one routed edge (Agents CLI cheatsheet, `references/adk-python-workflows.md`;
  vendor guidance, not found on adk.dev for Python on 22 October 2026, so
  verify the symbols in the installed package before use).
- **Delegation modes inside a graph.** Task-mode sub-agents are disabled
  inside graph workflows in ADK Python 2.0.0, and task-mode agents must be
  leaf agents (https://adk.dev/workflows/collaboration/, read 22 October
  2026). Model a specialist as a node instead; `adk-tool-interface-design`
  owns the delegation interface outside graphs.

When the project has `agents-cli-manifest.yaml`, consult the installed
`google-agents-cli-adk-code` skill (`references/adk-python-workflows.md`, or
the `ambient-expense-agent` recipe for an event-driven `Workflow` with an
approval pause and the `deep-search` recipe for a plan-approval loop, both in
`google/adk-recipes`); if it is not installed, adk-engineer explains how to
get it. The recipe shows the wiring; this reference owns the acceptance
contract.

### Confirmation mechanics

<!-- shared:tool-confirmation -->
**ADK tool confirmation mechanics** (google-adk 2.8.0 and 2.12.0 source, read
2026-10-27; confirm on the installed version):

- `FunctionTool(func, require_confirmation=True)` asks before every call;
  `require_confirmation=` also takes a callable, so the threshold lives in code
  that sees the arguments, not in the prompt. `McpToolset(require_confirmation=...)`
  applies the same to server tools.
- On `FunctionTool` the callable is invoked with the tool function's own
  validated arguments as keyword arguments, plus the context parameter only
  when the tool function declares one, so its parameters must match the
  function's. On `McpTool` it receives the tool arguments plus `tool_context`
  when the callable's own signature names it (or takes `**kwargs`). Sync and
  async callables both work.
- Return a strict `bool`. `None` or another falsy value lets the call run
  unconfirmed (community report #7010), and from 2.10.0 the framework's gate
  holds a call only on exactly `True`.
- Order on 2.12.0 (`flows/llm_flows/tools/_caller.py`): the plugin's
  `before_tool_callback`, each agent `before_tool_callback` in order, the
  confirmation gate, then the tool body. The confirmed resume re-dispatches the
  original call through the same path, so a `before_tool_callback` runs again
  and may refuse it. A bound that must hold whatever the model or the approver
  does lives in the tool body or the store, with the callback as the early
  refusal.
- With no confirmation attached, the call returns `{"error": "This tool call
  requires confirmation, please approve or reject."}`, sets
  `skip_summarization` and records a request through
  `tool_context.request_confirmation(hint=..., payload=...)`, keyed by the
  `function_call_id` (which must be present). A rejected confirmation returns
  `{"error": "This tool call is rejected."}` and the body never runs: report
  it as a cancellation with no attempt, not as an unknown outcome.
- Inside a tool, `tool_context.request_confirmation(hint=, payload=)` pauses
  with a message and the structure the approver must return; the reply
  arrives as `tool_confirmation.payload`. Below 2.10.0 a custom `BaseTool` must
  check `tool_context.tool_confirmation.confirmed` itself; from 2.10.0 the
  framework holds any tool whose `check_require_confirmation` answers `True`,
  and `BaseTool`'s default answers `False`, so a custom tool overrides that
  hook.
- The client answers with a `function_response` named
  `adk_request_confirmation` whose `id` is that request's `function_call_id`
  and whose `response` holds `confirmed` and `payload`; with resumability it
  also carries the original `invocation_id`. On 2.12.0 the framework refuses a
  confirmation whose original call's name or arguments differ from the call in
  history (`flows/llm_flows/tools/_confirmation.py`).
- The answer must come from the authenticated controlling user through the
  application's API, never from A2A, an unauthenticated `/run` or text the
  model wrote. Confirmation records consent; it does not authenticate the
  caller or grant business permission. Forged confirmation responses in
  history were fixed in 2.5.0 and 2.6.0; 2.11.0 adds HMAC stamps with
  `ToolCallIntegrityPlugin`.
- ADK 2.12.0 runs a confirmed tool once per approval (CHANGELOG, bfdeb4a,
  closes #7434); below 2.12.0 a re-sent approval could run the tool again. The
  resume page warns that long-running functions may run more than once when
  resuming. On every version, test a duplicate approval reply and keep an
  operation record or idempotency key: it, not the framework, makes a repeated
  approval converge on one effect.
- 2.12.0 accepts `require_confirmation` on workflow nodes (`@node`,
  `FunctionNode`; 988fd1a), so a gate can sit on the node rather than inside a
  tool; it is absent on 2.8.0. From 2.9.0 a failed node re-runs on resume, so a
  confirmed node whose body writes externally still needs the idempotency key.
- The confirmation page (adk.dev, read 2026-10-22) lists
  `DatabaseSessionService` and `VertexAiSessionService` as unsupported. With a
  persistent session store, a decision that may take hours, another person
  deciding, or completion that must survive restarts, use a durable review
  record instead of the in-session confirmation; approval is permission, not
  completion.
<!-- /shared:tool-confirmation -->

## Prepare a production handoff only when requested

Separate hosting from inference and state. Record the application host and
startup command, model backend/location, operator and runtime identities, caller
authentication, authorised tool/data access, session and artefact stores, and
shutdown/cleanup owner. Shared multi-instance state needs a shared store; a local SQLite file serves
one instance. A managed model serves inference; deploying the application and
authenticating its users are their own responsibilities.

For an architecture recommendation, explain which missing capability motivates
each service: application hosting, persisted conversation history, selected
long-term memory, document retrieval or analytical queries. They are distinct
jobs, and session storage keeps its own beside an analytical warehouse or memory
service. A build trigger, runtime IAM and an identity proxy are configured on
their own after ADK is installed. Produce concrete deployment requirements and acceptance
gates for the selected platform; actual platform implementation is a separate
task. This skill remains usable without other chapter skills installed.

## Evidence and implementation boundary

State handoffs, branch overlap, bounded exit and typed output are grounded in
offline tests of real ADK orchestration. The historical live samples used real
models but no travel/time API. Rich termination objects, extra normalisation/
summarisation nodes and external idempotency services are production principles
to implement and test when required, not features already proved by those demos.
