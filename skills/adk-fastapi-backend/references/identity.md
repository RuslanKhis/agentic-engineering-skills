# Identity: the verified-principal dependency

Read when building or reviewing how `/api` routes learn who is calling. This
file is the toolkit's only home for the IAP and Firebase verifier facts;
`adk-tool-auth-and-secrets` holds the principle (one internal principal;
signature, issuer, audience and expiry checked; outage handled apart from an
invalid credential) and tool credentials.

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
