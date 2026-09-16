# Memory Bank and privacy

Use this reference for semantic-memory eligibility, writes, recall, expiry, correction or personal-state erasure.
First locate the target project's memory tools, gateway, ledger, provider adapter and deletion worker; preserve its chosen services.

## Decide what the value controls

- Keep current permissions and transactional facts in their owning systems. Semantic memory may personalise an answer but grants no authority.
- Put an exact setting that changes product behaviour in a deterministic profile; distinguish changing this answer from updating the setting.
- Establish the smallest useful topic allowlist, candidate size and retention. A demonstration's topic names or lifetimes are examples, not portable defaults.
- Treat a request to forget as a correction or erasure action, not eligible input for new memory generation.

## Trace eligibility into the actual write

1. Identify the application consent signal and how authenticated context carries it to the write boundary.
2. Keep consent outside model-selected arguments. Include it in retry identity when it changes the meaning of an otherwise identical request.
3. Distinguish an instruction to the model to recognise an explicit remember request from deterministic application enforcement.
4. Verify allowed topics and bounded candidate content before staging; apply required transformations before any persistence or generation.
5. Submit the smallest useful protected fact or eligible event range, rather than a full session or arbitrary tool payload.
6. Inspect callback timing and temporary state behaviour under sequential and parallel tool calls and the selected session adapter.
7. Trace the candidate through ledger claim, provider submission and outcome recording; a returned candidate ID alone proves none of those steps.

If the task needs consent, make refusal observable as zero write attempts at the actual gateway boundary.
After-tool or final-output screening can fail after a side effect; a blocked response cannot establish that no write happened.

### Actual ADK handoff and cardinality

Use the trusted context paths and Runner assembly in
[integration-recipes.md](integration-recipes.md). Derive a candidate identity
from application, subject, invocation, function-call ID and topic; validate the
topic/value and require the IDs before staging. Recheck consent in the callback,
acquire the erasure/activity guard before claiming the candidate, and clear
temporary state in `finally` even on failure. Preserve the target's injected
services rather than coupling it to another API module's global singleton.

Parallel ADK event merging can serialise a staged dataclass into a dictionary.
Validate/reconstruct the candidate at the callback boundary and test the real
Runner/session adapter with a serialisation round trip. The source's parallel
case is a ticket tool plus one remember tool. A single `temp:memory_candidate`
slot is not a multi-candidate queue: if the target permits two remember calls
in one batch, implement and test per-call candidates or a durable outbox.

### Version-scoped provider request contract

The source's Vertex SDK sends one protected event through
`direct_contents_source`, exact `scope={"app_name": ..., "user_id": ...}` and
asynchronous generation. The meaningful configuration shape is:

```python
def generation_policy(topic, policy_version):
    return {
        "wait_for_completion": False,
        "allowed_topics": [{"custom_memory_topic_label": topic}],
        "metadata": {
            "application_topic": {"string_value": topic},
            "application_policy_version": {"string_value": policy_version},
        },
        "metadata_merge_strategy": "REQUIRE_EXACT_MATCH",
        "disable_memory_revisions": True,
    }
```

These metadata key names are illustrative: configure submission and recall to
use the same target-owned schema. Typed metadata values and merge constraints
are consistency controls, not consent or authorisation. Validate request bodies
with the installed SDK's actual models, not a dictionary-accepting fake.
Inspect retries and timeout units: this baseline's HTTP options use milliseconds,
whereas GAPIC timeout arguments use seconds. Its public LRO poller is
`MemoryBankServiceAsyncClient.get_operation` with `GetOperationRequest`.
Validate handle scope and retry policy on both initial and recovery polling;
do not assume every source path already performs the erasure sink's strict check.

## Reconcile asynchronous generation

| Outcome | What it establishes |
| --- | --- |
| Candidate staged | Eligible content exists in current application state; durability is still unknown |
| Accepted | A durable job or provider operation was accepted; specify which |
| Completed | Generation succeeded; it may have produced no useful fact |
| Ready | An authorised read retrieves the intended fact, or a verified provider guarantee establishes equivalent readiness |
| Indeterminate | The application cannot establish the outcome and must reconcile before retrying |

- Inspect implicit SDK retries, request deadlines and long-running-operation handling for the installed version.
- Persist the provider operation identity when available, validate its configured resource scope, and poll through a supported API.
- Reconcile an ambiguous timeout before resubmission. A stale claim without a handle is unresolved, not evidence of no write.
- Keep pending and indeterminate records discoverable for recovery and deletion; expiry must not silently erase unresolved work.
- Avoid claiming exactly-once generation from application deduplication or claiming readiness from completion alone.

When crash recovery of eligible content is required, use a durable outbox containing the protected payload or a durable reference to it.
An event-range design needs separate scan and completion cursors: record the job atomically with scan progress and advance completion only for settled ranges.
A scanner must revisit completed invocations missed before handoff; callbacks can run before the entire invocation is persisted.
Treat this as a production requirement to implement or report, not a property of any ledger or callback by name.

**Production addition — atomic late-handle bookkeeping.** A provider handle can
arrive after a stale claim was marked indeterminate. Preserve a valid late
handle without claiming success or regressing a settled status. Compare/update
handle, status, discovery index and retention atomically; reject conflicting
handles and keep uncertain records discoverable. Test both arrival/reconciler
orderings, completion racing attachment and a crash at the handoff.

The depth review reproduced two current-source failures offline: local
attachment drops a late handle after `mark_indeterminate`; Redis attachment's
read/modify/write can overwrite a newer indeterminate status with stale pending
state. The second used a controlled storage interleaving, not a live Redis test.
An outbox alone does not fix those ledger transitions. Treat this as an unresolved
source limitation; do not copy that attachment implementation as a safe recipe.

## Validate recall and retention

1. Derive exact application and subject scope from trusted context; an empty result stays within that scope.
2. Bound query length, total deadline, provider results and the final serialised response, including transformations that can expand text.
3. Validate returned resource identity, exact scope, approved topic, policy version and required time fields before model use.
4. If retrieval omits required expiry, fetch only an already-validated locator and revalidate the fetched identity, scope and retention fields.
5. Reject missing or expired required metadata; optional display fields may be omitted without inventing provenance.
6. Screen the accepted text and project only the fields the task needs; check failure logs for query or fact leakage.
7. Separate provider update time from the observation time or original source provenance of the underlying claim.

Determine fact TTL and revision TTL separately from the installed API's schema; constructor wiring does not configure either.
For Memory Bank APIs where request `ttl` controls revisions, verify fact lifetime at instance/resource level instead.
If revisions are disabled, say so. If enabled, include superseded values in access, retention and erasure design.
A built-in retriever is suitable only if its actual metadata, scope, logging and protection behaviour meets these requirements.

For the inspected ADK 2.8.0 adapter, `MemoryEntry` has metadata-capable fields,
but `VertexAiMemoryBankService.search_memory` populates only author, content and
timestamp. Inspect the conversion code, not just the model schema, before
depending on scope/expiry/topic/policy metadata. The inspected malformed-result
path also logs the raw retrieved object and exception chain. Test synthetic
canaries at that actual adapter/logging boundary; model-input screening cannot
restore dropped provenance or redact an earlier framework log. A raw provider
read can preserve the fields needed by policy, as the source does; other SDK
versions need their own inspection rather than a blanket ban on built-ins.

Resource spelling is another trap: the provider may return the configured
project ID or its numeric project number. Build exact allowed parent names
from independently verified configuration, retaining the same region/engine.
Accept only valid child paths beneath those parents. Revalidate after hydration
and before polling/deleting; never drop the project component or accept arbitrary
numeric projects to make a mismatch disappear. An unverified alias fails closed.

For the source's provider baseline, fact lifetime is configured at
`contextSpec.memoryBankConfig.ttlConfig.defaultTtl` (SDK
`ttl_config.default_ttl`); generation `ttl` controls revision lifetime. The lab
provisioning body sets a fixed 24 hours and disables revisions. Its
`MEMORY_TTL_SECONDS` setting alone does not update that resource. Trace every
retention setting through provisioning/update and readback, then verify stored
`expire_time`. Choose the target's retention deliberately and test configuration
drift. Revision-enabled correction/erasure remains additional production work.

## Coordinate erasure with writes and replay

1. Inventory the subject's active data and derivatives: profile, sessions, memories, run responses and any enabled analytics, documents or evaluation stores.
2. Define the implemented erasure scope and exclusions. Shared authoritative records require their own policy; an `ALL` label does not prove universal deletion.
3. Authenticate the owner and choose when new activity becomes blocked. Inspect the actual state mutation, not only a pending status response.
4. If immediate blocking at acceptance is required, establish the owner block atomically with acceptance; a worker-stage block is a narrower guarantee.
5. Acquire renewable worker ownership, drain active work and prevent new writes during deletion. On failure, retain the block and recovery evidence.
6. Settle the owner's known generation operations first. An uncertain write without a recoverable handle prevents a conclusive erasure result.
7. Enumerate and verify exact-scope records, delete matching resources, settle deletion operations and verify absence within explicit bounds.
8. Similarity-search emptiness is insufficient proof of absence. On retry, recheck prior successes that delayed writes could have invalidated.
9. Keep content-free replay tombstones for the original retry window so an erased request receives a gone outcome rather than re-executing.
10. Preserve the original expiry horizon; erasure must not restart retry retention. Prevent old sessions or restored derivatives from recreating erased content.
11. Report deleted, pending expiry, retained exception and failed sinks according to actual evidence, with a separate overall request status if needed.

Fence final publication too. A worker can lose its lease after every sink has
returned but before it marks success. The source's Redis completion path uses
one transaction equivalent to:

```text
require current claim == this worker's claim
require request.owner == selected owner and request.status == PROCESSING
write COMPLETED with operational-record retention
remove pending entry, worker claim and owner admission block
```

If the check fails, do not publish completion or unblock new activity. Test lease
loss between the final sink and this transaction. This is an implemented
application-store mechanism with Redis test coverage in the source, not proof
that an already-dispatched provider request was cancelled or that latest hosted
erasure acceptance passed.

Application deletion does not establish immediate physical removal from provider retention systems or backups.
Whole-environment teardown is not evidence that the scoped user-erasure workflow preserves another user's data.

## Validate completion at the claimed boundary

Use synthetic owner and control-owner fixtures. Inspect existing evidence first; execute only validation within the authorised task scope.

| Case | Required observation |
| --- | --- |
| Consent denied or invalid topic | No gateway write; safe bounded result |
| Consented sequential and parallel tools | Real candidate reaches ledger and gateway under the correct owner |
| Submission timeout or lost response | Known operation reconciled; unknown outcome retained without blind duplicate write |
| Wrong scope, missing expiry or expired fact | No unauthorised or unverified fact reaches model context |
| Successful generation and fresh recall | Completion and intended fact observed separately |
| Restart or second replica | Recall and relevant recovery state survive the claimed deployment boundary |
| Erasure with active or uncertain write | Ordering and admission policy hold; incomplete state is not published as complete |
| Erasure repeat, delayed replay and control owner | No resurrection; repeat is safe; unrelated scope remains intact |

Label cloud-client doubles as offline evidence. Preserve stronger production requirements when an inspected implementation lacks them.
Record implemented, tested and still unverified outcomes separately; neither an aggregate test count nor resource cleanup supplies missing hosted acceptance.
