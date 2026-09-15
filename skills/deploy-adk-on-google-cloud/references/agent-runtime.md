# Deploy an ADK agent to Agent Runtime

Read this branch when managed query and session APIs fit the application. Apply the safety, compatibility, lifecycle and validation workflow in [SKILL.md](../SKILL.md) first. The commands below illustrate the recorded ADK 2.8.0 contract; execute mutations only against the resolved, authorised plan. This skill does not supply a `deploy.sh` wrapper.

## 1. Resolve the package and identities

Inspect the current application's agent export, dependencies, imports, tool effects and session needs. Select the project, supported runtime region, model endpoint, deploying principal, runtime principal and caller. Verify CLI credentials and ADC separately, including the quota project; they can identify different accounts. Successful login does not establish deployment or inference access.

The recorded baseline used Python 3.11–3.13 guidance and these direct dependencies in the uploaded agent's `requirements.txt`:

```text
google-adk[a2a]==2.8.0
google-cloud-aiplatform[agent_engines]==1.153.1
```

Retain the existing environment and pins; a new isolated baseline may use these declarations. Run `python -m pip check` where applicable. These are dated direct pins, not a transitive lock. The `[a2a]` extra was retained after an older ADK 2.2.0 startup failed importing the optional `a2a` module; that failure is not asserted for 2.8.0. For another version, inspect the installed CLI and packaging path before reusing these commands.

Keep hosting and model inference separate. The recorded example used `AGENT_RUNTIME_LOCATION=us-central1`, `GOOGLE_CLOUD_LOCATION=global`, `GOOGLE_GENAI_USE_ENTERPRISE=True`, and an agent-selected `gemini-3.5-flash` with explicit Gemini `client_kwargs={"location": "global"}`. Confirm model availability and supported locations for the chosen version. A `MODEL_ID` variable only works if application code reads it. Export resolved operator settings deliberately for the deployment process; a configuration file beside the package is not automatically loaded by the command shown below.

Verify the deploying principal's required permissions and the actual runtime identity independently. The recorded deployment used the default Reasoning Engine Service Agent with `roles/aiplatform.reasoningEngineServiceAgent`; the deployer used AI Platform permissions. A dedicated runtime identity and customer login layer were production advice, not implemented features. Prefer platform identity to downloaded service-account keys.

Preflight the project number, billing, quota and enabled APIs. The recorded allowlist was AI Platform, Resource Manager, IAM, Service Usage, Storage, Logging, Monitoring, Trace and Telemetry (`aiplatform`, `cloudresourcemanager`, `iam`, `serviceusage`, `storage`, `logging`, `monitoring`, `cloudtrace`, `telemetry`, each suffixed `.googleapis.com`). Activate only missing services within authorisation, then recheck. Permission or transport errors block the claim of availability. Completion: package, target and each identity's required permissions are accounted for.

## 2. Inspect what will be uploaded

Keep the agent self-contained: its folder contains `agent.py`, `__init__.py`, requirements and every required local module/data file. Exercise local import and package staging with a substituted provider boundary before deployment. Imports that work only because of the developer's checkout are insufficient.

Inspect the exact staged files. Use `.ae_ignore` for local environments, credentials, session databases, state, logs, temporary files and caches, while preserving required application data. Exclusion is not the whole configuration boundary: ADK reads agent-local `.env` and `.agent_engine_config.json` separately; those can inject runtime environment values or additional source folders. Refuse unintended instances and relocate operator configuration outside the upload folder. Inspect both channels deliberately if the application legitimately uses them.

The recorded CLI stages source and a generated Dockerfile directly; this path needed no customer staging bucket or repository-maintained container image. Recheck this for other deployment methods. Completion: a sanitised staging manifest identifies every included file and the configuration ADK consumes outside staging.

If supplying `--temp_folder`, use a fresh owned directory: the installed CLI may remove existing contents. Inspect native failure paths as well as the happy-path command. In ADK 2.8.0, native creation is followed by a source update; if that update raises, the SDK attempts to delete the newly created runtime. Include this conditional deletion in a separately approved failure-cleanup scope before invocation, or implement an explicit SDK workflow that preserves the resource and recovery state for reviewed cleanup. An existing runtime updated through `--agent_engine_id` is excluded from that automatic deletion branch.

## 3. Persist intent, then submit once

Choose a fresh state record for a new deployment. Record ownership, project ID and verified project number, runtime region, source/configuration fingerprint and intended operation. Parse state as data; reject a mismatched target or inherited resource ID. Hold one operation lock across state inspection, submission, polling and state updates. A local `fcntl.flock` needs its descriptor retained by the running child; leave the lock file in place. Multi-host coordination requires a separate design.

Before any submission, persist pending intent and the path for a sanitised deployment log. Inspect existing resources and pending operations first. The version-specific create command is:

```bash
CLOUDSDK_CORE_ACCOUNT="$OPERATOR_ACCOUNT" \
GOOGLE_CLOUD_QUOTA_PROJECT="$GOOGLE_CLOUD_PROJECT" \
adk deploy agent_engine \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="$AGENT_RUNTIME_LOCATION" \
  --display_name="$AGENT_DISPLAY_NAME" \
  "$AGENT_FOLDER"
```

For an authorised update, add `--agent_engine_id="$RESOURCE_ID"` before the folder argument, using the verified saved target. A completed repeat in the recorded lifecycle updates that resource; it does not create a new lab. This is not a production rollout/rollback policy.

Accept an output resource name only if its project equals the intended ID or verified number, its region matches, and an update returns the existing ID. Multiple IDs or an unexpected target require reconciliation. A printed ID before failure is recovery evidence: preserve it and pending intent. If interrupted or uncertain, inspect the log, exact resource and provider operations; when no ID was returned, inspect the project's deployment inventory. Remove pending intent only after a documented, resolved outcome. Completion: one identified resource has confirmed readiness, or pending recovery state accurately preserves uncertainty.

## 4. Verify the managed HTTP contract

Use the caller access token without printing it and JSON serialisation for request bodies. The recorded regional endpoints were:

```text
https://RUNTIME_REGION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/RUNTIME_REGION/reasoningEngines/RESOURCE_ID:query
https://RUNTIME_REGION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/RUNTIME_REGION/reasoningEngines/RESOURCE_ID:streamQuery?alt=sse
```

Send `Content-Type: application/json` and Bearer authorisation. First create a synthetic session through `:query`:

```json
{"class_method":"async_create_session","input":{"user_id":"synthetic-user"}}
```

Save `output.id`, then invoke `:streamQuery` using the same user and returned session:

```json
{"class_method":"async_stream_query","input":{"user_id":"synthetic-user","session_id":"SESSION_ID","message":"SYNTHETIC_TEST_MESSAGE"}}
```

The recorded client used a 15-second connection limit, 60-second session-creation limit and 120-second query limit with HTTP failures propagated and no automatic model retries. Choose explicit bounds for the current run. Client timeout limits waiting; it does not prove remote cancellation or bound model/tool calls. The recorded query supplied no `run_config` or server model-call budget.

Parse the actual transport. The managed endpoint returned NDJSON even with `alt=sse`; accept JSON lines and SSE `data:` payloads, ignoring blank/metadata/comment lines and `[DONE]`. Reject malformed JSON, non-object events, recognised application errors and incomplete required evidence. Keep native response fixtures: wrapping test events into invented SSE concealed the original parser defect.

Define the application's structured success oracle before the call. For the support-triage example it was exactly one successful `route_support_ticket` response, a recognised/expected queue, and nonempty non-thought answer text. That narrow oracle does not correlate call IDs, invocation IDs or final-event ordering. Add those assertions and corresponding real-format tests where the application needs stronger guarantees. Inspect final wording too: a model once claimed ticket logging and future follow-up although the tool only selected a queue. Require claims to match actual tool effects.

For recall, classify a synthetic message with a distinctive marker, then ask what it described and what decision was made using the same session. Require the previous facts and no redundant action. Starting a new session for each smoke invocation cannot establish recall. Inventory sessions created by tests and include their disposition in cleanup.

Treat `user_id` as application data, not proof of end-user identity. The recorded local SDK refused another user's session with HTTP 500; that is neither a clean 403/404 contract nor live customer authorisation proof. Verify the actual caller boundary and, if exposed to end users, authenticated ownership checks. Event streaming also does not imply token streaming: the recorded default buffered model text; explicit streaming and partial/final handling remained an unimplemented extension. Completion: real tool evidence, grounded text and the required session/negative checks pass with observed transport recorded.

## 5. Delete, reconcile and prove absence

Use the authorised exact recorded project, region and ID. Record deletion intent before a DELETE request. The recorded endpoint is `https://RUNTIME_REGION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/RUNTIME_REGION/reasoningEngines/RESOURCE_ID?force=true`; forced deletion includes child resources such as sessions. Save the returned long-running operation name atomically against the unchanged resource URL without `?force=true`.

- With a saved operation name, resume polling its regional `v1beta1` URL; preserve recovery state on timeout or terminal error.
- If the DELETE response was lost before its name was saved, GET the exact resource. A 404 establishes absence. Otherwise reconcile the provider operation before resubmitting; a present resource alone does not authorise another DELETE.
- Use bounded polling and re-evaluate budget before extending it. The recorded implementation allowed 120 polls at five-second intervals with individual HTTP bounds; that is a baseline, not a required production policy.
- Require successful operation completion and a separate resource GET 404. Permission failure, transport failure and other statuses are not absence.
- Write a completed-deletion receipt before removing active state. A repeat uses the receipt for GET-only absence verification. If the resource is present, stop; an old receipt is not authority to delete it. Preserve receipts and use fresh state for another deployment.

Inspect any source-build artefacts and retained resources relevant to cost closure. The example declared no separate customer cluster/database/staging bucket, left shared APIs and Google-managed identities intact, and did not prove physical erasure of logs/backups. Completion: owned runtime and children have the verified disposition required by the plan, independent inventory covers available visibility, and retained/unknown items are explicitly reported.

## Evidence limits

The September 2026 baseline had offline lifecycle/locking/packaging tests with provider doubles, real installed HTTP handlers and routing tool with a scripted model, and real loopback transport. Live checks separately covered original create/repeat, replacement all-queue routing and explicit recall after prompt repair, and both runtimes' cleanup/repeat/independent absence. Fresh-project API activation, manual interrupted-deploy recovery and the replacement's repeat were not live verified. Production multi-user authorisation, strict stream correlation, model/tool budgets, transitive locks and rollout controls remain work to implement and validate for the target application.
