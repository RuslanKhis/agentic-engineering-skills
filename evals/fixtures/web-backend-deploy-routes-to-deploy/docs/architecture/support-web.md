# Design: support assistant web app (pilot)

Status: accepted 2026-10-20

- One FastAPI app (`app/server.py`) runs the ADK Runner in process and serves the built React
  SPA from `web/dist` with `app.frontend()`; `/api` is behind the verified-principal dependency
  (IAP assertion) and unknown `/api` paths return 404 instead of the SPA shell.
- ADK's own `adk api_server` routes are not mounted.
- Identity: IAP on the Cloud Run service; the user ID comes from the assertion's `sub`.
- Pilot group: the 25 people in the support team's Google group `support-pilot@harbour.example`.
- Region: europe-west2. Project: to be confirmed by the platform team (dev project
  `harbour-support-dev` is ours).
- Build: `npm ci && npm run build` in `web/`, then the Python image.

## Not decided yet

- Concurrency per instance and the request timeout for long replies.
- Whether IAP sits on the service or on a load balancer.
