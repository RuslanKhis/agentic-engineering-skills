# Cloud Run + IAP deployment runbook (pilot) — NOT YET EXECUTED

Nothing here has been run. Every step that mutates cloud state needs the
operator's explicit approval of the concrete values first.

## Assumptions (questions nobody could answer in the authoring session)

| # | Question | Assumption used |
|---|----------|-----------------|
| 1 | Which GCP project? The design doc says "to be confirmed by the platform team"; `harbour-support-dev` is ours. | Pilot goes to `harbour-support-dev` only. Do not use another project without the platform team's confirmation. |
| 2 | IAP on the service or on a load balancer? (undecided in `docs/architecture/support-web.md`) | IAP directly on the Cloud Run service (`--iap`): no load balancer to own for 25 users. Ingress stays `all`; IAP is the gate. Revisit if Cloud Armor/WAF is required. |
| 3 | Concurrency and request timeout | `--concurrency 10`, `--timeout 300`; `/api/chat` is not streamed. |
| 4 | Instance count | `--min-instances 1 --max-instances 1`: sessions are `InMemorySessionService`, so a second instance or a restart loses or splits conversations. Acceptable for a pilot, stated to users. |
| 5 | Pilot group | `group:support-pilot@harbour.example` gets `roles/iap.httpsResourceAccessor` on the service. |
| 6 | Region | `europe-west2`. Model location is unverified: `gemini-3.5-flash` must be available at the location in `GOOGLE_CLOUD_LOCATION`; check before deploying. |
| 7 | Model backend | Vertex AI with the runtime service account (no API key). |

## Blockers to resolve before a real deploy

1. **Data store is local SQLite.** `app/agent.py` opens `Store(settings.db_path)`
   (default `support.db`). On Cloud Run the filesystem is per-instance and lost
   on restart, so the `orders`, `profiles` and `refunds` tables would be empty
   or reset, and `issue_refund` records a refund only there after calling the
   payments provider. A lost refund record means the order can be refunded
   again. Decide where orders come from (seed, sync, or a durable database)
   and where refunds are recorded. Until then do not point `PAYMENTS_BASE_URL`
   at a live provider; use a sandbox or leave refunds disabled for the pilot.
2. **`web/package-lock.json` is missing**, and the Dockerfile uses `npm ci`.
   Generate and commit it (`cd web && npm install --package-lock-only`) with
   the pinned versions in `package.json`.
3. **`IAP_AUDIENCE` is only known after the service exists** (it contains the
   project number and service identity). With it empty, every `/api` call is
   rejected (fail closed). Confirm the exact audience string for direct Cloud
   Run IAP in the IAP signed-headers documentation before setting it, then
   redeploy with the variable set. A wrong value also fails closed.
4. **Secrets.** `PAYMENTS_API_KEY` goes in Secret Manager and is mounted with
   `--set-secrets`; never in `--set-env-vars`. Mail provider auth is not
   configured in `app/clients/mail.py`'s constructor; confirm how it
   authenticates.
5. **Pilot-group IAP access and the OAuth consent screen** (internal) need
   to exist in the project; a project admin does this.

## Identities

| Role | Identity |
|------|----------|
| Operator | the person running these commands (`$OPERATOR_ACCOUNT`) |
| Build | the Cloud Build service account resolved with `gcloud builds get-default-service-account` |
| Runtime | new `support-assistant-run@harbour-support-dev.iam.gserviceaccount.com`: `roles/aiplatform.user` and `roles/secretmanager.secretAccessor` on the one secret only |
| Callers | members of `support-pilot@harbour.example` (IAP), plus the IAP service agent with `roles/run.invoker` |

## Commands (to review, not run)

```bash
export PROJECT_ID=harbour-support-dev REGION=europe-west2 SERVICE=support-assistant
export RUNTIME_SA=support-assistant-run@$PROJECT_ID.iam.gserviceaccount.com

# 0. offline checks
python -m unittest discover -s tests -t .
(cd web && npm ci && npm test && npm run build)
docker build -t support-assistant:local .        # optional local image check

# 1. deploy (build in Cloud Build from the Dockerfile; no unauthenticated access)
gcloud run deploy $SERVICE --project=$PROJECT_ID --region=$REGION --source=. \
  --service-account=$RUNTIME_SA --no-allow-unauthenticated --iap \
  --min-instances=1 --max-instances=1 --concurrency=10 --timeout=300 \
  --set-env-vars=GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=<validated-location> \
  --set-secrets=PAYMENTS_API_KEY=support-payments-key:latest

# 2. grant the pilot group (after the audience/IAP setup is confirmed)
gcloud iap web add-iam-policy-binding --resource-type=cloud-run \
  --service=$SERVICE --region=$REGION --project=$PROJECT_ID \
  --member=group:support-pilot@harbour.example --role=roles/iap.httpsResourceAccessor

# 3. set IAP_AUDIENCE (value from the IAP docs for direct Cloud Run IAP) and redeploy
gcloud run services update $SERVICE --project=$PROJECT_ID --region=$REGION \
  --update-env-vars=IAP_AUDIENCE=<audience>
```

Use `--update-env-vars` for later changes so existing variables are kept.

## Acceptance checks (after approval and deploy)

- Signed out / outside the group: `/` and `/api/chat` are denied by IAP.
- A direct request to the `run.app` URL with no IAP assertion gets 401 from `/api`.
- In a browser as two different pilot users: each gets a reply, a follow-up
  in the same session recalls the earlier turn, and user B cannot load user
  A's `session_id` (new session is created instead).
- `lookup_order` for another user's order returns "not found" for the caller.
- Unknown `/api/x` returns 404 JSON, not the SPA shell.

## Journal and cleanup (fill in when something is created)

Record: service name and UID, image digest, runtime service account, secret,
IAM bindings added, build operation IDs, source staging object generations.
Cleanup is a separate approved step covering only those recorded resources:
delete the service, the added IAM bindings, the runtime service account, the
secret and the owned images/source objects, then re-read each to confirm.
