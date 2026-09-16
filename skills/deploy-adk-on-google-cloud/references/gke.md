# GKE: existing cluster or an isolated lab

Read this when deploying, reviewing or adapting an ADK workload on GKE. Apply the [shared lifecycle and approval gates](../SKILL.md). Prepare the actual manifests, target coordinates, IAM changes and cleanup before requesting any missing approval; perform cloud mutations only within the user's explicitly approved scope.

**Evidence boundary.** The source-tested path created an exclusively owned GKE Autopilot lab, built a custom image and served the bundled ADK UI through an authenticated localhost tunnel. Real routing, explicit recall, direct connection recovery and rebuilt telemetry behaviour passed. Shared-cluster adaptation, generated `adk deploy gke` scaffolding, production ingress/auth and durable external state were not exercised by that acceptance.

Use sections 1–5 for implementation and acceptance; section 6 adds the deeper recovery rules needed only for owned-cluster teardown. For a concrete failure, read [troubleshooting.md](troubleshooting.md); for external state, user authentication or a production release pipeline, read [production.md](production.md).

## 1. Select the ownership boundary

- **Existing cluster requested or already part of the product:** inspect its exact project/location, cluster identity, access policy, workload identity configuration and intended namespace. Produce a namespace/workload-level change. Treat the cluster, shared registry, controllers and existing grants as externally owned. The lab's cluster-deletion model must not be transferred to this branch.
- **Isolated teaching/test deployment:** use a fresh dedicated namespace and unused cluster/repository names, with a new ledger bound to project, location and source. Explicitly account for billable retained infrastructure and cleanup before creation. A cluster with a matching name or copied label does not establish ownership.
- **Production workload:** use the team's existing release and infrastructure process. Confirm topology, availability, identity, network and state requirements before adapting the lab manifests. Do not create a new cluster merely because the chapter did.

Done when each resource is marked owned, explicitly reused or outside scope, with corresponding deletion limits.

## 2. Inspect configuration and identity

Select resource/quota project explicitly and separate hosting/build location from model location. Resolve current model availability; the tested model used a global endpoint independently of the cluster's region.

Inspect the required APIs and effective permissions before deployment. The source lifecycle checked Container, Compute, Artifact Registry, Cloud Build, Vertex AI and IAM; inspect supporting Storage, Resource Manager and Logging operations in the target implementation too. Enabling missing APIs and changing IAM are separate mutations in the reviewed plan.

Map these roles even when one account holds more than one:

| Identity | Required responsibility |
| --- | --- |
| Operator / release runner | Submit changes and access the selected Kubernetes resources |
| Cloud Build account | Read staged source, write image/logs |
| Node account | Node operation and image pulls |
| Kubernetes service account | Runtime model and tool calls through workload identity |
| Caller | Reach the application through the chosen authenticated boundary |

Resolve the actual regional build identity and inspect the completed Build's account. A guessed default Compute account caused a real deployment defect. A node's registry reader permission does not grant the agent model access. Workload Identity Federation avoids placing a service-account key in the Pod; inspect the target cluster's supported configuration before choosing its principal binding. The tested direct KSA principal shape was:

```text
principal://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/PROJECT_ID.svc.id.goog/subject/ns/NAMESPACE/sa/KSA_NAME
```

Prepare the actual principal and narrowly scoped roles. Source-tested project-wide build grants were broad lab bootstrap permissions; least-privilege named build identities are production adaptations. Record only newly added grants and preserve existing/conditional grants.

The concrete lab mapping explains which responsibility each grant served. Use it to diagnose the permission boundary, then derive the target application's narrower scopes; it is not a blanket grant prescription.

| Tested identity | Tested roles and scope | Operational boundary |
| --- | --- | --- |
| Actual regional default Cloud Build account | Project `roles/storage.objectAdmin`, `roles/logging.logWriter`, `roles/artifactregistry.writer` | Source archive access, build logs and publishing the image |
| Explicit default Compute account used by GKE nodes | Project `roles/container.defaultNodeServiceAccount`; `roles/artifactregistry.reader` on the owned repository | Node operation and pulling the image |
| Direct namespace/KSA principal | Project `roles/aiplatform.user` | Runtime model invocation |

Build and node roles used the same Google service account in the recorded campaign; they remain distinct responsibilities. Changing the KSA's model permission does not repair source-upload access or node image pulls. Preserve the existing cluster's node identity and workload-identity mechanism when adapting a product deployment.

Check `gke-gcloud-auth-plugin` is installed before depending on `get-credentials` or kubectl authentication. Plugin installation is a local prerequisite, not an API-enablement operation. A successful gcloud sign-in alone does not establish that kubectl can authenticate.

Use a private kubeconfig for this operation. With all variables resolved, this command selects the known cluster without changing the user's normal kubectl context:

```bash
export KUBECONFIG="$PRIVATE_KUBECONFIG"
gcloud container clusters get-credentials "$CLUSTER_NAME" \
  --location="$DEPLOYMENT_REGION" --project="$PROJECT_ID" \
  --account="$OPERATOR_ACCOUNT" --billing-project="$PROJECT_ID"
```

Done when the actual caller, build, node and runtime identity paths and target kubeconfig are recorded.

## 3. Prepare the image and manifests

Stage an explicit allowlist of necessary build inputs in a temporary directory. The tested source needed six files: Dockerfile, application wrapper, root requirements and the agent package's initialiser, implementation and requirements. Adapt that list to the actual imports/assets; exclude `.env`, secrets, credentials, state, SQLite databases and audit output before upload. Docker ignore rules alone do not protect the earlier Cloud Build upload boundary.

Inspect the application entrypoint, discovered app name, listener, session backend and health endpoint. The tested wrapper exposed ADK's `/health`; readiness/liveness did not use an invented `/healthz`. Its SQLite file under `/tmp` survived a process restart with the same file, not Pod replacement or multiple replicas. Its non-root user needed a writable home to save telemetry consent; verify any repaired image after rebuilding.

Render concrete manifests locally: namespace, KSA, Deployment, Service, image reference, environment, resource requests/limits and probes. Inspect the target's actual port and startup behaviour. The tested workload used one replica, CPU/memory/ephemeral-storage bounds, `/health` readiness/liveness and ClusterIP. These are example settings, not production sizing or readiness guarantees.

### Connect the server, workload and Service

For a project using ADK's packaged FastAPI server, the essential wiring at the tested version was:

```python
import os
from pathlib import Path

from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(
    agents_dir=str(Path(__file__).resolve().parent),
    session_service_uri=os.environ.get(
        "SESSION_SERVICE_URI", "sqlite+aiosqlite:////tmp/adk_sessions.db"
    ),
    allow_origins=["https://example.invalid"],
    web=True,
)
```

This is an adaptation sketch, not a replacement for an existing server. The parent directory must contain the actual agent package with its exported root agent; discover the resulting app identifier through `/list-apps`. Preserve the application's CORS settings and authenticated access path. The intentionally nonmatching example origin does not provide authentication, and same-origin UI access does not need a permissive cross-origin policy. The image must include the selected session driver's dependencies and run its server on `0.0.0.0:8080`; `EXPOSE` alone does not start a listener. The recorded image used exec-form `uvicorn app:app --host 0.0.0.0 --port 8080` and a non-root user with a writable home.

The following YAML makes the tested relationships explicit. It uses generic names and a deliberate image placeholder, so it is a **rendering example**, not a directly deployable artefact. Resolve names, namespace ownership, model/backend configuration, image digest and the application's actual server contract first. For a shared cluster, use the namespace selected by the platform owner. Create a new namespace only in the approved ownership plan.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: agent-runtime
  namespace: agent-lab
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-api
  namespace: agent-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: agent-api
  template:
    metadata:
      labels:
        app.kubernetes.io/name: agent-api
    spec:
      serviceAccountName: agent-runtime
      containers:
        - name: agent
          image: REGISTRY_HOST/PROJECT/REPOSITORY/IMAGE@sha256:REPLACE_WITH_DIGEST
          ports:
            - name: http
              containerPort: 8080
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
              ephemeral-storage: 512Mi
            limits:
              cpu: "1"
              memory: 1Gi
              ephemeral-storage: 1Gi
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: agent-api
  namespace: agent-lab
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: agent-api
  ports:
    - name: http
      port: 80
      targetPort: http
```

Before applying the rendered result, check these relationships locally:

- The KSA name and namespace exactly match both `serviceAccountName` and the IAM workload principal. A direct KSA principal does not by itself require an IAM-service-account annotation; use the target cluster's selected identity mechanism consistently.
- Deployment selector, Pod labels and Service selector identify the same workload. The Service's port 80 resolves to the named container port 8080; the tunnel therefore forwards to Service port 80.
- The image contains the intended package and server, and the manifest uses the resolved digest. Add the application's explicit **non-secret** project/location/backend environment and ownership metadata to the rendered workload; the example omits values that must be derived from the target.
- Parse all YAML documents; inspect the final render for unresolved tokens, wrong namespace, unintended public exposure and lost existing settings. Server-side dry-run adds cluster contact and admission checks; local parsing does not prove the cluster will accept the result.
- Inspect effective Pod resources after admission. In the historical run, requests remained 500m/512Mi and Autopilot reduced the declared ephemeral-storage limit from 1Gi to 512Mi. Record the actual adjustment instead of declaring the authored manifest to be the live resource contract.

Use cheap process/server probes. A healthy `/health` response does not establish model credentials, tool reachability or session durability. Add startup-probe behaviour only when the measured startup contract warrants it, and validate it as a new adaptation.

Keep the unauthenticated development server behind Kubernetes-authorised access. ClusterIP restricts reachability but does not authenticate sessions or isolate tenants. In a shared cluster, consider which other workloads can reach it. Public ingress, TLS, workload network controls, user authorisation, durable state, autoscaling and startup probes are proposed production work unless already present and verified.

Done when source inventory, image build configuration and fully rendered workload diff are reviewable.

## 4. Deploy once and reconcile uncertain outcomes

The source-tested build command shape was:

```bash
gcloud builds submit "$SANITISED_SOURCE_DIR" \
  --project="$PROJECT_ID" --region="$DEPLOYMENT_REGION" \
  --account="$OPERATOR_ACCOUNT" --billing-project="$PROJECT_ID" \
  --tag="$UNIQUE_IMAGE_TAG" --async --format=json
```

Resolve and authorise source staging, account and repository permissions before submitting. `--account` in this command selects the **gcloud caller**, not the account that executes the build. A named build identity uses the separate build service-account option: verify `gcloud builds submit --help` for the installed CLI, including `--service-account`, and resolve its resource format and source/log permissions before use. The chapter deployed with the discovered regional default; the named-account adaptation was not its tested path. In either case, verify the returned Build's `serviceAccount` against the planned execution identity.

Record submission intent before the call and the returned build ID immediately afterwards. Wait for terminal state and verify the actual account/source; then resolve the image:

```bash
gcloud artifacts docker images describe "$UNIQUE_IMAGE_TAG" \
  --project="$PROJECT_ID" --account="$OPERATOR_ACCOUNT" \
  --billing-project="$PROJECT_ID" --format='value(image_summary.digest)'
```

Deploy the validated `repository/image@sha256:...` reference. Confirm Kubernetes applies the intended namespace/KSA/env/resources, then wait for rollout and inspect the running Pod's image ID and provider-adjusted resources. A rollout is infrastructure evidence; model/tool acceptance follows separately.

A lost build response must reconcile to exactly one regional build matching the recorded unique tag. Multiple candidates, active builds or missing provenance retain pending state and prevent another submission or teardown underneath a build. A missing resource during pending creation does not establish operation completion; a visible resource during pending deletion does not authorise replaying DELETE. The source lab's repeated completed setup verified the existing workload without rebuilding; updating an existing product follows its explicit release/rollback mechanism instead.

Done when terminal build, digest, workload identity and rollout evidence identify the deployed source.

## 5. Exercise the documented access path

An authenticated loopback tunnel command shape, after resolving the target, is:

```bash
kubectl port-forward --address=127.0.0.1 --namespace="$NAMESPACE" \
  "service/$SERVICE_NAME" "$LOCAL_PORT:$SERVICE_PORT"
```

Own and stop only the tunnel process this operation started. Wait for its own successful listener message before probing, so an unrelated local server cannot masquerade as the target. The source smoke used a temporary kubeconfig, unique synthetic user/session IDs, bounded HTTP requests, one model submission without automatic retry, session deletion and tunnel cleanup that reported failure.

Check `/list-apps`, create a session using the actual installed API contract and run a real tool/model turn. In ADK 2.8.0 session state was the direct JSON body; another `state` wrapper produced unwanted nested state. Require the expected successful structured tool result and grounded answer. Ask an explicit later recall question; sharing a session ID alone is not recall evidence.

Open the actual packaged browser UI through the documented tunnel. In the recorded follow-up, direct disconnection showed a fetch error and restored input; an optional recorder's HTTP 502 restored input without a visible error. Test instrumentation can change the failure, so distinguish both paths. Retry only a known unaccepted request; an accepted timeout needs reconciliation. A failed local bubble can remain after retry without implying duplicate accepted actions.

Done when live app, browser and error observations are attributed to the actual image/access path and retained limitations are explicit.

## 6. Clean up at the authorised ownership level

For an existing/shared cluster, remove only the operation's owned workloads and eligible added bindings; preserve the cluster, shared namespace content, images and controller resources outside the task. For an isolated owned lab, inventory namespace/resource identities and dependencies before deleting its namespace, cluster or exclusive repository. Default cleanup may retain the billable cluster, image storage and node grants.

Preserve a provider baseline for exclusively owned lab teardown. Late controller-created ConfigMaps, Secrets, Pods and leases can cause safe refusal. Verify exact reviewed UID, immutable creation time, authenticated create audit, original creator/binding identity and fresh current metadata before reconciling an exception. A system namespace, manager name or refreshed blanket baseline is insufficient. The tested inventory covered namespaced resources, not every possible cluster extension or concurrent administrator action.

### Reconcile exact late objects without widening ownership

Use the project's existing recovery implementation where it has these properties. Otherwise prepare the reconciliation algorithm and refusal tests before accepting a late object. This is conditional recovery for an exclusively owned cluster, not a reason to adopt controllers in a shared cluster.

1. Capture the complete blocker set as **metadata**: kind, namespace/name, UID, immutable creation timestamp and owner UIDs. Keep Secret/ConfigMap contents out of persisted snapshots and reports. Preserve the original namespace and controller baseline.
2. Obtain one successful authenticated create event for the exact resource, method and bounded creation-time interval. Refuse duplicate matches, unknown actors, missing dependencies and truncated audit responses. A principal string or managed-field manager name alone does not establish that the original trusted controller performed the create.
3. Validate the applicable provenance anchor from the table below. Preserve any missing audit-response UID as an explicit evidence limitation; accept a substitute proof only in a reviewed branch that defines it. Some branches require the response UID and have no fallback.
4. Re-read **every target and every proof dependency** immediately before recording results. A changed target, namespace, creator, Node or binding invalidates the batch. Save all receipts atomically after every check passes; leave no partially accepted batch.
5. Each receipt covers only its exact reviewed object UID and creation identity. A replacement or a new descendant of that late object needs its own evidence. Keep it outside the original controller trust roots. Re-run cleanup inventory against the unchanged original baseline plus the exact receipts.

| Observed object/actor branch | Evidence that anchored the source implementation |
| --- | --- |
| Provider ConfigMap/Secret created by a Kubernetes service account | Exact authenticated creator, its original service-account UID, target's original namespace UID and creation-time ordering. For cross-namespace controllers, verify both original namespace UIDs. |
| Lease created by a system User principal | Exact creator and an original RoleBinding UID with the expected User subject; a matching name alone is insufficient. |
| Node Lease | Earlier readiness record of Node name/UID/provider ID; matching current Node and Lease owner UID; exact `system:node:<name>` creator and expected project/location. The Node is not added as a new cleanup trust root. |
| VPA controller Lease | Exact `system:<lease-name>` creator plus successful provider bootstrap PATCH response matching binding UID, role reference and subjects, corroborated by an original baseline control identity. That bootstrap proves provenance; it is not evidence that a reader binding grants Lease-write permission. |
| Autoscaler balloon Pod | Exact autoscaler creator and exact create-audit response UID; the narrowed delayed-event case also requires response creation time. |

These are explanations of the tested proof branches, not a universal allowlist of future controller names. Unknown resource/principal combinations remain unresolved. Kubernetes/GKE versions and installed controllers can change the required evidence.

Two live repairs explain why the proof must be concrete. The original VPA branch recognised the admission-controller actor but refused the distinct recommender/updater actors; each was added only with the same original-identity and bootstrap checks. A balloon Pod's successful audit arrived 1.012507 seconds after its second-rounded creation timestamp. The repair widened **only that branch** from one to two seconds and required exact response UID and creation time for the additional second. Other windows stayed unchanged. Regression tests retained refusal for wrong actors, replaced bindings, absent subjects, wrong/missing response UID/time and out-of-window events.

The successful late-object reconciliation and cleanup were live observations. Atomic-batch replacement, wrong-actor and descendant-refusal cases were tested with provider doubles. In the follow-up, 15 of 17 successful receipts lacked target UIDs in the audit response; those receipts disclosed narrower evidence using exact resource/create time, authenticated creator, original control identities and a freshly rechecked reviewed UID. Do not summarise this as a returned provider UID for every object.

List all blockers together and retain metadata without secret contents. One inventory can fan out over many Kubernetes resource kinds; refusal, audit lookup and repetition still consume time/actions. Reserve capacity for reconciliation and independent checks before spending the optional testing allowance. Preserve failed budget constraints rather than revising the historical pass criterion.

Remove only exact owned source object generations, using a generation precondition. Keep shared staging buckets, enabled APIs, provider identities, build/log history and applicable retention. Retain node grants while the cluster needs them; remove only recorded additions. Preserve the repository required by a retained cluster too. The source lifecycle refuses repository deletion until the owned cluster is removed; adapting shared-registry image deletion needs its own ownership and reference analysis.

Verify resource absence and eligible grant removal through repeat cleanup and independent reads. Verify the saved cluster DELETE operation reached its terminal successful state as well as observing cluster absence. Autopilot backing VMs/disks were not fully visible through the recorded direct Compute interface, so the audit did not claim individual direct deletion evidence for them. Report that visibility limit and the retained resource inventory; cluster absence alone is not proof of physical erasure or guaranteed zero future charges.
