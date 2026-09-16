# Cloud prerequisites and a bounded external campaign

Read only when live acceptance is requested. Planning or ordinary offline
orchestration work does not need a cloud project. No previous companion approval
transfers to a new task.

## Prepare a reviewable envelope

Name exact account/project, runtime identity, region/model/backend, APIs, resources,
fixtures, commands, request/query limits, retry policy, window and cleanup deadline.
Obtain explicit approval before paid calls or mutation. Estimate current costs
from official pricing for the proposed configuration; label unknowns. Counts and
time limits are not hard spending caps. Scope changes need a new decision.

Use one isolated owned lab with synthetic data. Keep an inventory before accepted
operations and reconcile pending outcomes before resubmission. Bound retries to
identified transient, idempotent operations; never rerun a whole suite just to
obtain PASS. SDK retries and tool continuations count as actual attempts.

## Preflight without mutation

1. Determine the backend from this project's actual SDK/configuration. Vertex/Agent
   Platform ADC and Gemini Developer API keys are alternative modes. Root `.env`
   settings may not reach a nested application; shell variables can also override
   file settings. Report presence/mode without credential values.
2. For ADC, distinguish active CLI identity, ADC identity and quota project.
   Inspect credentials without printing a token. Prefer short-lived credentials;
   do not download service-account private keys to make the demo work.
3. Check billing, model access, enabled APIs and effective runtime permissions.
   Vertex prediction uses `aiplatform.googleapis.com`; billing inspection may need
   `cloudbilling.googleapis.com`, which does not itself link billing. An explicit
   `--project` and `--billing-project` on relevant `gcloud` checks avoids inspecting
   the wrong API consumer. Use `--quiet` to prevent implicit activation prompts.
4. A successful empty API listing can establish “disabled”; a permission or
   transport failure cannot. Read-only operator success is not proof of runtime
   permission. Finding an enabled API does not test fresh-project activation.
5. Missing billing, API/model access or credentials stops dependent live requests.
   Continue offline checks. Present human login/terms steps and approved activation
   separately; do not grant Owner/Editor, link billing or raise quotas as a repair.

Use the SDK version's accepted environment names. The historical checked setup
used `GOOGLE_GENAI_USE_ENTERPRISE=true`, project and `global` location; do not assume
that name or region is correct for every release/model. Likewise, a valid key
does not establish model availability, billing eligibility or authorisation.

### Diagnose the actual launch configuration

Record a sanitised launch manifest: working directory, interpreter/SDK versions,
configuration file paths, relevant key presence, selected backend, target project,
quota project, CLI identity, runtime credential type/principal, region and model.
Record provenance (shell, nested file, explicit client option or default), not
secret values. A successful IDE project selection or replacement root key does
not repair a nested process's configuration. Resolve disagreement before sending.

For the checked Vertex path, effective runtime permissions include
`aiplatform.endpoints.predict` and quota-project `serviceusage.services.use`.
Use the credentials the application will actually use for permission checks;
operator permissions or successful token refresh alone prove neither. Determine
the principal through supported credential metadata or scoped identity inspection,
without dumping the ADC file, token, refresh token or HTTP authorisation headers.
Leave unresolved identity/model access as a blocker rather than guessing.

Portable CLI inspections adapted from the historical reader path follow. Set
`TARGET_PROJECT` to the selected project first; inspect each exit status before
proceeding. These commands inspect CLI context and prerequisites, not ADC identity:

```bash
: "${TARGET_PROJECT:?Set the intended Google Cloud project ID}"
gcloud auth list --quiet --filter=status:ACTIVE --format='value(account)'
gcloud config get-value project --quiet
gcloud projects describe "$TARGET_PROJECT" --project "$TARGET_PROJECT" \
  --billing-project "$TARGET_PROJECT" --quiet --format='value(projectId)'
gcloud services list --enabled --project "$TARGET_PROJECT" \
  --billing-project "$TARGET_PROJECT" --quiet \
  --filter='config.name=aiplatform.googleapis.com OR config.name=cloudbilling.googleapis.com' \
  --format='value(config.name)'
```

Only when the Cloud Billing inspection API is available, read billing status:

```bash
gcloud billing projects describe "$TARGET_PROJECT" --project "$TARGET_PROJECT" \
  --billing-project "$TARGET_PROJECT" --quiet --format='yaml(projectId,billingEnabled)'
```

CLI authentication and ADC are separate configurations; see Google's
[authentication guidance](https://docs.cloud.google.com/sdk/docs/authenticate).
The [service-list command](https://docs.cloud.google.com/sdk/gcloud/reference/services/list)
supports explicit project/consumer selection. These references were checked on
16 September 2026; live commands were not repeated during skill maintenance.

| Symptom | Evidence to inspect and next step |
| --- | --- |
| Project lookup denied | Check intended account, impersonation/configuration and project access. A UI selection does not establish access. Keep resource state unknown until a permitted read succeeds. |
| `SERVICE_DISABLED` names an unexpected consumer | Check the error's consumer against both target and quota project, then retry only the corrected read within its allowance. Do not activate an API in an unrelated CLI consumer project. |
| Billing API unavailable versus `billingEnabled: false` | These are different results. Request only the needed approved inspection capability; an explicit false requires the billing owner to resolve linkage separately before model use. |
| Key exists but requests use ADC, or a root key was replaced | Inspect actual client/backend selection and nested configuration. Test the selected mode separately; a Vertex pass does not validate Developer API key mode. |
| OAuth identity request fails | Inspect that identity endpoint's auth/header contract. Unrelated quota headers or broad IAM grants are not an identity repair. |
| Certificate validation fails in one interpreter | Check that environment's declared certificate trust and proxy configuration. Preserve TLS verification. |
| 429 or 503 | Classify transient capacity/rate failure versus exhausted quota, billing or spending constraints. Backoff cannot repair an exhausted allocation. Use bounded safe retries only when approved. |

The last row is a production diagnostic rule, not a claim that this chapter
exercised live quota exhaustion. Consult the selected service's error guidance;
[Gemini Developer API troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting)
is not a substitute for Vertex-specific access checks. For a strict request
allowance, implement [model-call-controls.md](model-call-controls.md).

On a project change, preserve the old ownership/recovery record and start fresh
state tied to the new approved project. Do not replay old resource IDs. Verify
the new identity, billing, APIs and model access before recreating anything;
already configured software and trial credit do not establish permission or
free execution. Reusing the same project/state must preserve earlier counters
and deadlines, not silently reset them.

## Functional acceptance and cleanup

Assert meaningful outputs with the intended runtime identity, including actual
tool execution where advertised. Run local negative cases even when the approved
live campaign covers only happy paths. For a frontend, use its real browser path;
record first meaningful and final correct output times, cold/warm samples, failures
and settings. A backend pass does not establish browser usability.

Agree workflow-specific targets before paid testing. A possible starting point
is 5 seconds to warm meaningful text, 20 seconds to a simple final answer and
30 seconds to a tool/RAG answer, with one cold and five warm samples if approved.
These are proposals, not service guarantees. A timing interval spanning a target
is inconclusive, even if the owner accepts that experience. Do not move a threshold
after measurement or claim p95 from a small smoke sample.
Use [local-runbook.md](local-runbook.md) for concrete HTTP, browser, timing and
local cleanup procedures; distinguish observed UI intervals from backend spans.

With confirmation, delete only exact task-owned resources/sessions and added
grants. Repeat the supported deletion path and independently inspect absence and
pending operations; preserve shared resources and other users' populated data.
Stop owned local servers and dispose of isolated temporary credentials/copies.
Session deletion does not establish privacy-worker or artifact erasure.

Enabled shared APIs, provider logs and billable retention may remain deliberately.
Deleting a top-level RAG/index resource may leave a chargeable regional database
or serving backend. Verify its separate lifecycle; broad regional deletion needs
explicit ownership/exclusivity checks and separate confirmation. Do not disable
shared APIs to manufacture activation evidence. Report remaining state and cost
caveats rather than promising zero charges or physical backup erasure.

For a broader cleanup review, use asset inventory for discovery and direct
service/operation reads for current state. A stale discovered child is not proof
of a running parent; a disabled API or denied listing is not an empty inventory.
Report checked project/regions, exact owned IDs, pending operations, retained
state and uninspectable services separately. Managed resources in a provider's
tenant project may not appear in the customer's normal database inventory.
Request further inspection or deletion only for the ownership scope in question.
Cloud Storage's [soft-delete documentation](https://docs.cloud.google.com/storage/docs/soft-delete)
explains why logically deleted objects can remain retained and billable. The
historical broader project recheck did not establish blanket zero residual cost.
