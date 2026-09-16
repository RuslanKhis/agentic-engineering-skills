# Local ADK integration operations

Use this workflow when a safe-tool task also needs Gemini configuration
diagnosis, Vertex API prerequisites, interrupted activation recovery or a local
ADK Web exercise. Skip unrelated branches. This is local integration guidance;
it supplies no application deployment or cloud teardown procedure. Use the
target's existing tools and preserve its dependency pins.

The observations below come from local **ADK 2.8.0**,
**google-genai 2.23.0** and Python 3.11 on macOS. Inspect installed behaviour
before adapting commands. Read [compatibility](compatibility.md)
for evidence boundaries and [validation](validation.md) for live
test authorisation and reporting.

## 1. Resolve the effective runtime configuration

Record the selected interpreter, application directory, ADK executable, model,
backend, location and credential mode. Use the interpreter that will launch the
application. These local checks reveal version and architecture problems without
loading application code or credentials:

```bash
"$PYTHON" -c 'import platform, sys; print(sys.version); print(platform.machine())'
"$PYTHON" -m pip check
"$ADK" web --help
```

Select executable paths from the target's environment. An Apple
Silicon install failed with an Intel interpreter under Rosetta and succeeded
with an already installed native interpreter. Diagnose architecture and wheel
availability before changing pins or installing a global compiler toolchain.
Recreate only an owned disposable environment when necessary.

Trace configuration precedence through the actual launch command and installed
loader. Report variable presence and non-secret settings; keep secret
values, tokens and credential-file contents out of output. Choose one backend:

| Symptom or decision | Check and next action |
| --- | --- |
| “No API key was provided” | Verify which application directory and dotenv file the loader selects, the intended authentication mode, and whether the server restarted after configuration changed. Keep credentials out of browser chat. |
| Root configuration changed but behaviour did not | In the observed ADK path, chapter-local `.env` shadowed root configuration. Trace local files and inherited environment rather than assuming a root edit took effect. Preserve unrelated settings. |
| Controlled Vertex test | Use existing ADC with explicit project/location. Exclude API-key inheritance and unwanted backend overrides in the child process. The historical run used `PYTHON_DOTENV_DISABLED=1`; verify support before relying on it. |
| API-key metadata request succeeds | Record only the operation tested. Model metadata access establishes neither key ownership nor successful generation; ADC checks do not validate API-key ownership. |

The historical Vertex selector was `GOOGLE_GENAI_USE_ENTERPRISE=true`, with
`GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`. Inspect the pinned SDK's
selector before reuse. Model location identifies the model endpoint; it does
not establish an application hosting region. Complete this step with one
unambiguous runtime configuration, or a specific missing prerequisite.

## 2. Inspect prerequisites through the runtime identity

Use a read-only preflight with the **same credential source** the application
will use. A successful CLI project lookup or selected `gcloud` account does not
establish application access. For the historical local user-ADC path, the checks
were actual access-token identity, exact quota project, runtime permissions and
the exact `aiplatform.googleapis.com` service. Other credential types need their
own supported identity checks; this does not validate deployed workload identity.
Google documents [CLI authentication separately from application credentials](https://docs.cloud.google.com/sdk/docs/authenticate).

| Check | Required interpretation |
| --- | --- |
| Principal | Compare the token's verified identity with the expected account. An email alias or CLI login is insufficient. |
| Quota project | Compare the actual ADC quota project with the explicitly intended quota project. It may differ from the resource project; verify both rather than silently rewriting shared ADC settings. |
| Runtime permissions | Inspect `aiplatform.endpoints.predict` and `serviceusage.services.use` for this historical Vertex path. Use equivalent least-privilege checks appropriate to the selected API. |
| Exact API state | Distinguish `ENABLED`, `DISABLED` and unavailable inspection. Avoid requiring broad project/service listing access when an exact-service check suffices. |
| Billing | Explicit `billingEnabled=false` is a failed prerequisite. Permission denial or an unavailable billing metadata API means unknown billing state, not disabled billing. |

Separate **PASS**, demonstrated **FAIL**, and **BLOCKED** inspection in the
report. In the chapter helper, exit `0` could coexist with blocked billing
metadata, `1` meant a demonstrated failure and `2` a blocked required check.
Read every section; preserve the target helper's own documented exit semantics.
Model access and available quota still require an authorised model request.

If implementing the equivalent user-ADC identity inspection, the historical
helper isolated its identity lookup from quota headers using a credential clone.
It retained the original quota-bearing credentials for project requests. This
avoided mistaking an identity-endpoint quota rejection for failed model access.
Complete preflight with sanitised evidence of each check; continue offline work
while login, billing or permission prerequisites remain unresolved.

## 3. Activate only the selected API, then reconcile

Enter this branch when activation is in scope. Inspect the target's
existing setup command and prepare its exact project, API allowlist, expected
principal/quota project, recovery-state path, timeout and retained effects.
Apply the skill's consequential-operation authorisation rule before mutation;
retain approval already granted for that exact scope. The skill ships no
activation helper and requires no dependency on the chapter repository.

A suitable helper provides a read-only plan, verifies enable permission, saves
intent before submission and persists an accepted operation ID before polling.
It serialises updates, writes recovery state atomically with restricted access,
and binds that state to project, principal, quota project and API. Its total
budget covers requests, polling and readiness. The chapter used three minutes;
choose the target's documented bound.

| Observed state | Permitted next action |
| --- | --- |
| No saved submission; API disabled | After approval and prerequisite checks, submit the allowlisted activation once and save its operation ID. |
| API already enabled; no unresolved submission | Record a no-op. This verifies the baseline, not API activation. |
| Saved accepted operation pending | Poll that operation under the remaining budget. After interruption, resume from the same state. |
| Operation reports success | Independently check the exact service reaches `ENABLED` before recording readiness. |
| Submission unknown without an operation ID | Preserve state and obtain operator reconciliation. Removing state or creating a fresh path to force another submission loses the uncertainty record. |
| Operation failed, saved ownership differs, or previously ready API is now disabled | Stop automatic submission and report the reconciliation need. Refuse mismatched ownership before provider calls. |

Repeat completed setup against the same state and inspect provider state
and submission count. Actual activation requires a successful terminal operation,
verified readiness and a repeat with no extra mutation. Report no-ops separately.
Retain recovery metadata and report unresolved operations. Keep shared API
enablement intact during cleanup; disabling it is not application teardown.

Historically, one real disabled-to-enabled transition and completed repeat passed.
Injected live partial-failure recovery was not run; refusal/recovery branches
were tested offline. The model/UI campaign used a different, already configured
project. These separate passes do not establish complete fresh-project onboarding.

## 4. Exercise and clean up the owned local runtime

After offline checks and required live-test approval, inspect the selected
port and record process ownership. An occupied port means select another unused
port; preserve the existing process. With ADK 2.8.0, a disposable launch shape is:

```bash
"$ADK" web "$APPS_DIR" --host 127.0.0.1 --port "$PORT" --no_use_local_storage
```

Set `APPS_DIR` to the app parent directory and `PORT` to the selected port.
Confirm flags using installed help. Keep the unauthenticated development UI on
loopback. Use synthetic payloads and the actual tool/session/confirmation path.
Enable the browser's Streaming option when measuring streamed answers, and
verify streaming at the model boundary. Loading and thinking indicators do not
count as answer text. Preserve the approved request allowance across restarts
or application reloads; turns may require multiple model calls. Request/token/time
bounds constrain exposure but do not constitute a hard spending cap.

Separate the tool's in-memory mock state from persistent ADK chat state. The
observed default command wrote `<agent>/.adk/session.db` and local artifacts
that survived restart; the disposable flag avoids that default local storage.
Inspect the actual session backend rather than assuming every ADK client uses
this path.

| Owned item | Cleanup and verification |
| --- | --- |
| Server | Stop the recorded process with `Ctrl-C` or its verified PID. Inspect the listener and confirm loopback connection refusal; a timeout or HTTP error is not proof of shutdown. |
| Sessions/artifacts | Delete selected disposable sessions through ADK, or remove the exact owned `.adk` directory after shutdown. Verify absence and that repeating cleanup succeeds. |
| Temporary lab files | Remove only inventoried owned source copies, environments, caches and database backups. Include review copies in the inventory. |
| Activation state/API | Retain the agreed recovery metadata and enabled API; report any pending operation. |
| Existing credentials/provider data | Preserve credentials and shared configuration. Local deletion does not revoke access, erase provider logs or undo model charges. |

For an approved directory removal, refuse symlink targets, validate ownership
before recursive deletion, surface filesystem errors and check absence. Verify
shutdown independently of the server's own success message. Report inaccessible
or API-disabled inventories as blocked, never empty, and scope absence claims
to what was actually inspected. Complete with owned-runtime absence, retained
state and remaining inspection limits explicitly recorded.

If the task also created object storage, an empty live-object list does not
establish zero retained data or zero future cost. Check relevant versions,
soft-deleted records and retention metadata. Cloud Storage can continue charging
for soft-deleted objects until retention ends; those objects cannot be purged
early, and changing a policy does not shorten their existing retention. Report
the remaining scope and expiry instead of restoring data or changing shared
policies to make cleanup look complete. This was a wider account-check lesson,
not a cloud resource created by the Chapter 1 application. See [Cloud Storage
soft delete](https://docs.cloud.google.com/storage/docs/soft-delete).
