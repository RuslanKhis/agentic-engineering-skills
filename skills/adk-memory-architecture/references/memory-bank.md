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
