Nothing is deployed. I prepared the deployment files and a runbook, but made no cloud calls and ran no tests. Bash is disabled in this session, so the unit tests, the container build and the skill's `inspect_project.py` check were all **not run**. I also didn't confirm that `app.frontend()` exists in the installed SDK.

## What I added
- `Dockerfile`: a two-stage build with `npm ci` and `npm run build` in `web/`, then a Python 3.12 image running one non-root uvicorn process on `$PORT`.
- `.dockerignore` and `.gcloudignore`: exclude `.env`, `*.db`, `.claude`, tests, docs and `node_modules`.
- `docs/deploy/cloud-run-iap.md`: the unrun `gcloud` commands, the order of steps, acceptance checks and cleanup. The IAP setup is service-level, with the pilot group `support-pilot@harbour.example` getting `roles/iap.httpsResourceAccessor`.
- `app/` and `tests/` are untouched.

## Questions I couldn't ask, and what I assumed
- **Project:** I assumed `harbour-support-dev`. The design says the platform team still has to confirm it.
- **Payments and mail:** I assumed sandbox endpoints for the pilot, because `issue_refund` would otherwise move real money.
- **Limits:** I assumed `--max-instances 1`, concurrency 8 and a 300 s timeout. The design leaves these undecided.
- **IAP placement:** I assumed IAP on the service, not on a load balancer.

## Blockers before the pilot is useful
1. **Missing lockfile:** `web/package-lock.json` doesn't exist, so the Dockerfile's `npm ci` will fail. It needs `npm install --package-lock-only` in `web/` and a commit, which I couldn't do without network access.
2. **Sessions:** they live in memory, so a restart loses open chats and instances don't share them. That is why the plan pins one instance.
3. **Orders and refunds:** they live in a SQLite file inside the container. It starts empty and loses refund records on every restart, so refunds and the duplicate-refund check won't work. Refunds need Cloud SQL or similar before the pilot relies on them.
4. **IAP audience:** `IAP_AUDIENCE` must match the service. Until it's set, every `/api` call returns 401. Confirm it against a captured token on the first live run.
5. **Model settings:** the model backend env var and region come from the skill's ADK 2.8 example. Check them against ADK 2.12 and confirm `gemini-3.5-flash` is available in that region.

## Left undone
- Enabling APIs, creating the service account and secret, deploying, setting IAP access and every live check are not done. Each is listed in the runbook and needs approval of the exact values first.