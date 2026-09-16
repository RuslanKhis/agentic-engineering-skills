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

Dynamic parents using `ctx.run_node` can use `rerun_on_resume=True` so completed
child results can be replayed. This is a framework capability, not a guarantee
that arbitrary external actions execute exactly once. Put side effects in
idempotent child nodes and reconcile uncertain provider outcomes before retries.
The historical chapter tested completed-history persistence, not interruption
and replay of a child workflow. Reproduce actual interruption/recovery if the
target feature depends on it, and label that new evidence separately.
