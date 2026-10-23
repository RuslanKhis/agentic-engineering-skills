# Events, state and response consumption

Inspect the target SDK and application's result contract before changing its
consumer. The details below were checked against ADK 2.8.0 implementation.

## Process the whole run deliberately

A session contains conversation state and events from multiple invocations. An
invocation is logical work; a paused invocation may resume under the same ID in
a later Runner call. End of one iterator is not proof that paused work finished.
With the default Runner configuration, create the session before calling
`run_async`; `auto_create_session` is a separate supported configuration.

For a complete, non-partial event, the Runner appends/processes it before yielding
it to the application, then allows the producer to resume when iteration advances.
Consume to exhaustion, deliberately cancel, or close through the application's
chosen lifecycle. Returning on the first final-looking event can interrupt work.
Do not invent one universal text-extraction helper: some workflows return several
branch outputs, a particular state key, or structured node output.

`event.is_final_response()` helps select response semantics, but several agents
can produce final responses in one invocation. Check content/parts/text before
reading them, handle failure rather than manufacturing an empty success, and
preserve the workflow's designated author/node/state result.

Choose and test the result adapter explicitly:

| Application contract | Selection after consuming the run |
| --- | --- |
| One named conversational agent | Retain text-bearing final responses from the designated author; define what no matching response means. |
| Sequential or loop artefact | Read the designated committed key after a successful current turn; a critic acknowledgement is not the artefact. |
| Parallel branches | Read every required branch result after the join; one final text cannot represent all branches. |
| Typed `Workflow` result | Use the expected node/workflow's structured `event.output`, with its author and `node_info.output_for` provenance. JSON uses `nodeInfo.outputFor`. Preserve valid empty output such as `[]`. |

For graph output, a result may be a Python/Pydantic value with no text parts.
Do not discard it with `if event.output` or use `str(value)` as a JSON serializer.
Validate the expected type/schema and presence for that node. In the checked
plain-function Workflow path, a bare `None` may produce no output event; if null
is a meaningful result, return an explicit typed envelope such as
`{"value": None}`. `event.output is None` cannot distinguish absent output from
a successful null result. Consume the remaining
events, check error/paused status and then deliver the result. Early text must
not hide a later tool or workflow failure. The structured-output and callback
recipes in [test_runtime_contracts.py](../tests/test_runtime_contracts.py) exercise
the real Runner with the model boundary substituted.

Persistent result keys need a freshness contract. A new failed turn can leave a
previous turn's successful value in the same session. Gate delivery on the current
turn's success and expected producer; if the application permits reuse, record
and compare the producing invocation/version. Do not blindly clear shared state
or treat a populated `final_copy` as proof of new work. Test success followed by
failure on the same populated session, not only failure on an empty session.

## Commit and durability are separate

Writing through tracked `context.state` updates the invocation's view immediately.
The corresponding `event.actions.state_delta` must reach a successfully processed
complete event to establish the service-side transition. Earlier local reads are
not proof that a persistent service committed the value. `temp:` keys are scratch
space, not durable resume data.

Resume and durable execution are different promises. ADK's own resume
(`ResumabilityConfig(is_resumable=True)` on the `App`) restarts an
interrupted invocation from the last completed step with the tools run
**at least once**, "and may run more than once"; it is not supported from
`adk web` or the CLI, not on by default for custom agents, and a workflow
modified between pause and resume is unsupported (google/adk-docs
`docs/runtime/resume.md`, read 2026-10-23; vendor documentation). So the
caller still detects the failure and re-invokes, and every tool behind a
resumable step carries the idempotency key and reconciliation from
`safe-api-tool-calls`. A durable-execution engine removes the caller from
that loop and survives a worker crash or a wait of days; it does not remove
the key, because every engine checkpoints a step's result, and a crash after
the provider accepted the write but before the checkpoint re-executes the
step. Two engines publish ADK integrations with tests worth copying:

- **Temporal** (`temporalio-google-adk` 0.0.1 on PyPI, 2026-10-07,
  pre-release; temporalio/ai-integrations commit bb179c3, MIT,
  `python/google_adk/README.md` and `tests/`, read 2026-10-23). Each model
  call runs as the `invoke_model` activity and MCP tools as activities
  through `TemporalMcpToolSet`; the `GoogleAdkPlugin` makes the workflow
  deterministic by routing ADK's `time` and `uuid` through the workflow
  clock and id generator. Facts that change a design: the MCP toolset
  requires MCP SDK 1.x, which fixes the `mcp` major for a project that
  adopts it; `factory_argument` values are recorded in workflow history and
  visible in the web UI without a payload codec, so credentials are
  resolved worker-side inside the toolset factory; on a human-in-the-loop
  resume, completed nodes fast-forward and `rerun_on_resume=True` bodies
  re-execute, so side effects go through activities or are idempotent;
  long chats grow history and need `continue-as-new` boundaries between
  turns; and workflow code re-executes on every replay, so ADK's
  OpenTelemetry metrics, spans and logs are re-recorded unless Temporal's
  replay-safe providers are installed (one execution plus three replays
  recorded four times in its own example). Its `Replayer` tests replay
  recorded histories for single-agent, multi-agent, graph-workflow and
  human-in-the-loop cases, which is the shape of a determinism regression
  test: a recorded history that no longer replays is a breaking change.
- **DBOS** (`dbos-google-adk` 0.1.0 on PyPI, 2026-05-07; dbos-inc/dbos-google-adk
  commit 288757e, MIT, `README.md` and `tests/test_dbos_plugin.py`, read
  2026-10-23; declares `google-adk>=1.32.0`, unverified on 2.x here). Needs
  only Postgres, and its declared ADK floor predates 2.x, so a project on a
  2.x pin adopts it behind a compatibility gate: a planned test that imports
  the plugin against the pinned google-adk and runs its fork-replay case,
  reported as not run until the packages are installed; the pin is not
  changed for the engine. `DBOSPlugin` on the `Runner` checkpoints every model call
  and must run inside a `@DBOS.workflow()`, tools are `@DBOS.step()`
  functions, and `DBOSEventSummarizer` makes the compaction call durable
  too. Its replay test forks past the last recorded step and asserts the
  tool body ran once (`call_count == 1`), and its failure test records that
  ADK does not recover from a tool exception on its own; the exception
  propagates and the step's retry policy decides.

The same decision has two neighbours that name the other half: the review
record that outlives a process (`adk-operational-guardrails`, human review,
"a separate durable review operation") and the idempotency key that the
engine does not retire (`safe-api-tool-calls`, writes and confirmation).
Choose in this order: plain `ResumabilityConfig` with idempotent tools when
a caller can re-invoke and nothing waits longer than a request; an engine
when runs must survive a crash with no caller or wait for a human for days;
and in both cases the kill-after-the-write test from `safe-api-tool-calls`
(kill after the tool returns: body ran once; kill after the provider
accepted: one effect at the provider double through the key; the same test
on plain resume shows the duplicate the key absorbs). Version-pin the
engine, keep secrets out of its history, and treat its replay tests as part
of the suite.

Four rules for code around a pause, whichever engine resumes it (langchain-ai/docs commit 23152b1, MIT, `src/oss/langgraph/interrupts.mdx`, "Rules of interrupts", read 2026-10-23; another framework's rules, restated for ADK): a
node re-runs from its beginning on resume, so everything before the pause
runs again and any side effect there is idempotent or moved after the pause;
never wrap the pause in a bare exception handler, because a pause that is
caught never reaches the caller (catch specific exceptions, and keep the
pause outside the handled block); never reorder or make conditional the
pause points inside one node, because resume values are matched to pauses
by position; and never loop around a pause with a condition that can differ
between executions, such as a `while True` validation loop. On ADK the node
is a workflow node with `rerun_on_resume=True` or a tool that requests
confirmation, and the first rule is the at-least-once statement above read
from the node's side.

Tracked writes occur at the top-level state assignment/update boundary in the
checked SDK. `context.state["cart"]["items"].append(item)` can change a local
object without producing a state delta. Use copy–modify–reassign when changing
mutable nested values:

```python
from copy import deepcopy

cart = deepcopy(context.state.get("cart", {"items": []}))
cart["items"].append(item)
context.state["cart"] = cart
```

This is a callback/tool fragment; `context` and validated `item` come from the
application. Verify the complete event's delta and reload through the session
service. An in-memory alias appearing changed is weaker evidence than a committed
delta; persistence claims additionally require the configured durable service.

Choose state scope deliberately: unprefixed keys are session-scoped, `user:` is
shared across one user's sessions within an app, `app:` across the app's users
and sessions, and `temp:` is invocation scratch state omitted from persistence.
On adk-python main a `temp:` delta is applied to the in-memory session state
for the rest of the invocation and trimmed from the persisted event
(`sessions/base_session_service.py`, `_apply_temp_state` and
`_trim_temp_delta_state`, ed76f94, read 2026-10-22; confirm on the pinned
version), so a later tool or callback in the same invocation can read it and
the next invocation cannot. When parallel function calls complete, ADK merges
their response events into one: actions are deep-merged, nested dicts
recursively and otherwise the later event's value winning for the same key,
and UI widgets are concatenated without a duplicate check
(`flows/llm_flows/tools/_batch_executor.py`, same commit). Give tools that
may run in parallel distinct top-level state keys.
Keep caller-specific results and permissions out of `app:` and mutable module
globals. These scopes do not authenticate the supplied user ID or isolate tool
credentials; test populated control sessions when claiming data separation.

`InMemorySessionService` loses data when its process stops. ADK Web's default local
SQLite session store survives a restart. Use the configured persistent service
and an actual process restart to validate durability; recreating a Python object
or a mock is insufficient. Redacting application telemetry does not redact saved
session events. Check both data paths and their retention/access rules.

`context.save_artifact(...)` saves bytes via the artifact service; the subsequent
event's `artifact_delta` is metadata/receipt, not the file itself. Deleting a
session does not establish artifact erasure, privacy-worker coverage, provider
backup erasure or removal of provider request records.

## Streaming and browser claims

`run_async` is an async event iterator even with `StreamingMode.NONE`. Model
chunk streaming requires an appropriate run configuration, such as
`RunConfig(streaming_mode=StreamingMode.SSE)` in the checked version. Partial
events support display and are not session commits; a successful streamed
response later produces a complete event. Cancellation/failure can prevent that.

In checked ADK Web, **More options → Streaming** changes model streaming and is
stored in the browser profile. Hold that setting constant when comparing runs.
Measure from Submit to first meaningful content and to the complete correct
result. Spinners and heartbeats are not meaningful answers. Record cold/warm,
sample count, raw timing intervals and failures; small smoke samples do not
establish p95 or a service guarantee.

ADK Web is a local unauthenticated developer UI. Keep it on loopback; `userId`
partitioning is not authenticated caller identity. A local UI with a cloud model
is not a cloud-hosted application. Customer authentication and tenant enforcement
are separate work, not a toggle this skill silently supplies.

## Recovery claims

For application-stage reuse, read [checkpoint qualification](checkpoint-reuse.md).
Framework replay capability does not establish that a retained result is valid
for changed inputs, current authority or a new draft.

Dynamic parents using `ctx.run_node` can use `rerun_on_resume=True` so completed
child results can be replayed. This is a framework capability, not a guarantee
that arbitrary external actions execute exactly once. Put side effects in
idempotent child nodes and reconcile uncertain provider outcomes before retries.
The historical chapter tested completed-history persistence, not interruption
and replay of a child workflow. Reproduce actual interruption/recovery if the
target feature depends on it, and label that new evidence separately.

From ADK 2.9.0 a node that failed runs again when the workflow resumes;
before 2.9.0 it replayed as though it had completed (CHANGELOG 2.9.0,
91573eb: "Make node bodies idempotent: a node that performs an external side
effect and then fails will perform that side effect again on every resume";
read 2026-10-22 at main commit ed76f94). On the 2.8.0 baseline the old replay
applies, so the same workflow behaves differently across the pin. Either way,
a node body that writes outside the process carries an idempotency key and
reconciles an uncertain outcome before it acts again; `safe-api-tool-calls`
owns that contract and its tests. Acceptance on 2.9.0 or later: a test fails
a node after its side effect, resumes, and asserts the effect occurred once at
the provider double.
