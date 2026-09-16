# Verify application and Cloud Run changes

Read when turning an application optimisation into an executable acceptance test,
planning a bounded provider experiment, or recovering its incomplete receipt.
Use [lifecycle.md](lifecycle.md) for authority and ownership and
[validation.md](validation.md) for the saved-event checker. Adapt the following
recipe to the target's workflow; it does not require the companion repository.

## Build an acceptance ladder

1. **Choose the claim and fixture.** Draw the actual dependency order: schema →
   authorised query → complete stored result → preview/format/export. Currency
   lookup can run independently when its inputs are already known. Use synthetic
   rows with unique keys and known totals. Verify that setup creates the columns,
   types and relationships requested by the application before any model test.
   A successful schema lookup against a local dictionary proves no database access.
2. **Exercise real orchestration offline.** Keep the actual exported `App`,
   Runner, session service, ADK `State`, tools and HTTP adapter. Replace model and
   provider transports with deterministic doubles before application import;
   inspect tests for constructors or callbacks that could still contact a provider.
   Have the model double emit correlated function calls, consume actual tool
   responses and finish with a complete answer. Record the expected dependency
   order, arguments, result values and state deltas. Include a terminal failure.
3. **Check the installed boundary.** Run the target's existing packaging checks
   outside its source directory where possible. Confirm prompt/resources and the
   selected agent are present; importing from a checkout can hide omitted package
   data or accidental package discovery. Keep the target's package manager and pins.
4. **Run only the approved live stage.** Verify provider results before dependent
   work. Read the complete stream, correlate invocation/tool-call IDs and require a
   complete answer after its prerequisite results. Assert currency values against
   the returned structured tool data, not a hard-coded historical exchange rate.
   Stop dependent stages on failure; run independent stages only if the existing
   scope and remaining allowance include them.
5. **Promote only the tested claim.** Record separate application, component,
   hosted, browser and cleanup verdicts. A standalone export pass does not prove
   the agent selected that export tool. A hosted schema profile does not prove
   hosted SQL permissions, exports, caching or nested agents.

Do not accept `is_final_response()` alone: the real ADK 2.8.0 nested-budget
contract also marks a content-free limit-error event as final. Check error fields,
required content, completion reason and the full stream. The optional
[ADK budget tests](../tests/test_part1_adk_budget.py) reproduce this and the child
generation limit below with real Runner/tool/session orchestration and model
doubles; they make no provider calls.

For preview/export acceptance, generate more rows than the preview limit, with a
deterministic order and exact expected values. Compare the full CSV's row count,
keys and values with the full result. Check that the preview remains bounded and
that successful export clears the exact local/state reference. Exercise two
distinct requests so a mutable last-result pointer cannot make both pass against
the same data. Durable or cross-instance retrieval requires its own replacement
test; a same-process CSV test cannot establish it.

The historical first full-tools run failed its combined answer while SQL, cache,
formatter and Skill-loading components passed. A later separately bounded run
verified real currency and complete CSV results. Preserve both outcomes; component
success never repairs the earlier integration verdict.

## Make the budget enforceable before dispatch

Choose limits from the workload and approved envelope. Historical test limits
are examples, not production defaults or monetary guarantees. Put the admission
check at a supported provider boundary below all relevant callers; a callback on
only the root agent can miss child requests. Preserve counters across recovery.

| Operation | Reservation and failure test |
| --- | --- |
| Model generation | Count root and nested logical calls plus actual SDK attempts. In the ADK 2.8.0 experiment, `max_llm_calls=1` still allowed the root's first call and two separate `AgentTool` child calls before blocking the next root call. Verify the aggregate counter rejects the next attempt before transport; provider event counts alone do not prove attempts. |
| Input/cache | Bound encoded request bytes including instructions, tools, current contents and the recorded cached prefix. A short request containing a cache ID is not a short effective input. Reject unknown cache references; retain pending cache creation before dispatch so a lost response cannot trigger another creation. Byte limits are not token estimates. |
| Output | Bound output tokens but test completion at that bound. `MAX_TOKENS` is a failure even when the text resembles a useful table. Choose a sufficient approved cap before execution; increasing it after failure changes the experiment. |
| Query/load | Reserve the planned job ID and location before submission; apply authorised resources, bytes-billed and independent result limits. Inspect both request retries and job retries, plus upload retries for fixture loads. Recover by the same job ID after a timeout; verify no second submission. |
| Export | Reserve count and encoded bytes before upload; retain unique object name and returned generation. Test create-only preconditions and refusal before provider contact when the allowance is exceeded. |
| HTTP tool | Count possible redirect requests and SDK retries, with connect/read/overall deadlines. Disable unnecessary redirects or validate each permitted destination; bounding hops alone does not enforce a destination allowlist. |
| Recovery | Bind the receipt to target, profile, owner and original start time. Resume cumulative counts and elapsed allowance; a fresh process must not reset either. Test expired and mismatched receipts without transport calls. |

The retained single-process harness used a reentrant lock around reservations and
writes, unique private temporary files, file flush/fsync and atomic replacement.
Concurrent SDK callbacks had previously raced on a shared temporary filename.
Test concurrent reservations against the exact final counter and persisted file;
atomic replacement alone does not prevent lost updates. A multi-process or
distributed deployment needs corresponding coordination. Use supported client
wrappers in reusable code; the historical private-SDK instrumentation is not a
portable implementation to copy.

## Turn reproduced failures into focused tests

| Failure observed in Part 1 | Test that changes the acceptance decision |
| --- | --- |
| Dict doubles hid unsupported `State.pop()` | Execute export through real ADK `State`/Runner; assert the persisted reference-clearing delta, not just an in-memory dict value. |
| Content-free events crashed the CLI | Include content-free progress, a real function call/response, multipart answer and a late error; assert rendering and failure propagation. |
| Provider failure became a plausible currency rate | Raise a transport/TLS exception; require explicit failure without a numeric rate and skip conversion. Use verified TLS for the successful path. |
| Partial fixture setup disagreed with schema tools | Run actual setup orchestration with SDK transports doubled; repeat exact rows, check relations, interrupt the second table load and recover without adopting foreign tables. |
| Setup probe replaced an existing object | Seed the old fixed probe name; require a unique create-only probe and generation-bound deletion while preserving the seeded object. |
| Budget/receipt recovery repeated paid work | Simulate accepted submission with a lost acknowledgement and an exhausted allowance; reconcile the same identity and keep model/query invocation counts unchanged. |

## Finish or recover cleanup independently

Record functional acceptance before cleanup. Verify recorded query/load jobs are
terminal before deleting their fixtures. An ownership marker alone is insufficient
for recursively deleting a bucket/dataset that now contains unexpected objects or
tables; stop for reconciliation and preserve unrelated contents.

Provide a cleanup-only path using the same receipt. Separate cleanup-read capacity
from paid invocation allowance; a cleanup retry must not rerun the application.
Keep primary failure and cleanup failure separately visible. Verify absence with
the owning service and exact identity: stale aggregated inventory may disagree,
while permission errors establish neither presence nor absence. Finish with
explicit active-resource, retention and unresolved-state outcomes.
