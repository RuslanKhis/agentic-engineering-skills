# Connect and host the managed backends

Read this when connecting an implementation to managed services, moving an
existing local application to Cloud Run, changing projects, or preparing a
reviewable deployment. Read [operations-validation.md](operations-validation.md)
for approval, ownership and cleanup rules. This is a portable sequence derived
from the tested lab, not a dependency on its scripts or a fixed cloud topology.

## Choose what is actually being deployed

| Topology | What must be established | What it does not establish |
| --- | --- | --- |
| In-memory services with a scripted model | Application contracts in one process | Restart survival, real retrieval, provider access |
| Local authenticated API with managed backends | Real service calls through the local serving boundary | Cloud Run identity, networking, CPU lifecycle or revision restart |
| Hosted API with managed backends and shared coordination | Serving identity, private connections, cross-process state and deployed acceptance | Load/HA, backup restoration or complete privacy compliance |
| Remote managed agent runtime behind an application gateway | Explicit end-user propagation and owned session mapping on both hops | The in-process Runner recipe cannot be copied unchanged |

The source lab demonstrated the second topology completely on an earlier
baseline and only part of the third on its latest baseline. Remote runtime,
browser UI and production high availability were not implemented by this
chapter. Select the requested topology before inventing resources.

## Build a configuration map before provisioning

Record these as distinct settings, with their provenance and validation owner.
Keep resource selectors out of model arguments and user-editable session state.

| Setting | Resolve and validate |
| --- | --- |
| Project ID and numeric project number | Obtain the number from a trusted project lookup; carry the verified mapping into both runtime and erasure worker |
| Model backend, model name and endpoint location | Match the configured inference API and currently supported model endpoint; a Gemini API key and workload ADC are different credential paths |
| Sessions and Memory Bank parents | Separate configured engine IDs/resources; never infer one from the other even if deliberately colocated |
| Agent, RAG, screening and warehouse locations | Validate each service separately; a global model endpoint does not make storage global |
| RAG release registry and manifest | Pin the approved generation and scoped corpus; keep staging/publication authority separate |
| BigQuery job project, location, source and serving datasets | Check location compatibility, effective view authorisation and runtime read permissions |
| Run/profile/memory/privacy coordination state | Use shared durable state when multiple replicas or workers participate; record TTLs and key namespaces |
| Secret versions and HMAC keyrings | Use exact managed-secret versions where reproducibility requires them; separate run and privacy keys and preserve verification keys for the retry horizon |
| Public endpoints and health path | Use the real application route and chosen platform's routing contract; a provider-generated 404 is not necessarily an application response |

Changing a root environment file is not evidence that a child service, mounted
secret version, worker or model API key changed. Inspect effective configuration
through an allowlisted metadata report; do not print keys or dump environments.
For a project change, create fresh lifecycle state and reconcile the old target
separately. Never rebind old resource identities by editing a journal.

## Prove prerequisites without changing them

1. Identify CLI operator, local ADC/quota project, deployed runtime, erasure
   worker, ingestion identity and authenticated end user. Cloud permission and
   end-user data scope are different checks. Ambient credential overrides can
   select a different identity from the interactive CLI account.
2. Use explicitly scoped reads for project access, billing status, required
   APIs, effective quotas, existing backend configuration and permissions.
   A 403 or transport failure is an unknown check, not an absent resource.
3. Derive the API list from selected features. The source used Vertex AI,
   BigQuery, Storage, Secret Manager, DLP, Model Armor, IAM/impersonation and
   Firebase Auth/API-key services; hosting added Run, Compute, Redis, Artifact
   Registry and build services. This is not an instruction to enable all of
   them for every app. API readiness alone proves neither quota nor IAM.
4. If using the lab's Firebase custom-token pattern, verify Auth configuration
   in the existing selected project before paid provisioning. Provider sign-in
   enablement and application tenant claims are separate choices; a custom
   tenant claim does not itself create an Identity Platform tenant. Do not
   replace a target's working identity provider with Firebase for this skill.
5. For each resource adapter, verify the serving identity's required calls,
   including metadata GETs used to validate retrieved records. An operator's
   successful retrieval or a role name alone is insufficient evidence.

For an authorised operator, these are example metadata-only checks; substitute
the selected account/project through the target's existing configuration:

```bash
gcloud auth list --filter=status:ACTIVE --format='value(account)'
gcloud projects describe "$PROJECT_ID" --format='value(projectId,projectNumber)'
gcloud services list --enabled --project "$PROJECT_ID" --format='value(config.name)'
```

They do not validate ADC identity, billing or complete service permissions. Do
not run login, change global CLI settings, enable APIs or export access tokens
as part of these read-only checks.

## Prepare the dependency-ordered deployment

Prepare the exact commands using the target's existing deployment system. The
following order is a design contract, not a shell script to execute blindly.

1. Complete local contract tests and freeze the intended source/dependencies.
2. Resolve API prerequisites; any required activation is its own reviewed
   mutation. Keep API preparation state distinct from application ownership.
3. Inspect regional RAG mode and ownership. Creating a first corpus can have
   a broader backend lifecycle; prepare a separately scoped foundation only
   if this design needs one. Inspect before accepting ongoing capacity costs.
4. Establish workload identities and narrow grants, versioned policy templates,
   session/memory parents, source/serving data and release storage. Configure
   memory fact lifetime at the instance level; see
   [memory-bank.md](memory-bank.md) for expiry and resource-name traps.
5. Stage/import/evaluate the immutable policy candidate, then promote it with
   the recorded generation precondition. Verify retrieval as the runtime
   identity before treating operator evaluation as serving readiness.
6. Add shared coordination, configuration secrets and hosting only for a
   hosted target. Keep the application, worker and operator identities distinct.
7. Generate runtime and worker configuration from verified outputs; do not
   make users hand-copy project numbers or operation identities into files.
8. Verify created resources, refresh only explicitly owned synthetic fixtures
   when their freshness contract expires, and run the authorised acceptance
   phases. Setup can consume most of a short fixture freshness window.

## Cloud Run mechanics that affected this chapter

- **Two authentication gates:** when the app uses `Authorization` for an
  end-user token, use a separately audience-bound Cloud Run ID token in
  `X-Serverless-Authorization`. Keep service-invocation permission separate
  from application identity verification. Google's [service authentication
  guide](https://docs.cloud.google.com/run/docs/authenticating/service-to-service)
  documents the header behaviour; never reuse one token as both identities.
- **Shared state:** the tested hosted lab used private Redis with TLS, CA
  verification and authentication over Direct VPC egress. Preserve the target's
  equivalent secure store; a process-local dictionary cannot coordinate two
  services or an erasure job. Do not copy the local unauthenticated loopback
  Redis configuration into hosting.
- **Background work:** the lab's in-process memory reconciler required CPU
  outside HTTP requests. Its always-allocated CPU/minimum instances incurred
  idle charges. If the target should scale to zero, use an appropriate durable
  worker/queue or prove the chosen lifecycle; do not assume a coroutine keeps
  running after the request or instance ends.
- **Images:** build from an explicit source allowlist, exclude credentials and
  journals, target the deployment architecture, run as a non-root user and
  inspect the immutable digest actually deployed. A host virtualenv pass does
  not establish the image's dependency set or execution architecture.
- **Private evidence:** use a narrowly authorised probe/job when needed for
  private state; do not add a public administrative endpoint merely for tests.
  Retain one execution identity, explicit retry limits and its complete logs.
- **Restart proof:** verify the provider's replacement revision and a response
  from that revision before asserting post-restart recall. A new HTTP client,
  a new session or a successful deployment operation alone proves less.

The source used two services to exercise cross-process behaviour; that is a test
topology, not a minimum production resource count. Choose capacity, worker
retries and time limits for the target. Job queue/startup time sits outside a
task's execution timeout and needs its own overall deadline.

## Cutover and release evidence

For existing unprotected history, choose migration, expiry or a fresh logical
application namespace before admitting traffic. Stop legacy writes, stamp new
protected sessions and verify the new serving identity. A policy-version stamp
does not sanitise old events. Preserve the previous evaluated RAG candidate for
the rollback window; rollback is a new guarded promotion, not editing an active
corpus in place. These production cutover steps need their own rehearsal.

Acceptance must separately show authenticated model/tool execution, scoped
RAG/SQL, denied consent, completed generation, fresh-session recall, actual
restart recall, and erasure with a populated control owner. Use explicit
failed/not-run labels for dependent gates after a stop. Before teardown, export
all known worker/probe executions, including the final audit-export execution.
Use [failure-recovery.md](failure-recovery.md) for narrow diagnostics and
continuation rules instead of rebuilding the entire environment after each
failure. Source/evidence anchors are in [provenance.md](provenance.md).
