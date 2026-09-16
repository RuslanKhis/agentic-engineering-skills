# Token budgets and admission

Read when enforcing cumulative usage, sharing quotas, or adapting model selection. Outcome: new work is admitted against the appropriate scopes and already-spent usage remains visible even after a stop.

## Choose an honest contract

- A single-process demonstration can check current allowance before work and increment counters after responses. Label it post-response accounting: an in-flight response can overshoot, restart loses in-memory state, and concurrent reads followed by increments are not atomic admission.
- A service with concurrent requests or multiple instances needs shared, atomic reservation and settlement if it promises admission limits. Replacing a dictionary with Redis or Firestore does not itself make several scope checks atomic.

Derive tenant/user/session from authenticated application context and verify their relationship. Namespace keys by tenant, user, session and defined accounting period. Bind stored session ownership so another tenant cannot reuse it. Reuse session state across turns; avoid request-local runtime construction that resets cumulative quotas. Define day/month boundaries and expiry explicitly.

For a production service, add request/token rate, concurrent-work and queue-capacity limits independently of cumulative budgets. A valid reservation does not make an unbounded burst or queue acceptable. Follow [serving and lifecycle](serving-and-lifecycle.md) for admission order, replica scope, cancellation and capacity release; these service controls are production work, not supplied by the local guard.

## Reservation protocol for production

Implement against the target's chosen transactional store; this protocol is a design requirement, not a bundled distributed service.

1. Assign a trusted request ID and canonical reservation parameters. Reusing an ID with different identity, policy or allowance is a conflict.
2. Atomically inspect and reserve all required session/user/tenant allowances. Either every scope reserves or none does. Test competing admissions with capacity for only one.
3. Bind bounded model calls, output settings and time to the reservation. Estimate conservatively using input/context size, output/reasoning behaviour and maximum attempts. A token reserve is not a guaranteed currency cap.
4. Settle completed response usage exactly once using a stable response/attempt identity. Release unused capacity once; record overruns in every affected scope. Cancellation and output rejection do not erase already-incurred spend.
5. Keep uncertain usage conservative until reconciliation. Define reservation expiry, crashes, late reports and duplicate settlement; expiring a reservation cannot assume remote work cost nothing. Test these recovery paths with the actual store before claiming durability.

Define the production store-failure contract explicitly. If strict admission cannot establish valid control state or a reservation, refuse new expensive work with a static response; an unreachable store or malformed policy must not silently become zero spend or unlimited allowance. If settlement fails after work starts, preserve the reservation and known usage for reconciliation instead of releasing all capacity. Test unavailable, timed-out and malformed state before dispatch, then settlement failure after a completed response. The companion does not implement this recovery service.

Output-token limits bound one response, not all input/context tokens, retries, tool costs or total spend. Streaming usage may be cumulative snapshots. Detect the adapter's semantics and aggregate completed responses once; avoid adding reasoning to a total that already includes it. Prefer provider totals where reliable and explicitly record a conservative fallback when metadata is missing. The companion's zero-for-missing behaviour is a known limitation, not a recommended production policy.

## Degradation

Keep models and thresholds configurable. Select a policy before admitting new work and enforce a kill switch at every relevant invocation/expensive-operation boundary. Mid-flight changes need a documented consistency policy. Reduce optional work, choose a suitable lower-cost model or lower output allowance, then refuse new work with a static message. Validate quality as well as expenditure; a model named `cheaper_model` may cost more for a particular input/output mix.

Assert the actual endpoint/model and serialised generation settings with an offline SDK transport double. A logged `ModelDecision` does not prove the runner used it. Preserve a smaller configured output limit when applying a maximum; test smaller, unset and excessive values. Rechecking admission on an existing runner does not reconfigure that runner: rebuild or explicitly apply the chosen settings according to the application contract, then test a second invocation after the policy changes. The companion's `run_with_existing_runner()` rechecks the kill switch but does not apply a newly chosen model to its supplied runner.

Keep app feature controls separate from billing infrastructure authority. Use [cost controls](cost-controls.md) if cloud notifications drive policy. Pricing, model lifecycle and endpoint availability require current official verification before a new live campaign; historical model IDs are evidence, not defaults for new projects.

Acceptance tests: exhausted scope prevents any model call; two turns accumulate; tenant/user boundaries hold; session overrun still charges user and tenant; user overrun still charges tenant; repeated/cumulative usage is counted once; missing usage remains explicit; reservations race safely, settle once and recover after restart if implemented. For production admission, store failures and saturated capacity must produce zero model dispatch; use fake clocks and deterministic capacity, not live-model load. Run the served application path, not only store methods.
