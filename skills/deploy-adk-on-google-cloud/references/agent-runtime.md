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

Keep hosting and model inference separate. The recorded example used `AGENT_RUNTIME_LOCATION=us-central1`, `GOOGLE_CLOUD_LOCATION=global`, `GOOGLE_GENAI_USE_ENTERPRISE=True`, and an agent-selected `gemini-3.5-flash` with explicit Gemini `client_kwargs={"location": "global"}`. Confirm model availability and supported locations for the chosen version. A `MODEL_ID` variable only works if application code reads it.

### Trace configuration through the generated container

Resolve the following channels separately before translating a local agent into a deployment. These are inspected ADK 2.8.0 implementation details; recheck the installed generator for another version.

| Channel | Effective behaviour and implementation decision |
| --- | --- |
| Operator process environment | The chapter wrapper explicitly loads its outer `.env`. The native CLI command below does not load that file automatically or upload every exported variable. Use scoped process configuration for operator credentials and SDK calls; separately declare values the workload needs. |
| `--project` and `--region` | Select the managed resource and generated container defaults. The generated Dockerfile sets `GOOGLE_GENAI_USE_ENTERPRISE=1`, the selected project, and `GOOGLE_CLOUD_LOCATION` to the hosting region. A successful regional deployment does not establish the intended inference location. |
| Agent `.env` / explicit `--env_file` | ADK reads this file separately from source staging. Explicit project/region flags win for the deployment target; other file values can enter workload `env_vars`. Inspect that payload without disclosing values. The chapter rejects agent-local `.env` and does not use this channel. |
| `.agent_engine_config.json` / explicit platform configuration | Can supply runtime configuration and extra source packages. A nonempty environment-file mapping replaces the configuration's `env_vars` mapping in this baseline; do not assume the mappings are merged key by key. |
| Model constructor | The chapter's enterprise branch uses `Gemini(model=..., client_kwargs={"location": "global"})`; its local API-key branch returns the model name. That explicit client location keeps inference global even when the generated image's location is regional. Preserve the application's backend choice and prove its actual client receives the intended location. |
| `agents-cli deploy` (Agents CLI project) | A container build from the project `Dockerfile`, not this generator. Runtime variables come from the project `.env` plus `--env-vars`, with defaults added only when absent: `GOOGLE_GENAI_USE_ENTERPRISE=true`, `GOOGLE_CLOUD_LOCATION=global`, `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true`, `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`, `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`, `AGENT_VERSION` and, once the engine exists, `APP_URL` pointing at the `/api` passthrough. `GOOGLE_CLOUD_PROJECT` is reserved by the platform and rejected in `deployment_spec.env`; an update replaces the whole `env` block, so the CLI re-sends the live variables it did not set (Agents CLI 1.11.0, `src/google/agents/cli/deploy/agent_runtime.py`, read 22 October 2026). Verify the deployed `deployment_spec.env` keys, not the shell. |

In an offline staging test, capture both the generated Dockerfile and the SDK update configuration. Assert the hosting region, required non-secret runtime settings, intended model constructor arguments and absence of forbidden configuration keys. Checking the developer's environment alone misses this boundary. The inspected generator's defaults and the chapter's model helper explain the configuration pattern; the dated live campaign separately demonstrated regional hosting with global inference and workload identity.

Verify the deploying principal's required permissions and the actual runtime identity independently. The recorded deployment used the default Reasoning Engine Service Agent with `roles/aiplatform.reasoningEngineServiceAgent`; the deployer used AI Platform permissions. Prefer platform identity to downloaded service-account keys.

The platform offers a per-agent identity instead of that shared service agent ([Agent Identity](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-identity), read 21 October 2026; not exercised by the recorded campaign):

- Enable it with `.agent_engine_config.json` containing `{"identity_type": "AGENT_IDENTITY"}` beside the agent (the same configuration channel inspected above), `identity_type` in the SDK create config, or `agents-cli deploy --agent-identity`. Leave `identity_type` unset and the runtime keeps service-account behaviour.
- In an Agents CLI project the flag has three states: `--agent-identity`, `--no-agent-identity`, or neither, which keeps an existing agent's identity type and, for a new agent, reads the identity default from `agents-cli-manifest.yaml` (the setting the release notes call `agent_runtime_identity_default`, stored by 1.11.0 as `create_params.agent_runtime.identity_default`; absent means `service_account`) in `agents-cli-manifest.yaml` (projects created since 1.10.0 record `agent_identity`; older projects read as `service_account`). With Agent Identity the CLI first creates a bare engine (`client.runtimes.create` with `identity_type=AGENT_IDENTITY` and the display name), appends its baseline role bindings to the project IAM policy for `principal://<spec.effective_identity>`, then submits the source as an update; `--service-account` is ignored and cleared because the API rejects both, and `--dry-run` therefore needs `resourcemanager.projects.getIamPolicy` and `setIamPolicy`. Moving an existing service-account agent to Agent Identity grants the same roles after the update completes (Agents CLI 1.11.0, `src/google/agents/cli/deploy/agent_runtime.py` and `_cloud_validation.py`, read 22 October 2026). Record that policy edit in the ownership journal; it is a project-level mutation the deploy command performs on your behalf.
- Read the result from `spec.effectiveIdentity`, for example `gcloud ai reasoning-engines describe RESOURCE_ID --region=… --format="value(spec.effectiveIdentity)"`; `gcloud ai reasoning-engines list --region=…` is the matching read-only inventory (confirm the installed CLI with `gcloud help ai reasoning-engines`).
- The identity is a principal, `principal://agents.global.org-ORG_ID.system.id.goog/resources/aiplatform/projects/PROJECT_NUMBER/locations/LOCATION/reasoningEngines/ID`; all agents in a project are `principalSet://…/attribute.platformContainer/aiplatform/projects/PROJECT_NUMBER`. Creation grants only `roles/aiplatform.agentContextEditor` and `roles/aiplatform.agentDefaultAccess`; the documented baseline to add is `roles/aiplatform.expressUser` (inference, sessions and memory), `roles/serviceusage.serviceUsageConsumer`, `roles/browser`, `roles/logging.logWriter`, `roles/monitoring.metricWriter` and `roles/cloudapiregistry.viewer` (same page, re-read 22 October 2026). Agents CLI 1.11.0 grants a different first role: its `AGENT_IDENTITY_ROLES` are `roles/aiplatform.user`, `roles/serviceusage.serviceUsageConsumer`, `roles/browser`, `roles/cloudapiregistry.viewer`, `roles/logging.logWriter` and `roles/monitoring.metricWriter`, and its generated Terraform adds `roles/cloudtrace.agent`, with `--bq-analytics` `roles/bigquery.dataOwner` and `roles/bigquery.jobUser`, and `roles/storage.objectAdmin` on the logs bucket (`src/google/agents/cli/deploy/agent_runtime.py`, scaffold `single-project/variables.tf` and `iam.tf`, read 22 October 2026). State which set the target holds; `aiplatform.user` is broader than `expressUser`, so a hand-built deployment should start from the documented set and add only what a tool needs. The shared service agent's project grants do not transfer, so plan tool and session permissions per agent before switching.
- Its access tokens are bound to the runtime: using one elsewhere returns 401 `Context-Aware Access requirements are not met`. The documented opt-out, `GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES: False` in `env_vars`, is marked not recommended; treat it as a diagnosis aid, not a fix.

An Agent Gateway binding is not fixed at creation: the routing page shows `PATCH` on an existing agent with `updateMask=spec.deploymentSpec.agentGatewayConfig`, warns that patching does not change `identity_type` (an agent created without `AGENT_IDENTITY` must be recreated with both set), and states that changing the binding archives every pre-existing revision, irreversibly, and is only permitted while all traffic is on the latest revision ([route Agent Runtime traffic through Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-gateway-runtime-deploy), read 22 October 2026). Agents CLI exposes the same update as `agents-cli deploy --agent-gateway-egress` and `--agent-gateway-ingress`, each taking `projects/P/locations/R/agentGateways/G`, an empty value to unbind, omitted to leave unchanged; `agents-cli create --agent-gateway` or `scaffold enhance . --agent-gateway` rewrites the Dockerfile to consume the `AGENT_GATEWAY_ROOT_CERTIFICATES` build argument the platform injects and to set `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE` and `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH`, and a deploy with the egress flag against a Dockerfile without that argument fails (Agents CLI 1.11.0, `google-agents-cli-deploy` skill, read 22 October 2026). Treat a binding change as a release with no rollback target and present it as its own approval.

When the runtime is bound to an Agent Gateway and a call fails with 403 `Egress request is not authorized`, an unregistered hostname, `roles/iap.egressor`, or a startup crash reaching `telemetry.mtls.googleapis.com`, consult the installed Google skill `agent-platform-troubleshooting` (from google/skills); if it is not installed, adk-engineer explains how to get it.

Preflight the project number, billing, quota and enabled APIs. The recorded allowlist was AI Platform, Resource Manager, IAM, Service Usage, Storage, Logging, Monitoring, Trace and Telemetry (`aiplatform`, `cloudresourcemanager`, `iam`, `serviceusage`, `storage`, `logging`, `monitoring`, `cloudtrace`, `telemetry`, each suffixed `.googleapis.com`). Activate only missing services within authorisation, then recheck. Permission or transport errors block the claim of availability. Completion: package, target and each identity's required permissions are accounted for.

## 2. Inspect what will be uploaded

Keep the agent self-contained: its folder contains `agent.py`, `__init__.py`, requirements and every required local module/data file. Exercise local import and package staging with a substituted provider boundary before deployment. Imports that work only because of the developer's checkout are insufficient.

Inspect the exact staged files. Use `.ae_ignore` for local environments, credentials, session databases, state, logs, temporary files and caches, while preserving required application data. Exclusion is not the whole configuration boundary: ADK reads agent-local `.env` and `.agent_engine_config.json` separately; those can inject runtime environment values or additional source folders. Refuse unintended instances and relocate operator configuration outside the upload folder. Inspect both channels deliberately if the application legitimately uses them.

The recorded CLI stages source and a generated Dockerfile directly; this path needed no customer staging bucket or repository-maintained container image. Recheck this for other deployment methods. Completion: a sanitised staging manifest identifies every included file and the configuration ADK consumes outside staging.

### Verify the packager, not only the ignore file

The inspected 2.8.0 packager combines agent-folder `.gitignore`, `.gcloudignore` and `.ae_ignore` entries through `shutil.ignore_patterns`, which matches basenames. It is not a full Git-ignore parser: a nested path pattern or `!` re-inclusion should not be assumed to behave as it does in Git. Use patterns that the actual packager understands and inspect the resulting tree. The chapter excludes all `*.json` because its agent needs no JSON data; retain required JSON fixtures/configuration in an application that does use them and exclude credentials specifically.

Treat `extra_packages` as a separate upload boundary. In the inspected CLI, command-line paths resolve against the invocation directory; configuration-file paths resolve against the agent folder. Their files are copied separately from the agent's ignore-filtered tree. Review each resolved source root and packaged file. Default recursive copying can follow symlinks: inspect resolved destinations before copying, or build an explicit staging tree that rejects paths outside authorised roots. This is an implementation safeguard from local code inspection, not a claim that the historical live campaign exercised symlink attacks.

The recorded packaging regression inserted synthetic credentials, session databases and state files, then ran the installed staging code with only the Vertex client replaced. It initially exposed 27 private files in the package. The repaired test requires their absence **and** the presence of required source, dependencies and a nested helper. Reuse that two-sided test pattern: excluding everything is not a successful package. Capture `source_packages`, staged requirements, generated Dockerfile and runtime-configuration keys before the substitute SDK update returns; temporary staging is removed afterward.

Inspect the generated dependency installation as well as local `pip check`. This generator starts from `python:3.11-slim`, installs its selected `google-adk[a2a]` version, then installs the staged agent requirements. It can generate or augment requirements when the Agent Platform dependency is absent. A later requirement can change the earlier ADK installation, and a successful local Python 3.12 import cannot prove remote Python 3.11 compatibility. Keep the CLI's selected ADK version and uploaded requirements consistent, check staged includes/local paths resolve inside the package, and validate the resulting dependency environment before a paid build. These generator details were inspected locally; different methods may use a different base or resolver.

If supplying `--temp_folder`, use a fresh owned directory: the installed CLI may remove existing contents. Inspect native failure paths as well as the happy-path command. In ADK 2.8.0, native creation is followed by a source update; if that update raises, the SDK attempts to delete the newly created runtime. Include this conditional deletion in a separately approved failure-cleanup scope before invocation, or implement an explicit SDK workflow that preserves the resource and recovery state for reviewed cleanup. An existing runtime updated through `--agent_engine_id` is excluded from that automatic deletion branch.

## 3. Persist intent, then submit once

Choose a fresh state record for a new deployment. Record ownership, project ID and verified project number, runtime region, source/configuration fingerprint and intended operation. Parse state as data; reject a mismatched target or inherited resource ID. Hold one operation lock across state inspection, submission, polling and state updates. A local `fcntl.flock` needs its descriptor retained by the running child; leave the lock file in place. Multi-host coordination requires a separate design.

When implementing that guard, canonicalise the state path before deriving its lock, use a nonblocking exclusive lock and fail before provider reads if it is busy. The recorded implementation opens the lock with `O_NOFOLLOW`, passes its descriptor to the child and covers deploy, test and delete with the same guard. Its offline regressions prove that two concurrent creates submit once and that killing the wrapper parent does not unlock a still-running child. Test those lifecycle properties rather than only checking that a `.lock` file exists. The lock coordinates one state path; independent files or hosts targeting the same runtime require shared resource-level coordination.

An unlocked process and a resolved provider operation are different facts. After the last process holding the descriptor exits, the OS releases its lock while `.pending` must still preserve uncertain submission. Keep the pending marker until provider state is reconciled, including when the SDK may have attempted its own conditional deletion. Acquire the guard before reading any state that can select a target. In the recorded scripts, an inherited `RESOURCE_ID` without matching saved project/region state is refused before obtaining a token.

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

In an Agents CLI project the target is selected differently: `agents-cli deploy` updates the engine whose resource id is recorded in `deployment_metadata.json` and scans display names only when no id is recorded, stopping on a deleted engine or duplicate names; `--update-only` refuses to create; `--no-wait` returns the operation and `--status` polls it; `--dry-run` on Agent Runtime makes read-only network calls (enabled APIs, the target engine, IAM permissions, `actAs` on the service account, secrets) and exits 1 on a definite problem. When Terraform created the engine (`infra single-project --apply` or `infra cicd`), its `google_vertex_ai_reasoning_engine` carries `lifecycle.ignore_changes` on the container, source and deployment specs so the deploy command owns those fields and Terraform owns identity, service account and the rest; the Google skill says not to apply Terraform after an imperative deploy because the engine cannot be reconciled without taking it over (Agents CLI 1.11.0, `google-agents-cli-deploy` skill, read 22 October 2026). Record which tool owns which field in the ownership journal before the first mutation.

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

The recorded verifier accepts `function_response` and `functionResponse`, rejects top-level `error`, `error_code` or `errorCode`, and excludes parts marked `thought` from answer text. Preserve these field variations when using the same contract. Its SSE support covers one JSON event per `data:` line; full multiline SSE framing and incremental partial-event assembly need their own parser and fixtures if the target emits them. Do not promote the narrow verifier into a generic streaming library by changing only its label.

Keep a bounded, protected copy of a failed test's response and session identifier long enough to distinguish transport failure, parsing failure and application failure. If the verifier rejects an HTTP 200 after tool execution, inspect that exact session/history before submitting another model turn. The first live framing failure was recovered through a read of its existing session after the temporary stream had been lost; re-invocation would have added cost and potentially repeated actions. Use synthetic fixtures for regression tests and redact sensitive fields before retaining evidence.

Define the application's structured success oracle before the call. For the support-triage example it was exactly one successful `route_support_ticket` response, a recognised/expected queue, and nonempty non-thought answer text. That narrow oracle does not correlate call IDs, invocation IDs or final-event ordering. Add those assertions and corresponding real-format tests where the application needs stronger guarantees. Inspect final wording too: a model once claimed ticket logging and future follow-up although the tool only selected a queue. Require claims to match actual tool effects.

For recall, classify a synthetic message with a distinctive marker, then ask what it described and what decision was made using the same session. Require the previous facts and no redundant action. Starting a new session for each smoke invocation cannot establish recall. Inventory sessions created by tests and include their disposition in cleanup.

Use a different success oracle for a recall-only turn: required prior facts, grounded answer and no new action when the task asks only about history. A live audit helper incorrectly required another routing result for such a follow-up; the existing response was valid and was assessed without a blind retry. A single “every successful response must call a tool” rule would both reject correct recall and reward duplicate side effects. Record which assertion applies before each test message.

Treat `user_id` as application data, not proof of end-user identity. The recorded local SDK refused another user's session with HTTP 500; that is neither a clean 403/404 contract nor live customer authorisation proof. Verify the actual caller boundary and, if exposed to end users, authenticated ownership checks. Event streaming also does not imply token streaming: the recorded default buffered model text; explicit streaming and partial/final handling remained an unimplemented extension. Completion: real tool evidence, grounded text and the required session/negative checks pass with observed transport recorded.

## 5. Delete, reconcile and prove absence

Use the authorised exact recorded project, region and ID. Record deletion intent before a DELETE request. The recorded endpoint is `https://RUNTIME_REGION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/RUNTIME_REGION/reasoningEngines/RESOURCE_ID?force=true`; forced deletion includes child resources such as sessions, and without `force` a runtime with undeleted children fails with `FAILED_PRECONDITION` ([reasoningEngines.delete](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1/projects.locations.reasoningEngines/delete)). Save the returned long-running operation name atomically against the unchanged resource URL without `?force=true`.

- With a saved operation name, resume polling its regional `v1beta1` URL; preserve recovery state on timeout or terminal error.
- If the DELETE response was lost before its name was saved, GET the exact resource. A 404 establishes absence. Otherwise reconcile the provider operation before resubmitting; a present resource alone does not authorise another DELETE.
- Use bounded polling and re-evaluate budget before extending it. The recorded implementation allowed 120 polls at five-second intervals with individual HTTP bounds; that is a baseline, not a required production policy.
- Require successful operation completion and a separate resource GET 404. Permission failure, transport failure and other statuses are not absence.
- Write a completed-deletion receipt before removing active state. A repeat uses the receipt for GET-only absence verification. If the resource is present, stop; an old receipt is not authority to delete it. Preserve receipts and use fresh state for another deployment.

Inspect any source-build artefacts and retained resources relevant to cost closure. The example declared no separate customer cluster/database/staging bucket, left shared APIs and Google-managed identities intact, and did not prove physical erasure of logs/backups. Completion: owned runtime and children have the verified disposition required by the plan, independent inventory covers available visibility, and retained/unknown items are explicitly reported.

## Evidence limits

The September 2026 baseline had offline lifecycle/locking/packaging tests with provider doubles, real installed HTTP handlers and routing tool with a scripted model, and real loopback transport. Live checks separately covered original create/repeat, replacement all-queue routing and explicit recall after prompt repair, and both runtimes' cleanup/repeat/independent absence. Fresh-project API activation, manual interrupted-deploy recovery and the replacement's repeat were not live verified. Production multi-user authorisation, strict stream correlation, model/tool budgets, transitive locks and rollout controls remain work to implement and validate for the target application.
