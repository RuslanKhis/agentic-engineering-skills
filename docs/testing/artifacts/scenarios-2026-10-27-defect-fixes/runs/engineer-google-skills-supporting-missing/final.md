I wrote the deploy and cleanup scripts, but I couldn't run the unit tests or the docker build, so nothing is verified. The shell tool was disabled in this session. The ticket's status is `in-progress`.

**What I did**
- **Dockerfile:** the container now runs as a non-root user, with `/srv` writable for it.
- **`deploy/deploy.sh`:** creates the `support-agent-run` service account and deploys `support-agent` to `harbour-support-dev` in `europe-west2`. It sets ingress to `internal-and-cloud-load-balancing`, passes the payments key as a Secret Manager reference, and ends with readback commands.
- **`deploy/cleanup.sh`:** removes the service, the IAM bindings and the service account. It leaves the secret and the load balancer alone.
- **Dry run by default:** both scripts only print their `gcloud` commands unless you pass `--apply`.
- **Evidence section:** I filled it in with each check marked not run, and the open questions listed.

**Skill gap:** `google/skills:cloud-run-basics` isn't installed and nothing is available to find it. I took the ingress and service flags from `deploy-adk-on-google-cloud/references/cloud-run.md` instead. Check them against `gcloud run deploy --help` or the skill before approving.

**Assumptions I proceeded on, since nobody could answer**
- **IAP audience:** unknown, so `deploy.sh` requires `IAP_AUDIENCE` from the environment.
- **Secret name:** I assumed `payments-api-key` already exists.
- **Mail key:** the design says it comes from Secret Manager, but `MailClient` sends no credential. I assumed that's out of scope here.
- **Model settings:** `GOOGLE_GENAI_USE_VERTEXAI` and location `global` are copied from the skill's example. They aren't checked against ADK 2.12.0.
- **Load balancer access:** the load balancer's caller needs invoker rights on the service. I assumed the web platform team handles that with the serverless NEG.
- **No `.dockerignore`:** one isn't in the ticket's `touches` list, so I didn't add it. Local `__pycache__` or a `support.db` under `app/` would get copied into the image.

**Left undone**
- **Local checks:** the unit tests and the `docker build`.
- **Acceptance:** A1 and A2 need the `gcloud run services describe` readback after an approved deploy. A3 is only partly checked by reading the code. I haven't searched a built image for keys.
- **Deploy:** no cloud commands were run. Priya has to approve the exact commands before anything is applied.
- **Waits and cost:** the serverless NEG (W1) is still outstanding, and I didn't read the pricing page because I made no network requests.