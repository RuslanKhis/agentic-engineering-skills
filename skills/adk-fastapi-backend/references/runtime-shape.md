# Run-time shape on Cloud Run

Read before writing the Dockerfile, start command or service settings. Hosting
topology, ingress and IAM belong to `deploy-adk-on-google-cloud`; this file
covers what the application process must do.

- **One process per container.** `fastapi run app/main.py --port $PORT` runs
  a single Uvicorn process unless `--workers` or `WEB_CONCURRENCY` is set;
  leave both unset. FastAPI's deployment docs advise one process per container
  on cluster platforms; Cloud Run scales by instances. Templates that pass
  `--workers 4` are wrong for this shape.
- **Explicit timeout and concurrency.** Set the Cloud Run request timeout
  above the longest run (default 300 s, maximum 3,600 s) and concurrency no
  higher than the process admits. At POC depth run one instance, so a
  per-user run lock can live in process (SB19); beyond one instance it needs a
  shared store.
- **Reconnects attach, never resubmit.** Cloud Run ends a request at its
  timeout and may send the reconnect to another instance; the client attaches
  to the recorded run (`adk-frontend-integration`).
- **Work after the response.** Under request-based billing (the default,
  formerly "CPU only allocated during request processing") an instance gets no
  CPU once the response is sent, so `BackgroundTasks` may never finish. Work
  the user must not lose goes to Cloud Tasks with an idempotent handler.
- **Streams pass through untouched.** No `Content-Length` and no compression
  on `text/event-stream` (Starlette's `GZipMiddleware` already skips it); do
  not wrap stream responses in middleware that reads the body.
- **Lifespan owns clients.** Create the Runner, session service, database
  engine and verifier in the lifespan, not at import, so the app imports and
  dumps its OpenAPI document with no credentials.
- **One telemetry exporter owner.** With google-adk 2.12.0 FastAPI resolves
  below 0.142, so ADK's set-up owns the exporter. On a stack where FastAPI's
  native telemetry is available, leave its automatic exporter off
  (`FASTAPI_OTEL_AUTO_CONFIGURE` unset) and keep one owner
  (`adk-agent-observability`). FastAPI's exception logs fall under
  `protect-adk-sensitive-data`.
- **Settings from the environment.** `pydantic-settings` with a value-free
  `.env.example`; secrets from Secret Manager or the environment, never in
  `VITE_` variables, the bundle or prompts (SB16).
