# Compatibility and evidence boundaries

Read this reference when checking framework compatibility or deciding what the
Chapter 1 evidence establishes. Source names below identify historical
provenance; using this skill does not require the book repository. The behaviour
and limits are described here independently of those files.

For this package's actual interpreter, helper checks and independent agent
evaluations, read the [skill validation record](../tests/forward-evaluation.md).
For the later implementation-depth recheck and retained fixture validation,
read the [recheck record](../tests/depth-recheck.md).

## Historical environment

The final Chapter 1 audit dated **13 September 2026** records a fresh native
macOS 26.6.2 arm64 environment with **Python 3.11.14**, **google-adk 2.8.0**,
**httpx 0.28.1**, **tenacity 9.1.4** and resolved **google-genai 2.23.0**.
The first three packages were explicit dependency pins; google-genai was a
resolved dependency. These versions document the tested historical environment,
not the latest releases or verified compatibility with other agent environments.
The example uses `asyncio.timeout()`, which requires Python 3.11 or later;
that language requirement does not establish a tested version matrix.

The source-aligned manuscript is dated **15 September 2026**. Its production
adapter, durable operation design and PostgreSQL illustration are guidance,
not implementations verified by the companion suite. Skill-package validation
is a separate record and must not inherit the chapter's historical test count.

## Keep the evidence scopes separate

| Evidence | What was observed | What it does not establish |
| --- | --- | --- |
| Final source, offline | **59 tests passed with no skips**, including tool safety, ADK confirmation, HTTP/session/SSE wiring and verification helpers. HTTP integration uses scripted Gemini, controlled mock outcomes and blocked socket connections. | Live model reasoning, real payment-provider behaviour or broad framework compatibility. The 59 count is the full chapter suite, not this skill's helper tests. |
| Final source, live lookup retest | **Six browser turns and 12 streamed Gemini requests** using `gemini-3.5-flash`, Vertex `global`, LOW thinking and a one-second total lookup budget. **Two successful retrievals; four accurate terminal budget-expiry errors.** One tool invocation per turn, no observed loops. | Six successful retrievals, a service availability estimate, production latency percentiles or current-source live refund coverage. |
| Earlier LOW source, live refunds | Rejected confirmation produced zero mock-payment attempts and an accurate cancellation explanation. A separate approved refund completed once, immediately, without a lost response. | Live same-key recovery after a lost response. The later source added a lookup budget and description; its live campaign covered lookups only. |
| Lost refund response, offline | Deterministic public-tool and ADK HTTP tests forced a mock response loss, retried with the same key and recovered one cached refund result. | Real provider deduplication, restart recovery, concurrency safety or a live lost-response pass. |

All five warm live lookup answers **or errors** began within five seconds. Cold
first meaningful text was bracketed at 6.620–6.874 seconds. These are small
browser observations including failures; a responsive error is not retrieval
success. The model was real, while dispute and payment systems remained local
Python mocks. No real refund or managed-cloud application deployment occurred.

The historical audit also verified API activation separately. It did not run
the combined model/UI workflow on that newly activated baseline. This does not
establish complete fresh-project application onboarding.

Provenance: `requirements.txt`, `MANUSCRIPT.md`,
`verification/budget-retest-audit-2026-09-13.md` and
`verification/followup-audit-2026-09-13.md` from Chapter 1.

## Map the rules to their support

Here, **implemented** means the historical teaching example contains the
mechanism. **Production principle** identifies an extension or requirement
without a companion implementation or passing production test.

| Rule or boundary | Support and precise scope |
| --- | --- |
| Select retryable failures explicitly. | **Implemented:** `safe_dispute_agent/safe_api.py` selects HTTPX timeout/connect errors and HTTP 408, 429, 500, 502, 503, 504; other exceptions are not retried. `tests/test_safety.py` checks selected failures stop at four attempts and 400/401/403/404 plus unexpected errors receive one attempt. This selection alone does not make write replay safe. |
| Bound attempts and include backoff in the complete operation budget. | **Implemented, partial:** helpers allow at most four attempts, two-second cooperative attempt deadlines and exponential jitter capped at eight seconds. `safe_dispute_agent/agent.py` bounds the complete lookup at one second, including waits. Safety tests cover stalled work, interrupted backoff, transient recovery and correct timeout attribution. Refunds have no separate overall deadline. |
| Preserve caller cancellation. | **Implemented:** `test_caller_cancellation_is_not_retried_or_swallowed` verifies propagation after one API attempt. Cooperative cancellation cannot interrupt blocking synchronous work or undo an accepted remote side effect. |
| Create one replay key before internal write retries. | **Implemented, invocation scope only:** `issue_refund` creates one UUID-based key and passes it into `_issue_refund_call`. `test_lost_response_reuses_key_and_creates_one_refund` checks two attempts, identical keys and one cached transaction. Each separate public invocation creates a new key and mock client. |
| Represent exhausted writes as uncertain. | **Implemented:** refund exhaustion retains the original key, sets `retryable=False` and asks for human review without a new key. `test_refund_exhaustion_retains_key_and_requests_human_review` checks four same-key attempts and the terminal result. It does not implement provider reconciliation. |
| Require consent before dispatching the wrapped refund. | **Implemented at the ADK wrapper:** `FunctionTool(issue_refund, require_confirmation=True)` blocks missing/rejected consent. Public-tool and HTTP tests exercise approval and rejection. Calling the Python function directly bypasses this wrapper; consent is not authentication or business authorisation. |
| Validate numeric input before a payment attempt. | **Implemented, limited:** invalid type, boolean, non-positive and non-finite amounts are rejected; `test_invalid_amount_never_reaches_payment_api` verifies zero calls. The example accepts floats and does not validate currency precision, balances or business permission. |
| Make terminal results and cancellation explanations accurate. | **Implemented, limited:** public tools return structured terminal errors and agent instructions prohibit repeating them. HTTP tests check result propagation to model/SSE/session history. Earlier-source live rejection checks the actual explanation. No deterministic outer-call guard is implemented. |
| Persist authorised operation identity before dispatch. | **Production principle:** atomically create/load a durable operation record with unique business identity, exact payload and one provider key; reject changed payload under the same identity. An in-process cache is insufficient across workers, calls or restarts. |
| Reconcile uncertain outcomes using the existing operation. | **Production principle:** distinguish `pending`, `applied`, `not_applied` and `unknown`; account for every dispatched attempt. Recover crash windows and abandoned claims under the provider's documented replay scope, retention and lookup contract. Timeout alone cannot prove non-application. |
| Use exact money and trusted authority. | **Production principle:** validate decimal strings and currency-specific precision, convert to minor units, bind approval to exact details and an authenticated principal, and enforce balances atomically. Confirmation and one-operation idempotency do not prevent distinct operations overspending a balance. |
| Own production transport and complete budgets. | **Production principle:** manage a shared async-client lifecycle, transport phase timeouts, retry ownership across SDK layers and a total operation deadline. Honour valid provider `Retry-After` delays only within the remaining budget; otherwise stop or defer. The teaching mock lacks this production adapter. |
| Enforce outer-call and run limits in application code. | **Production principle:** a durable claim or equivalent guard must define repeat/resume/crash semantics. An application-owned ADK Runner may add a model-call cap, but another script's RunConfig is not inherited by ADK Web. Historical audit limits were verification-only. |
| Keep operational records safe and truthful. | **Production principle:** log safe references, attempts, status, exception class and elapsed time without replay keys or sensitive payloads. Preserve programming defects for monitoring. Historical tools instead expose a mock key and broadly translate public-tool exceptions. |
| Distinguish transaction atomicity from deduplication. | **Production principle:** a unique event ledger plus conditional state update can deduplicate owned changes and reject stale ordering; define payload-conflict handling and retention. The manuscript SQL is illustrative and was not executed by the companion tests. A database transaction does not include a remote provider's side effect. |

ADK confirmation and related schema APIs emitted experimental warnings in the
historical environment. Check the target project's installed API and run its
own offline integration tests before adapting these mechanisms. Record that
new validation independently of the historical observations above.

In the inspected ADK 2.8.0 local Web path, `PerAgentDatabaseSessionService`
routes to `SqliteSessionService`. This is distinct from `DatabaseSessionService`.
Google's [confirmation documentation](https://adk.dev/tools-custom/confirmation/#known-limitations)
lists `DatabaseSessionService` and `VertexAiSessionService` as unsupported.
The observed local SQLite-backed confirmation flow does not establish support
for either of those production session paths. Inspect the pinned implementation
and selected client/session path rather than inferring support from a database
filename or successful direct-function test.
