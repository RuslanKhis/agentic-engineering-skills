# Hosting plan (draft)

- Cloud Run service `research-agent`, project `sales-tools-prod`, region europe-west1,
  ingress internal-and-cloud-load-balancing, no unauthenticated access.
- Runtime identity: `research-agent@sales-tools-prod.iam.gserviceaccount.com`.
- Gemini Enterprise app lives in `sales-tools-prod` too.
- Open question from security: a remote peer's reply must never approve a procurement
  request on our side.
