# Identity and public-output boundaries

Read for gateway/tool changes, a cross-user access report, public event translation or credential leakage. Preserve the application's identity provider and response contract unless changing them is the requested task.

## Establish ownership

<!-- shared:verified-principal -->
**Identity comes from a verified principal.** Verify the caller's credential
at the server (signature, issuer, audience, expiry and required claims, with
the pinned provider library) and derive one internal principal from it. An
email address, a client-sent `user_id`, a session or thread locator, an
invocation ID, a model-chosen argument, user text and editable headers or
session state never prove identity. That principal is the only source of the
ADK `user_id` on every Runner and session call, of the owner key on every
record, and of the subject every tool and credential lookup acts for. Tools
read it from trusted context (`tool_context.user_id`, `ToolContext.session.user_id`
or the pinned SDK's accessor), never from their own arguments. Create and load
sessions under it; an unknown or foreign session fails without revealing that
it exists. A verifier outage and an invalid credential both deny access; only
the invalid credential should prompt a new sign-in.

ADK's own API server (`adk api_server`, `adk web`, `get_fast_api_app()`)
authenticates no end user: the session routes take `user_id` from the path and
`/run` and `/run_sse` from the body. ADK 2.12.0's change "take the ADK user id
only from an authenticated principal" (d0c4060) applies to the A2A request
converter only; it authenticates nothing on those HTTP routes. Keep them
behind IAP or the application's verified-principal dependency, or on internal
ingress. A test that sends a different caller-supplied `user_id` checks lookup
partitioning, not cross-user security; a cross-user claim needs distinct
authenticated principals at the real boundary.
<!-- /shared:verified-principal -->

Map the browser credential to a validated issuer/project, tenant where applicable and subject. Configure expected Firebase project and tenant behaviour explicitly if that provider is selected. In an ADK web application, the verified-principal dependency every `/api` router shares, with its IAP and Firebase verifier code, is built by `adk-fastapi-backend`.

Preserve an existing cookie-based identity boundary, including its CSRF/origin protections, rather than replacing it with the lab's bearer-token flow. Initialise identity clients under the selected worker lifecycle and fail startup when required trusted configuration is missing. Inventory alternate entrypoints such as development UIs, direct Runner calls and administrative routes: a session created by `adk web` is not automatically an authenticated application session.

Carry the same trusted identity into the tool and credential repository; do not introduce a version migration to change a valid accessor. If adding a server-created identity-state consistency guard, initialise it in session creation too. It is not a browser credential.

Inspect model-visible tool declarations, not just Python parameters: frameworks inject some arguments. A tool must not let model text select another user's credential or an arbitrary authenticated URL. Constrain operations/resources deterministically. When the tool is served by MCP Toolbox for Databases, bind the tenant or customer id as a `secure` parameter in code (`toolbox-adk` `secure_params=` or `bind_secure_param`): it is removed from the declaration the model sees, travels in the `secureArguments` field of the call, and a model that supplies it in ordinary arguments gets a tool error; Toolbox's documentation reserves secure parameters for client-supplied runtime context and keeps database credentials in the source configuration, and its client authenticates to the server with `CredentialStrategy.workload_identity(target_audience=<server URL>)` or the ADK-native user flow (mcp-toolbox v1.14.0, `docs/en/documentation/configuration/tools/_index.md` and the Python ADK SDK page, read 2026-10-22; vendor documentation). Check user/tenant ownership alongside an object locator, and recheck on history, cancellation and continuation routes that exist. Retain any required write confirmation/idempotency boundary.

Fail closed on missing identity, ambiguous credential selection, insufficient scope or unavailable policy. Do not fall back to an application-wide administrator credential. Validate argument types as well as ranges: booleans and fractional values are not valid integer limits; malformed timestamps should produce a safe invalid-argument outcome before credential/provider work. Bound provider text before sending it to the model or storing it. Authenticated Calendar titles and other external content remain untrusted data; they cannot authorise a second tool or bypass a write confirmation.

## Preserve identity across a service hop

For a separate gateway, agent or tool service, authenticate the calling workload and the forwarded user context independently. A caller ID token authenticates the service; it does not establish the end user's authority. Use a supported authenticated delegation mechanism, or a trusted short-lived assertion whose issuer, signature, receiver audience, expiry and applicable tenant/subject bindings the receiver validates. Define replay handling for the operation. A plain `X-User-ID` from an untrusted caller is not that assertion.

Test forged, expired, wrong-audience and replayed assertions as well as valid callers requesting another user's resources. Recheck authorisation at the receiver. This is production guidance: the companion's combined process does not implement or verify a gateway-to-runtime assertion protocol.

When Identity-Aware Proxy fronts the agent, the assertion is the `x-goog-iap-jwt-assertion` header: an ES256 JWT verified against the keys at `https://www.gstatic.com/iap/verify/public_key-jwk`, with `iss` equal to `https://cloud.google.com/iap`, `aud` equal to `/projects/PROJECT_NUMBER/global/backendServices/SERVICE_ID` for a Compute Engine or GKE backend service (`/projects/PROJECT_NUMBER/apps/PROJECT_ID` on App Engine), `exp` in the future and `iat` in the past with 30 seconds of skew, and the user taken from `sub` and `email` in the token rather than from the `x-goog-authenticated-user-*` headers (https://docs.cloud.google.com/iap/docs/signed-headers-howto, updated 2026-10-20, read 2026-10-22). A tenant is not an IAP claim; map the verified subject or hosted domain (`hd`) to a tenant in trusted code, and record that mapping as a decision. When Google Cloud API Gateway fronts the agent, the supported assertion is `X-Apigateway-Api-Userinfo`: the gateway verifies the client JWT, forwards its payload in that header as `base64url` JSON, and replaces the incoming `Authorization` header with its own OIDC token for the backend whenever `x-google-backend` is set, so the backend must read user claims from `X-Apigateway-Api-Userinfo` and never from `Authorization` ([API Gateway JWT docs](https://docs.cloud.google.com/api-gateway/docs/authenticating-users-jwt), read 2026-10-21). Two consequences (Google's `api-gateway-backend-security-and-rate-limiting` skill, read 21 October 2026): a Google ID-token scheme admits every Google identity that can mint a token for that audience, so the backend checks the `email` claim; and the gateway's `*.gateway.dev` default hostname cannot be disabled, so a load balancer, Cloud Armor or IAP in front of it is not the boundary. Lock the backend down in this order: gateway service account with `roles/run.invoker`, then the API config with `--backend-auth-service-account`, then `--no-allow-unauthenticated` on the backend. When that gateway is being provisioned or rate limited, consult the installed Google skill `api-gateway-backend-security-and-rate-limiting` (from google/skills); if it is not installed, adk-engineer explains how to get it.

## Project output; do not dump events

Consume the invocation according to its completion/cancellation contract. A final response can still contain thought-marked parts; allowlist public text and exclude those parts. Do not serialise the entire event, auth configuration, state delta, function arguments/results, callback URL or request headers to create a public response. A streamed UI should use a small trusted application event schema, with correlation retained server-side. Below google-adk 2.12.0 the framework's own serving endpoints (`/run`, `/run_sse`, `/run_live`, the dev server and the session endpoints) could expose OAuth2 secrets; 2.12.0 fixes that (see [compatibility and evidence](compatibility-and-evidence.md)), which makes the projection here a second guard rather than the only one. Those endpoints still take a caller-supplied user id on 2.12.0: its user-id fix applies to the A2A request converter only.

The optional `assets/public_text.py` adapter accepts trusted ADK-like event objects and returns final text or `None` for a non-final event. It rejects malformed shapes and enforces an explicit character cap. Its async collector consumes later events too. Preserve the application's existing streaming/cancellation semantics when adapting; do not replace a streaming UI with final JSON merely because the companion used JSON.

Projection is **not secret detection**: if a credential has already entered allowlisted public text, the adapter cannot identify it. Keep credentials upstream of the model and apply the target's content policy. Tests deliberately demonstrate this limitation. The adapter is not a whole-application confidentiality guarantee.

## Protect separate logging/export boundaries

Sanitise model/provider exceptions at the point before framework logging can capture raw payloads. A generic gateway 503 may occur too late. Test both framework logs and public output with synthetic exception canaries. Preserve diagnostic codes/opaque operation correlation without copying exception bodies.

The tested ADK 2.8.0 repair uses `on_model_error_callback` to raise a fixed safe exception `from None` before Runner logging. A safe message raised `from exc` can still include the original payload in a formatted traceback. Keep the real Runner in the regression test and substitute only the failing model transport/generator. Custom exporters may inspect exception objects or captured request bodies directly, so suppressing traceback chaining alone is not a universal redactor.

Give Runner, session service and provider clients explicit application-lifespan ownership. Close supported components on shutdown/failure, using `finally` ordering so one close failure does not skip the rest. Await relevant exporter flushing before judging canary absence. Protect OAuth callback query strings at ingress, proxy and application access logs; the lab's `--no-access-log` only controls its Uvicorn access logger.

Use allowlisted audit fields under the project's privacy policy. Stable opaque user IDs are still linkable; do not claim anonymity. Configure trace export/linkage deliberately and keep high-cardinality correlation out of metric labels. For ADK 2.8.0's legacy span-content path, explicitly configure `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` when content capture is prohibited; inspect other overrides/exporters too. That flag does not sanitise custom instrumentation or analytics. Treat `temp:` as a lifetime scope, not confidentiality or universal redaction.

Secret access auditing has its own configuration and attribution boundary; read [GCP auditability](gcp-credentials.md#audit-payload-access-deliberately) when cloud payload-read evidence is required.

Completion requires tests showing an owner mismatch denies before provider access, a forged tool/request identity cannot change ownership, non-public canaries do not enter public output, and relevant error/export boundaries preserve the policy. See [validation](validation.md). The historical companion does not establish full Firebase or every-exporter compliance; see [evidence](compatibility-and-evidence.md).
