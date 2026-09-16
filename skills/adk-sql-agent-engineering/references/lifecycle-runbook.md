# SQL application lifecycle runbook

Use this reference when implementing, diagnosing or recovering the cloud lifecycle
of an SQL application. It supplies algorithms and command patterns; it does not
require the book, companion scripts or a particular project layout. Adapt them to
the target's existing entry points and retain its dependency pins.

The recorded baseline was **local ADK Web with managed BigQuery and Gemini through
Vertex AI**. It provisioned synthetic tables and a runtime identity. Cloud service
hosting, public ingress, workload identity deployment and regional RAG backends
were not part of that SQL baseline. Add those only for a requested integration.

Read sections 1–3 for planning, 4–7 for implementation/recovery, and 8–10 for
closure. The approval boundary is defined in [the skill](../SKILL.md#4-obtain-approval-at-the-consequential-boundary);
query policy belongs in [execution safety](execution-safety.md).

## 1. Record the actual target and configuration

Complete this record before constructing clients. These are local planning names,
not environment variables the target application necessarily understands.

| Field | Record and verify |
| --- | --- |
| `SQL_RESOURCE_PROJECT` | Project containing the approved dataset; query-job and model projects too if different |
| `SQL_QUOTA_PROJECT` | Intended consumer for source ADC and impersonated credential requests |
| `SQL_OPERATOR_ACCOUNT` | Explicit CLI bootstrap account; separately establish the source ADC principal |
| Dataset and `SQL_BQ_LOCATION` | Exact dataset ID, approved tables and physical location |
| Model configuration | Backend, model ID, endpoint location and any separate model resource project |
| `SQL_RUNTIME_EMAIL` | Optional dedicated runtime account, owning project and provider unique ID |
| Recovery state | Private path, owner ID, state version, fixed fixture seed date and operation IDs |
| Limits | Query billing cap, row cap, per-call timeouts, lifecycle deadline and campaign cutoff |
| Configuration precedence | Process variables, each loaded `.env`, config defaults and credential overrides |

Inspect the loader rather than assuming precedence. In the tested application,
process variables won and the chapter-local `.env` filled missing values. Check
inherited API keys, `GOOGLE_APPLICATION_CREDENTIALS` and impersonation overrides
without printing their contents. Preserve unrelated credential files.

The baseline used one project for resources and quota. Intentional multi-project
designs need separate recorded permissions; equality is not a universal rule.
Vertex ADC and a Gemini Developer API key are different backend choices. A model
API key never replaces BigQuery credentials. A local project setting alone proves
neither access nor billing nor the effective principal.

## 2. Separate offline plan, read-only preflight and mutation

**Offline plan:** resolve local configuration and print exact inventory, identities,
API allowlists, role scopes, limits and cleanup scope. Keep imports/client factories
lazy: planning must work with a missing credential file and make no provider call.
It may describe prospective state without creating an ownership claim.

**Read-only preflight:** inspect project access, billing, API availability, actual
Python credentials and existing-resource ownership. The following pattern requires
explicit target variables and confines overrides to a subshell. It runs no login,
configuration write, API activation or resource mutation. Use the installed CLI's
supported flags; a failed inspection is a prerequisite failure, not absence.

```bash
(
  set -eu
  : "${SQL_RESOURCE_PROJECT:?Set the approved resource project}"
  : "${SQL_QUOTA_PROJECT:?Set the approved quota project}"
  : "${SQL_OPERATOR_ACCOUNT:?Set the approved CLI operator}"
  export SQL_QUOTA_PROJECT
  export CLOUDSDK_CORE_DISABLE_PROMPTS=1
  export CLOUDSDK_CORE_SHOULD_PROMPT_TO_ENABLE_API=0
  export CLOUDSDK_AUTH_IMPERSONATE_SERVICE_ACCOUNT=''
  export GOOGLE_CLOUD_QUOTA_PROJECT="$SQL_QUOTA_PROJECT"

  gcloud projects describe "$SQL_RESOURCE_PROJECT" \
    --account="$SQL_OPERATOR_ACCOUNT" --project="$SQL_RESOURCE_PROJECT" \
    --billing-project="$SQL_QUOTA_PROJECT" --quiet --format='value(projectId)'
  gcloud services list --enabled \
    --account="$SQL_OPERATOR_ACCOUNT" --project="$SQL_RESOURCE_PROJECT" \
    --billing-project="$SQL_QUOTA_PROJECT" --quiet --format='value(config.name)'
  gcloud billing projects describe "$SQL_RESOURCE_PROJECT" \
    --account="$SQL_OPERATOR_ACCOUNT" --project="$SQL_RESOURCE_PROJECT" \
    --billing-project="$SQL_QUOTA_PROJECT" --quiet --format='value(billingEnabled)'

  python - <<'PY'
import os
import google.auth
credentials, _ = google.auth.default()
actual = getattr(credentials, "quota_project_id", None)
print("ADC type:", type(credentials).__name__)
print("Source ADC quota project:", actual or "(unset)")
if actual != os.environ["SQL_QUOTA_PROJECT"]:
    raise SystemExit("Source ADC quota project differs from the approved target")
PY
)
```

Use the target's selected Python interpreter. Credential construction may inspect ADC;
this example does not refresh or display tokens. It does not prove the ADC account
matches the CLI account. Establish that principal through the credential source or
an approved identity-only check, retaining tokens solely in memory.

Keep the quota override in each later bootstrap/runtime/cleanup process. The source
ADC quota consumer is evaluated during impersonation before runtime credentials
can be used; setting a quota project only on the final credentials
does not correct the source exchange. Avoid rewriting shared ADC to fix one lab.

**Approved mutation:** present the completed plan, then execute only its authorised
operations. Compute missing APIs from a successful enabled-services response;
activate exactly that approved subset and reread it before creating resources.
Billing linking, quota increases and broad IAM grants are separate operations.
Completion criterion: known prerequisites and ownership, or a specific blocking
check with zero unintended mutation.

## 3. API and permission matrix

These names describe the tested Google Cloud path, not a universal service bundle.
Prefer required permissions/custom roles where the target already defines them.

| Purpose | APIs | Identity and access boundary |
| --- | --- | --- |
| BigQuery/Gemini through Vertex | `bigquery.googleapis.com`, `aiplatform.googleapis.com` | Runtime: `roles/bigquery.jobUser` on query-job project, `roles/aiplatform.user` on model project, dataset/view read access only |
| Prerequisite inspection | `serviceusage.googleapis.com`, `cloudbilling.googleapis.com` | Operator can inspect enabled services and billing; only approved activation needs `roles/serviceusage.serviceUsageAdmin` or equivalent |
| Fixture provisioning | BigQuery | Operator needs dataset/table creation, load-job submission and scoped data editing, e.g. appropriate `roles/bigquery.dataEditor` and Job User grants; runtime receives no fixture-write permission |
| Optional local impersonation setup | `iam.googleapis.com`, `iamcredentials.googleapis.com`, `cloudresourcemanager.googleapis.com` | Operator needs scoped account lifecycle, relevant project/account IAM and dataset access-list changes |
| Optional impersonated runtime | Same runtime APIs plus IAM Credentials | Named source operator gets `roles/iam.serviceAccountTokenCreator` only on the intended account; runtime gets `roles/serviceusage.serviceUsageConsumer` on the applicable quota project |

The tested runtime's dataset grant was `READER`, equivalent to its dataset read
purpose; do not convert it into project-wide data access. Source ADC also needs
any consumer permission required for its quota project. Inspect the existing
grants before adding any. An operator's existing Owner grant is evidence about
that run, not a setup recommendation. Preserve unrelated bindings and conditions.

An attached runtime identity may need no local impersonation helper. A Developer
API backend has a different model authentication/API contract; retain BigQuery
ADC and determine that backend's prerequisites separately. Secret Manager is
needed only if this application actually stores a secret there.

## 4. Implement a durable operation journal

Persist intent before the first external mutation, then record observed outcomes.
Use a private, versioned record such as the following shape (illustrative fields):

```text
version; target(project, dataset, location); owner_id; seed_date
dataset_status: provisioning | ready | deleting | deleted
tables: exact names, ownership labels, stable load job IDs
runtime: email, unique_id, source_operator
  status: provisioning | ready | deleting | deleted
  creation_started; account_delete_started
  project_grants: role -> preexisting | pending | added | removed
  dataset_grant; token_creator_grant: same provenance states
operations: provider identity, intended action, outcome, reconciliation evidence
```

Acquire an exclusive lock before reading/modifying the journal. Write a private
temporary file, flush and synchronise it, then atomically replace the record.
The source used POSIX locking and mode `0600`; use equivalent supported mechanisms
elsewhere. Distributed workers need a durable store with concurrency control,
which was not tested in the baseline. Preserve a recoverable backup.

Validate journal version, exact target/location, owner format and operation
inventory on every resume. Refuse mismatched configuration rather than redirecting
old IDs to a new project. Use a unique lab owner label on dataset and tables.
For an account, verify both its ownership marker and saved provider unique ID;
an account recreated with the same email is a different identity.

Record a grant as `preexisting` if it already exists. Otherwise persist `pending`
before the write, reread after uncertainty, and mark `added` when observed. Cleanup
may remove an observed grant recorded as `pending` or `added`, preserving unrelated
principals and pre-existing grants. Use provider concurrency controls when updating
policies/access lists; a full policy overwrite can erase concurrent changes.

If account creation was attempted but its outcome is unknown, retain the marker.
Reread the exact account and validate ownership before adopting the result. A
temporarily empty inventory does not authorise another create or a `deleted`
status. Establish the earlier request's outcome before an explicit recovery action.
Completion criterion: every owned mutation has durable intent and a reconcilable
identity; failures leave sufficient state for another process to continue.

## 5. Provision fixtures without duplicate loads

Use an isolated dataset with a target-specific safety naming rule and exact table
inventory. A suffix is a useful mistake guard, not ownership proof. Inspect all
existing tables and their labels first; preserve unknown resources and refuse
adoption by relabelling. Treat only the provider's genuine `NotFound` as absence.

For an approved lab, implement this sequence:

1. Generate the owner and fixed reporting seed date once. Persist all table load
   IDs before creation; derive IDs from owner plus table, not each attempt's time.
2. Create the absent dataset/tables with ownership metadata, explicit location and
   reviewed schemas. Apply required partition filters to appropriate fact tables.
3. For each table, fetch its recorded job by project, location and ID. Reuse an
   existing job. If absent, submit the same ID with `WRITE_EMPTY` and `CREATE_NEVER`.
4. If submission conflicts, fetch that same job. If submission times out or loses
   its response, preserve uncertainty and reconcile that ID before another action.
5. Wait within the configured bound, inspect terminal errors, then verify row
   counts and deterministic fixture answers. Mark the dataset ready only on pass.

`WRITE_EMPTY` prevents overwriting an existing populated fixture; `CREATE_NEVER`
prevents an accepted late load from recreating a table after deletion. Neither
replaces job reconciliation. Where available, verify the recovered job's type,
destination and configuration too; that stronger check is a production extension
to the recorded example's deterministic IDs and protected state.

Repeat setup must reuse completed loads and the original seed date. If data or
schema validation fails, stop and diagnose; use separately approved cleanup/new
lab creation to refresh fixtures. Never hide a mismatch with append or truncate.
Before deleting a partial lab, reconcile every recorded load and wait for accepted
work to settle. A still-pending or inaccessible job keeps deletion blocked.

## 6. Verify identity readiness before SQL or model calls

For optional impersonation, verify the owned account and expected unconditional
Token Creator binding for the recorded source operator, then runtime project
grants. Check dataset access separately. Construct the application's actual
credential path, with the same source ADC and quota setting used at runtime.
The tested path used 900-second impersonated credentials held only in memory and
explicitly shared between BigQuery and the Gemini client; it downloaded no keys.

Mint only a token to test readiness. The tested retry classifier required a
credential refresh error containing structured provider data with all of:

- HTTP code `403` and status `PERMISSION_DENIED`;
- `google.rpc.ErrorInfo`, reason `IAM_PERMISSION_DENIED`, domain `iam.googleapis.com`;
- permission `iam.serviceAccounts.getAccessToken` when included in metadata.

Use at most three readiness attempts, waits of 5 then 10 seconds, and a bounded
transport call (30 seconds in the tested implementation). These are historical
settings to adapt inside the target's total budget. Service-disabled errors,
429/quota failures, unknown errors and ordinary table permissions are not this
retry class. Return a sanitised reason without raw tokens or provider payloads.

If readiness still fails, verify source ADC identity, quota consumer and the exact
binding. A newly written correct grant may require more propagation time; perform
another identity-only check only within the authorised budget. Replaying an SQL
query or model request is not a readiness probe. Restore temporary environment
overrides and clear temporary credential caches after a diagnostic check.

After token readiness, run separately budgeted acceptance checks: establish the
effective database principal (`SELECT SESSION_USER()` is a BigQuery example),
verify known fixture answers, then exercise the model workflow. Token minting
alone does not prove dataset access or model availability. Export the selected
runtime identity before starting each process; retain bootstrap credentials for
provisioning and cleanup.

## 7. Diagnose interruption by stage

| Observation | Next action and stopping condition |
| --- | --- |
| Plan unexpectedly loads credentials | Move client/credential construction behind execution entry points; retest with unavailable credentials |
| API inventory or resource lookup is forbidden | Resolve the read permission; retain unknown state and perform no inferred activation/create/delete |
| Fixture submission returned no reliable result | Fetch the saved job ID/location; preserve state while the outcome remains uncertain |
| Resource is present with wrong owner/location or replaced account ID | Stop; select a new isolated target or restore matching state, preserving the existing resource |
| Journal is missing | Recover its backup and verify provider ownership; resource names alone cannot reconstruct grant provenance |
| IAM write succeeded but token refresh gets the recognised denial | Apply the bounded readiness procedure, then stop for diagnosis/propagation if still denied |
| Account delete returned successfully but listing remains populated | Poll exact owned metadata; preserve deletion intent and avoid another delete submission |
| Dataset cleanup reports runtime still active | Finish/reconcile runtime cleanup first, including its grant checks |
| Query cost/partition guard refuses a query | Correct scope or required filters; increasing limits is a separate decision, not lifecycle recovery |

Keep a lifecycle process deadline separate from SQL submission/result timeouts.
The recorded campaigns supervised lifecycle processes for 600 seconds while SQL
calls had separate 30-second limits. SDK metadata/upload defaults were not claimed
to obey the SQL timeout. A process stop does not cancel accepted cloud work.
Stop new submissions at the campaign cutoff and retain/reconcile accepted IDs.
Count model sends, query attempts, dry runs and loads separately; request counts
and usage estimates are not a hard total-spend cap.

## 8. Delete in dependency order and reconcile uncertainty

After the scoped cleanup approval, quiesce new application work. If disposable
local ADK sessions are included, delete only their recorded IDs while the local
API is available, then stop its processes. Remove runtime impersonation overrides
from cleanup processes and use the recorded bootstrap operator.

1. Validate journal and current ownership. Mark runtime `deleting` before writes.
2. Remove only owned `pending`/`added` dataset, project and Token Creator grants,
   rereading policies and preserving unrelated members, conditions and grants.
3. Persist `account_delete_started` before requesting account deletion. After a
   submitted or uncertain request, reconcile metadata rather than resubmitting.
4. Check absence at most three times with 5/10-second waits in the tested pattern.
   Revalidate owner and immutable ID on every visible result. Permission failure
   or a replaced identity stops immediately; exhausting reads retains `deleting`.
5. Confirm grant removal independently of account absence, then mark runtime
   `deleted`. If deletion was never accepted, establish that fact before an
   explicitly authorised retry; do not erase the attempt marker to force one.
6. Only now reconcile all fixture jobs, mark dataset `deleting`, and delete the
   allowlisted owned tables. Delete the empty dataset with `delete_contents=False`.
   An unexpected/new table must make cleanup fail safely rather than recurse.
7. Reread dataset absence before recording `deleted`. Repeat completed cleanup;
   it should reconcile recorded state without duplicate loads, grants or accounts.

If the dataset is already absent, still finish recorded runtime/grant cleanup.
If a resource reappears after confirmed deletion, stop for independent inspection.
Neither case is a reason to discard unresolved recovery information.

## 9. Establish closure and state its limits

Use an independent read-only pass against the exact journal inventory: account
GET/list absence, dataset GET/list absence, each table GET absence, owned grants
absent and pre-existing bindings preserved. Reconcile accepted query/load IDs to
terminal outcomes. Record project, location, check time, provider result and any
unresolved inventory; a permission or transport error is not a passed absence check.

For authorised local cleanup, verify session GET/list results and session/event
counts where available, then verify owned processes and listeners are gone.
Dataset deletion does not remove local ADK history. Preserve private recovery and
sanitised evidence; retain APIs, operator ADC, pre-existing IAM and provider job/
audit history unless their separate removal was explicitly in scope.

Visible BigQuery deletion can leave time-travel/fail-safe retention. Report exact
absence separately from physical erasure, retained storage and billing invoices.
For an explicitly requested wider project audit, authoritative service inventories
can resolve stale asset-index entries; `SERVICE_DISABLED` and inaccessible
anonymous datasets leave coverage gaps. Check the actual locations in scope.

Optional unrelated services remain separate: zero RAG corpora does not by itself
establish an unprovisioned regional backend. A default backend configuration also
does not prove active capacity or charges. Regional RAG unprovisioning needs its
own ownership/exclusivity checks, exact regional approval, operation record and
post-operation config/corpora/pending-operation checks. Routine SQL cleanup neither
requires nor authorises that branch, compute deletion or shared bucket changes.

## 10. Recorded evidence and implementation acceptance

The following labels describe September 2026 evidence, not a new live run or a
guarantee for another environment. See [compatibility](compatibility.md) for the
tested versions and provenance.

| Evidence class | Established behaviour and limit |
| --- | --- |
| **LIVE VERIFIED — 13 September initial campaign** | Local setup was interrupted after one fixture load was accepted; that job was later observed DONE and reused during resume. Repeated setup accepted five unique loads. This did not test a job still pending at later inspection. |
| **LIVE VERIFIED — 13 September follow-up** | Runtime readiness recognised the structured IAM denial, waited five seconds and succeeded on its second attempt before querying. Effective runtime identity, fixture answers and repeated provisioning/cleanup passed. |
| **LIVE VERIFIED — both campaigns; 15 September recheck** | Exact SQL-owned accounts/datasets/tables were absent, owned grants removed and unrelated grants preserved. Accepted jobs reached terminal state; local sessions/processes were removed. The later check reconfirmed exact resource absence. |
| **OFFLINE VERIFIED** | Missing-credential planning, exact API activation allowlists, foreign-resource refusal, uncertain creation, pending-grant recovery, still-pending load refusal and the corrected stale-delete metadata polling branch. |
| **NOT RUN live** | Fresh-project API activation, corrected stale-delete polling under another stale-read event, live query/browser timeout recovery and deployed application hosting. |
| **PRODUCTION PRINCIPLE** | Distributed journal concurrency, complete lifecycle deadlines, recovered-job configuration validation and target-specific caller isolation need their own implementation and tests. |

For a new implementation, exercise the public lifecycle entry points with provider
doubles: no-provider planning, repeated setup, response loss after accepted work,
foreign/replaced resources, missing permissions, selective grant cleanup and
uncertain deletion. Assert mutation counts and preserved resources, not just error
messages. Use a separately approved live campaign for claims that require a real
provider; retain failed stages and do not resample simply to obtain a passing label.
