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
