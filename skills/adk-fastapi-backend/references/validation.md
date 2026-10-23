# Validation

Read before writing or running tests for a changed boundary. Drive the app
with its lifespan running, because the Runner, session service and verifier
are created there:

- `with TestClient(app) as client:` (FastAPI's test client), or
- `httpx.AsyncClient(transport=httpx.ASGITransport(app=app))` inside
  `asgi_lifespan.LifespanManager(app)` for async tests.

Replace the model with a scripted `BaseLlm` subclass that counts calls, so a
test can assert "no model call". Replace the verifier with a dependency
override for ownership tests, and monkeypatch the provider call (for example
`firebase_admin.auth.verify_id_token`) to test the real verifier's error
mapping. Keep real FastAPI, Runner, session service and database.

| Test | Expected result | Rule |
| --- | --- | --- |
| No verifier configured | Every `/api` route returns 401; health and SPA assets still load; no model call | SB01 |
| Missing, expired, wrong-audience or malformed token | 401 with `WWW-Authenticate` | SB02 |
| Verifier outage (key fetch fails) | 503, no sign-in prompt | SB13 |
| Unsigned IAP identity headers without the assertion | 401 | SB02 |
| A body naming another `user_id` | The run happens in the caller's own scope; the other user has no new session | SB03 |
| Two users, same record or session ID | The other user gets the same 404 body as an unknown ID, with no model call | SB03, SB04 |
| ADK paths (`/run`, `/run_sse`, `/run_live`, `/list-apps`, `/apps/...`, `/dev-ui/`) with JSON and browser `Accept` | No ADK data, no docs UI, no schema, no model call; under `/api` a JSON 404, never the shell | SB05 |
| OpenAPI dump in a process with no credentials | Exits 0; regenerating the client leaves no diff; ADK routes absent | contract |
| `alembic upgrade head` then `alembic check` on a database that holds ADK's tables | Clean; ADK table definitions unchanged | data |
| A forced exception | Generic 500 with a request ID; no stack, SQL or provider text | SB13 |
| Deployed settings | `/docs`, `/redoc`, `/openapi.json` serve neither docs nor schema; `nosniff`, CSP with `frame-ancestors 'none'`, `Referrer-Policy` and HSTS present | SB07 |
| Preflight from an unlisted origin | No `Access-Control-Allow-Origin` | SB06 |
| Oversize body; over-long or unknown fields; malformed ID | 413 or 422 | SB09 |
| Disallowed upload type or size; an uploaded HTML file | Rejected; never rendered from the app's origin | SB11 |
| A fetch route given the metadata address or name, or a redirect to them | Refused before any request leaves | SB12 |
| A denied request (internal tool and above) | One log line with principal, route and request ID; no message content | SB14 |
| `make check` | Runs the Python and JavaScript audits and the secret scan | SB15, SB16 |
| From MVP: a revoked token on a sensitive action (`check_revoked=True`) | 401 | SB20 |
| From MVP: Schemathesis over the non-agent routes | No 5xx | SB09 |

A passing local suite proves the application's boundaries, not IAP, Firebase
key rotation or Cloud Run behaviour; record those as unverified until an
authorised live run.

## This skill's own checks

- Helper: `python -m unittest discover -s tests -p 'test_*.py'` from the skill
  directory (offline, standard library).
- SDK contracts: `python -m unittest discover -s tests -p runtime_contracts.py -v`
  in an environment with the versions in [compatibility](compatibility.md).
  On 23 October 2026 all 8 passed on google-adk 2.12.0 and FastAPI 0.141.1:
  the `app.frontend()` fallback (shell for browser navigation under `/api` and
  `/docs`, JSON 404 otherwise, disabled by a `404.html`, no `dependencies`
  argument), ADK's server letting an anonymous client create and list another
  user's sessions, a fail-closed dependency keeping rejected calls away from
  the model, `DatabaseSessionService`'s five tables and Alembic's unfiltered
  drop proposal, Firebase's error-class order, and ADK's OpenTelemetry cap.
- The scratch application that exercised the full recipe (24 tests) is not
  shipped; its shape is the layout in `adk-system-designer`'s web application
  defaults.
