# Sessions and state

Use this reference for session persistence, state updates, ownership, context retention, request replay or concurrent turns.
Adapt the workflow to the target project's existing framework and boundaries; a named SDK class is not a required architecture.

## Find the actual serving boundary

1. Trace one request from its public entry point through authentication, scope mapping, session access, Runner and release.
2. Identify the selected session backend and whether its state survives a process restart and a second replica.
3. Locate startup and shutdown hooks. Establish where protection clients, tool plugins, reconciliation and telemetry are initialised.
4. Check the invoked deployment entry point actually executes those hooks. A discoverable agent or constructed App may bypass them.
5. Record the exact adapter versions and supported constructor shape before adapting examples.

Finish with a compact boundary map naming the owner of each control and any path that bypasses it.
Passing an App to Runner preserves registered plugins; it does not initialise missing application controls.
Register tool-result protection before observers that can export those results, and close owned clients on failed startup as well as shutdown.
For concrete assembly, injected context fields, plugin return semantics,
public-event projection and rotation-safe replay, read
[integration-recipes.md](integration-recipes.md).

## Resolve identity and session ownership

- Derive a stable internal subject from verified issuer, tenant and provider subject; keep workload identity separate.
- Qualify session operations by application, verified subject and locator. Reauthorise every exposed history, state, export, cancel or delete route.
- If an application thread maps to a remote session, qualify the mapping by owner, thread and runtime resource.
- Let the selected service create new locators. An unknown supplied locator must not silently create caller-chosen state.
- Validate the selected adapter's owner checks and returned object; avoid treating a shared workload permission as end-user authorisation.
- Map tested absent and foreign-owner outcomes to the same public not-found result while preserving operational failures separately.
- Inspect broad exception handlers: mapping every `ValueError` to not found can conceal unrelated SDK or configuration failures.

Done means the owner predicate is demonstrable at each exposed route; a hidden item in the UI is insufficient evidence.

## Put each value in the right state

| Value | Decision |
| --- | --- |
| One-invocation intermediate | Use the framework's temporary scope; verify it does not become durable history |
| Conversation workflow state | Persist through supported state deltas, not mutation of a detached session dictionary |
| Exact operational setting | Use an authoritative profile or supported deterministic user-state store |
| Semantic preference | Use the memory workflow only when its eligibility and read controls apply |
| Identity, permission or secret locator | Keep it in trusted server context, outside model arguments and public state |

Verify state-prefix semantics against the actual backend. A prefix is a namespace, not encryption or a client-write prohibition.
Protect a value before writing state, events, artefacts or queues; screening the later tool response does not undo an earlier write.
For ADK, inspect `ToolContext.state`, callback state, `output_key` or explicit event deltas as applicable to the existing code.

## Separate retained history from active context

- Choose session expiry explicitly and verify the stored resource; service defaults are not the product's retention decision.
- Give memory facts, memory revisions and public replay records separate retention rules.
- Stamp protected history with a policy version and reject incompatible or unstamped restoration unless an explicit migration path handles it.
- Treat a version stamp as a compatibility check, not proof that historical raw data was transformed or deleted.
- If long conversations are in scope, locate context counting, compaction or retrieval and its continuation tests; persistence alone provides none.
- Preserve authoritative locators and workflow decisions across compaction while checking current permission when they are used.

## Coordinate writers and retries independently

1. Establish one active session writer across replicas through a queue, store capability or renewable lease.
2. For leases, inspect acquisition, renewal, expiry, owner-checked release and downstream enforcement after ownership loss.
3. Exercise an invocation longer than the lease. A successful expiry test that admits a second writer can reveal a safety gap.
4. A privacy activity heartbeat permits ordinary activities to coexist; it does not provide session mutual exclusion.
5. Qualify an idempotency record by owner and a canonical request including policy-relevant inputs such as consent.
6. Reuse the completed public response for an equivalent retry. Reconcile pending or indeterminate work before re-executing side effects.
7. Distinguish completed-response replay from streaming reconnect, which needs an ordered public stream and attachment to the existing run.

An expiring lock with compare-and-delete release is an incomplete long-running writer guarantee unless work is bounded safely below expiry.
Treat a field named `fencing_token` as evidence only when the relevant downstream writes validate current ownership.

## Validate the selected claim

Use existing tests for review; for authorised implementation work, add focused cases at the actual route and adapter seams.

| Case | Required observation |
| --- | --- |
| Rejected first message | No session creation or unapproved invocation |
| Owned, absent, foreign or malformed locator | Correct owner outcome without cross-owner content or unintended creation |
| Outage or unrelated SDK validation failure | Safe operational failure, distinguishable internally from absence |
| Restart or second replica | Required state actually persists; process-local fixtures are labelled accordingly |
| Long concurrent turns or lease loss | Stale writer cannot continue protected writes under an expired claim |
| Completed retry, uncertain retry or erased retry | Reuse, reconciliation or tombstone outcome; no unintended new invocation |
| Startup failure or shutdown | Required controls fail closed and owned clients are released |

Report the implemented control, supporting test boundary and remaining production requirement separately.
Record missing context management or lease renewal as gaps; do not infer them from a passing aggregate suite.

## Production extensions when the requirement calls for them

**Long conversations:** define a context budget and overflow rule independently
of transcript retention. Reserve required instructions, current request, exact
workflow state and function-call/result relationships; select protected summaries
or retrieved history for the remaining budget. Keep authoritative locators and
cited releases, but recheck permissions and pending approvals. Test a pending
action across compaction, process restart and a second replica. The companion
does not implement a compactor or prove these continuation cases.

**Remote runtime:** choose an actual remote SDK/API boundary instead of running
both a local Runner and a remote agent accidentally. Keep a durable mapping of
owner, application thread, remote resource and remote session. Verify every
history/list/attach/cancel route's owner filter; general resource IAM does not
prove end-user filtering. Authenticate the service hop and keep the browser
behind the application's gateway. This is a design extension, not the source
lab's hosted in-process Runner.

**Streaming reconnect:** persist only approved public events with run ID,
monotonic sequence/cursor and bounded retention. Reconnect attaches to that run
without executing its tools again. Test wrong owner, duplicate reconnect, expired
cursor, disconnected consumer and worker loss. Preserve completed-response and
erased-response semantics independently of the stream. The source's buffered
JSON/replay implementation does not provide this public event log.
