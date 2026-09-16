# Operate and diagnose an authenticated-tool integration

Read for an approved lab, setup failure, release plan or cleanup review. This runbook translates observed failures into ordered checks; it is not a deployment script. Use [GCP credentials](gcp-credentials.md) for authority and custody, [validation](validation.md) for acceptance, and the entrypoint's approval boundary before external actions.

## 1. Declare the integration being tested

Record each boundary independently: application identity, provider, credential store, model and serving platform. Useful stages are local identity/mock provider/local store; the same application with real Secret Manager; and real model/tool acceptance. Real Google consent, Firebase and hosted deployment each add separate gates. Changing one component to live does not make the others live.

The historical successful combination was a loopback gateway, development JWT, mock Calendar, real Secret Manager and real Gemini. Use this as a debugging sequence, not a production authentication template. Decide which stage answers the user's question before provisioning anything.

## 2. Resolve configuration and identity before spending

Inventory the selected project, location, CLI operator, application ADC source, impersonation target, quota project, model backend/key source, resource names and process configuration. Report only required metadata. A changed IDE project or successful CLI login does not prove application access: [CLI credentials and ADC are separate](https://docs.cloud.google.com/docs/authentication/application-default-credentials). A root environment file may differ from the service's file, and an already-running process may retain old settings.

For a disposable lab, use a private per-run directory for generated ADC/configuration, database and logs. If isolating CLI configuration, use `CLOUDSDK_CONFIG` according to the [CLI configuration contract](https://docs.cloud.google.com/sdk/gcloud/reference/topic/configurations); do not assume an empty directory inherits the operator's login. Keep the normal login and ADC intact. Record only owned temporary paths for later cleanup. Never print credential-file contents or use token-printing commands as a readiness report.

Read-only preflight examples, after resolving `PROJECT_ID` to the user's intended target:

```bash
gcloud projects describe "$PROJECT_ID" --format='json(projectId,projectNumber,lifecycleState)'
gcloud services list --enabled --project="$PROJECT_ID" --format='value(config.name)'
```

Choose API requirements from the selected path: Secret Manager for custody, IAM Credentials for impersonation, and the actual model/provider APIs. A missing API requires a separate approved activation step. Billing, quota or key-attribution queries may be unavailable; preserve that uncertainty rather than enabling additional services just to complete an inventory. Configuration claiming a key belongs to a project is weaker evidence than verified attribution.

## 3. Make setup repeatable through partial failures

Before the first mutation, validate required private inputs without echoing them and inventory **all** proposed identities/secrets to establish ownership or absence. Use successful exact listings; a failed describe, permission denial or failed list is not absence. If approved API activation changes what can be inventoried, repeat the ownership inventory before resource creation. Reject a same-named unowned resource before touching any other target.

Persist successful creations and exact selected version names as they happen. A repeat should reuse a valid owned resource, avoid adding duplicate secret versions and leave unrelated resources unchanged. A secret write's returned numeric version is the activation candidate; a subsequent lookup of `latest` may select a disabled or unrelated version. On partial failure, retain the ledger and make cleanup possible without rerunning the failed provisioning stage.

For shell automation, inspect machine-output contracts too. In the chapter, CLI `value(name)` transformation shortened resource names and broke comparisons until full output was requested with `value[no-transforms](name)`. Prefer structured JSON or explicitly untransformed output and test the actual format. Offline CLI doubles should model transformed names, denied listings, stale listings, API activation, name collisions and failure after the first creation. A happy-path fake can hide the defect it is meant to test.

## 4. Diagnose the first failed gate

| Observation | Next discriminating check | Response |
| --- | --- | --- |
| Project lookup denied | Exact CLI account, target project and required access | Stop dependent setup; existence and API availability remain unknown |
| Just-created account returns `NOT_FOUND` | Exact successful creation record and account name | Bound read-only visibility checks; do not replay creation |
| Account exists but token minting returns `iam.serviceAccounts.getAccessToken` denial | Target identity, caller and scoped Token Creator grant; compare CLI and application paths when an approved probe permits | Retry only recognised propagation under the finite budget; do not broaden grants |
| Scope/API/quota-project error during credential refresh | Credential configuration and relevant enabled service | Fix that prerequisite; do not classify every 403 as propagation |
| `ACCESS_TOKEN_SCOPE_INSUFFICIENT`, `SERVICE_DISABLED` or `UREQ_PROJECT_BILLING_NOT_FOUND` | Scope, consumer project/API or billing prerequisite respectively | Stop the dependent path and reconcile partial setup; an unavailable billing query does not mean billing is disabled |
| Impersonation works but secret access fails | Exact secret, selected version/state, runtime resource grant and quota project | Test this layer before repeating OAuth and writing more versions |
| Model metadata succeeds but generation returns 429 | Safe structured reason/quota details, backend, actual key source and applicable billing status | Metadata proves model discovery, not generation admission |
| Provider refresh fails | Recognised invalid grant versus transient/transport/schema failure | Apply the [lifecycle policy](oauth-lifecycle.md); preserve valid durable consent on transient failure |
| Health check passes but chat/tool fails | Real authenticated route, owned session, correlated tool call/result | Health is not functional acceptance |

Account visibility and IAM grant effectiveness are separate. The observed grant became effective after about 90 seconds without alteration; this is one measurement, not a fixed sleep or SLA. [IAM propagation](https://docs.cloud.google.com/iam/docs/access-change-propagation) varies. The lab reader helper allowed eight attempts 30 seconds apart only for its recognised IAM denial; choose explicit bounds for the target and stop on exhaustion. Then test actual secret access: token minting alone does not verify secret-level permission.

The model incident reproduced a depleted-prepayment 429 with a second model, then stopped. Preserve selected reason/quota/retry identifiers and a safely redacted explanation when structured details are absent; do not store raw response bodies or headers. A funded balance cannot guarantee freedom from rate limits, and a generic 429 cannot establish depleted credits. Check the selected backend's current [billing](https://ai.google.dev/gemini-api/docs/billing) and [rate-limit](https://ai.google.dev/gemini-api/docs/rate-limits) guidance. Billing admission failures need the account prerequisite resolved; model switching and retry loops do not repair it. Keep the user's default model unchanged unless the task includes migration. Alternate-model probes, when justified and approved, need their own small send budget and stop once the cause is established. Payment amounts and purchases are owner decisions, not automatic skill actions.

## 5. Enforce the real work budget

Count HTTP/model attempts at the transport boundary, not just ADK events or top-level CLI commands. Failed sends may produce no event; SDK/transport retries may occur below a configured model retry policy. The recorded GenAI 2.23.0 path needed independent protection against aiohttp connection retries. Inspect the pinned transport and test with an external boundary double instead of applying private monkey patches from an old SDK to a new one.

Reserve each request's maximum duration inside one monotonic campaign deadline before dispatch, with a separate allowance for cleanup. Stop new test work when its budget expires while keeping owned-resource cleanup available under its approval. Account for model turns, tool calls, retries and provider pages separately. For resumable verification harnesses, record dispatch intent before sending so a crash cannot silently replay a paid attempt. A timeout leaves dispatch outcome uncertain; it does not refund the attempt. Close the campaign on success, known blocker or exhausted budget; another run needs fresh accounting under its approved scope. A model answer with a tool usually takes multiple model sends.

## 6. Prepare a hosted release without overstating the lab

The companion ships no managed deployment. Preserve the target's platform and deployment tooling; prepare its exact release plan rather than copying a local Uvicorn command to production. Complete the applicable gates before release:

| Target | Work that the local lab does not establish |
| --- | --- |
| Combined hosted gateway and agent | Attached keyless runtime identity, real application identity, production OAuth origin/redirect, durable sessions/connections and content-safe ingress logs |
| Gateway plus separate agent/tool service | Workload authentication and trusted end-user context on the second hop; see [identity boundaries](identity-and-output.md) |
| Multiple processes/replicas | Shared transactions/revisions, refresh coordination, cache invalidation, restart and warm-replica acceptance |
| Managed authentication | Supported provider/finalisation/continuation contract; see [continuations](adk-continuations.md) |

Keep development/staging/production projects, workloads, OAuth clients, redirects and credentials separate. Test the deployed runtime's actual identity and version binding, error/log/export paths, denied users, later calls and release rollback. Local SQLite, local encrypted files and a development JWT signer are lab choices, not evidence of production persistence or identity. Secret version rollback also depends on whether the provider still accepts the old material.

## 7. Close with scoped evidence

Stop owned serving/worker processes before cleanup, flush their logs/exporters and retain only sanitised evidence. Preview all owned deletion targets together, confirm the separate cleanup plan, then recheck ownership before each deletion. Repeat cleanup for already-absent resources and independently verify exact absence; API denial or an empty failed query is inconclusive. Check partial-setup residue and preserve pre-existing grants/resources and the operator's normal credentials.

Retain the same project/resource-name settings used for creation; do not fall back to default names during recovery. The cleanup principal needs the exact listing permissions used to prove absence as well as deletion permission. Cloud deletion does not clean local configuration/databases, OAuth clients, consent-screen settings or provider grants. Handle each owned artefact explicitly. Preserve key/ciphertext pairs when resuming a local encrypted store.

Report separate outcomes for local disconnect, provider revocation, version disabling/destruction, cloud resource deletion and removal of owned local files. Disconnect does not erase sessions, events, indexes or backups. Disabled secret versions are still active for [Secret Manager billing](https://cloud.google.com/secret-manager/pricing); retirement is not cost closure. Billing reports can arrive later, and absence of the lab's resources does not establish an empty project. Do not disable project billing or delete unrelated resources as an implicit cleanup step.

Completion is an evidence table showing what ran, which identities/backends were real, what remains unknown, the owned-resource ledger and verified cleanup. See [compatibility and evidence](compatibility-and-evidence.md) for the source of these lessons. External documentation above was checked on 16 September 2026; recheck provider/SDK contracts when applying this runbook.
