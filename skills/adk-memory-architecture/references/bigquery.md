# Expose structured records through narrow BigQuery tools

Use this reference when an agent needs scoped structured facts from BigQuery. Keep conversation continuity in the target's session service. Use the owning transactional API for actions and for current-state answers whose consistency requirements a warehouse copy cannot meet.

## 1. Decide what the data can answer

- Establish the requested mode: inspect and report for a review; implement the requested interface for a change; run only authorised checks for validation. Schema, IAM and live query changes are separate actions from drafting a design.
- Identify the system of record, ingestion lag contract, permitted question types and required answer freshness. Distinguish dated history, replica state and authoritative current state before choosing the tool.
- Inspect the installed ADK/BigQuery interfaces, configuration validation, client lifecycle, domain schema, existing query layer and error contract. Preserve the target's supported SDK conventions and domain status names; example ticket fields are not a required schema.
- Determine what every timestamp proves. `MAX(source_synced_at)` means the newest observed row sync; it does not prove all updates arrived, all rows are equally recent or missing records do not exist.
- Use a completeness watermark only when ingestion guarantees that all relevant updates through that point have been incorporated. Otherwise expose a clearly named observation such as `latest_row_synced_at` and leave completeness unknown. Compare a valid watermark with the question's allowed delay.
- Align the agent instruction and public result labels with that contract. A label such as `fresh` based only on row age must not become “complete current state”. Route stricter questions to the owning API or explain the uncertainty.

Complete the decision with the supported questions, ownership mapping and explicit freshness/completeness contract.

## 2. Inspect and enforce trusted scope

- Resolve authenticated subject to the target's trusted tenant/customer or equivalent domain keys. Keep model-selected identity and arbitrary SQL out of a narrow business tool's schema.
- Use fixed application-owned SQL or the target's existing constrained query interface. Bind values as query parameters; select table/view identifiers only from validated trusted configuration because parameters do not replace identifiers.
- Apply all required ownership predicates on every query, including lookups by a remembered record ID. A high-entropy locator and a previous access decision do not grant current access.
- Trace the serving view, source dataset authorisation and workload grants independently. View DDL alone does not authorise the view or configure its readers.
- Where authorised views fit the target, authorise the serving view to read source data and give the workload only its required serving access and query-job permission. Separate analytics writer access from record reader access.
- Retain application predicates when many users share one workload identity. A row policy based on `SESSION_USER()` normally identifies the job's workload, not the signed-in end user.
- After migrations, replacement or backfill, verify effective view grants and row controls using the serving identity. Do not infer them from an operator's successful query.

Complete this phase when each identity boundary is enforced in code or effective data access controls and can be tested separately.

A typical authorised-view topology is:

```text
source dataset access entry:
  view: {projectId: serving_project, datasetId: serving_dataset, tableId: serving_view}
serving workload:
  read permitted serving data + create query jobs in the selected query project
analytics workload (if enabled):
  write only the separate analytics destination
```

DDL and these access entries are different mutations. Preserve unrelated
existing ACL entries and use the supported concurrency precondition instead of
uploading a stale replacement ACL. Check region compatibility and the full view
identity. After create, replacement and repeat, test serving-view read succeeds,
protected-source read/mutation and view redefinition are denied where outside
the role, unrelated ACLs remain, and analytics grants do not widen source access.
These provider checks need approved live scope; a mocked DDL test proves less.

## 3. Implement a bounded result contract

1. Map the source lifecycle deliberately; validate status/category values and timestamp types rather than treating every non-closed state as open. Preserve target domain terminology.
2. Project only needed typed fields. Free-text subjects, notes and provider payloads require an explicit purpose and content-protection path before model exposure; authorised SQL can still return hostile or sensitive text.
3. Define distinct success, unavailable and unknown-freshness outcomes. A backend failure with an empty list is not evidence that the caller has no records. Keep provider exceptions, query values and client objects out of public results.
4. Define a trusted row limit, deterministic ordering and tie-breaker. If results can be truncated, expose pagination or `may_have_more` as appropriate; do not present the limited rows as a complete count. Bind continuation tokens to the same authenticated scope.
5. Bound transferred rows/bytes and the complete serialised result. A SQL `LIMIT` bounds selected rows, not scan cost or payload bytes.
6. Apply the configured query-byte cap to the actual BigQuery job and choose explicit query project/location. Keep business identifiers out of diagnostic SQL, job labels and error text.
7. Screen the projected result wherever the target's content policy requires it. Publish a complete protected result or a safe failure; preserve typed validation and authorisation independently of screening.

## 4. Choose the required execution guarantee

For every runtime, specify submission/result timeouts, retry behaviour, cancellation behaviour and the work budget. Trace synchronous work behind async wrappers: cancelling the caller does not kill a worker thread or prove the server-side query stopped.

Where the production requirement includes bounded admission and reconciliation of uncertain work, implement this extension in the runtime query layer:

1. Own and close the client per worker process using the target's workload authentication. Admit work through a bounded queue/pool and carry one monotonic deadline across queueing, directory lookup, query work and projection.
2. When a cost estimate is required, dry-run the exact SQL, parameters and location. Reject an unavailable or excessive estimate. Retain the execution byte cap because an estimate does not reserve capacity or replace it.
3. Generate an opaque job ID and durably record job project/location, query identity and reconciliation deadline before real submission. If recording fails, do not submit.
4. Bound submission, polling and result-page requests by the remaining deadline. Configure SDK retries deliberately so lost responses cannot trigger untracked replacement jobs.
5. On timeout, caller cancellation or uncertain submission, stop releasing results and reconcile the recorded job. Request cancellation where appropriate, preserve caller cancellation, and have a durable worker verify terminal state or a clearly recorded unresolved outcome.

A successful cancellation request is not terminal-state evidence. A lost submission response does not prove that no job exists. Setup-script journalling does not establish those guarantees in a separate runtime executor; inspect both paths before making the claim.

### Job completion is not the end of result I/O

Treat submit → job wait → page fetch → validation/projection → public release
as separate stages under the same remaining deadline. `job.result(timeout=...)`
can return a lazy iterator whose later fetches still perform network I/O.
Bound real page reads and final bytes, handle caller cancellation and preserve
the query identity. A failure after one page must not become a successful
partial or empty answer unless that is the explicit public contract.

Use a lazy double that yields one page then blocks or fails. Assert bounded
safe failure, no partial release and no replacement query. The source contract
test returns an eager list, so it does not establish those guarantees; its
runtime iterates results outside the inner job-result timeout handler.

### Optional pagination contract

For a target that needs more than one bounded page, use a stable final order,
such as `ORDER BY updated_at DESC, record_id ASC`. Apply it to the final query
result, not only an inner CTE. Fetch N+1 rows and return N to derive `has_more`,
or expose a conservative `may_have_more` when only N were requested. An example
keyset condition for that order is:

```sql
updated_at < @last_updated_at
OR (updated_at = @last_updated_at AND record_id > @last_record_id)
```

Combine it with the same trusted ownership/filter predicates. Bind a
tamper-evident continuation token to owner, query/filter/policy version, last
sort tuple and expiry; reauthorise every page. Define whether pages share a
fixed result/snapshot or are best-effort current reads. Keyset pagination alone
does not prevent movement when a row's sort key changes. Test equal timestamps,
N/N+1 boundaries, changed rows, forged tokens and cross-owner reuse.

This is an extension: the source limits an inner query, has no final stable
ordering contract or pagination marker, and must not be described as returning
all matching records.

## 5. Verify ingestion and the view contract

- If the serving table represents current rows, specify its business key, deduplication rule and source-version ordering. Prevent an older late-arriving event from replacing a newer state.
- Define deletes, missing rows, schema changes and backfills explicitly. Advance a completeness watermark only after its coverage contract is satisfied, including the relevant partitions and scope.
- Keep append-only analytical history separate from a current-row serving table where the domain needs both. Set purpose, partitioning, retention and access controls independently.
- Treat synthetic fixture merges as fixture setup, not proof of a production replication engine. Test importer guarantees with duplicate, out-of-order and missing updates.
- Treat agent analytics as a separate privacy route. Inventory the complete exporter schema and actual sinks, minimise fields and test synthetic sensitive-data canaries; disabling a content formatter alone does not prove whole-row minimisation.

### Analytics needs a startup, schema and loss contract

Keep analytics explicitly opt-in. Against the installed plugin, verify an
event allowlist, excluded content/content-parts/attributes, multimodal and
session-metadata switches, and whether it auto-creates or upgrades schema/views.
The source disables broad content capture and schema/view mutation; that is a
configuration contract, not proof about every emitted row. Keep schema setup
under operator authority and prevent request metadata from widening capture.

Register protection before exporters at the actual startup boundary. Capture
complete emitted rows/objects under success, failure and exception paths;
inspect IDs, attributes and offloaded content as well as text. Exercise a full
queue and shutdown timeout, and report lost/undelivered events. Missing metrics
are not a verified zero-drop count, and missing telemetry is not evidence that
no tool ran. See [integration-recipes.md](integration-recipes.md) for event
projection and client ownership; the source's configuration-only tests do not
establish a full telemetry privacy guarantee.

## 6. Validate and report

- Assert trusted parameter binding and cross-tenant/customer isolation, including a model request naming another user and a stored locator whose owner changed.
- Test empty success versus backend failure, stale/missing/future timestamps, recent-row-plus-missing-update cases, unknown lifecycle values and oversized fields. Assert that the answer respects the completeness contract.
- Test deterministic limiting/pagination and actual byte-cap configuration. For a durable executor, exercise lost submission, caller cancellation, timeout, failed cancellation and restart reconciliation without duplicate jobs.
- Verify the serving identity can query the intended view and cannot directly read protected source data or administer datasets when those permissions are outside its role.
- Use offline tests for deterministic failures and authorised bounded live checks for effective IAM/provider behaviour. Report PASS, FAIL, NOT RUN or UNKNOWN against each selected guarantee.

Complete the work with the tool/data contract, changed components, validation evidence and unresolved conditions. The source companion implements fixed scoped SQL, a row limit, projection, per-call timeouts, an execution byte cap and best-effort timeout cancellation. Its row-age label does not establish completeness; its runtime does not implement dry runs, durable job reconciliation, bounded admission or a complete result-byte budget. Treat those as production work where required, not verified inherited features.
