# Validate the selected guarantee

Use the target's existing test runner and interpreter. Keep test doubles at provider or model boundaries so that assertions exercise the real retry wrapper, tool function and confirmation plumbing. Use synthetic payloads and fail closed on unexpected network calls.

## Reads and deadlines

- A transient failure followed by success returns real fixture data within the chosen budget.
- Terminal errors such as the provider's non-retryable 400 take one attempt.
- Repeated eligible failures stop at the configured total attempt count, including the first attempt.
- A genuinely delayed cooperative call is cancelled at the attempt or operation deadline. A real backoff sleep is also interrupted by the complete-operation deadline; removing sleeps in every test would miss that bug.
- A provider-native timeout raised before the deadline is not mislabelled as budget expiry. Caller cancellation propagates and is not retried.
- The public result distinguishes successful data from a terminal error. Count retrieval successes separately from fast error responses.
- Malformed or incomplete provider success data never becomes validated business success. Expected failure translation preserves the public schema; unexpected defects remain visible in safe diagnostics without leaking payloads or keys.

## Writes and confirmation

- With no established replay contract, a provider that commits and loses its response is called once; the outcome remains unknown rather than causing an automatic second write.
- With a documented replay contract, commit-then-lost-response recovery uses the same key and canonical payload and produces one logical side effect. Count side effects as well as method calls.
- If implementing durable recovery, reconstruct the service/worker and repeat the same operation; assert identity reuse. Reject changed payloads and test concurrent claim behaviour. An instance dictionary cannot pass as durable storage.
- Preserve unknown state across multiple attempts, including a later terminal rejection. Exercise key-retention expiry and reconciliation rules when the integration implements them.
- Invalid amounts and unauthorised actors never reach the provider. Exact money and approval policy must follow the target's business rules.
- Preserve contract-valid amount spellings; do not add canonical-only acceptance when the provider contract permits other decimal strings. Test the exact dispatched and returned values.
- Change the business revision or approved details during a confirmation pause: execution must revalidate and send zero provider requests. Exercise balance races when implementing that guarantee.
- Invoke the real confirmation wrapper: missing consent and rejected consent cause zero provider calls; approved consent permits the authorised action. Directly calling the underlying function is insufficient.
- Exercise the client/session pause-and-resume path independently of the direct wrapper. A scripted model checks wiring; it cannot prove that a live model describes rejection accurately.

Implement only tests relevant to changed guarantees. Preserve the source of any reused test and adapt its public interface to the target. Do not claim restart, concurrency, real-provider or approval guarantees that were not exercised.

For concrete ADK ASGI/session/SSE mechanics and pre-live limit checks, use [ADK verification](adk-verification.md). For activation recovery, test the decision table in [ADK operations](adk-operations.md) with a fake metadata/enable client before exercising an approved live target.

## Live verification

Prepare the exact isolated target, credentials mode, provider/model, location, request and token/cost ceilings, duration, stop conditions and cleanup inventory before requesting approval. Inspect prerequisites without a model call. Do not automatically enable APIs, refresh grants, rotate keys or switch projects to make a test pass.

Use the target's actual model/client/session route. Observe request, provider/tool result and final user-facing answer. Preserve failed samples rather than replacing them. For rejection, check both zero side effects and an accurate cancellation answer. A successful write without a lost response does not verify recovery from lost responses.

Stop when the approved sample or budget ends. Reconcile uncertain calls before another dispatch. Cleanup requires its own concrete confirmed scope, and retained state or resources must be reported honestly.

## Completion report

Provide the affected files, exact commands, test counts/results and compatibility observed. Separate the following claims:

| Evidence | What it supports |
| --- | --- |
| Source or syntax inspection | The implementation shape or parseability; no execution guarantee |
| Offline provider doubles | The exercised orchestration and failure path under the fixture contract |
| Offline ADK HTTP/session test | The tested wrapper/client plumbing with substituted model responses |
| Approved live test | Only the observed provider/model, version, credentials mode and workflow |
| Production principle | A requirement or recommendation still needing implementation and validation |

Record partial scans, missing prerequisites, unsupported APIs, unexecuted branches, remaining manual steps and any task-owned state that remains. A second invocation should reuse the existing implementation and state rather than creating a parallel solution.
