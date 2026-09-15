# Custom JSON API

Use this procedure for a final-answer HTTP interface, including a gateway in front of an existing ADK API server. Preserve an existing equivalent contract instead of renaming it to match the book.

## Specify before wiring

For a new small interface, a useful request is `{ "message": "...", "session_id": null }`; a continuation supplies the returned session ID. A useful response is `{ "session_id": "...", "response": "..." }`. The server obtains the caller separately. Set finite message/body limits and validate session identifiers before constructing paths. The tested example used 8,000 characters and a 1–128 character identifier; select limits appropriate to the product rather than assuming those values bound cost.

Choose creation semantics explicitly. Recommended production semantics: omission creates; a supplied ID resumes an existing caller-owned conversation; unknown and other-user IDs receive the same safe not-found response. Browser-allocated IDs are also viable when the server explicitly authorises creation. The teaching local JSON and ADK API gateways create an unknown supplied ID in the caller's scope, while managed JSON returns 404. Do not accidentally change a customised application's chosen behaviour.

If introducing a request reference, add it to server success/error models, headers/CORS exposure and client validation together. A random request ID provides correlation; durable idempotency requires a separate operation record.

## Server implementation order

1. Reuse the app's verified authentication dependency. Keep model access behind it. Check user/session scope before execution; put the same check on any added history or cancellation endpoint. For greenfield offline work, use a test-only dependency override; fail closed in the production route until its real verifier is configured.
2. Reuse stable agent configuration. Create loop-bound session/client resources in the web application's lifespan, after worker creation, and close them at shutdown using the pinned SDK's supported lifecycle. In-memory sessions are suitable only when process-local persistence is acceptable.
3. Put the overall timeout outside conversation-lock acquisition and agent execution. Key admission by trusted user/tenant plus conversation. A process-local `asyncio.Lock` does not coordinate replicas. Preserve cancellation as control flow, and own the iterator until consumption and closure finish.
4. Construct the model's new user content from the validated request. Do not replay browser-supplied history as authoritative stored history when the server already owns the session.
5. Collect public content under an explicit success policy. Inspect every event for reported run errors, including events after final-looking text. Exclude thought-marked parts and unapproved authors. Decide whether reported tool errors make the whole operation fail or produce a typed partial outcome. Select completed text once; do not append a full aggregate after its partial chunks. Avoid an implicit partial-text success fallback unless the response schema defines it.
6. Return controlled public errors. Typical mappings are 401/403 for authentication/authorisation, safe 404 for unavailable conversations, 422 for invalid input, 502 for upstream failure and 504 for deadline expiry. Retain the project's established equivalents. Use allowlisted private diagnostics; sanitised HTTP text does not sanitise `logger.exception` or SDK traces.

The companion's local final-response collector is **not** a complete implementation of step 5: a later reported ADK error can leave earlier text as HTTP 200. Its managed collector rejects event-level errors but only logs tool-error envelopes and can fall back to partial text. Implement and test the product's stronger policy rather than copying either uncritically.

## Existing ADK API service

Keep the browser pointed at the application gateway. Authenticate gateway-to-service calls using the platform's workload identity mechanism; keep that credential separate from the application user. Scope upstream session operations with the server-derived user and validated session ID. Translate returned ADK events into the small public response.

The tested gateway consumes `/run` as a collected response. An upstream `/run_sse` route is a separate option and does not make the existing JSON browser stream tokens. Verify the selected server's pinned request schema and session behaviour locally before making remote calls. A proxy lookup receiving 403 is not evidence that it should create a session.

## Browser implementation order

1. Keep the API helper independent of token storage or sign-in. Pass the credential from the app's verified auth flow. Never store a production secret in a `VITE_` or `NEXT_PUBLIC_` variable.
2. Validate the response at runtime: required ID and text fields must have the intended types and bounds. TypeScript type assertions do not validate incoming JSON. Handle string, structured and validation-list error bodies without displaying raw untrusted provider detail.
3. Maintain transcript, current conversation ID, draft, in-flight state and controlled error state. Use stable message IDs. A new-conversation button clears the local selection; it does not silently delete backend history.
4. Use an `AbortController` with a bounded response/body deadline. The tested demo used 130 seconds around a 120-second backend budget, which is evidence of bounded waits, not a latency objective. Disable overlapping sends and restore controls on settled outcomes.
5. Do not automatically resend an agent invocation after a timeout. For mutating tools, retain its operation key and present an in-progress/unknown outcome until server reconciliation resolves it. Reconnect/status retrieval is different from executing the user's message again.

Finish with the tests in [validation.md](validation.md), covering both the request helper and an HTTP route with the model boundary replaced. Pure rendering assertions cannot prove that the correct backend tool ran.
