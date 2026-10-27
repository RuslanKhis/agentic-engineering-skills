# Hosting a browser frontend with an ADK backend

Read when a deployment includes a web interface, or when choosing where the
browser's static files and the agent's run and stream paths are served. The
application side (principal dependency, routes, process shape) belongs to
`adk-fastapi-backend`; the stream contract to `adk-frontend-integration`.

## Topologies, simplest first

| | Topology | Use when | Watch |
| --- | --- | --- | --- |
| A | **One Cloud Run service** (default): FastAPI serves the built SPA with `app.frontend()` and `/api` on the same origin, Runner in process | A POC, internal tool or MVP | ADK's own routes are not mounted; an `/api` catch-all 404 stops the SPA fallback answering under `/api`; with IAP on the service the backend verifies the signed assertion against the Cloud Run audience `/projects/PROJECT_NUMBER/locations/REGION/services/SERVICE_NAME`, a fact the first live run confirms against a captured token |
| B | **Gateway in front of a private ADK service**: the public service authenticates and calls an internal-ingress ADK service with its own ID token | The agent is deployed separately | The private service accepts only the gateway's service account (`roles/run.invoker`); the gateway overwrites `user_id` |
| C | **Backend-for-frontend in front of Agent Runtime** | The agent runs on managed Agent Runtime | The BFF keeps session ownership; see [Agent Runtime](agent-runtime.md) |
| D | **Static assets on Firebase Hosting or Cloud Storage**, the SPA calling the Cloud Run URL directly | Assets need a CDN at public scale | Cross-origin: an explicit origin allowlist, never `*` with credentials; no run or stream path through Hosting |
| E | **External Application Load Balancer** with Cloud CDN for assets and IAP, `run.app` ingress restricted to internal and load balancer | Organisation-wide workforce access, WAF or Cloud Armor at the edge | IAP cannot be on both the load balancer and the service; IAP and Cloud CDN do not combine on one backend; the IAP audience is the backend service form, `/projects/PROJECT_NUMBER/global/backendServices/SERVICE_ID` |

## Stream and timeout rules

- **Firebase Hosting rewrites end at 60 seconds** with a 504, so no run or
  stream path goes through Hosting; Hosting serves assets only. Older community
  reports also say rewrites buffer whole responses; that is unconfirmed, and
  the 60-second limit already rules streams out.
- **Cloud Run's request timeout** defaults to 300 s and can be raised to
  3,600 s. Set it above the longest run. When a request is cut, a reconnect may
  reach another instance, so the client attaches to the recorded run instead
  of resubmitting it.
- **Keep-alive.** ADK's `/run_sse` sends no keep-alive. FastAPI's
  `EventSourceResponse` (as a path operation's `response_class`) and
  ag-ui-adk (through sse-starlette) send a `: ping` comment every 15 s, which
  page code cannot see; add a named heartbeat event the page can see and a
  client watchdog that reopens a silent stream.
- **No buffering.** No `Content-Length` and no compression on
  `text/event-stream`; a BFF pipes the stream without reading it. Assert the
  response headers in the deployed-path test.
- **One process per container** (`fastapi run`, no `--workers`), explicit
  concurrency, and, at POC depth, one instance so a per-user run lock can live
  in process.

## Checks at the deployed URL

- Signed out: every `/api` route is denied, and ADK's paths return no ADK
  data, no docs UI, no schema and cause no model call (the SPA shell for a
  browser navigation is acceptable).
- A stream longer than 60 seconds arrives with its first frame before
  completion and its heartbeat within the interval.
- No Hosting rewrite targets a run or stream path.

Sources, read 23 October 2026:
[Firebase Hosting and Cloud Run](https://firebase.google.com/docs/hosting/cloud-run) (60-second timeout, 504);
[Cloud Run request timeout](https://docs.cloud.google.com/run/docs/configuring/request-timeout);
[IAP for Cloud Run](https://docs.cloud.google.com/iap/docs/enabling-cloud-run) (direct IAP recommended; not with Cloud CDN);
[IAP signed headers](https://docs.cloud.google.com/iap/docs/signed-headers-howto) (audience formats);
ADK 2.12.0 `cli/api_server.py` (`/run_sse` is a plain `StreamingResponse`);
FastAPI `fastapi/sse.py` and sse-starlette 3.5.0 (15 s pings).
