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

For the recorded ADK 2.8.0 adapter, use this mapping after checking the target service's contract:

| Operation | Recorded upstream contract |
| --- | --- |
| Read a session | `GET /apps/{app}/users/{verified_user}/sessions/{session}` |
| Create after confirmed absence, when the chosen contract permits it | `POST` to that same session path; use the server's documented initial-state body |
| Execute the new message | `POST /run` with the body below |
| Stream upstream events | `/run_sse` is a separate route; consuming it in a collector still gives the browser one final JSON response |

Encode each path segment independently with `urllib.parse.quote(value, safe="")`, after validating its syntax and scope. The served application package/folder (`support_agent` in the recorded example) supplies `appName`; the Python agent name and CopilotKit registration (`support_triage` there) are different identifiers. Discover the actual served application instead of deriving it from the UI label.

```python
payload = {
    "appName": upstream_app_name,
    "userId": verified_user_id,
    "sessionId": validated_session_id,
    "newMessage": {"role": "user", "parts": [{"text": validated_message}]},
}
```

Keep an `httpx.AsyncClient` in the worker lifespan, use `follow_redirects=False` when forwarding credentials, and include token acquisition, session operations and body consumption in the overall deadline. The companion collector accepts an event list, an `events` envelope, or one event. Scan the whole collection for `error_code`/`errorCode` and `error_message`/`errorMessage` before selecting the last nonpartial public model/assistant text. Keep thought filtering and the explicit tool-error policy from the server procedure above. These accepted envelopes are this adapter's behaviour, not a promise that every ADK server returns every shape.

Only a confirmed metadata 404 permits the selected creation path. The teaching gateway accepts a creation-race 409 without readback; a production gateway must read the exact session back and establish caller ownership before continuing. A 403, timeout or invalid payload is not absence. Test the mapping with an HTTP mock transport that checks the actual URL, body and caller scope, including two users with the same session ID. This adapter has offline HTTP evidence; a new Cloud Run/GKE service still needs its own authorised live check.

### Private Cloud Run identity

Use a Google-signed **ID token**, with the receiving service's accepted audience, for gateway-to-Cloud-Run authentication. An OAuth access token for Google APIs and the browser's sign-in credential serve different purposes. Keep the audience as the service URL or configured custom audience, separate from the `/run` request path. Grant the gateway identity `roles/run.invoker` on the specific receiving service. [Cloud Run service authentication](https://docs.cloud.google.com/run/docs/authenticating/service-to-service) documents this contract.

For an attached Google Cloud identity, the recorded Python helper can acquire the ID token through metadata. On a workstation, the helper reads `GOOGLE_APPLICATION_CREDENTIALS` and supports an `impersonated_service_account` configuration; an ordinary user ADC login alone does not satisfy this helper. This branch was rechecked in installed google-auth **2.57.1** during the skill depth review; the historical campaign recorded 2.58.0. Inspect the installed helper before transferring the recipe to another version. Once the exact identity and credential change are authorised:

```bash
gcloud auth application-default login \
  --impersonate-service-account="$GATEWAY_SERVICE_ACCOUNT"
export GOOGLE_APPLICATION_CREDENTIALS="${CLOUDSDK_CONFIG:-$HOME/.config/gcloud}/application_default_credentials.json"
```

This replaces local ADC configuration; retain the user's intended authentication setup. Confirm the actual generated path if a custom gcloud configuration is used. The operator needs Token Creator on the impersonated service account; any new IAM grant is a separate, scoped change. The configuration has no service-account private key, but remains sensitive credential material. See [local ADC impersonation](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment#sa-impersonation).

Set the gateway's server-only `UPSTREAM_AUTH_MODE=google-id-token` and explicit `UPSTREAM_AUDIENCE`. The corresponding helper pattern is:

```python
import asyncio
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2 import id_token

async def service_headers(audience: str) -> dict[str, str]:
    token = await asyncio.to_thread(
        id_token.fetch_id_token, GoogleAuthRequest(), audience
    )
    return {"Authorization": f"Bearer {token}"}
```

Call this within the overall deadline; cancelling the await does not stop a synchronous worker, so bound transport time and worker capacity in production. Treat token acquisition failure as a controlled upstream error and invoke no agent. Never return or log the token. Keep application-user verification in addition to this service credential. The companion verifies sanitised failure offline; **workstation impersonation and private Cloud Run invocation were not live-tested**.

## Browser implementation order

1. Keep the API helper independent of token storage or sign-in. Pass the credential from the app's verified auth flow. Never store a production secret in a `VITE_` or `NEXT_PUBLIC_` variable.
2. Validate the response at runtime: required ID and text fields must have the intended types and bounds. TypeScript type assertions do not validate incoming JSON. Handle string, structured and validation-list error bodies without displaying raw untrusted provider detail.
3. Maintain transcript, current conversation ID, draft, in-flight state and controlled error state. Use stable message IDs. A new-conversation button clears the local selection; it does not silently delete backend history.
4. Use an `AbortController` with a bounded response/body deadline. Start its timer before `fetch`, retain it while awaiting `response.json()`, and clear it in `finally`; a server can send headers and then stall the body. The tested demo used 130 seconds around a 120-second backend budget, which is evidence of bounded waits, not a latency objective. Disable overlapping sends and restore controls on settled outcomes.
5. Do not automatically resend an agent invocation after a timeout. For mutating tools, retain its operation key and present an in-progress/unknown outcome until server reconciliation resolves it. Reconnect/status retrieval is different from executing the user's message again.

Finish with the tests in [validation.md](validation.md), covering both the request helper and an HTTP route with the model boundary replaced. Pure rendering assertions cannot prove that the correct backend tool ran.
