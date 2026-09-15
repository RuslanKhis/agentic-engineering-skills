# Execution and operations

These are production principles for implementation and review. The companion verified a narrower subset, listed in [compatibility.md](compatibility.md). Apply controls according to the real data surface and requested scope; report absent controls as gaps instead of claiming the sample supplies them.

## Trusted request and query checks

Preserve the original request and authenticated caller scope in host-owned state. The model's copied question, selected domain, declared table list and operational reason are untrusted proposals. Before execution, bind the candidate to the authorised domain and schemas actually retrieved for this invocation. Compare parsed physical references with that trusted scope. A candidate must not widen its own permissions by naming another otherwise approved domain.

Use a parser for the target dialect, supporting a deliberately bounded query grammar. Validate one read-only query, actual physical references, result projections and allowed operations; reject unsupported constructs before creating a database job. A regular expression or a leading `SELECT` check is insufficient. Verify nested CTE scopes, shadowing, case semantics, views, table functions and namespaced calls against the parser and provider behaviour. Fail clearly for constructs the policy cannot resolve.

Use explicit project/dataset/table identities from trusted configuration. Reject unqualified physical references when the boundary depends on full qualification. Resolve CTEs lexically; a global bag of CTE names can misclassify a physical reference. Avoid case-folding identifiers unless the provider's relevant identity rules permit it. The companion's simpler parser is not a complete production sandbox and is not bundled here as one.

Enforce the necessary column, view, join, function and connection policies. Blocking cross joins does not validate all remaining join predicates. Read-only SQL can still disclose unauthorised data, invoke external functions or spend substantial resources. The database identity's least privilege is an independent boundary. Add negative tests that assert zero submission, not only an exception message.

Bind supplied values through typed database parameters. Check duplicate and missing parameter names, approved types, finite numeric values, range/precision and temporal semantics. Reconcile SQL parameter references with declarations. If the product requires every user-derived value to be bound, implement that contract explicitly; validating only declared parameters does not enforce it. Parameterisation prevents values becoming SQL structure; it does not establish query correctness.

## Bounded execution

Perform a dry run where supported and apply the execution job's billing ceiling independently. A row limit does not bound bytes scanned. Treat a missing cost estimate as unknown and apply a documented policy: normally refuse or require a separately approved bounded exception. The companion substituted zero for a missing estimate; do not inherit that shortcut silently.

Keep database location explicit and distinct from the model endpoint. Bound retries, submission, polling, paging and total elapsed time. Separate per-call timeouts do not form a cumulative deadline. Compute remaining time from a monotonic deadline when a total request budget is required. Use stable job identifiers or the provider's supported idempotency mechanism before side-effecting submission; a timeout does not prove the query never ran. Reconcile an uncertain outcome before resubmitting.

Cancel when appropriate, but report cancellation as confirmed only when the provider establishes it. Keep cleanup/reconciliation state for pending work. If implementing SQL repair, budget attempts inside the same deadline, preserve trusted intent and scope, and rerun all checks. Authentication, permission and quota failures should not trigger SQL rewrites. A retry must not duplicate a query whose outcome remains unknown.

Bound returned rows and response bytes independently. Preserve exact numeric meaning during serialisation. Report partial/truncated results explicitly; requesting only the first rows does not prove a complete answer. Query observation/completion time is not source freshness. Use source metadata for a freshness claim and disclose its meaning.

Keep public errors short and sanitised, with bounded reason codes. Review tool events, trace payloads and intermediate messages as well as final prose. Avoid leaking parameters, raw provider errors, Pydantic input dumps or full candidate SQL to an unauthorised caller. Allowlist telemetry fields before export. Check the installed framework's content capture settings and each exporter separately; a single tracing switch is not a universal analytics control.

## Cloud lifecycle

Start with a read-only inventory of the explicitly selected project. Check actual project access, billing state and required APIs separately; changing a UI project selector is not connectivity evidence. Distinguish CLI credentials, Application Default Credentials (ADC), resource project and ADC quota project. Inspect actual configuration precedence, including service-local `.env` files. A root API key update need not change a child application's configuration. Do not print keys or tokens.

Use ADC locally and workload identity in managed environments where suitable. Use Secret Manager when a secret is actually required. A model API key does not provide BigQuery credentials. Keep operator provisioning permissions separate from runtime query permissions. For a BigQuery/Vertex runtime, begin with job submission and Vertex access at the required project scope and read access only on the approved dataset; inspect quota-consumer and impersonation needs for that environment. Grant token creation only on the intended account. Avoid downloaded service-account keys and Owner/Editor shortcuts.

Before a consequential command, follow the approval step in [../SKILL.md](../SKILL.md#4-obtain-approval-at-the-consequential-boundary). The reviewable operation record must include:

- Exact resource and quota project, model endpoint, database location, account and resources.
- API and IAM changes as explicit allowlists, exact commands and any existing resources affected.
- Maximum model calls, bytes billed, elapsed time, polling/retry bounds and an estimated or capped spend agreed for the target.
- Unique ownership labels/identifiers, durable state path, resource/job IDs, recovery procedure and separate cleanup commands.

Use unique owned resources for live tests. Record ownership and pending operations before creation. Reuse stable load/job IDs and seed dates on repeat setup. A permission or transport failure is not `NotFound`; stop and preserve state. Existing resources require matching ownership, not a convenient name. Fresh project/region setup needs fresh state rather than old deployment IDs.

After IAM changes, check readiness using the narrowly relevant identity/token operation with a finite retry budget. Retry only recognised propagation errors; do not replay a model request or query to test token readiness. Keep tokens in memory and output only necessary identity evidence.

Keep teardown separate: stop the application, remove runtime overrides, inspect the ownership record, obtain cleanup confirmation, reconcile pending jobs, delete only owned resources/grants, repeat cleanup safely, then independently inspect absence. Preserve recovery state until deletion is established. APIs and pre-existing grants/resources normally remain; say exactly what was retained. Expired credentials or a partial inventory prevents a complete-cleanup claim.
