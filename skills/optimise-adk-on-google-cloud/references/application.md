# Optimise the application path

Use this reference for tools, context, child interfaces, output and independent
I/O. Keep the existing business task and change the boundary supported by the
evidence. The source examples used ADK 2.8.0; verify the target's interfaces before
adapting a recipe.

## Remove an unnecessary remote adapter

Find whether a tool call provisions or wakes another service, builds a client
repeatedly or crosses a redundant HTTP boundary. An in-process adapter can remove
that hop while the database still executes remotely. Retain a remote boundary
when isolation, separate permissions, independent scaling or locality justify it.
Measure the adapter separately from query submission and execution.

Create a reusable client per worker process where its concurrency contract
permits. Close it in lifespan/shutdown. Lazy construction helps rare paths;
deferring work needed by every request only moves its cost. A synchronous SDK
inside `async def` still blocks. Use a native async API or bounded offload for
blocking I/O, with admission capacity tied to request concurrency and downstream
quotas. Cancelling an await does not necessarily cancel a thread or accepted job.

Moving code into the process also moves responsibility for policy. Derive caller
and tenant from trusted invocation context. Validate the requested operation and
resource immediately before execution. For SQL, one parsed read-only statement
is a useful restriction, but does not establish table/column authorisation or
cost bounds. Apply resource policy, parameterise values, dry-run the permitted
query, set bytes-billed and result limits, and retain the planned job identity
for ambiguous submissions. These are production controls to implement and test;
the companion's parser alone did not provide them.

Keep runtime read/query permissions separate from fixture creation and export
permissions. BigQuery job creation and dataset access are different grants.
Choose permissions for the actual operation and permitted dataset; avoid copying
a deployment identity's broader access into the agent.

## Disclose schema detail when needed

Give the agent a small catalogue of permitted tables and purposes. Retrieve
versioned details only for selected tables. Apply access policy before disclosure,
bound requested table count and encoded response size, and make an unknown name
an explicit outcome. Build or refresh metadata through a controlled process and
test drift against the deployed schema.

Do not invent columns to satisfy a question. A dataset without dates cannot
answer a quarter filter. Schema descriptions must match stored types; changing
the prompt does not convert floating-point money into decimal amounts. Use the
target's actual representation and explicit currency/conversion policy.

Validate that an unrelated schema is not returned and that requested, authorised
columns are present. A model's claim that it loaded schema is insufficient.

## Separate reasoning previews from complete results

Bound rows, columns, each cell and total encoded bytes **before** returning data
to the model. `to_dataframe().head(10)` still materialises the full result first.
Apply independent query/result-production limits before constructing the preview.
Reject non-finite numeric values and ragged rows in a structured handoff. Treat
column names and cell text as untrusted data, even inside JSON or XML tags.

Keep complete results in a durable store when later turns or another instance
must retrieve them. Issue an opaque result reference tied to the exact query,
tool call, owner/tenant and expiry. A mutable `latest_result` state field can
select an old or concurrent query accidentally. Bind formatting and export to the
specific successful result; skip downstream work when that result failed.

Local temporary files and Python globals are process/instance-local. A durable
session record does not make a file path durable. On Cloud Run, warm instances
and affinity do not guarantee that a later request finds that file. Test a change
of process/instance rather than only two calls in one process.

Authenticate downloads and recheck ownership, permitted columns and expiry.
`gs://` identifies an object; it is not a browser download grant. A signed URL is
a bearer credential and belongs outside model context where practical. Give
exports unique names, bounded retention and ownership-aware cleanup. Choose and
test a spreadsheet-formula policy for CSV, or use a suitable non-spreadsheet
format. Raw CSV is not automatically safe to open in a spreadsheet.

In ADK State, use supported assignment to create a state delta. Do not assume
every dictionary mutation method is supported. Test the persisted event/state
change through the actual Runner, not just a Python dictionary double.

## Match the child and output to the task

For simple retrieval, return the requested result directly; for analysis, keep
the reasoning and limitations needed to interpret it. Test both request classes.
Conciseness must preserve failures and uncertainty. Reject `MAX_TOKENS` or another
incomplete finish instead of counting a truncated table as a faster answer.

For a narrow formatter/validator, `include_contents="none"` excludes prior-turn
conversation contents. Current input, instructions, current-turn tool exchanges
and interpolated state can remain. Test with a distinctive old-history marker
and bounded current data; inspect the actual outgoing model request. Check that
the old marker is absent and current facts are present. Answer text alone is
weak evidence. Ensure the child is actually registered and receives this result.

Choose a compact `output_schema` when the caller needs machine-readable output.
Validate semantic/cross-field rules after generation. An advisory SQL review can
accept only with a candidate query and no errors, and reject with errors and no
candidate. Neither that schema nor a model's `is_valid=true` authorises execution.
Use deterministic control flow when the next operation depends on acceptance.

Preserve an existing `AgentTool` integration unless another boundary solves the
task better. ADK 2.8's `mode="single_turn"` child registered in `sub_agents` is an
alternative task delegation interface, not a one-model-call budget. Count child
tool/model work separately. Define concurrency ownership for shared state.

## Overlap independent I/O deliberately

Draw the dependency order first. Overlap independent reads; await prerequisites
before dependent operations. Use `TaskGroup` for a bounded all-or-nothing batch,
or implement an explicit partial-success policy. Shared mutable lists obscure
ordering; return results to the caller instead.

For an ADK tool batch, verify that function calls are co-emitted and execution
intervals overlap. Prompt wording and two tool names in a response do not prove
parallel execution. Do not extend that result into a claim that every request or
worker is parallel. Request concurrency is a separate capacity decision.

Reuse HTTP transports in application lifespan where appropriate; bound pools,
per-host connections, in-flight work, bytes before decoding, connect/read/overall
deadlines and total retry time. A per-process semaphore is not a distributed
quota across instances. Retry only eligible transient operations; preserve the
planned identity of non-idempotent work rather than resubmitting blindly.

When a provider fails, return an explicit failure without a plausible numeric
fallback. Keep mock data behind an explicit test mode. Preserve TLS verification.
For currency/reference-data tools, validate supported symbols and finite positive
values, retain source/date, and use suitable decimal arithmetic. A latest
reference quote is not a real-time trading quote. Test failure and partial-answer
behaviour as well as the happy path.
