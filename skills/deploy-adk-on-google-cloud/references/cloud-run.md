# Cloud Run: native ADK or an application container

Read this when deploying, reviewing or adapting an ADK agent for Cloud Run. Apply the [shared lifecycle and approval gates](../SKILL.md). Prepare concrete configuration, commands, IAM changes and cleanup before requesting any missing approval; perform cloud mutations only within the user's explicitly approved scope.

**Evidence boundary.** Native ADK and custom Docker paths were exercised live with ADK 2.8.0. Both passed actual browser routing, explicit recall and direct connection recovery. The custom image also passed telemetry opt-out and page reload. Fresh-project API activation, production tenant authorisation and replacement durability were not established. Resolve current versions and flags using the compatibility reference before adapting this recipe.

## 1. Choose the serving boundary

- **Native ADK:** use the installed CLI's generated API server when its supported routes and packaging meet the task. Inspect `adk deploy cloud_run --help` and passthrough arguments; generated packaging is version-sensitive.
- **Custom container:** use the repository's existing FastAPI/ASGI application or create an explicit wrapper when custom routes, middleware or dependencies are needed. Inspect its actual ADK app discovery and HTTP contract instead of inferring these from the agent's internal name.
- The tested app was discovered as the package `support_agent`, while its agent object was named `support_triage_agent`. Query `/list-apps` through authorised transport before constructing session URLs.
- ADK's bundled UI is a development/testing interface. Keeping it private is appropriate for an operator walkthrough. A production frontend and an API-only serving configuration are separate adaptations requiring their own tests.

Done when the selected mode, app name, callable endpoints, runtime entrypoint and session backend are recorded.

## 2. Resolve identities, locations and packaging

Read the active account, project, enabled APIs, billing/quota prerequisites and existing resources. In the tested path the required API set included Run, Cloud Build, Artifact Registry, Vertex AI, IAM, Storage, Resource Manager and Logging. API activation is a mutation; record only the missing APIs intended for the approved plan.

Keep the hosting/build region separate from the model endpoint. The tested model used `global`; do not replace a repository's current supported model settings from this historical example.

Resolve Cloud Build's actual account in the submission region:

```bash
gcloud builds get-default-service-account \
  --project="$PROJECT_ID" --region="$DEPLOYMENT_REGION" \
  --account="$OPERATOR_ACCOUNT" --billing-project="$PROJECT_ID"
```

Map the deployer, build service account, runtime service account and caller independently. The runtime needs model/tool access; the caller needs service invocation. A local reader that resolves service metadata also needs permission to inspect it. Build rights do not grant runtime inference rights. The tested setup's project-wide build roles were broad lab permissions; propose narrower resource-scoped permissions or a named build identity for production and verify effective access.

Prepare a sanitised upload directory and inspect its file list. Exclude local `.env`, credentials, keys, state, sessions, logs and unrelated source from the upload *and* Docker context. Inspect native ADK's package ignore mechanism separately. Use workload IAM in managed deployment; remove inherited developer API keys from build/deploy subprocess environments.

For custom containers, check the listener uses `0.0.0.0` and the configured port; inspect the actual command instead of assuming `PORT` controls a hardcoded Uvicorn argument. Run as a non-root user. If the SDK writes configuration under its home directory, create that writable home: a missing home caused real telemetry opt-out HTTP 500s. Do not mistake a host-file repair for a rebuilt deployed image.

Done when source exclusions, actual build identity, runtime grants and every deployment variable have concrete reviewed values.

## 3. Construct and execute the chosen deployment

The fragments below show tested command shapes with generalised variable names. Resolve each variable, inspect local help, add required resource ownership recording and obtain any missing approval before running mutations. They are not a complete provisioning script.

Native ADK's tested private development deployment used:

```bash
CLOUDSDK_CORE_ACCOUNT="$OPERATOR_ACCOUNT" \
GOOGLE_CLOUD_QUOTA_PROJECT="$PROJECT_ID" \
adk deploy cloud_run \
  --project="$PROJECT_ID" --region="$DEPLOYMENT_REGION" \
  --service_name="$SERVICE_NAME" --app_name="$APP_NAME" \
  --with_ui "$AGENT_DIR" -- \
  --service-account="$RUNTIME_SERVICE_ACCOUNT" \
  --build-service-account="projects/$PROJECT_ID/serviceAccounts/$BUILD_SERVICE_ACCOUNT" \
  --no-allow-unauthenticated
```

Inspect the native source staging bucket, service-specific upload prefix and generated image repository before submission. Some SDK resources have fixed names; their existence does not authorise adoption or deletion. Journal accepted source generations, build identity, resolved image and service UID. Existing shared infrastructure requires an explicit reuse plan.

The tested custom route used a reviewed Cloud Build configuration that built, pushed and deployed one image:

```bash
gcloud builds submit "$SANITISED_SOURCE_DIR" \
  --project="$PROJECT_ID" --region="$DEPLOYMENT_REGION" \
  --account="$OPERATOR_ACCOUNT" --billing-project="$PROJECT_ID" \
  --config="$BUILD_CONFIG" \
  --service-account="projects/$PROJECT_ID/serviceAccounts/$BUILD_SERVICE_ACCOUNT" \
  --gcs-source-staging-dir="$OWNED_SOURCE_STAGING_URI" \
  --ignore-file="$UPLOAD_IGNORE_FILE"
```

Prepare the configuration's required substitutions explicitly; inspect whether it already deploys before adding another deploy step. Its deployed service must select the runtime account and authenticated invocation. The source-tested custom pipeline tagged by Cloud Build ID. Deploying an explicitly resolved digest, locking all dependencies with hashes and pinning a base-image digest are proposed production improvements, not features inferred from a unique tag.

After submission, verify the provider's terminal build state, actual build account, service Ready condition, revision/image and saved ownership identity. Preserve private logs and submission intent even when a CLI exits successfully: the tested native ADK CLI printed an explicit source-access rejection yet returned zero.

If that occurs, distinguish a rejected request from an accepted build or lost response. Inspect service absence, matching regional builds and exact source generation. IAM listing alone is not proof of effective access; propagation was plausible in the observed failure, not proven. The chapter's recovery authorised only an explicitly rejected archive with unchanged identity and no accepted build. Adapt that proof to the current repository before deleting an exact generation or resubmitting; an arbitrary deployment error does not satisfy it.

Done when provider evidence identifies the accepted image/revision and intended service; otherwise retain the pending state and reconcile.

## 4. Verify the actual caller and browser path

Use an identity token appropriate for the actual caller and service, without exposing it in logs, saved artefacts or command arguments. Verify denied anonymous/invalid credentials independently from successful authorised access. Cloud Run IAM gates service entry; caller-supplied ADK `userId` does not bind a conversation to that caller. Production user/session authorisation must be implemented separately.

For browser testing, exercise the documented transport end to end. The tested ordinary CLI-token route returned 401 with a custom OAuth client, while an authenticated gcloud proxy returned module 403s caused by origin handling. Inspect token audience/client, verified caller, Host and Origin before changing service policy.

The source-tested workaround was a narrowly scoped local bridge: bind exact loopback, accept only its exact Host and absent/exact local Origin, discard caller-supplied forwarding headers, translate to the resolved owned HTTPS service and preserve upstream IAM verification. It refreshed existing standard user ADC, checked the caller's verified email, held the short-lived token in a private temporary flags file and removed it on startup failure, expiry or shutdown. This is a specific tested workaround; adapt and test its trust boundary instead of treating origin rewriting as general advice or making the service public.

Check `/health`, then the real model/tool workflow, all intended routing outcomes and explicit same-session recall. Inspect structured results and grounded text: a classifier that selects a queue must not claim it filed a ticket or promised follow-up. Disconnect the actual local transport only within the agreed test scope, observe error feedback and usable input, restore it and retry only after establishing the first request was not accepted.

The observed SDK retained a failed local message bubble. Two bubbles alone did not prove two server actions. A lost response or accepted timeout needs server-side reconciliation, not automatic retry. Native optional telemetry/debug endpoints returned 404 despite a working core chat; custom telemetry persisted through a reload in the same instance only.

Done when the caller's real workflow and its measured limitations are recorded against the deployed revision.

## 5. Remove the owned deployment and verify

Inventory the services, image repositories, source archives/buckets, added IAM bindings and retained state created for this task. Default deletion in an unfamiliar repository may leave billable images or staging objects. Establish what its cleanup entrypoint actually removes before using it.

Delete only authorised owned resources, with immutable identities/generations checked immediately before mutation. Keep shared source buckets and pre-existing grants; remove exact owned source generations instead. Coordinate shared build-account grants until all relevant builds are terminal. An empty exclusive bucket needs its bucket deletion operation after its contents are removed; object removal is not bucket deletion.

For a service-account GET returning 403, require a successful complete project inventory excluding both recorded name and immutable UID before claiming absence. Permission failures and incomplete listings remain unknown. Repeat cleanup and independent provider reads must confirm the intended removals; retain the receipts.

Native in-memory sessions and custom `/tmp` SQLite are ephemeral. Local restart tests do not prove instance replacement or replica continuity. External sessions, artefact storage, IAP/custom frontend auth, least-privilege build policy and controlled egress remain production work unless the target repository implements and verifies them.
