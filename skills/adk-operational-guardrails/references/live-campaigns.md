# Reproduce a bounded live verification

Read when local tests pass but provider, browser or deployment behaviour still needs evidence. This procedure adapts the chapter's completed model campaigns and preflight repairs; it supplies no authority to run a new campaign. Use [validation](validation.md) for offline acceptance and [serving/lifecycle](serving-and-lifecycle.md) for deployed integration and cleanup.

## Establish a reproducible baseline

Identify the exact source and dependency environment, served entry point, model backend, effective model/output configuration and state lifetime. Use a clean temporary source/configuration scope or the project's equivalent isolation. Record hashes/versions and keep secrets out of the evidence. A `requirements.txt` pin on ADK does not freeze its transitive SDKs; capture the resolved environment as well.

Decide which dependencies are real and which remain mocked before running anything. Real Gemini with a local review publisher tests model/tool behaviour, not delivery to a reviewer. Browser activity through ADK Web does not automatically test a separate application runtime. Keep an acceptance row for each actual path and rerun the affected rows after a shared-tool or instruction correction.

## Preflight as separate gates

Run read-only commands with explicit targets, bounded timeouts and automatic API-remediation prompts disabled. Check the installed CLI help before constructing its exact invocation. Configure a child process rather than rewriting the user's active account, project or credentials. Emit normalised statuses and allowlisted metadata instead of raw provider errors, tokens or environment contents.

| Gate | What passing establishes | What it does not establish |
| --- | --- | --- |
| Selected project is accessible and active | The operator can read this project | ADC or deployed identity can generate models |
| Required services are enabled | Current API state for the intended request consumer | The skill enabled them, or runtime IAM is sufficient |
| Billing read succeeds and is linked when required | Observed billing status | Available model capacity or exact future cost |
| Runtime credential/backend configuration is consistent | Intended identity/project/location/key source selected | Actual model access without a live request |
| Approved bounded model request succeeds | This identity/model/endpoint worked for this request | Every region/model or a deployed service account works |

A billing read failing because its prerequisite API is disabled says nothing conclusive about whether the target has billing linked. Classify authentication failure, access denial, disabled API, transport failure and unknown provider state separately. Do not treat repeated `403`s as transient model failures, rotate accounts automatically or enlarge IAM grants to unblock them.

Check root and nested configuration for conflicting key/backend selection without printing key values. For an ADC-only campaign, remove API keys and dotenv fallback from its child environment; for an API-key campaign, verify the key belongs to the approved target without disclosing it. An account/project update in an IDE or CLI does not prove the runtime selected it.

If activation was separately approved, persist its operation identity, poll within a bounded deadline and independently read enabled state. A null/empty CLI JSON body may accompany an accepted operation reported on stderr. Parse only the expected identity/status, not arbitrary commands printed by a provider. Resume that operation instead of submitting it again. An already-enabled state verifies readiness, not fresh activation; record a fresh-project activation test as unrun if it was not exercised.

## Enforce the campaign, not just its written plan

After recurring structural failures, complete a short re-entry record before
proposing another broad paid experiment: first reached failure and later known
blockers; classification (transport/schema, unrepresentable outcome, copying/coverage,
retrieval or semantic); retained reproducer and honest passing reference through the
actual schema/checker/runtime; changed boundary and offline regressions; new hypothesis
and discriminating observation; diagnostic/release phases and their stop/continue
rules; exact cost/call envelope. A reference that invents relationships or drops
required safeguards is invalid. There is no universal repeat threshold or new paid
allowance. This checkpoint is offline work; reuse valid authorization within scope.

Declare a diagnostic canary and conditional fixed cohort in the plan before approval
when that sequence answers the question. Preserve an already-approved fixed cohort's
protocol: no invented early-stop rule, substituted cases or added retries after seeing
failures. Budget/safety stops still apply and leave missing cases visible. Keep replay
results separate from original historical failures. Optimize what the next experiment
can distinguish, not just whether it fits the spending ceiling.

Create a reviewable envelope containing exact target/identity, models/endpoints, allowed operations, synthetic inputs, maximum submissions, maximum actual provider attempts, output limit, deadline for new submissions, cleanup deadline, estimated cost, allowance and retained resources. Get approval for that envelope. Reserve room for required negative cases and targeted retests rather than spending it all on happy paths.

Implement or inspect the transport-level bound before paid work:

1. Validate actual destination, operation, model and output settings immediately before dispatch. Avoid redirects or alternate generation/cache APIs escaping the allowlist. A smaller existing cap must remain smaller.
2. Atomically reserve an attempt in a shared ledger before HTTP. Keep one campaign identity, deadline and counter across local server restarts, browser phases and CLI processes. A per-process counter or a new ledger per restart resets the protection.
3. Count attempts even when HTTP fails or the outcome is ambiguous. Control SDK/transport retries and automatic tool execution at their actual layer. Test that a simulated 503 produces the intended number of wire attempts, and that both streaming and nonstreaming requests use the same boundary.
4. If the ledger is unavailable, full, expired or inconsistent, refuse dispatch. Do not silently create a new campaign or extend its time. Changing the approved models/region, increasing submissions/attempts or adding a retest outside the envelope requires a new decision.
5. Record completed response usage once, separately from partial snapshots. Keep input, candidate output, reasoning and provider total semantics explicit; do not add reasoning twice. Maintain unknown usage rather than converting it to free usage.

The historical harness used a transactional SQLite ledger across local processes and tested actual HTTP boundaries. That demonstrates the enforcement pattern; it is not a distributed ledger or a supported SDK plugin to copy unchanged. Adapt through an interface verified for the installed SDK. A model-call cap can still allow more HTTP attempts through retries, and a submission can contain several model calls.

Treat estimates as estimates: input/context growth, reasoning, retries, transport failures and retained infrastructure can change cost. A campaign allowance is not a provider-enforced currency cap.

### Admit continuations within explicit quotas

Include stage/case continuation quotas in the envelope: permitted repair/recovery
operations, maximum new submissions and actual sends (including SDK retries),
reserved cost and remaining admission window. These are allocations within the
shared campaign ceiling, not fresh budgets. Distinguish reconnecting to existing
work from dispatching a new attempt. Check consumed counts and uncertain outcomes
durably across failures, interruption and restart before admitting either path.

Retry only the affected stage with verified unaffected upstream artifacts and
invalidate its dependent descendants. Bind reuse to source/full inputs,
instructions/schema, model configuration, authoritative response/native projection
and relevant code; reviews also need the exact draft/frame/invocation/images.
Qualify persistence through realistic Runner/write/reopen/reuse checks first.
Keep originals immutable and link each new attempt separately. Where installed,
evaluation and workflow guidance provide the detailed progressive-validation and
checkpoint procedures; neither is required to enforce this envelope.

Reuse approval already covering the exact continuation, target, operation and
limits. Local code repair does not grant unlimited paid retries. Expanded paid
scope needs a reviewable updated envelope and new approval; preserve prior
consumption. If no allocation remains, stop paid dispatch and continue offline
diagnosis. A changed failure does not reset quotas. Deduplication must look up
failed, interrupted and no-response attempts as well as successes; a permitted
new attempt is explicit, rather than a blind replay of an uncertain request.

### Keep the accounting categories visible

| Category | Meaning and admission treatment |
| --- | --- |
| Settled charges | Authoritative reconciled charges, deduplicated by receipt/attempt; retain even if output is rejected |
| Conservative request reservations | Pre-dispatch allowance for admitted work, derived from verified request bounds; settle or transfer to an unknown hold without counting twice |
| Unknown-charge holds | Unreconciled possible spend after failure, interruption or missing receipt; remain encumbered until authoritative reconciliation |
| Observed provider balance | Timestamped external observation that may lag settlement; not interchangeable with the campaign ledger |
| Remaining campaign allowance | Approved monetary allowance less settled campaign charges, open reservations and unknown holds; counts and time limits still apply independently |

Use mutually exclusive accounting states for each reserved amount so transitions
do not double-charge capacity or release it early. Report overruns explicitly;
negative remaining allowance blocks further admission. A small actual charge on
one request does not justify lowering an unverified conservative bound for future
requests. Revise estimates only from verified pricing and effective input/output/
retry bounds, within existing approval. A displayed balance does not prove that
an uncertain request was free. Use [token budgets](token-budgets.md) for atomic
admission/settlement and actual-store crash/late-receipt tests.

### Turn the envelope into a coverage and cost worksheet

List every affected path/model configuration and its required input classes before allocating submissions. For example, a **proposed** 12-submission campaign across two local servers and one CLI could allocate three cases per path—complete low-value request, complete high-value request and missing required input—then reserve one slot per path for continuity or a targeted retest. If a correction uses a reserve, the displaced continuity case remains unrun. Additional models or configurations require their own coverage decision; twelve is an illustration, not a recommended limit or inherited approval.

Record start time, last admission and final local closeout separately. An illustrative 30-minute window could allow 25 minutes for new work and five for bounded completion/accounting/cleanup. Intersect every request timeout with the remaining window; check the deadline again before each provider attempt. Choose margins for the actual workload and obtain approval for that schedule. The final local deadline cannot prove remote cancellation or final billing.

Build the estimate from current official prices for the selected backend/model/location, noting date, currency and billing units. For each priced attempt class, record its maximum attempt count, bounded input/context, output, separately charged reasoning if applicable, and any tool/storage charges. Calculate `attempts × (input units × input rate + output units × output rate + other charges)` after converting to the provider's units; include reasoning only in its actual billing category. Sum expected cases and a conservative maximum-attempt scenario. Identify unbounded context, unknown usage, caching assumptions and exclusions rather than presenting an exact maximum without support. Choose the allowance after showing this worksheet; reduce work if the estimate exceeds it.

This skill supplies the procedure and acceptance cases, not a ready-made campaign launcher or transport ledger. Do not substitute the invocation guard asset for cross-process campaign enforcement. Prepare and test that integration in the target project before paid execution.

## Exercise outcomes, not attractive transcripts

For each workflow, include required inputs and state the expected observable operation. Also test missing input deliberately: clarification with zero tool calls is correct when a required reason is absent, and must not be relabelled successful review submission. Use synthetic identities/orders and fresh sessions when isolation is the experimental unit; test a second turn separately when continuity is the claim.

Check real function calls/responses and the final user-facing claim. Low-value approval in an approval-only tool must still say no payment; a high-value request must remain pending and must not be submitted repeatedly. A model can call the correct tool and still invent a completed payment afterwards. Keep the failing sample, fix the contract/instructions, prove the serialised follow-up request offline, then run only the approved targeted retest. Do not substitute a passing model/path for untested affected ones.

For browser work, observe loading, disabled input, restored input, meaningful result and a subsequent successful request after an injected offline provider error. Confirm the actual streaming setting and network path rather than inferring token streaming from an SSE connection. Read session/tool evidence through the application's authorised interface when available. Model prose about a team, queue or future update is not a delivery receipt.

Measure timing only when relevant to the request. Separate process startup, first meaningful content and final completion; identify cold/warm state and observation uncertainty. Preserve target misses. Streaming can expose content before completion but cannot expose text that inference has not produced. Avoid changing model, region and token settings simultaneously during diagnosis.

Human pauses, laptop closure and connection loss confound a timing sample; retain
its failure and charges without inferring a latency defect. Reconnect to an
existing operation where supported before considering another counted dispatch.
Saved-stage recovery and clean end-to-end latency require separate evidence.

## Close with scoped evidence

Reconcile submissions, attempts, completed usage and explicit unknowns. Stop only owned processes and close their clients/tabs; preserve sanitised evidence before removing disposable state. For approved cloud resources follow the separate owned cleanup procedure; do not disable pre-existing APIs or erase the operator's ADC as routine cleanup. Report what remains, including delayed billing/retention limits, rather than “everything is free now”.

Publish a compact matrix: source/version, path, real versus mocked boundaries, input class, actual tool effect, final claim, attempts, known usage, pass/fail/unverified and cleanup scope. Carry forward failures and missing coverage. The chapter's finite campaigns establish those selected observations, not universal model compliance or production scale.
