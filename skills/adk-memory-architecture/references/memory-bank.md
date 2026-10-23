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

### Native write and recall surfaces

The ADK surfaces the write and recall boundaries above sit on, read on
https://adk.dev/sessions/memory/ on 22 October 2026 (confirm against the
installed version; the adapter inspected for this reference is 2.8.0 and
Agents CLI scaffolds `google-adk>=2.12.0`):

- Writes: `await callback_context.add_session_to_memory()` sends the whole
  session; `await memory_service.add_events_to_memory(app_name=, user_id=,
  events=, session_id=, custom_metadata=)` appends a delta without
  re-ingesting the session. The delta form is the one this reference's
  "smallest useful protected fact or eligible event range" rule needs; the
  whole-session form submits everything the consent gate did not screen.
- Recall: `PreloadMemoryTool()` retrieves memories at the start of every turn
  and injects them into the instruction, so every request pays for recall and
  the scope check must run before the model sees anything; `LoadMemoryTool()`
  retrieves only when the model decides to call it, so a missed call is a
  missed fact and the query is model-chosen. The validation steps below apply
  to both; a built-in tool is acceptable only when its actual metadata and
  logging behaviour passes the "Validate recall and retention" checks.
- `InMemoryMemoryService` performs keyword matching and does not survive a
  restart; `VertexAiMemoryBankService` extracts facts with a model and needs
  the Agent Platform resource and identity described in
  [managed-deployment.md](managed-deployment.md). ADK 2.11.0 adds a SQLite
  memory service (`memory/_sqlite_memory_service.py`, selected with a
  `sqlite://` memory service URI; CHANGELOG 2.11.0, 9625b06, read
  2026-10-22), a local durable store for one process that is still keyword
  recall without extraction, consent or erasure; absent on the 2.8.0
  baseline.

The `cross-session-memory` recipe in `google/adk-recipes`
(`app/app_utils/memory_config.py`, `app/agent.py`, `app/fast_api_app.py`)
wires `PreloadMemoryTool` plus an `after_agent_callback` that calls
`add_session_to_memory`, and tests it with a Runner and a mock model (Agents
CLI 1.11.0, `google-agents-cli-adk-code` skill, `references/samples.md`, read
22 October 2026; vendor guidance). It demonstrates the wiring, not consent,
topic allowlists, erasure or the reconciliation table below; add those before
calling it a memory feature. When the project has `agents-cli-manifest.yaml`,
consult the installed `google-agents-cli-adk-code` skill
(`references/adk-python.md`, "Memory", or the `cross-session-memory` recipe);
if it is not installed, adk-engineer explains how to get it.

The long-horizon-harness recipe in the same repository shows the write-back
loop at production shape (google/adk-recipes be63596,
`core/python/long-horizon-harness/docs/memory.md` and `horizon/memory/`, read
2026-10-22; vendor sample, "not production use"): Memory Bank is its only
durable cross-session store; an `after_agent_callback` flushes the session
with `add_session_to_memory`, throttled per session (120 s cooldown, 50 per
session); a model-callable `memory(content, scope)` tool writes `user` or
`agent` facts under character limits (1375 and 2200), after an exact-text
dedup and a content-safety scan, because memory is replayed into later turns
and is therefore an untrusted-input boundary; a background "review fork" (a
restricted sibling agent on its own runner, fire-and-forget, never blocking
the reply) decides what is worth saving; a pre-compaction flush fires from the
events summariser so facts are saved before old turns are summarised away;
and a nightly pass calls Memory Bank `memories.generate` to consolidate a
structured profile (schema applied to the Agent Engine resource at provision
time) and to reconcile duplicates and contradictions, returning `created`,
`updated` and `deleted` counts. Its own honesty notes carry over: the forks
are best-effort and drained for about four seconds at shutdown, so a hard
kill loses that turn's write; dedup before the nightly pass is exact-text
only; the structured profile needs a Vertex Memory Bank engine with
generation enabled and no-ops on any other service. What the recipe does not
have is what this reference requires before the loop is a memory feature:
consent per topic, the reconciliation table below, erasure by label and
revision, and a test that a failed write is observable rather than silent.

The consolidation and revision semantics the loop relies on are Memory
Bank's own (Google Cloud, "Memory revisions", https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank/revisions, updated 2026-10-21, read 2026-10-23; vendor documentation, confirm against the current page): on `memories.generate`, new information creates a
memory when nothing in the same scope covers it, updates an existing memory
when the consolidation process judges the new information "duplicative,
complementary, or contradictory" to it, and deletes a memory the new
information invalidates; the same three outcomes are available directly
through `CreateMemory`, `UpdateMemory` and `DeleteMemory`. Revisions are on
by default and record every change from either path; the generate response
carries a `previous_revision` for each updated or deleted memory, and
`memories.rollback(name=..., target_revision_id=...)` restores that
revision, which is the rollback path for a poisoned fact. `revision_labels`
passed in the generate `config` label the revisions with the data source
that produced them, and `memories.revisions.list(name=..., config={"filter":
'labels.<key>="<value>"'})` finds them, which is the erasure-by-source path
the reconciliation table asks for. Disabling revisions
(`disable_memory_revisions`, below) gives up both paths; say so in the
design if it is chosen for cost. On 2.12.0 the generate request accepts
`allowed_topics`, `disable_consolidation`, `disable_memory_revisions`,
`metadata`, `metadata_merge_strategy`, `revision_expire_time`,
`revision_labels`, `revision_ttl`, `ttl` and `wait_for_completion` through
`custom_metadata` (installed package, `vertex_ai_memory_bank_service.py`,
read 2026-10-23), so labels and topics travel on `add_events_to_memory`
without a raw client. The gold set that proves the update and abstention
behaviour is structured by the five memory abilities in
[retrieval strategy](retrieval-strategy.md#measure-recall-on-a-gold-set-before-drafting).
Two rules from the security skill apply on the write side: events from an
invocation that read untrusted content (a fetched page, an inbound email, a
search result) are not written back except through the quarantined reader
path, and nothing in memory grants authority (an entitlement topic is never
an allowed topic). When an existing design already keeps a product setting
such as a delivery address in semantic memory rather than in a
deterministic profile field, keep it working under the newest-wins rule and
record the migration to a profile field as a decision; do not migrate inside
a fix.

### Minimal write-back sequence on 2.8.0

The sections below state the contracts; this is the smallest implementation
that meets them, with the accessor names read in the 2.8.0 source
(`agents/context.py`, `memory/base_memory_service.py`; source-verified, not
executed). One `Context` class backs tool and callback contexts and exposes
`user_id`, `session`, `invocation_id`, `function_call_id` (set for a tool
call), `custom_metadata` (the dict passed as `RunConfig.custom_metadata`),
`run_config`, `state`, and the memory methods `add_session_to_memory()`,
`add_events_to_memory()`, `add_memory()` and `search_memory()`.

1. Consent and scope enter as trusted context, never as model arguments: the
   verified user id is the Runner's `user_id`; a per-topic consent flag
   travels in `RunConfig.custom_metadata` or a profile row read at the
   invocation boundary.
2. A tool (or an after-turn judge) stages a candidate per `function_call_id`
   in `temp:` state with its topic; it does not write.
3. One `after_agent_callback` rechecks consent and scope, then writes the
   delta with `add_events_to_memory(app_name=, user_id=, events=, session_id=,
   custom_metadata=)` carrying the policy metadata; `add_session_to_memory`
   writes the whole session and is used only when every event is permitted.
4. Each write lands in a ledger as accepted, failed or indeterminate; an
   indeterminate write is reconciled by `search_memory` before any
   resubmission, and the callback never raises into the user's turn.
5. Recall is filtered in code after `search_memory`: foreign scope, topic,
   tombstone, expiry and size, because the provider returns what it has.
6. `BaseMemoryService` has no delete method in 2.8.0 nor in 2.12.0 (installed
   package, read 2026-10-23: `add_session_to_memory`, `add_events_to_memory`,
   `add_memory`, `search_memory` only), so forgetting
   and erasure write a tombstone the recall filter honours first and then
   delete through the provider's own API (for Memory Bank, the Agent Engine
   memories resource, which the erasure section below treats as a sink to
   settle and verify); `InMemoryMemoryService` is erased by removing the
   entries directly.

When several users share a subject (a site, an account, a customer), the
memory scope stays `(app_name, user_id)` and the subject id is a tag on the
fact and a filter at recall, never a scope of its own; a fact that every user
of the subject should see belongs in the owning record, written by its tool.
A test with two users on one subject proves the first user's preference never
surfaces for the second.

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
        "disable_memory_revisions": False,  # revisions stay on: rollback and label-scoped erasure need them
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
On a Spanner target, Spanner Queues are a ready-made outbox: send and acknowledge run inside ordinary read-write transactions, delivery is at-least-once under short renewable leases, and the acknowledgement is a `DELETE ... ASSERT_ROWS_MODIFIED 1` so a lost race surfaces instead of vanishing; they require the Enterprise or Enterprise Plus edition (Google's `spanner-basics` skill, read 21 October 2026; vendor guidance, confirm against current docs). The scan and completion cursors above still govern what the queue carries.

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
timestamp; on 2.12.0 it also fills `custom_metadata` from the memory's
metadata, with `author` always `user` and the fact as the content (installed
package, read 2026-10-23), so scope, topic and expiry are your own metadata
keys written at generation time, not provider fields. Inspect the conversion code, not just the model schema, before
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
On a relational session store those copies are concrete: the point-in-time and continuous-backup windows in [sessions-state.md](sessions-state.md) still hold erased rows, and an AlloyDB discrete backup "exists independently from its original cluster" and survives the cluster's deletion (https://docs.cloud.google.com/alloydb/docs/backup/overview). Report them as retention still running, with their expiry dates.
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
