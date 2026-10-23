# Sources

Read 23 October 2026 unless stated. Facts are paraphrased; nothing is copied.

- FastAPI [release notes](https://github.com/fastapi/fastapi/blob/master/docs/en/docs/release-notes.md):
  SSE in 0.135.0, `app.frontend()` in 0.138.0, frontend dependencies in
  0.139.0, native OpenTelemetry in 0.142.0, opt-in exporter in 0.143.0; current
  0.161.1. `fastapi/sse.py` (15 s ping) and `fastapi/routing.py`
  (`_FrontendStaticFiles`, navigation detection) read in the 0.141.1 and
  0.161.1 wheels. [Docker deployment docs](https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md)
  (one process per container). MIT.
- FastAPI [bundled skill](https://github.com/fastapi/fastapi/tree/master/fastapi/.agents/skills/fastapi)
  and [library-skills](https://pypi.org/project/library-skills/) 0.0.19.
- google-adk 2.12.0: [`cli/fast_api.py`](https://github.com/google/adk-python/blob/main/src/google/adk/cli/fast_api.py)
  (non-loopback warning only with `bind_host`; `trigger_auth_verifier` for
  `/trigger/*`), [`cli/api_server.py`](https://github.com/google/adk-python/blob/main/src/google/adk/cli/api_server.py)
  (unauthenticated endpoints; `user_id` in path and body; `/run_sse` without
  keep-alive), [`sessions/database_session_service.py`](https://github.com/google/adk-python/blob/main/src/google/adk/sessions/database_session_service.py)
  and `sessions/schemas/v1.py` (five tables, `create_all`),
  [CHANGELOG](https://github.com/google/adk-python/blob/main/CHANGELOG.md) line
  for commit d0c4060 (A2A request converter only). Package metadata:
  `opentelemetry-api>=1.39,<=1.42.1`. Apache-2.0.
- ag-ui-adk 0.11.0 ([source](https://github.com/ag-ui-protocol/ag-ui/tree/main/integrations/adk-middleware/python)):
  `user_id_extractor` receives `RunAgentInput`; `add_adk_fastapi_endpoint`
  forwards `dependencies=` to the run route only. MIT.
- [IAP signed headers](https://docs.cloud.google.com/iap/docs/signed-headers-howto)
  (header, ES256, key URL, issuer, audience formats including Cloud Run);
  [IAP for Cloud Run](https://docs.cloud.google.com/run/docs/securing/identity-aware-proxy-cloud-run).
- [firebase-admin](https://firebase.google.com/docs/auth/admin/verify-id-tokens)
  7.7.0, `auth.verify_id_token` signature and error classes read in the wheel;
  [API keys for Firebase](https://firebase.google.com/docs/projects/api-keys) (public by design).
- [Cloud Run request timeout](https://docs.cloud.google.com/run/docs/configuring/request-timeout)
  (300 s default, 3,600 s maximum);
  [Cloud Run billing settings](https://docs.cloud.google.com/run/docs/configuring/billing-settings)
  (request-based billing allocates CPU only during requests).
- Starlette 1.9.0 `GZipMiddleware` (skips `text/event-stream`);
  [Alembic `include_object`](https://alembic.sqlalchemy.org/en/latest/api/runtime.html#alembic.runtime.environment.EnvironmentContext.configure.params.include_object);
  [oasdiff breaking changes](https://github.com/oasdiff/oasdiff/blob/main/docs/BREAKING-CHANGES.md);
  [Schemathesis](https://schemathesis.readthedocs.io/) 4.32.4;
  [`@hey-api/openapi-ts`](https://www.npmjs.com/package/@hey-api/openapi-ts) 0.99.0.
- Research behind this skill: `docs/research/fastapi-react-skills-2026-10-22.md`
  and `docs/research/web-app-baseline-proposal-2026-10-22.md` in the toolkit
  repository.
