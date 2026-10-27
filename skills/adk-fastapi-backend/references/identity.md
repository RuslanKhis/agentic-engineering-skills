# Identity: the verified-principal dependency

Read when building or reviewing how `/api` routes learn who is calling. This
file is the toolkit's only home for the IAP and Firebase verifier facts;
`adk-tool-auth-and-secrets` holds the principle (one internal principal;
signature, issuer, audience and expiry checked; outage handled apart from an
invalid credential) and tool credentials.

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

## Shape

```python
@dataclass(frozen=True)
class Principal:
    subject: str          # the owner key used in every query and ADK call
    email: str | None = None

class InvalidCredential(Exception): ...     # 401, ask to sign in again
class VerifierUnavailable(Exception): ...   # 503, no sign-in prompt

async def get_principal(request: Request) -> Principal:
    verifier = getattr(request.app.state, "verifier", None)
    if verifier is None:                                   # fail closed (SB01)
        raise HTTPException(401, "sign in required", headers={"WWW-Authenticate": "Bearer"})
    try:
        return await run_in_threadpool(verifier.verify, dict(request.headers))
    except InvalidCredential:
        raise HTTPException(401, "sign in required", headers={"WWW-Authenticate": "Bearer"})
    except Exception:                                      # an error in auth denies (SB13)
        raise HTTPException(503, "identity check unavailable")

CurrentPrincipal = Annotated[Principal, Depends(get_principal)]
```

Create the verifier in the lifespan from settings, never at import, so the
OpenAPI dump runs without credentials. Attach the dependency to every `/api`
router; leave only static assets and a health check public. Tests replace it
with `app.dependency_overrides[get_principal]`, and that override never exists
in a deployed build.

## IAP

- Read only the signed assertion header `x-goog-iap-jwt-assertion` (ES256).
  Verify it with `google.oauth2.id_token.verify_token(assertion,
  google.auth.transport.requests.Request(), audience=AUDIENCE,
  certs_url="https://www.gstatic.com/iap/verify/public_key")`; the issuer is
  `https://cloud.google.com/iap`. Use its `sub` as the subject and `email` for
  display.
- Audience: IAP enabled directly on Cloud Run uses
  `/projects/PROJECT_NUMBER/locations/REGION/services/SERVICE_NAME`; behind a
  load balancer it is `/projects/PROJECT_NUMBER/global/backendServices/SERVICE_ID`.
  Confirm against a captured token in the first goal that uses it.
- Never trust `X-Goog-Authenticated-User-Email` or `-Id`: they are unsigned
  and can be forged when IAP is bypassed. With a load balancer, restrict
  `run.app` ingress so it cannot be bypassed (`deploy-adk-on-google-cloud`).
- Allow access with an IAP group binding, not per-user grants.
- Not verified: whether IAP enabled directly on Cloud Run supports external
  identities (Identity Platform); Google's pages are silent either way. Use
  Firebase or Identity Platform tokens for external users until it is settled.

## Identity Platform or Firebase Authentication

- The browser signs in with the Firebase web SDK and sends the ID token as
  `Authorization: Bearer <token>` with `fetch` (never in a URL, never through
  native `EventSource`, SB08).
- Verify with `firebase_admin.auth.verify_id_token(token,
  check_revoked=False, clock_skew_seconds=0)`; `clock_skew_seconds` accepts
  0–60. It is synchronous and may fetch keys, so call it off the event loop.
  Use `claims["uid"]` as the subject.
- Error mapping: `ExpiredIdTokenError` and `RevokedIdTokenError` are
  subclasses of `InvalidIdTokenError`, so catch them before it or together
  with it; these, `UserDisabledError` and `ValueError` (malformed) are
  invalid credentials. `CertificateFetchError` is an outage.
- `check_revoked=True` costs a lookup per call; use it before sensitive actions
  (SB20, from MVP) rather than on every request.
- The Firebase web API key is a public identifier by design. Allowlist it in
  the secret scan and restrict it in the console (SB16).
- An allowlist of users or domains for a POC lives in the dependency, checked
  after verification.

## Local development

A test principal comes from a dependency override in tests, or a settings
flag that only a local environment accepts and a deployed build refuses at
start-up. A hard-coded user in the browser or in the request body is never the
mechanism.
