# Design the runtime and delivery contracts

Use the relevant sections when a requirement depends on context size, browser
delivery, concurrent work, performance or release continuity. Explain the choice
and tradeoff through the user's journey; implementation belongs with the relevant
specialist. These are design obligations to verify, not claims about every SDK.

## Bound context and preserve useful state

Distinguish persisted conversation events, selected model context, reusable input
caches and long-term memory. Summarising or limiting model input does not erase
stored history. Verify where a limit acts: database retrieval, returned events or
the outgoing model request. Preserve required facts and complete tool exchanges;
a compaction trigger is not a hard bound on the next tool response. Cache choices
need measured reuse, owner scope, freshness, expiry and independent deletion.

Bound query work and data before materialisation, then bound the complete payload
sent to the model. A small preview does not justify loading an unbounded result
first. Store full results durably when downloads must survive worker replacement;
authorise retrieval and specify expiry. A URI or local path is not an access grant.
Validate meaning and completeness separately from a structured response's shape.

Choose an explicit same-conversation policy: serialize, queue, reject overlap or
resolve conflicts. Multiple workers need shared enforcement; a lease requires a
version or fencing check that prevents an old owner from committing protected
writes. Persistent events alone do not coordinate whole turns. Reconnecting to
observe existing work is distinct from submitting it again.

For asynchronous persistence or memory ingestion, freeze the accepted batch and
its identity before sending it; advance a cursor only after confirmed completion.
New input belongs to another batch. Account for pending and in-flight data, and
make required terminal processing finish before source expiry. A crash-durable
acknowledgement needs a durable record before it is sent.

## Specify the browser contract independently of hosting

Choose completed JSON or incremental events according to user benefit. A tool
card can display a completed JSON result; streaming earns its extra state and
failure handling when progressive delivery matters. A gateway can preserve this
contract while execution moves between local and remote runtimes.

Define application-owned output schemas independently from tool inputs. Give
messages and tool calls stable identities; correlate results to exact calls,
including simultaneous calls to the same tool. Specify how deltas, aggregates,
duplicate events and ordering affect the displayed result. Keep a provisional
preview distinct from the accepted answer and verified business-operation status.
An HTTP success or renderer completion does not override a late execution error.

Authorise send, history, reconnect, cancel, result and delete operations. Enforce
the same caller checks on alternate backend routes. Test
actual provider events, gateway translation, forwarding and browser rendering:
an SSE connection alone does not prove incremental delivery. Bound body bytes,
events and retained client state, and define slow-consumer/backpressure behavior.
Continuous input also needs a policy for disposable versus non-discardable data.

## Account for work through completion and cancellation

Include admission waits, state access and response-body consumption in the total
deadline. Fit dependency timeouts inside it and reserve separate cleanup time.
Cancel owned tasks and close streams, while retaining capacity and usage charges
for threads or remote work that may still run. Keep recovery possible after the
interactive budget ends.

Distinguish parallel branches within a request from concurrency across requests.
Declare required/optional results, sibling cancellation and consistency when
several reads must describe the same snapshot. Unavailable optional data remains
unavailable. Choose in-process adapters or separate services based on measured
latency, independent scaling, isolation and permissions. For implementation, check
that blocking I/O cannot stall the event loop and bound any worker offload.

Measure latency, throughput, availability and cost per successful task separately.
Compare equivalent workloads, quality and failed observations with cold/warm/cache
conditions recorded. An optimisation that truncates required output fails the
task. More application replicas do not shorten a remote model generation.

## Preserve contracts through startup and release

Budget active, starting and draining instances, per-worker clients/pools and
downstream quotas together. Requested capacity must become ready before it helps;
replica count alone does not prove failure-domain resilience. Give readiness,
liveness and graceful shutdown separate responsibilities. A shared dependency
outage should not trigger restarts that cannot repair it.

Record the actual serving entrypoint, configured application, immutable release
and effective routing. Verify required settings and packaged modules reach that
path. Rehearse session-schema migration, mixed-version operation and rollback
against persisted state, queued jobs and previous external effects. Define
candidate acceptance and rollback thresholds before a staged release; a traffic
split alone does not produce comparable samples. Drain accepted work within a
bound before closing its dependencies, then verify temporary capacity cleanup.
