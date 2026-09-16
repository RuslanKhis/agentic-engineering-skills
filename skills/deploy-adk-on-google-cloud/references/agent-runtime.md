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

In an offline staging test, capture both the generated Dockerfile and the SDK update configuration. Assert the hosting region, required non-secret runtime settings, intended model constructor arguments and absence of forbidden configuration keys. Checking the developer's environment alone misses this boundary. The inspected generator's defaults and the chapter's model helper explain the configuration pattern; the dated live campaign separately demonstrated regional hosting with global inference and workload identity.

Verify the deploying principal's required permissions and the actual runtime identity independently. The recorded deployment used the default Reasoning Engine Service Agent with `roles/aiplatform.reasoningEngineServiceAgent`; the deployer used AI Platform permissions. A dedicated runtime identity and customer login layer were production advice, not implemented features. Prefer platform identity to downloaded service-account keys.

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

Use the authorised exact recorded project, region and ID. Record deletion intent before a DELETE request. The recorded endpoint is `https://RUNTIME_REGION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/RUNTIME_REGION/reasoningEngines/RESOURCE_ID?force=true`; forced deletion includes child resources such as sessions. Save the returned long-running operation name atomically against the unchanged resource URL without `?force=true`.

- With a saved operation name, resume polling its regional `v1beta1` URL; preserve recovery state on timeout or terminal error.
- If the DELETE response was lost before its name was saved, GET the exact resource. A 404 establishes absence. Otherwise reconcile the provider operation before resubmitting; a present resource alone does not authorise another DELETE.
- Use bounded polling and re-evaluate budget before extending it. The recorded implementation allowed 120 polls at five-second intervals with individual HTTP bounds; that is a baseline, not a required production policy.
- Require successful operation completion and a separate resource GET 404. Permission failure, transport failure and other statuses are not absence.
- Write a completed-deletion receipt before removing active state. A repeat uses the receipt for GET-only absence verification. If the resource is present, stop; an old receipt is not authority to delete it. Preserve receipts and use fresh state for another deployment.

Inspect any source-build artefacts and retained resources relevant to cost closure. The example declared no separate customer cluster/database/staging bucket, left shared APIs and Google-managed identities intact, and did not prove physical erasure of logs/backups. Completion: owned runtime and children have the verified disposition required by the plan, independent inventory covers available visibility, and retained/unknown items are explicitly reported.

## Evidence limits

The September 2026 baseline had offline lifecycle/locking/packaging tests with provider doubles, real installed HTTP handlers and routing tool with a scripted model, and real loopback transport. Live checks separately covered original create/repeat, replacement all-queue routing and explicit recall after prompt repair, and both runtimes' cleanup/repeat/independent absence. Fresh-project API activation, manual interrupted-deploy recovery and the replacement's repeat were not live verified. Production multi-user authorisation, strict stream correlation, model/tool budgets, transitive locks and rollout controls remain work to implement and validate for the target application.
