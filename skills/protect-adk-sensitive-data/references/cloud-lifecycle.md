# Cloud readiness, controlled setup and cleanup

Use only when the task needs managed services or resource lifecycle work. The
approval requirements in [SKILL.md](../SKILL.md) apply. No provisioning or
deletion script is bundled: generate a concrete plan for the target's existing
infrastructure tooling, validate it offline, and execute only the approved scope.
For startup/import, TLS, permission, quota, unexpected SDK return, or accounting
failures, use the matching recipe in [troubleshooting.md](troubleshooting.md).

## Keep the configuration planes explicit

Populate this matrix from the target application before generating commands.
Variable names below describe the companion convention; adapt to the target's
configuration rather than adding a second configuration system.

| Plane | Record | Verification and implication |
| --- | --- | --- |
| Operator | Explicit CLI account and template/IAM administration identity | CLI login and SDK ADC can select different identities. Keep administrative credentials out of the application process |
| Runtime | ADC/workload identity source, expected principal, quota project | Read permissions, sanitise permissions and model access are separate tests; a created impersonation file proves none of them |
| Model | Backend, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, model ID, output limit | In the historical Vertex run both API-key variables were empty. A security-backend switch does not switch the model backend |
| Protection | `SECURITY_PROJECT_ID`, `SECURITY_LOCATION`, three SDP IDs, full input/output Armor names | Check the exact configured resources and regional endpoints. Model and protection locations need not be identical |
| Gateway | Auth verifier, policy version, request/RPC deadlines, concurrency, session store, public routes | Identify every HTTP/SSE/runner entry point and which protection sequence it executes |
| Telemetry | Application, ADK/GenAI capture, SDK debug logs, exporters, proxy logs | Disable content capture at each receiving layer; application log filtering alone cannot cover another exporter |

The historical configuration used Vertex generation at `global` and protection
services at `us-central1`. These are evidence values, not deployment defaults.
The companion's `PROTECTION_BACKEND=local` replaced protection services only;
ordinary requests still called Gemini. Offline checks must replace the model too.

Use the exact inspected settings and override semantics in
[observability configuration](implementation-recipes.md#configure-and-verify-observability).
Validate the effective deployment configuration before constructing the runtime
and inspect emitted records with a synthetic canary; an environment variable's
presence alone proves no telemetry property.

## Establish the actual target

Record the operator identity separately from the application identity. Inspect
the explicitly selected project and API metadata with bounded read-only calls;
never silently change `gcloud config` to make a command succeed. For example,
with `GCP_PROJECT_ID` and `OPERATOR_ACCOUNT` already resolved by the user or
trusted configuration:

```sh
gcloud projects describe "$GCP_PROJECT_ID" --account="$OPERATOR_ACCOUNT" --format='value(projectId,lifecycleState)'
gcloud services list --enabled --project="$GCP_PROJECT_ID" --account="$OPERATOR_ACCOUNT" --format='value(config.name)'
```

Set subprocess timeouts and disable interactive API-enablement prompts. Do not
dump tokens, full ADC files, `.env` contents or HTTP authentication diagnostics.
An inaccessible project remains **unverified** even if an IDE shows it selected.
Separate CLI login, ADC source identity, quota project and model backend. A root
API key change does not rewrite chapter/package-local configuration, and an API
key for one backend is not proof of ADC access to another. Do not copy keys into
the skill or create credentials just for inspection.

Identify which APIs are needed: `dlp.googleapis.com`,
`modelarmor.googleapis.com`, and `aiplatform.googleapis.com` for Vertex model
generation; `iam.googleapis.com` / `iamcredentials.googleapis.com` only when the
identity workflow requires them. `serviceusage.googleapis.com` supports service
usage checks. Missing API availability, billing, content-use permissions or
quota are distinct blockers. A template GET proves none of the paid model path.
If a billing-status read reports `SERVICE_DISABLED` for
`cloudbilling.googleapis.com`, billing status is unknown; that is neither a
disabled-billing verdict nor permission to activate another API. Keep service
activation explicit and separate from content requests. Record each required
API as already enabled, activated in this run, missing, or inaccessible; an
already-enabled API does not exercise fresh-project activation.

Use configured model/security projects and locations, not historical defaults.
Verify current model availability and provider filter/location support against
primary documentation when planning a new environment. Matching resource
locations alone is not a residency guarantee: review the effective policy and
all services that receive or store content.

## Produce the approval-ready change

Present a resource/command manifest with concrete values, separated into setup,
runtime checks, paid test calls and cleanup. Include the intended identity and
quota project, API changes, each template's policy, estimated cost bound,
maximum calls per service, absolute stop time and ownership journal path.
Unresolved names or cost limits mean the plan is not ready to execute.

For the baseline combined pattern, the resource set is two SDP inspection
templates (deny and PII), one SDP de-identification template and input/output
Armor templates. Reuse an existing approved policy when appropriate; do not
create duplicate templates just because an example uses five. Template
configuration should omit finding quotes, reject transformation failures,
disable payload logging, and avoid ignoring partial screening failures.

Prefer the existing deployment identity through ADC/workload identity. Separate
template administration from runtime content use. The historical custom runtime
role contained these seven permissions; treat it as evidence for that exact
workflow, not a universal role:

```text
aiplatform.endpoints.predict
serviceusage.services.use
dlp.inspectTemplates.get
dlp.deidentifyTemplates.get
modelarmor.templates.get
modelarmor.templates.useToSanitizeUserPrompt
modelarmor.templates.useToSanitizeModelResponse
```

Inspect current method requirements and existing grants before proposing any
change. Model Armor's sanitise method requires a distinct use permission;
template viewing is separate. [SanitizeUserPrompt IAM reference](https://docs.cloud.google.com/model-armor/reference/rest/v1/projects.locations.templates/sanitizeUserPrompt).
Do not grant service-agent roles to a workload to bypass errors.
[Model Armor role reference](https://docs.cloud.google.com/model-armor/access-control/roles-permissions).

If impersonation is needed, scope Token Creator to the exact service account.
Creating an impersonated ADC file is still a credential operation requiring
approval. Such a file may embed a refresh token even though the minted access
tokens expire. Keep it private (directory `0700`, file `0600` on POSIX), outside
version control and logs, and include local credential removal in the plan.
Do not create downloadable service-account private keys.

## Assemble resources in dependency order

Use this dependency order with the target's existing IaC or setup scripts:

1. **Prerequisites:** resolve the configuration matrix, service support, API
   state and exact owned/foreign-resource inventory. Save prior IAM state before
   changing it. Passing a plan/dry-run establishes the proposed shape only.
2. **SDP policy:** create or reconcile deny-inspection, PII-inspection and
   de-identification templates. Read back the actual names and policy. Deny and
   PII templates must remain distinct when credentials must be rejected before
   permitted PII replacement. See [sdp.md](sdp.md) for their contracts.
3. **Armor policy:** create or reconcile input/output templates referencing the
   resolved SDP resources. In the combined pattern input SDP may transform;
   output SDP inspects and withholds disallowed PII. Read back required filters,
   partial-failure behaviour and payload-logging settings. See
   [model-armor.md](model-armor.md) for verdict and filter semantics.
4. **Runtime access and configuration:** apply only the needed grants, then
   export resource names from successful readbacks to the runtime configuration.
   Bind the deployed policy version to that configuration. Do not synthesize
   successful outputs from the names a failed create intended to use.
5. **Runtime preflight:** use the application's actual identity to GET every
   configured template and compare effective policy. Check detector sets and
   thresholds, all-finding replacement, transformation-error rejection, Armor's
   SDP references, required filters and content-logging/partial-failure controls.
   A template's existence alone is not a configuration pass.
6. **Bounded acceptance:** after the offline gates, establish content-use/model
   permission with the minimum approved synthetic calls, then exercise the
   actual protected entry point. Use the evidence gates below.

The inspected Python clients used explicit `ClientOptions(api_endpoint=...)`:
`dlp.{security_location}.rep.googleapis.com` and
`modelarmor.{security_location}.rep.googleapis.com`. DLP names are
`projects/{project}/locations/{location}/inspectTemplates/{id}` or
`.../deidentifyTemplates/{id}`; Armor names are
`projects/{project}/locations/{location}/templates/{id}`. An Armor template can
therefore exist while pointing to an incorrect SDP name. Validate every resolved
reference. Confirm endpoint and location support for a new environment before
copying these historical SDK forms. Cross-project references require separately
verified service-agent access; the historical same-project campaign did not
establish that integration.

## Idempotent reconciliation

For any setup helper you generate:

1. Offer `--help` and `--dry-run`; validate targets before client creation.
   Dry-run must not enable APIs, create credentials or make paid content calls.
2. Bind a private ownership journal to the exact project, location and run ID.
   Record intent before mutation, returned identifiers after success, and enough
   prior state to restore only changes this workflow owns. Never record secrets.
3. Before creating a deterministic name, read the existing resource. Refuse a
   same-named foreign resource. An ambiguous failed read is not absence.
4. Reconcile a successful repeat to the same owned resource; do not create a new
   resource on each invocation. Preserve partial state after failure so recovery
   can finish or clean up safely.
5. Bound retries and total time. On an uncertain create/side-effect response,
   reconcile by identity/idempotency key before retrying. Count actual RPC
   attempts where possible: one CLI command may paginate or retry internally.

Switching projects requires fresh target-bound state; do not reuse old resource
IDs or discard the old journal until its resources are accounted for. These
ownership and recovery principles come from the historical lifecycle tests (E8).

## Bounded live verification and cleanup

After explicit approval, use an isolated disposable target and synthetic data,
unique resource identifiers and labels where the service supports them. Verify
preflight reads, then the minimum content calls needed to establish runtime
permissions, then the bounded gateway cases. Stop on quota errors or exhausted
budgets. Diagnose a 429 by backend, credential/quota project, model, response
metadata and current quota; never assume a payment on another backend fixed it.
Start with retries disabled. Report cold/warm timing and sample count honestly.
For the accounting implementation, retry layers, diagnostic privacy and concrete
historical limits, read [troubleshooting.md](troubleshooting.md#live-budget-and-retry-accounting).

Use separate evidence gates so a health response cannot stand in for functional
or permission checks:

| Gate | Meaningful completion evidence |
| --- | --- |
| Import/startup, offline | Selected interpreter imports typed SDK messages; target application starts with the model and providers replaced; child process exits cleanly |
| Template readiness, read-only | Exact configured resources read under runtime identity and effective policies validated; missing/denied/transport failures reported distinctly |
| Runtime authorization, live | Synthetic direct inspect/de-identify and input/output sanitise assertions pass under runtime identity; then a genuine model response on the configured backend |
| Protected gateway, live | Authenticated useful answer and owned-tool result; transformed persisted/tool state; cross-user, cross-session and invalid-auth refusal with no unauthorized disclosure |
| Release and latency | Screened final text for both JSON/SSE; initial status event excluded; passing usable answers required before a latency target can pass; raw cold/warm counts and range reported |
| Teardown | Exact owned template absence; runtime principal/grants removed or restored; other IAM preserved; child processes gone, port closed, temporary credential/configuration removed |

Do not put paid canaries into every health probe. Use ordinary liveness for
process health and bounded readiness/configuration checks appropriate to the
deployment. A provider outage should withhold affected requests without
triggering an uncontrolled restart/probe/call loop. The historical campaign used
explicit acceptance, not continuous paid health testing.

## Hosting and integration coverage

The historical deployment was a local loopback HTTP/SSE gateway calling managed
providers. It did not deploy that gateway to Cloud Run, GKE or Agent Runtime.
Apply these as **production guidance** only when hosted deployment is requested:

| Surface | Boundary decision before release |
| --- | --- |
| Cloud Run or GKE gateway | Run the same protected application routes, attach a runtime identity, integrate real authentication, and check ingress/egress, concurrency and timeout settings. Re-run the deployed route canaries; a container start is insufficient |
| Managed Agent Runtime or another managed runner | Establish where input first becomes an event/history write, which callbacks actually execute, and who releases output. If the service stores raw input before application screening, an application callback cannot repair that earlier disclosure |
| Model Armor proxy/platform integration | Document the hops it covers. A model-request proxy alone does not protect application ingress persistence, tool side effects, local history, alternate provider routes or public streaming. Preserve controls at those boundaries |
| Multiple replicas | Move ownership checks, session/policy state and same-session serialization to appropriate shared storage/concurrency controls. The companion's in-memory sessions and locks are process-local |
| Production identity | Replace the development bearer fixture with the trusted identity verifier. The companion fixture refuses production mode; changing that flag is not an authentication integration |

For each surface, draw the actual route from authenticated ingress through
screening, persistence, model/tool calls and release, including bypass routes
such as a plain ADK web entry point. Protect or remove bypass routes before
making a hosted protection claim. Reuse [boundaries.md](boundaries.md) for the
application invariants instead of redesigning an unrelated hosting stack.

Residency review follows every recipient: gateway region, model endpoint,
protection services, session storage, logs/traces and retained provider data.
The historical global-model/regional-protection combination establishes no
regional residency guarantee. Choose supported regions and effective policies
for the target's actual requirement before deployment.

## Owned teardown and retained state

Cleanup is a separate approved operation. Delete only journal-owned resources,
restore only this run's scoped IAM changes, remove private local credentials,
and retain unrelated resources/shared APIs. Continue independent cleanup after
one failure, then verify each resource's absence with an independent read.
Repeated cleanup should succeed when the owned resources are already absent.
The recorded Model Armor SDK deletion returned `None`, not a long-running
operation; check the installed return type before calling `.result()`.
Delete dependent Armor templates before the SDP resources they reference.
Remove only grants this run added; if concurrent or foreign bindings remain on
an owned custom role, preserve it for reconciliation rather than deleting a
shared dependency. Keep prior-policy and ownership evidence through the final
independent reads. Deleted IAM resources may leave tombstones/reserved IDs, so
a later campaign needs fresh names rather than trying to reuse deleted IDs.

Report failed or unobservable deletions, retained backups/soft-deleted data,
versions, endpoints, disks and other billable descendants if the task created
them. Resource absence and billing-ledger settlement are different checks.
Never conclude a whole project is cost-free from an empty list in one region or
service. This chapter-level pattern requires no VM, Spanner instance or RAG
corpus; creating those needs a separate scoped requirement and approval.

For an inventory-based cleanup claim, confirm successful direct service reads
and complete pagination in the stated locations. An asset index can lag behind
deletion; a disabled API, permission failure or unsupported wildcard route means
that direct check is unverified. Correct the query/attribution within the
authorized scope instead of translating an error into zero resources. Record
retention timestamps and unknown sizes separately from active workloads.

The 15 September read-only cleanup audit found Chapter 8's templates absent,
while soft-deleted storage from other chapters and source staging remained.
That is useful evidence that a successful scoped teardown and a project-wide
zero-charge claim are different conclusions. Those buckets were not created by
the Chapter 8 lifecycle. Template deletion also does not erase provider logs,
backups or earlier usage. Check current retention and billing evidence when a
user asks about continuing charges; historical timestamps are not today's state.

## Evidence and source navigation

These are provenance pointers in the pinned companion described by
[compatibility.md](compatibility.md), not files required by an installed skill:

| Lesson | Public companion source / evidence |
| --- | --- |
| Configuration, readiness and activation distinctions | `.env.example`; `README.md`, “Real Google Cloud mode” and “Optional independent verification campaign”; `scripts/preflight.py` |
| Setup dependency order, endpoints and actual outputs | `infrastructure/provision_dlp.py`, `provision_model_armor.py`, `lifecycle.py`; `tests/test_lifecycle_cli.py` |
| Activation and real partial-setup recovery | `audit/INDEPENDENT_AUDIT_2026-09-13.md`, “Access, activation and complete lifecycle”: five activations; Service Usage already active; typed cause of early PermissionDenied unknown |
| Full managed gateway and cleanup | `audit/INDEPENDENT_AUDIT_2026-09-14.md`, “Release gates and applicability”, “Setup, tests and meaningful live assertions”, “Reproducibility and cleanup”: 20 gateway cases passed; API activation not repeated |
| Inventory lag, inaccessible listings and retained storage | `audit/CLEANUP_RECHECK_2026-09-15.md`, “Retained storage can still incur charges” and “Important scope and access limits”: historical read-only cross-chapter inventory, not an expanded Chapter 8 deployment |

Hosted guidance above has no corresponding historical hosted-release claim.
