# Cloud readiness, controlled setup and cleanup

Use only when the task needs managed services or resource lifecycle work. The
approval requirements in [SKILL.md](../SKILL.md) apply. No provisioning or
deletion script is bundled: generate a concrete plan for the target's existing
infrastructure tooling, validate it offline, and execute only the approved scope.

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

Cleanup is a separate approved operation. Delete only journal-owned resources,
restore only this run's scoped IAM changes, remove private local credentials,
and retain unrelated resources/shared APIs. Continue independent cleanup after
one failure, then verify each resource's absence with an independent read.
Repeated cleanup should succeed when the owned resources are already absent.
The recorded Model Armor SDK deletion returned `None`, not a long-running
operation; check the installed return type before calling `.result()`.

Report failed or unobservable deletions, retained backups/soft-deleted data,
versions, endpoints, disks and other billable descendants if the task created
them. Resource absence and billing-ledger settlement are different checks.
Never conclude a whole project is cost-free from an empty list in one region or
service. This chapter-level pattern requires no VM, Spanner instance or RAG
corpus; creating those needs a separate scoped requirement and approval.
