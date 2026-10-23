# Compatibility and version decisions

Read before relying on a version-gated FastAPI feature, and whenever the
project's FastAPI, ADK or ag-ui-adk version differs from the tested stack.
Record declared and resolved versions separately; the helper reads `uv.lock`.

## Tested stack

Exercised on 23 October 2026 with CPython 3.12.9 on macOS, against a scratch
application (FastAPI app factory, in-process Runner, scripted model, Alembic
migrations beside `DatabaseSessionService`) and this skill's
`tests/runtime_contracts.py`:

| Package | Version |
| --- | --- |
| google-adk | 2.12.0 |
| fastapi | 0.141.1 (the highest that resolves beside google-adk 2.12.0) |
| starlette | 1.9.0 |
| pydantic | 2.14.1 |
| pydantic-settings | 2.16.1 |
| sqlalchemy (asyncio) | 2.1.6, with aiosqlite 0.22.1 |
| alembic | 1.20.1 |
| firebase-admin | 7.7.0 |
| google-auth | 2.62.0 |
| httpx | 0.28.1; asgi-lifespan 2.1.0; pytest 9.1.1 |
| `@hey-api/openapi-ts` | 0.99.0 with typescript 5.9.3 (its peer dependency) |

What ran: 24 scratch-app tests (fail-closed principal, Firebase error mapping
with the verifier replaced, IAP unsigned headers refused, forged `user_id`,
two-user ownership, ADK paths, SPA fallback, docs and headers, CORS, size
limits, generic errors, credential-free OpenAPI dump, migrations beside ADK's
tables), 8 runtime contracts, and two client generations from the same dump
with no difference. Not run: real IAP or Firebase tokens, Cloud Run, oasdiff,
Schemathesis.

## FastAPI feature gates

From FastAPI's release notes, read 23 October 2026:

| Feature | First version |
| --- | --- |
| `fastapi.sse.EventSourceResponse`, with a `: ping` comment after 15 s idle, only when used as `response_class` on a path operation that yields | 0.135.0 |
| `app.frontend("/", directory="dist")` and `router.frontend(...)` | 0.138.0 |
| Dependencies applied to frontend routes, inherited from the app, router or `include_router` (`frontend()` itself takes no `dependencies` argument) | 0.139.0 |
| Native OpenTelemetry instrumentation | 0.142.0 |
| Automatic exporter set-up only with `FASTAPI_OTEL_AUTO_CONFIGURE=true` | 0.143.0 |

ag-ui-adk keeps its own SSE through `sse-starlette` (15 s pings), so an older
FastAPI still streams there; without `EventSourceResponse`, use
`sse-starlette` too.

## Known conflict: ADK 2.12.0 and FastAPI 0.142+

google-adk 2.12.0 requires `opentelemetry-api>=1.39,<=1.42.1`; FastAPI 0.142.0
and later require `opentelemetry-api>=1.44.0`. A resolver therefore picks
FastAPI 0.141.1 at most beside google-adk 2.12.0 (checked with uv on 23
October 2026; current FastAPI is 0.161.1). Consequences:

- FastAPI's native telemetry is unavailable; ADK's telemetry set-up is the
  one exporter owner.
- FastAPI's bundled skill describes the latest release; where it teaches a
  0.142+ feature, the locked version wins. Record the gap in Evidence.
- Lifting it is a version decision for ADK and FastAPI together, made when an
  ADK release widens the cap. Do not force-install around the resolver.

FastAPI 0.144–0.161 also brought breaking changes (`root_path` parameter
deprecated, `**extra` removed from parameter functions, form, null and default
handling changed); read the release notes before that move.

## Starlette's test client

Starlette 1.9 warns that using `httpx` with `starlette.testclient` is
deprecated in favour of `httpx2`. The tests still pass on httpx 0.28.1;
follow the project's choice and record the warning rather than switching
clients silently.
