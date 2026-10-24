# Public acceptance and optional extensions

Read this for end-to-end acceptance, context/performance regressions, telemetry,
follow-ups or managed-tool selection. Use only the sections relevant to the changed
boundary. These recipes supplement [validation.md](validation.md); live work still
follows [execution-safety.md](execution-safety.md). Examples of proposed controls
are not claims that the companion implements them.

## 1. Establish a public outcome oracle

Freeze a supported question, approved interpretation, synthetic data and expected
answer before observing new model samples. Check the public response, not a helper's
intermediate result. Compare equivalent queries by their answers and policy, rather
than requiring identical SQL text.

Assert these parts of the target's actual public contract:

| Evidence | Assertion |
| --- | --- |
| Dispatch and outcome | Expected route/template or supported domain; final success/refusal status |
| Answer | Every requested metric, exact values, population keys and required ordering |
| Cardinality | Unique grouping keys and reported returned-row count equal to actual rows |
| Execution | Expected query/job evidence from the substituted or real boundary |
| Completeness | Truncation/total-row fields agree, if that contract is implemented |
| Refusal | The final explanation is useful and no forbidden metadata/author/query call occurred |

A synthetic job ID proves an offline response contract; it is not live job evidence.
The aggregate checker covers metric/key equivalence, not this whole envelope.
Freeze explicit equivalent metric aliases; retain exact finite numeric checks and
reject conflicting aliases. Assert ranking order independently. Use an LLM judge
for presentation quality if useful, alongside deterministic numerical checks.

Add a negative control through the same public path: change a seeded customer total
from its expected 200 to 700 while leaving route, status and job evidence successful.
The acceptance test must fail. Also remove a requested total while retaining its
average; plausible prose and the remaining metrics must not pass the oracle.

**Historical observation:** the 11 September audit found a smoke CLI reporting PASS
for the wrong 700 result because it checked route/status. Later generated answers
exposed overly narrow alias checks. Corrected checks preserved expected numbers and
replayed the exact captured outputs; original command failures and browser flags
remained recorded. A replacement paid sample is not an adjudication of the original.

**Completion criterion:** the known-correct response passes, the deliberate wrong
answer fails, and the report separates numerical correctness, execution policy and
public-response correctness.

## 2. Climb the framework-to-user acceptance ladder

Preserve real orchestration and replace only external boundaries for offline work.
Guard against accidental authentication/provider construction. Import configuration
only after inspection and use the project's existing isolation mechanism.

1. **Application boundary.** Exercise each route with scripted model proposals and
   an appropriate database substitute. Count routing, authoring, metadata, dry runs
   and executions independently. Invalid context must stop at its intended stage.
2. **SDK wire and return path.** When structured contracts change, capture the actual
   framework-generated provider request with an HTTP boundary double. Assert required
   fields on that payload. Feed valid ready, explicit-null refusal and incomplete
   ready responses back through the framework. A local schema snapshot alone misses
   transformations between the application model and the provider.
3. **Runner.** Consume the invocation stream to completion with an explicit call
   budget supported by the installed API. Identify the final application output;
   an intermediate router/candidate event is insufficient. Test malformed output,
   refusal and handled failure, then verify a subsequent supported request works.
4. **HTTP/SSE.** Create a real local session, submit through the public endpoint,
   decode real serialised events and assert the final response using the same oracle.
   Include malformed requests, a multi-turn session and error-to-success recovery
   if those are product contracts. A substitute HTTP route does not test this layer.
5. **Browser, when a UI is supplied.** Exercise actual submission, loading/disabled
   submit state, final rows, useful refusal and recovery. Record submit-to-meaningful
   rendered answer separately from invocation completion. Inspect what intermediate
   content the intended audience can actually see.

For an ADK integration, inspect the installed Runner, callback and event APIs before
writing the harness; their exact names are version-sensitive. In the companion's
ADK 2.8.0 path, runtime nullable defaults and provider-required nullable fields are
distinct contracts. Its refusal originally failed a second validation after ADK
removed null fields. See [implementation.md](implementation.md#author-contract-and-adk-integration)
for the tested adaptation, not a universal SDK recipe.

If persistent UI history is a requirement, restart the local process and reload a
populated session. Assert the same result/job reference reappears and model/query
counters remain unchanged. This establishes history restoration without replay;
it does not establish a semantic follow-up resolver or authenticated tenant identity.

Keep observer failures distinct from application failures. If a selector wait times
out, inspect existing result/counters before resubmitting. A browser disconnect or
cancelled task does not prove that a provider job stopped; test reconciliation when
that lifecycle is implemented. Live cancellation/recovery needs its own approved
case, rather than being inferred from an offline cancellation double.

**Historical evidence:** the companion exercised the actual Runner and HTTP app
offline, an actual offline browser error/recovery path on 11 September, and live
browser answers/refusals/history restoration on 13 September. Live provider/browser
timeout recovery was **NOT RUN**. Preserve these separate evidence classes.

## 3. Measure routing and context work separately

Create labelled near-matches around the full template contract: paraphrases, missing
values, negation, different metric/grain, extra filters and changed reporting periods.
Measure template precision/recall, parameter extraction, clarification behaviour and
latency separately. Weight false fast matches heavily: a reviewed query can execute
successfully while answering a different question. A scripted router tests dispatch,
not the model classifier's measured precision.

Use two deterministic regressions for the implemented architecture:

- Add a small artificial delay at each substituted model call. Record start/end
  spans and verify the intended serial stages: one router on a reviewed route;
  router plus author on the successful generated route described by this skill.
  Assert exact answers remain unchanged. Do not replace a necessary reasoning stage
  solely to meet a universal two-call rule in a different architecture.
- Add many unrelated tables outside the selected context. Capture actual schema
  requests and the author input: only selected schema detail should appear. Check
  router-catalogue and author-context sizes independently; a compact map can still
  grow too large. A client cache is not evidence of a scoped metadata/result cache.

The companion's delayed public Workflow test checked at most two model round trips,
real dry-run/execution calls through substitutes and unchanged results. Its fresh
metadata sentinel checked delivery, not full schema-drift handling. Wider catalogue
scaling and prompt-size budgets are target-specific tests to implement.

For approved live measurements, freeze questions, expected outcomes, application and
observer versions before sampling. Record backend/model/settings, cold/warm meaning,
sample counts, errors and stage boundaries. A spinner or router JSON is not meaningful
answer content. Attribute model, metadata, query, serialisation and rendering time
separately; residual elapsed time is not automatically database time.

**Historical failed gate:** the 13 September follow-up returned correct results in
six browser samples per SQL route, but retained a scoped end-to-end **FAIL** for
responsiveness. All five warm generated first answers missed 5 seconds; one of five
fast warm first answers also missed. Generated warm final answers had a 14.1667-second
median (9.0765–25.4754 seconds), with all six generated finals below 30 seconds.
These are small dated observations, not an SLA. Removing model stages coincided
with improvement, but differing successful sample membership and model variability
prevent an isolated causal estimate. Keep correctness and responsiveness verdicts
separate, and do not turn a progress message into a successful first-answer sample.

## 4. Verify telemetry before export

**Production extension:** the companion supplied private audit instrumentation, not
a production analytics exporter. Define an output allowlist before adding one.

Useful fields include finite route/template/domain codes, context counts, stage
durations, model tokens, estimated/actual bytes, bounded validation codes, attempt
counts, policy/template version, outcome, response size and completeness. Use only
values actually measured. Keep job IDs needed for reconciliation in protected
operational records; arbitrary identifiers and free-text model reasons make poor
metric labels. Predictable-value hashes are not reliable anonymisation.

An offline exporter test should:

1. Inject distinct synthetic canaries into the prompt, parameters, tool arguments,
   tool results, model reason, provider exception and session state.
2. Exercise success, refusal and failure through the public workflow with each
   configured logging, tracing and analytics exporter directed to an in-memory sink.
3. Flush/shut down each exporter and inspect the actual outgoing records, including
   batched records and nested attributes. Assert only the allowlist leaves the process.
4. Verify that disabling one exporter's content capture does not silently leave a
   second exporter capturing the canaries. Test the installed package's settings.

For relevant ADK versions, inspect `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` as a
trace-content setting; it is not a universal switch for an analytics plugin or
custom logger. Filter before export. Record destination access, retention, region
and shutdown behaviour in the implementation's operational contract. Later masking
cannot retract an earlier disclosure.

## 5. Resolve follow-ups against a trusted plan

**Production extension:** history persistence alone does not implement these steps.
Save the selected template/domain, semantic/template version, metric, grain,
resolved window/timezone, bound values, ranking selection and presentation order.
Keep any large result behind an opaque reference with explicit freshness and access.

A minimal selection-versus-presentation fixture:

| Customer | Completed revenue |
| --- | ---: |
| Z | 100 |
| Y | 90 |
| A | 1 |

The original request selects the top two by revenue: Z, Y. “Sort that result by
customer ID” returns Y, Z. Replacing the selection with `ORDER BY customer_id LIMIT 2`
would instead return A, Y and change the meaning. Determine whether the user requests
a display-only reorder or a new selection; clarify when ambiguous.

Test changing region while retaining the agreed metric/window, crossing midnight
without silently moving a saved relative window, and an explicit period change.
Reauthorise each resulting request; previous SQL does not stay trusted indefinitely.
Cache keys and reads must account for caller/effective scope, policy and semantic
versions, parameters, window and freshness. Test permission revocation and cross-user
access before accepting a cache hit. A cached plan is not permission to reuse rows.

## 6. Choose and test a managed or specialist branch

**Design options, not shipped integrations:** select the narrowest capability that
fully expresses the requested business operation.

| Branch | Suitable responsibility | Contract to establish |
| --- | --- | --- |
| Reviewed function/query tool | Stable operation with known meaning | Narrow inputs, fixed metric/window/grain, expected output |
| Database/schema toolset | Selected discovery or analytical operations | Enabled capabilities plus argument/data restrictions |
| Governed data agent | Reusable authored definitions and verified queries | Managed resource, semantics, execution identity and evidence. ADK's `DataAgentToolset` is read-only by default (`list_accessible_data_agents`, `get_data_agent_info`, `ask_data_agent`); `DataAgentToolConfig(enable_data_agent_modification=True)` adds create, update and delete, waiting up to `data_agent_modification_timeout_seconds` (default 60); `max_query_result_rows` defaults to 50; its credentials config extends a base the docs call experimental and "should not be used for production projects" (https://adk.dev/integrations/data-agent/, read 2026-10-22, and `tools/data_agent/config.py` at adk-python main ed76f94; supported from ADK Python 1.23.0) |
| MCP database service | Shared database tools across clients | Server lifecycle, identity propagation, pooling and policy |
| Custom author/executor | Application-owned SQL and cross-system rules | Local orchestration, validation, limits and maintenance |

Check current official contracts for the target SDK/service only when selecting or
integrating that branch. Names such as `BigQueryToolset` and `DataAgentToolset` identify
different responsibilities; a product name alone establishes no policy guarantee.

For Google's remote MCP servers the recorded contract facts are: callers need
`roles/mcp.toolUser` in addition to the data roles; BigQuery jobs run through the
server carry the label `goog-mcp-server:true` and are billed to the project the call
names, so a model-chosen project argument is a cost and scope hole; and the read-only
toolsets (`execute_sql_readonly`, and Cloud SQL's `/mcp/readonly` endpoint) refuse
DML and DDL while a `SELECT` can still invoke remote functions
(https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp; the Cloud SQL endpoint
is from Google's `cloud-sql-basics` skill, read 21 October 2026, vendor guidance,
confirm against current docs). Connection parameters, tool filters and header
propagation belong to adk-agent-interoperability.

Two more facts change a design on this branch (Google Cloud documentation,
"Control MCP use with IAM", last updated 2026-10-22, and "Use the BigQuery
MCP server", last updated 2026-10-21; read 2026-10-24). Read-only can be
enforced by the platform rather than by tool choice: an IAM deny policy on
`mcp.googleapis.com/tools.call` with the condition
`api.getAttribute('mcp.googleapis.com/tool.isReadOnly', false) == false`
refuses every tool not marked read-only. The page's example denies it to
every principal (`principalSet://goog/public:all`) and attaches it with
`gcloud iam policies create <name> --attachment-point=cloudresourcemanager.googleapis.com/projects/PROJECT_ID --kind=denypolicies --policy-file=policy.json`
(its JSON sample carries a trailing comma, so validate the file before
use); `adk-tool-auth-and-secrets` and the installed
`google/skills:iam-helper-for-policy-management` own the change itself.
`tools/list` still returns the read-write tools, so pair the deny with a
`tool_filter` that keeps them away from the model; the attributes are
enforced only on the `mcp.tools.call` permission, and deny conditions can
also use `tool.name`, `resource.service` and `request.auth.oauth.client_id`.
The BigQuery server's tool reference (last updated 2026-10-15) lists
`list_dataset_ids`, `list_table_ids`, `get_dataset_info`, `get_table_info`,
`execute_sql_readonly`, `execute_sql`, `get_query_results`, `get_job` and
`cancel_job`; a read-only agent's filter names only the tools it needs from
the first five plus `get_query_results`, and never `execute_sql` or
`cancel_job`. The project the job runs and bills in is the `project_id`
argument, so pin it in a `before_tool_callback` rather than letting the
model choose it. The server needs no separate enablement: it is on when the
BigQuery API is enabled. Calls need the scope
`https://www.googleapis.com/auth/bigquery` and the roles
`roles/mcp.toolUser`, `roles/bigquery.jobUser` and
`roles/bigquery.dataViewer`; grant no data-editing role to the agent's
identity, since the MCP deny governs MCP tool calls, not what the identity
could do through the BigQuery API directly.
And BigQuery's server limits `execute_sql` and `execute_sql_readonly` to
three minutes of processing by default and returns at most 3,000 rows, with
no quota of its own beyond the BigQuery API's, so an answer computed over a
capped result may be incomplete: the completeness and refusal path checks
whether the result hit the cap and says so rather than reporting a total.
The documentation does not describe how a capped result is marked; treat a
result of 3,000 rows, or one carrying a page token or an incomplete job, as
capped, prefer pushing the aggregation into the query so the result stays
small, and confirm the actual shape on the first approved live call.
Google recommends a separate identity for agents that use these tools.
Choose between this branch and Toolbox on what each can enforce: the managed
server gives IAM-enforced read-only exploration under an agent identity, and
Toolbox gives reviewed templates, a dataset allowlist and tenant ids the
model cannot see; the managed server has no equivalent of `allowedDatasets`,
templates or secure parameters.

### MCP Toolbox for Databases as the executor

When the executable branch is Google's MCP Toolbox for Databases (`googleapis/mcp-toolbox`, formerly genai-toolbox, v1.14.0; `docs/en/documentation/configuration/security/read-only.md`, `configuration/tools/_index.md` and `integrations/bigquery/tools/bigquery-execute-sql.md`, read 2026-10-22; vendor documentation, confirm on the installed server version), the four boundaries of this skill map onto its configuration, and the ticket's checklist is:

- **Read-only at the source, not in a prompt or a string check.** Set `readOnly: true` on the source. Toolbox enforces it at the engine: for Cloud SQL and AlloyDB PostgreSQL it injects `cloudsql_session_read_only=locked` or `alloydb_session_read_only=locked` into the connection string, so every transaction on the connection is read-only and a write fails with `SQLSTATE 25006`; for Cloud SQL MySQL it sets `read_only_connection=true` on the driver; for BigQuery it dry-runs every statement (`dryRun: true`) and rejects any statement type other than `SELECT`. Because the lock lives in the DSN rather than a runtime `SET`, `COMMIT; SET default_transaction_read_only = off;` chaining cannot escape it and a PgBouncer-style pooler is not poisoned. With read-only on, Toolbox also prunes write-capable tools from the catalogue and advertises `readOnlyHint: true`; treat the hint as a hint (`adk-agent-security`), the DSN lock is the control.
- **BigQuery flags.** `readOnly: true` defaults `writeMode` to `blocked` (only `SELECT`); `protected` permits writes only to the session's temporary dataset; `readOnly: true` with `writeMode: allowed` is rejected at server startup. `allowedDatasets` adds a dry-run analysis that rejects a query naming a table outside the list; authorized views are exempt only when every table name is fully qualified; and dataset-level DDL, `EXECUTE IMMEDIATE`, procedures, functions, `CALL`, `SET @@dataset_id`, `EXTERNAL_QUERY` and region-level `INFORMATION_SCHEMA` views stay disallowed because they cannot be analysed statically.
- **No free-form execution unless the ticket says why.** The prebuilt `bigquery-execute-sql` tool's own page says it "is intended for developer assistant workflows with human-in-the-loop and shouldn't be used for production agents"; a production agent gets reviewed `bigquery-sql` templates, and a ticket that keeps the free-form tool records the justification and the read-only flags in its Evidence section.
- **`parameters`, not `templateParameters`.** Basic parameters bind through the driver. Template parameters are inserted into the statement text unquoted and "can directly replace identifiers, column names, and table names", so the documentation calls them "prone to SQL injections"; use one only behind `allowedValues` (or `minValue` and `maxValue`), with `escape` for an identifier, and a reviewer's sign-off on the template, never for a value the user supplies.
- **Tenant and user ids as `secure` parameters.** A parameter with `secure: true` is published in `secureInputSchema` rather than `inputSchema`, stripped from the declaration the model sees, bound in code by the host application (`toolbox-adk` `secure_params=` or `bind_secure_param`), and carried in the `secureArguments` field of `tools/call`; a model that supplies it in ordinary `arguments` gets a tool execution error (`isError: true`), a missing one is rejected before the request leaves the client, and a client that has not negotiated the feature is refused (`-32021` on protocol 2026-07-28, `-32602` earlier). Secure parameters are always required and cannot carry `default` or `authServices`. The documentation reserves them for client-supplied runtime context and says database credentials belong in the source configuration, not in per-request parameters; `adk-tool-auth-and-secrets` owns the identity the host binds.
- **Fixtures from the bypasses Toolbox names.** Its read-only page lists why soft locks fail; each is a deterministic negative case for the double and, when approved, the live server: `WITH d AS (DELETE FROM users RETURNING *) SELECT * FROM d;`, `SELECT purge_inactive_records();` (a UDF that writes), and `COMMIT; SET default_transaction_read_only = off; DROP TABLE orders;`. Each must fail closed with zero jobs or rows changed, and the same three cases run against this skill's own parser path when the executor is the application. Offline, the double that answers these cases stands in for the Toolbox server at its documented contract (the `secureInputSchema` split, the secure-in-arguments error, `SELECT`-only under `readOnly`), which adk-engineer's rule permits; the ADK SDK itself is never imitated, and a pass on the double is offline evidence until the same cases run against the installed server.

What Toolbox does not supply: the business meaning, grain and reviewed values of §1 to §3 above, the per-request cost ceiling and labels, result completeness and freshness, and the refusal path. Those stay the ticket's work. When the Toolbox server itself must be deployed or its sources provisioned, that is `deploy-adk-on-google-cloud`'s and the database product skill's operation; `adk-agent-interoperability` owns the `ToolboxToolset` connection, protocol pin and credential strategy.

Before connecting a branch, record whether it proposes SQL or executes work itself.
Use a service-boundary double to count operations and inspect identity, scope and
arguments. If SQL executes before the tool returns, a later local rejection cannot
be called “zero query execution.” Restrict both available tools and accepted arguments;
a narrow tool list can still expose an unrestricted SQL/table argument.

Give each executable branch its own cost/deadline limits, output/completeness and
failure contract, then evaluate the same business oracle and refusal cases. Define
streaming, cancellation and conversation continuity explicitly; coordinator history
does not create a conversation inside another service. A managed branch needs its
own separately approved live acceptance, not the companion custom-executor verdict.

Repeated slow-path demand can justify a reviewed tool/template. Use sanitised intent
evidence, obtain business review of the metric and policy, then add near-match and
adversarial tests before promoting it. Repetition establishes demand, not correctness.
