# Runtime state, streams and deferred work

Use this reference when an ADK Agent Runtime turn involves incremental delivery,
live input buffers, asynchronous persistence, optional memory writes or a job
whose result arrives later. These are production designs to adapt and validate;
the historical routing campaign did not establish them as hosted capabilities.
Inspect the target's current APIs and preserve their successful behaviour.

## Separate preview delivery from accepted completion

Identify the serving surface. The ADK HTTP server's `/run_sse` request with
`streaming: true` differs from a deployed runtime's `async_stream_query` or
`:streamQuery?alt=sse` surface. An async iterator can yield whole events with no
incremental answer text. For ADK 2.8, an explicit `RunConfig` with
`StreamingMode.SSE`, serialised using `model_dump(mode="json")` for the remote
query wrapper, requests incremental behaviour; still verify actual delivery.

Declare which author supplies the answer and whether text is a delta or a
cumulative snapshot. Treat partials as provisional display only. Filter thought
text and tool-bearing events out of user-facing answer text while retaining
their required protocol fields in the underlying conversation. Do not invoke a
tool again from a partial function-call fragment.

For a finite, single-answer invocation, retain a nonpartial `STOP` answer as a
candidate until the complete stream ends without an error. Reject interruption,
truncation, missing completion metadata under that policy, mismatched identities,
late errors and subsequent answer text. Replace the preview with the accepted
answer instead of concatenating the complete text onto its partials. Mark failed
or timed-out previews incomplete and keep them out of completed conversation
state. A multi-agent graph or bidirectional connection needs its own explicit
answer/turn-completion policy; connection closure is not a universal turn signal.

Bound response bytes before decoding, events, visible text, individual transport
operations and the whole turn. Close abandoned iterators and propagate
cancellation. Read complete SSE frames; one network chunk is neither one token
nor necessarily one event. Measure first event, first eligible nonblank partial
and accepted completion at each client/server/proxy boundary. A complete answer
with zero partials proves completion but fails an incremental-delivery claim.

Use [validation.md](validation.md) and [check_run.py](../scripts/check_run.py)
for a saved **one-invocation tool-and-answer smoke** after safe transport decoding.
Keep invocation/call IDs and completion/error metadata. The checker is not an
SSE parser, browser renderer, live budget controller or a long-running-job
continuation validator. Its one-call-per-tool contract intentionally rejects
legitimate more complex trajectories; test those through a suitable adapter.

## Make optional memory writes durable rather than awaited on every turn

Use current session context when it suffices. Retrieve bounded authorised memory
on demand, or preload it only when most turns need it. If memory is required for
the answer, await it under a deadline. Otherwise enqueue exact completed events
for a supervised worker; `await` and an unretained `create_task()` do not provide
durable background delivery.

Choose incremental ingestion or terminal ingestion. For incremental work,
capture exact event IDs after an acknowledged durable cursor, retain a stable
work identity, and advance the cursor only after completion. At close, process
only unacknowledged events. For terminal work, use an explicit close action or
idle sweep and ingest the selected conversation once. A response callback is
not a close event; TTL deletion is not a dependable pre-expiry processing hook.

An outbox should atomically retain owner, session, exact event IDs or immutable
payload reference and delivery status. Record provider operations and reconcile
uncertain writes. A diagnostic metadata key is not provider-enforced idempotency;
a crash after remote acceptance but before local acknowledgement can replay work.
Implement supported deduplication or reconciliation and test that gap. Specify
memory retention/deletion separately from session cleanup. These rules optimise
the response path; a general memory architecture is outside this skill's scope.

## Bound input and observe failed consumers

Bound per-session chunk count **and** chunk bytes, plus aggregate concurrent
sessions, queued age and in-flight work. Moving each frame into a task merely
relocates an unbounded queue. Choose overload behaviour by data meaning: a codec
may tolerate explicitly dropped disposable audio; transcripts, approvals, tool
results and payments require backpressure, admission rejection or a visible
failure rather than silent loss.

Retain the consumer task, await processing and observe failure even while input
is idle. Race waiting for input against consumer termination. Apply processing
deadlines and call `task_done()` in `finally`; bounded workers may be useful for
measured concurrency. Ensure upstream transport honours rejection/backpressure.

On shutdown, close admission under the same gate used by producers, enqueue the
termination signal after accepted input, and allow a bounded drain. If the
consumer fails or drain expires, cancel and await owned tasks and report discarded
work. An unbounded `queue.join()` can hang after its only consumer has failed.
Cancellation does not prove a provider undid previously accepted work.

## Freeze completed turns before persistence

Assign input to a logical turn before sealing it. Persist completed turns or
selected summaries rather than every UI fragment, according to the required
durability of accepted input. An immutable batch contains trusted owner/session,
turn/batch identity, ordered payload and delivery status.

Under a lock, detach that completed batch from pending input **before** the first
storage await; serialise flush attempts. New input belongs to another pending
buffer. Clear only the acknowledged in-flight batch, never a shared list that may
have received input while storage was running. Retain a failed batch unchanged,
including its key, and deliver it before advancing under the chosen ordering
policy. A late append to a sealed turn needs an explicit rejection or separate
sequenced-batch policy, not a silent change of the retried payload.

The store must enforce idempotency and reject conflicting payloads under the same
owner/session/turn key. A client-generated hash alone does not prevent duplicate
effects. A timeout may follow a committed write; retry or reconcile with the
original identity. Include pending and in-flight data in count/byte bounds so a
failed batch cannot allow unlimited later input.

The in-memory swap prevents one concurrency bug but does not survive process
loss. Use a transactional outbox or journal before acknowledging crash-durable
acceptance. Multiple processes require store-level coordination. Summarisation
needs the same frozen-source rule; summary quality is a separate acceptance test.

Exercise input arriving during a blocked write, concurrent flushes, rejection
after sealing, failure after remote acceptance, repeated delivery with the same
key, conflicting key reuse, retained-failure overload and shutdown with pending
work. Verify exact saved data and remaining pending data, not just write counts.

## Keep tool-call identity separate from durable job identity

`LongRunningFunctionTool` marks a deferred response protocol. Its start function
must submit work and return promptly; the wrapper does not create a durable
worker. Replace process dictionaries and daemon threads with a job service when
work must survive restart. Persist an authorised owner/idempotency-key/request
binding and outbox entry before acknowledging the job. Duplicate starts reuse
the same job; conflicting input under the same key fails.

Keep `pending`, `running`, `done`, `failed` and `cancelled` distinct. Use worker
leases, execution deadlines, terminal-state protections, retention and bounded
status polling. Authorise start/status/cancel/result operations. An opaque handle
is not permission. Authenticate and deduplicate callbacks, then read current
durable status rather than trusting an arbitrary callback body.

Persist the mapping between ADK `call.id`, function name, application `job_id`,
session, invocation and trusted owner. Collect actual calls identified by
`event.long_running_tool_ids` and pair their initial responses by call ID; they
can arrive in separate events. Keep reading the initiating stream to account
for every submission. Reconcile missing responses through the durable start key,
and follow an explicit policy if more than one job was submitted.

The trusted coordinator constructs the later GenAI `FunctionResponse` using
the **original function-call ID and name**. The job ID remains inside its payload.
Require a matching authorised terminal job; bound successful summaries and return
safe public failures for failed/cancelled jobs. `Content(role="user", ...)` is
the SDK envelope, not authority for an end user to fabricate a worker result.
Resume the same authorised session, with separate budgets for starting and
continuing the model turn. Durable sessions/resumability do not themselves
deliver jobs or deduplicate continuations.

Test different call/job IDs, wrong job/function/owner/session, lost initial
acknowledgement, failed/cancelled results, duplicate callbacks, restart and
bounded reports. Verify durable acceptance, terminal worker outcome, correlated
continuation and the completed model explanation separately. Cleanup of job
records/results/queues follows their own ownership and retention policy; see
[lifecycle.md](lifecycle.md) before any external mutation.
