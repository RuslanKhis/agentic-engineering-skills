I finished the local work for G04, but nothing has been deployed. The 11 offline unit tests pass, and the Evidence section and status are filled in. The tests ran on system Python 3.9.13 rather than the repository's 3.12. I made no cloud calls and no network requests, and I left the changes uncommitted.

**What I changed**
- **`Dockerfile`:** the container now runs as a non-root user, with a writable home and a writable SQLite path.
- **`.dockerignore`:** new, excluding `.env` files, key files, databases, docs and tests from the image.
- **`deploy/deploy.sh`:** new and review-only. It deploys with `--ingress internal-and-cloud-load-balancing`, `--no-allow-unauthenticated`, the `support-agent-run` service account, min instances 0, and Secret Manager references. It ends with a `describe` readback.
- **`deploy/cleanup.sh`:** new. It deletes only the Cloud Run service, after you type the service name to confirm.
- **`docs/tickets/support-agent/G04.md`:** Evidence section filled in, and status changed to `in progress`.

**Checked**
- The unit tests pass; both scripts only passed `bash -n` (syntax); I searched the repo for key literals and found none.
- A1 (ingress), A2 (runtime identity and roles) and A3 (no key in the image) are not verified. A1 and A2 need the readback after an approved deploy. A3 needs the image built and searched.

**Not done**
- **`docker build`:** not run. It needs the network to pull the base image and packages, and the Docker daemon was down. Run it locally before deploying.
- **`google/skills:cloud-run-basics`:** not installed, and I didn't invent its instructions. The service and ingress commands come from the repo's `deploy-adk-on-google-cloud` Cloud Run reference. To install it: `npx skills@latest add google/skills --skill cloud-run-basics`, restart the agent, then check `deploy.sh` against it.
- **Cloud steps:** the image push, `deploy.sh`, IAM and secret grants, and the readback all wait for Priya's approval of the exact commands. The serverless NEG and URL map wait on W1 (the web platform team).

**Open questions and my assumptions** (all listed in the ticket)
1. Payments secret name: I assumed `payments-api-key`, mounted as `PAYMENTS_API_KEY`.
2. Mail credential: the mail client sends none, but the design says mail credentials come from Secret Manager. I mounted nothing, and this needs a decision and a code change.
3. Image repository and tag: `IMAGE` is a required variable, so the script won't run without it.
4. `IAP_AUDIENCE`: supplied at deploy time, since the chat endpoint needs it.
5. Sizing: I set `--max-instances 3` and left CPU and memory at defaults.
6. Pricing: I didn't read the Cloud Run pricing page the ticket mentions.