# web-backend-deploy-routes-to-deploy: what the fixture holds

Bases: support-assistant (ADK app, FastAPI, IAP principal in `app/auth.py`) and support-web
(Vite React SPA in `web/`, DESIGN.md). Overlay:

- `app/server.py`: one FastAPI app, `/api` router with `dependencies=[Depends(current_principal)]`,
  an `/api` catch-all 404, docs/openapi off, `app.frontend("/", directory="web/dist")` — the
  designer's web defaults (topology A). Serves A1: the backend design is already done; the agent
  should lead with deployment, not redesign it.
- `pyproject.toml`: fastapi 0.138.0 (the release that has `app.frontend()`).
- `docs/architecture/support-web.md`: accepted design; region europe-west2; dev project
  `harbour-support-dev`; concurrency and request timeout undecided (A2 expects the agent to set
  one process per container with explicit timeout and concurrency); IAP placement undecided (A3:
  IAP signed assertion with the Cloud Run audience form, treated as a fact the first live run
  confirms).
- No Dockerfile, no deploy script, no Firebase config: anything the agent writes is new.
- No cloud credentials: A4 expects exact project/region/commands presented for approval and the
  live deployment reported as not run.

Original context (unchanged): "An ADK 2.12 web app built from the designer's web defaults: one
FastAPI app with the Runner in process, /api behind a verified-principal dependency, the SPA served
by app.frontend(); no cloud credentials in the session."
