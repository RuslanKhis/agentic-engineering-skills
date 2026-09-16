# Connect, deploy and clean up a managed backend

Use this runbook when connecting either frontend contract to an existing Agent Runtime, or preparing an explicitly requested owned deployment. It does not require the book, companion scripts or another skill. Adapt the project's existing lifecycle tooling; the cloud commands below are ingredients for a resolved plan, not a bundled deployment wrapper. The version-specific baseline is ADK 2.8.0 and aiplatform 1.153.1; read [compatibility](compatibility.md) before using it with different pins.

| Requested outcome | Path |
| --- | --- |
| Connect an existing Runtime | Establish the caller/target in steps 1–2, then use steps 4–5. Preserve its deployment and ownership. |
| Create an owned test Runtime | Complete steps 1–3, then connect, verify and perform separately authorised cleanup. |
| Update an existing application | Record its exact identity and rollback information; obtain the requested update scope. An update does not transfer cleanup ownership. |
| Prepare a proposal or work without credentials | Complete local implementation, package inspection and offline tests. Report remote prerequisites as unverified. |

Respect approval already given for the exact targets and effects in the current task. Obtain a decision only for missing or expanded scope. API activation, IAM changes, deployment, paid verification and deletion are distinct effects; a deployment request does not implicitly authorise the others. Resolve their exact commands, bounds and retained resources before the applicable approval boundary.

## 1. Fix the target and interpreter

Run application commands from the target project with its existing environment active. Activate it again in each new backend terminal. Resolve the following inputs; the values below illustrate configuration, not an approved target:

```bash
PROJECT_ID=your-project-id
OPERATOR_ACCOUNT=operator@example.invalid
RUNTIME_REGION=us-central1
MODEL_LOCATION=global
export PROJECT_ID OPERATOR_ACCOUNT RUNTIME_REGION MODEL_LOCATION
```

Record the selected model in the application's actual model configuration. Runtime hosting location and Gemini inference location are independent. The recorded agent explicitly passed `client_kwargs={"location": "global"}` to its Gemini model; exporting a model/location variable works only if the deployed application reads it. Inspect nested configuration and inherited shell values without printing secrets.

For a new deployment, select an unused private state directory outside the upload package. Record project ID and verified project number, identities, region, source/configuration hashes, an unpredictable ownership label, baseline resources, submission limits and cleanup scope. Store the journal as data with atomic writes and private permissions. Hold an exclusive lock across **loading** state and deciding/submitting the next operation. A local file lock does not coordinate multiple deployment hosts.

For resumption, use the original state. For another project or a completed-and-deleted lab, start a new authorised lifecycle with fresh state. An empty/missing journal does not authorise adoption of an existing resource.

## 2. Read-only preflight; bootstrap only when required

These reads deliberately scope the CLI account, project and quota consumer:

```bash
gcloud projects describe "$PROJECT_ID" \
  --project="$PROJECT_ID" --account="$OPERATOR_ACCOUNT" \
  --billing-project="$PROJECT_ID" --format=json --quiet
gcloud services list --enabled \
  --project="$PROJECT_ID" --account="$OPERATOR_ACCOUNT" \
  --billing-project="$PROJECT_ID" --format=json --quiet
gcloud billing projects describe "$PROJECT_ID" \
  --project="$PROJECT_ID" --account="$OPERATOR_ACCOUNT" \
  --billing-project="$PROJECT_ID" --format=json --quiet
```

Validate the returned active project ID and numeric project number; save that number as `PROJECT_NUMBER`. A denied or disabled inspection API means **unknown**, not disabled billing or an empty inventory. Do not activate an API in a different CLI consumer project to make an inspection succeed. Connecting an existing Runtime requires the selected caller's resource/session access; creation additionally requires verified billing, API baseline and deployment permissions. Do not impose deployment IAM administration on a caller that only needs to use an existing service.

CLI credentials, ADC, ADC quota project and deployed workload identity are separate. For the recorded workstation operator-ADC profile, establish the approved ADC email and quota project before mutation. A selected CLI account alone is insufficient. The following optional read-only check refreshes a short-lived token and uses token information without printing token values or response bodies:

```python
import os
import sys
import google.auth
from google.auth.transport.requests import Request
import requests

try:
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(Request())
    response = requests.post(
        "https://oauth2.googleapis.com/tokeninfo",
        data={"access_token": credentials.token}, timeout=20,
    )
    response.raise_for_status()
    email = response.json().get("email")
    if email != os.environ["OPERATOR_ACCOUNT"]:
        raise ValueError("identity mismatch or unavailable")
    if credentials.quota_project_id != os.environ["PROJECT_ID"]:
        raise ValueError("quota mismatch")
except Exception:
    sys.exit("ADC identity/quota unverified; no token or response body logged.")
print("Approved operator ADC identity and quota project verified.")
```

Run it only in a trusted local environment without HTTP debug logging. An unavailable email stops this profile; do not guess it. Inspect an existing `gcloud` impersonation override before comparing CLI and ADC identities. A workload or impersonation design requires its own explicit caller contract. If credential correction is part of the task, the recorded user-ADC setup is `gcloud auth login "$OPERATOR_ACCOUNT"`, `gcloud auth application-default login "$OPERATOR_ACCOUNT"`, then `gcloud auth application-default set-quota-project "$PROJECT_ID"`. These change local credential configuration; they do not grant IAM or prove deployed model access. Prefer short-lived credentials over downloaded service-account keys.

For **default managed Runtime identity** readiness, inspect project IAM:

```bash
gcloud projects get-iam-policy "$PROJECT_ID" \
  --project="$PROJECT_ID" --account="$OPERATOR_ACCOUNT" \
  --billing-project="$PROJECT_ID" --format=json --quiet
```

Match `serviceAccount:service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com` and the unconditional role `roles/aiplatform.reasoningEngineServiceAgent`. Substitute only the verified number. `roles/aiplatform.serviceAgent` is a different role. Google-managed identities live outside the customer's project: `gcloud iam service-accounts describe` there is not the readiness test. The binding establishes configuration, while a real managed model call establishes functional access. For a deliberately selected custom workload identity, inspect that identity's actual permissions instead of forcing this default profile.

If new shared setup is requested, prepare only the missing, approved changes:

| Prerequisite | Recorded procedure and stopping condition |
| --- | --- |
| APIs | The lab permitted missing `aiplatform.googleapis.com`, `cloudresourcemanager.googleapis.com`, `iam.googleapis.com`, `serviceusage.googleapis.com`, plus `cloudbilling.googleapis.com` for inspection. Storage, Logging, Monitoring, Trace and Telemetry were required existing deployment baseline. Derive the target path's requirements; this historical allowance is not permission to activate them. |
| Billing inspection unavailable | An explicitly approved Cloud Billing API activation may precede inspection. Require `billingEnabled: true` before further provisioning; billing-account linking/upgrades require a separate decision. |
| Standard identities missing | Check `gcloud components list --only-local-state --format=json`. If needed, `gcloud components install beta --quiet` is a separate local setup action. The recorded generation command is `gcloud beta services identity create --service=aiplatform.googleapis.com`, with the same explicit project/account/billing-project flags. It may return the Vertex service agent while also generating the Runtime identity. |
| Exact Runtime role missing after generation | Reread IAM, then apply only an approved `gcloud projects add-iam-policy-binding "$PROJECT_ID" --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform-re.iam.gserviceaccount.com" --role=roles/aiplatform.reasoningEngineServiceAgent --condition=None`, adding the same scoped flags. Preserve other bindings. |

Persist baseline and intent before each bootstrap mutation; reread after completion. A ready baseline is a no-op. Unknown acceptance leaves a pending receipt and blocks resubmission; deleting that receipt is not recovery. Shared APIs and standard managed identities/IAM remain after temporary Runtime cleanup. Preflight is complete only when the selected path's required checks pass, with model access/quota still labelled unverified until functional verification.

## 3. Prepare and deploy one owned Runtime

Keep the agent package self-contained, with its actual export, dependencies and required local modules. Inspect the exact staged files and generated configuration. Keep credentials, private state/logs, environments and caches outside the upload; use the installed CLI's exclusion mechanism. Agent-local `.env` and `.agent_engine_config.json` can affect deployment even when excluded from staging, so review both configuration channels explicitly. The recorded bounded path refused both files and supplied an external configuration using an **absolute** path, because ADK changes working directory during packaging.

Example external configuration after replacing the ownership-label value with the journal's generated token:

```json
{
  "min_instances": 0,
  "max_instances": 1,
  "resource_limits": {"cpu": "1", "memory": "2Gi"},
  "labels": {"frontend_lab": "replace-with-recorded-ownership-token"}
}
```

These are the tested limits, not universal capacity advice or a spending cap. Permit only reviewed keys: `env_vars` and `extra_packages` can inject additional configuration or source. If specifying `--temp_folder`, use a fresh owned staging directory; ADK removes existing contents. Inspect `adk deploy agent_engine --help` in the selected environment; `--staging_bucket` is deprecated and unused in this baseline.

**Choose a lifecycle implementation before submission.** The tested bounded design first saved create intent, submitted REST `POST /v1beta1/projects/PROJECT_ID/locations/RUNTIME_REGION/reasoningEngines` to the regional `RUNTIME_REGION-aiplatform.googleapis.com` endpoint with `displayName` and the ownership `labels`, and saved the returned long-running operation name before polling. Authenticate through the verified ADC caller, for example an authorised HTTP session; keep access tokens out of argv and logs. It then verified operation success and the exact resource's ownership before updating that saved resource with ADK. Implement/adapt this journalled operation sequence in the target lifecycle runner; a bare HTTP command without persisted response/recovery handling is insufficient. Bound individual requests, polling and total duration. A response lost before its operation ID is saved leaves unknown acceptance and requires provider reconciliation.

The following is the **update stage only**, after the runner has verified ownership, saved pending-update intent and resolved `RESOURCE_ID`, `DISPLAY_NAME`, `RUNTIME_CONFIG` and `AGENT_FOLDER`. The last two paths must be absolute. Capture stdout/stderr into a fresh private per-attempt log, bound subprocess duration and consume an attempt before starting:

```bash
env -u GOOGLE_API_KEY -u GEMINI_API_KEY -u GOOGLE_GENAI_USE_VERTEXAI -u RESOURCE_ID \
  CLOUDSDK_CORE_ACCOUNT="$OPERATOR_ACCOUNT" \
  CLOUDSDK_CORE_PROJECT="$PROJECT_ID" \
  CLOUDSDK_BILLING_QUOTA_PROJECT="$PROJECT_ID" \
  GOOGLE_CLOUD_PROJECT="$PROJECT_ID" \
  GOOGLE_CLOUD_LOCATION="$MODEL_LOCATION" \
  GOOGLE_GENAI_USE_ENTERPRISE=true \
  AGENT_RUNTIME_LOCATION="$RUNTIME_REGION" \
  adk deploy agent_engine \
    --project="$PROJECT_ID" --region="$RUNTIME_REGION" \
    --display_name="$DISPLAY_NAME" --agent_engine_id="$RESOURCE_ID" \
    --agent_engine_config_file="$RUNTIME_CONFIG" "$AGENT_FOLDER"
```

Shell expansion supplies the verified ID to the explicit flag while `env -u RESOURCE_ID` removes a stale inherited setting from the child. The approved ADC configuration still needs to resolve to the verified caller. Changing shell model settings does not alter agent code that pins another endpoint.

Omitting `--agent_engine_id` takes ADK's native creation path. In 2.8.0, a failed source update can trigger SDK deletion of the just-created resource; account for that conditional cleanup before choosing this alternative. The journalled empty-create/explicit-update design keeps recovery under the lifecycle runner. Neither approach authorises adoption of an unrelated existing ID.

ADK can catch a deployment exception and return exit zero. Require fresh success evidence for the exact saved resource plus provider readback; the recorded CLI marker was `Deployed to Agent Platform: RESOURCE_NAME`. Validate project ID or verified project number, region, resource identity/ownership and `spec.deploymentSpec` limits independently. Persist provider completion separately from configuration validity. Finish with one verified target or an accurately preserved pending/failed state—not an automatic second creation.

## 4. Hand the resource to the gateways and browsers

Record the full returned name as `AGENT_RUNTIME_RESOURCE_NAME`, accepting only the selected project ID or its verified number and Runtime region. Generate settings from that output; keep browser credentials separate. These are the recorded adapter keys; map them to the existing target application's configuration:

```bash
export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"
export GOOGLE_CLOUD_LOCATION="$MODEL_LOCATION"
export GOOGLE_GENAI_USE_ENTERPRISE=true
export AGENT_RUNTIME_LOCATION="$RUNTIME_REGION"
export AGENT_RUNTIME_RESOURCE_NAME="$VERIFIED_RESOURCE_NAME"
```

Load settings through the application's reviewed configuration loader; do not source arbitrary provider output as executable shell. Verify an existing connection with the retained owning `vertexai.Client(project=PROJECT_ID, location=RUNTIME_REGION)` and `client.agent_engines.get(name=VERIFIED_RESOURCE_NAME)` before submitting a model query. Recreate/restart cached SDK connections after changing the target.

| Process | Start and check |
| --- | --- |
| JSON Python gateway | From the application directory and active environment, run `python -m uvicorn "$JSON_GATEWAY_ASGI" --host 127.0.0.1 --port 8000`; resolve the module:app value from the implementation. Retain the existing public JSON route. |
| AG-UI Python gateway | In another active-environment terminal, run `python -m uvicorn "$AGUI_GATEWAY_ASGI" --host 127.0.0.1 --port 8080`. Configure explicit ADK SSE and the translator described in [managed-runtime.md](managed-runtime.md). |
| Vite/React | From its frontend directory, use its existing package manager/lockfile and scripts. Point the API helper at the JSON gateway; allow the exact browser origin in CORS, including the preview origin when testing a built bundle. |
| Next.js/CopilotKit | Configure its server-only backend URL, matching agent identifier and authenticated caller forwarding; use its own locked install/build/start workflow. Restart after changing server configuration. Keep a shared-token teaching BFF bound to loopback; it is not public sign-in. |

Stop an old backend before reusing its port. First test the selected backend directly with a synthetic request; then exercise that same contract through the actual browser. Serving frontends locally is separate from deploying their hosting infrastructure. Both gateways may use the same owned Runtime; retain it until all approved interface tests finish.

## 5. Verify without accidental repeated model work

Record one bounded synthetic smoke's session identity before submission and retain private events incrementally. Verify the actual structured tool result, expected business outcome, final non-thought answer and absence of reported application/tool failure through stream completion. Plausible prose, HTTP 200 or a deployment marker alone is insufficient. Use the installed SDK's supported JSON-lines/SSE parser. Test recall by keeping the session ID across a local gateway restart, without replaying browser history.

Application code without a retry loop may still retry through its SDK transport. The recorded hardened smoke used this aiplatform 1.153.1 client configuration:

```python
import os
import httpx
import vertexai

client = vertexai.Client(
    project=os.environ["PROJECT_ID"],
    location=os.environ["RUNTIME_REGION"],
    http_options={
        "timeout": 120000,
        "retry_options": {"attempts": 1},
        "async_client_args": {"transport": httpx.AsyncHTTPTransport(retries=0)},
    },
)
```

Retain the owner through the async stream and close it using the installed SDK lifecycle; the recorded smoke called `await client.aio.aclose()`. Its optional aiohttp transport had internal disconnect retries, hence the explicit HTTPX selection. This is the smoke's tested configuration, not a claim that every historical gateway had this retry policy. Use actual SDK/HTTP boundary tests to count submissions on 429 and disconnect failures before promising one attempt. Bound session work, lock waiting, query consumption and diagnosis inside the overall deadline. Count failed and uncertain submissions; one application request can produce several model generations. A timeout does not prove remote cancellation.

Complete browser validation with loading/error recovery, tool-card correctness, streaming/final rendering and the intended persistence. Use [validation.md](validation.md) for the selected contract. Report SDK, browser and live-provider evidence separately.

## 6. Recover and clean up the owned target

Use the original private journal and verified caller. Cleanup needs ownership and deletion/inspection access; unrelated deployment prerequisites such as a billing-read failure must not unnecessarily strand a resource. Stop only local processes started by this workflow. Obtain cleanup approval if its exact effects/targets were not already approved.

The recorded deletion contract is REST `DELETE /v1beta1/projects/PROJECT_ID/locations/RUNTIME_REGION/reasoningEngines/RESOURCE_ID?force=true` on the same regional endpoint. Force deletion includes child sessions. Save intent before submission and atomically bind the returned operation name to the exact resource URL **without** `?force=true`. Poll that operation within bounds, require completion without error, then independently GET the exact Runtime and known sessions for confirmed 404. Check the complete paginated inventory for owned survivors; access failures remain unknown.

| Saved observation | Required next action |
| --- | --- |
| Bootstrap ready | Reread and return; submit no setup changes. Preserve shared APIs/managed identities and IAM. |
| Completed deployment, repeat requested | Determine whether the command verifies or updates. The recorded provision repeat updated the same ID and consumed another attempt; it was not a no-op. |
| Create/update pending or acceptance unknown | Poll the saved exact operation, or establish its target from provider evidence. Refuse fresh mutations meanwhile. Labels alone identify candidates, not an accepted operation. |
| Update terminal with error, or completed with invalid limits | Preserve failure and forbid functional success claims. Once operation completion and ownership are established, allow owned cleanup. |
| DELETE intent saved but operation empty, even with resource 404 | Preserve uncertainty and reconcile the accepted operation before declaring lifecycle completion or resubmitting. |
| Regional DELETE operation | `projects/PROJECT_NUMBER/locations/REGION/operations/OPERATION_ID` does not encode a Runtime. Require the original matching operation/resource receipt or authoritative exact-target evidence; a nearby same-region operation is insufficient. |
| Deletion completed but independent inspection failed | Record completion separately; retry the permitted inspection/finalisation without rewriting history as unknown acceptance. |
| Completed cleanup repeated | Use the implementation's documented semantics. Chapter 5's wrapper may DELETE the exact already-absent ID and accept 404; other tooling can use GET-only verification. Never infer authority to delete a replacement resource. |
| Reconciliation finished | Complete local marker/configuration cleanup and preserve the final receipt. Remove generated gateway settings so later starts cannot silently reuse the deleted target. |

Retain unrelated resources, pre-existing grants and shared prerequisites. Inspect applicable source/build artefacts and retention using the exact owned identities; a resource's disappearance is not proof of physical erasure or zero future charges. Report absent, retained, pending and inaccessible separately. Preserve sanitised evidence before removing private working state.

## Evidence boundaries

The September 13 campaign verified two updates of one Runtime, a successful SDK smoke, both **local** browsers, recall after gateway restart, and completed delete/repeat. Standard identity generation and the exact managed role grant were live; API activation was not exercised because the baseline became ready beforehand. Offline tests covered configuration propagation, child-environment isolation, transport retry refusal, state races, partial failures and interrupted/regional-operation recovery. Production identity, distributed deployment coordination, cloud-hosted frontends and live injected recovery remain additional work. September 15 cleanup inventories had retention and visibility limits; they do not justify a zero-cost guarantee.
