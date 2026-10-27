I prepared the Cloud Run and IAP deployment but did not deploy it. The unit tests were not run either, because Bash is disabled in this session. I also made no cloud calls and no network requests.

**What I added**
- `Dockerfile`: builds the React app, then a Python 3.12 image with the pinned dependencies. It runs as a non-root user with one `fastapi run` process on `$PORT`. The source stays at `/srv` because `app/helpdesk.py` and `app.frontend()` find `help/` and `web/dist` relative to the repo root.
- `.dockerignore` and `.gcloudignore`: exclude `.env`, databases, `.claude`, tests, docs and `node_modules`.
- `deploy/RUNBOOK.md`: the assumptions, the blockers, the identity plan, the `gcloud` commands to review, the acceptance checks and a cleanup and ownership-journal outline.

No application code changed.

**Questions I couldn't ask, and what I assumed**
- **Project:** `harbour-support-dev`. The design doc says the platform team still has to confirm it.
- **IAP placement:** IAP directly on the Cloud Run service (`--iap`), with no load balancer.
- **Sizing:** concurrency 10, timeout 300 s, and exactly one instance (min 1, max 1). Sessions are in memory, so a restart or a second instance loses conversations.
- **Pilot access:** `support-pilot@harbour.example` gets `roles/iap.httpsResourceAccessor`.
- **Model backend:** Vertex AI through a new runtime service account. The Gemini model's availability in the chosen location is unchecked.

**Blockers before a real deploy**
1. **Order and refund data is in local SQLite** (`Store(settings.db_path)` in `app/agent.py`). On Cloud Run it is per-instance and wiped on restart, so orders would be empty. A refund is recorded only there after the payments call, so a lost record could allow a repeat refund. Decide on a durable store, and keep payments on a sandbox or refunds off until then.
2. **`web/package-lock.json` is missing**, so `npm ci` in the Dockerfile will fail until one is generated and committed.
3. **`IAP_AUDIENCE` can't be set until the service exists.** Until it is set, every `/api` call is rejected. Check the exact audience format for direct Cloud Run IAP in Google's docs first.
4. **Secrets and mail auth:** `PAYMENTS_API_KEY` should go in Secret Manager. I couldn't tell how the mail client authenticates.
5. **A project admin has to set up** the OAuth consent screen and the IAP and IAM bindings.

**Left undone**
- Local tests and the Docker build were not run.
- No resources were created.
- Deployment and live verification still need your approval of the concrete values in the runbook.