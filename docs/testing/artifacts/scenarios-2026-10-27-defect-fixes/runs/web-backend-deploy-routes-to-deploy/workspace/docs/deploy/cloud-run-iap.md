# Deploy: support assistant on Cloud Run behind IAP (pilot)

Status: prepared, **nothing has been run against any cloud project**. Every command below needs
explicit approval of the exact values before execution. Topology A from the design
(`docs/architecture/support-web.md`): one Cloud Run service, IAP enabled directly on the service.

## Questions that were not answered (assumptions used)

| Question | Assumption |
| --- | --- |
| Which project? Design says "to be confirmed by platform team"; `harbour-support-dev` is ours | Use `harbour-support-dev` for the pilot; confirm before any command |
| Who is the pilot group? | Google group `support-pilot@harbour.example` (25 people) gets `roles/iap.httpsResourceAccessor` on the service |
| Is the pilot allowed to use real payments/mail? | No. Point `PAYMENTS_BASE_URL` / `MAIL_BASE_URL` at sandbox endpoints; `issue_refund` sends real money otherwise |
| Where does order data come from? | Unknown. `app/store.py` is a local SQLite file; see blockers |
| Concurrency / timeout (design: undecided) | `--max-instances 1`, `--concurrency 8`, `--timeout 300` |
| IAP on service or load balancer? (design: undecided) | On the service (topology A, simplest). Revisit if Cloud Armor/WAF is required |

## Blockers to resolve before a pilot with real use

1. **Sessions are `InMemorySessionService`.** They vanish on restart/scale-in and are not shared
   between instances. The pilot therefore pins `--max-instances 1`; a restart loses open chats.
   Durable sessions need a database session service (separate change).
2. **Orders, profiles and refunds live in `support.db`, a SQLite file in the container.** It is
   empty on every new instance and the refund record is lost on restart, so refund history and the
   duplicate-refund check do not survive. Needs Cloud SQL (or an agreed seeded read-only copy) and
   a migration before refunds are enabled. Until then set `SUPPORT_DB_PATH=/tmp/support.db`
   and treat the pilot as read-only/sandbox.
3. **`web/package-lock.json` is missing**, so the Dockerfile's `npm ci` fails. Generate and commit it
   (`npm install --package-lock-only` in `web/`); not done here (no network).
4. **IAP audience** `/projects/PROJECT_NUMBER/locations/europe-west2/services/SERVICE_NAME` must be set as
   `IAP_AUDIENCE`; confirm against a captured live token on the first run. Without it every `/api` call returns 401.
5. `IAP_AUDIENCE` and the sandbox URLs are not secrets; `PAYMENTS_API_KEY` is: use Secret Manager.
6. **Project number and `app.frontend()` behaviour** were not verified locally (SDK not installed).

## Variables

```bash
PROJECT_ID=harbour-support-dev        # confirm
REGION=europe-west2
SERVICE=support-assistant
RUNTIME_SA=support-assistant-run@$PROJECT_ID.iam.gserviceaccount.com
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')
```

## Plan (each step is a separate approval)

Read-only first: active account/project, enabled APIs (run, cloudbuild, artifactregistry, iap,
aiplatform, secretmanager), existing service `$SERVICE`, org policy on IAP/domain restriction.

Mutations, in order:

1. Enable missing APIs (billing-affecting; list only the missing ones).
2. Create runtime service account `$RUNTIME_SA`; grant `roles/aiplatform.user` (model) and
   `roles/secretmanager.secretAccessor` on the one secret only.
3. Create the `PAYMENTS_API_KEY` secret (sandbox key supplied by the owner; never in this repo).
4. Deploy from source (Cloud Build uses the Dockerfile; requires the lockfile):

```bash
gcloud run deploy "$SERVICE" --project "$PROJECT_ID" --region "$REGION" --source . \
  --service-account "$RUNTIME_SA" \
  --no-allow-unauthenticated --iap \
  --ingress all \
  --min-instances 0 --max-instances 1 --concurrency 8 --timeout 300 \
  --set-env-vars "GOOGLE_GENAI_USE_ENTERPRISE=True,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=global,SUPPORT_DB_PATH=/tmp/support.db,IAP_AUDIENCE=/projects/$PROJECT_NUMBER/locations/$REGION/services/$SERVICE,PAYMENTS_BASE_URL=<sandbox>,MAIL_BASE_URL=<sandbox>" \
  --set-secrets "PAYMENTS_API_KEY=payments-api-key:latest"
```

   `--iap` is a gcloud beta/GA flag depending on version; check `gcloud run deploy --help`.
   Model backend env names and location must match the installed ADK 2.12 / google-genai 2.21
   contract (`GOOGLE_GENAI_USE_ENTERPRISE` follows the deploy skill's tested ADK 2.8 example;
   verify against the pinned SDK, and confirm `gemini-3.5-flash` is served in that location).
5. IAP access for the group, and the IAP service agent invoker role:

```bash
gcloud iap web add-iam-policy-binding --project "$PROJECT_ID" --region "$REGION" \
  --resource-type=cloud-run --service "$SERVICE" \
  --member "group:support-pilot@harbour.example" --role roles/iap.httpsResourceAccessor
# IAP service agent needs roles/run.invoker on the service:
#   service-$PROJECT_NUMBER@gcp-sa-iap.iam.gserviceaccount.com
```

IAP on a service uses the `run.app` URL; with `--ingress all` that URL is directly reachable, but
`--no-allow-unauthenticated` plus IAP means requests without IAP identity are rejected, and the
app additionally verifies the signed assertion.

## Acceptance checks at the deployed URL (not run)

- Signed out / no assertion: every `/api` route returns 401/redirect, unknown `/api/x` is 404 (not the SPA shell), no ADK routes or docs answer.
- A pilot member signs in via IAP, SPA loads, `POST /api/chat` returns a reply and a second message in the same `session_id` recalls the first.
- Two different pilot accounts cannot load each other's `session_id`.
- A non-member Google account is refused by IAP.
- Revision shows the intended runtime SA, env keys, secret reference, max-instances 1.

## Cleanup (separate confirmed operation, resources created by this deployment only)

Delete the Cloud Run service, the runtime SA and its bindings, the secret, the IAP binding, and the
source/`cloud-run-source-deploy` images this deployment created. Do not delete shared buckets or
repositories; record exact identities in a journal when provisioning.
