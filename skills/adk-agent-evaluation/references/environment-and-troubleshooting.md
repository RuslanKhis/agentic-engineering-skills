# Evaluation environment and troubleshooting

Read this when preparing live evaluation, switching projects/providers, diagnosing access failures, or checking setup and cleanup. These procedures generalise the companion's live preflight and offline setup regressions. Fresh API activation, deployment and least-privilege production IAM were not verified by that campaign. Read-only preparation can proceed independently of paid-execution approval.

## Resolve the effective configuration

1. Identify the interpreter, working directory and exact entrypoint for each stage: CLI, pytest, browser server, evaluator worker and scorer. Read where each loads dotenv and whether existing environment variables win. Locate when the agent/provider client is constructed; changing settings after import may be too late.
2. Record a configuration map containing **sources and presence**, not secret values: process overrides, selected dotenv file, provider selector, project/location, requested model and credential route. A root dotenv edit does not update a chapter-local file. Two terminals and a running server can retain different effective settings.
3. Keep CLI identity, Python ADC identity, ADC quota project, API-key-associated project and resource project distinct. A UI project selector or successful CLI login does not prove Python uses that identity/project. Where identity cannot be resolved safely, report it as unknown rather than decoding or printing tokens.
4. For an approved project switch, use a fresh run directory and new resource/state identifiers for that target. Preserve old state as historical evidence; do not feed old deployment IDs to a new project's setup. Inspect the target's existing setup script before invoking it. Updating credentials alone neither migrates resources nor proves access.
5. Prefer an explicit child-process environment for an experiment. In the verified ADK 2.8.0 Vertex path, an empty `GOOGLE_API_KEY` plus `GOOGLE_GENAI_USE_ENTERPRISE=true` selected ADC while preserving the stored key. This depends on client routing and dotenv precedence; confirm both in the installed version. Set the selected project/location and model before client construction. Remove only task-scoped overrides when returning to another route.
6. Restart an owned long-lived server when its import-time configuration changes; record the new process identity and effective non-secret settings. Do not restart another user's service. ADC login/quota-project changes persist beyond a subprocess overlay: propose their exact scope when needed instead of treating them as temporary variables.

Completion: every intended stage has a resolved configuration source, selected target and credential route, or a specific blocker. No secret replacement is implied by this inspection.

## Read project/API state before proposing changes

The following read-only commands use `EVAL_PROJECT` and `EVAL_ACCOUNT`, already set to the reviewed target and CLI identity. They are adaptation examples, not a requirement to install gcloud or use user credentials in CI.

```bash
gcloud auth list --filter=status:ACTIVE --format='value(account)'
gcloud projects describe "$EVAL_PROJECT" \
  --project="$EVAL_PROJECT" --account="$EVAL_ACCOUNT" \
  --billing-project="$EVAL_PROJECT" --format='value(projectId)'
gcloud services list --enabled \
  --project="$EVAL_PROJECT" --account="$EVAL_ACCOUNT" \
  --billing-project="$EVAL_PROJECT" \
  --filter='config.name=aiplatform.googleapis.com' --format='value(config.name)'
```

Check each exit status and validate the returned project/service names. Bound read attempts and command duration. Interpret results as three states:

| State | Evidence | Next action |
| --- | --- | --- |
| Enabled | Successful authoritative list returns exactly the required API | Reuse existing state; proceed to independent authentication/access checks. |
| Confirmed missing | Successful, correctly scoped authoritative query returns no matching enabled API | Prepare an exact activation proposal if that service is actually needed. |
| Unknown | Permission denial, authentication/transport failure, timeout or unexpected response | Stop dependent setup; diagnose the failed boundary. Do not infer absence or activate. |

For missing state, show the exact target and command before seeking activation approval. An approved adaptation is `gcloud services enable aiplatform.googleapis.com` with the same explicit scope flags. Do not disable a working service to create a missing-state test. Keep environment-file writes separate; update only intended configuration fields after readiness is confirmed, preserving unrelated keys and secrets.

If an enable request times out or returns an error after submission, its outcome may be unknown. Retain a sanitised operation identifier if provided, query that operation through the supported CLI/API and independently re-read service state. Do not automatically submit another activation. A later confirmed-enabled run must reuse completed setup. Offline tests should simulate missing, denied, timeout, accepted-then-error and already-enabled/repeat branches. Historical coverage of those branches used a fake gcloud executable; it did not establish fresh live activation.

## Prove each permission boundary separately

Use this order so a later failure has a useful explanation:

1. Confirm project visibility and API state.
2. Verify the selected ADC or key route without exposing credentials. Successful credential refresh establishes authentication only.
3. After scoped paid-call approval, make the smallest useful inference preflight with the selected model/location and isolated tools. Preserve its result rather than adding ad hoc model/region fallbacks.
4. If managed scoring is needed, verify its separate service/identity requirements and result-export path. A model response proves neither scorer access nor tool-backend permissions.
5. Exercise actual remote tool contracts in the approved staging target when that is part of the request. Local synthetic tools cannot establish remote schemas, authentication or unknown-write handling.

Classify errors before retrying: identity/configuration, permission, billing/quota, unsupported model/location, transient transport, product failure or evaluator failure. Limit retries to diagnosed transient infrastructure failures; retain product failures as observations. A permission-denied service-account lookup does not prove that the account is absent. Provider-managed service-agent membership may require project IAM evidence. Successful execution by an Owner account is not proof of a least-privilege production policy.

Check interpreter architecture as well as versions when a worker fails before importing the agent. The historical campaign encountered an incompatible native execution environment before model work. A traceback before dispatch is different evidence from a provider rejection; preserve that distinction.

## Finish with a scoped cleanup claim

Before live work, record owned process IDs, ports, local paths and any created cloud resource identifiers, including project/location and operation state. Distinguish pre-existing state from created state. Cleanup remains a separately confirmed action against that ledger; verify completion and make a repeat invocation a harmless no-op.

For this chapter, local ADK Web plus cloud inference created no deployed application or persistent billable infrastructure. Stopping a local process does not reverse accepted provider usage, provider-side retention or resources created elsewhere. Say precisely which owned resources were removed, which inventories/regions were checked, and which checks were denied or incomplete. A disabled API or stale asset index is not authoritative proof of absence. Do not turn a scoped test cleanup into a project-wide no-cost guarantee or delete shared resources to obtain one.

Completion: report the observed access/setup state, executed versus proposed operations, owned-resource disposition and remaining unknowns. General Cloud Run, GKE or Agent Engine deployment is outside this skill's job; evaluating an already deployed target should preserve that target's deployment process.
