# Verify runtime integration and failure recovery

Read when turning Agent Runtime optimisation advice into reproducible tests,
extending a previously verified profile, or validating streams and deferred work.
Use [runtime-application-integration.md](runtime-application-integration.md) for
the executing path and [runtime-lifecycle.md](runtime-lifecycle.md) before any
provider mutation. These recipes use injected boundaries; cloud execution is a
separate approved stage.

## Choose the boundary, then the substitute

Use the target's existing interpreter and preserve dependency pins. Inspect tests
for constructors, imports and callbacks that can contact a provider. Keep actual
App/Runner/session/event/tool orchestration when testing ADK behaviour; replace
model generation and external storage/query/HTTP transports. A generic dictionary
or a permissive fake CLI can hide the exact contract that failed in production.

| Claim | Execute | Observe directly |
| --- | --- | --- |
| Profile and App settings apply | Real startup in a fresh process | Selected model, tools, summariser and App passed at the actual constructor |
| Conversation is reused | Two turns plus a fresh client read | Same authorised owner/session and stored first-turn events |
| Compaction selects context | Real ADK Runner with deterministic generation | Summariser input, compaction metadata, next request and retained raw storage |
| Deployment carries a change | Actual generator/serializer with transports replaced | Archive entries, generated loader, serialized spec and later effective provider GET |
| Streaming completes | Actual consumer reading the entire finite stream | Provisional updates, accepted answer only after clean exhaustion, late-error rejection |
| Deferred work resumes correctly | Actual start/response/continuation seam | Original call ID/name, job identity and authorised terminal result before resumed generation |

Use distinctive synthetic markers instead of personal data. Preserve event and
operation identities; redact diagnostic output without rewriting captured failures
into success. Keep component, application, hosted, delivery and cleanup verdicts
separate. Replaying a saved JSON file establishes no remote provenance.

## Use controlled interleavings rather than timing guesses

For asynchronous failures, block at an injected adapter using `asyncio.Event` and
advance the exact race deliberately. Arbitrary sleeps can miss the fault on a fast
or slow machine. Assert values and identities as well as call counts.

| Reproduction | Required acceptance after a target repair |
| --- | --- |
| Begin saving sealed turn A; append turn B while the store is blocked; release A | Stored A contains exactly A and B remains pending; no shared-buffer clear removes it |
| Store accepts A but raises before acknowledgement; retry | Same immutable key and bytes, store-enforced deduplication, no double effect and no replacement with later input |
| Two flushes contend while input arrives | Serialised delivery of the same pending batch; explicit sealed-turn policy and no lost or reordered accepted data |
| Consumer fails while producer is waiting for new input | Supervisor observes failure without needing another incoming frame and stops admission |
| Processor raises `TimeoutError` after a successful queue read | Processing failure is surfaced; it is not treated as an idle queue timeout |
| Shutdown follows a failed consumer | Bounded failure-aware drain; no indefinite `queue.join()` or false successful-processing claim |
| An uncertain external submission is retried | Original job/operation identity reconciled; no new side effect just because acknowledgement was lost |

The companion's buffer caught `asyncio.TimeoutError` around both `queue.get()`
and the processor await. On Python 3.11 this is an alias of built-in `TimeoutError`,
so a processor timeout entered the idle-poll handler. A controlled offline probe
reproduced successful-looking shutdown after that failure. Keep the queue-wait
handler scoped to the wait alone, then handle processor failure through the
supervisor. Calling `task_done()` updates queue accounting; it does not attest to
successful processing. See the [Python exception definition](https://docs.python.org/3.11/library/asyncio-exceptions.html).

The separate persistence demonstration also reproduced loss of B during A's
write. These examples remain simplified companion code, not implementations of
the stronger protocols in [runtime-state-and-streams.md](runtime-state-and-streams.md).
Do not copy their shutdown or join/await/clear ordering into a production adapter.

## Validate memory and jobs at each acknowledgement boundary

For memory ingestion, capture exact completed event IDs after the acknowledged
cursor and freeze the payload before handing it to a worker. Drive the worker
through claim, provider submission, accepted operation, terminal completion and
cursor acknowledgement. Fail between each pair. Verify that the cursor advances
only over the acknowledged batch and that newer events are not silently consumed
by a mutable "latest events" lookup. A stable local key does not prove the remote
service deduplicates ingestion.

For a job, keep durable acceptance, worker completion and the resumed model answer
as three separate checks. Use deliberately different function-call and job IDs.
Pair the actual initial call/response across events, consume the entire initiating
stream, and test more than one submission rather than trusting a "call once"
instruction. Read the terminal record through the authorised backend before
constructing a `FunctionResponse`; never trust an end-user-supplied terminal body.

Exercise failure, cancellation, duplicate callback, replaced owner/session,
conflicting idempotency key, lost initial response and worker restart. Verify that
an already accepted job is recovered under its original key and that stale workers
cannot replace a newer terminal result. Bound stored output before download and
the model-facing summary before continuation. A correct response envelope alone
proves neither job durability nor a complete resumed answer.

## Test streaming without confusing it with a tool verifier

For a decoded finite invocation, the optional
[finite answer consumer](../assets/finite_answer_stream.py) provides a reusable
completion boundary. Read its contract and limits before adapting it. It keeps
previews provisional, excludes thought/tool-bearing text from display and returns
an accepted answer only after a designated author's nonpartial STOP candidate and
clean stream exhaustion. The caller then replaces the preview and commits the
completed answer. A callback that already persists previews as complete messages
would defeat that separation.

Match the supported decoded Part schema as well as the final marker. Function,
code-execution and server-side tool parts can accompany preliminary model text;
a STOP marker alone does not make that text an answer. The component has a
text-only acceptance contract and rejects unsupported non-null Part payloads.
Inspect the target SDK's actual serialisation when extending it for multimodal
output; silently ignoring a new field can change completion semantics.

After copying the component into the target package, integrate it at the decoded
event boundary. Here `events` is the owned iterator, and `show_snapshot` updates
only provisional display state:

```python
from finite_answer_stream import StreamLimits, consume_answer

answer = await consume_answer(
    events,
    answer_author="support_agent",
    invocation_id=trusted_invocation_id,
    preview_mode="delta",
    send_preview=show_snapshot,
    limits=StreamLimits(),
    min_partials=0,
)
# Commit answer.text only after this returns, replacing the preview.
```

Select the target's actual author and `delta` or `snapshot` input semantics.
The callback always receives reconstructed display snapshots, including meaningful
whitespace and deliberate empty-text corrections. `min_partials` counts nonblank
eligible input partials; zero asks for completion without a delivery claim.

Teaching defaults are 256 events, 64 KiB per event, 1 MiB of total compact UTF-8
event bytes, 64 KiB aggregate eligible text, 60 seconds overall and two seconds
for closure. Every bound is inclusive and configurable. The text budget counts
each incoming cumulative snapshot again and includes the final answer; it is not
just the size of the final display. Re-encoding decoded events cannot bound the
original transport allocation or detect duplicate JSON keys already discarded by
the decoder. Apply raw frame, decoding and semantic tool limits upstream.

On `StreamRejected`, mark the preview incomplete; the message is a fixed code and
`cleanup_failed` separately reports unsuccessful iterator closure. Caller
cancellation propagates; a fixed exception note records secondary close failure.
If an adapter swallowed cancellation but left a pending task cancellation request,
the helper raises a new cancellation with a fixed note; the swallowed exception's
identity is unavailable. An adapter that also clears that request with `uncancel()`
can hide it. Test cooperative cancellation at the actual adapter boundary.
The helper calls `aclose()` when the owned iterator provides it, even after clean
exhaustion. An adapter without that method still needs its supported transport
closure by the caller. No failed or unclosed stream returns an accepted answer
when the provided closure operation reports failure.

The consumer does not parse SSE, authenticate a caller, authorise a session or
validate the business meaning of tool responses. Decode bounded transport frames
first and retain trusted invocation identity; test required tool results separately
through the actual workflow. For the narrower saved one-call-per-tool smoke,
use [check_run.py](../scripts/check_run.py). Neither helper verifies arbitrary
multi-agent graphs or bidirectional turn completion.

Exercise a late error after a plausible final, thought-only output, tool-associated
text, MAX_TOKENS, missing/conflicting metadata, another invocation, malformed
markers, an enormous single event, cumulative bytes, and multibyte UTF-8 limits.
Drive stalled input, callback failure, caller cancellation and iterator-close
failure. Assert that no accepted answer escaped on failure and that owned cleanup
was attempted without masking the primary cancellation/error. Cooperative timeouts
cannot force a blocking or cancellation-suppressing adapter to stop. Once control
returns, reject an expired operation or closure rather than interpreting suppressed
cancellation as success. Check the absolute clock too: synchronous work can delay
the timeout callback. Local closure cannot undo a remote tool operation.

Then test the actual SDK/REST adapter, application server, proxy and browser as
separate stages. An async iterator is not proof of token delivery. Explicitly
configure the selected streaming surface; require eligible nonblank partials only
when testing incremental delivery. A complete answer with zero partials passes a
completion claim but not a two-partial delivery claim. Delta and snapshot displays
need different assembly, and the complete answer replaces either preview.

The historical remote terminal client established continuity and complete routing
results under an external harness. It printed text without the full consumer or
an SSE RunConfig. That outcome establishes neither this helper's deployment nor
browser delivery. Stream and token-compaction tests bundled with the portable
skill are offline evidence, not new hosted coverage.
