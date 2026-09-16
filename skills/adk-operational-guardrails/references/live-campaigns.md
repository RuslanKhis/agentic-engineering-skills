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

Create a reviewable envelope containing exact target/identity, models/endpoints, allowed operations, synthetic inputs, maximum submissions, maximum actual provider attempts, output limit, deadline for new submissions, cleanup deadline, estimated cost, allowance and retained resources. Get approval for that envelope. Reserve room for required negative cases and targeted retests rather than spending it all on happy paths.

Implement or inspect the transport-level bound before paid work:

1. Validate actual destination, operation, model and output settings immediately before dispatch. Avoid redirects or alternate generation/cache APIs escaping the allowlist. A smaller existing cap must remain smaller.
2. Atomically reserve an attempt in a shared ledger before HTTP. Keep one campaign identity, deadline and counter across local server restarts, browser phases and CLI processes. A per-process counter or a new ledger per restart resets the protection.
3. Count attempts even when HTTP fails or the outcome is ambiguous. Control SDK/transport retries and automatic tool execution at their actual layer. Test that a simulated 503 produces the intended number of wire attempts, and that both streaming and nonstreaming requests use the same boundary.
4. If the ledger is unavailable, full, expired or inconsistent, refuse dispatch. Do not silently create a new campaign or extend its time. Changing the approved models/region, increasing submissions/attempts or adding a retest outside the envelope requires a new decision.
5. Record completed response usage once, separately from partial snapshots. Keep input, candidate output, reasoning and provider total semantics explicit; do not add reasoning twice. Maintain unknown usage rather than converting it to free usage.

The historical harness used a transactional SQLite ledger across local processes and tested actual HTTP boundaries. That demonstrates the enforcement pattern; it is not a distributed ledger or a supported SDK plugin to copy unchanged. Adapt through an interface verified for the installed SDK. A model-call cap can still allow more HTTP attempts through retries, and a submission can contain several model calls.

Treat estimates as estimates: input/context growth, reasoning, retries, transport failures and retained infrastructure can change cost. A campaign allowance is not a provider-enforced currency cap.

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

## Close with scoped evidence

Reconcile submissions, attempts, completed usage and explicit unknowns. Stop only owned processes and close their clients/tabs; preserve sanitised evidence before removing disposable state. For approved cloud resources follow the separate owned cleanup procedure; do not disable pre-existing APIs or erase the operator's ADC as routine cleanup. Report what remains, including delayed billing/retention limits, rather than “everything is free now”.

Publish a compact matrix: source/version, path, real versus mocked boundaries, input class, actual tool effect, final claim, attempts, known usage, pass/fail/unverified and cleanup scope. Carry forward failures and missing coverage. The chapter's finite campaigns establish those selected observations, not universal model compliance or production scale.
