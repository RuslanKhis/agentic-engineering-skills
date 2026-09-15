# Reads, retries and deadlines

Use this workflow when implementing, adapting or reviewing an external API read or its shared transport wrapper. These are production principles to apply to the target project. They do not establish that Chapter 1 implements a real HTTP transport or every safeguard below.

## 1. Establish the actual call path

Trace the public tool through adapters, SDKs and transport. Inspect the installed versions, current signatures, result schema, client lifecycle and existing tests. Preserve the project's package manager, dependency versions and public interfaces unless the requested change requires a migration.

Read the provider's contract for the particular operation, including error semantics, rate limits and retry guidance. Confirm that a purported read has no business side effect; its name or HTTP method is insufficient. Inspect SDK and transport retry defaults as well as application retries. Finish with an identified retry owner and a bound on combined requests and waits; nested loops can multiply both.

## 2. Select retries explicitly

Choose a predicate scoped to that operation and provider. Distinguish selected transient connection, timeout and HTTP failures from authentication, validation, permission and programming errors. Retrying every exception or every server error is not a substitute for a contract. If evidence is incomplete, retain a conservative policy and state the unresolved assumption.

Bound total attempts, counting the first request, and use asynchronous backoff with jitter when appropriate. Respect documented `Retry-After` handling: validate delays or HTTP dates, account for the remaining budget, and stop or defer if the required wait will not fit. Do not shorten the provider's minimum delay merely to squeeze in another attempt. Complete this step when the eligible failures, stopping conditions and retry ownership are explicit in code or review findings.

## 3. Bound distinct layers

Configure the actual transport's connect, read, write and connection-pool timeouts where supported. A read timeout commonly limits the wait for the next data chunk; it does not bound an entire response stream.

Wrap each cooperative attempt with its own deadline, then bound the complete operation, including pool waits, attempts, response processing and backoff. Select values from the workflow's latency needs and provider behaviour. The chapter's one-second lookup, two-second attempt and four-attempt limit are teaching choices, not defaults. Keep model inference and the overall conversation budget separate.

When using `asyncio.timeout()`, retain its context object and check `.expired()` before translating a caught native `TimeoutError` into that deadline expiring. An inner operation can raise `TimeoutError` independently. Preserve caller cancellation; it must escape rather than become a retry or an ordinary tool failure. Nested deadlines must preserve which enclosing budget expired.

Deadlines cancel cooperative asynchronous work; they cannot interrupt blocking code, guarantee an exact wall-clock return time or undo remote effects. Await asynchronous I/O and sleeps. Reuse an appropriately scoped asynchronous client and close it through the application's lifecycle; creating a client on every retry wastes pooling. Completion requires a visible deadline around the whole retry loop and an identified owner for client cleanup.

## 4. Return and verify meaningful outcomes

Preserve the established result schema and callers. Translate expected provider failures at the existing boundary, distinguish total-budget exhaustion from other failures, and retain useful diagnostic information through the application's error handling. Measure successful retrieval separately from the time to any answer or error.

Use deterministic local substitutes and the project's test runner to verify the changed behaviours:

- A selected transient failure can recover; a non-selected error stops after one attempt.
- Exhaustion observes the configured combined request limit, including SDK retries.
- A genuinely stalled cooperative call is cancelled by its attempt deadline; the total deadline also interrupts backoff and prevents further dispatch.
- An unrelated native `TimeoutError` is not relabelled; caller cancellation propagates without another request.
- Relevant `Retry-After`, client reuse/closure and result compatibility paths behave as specified.

Assert call counts, outcomes and cancellation, using tolerances for real timing. Finish when relevant checks pass and any untested provider behaviour is identified. Offline mocks establish application behaviour, not live provider availability or model response quality.
