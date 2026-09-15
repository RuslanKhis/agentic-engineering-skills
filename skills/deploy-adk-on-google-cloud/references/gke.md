# GKE: existing cluster or an isolated lab

Read this when deploying, reviewing or adapting an ADK workload on GKE. Apply the [shared lifecycle and approval gates](../SKILL.md). Prepare the actual manifests, target coordinates, IAM changes and cleanup before requesting any missing approval; perform cloud mutations only within the user's explicitly approved scope.

**Evidence boundary.** The source-tested path created an exclusively owned GKE Autopilot lab, built a custom image and served the bundled ADK UI through an authenticated localhost tunnel. Real routing, explicit recall, direct connection recovery and rebuilt telemetry behaviour passed. Shared-cluster adaptation, generated `adk deploy gke` scaffolding, production ingress/auth and durable external state were not exercised by that acceptance.

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

Resolve and authorise source staging, account and repository permissions before submitting. Where the target uses a named build identity, set the CLI's verified account option rather than inheriting an unexpected default. Record submission intent before the call and the returned build ID immediately afterwards. Wait for terminal state and verify the actual account/source; then resolve the image:

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

List all blockers together and retain metadata without secret contents. One inventory can fan out over many Kubernetes resource kinds; refusal, audit lookup and repetition still consume time/actions. Reserve capacity for reconciliation and independent checks before spending the optional testing allowance. Preserve failed budget constraints rather than revising the historical pass criterion.

Remove only exact owned source object generations, using a generation precondition. Keep shared staging buckets, enabled APIs, provider identities, build/log history and applicable retention. Retain node grants while the cluster needs them; remove only recorded additions. Verify resource absence and eligible grant removal through repeat cleanup and independent reads. Report retained resources and visibility limits without claiming physical erasure or guaranteed zero charges.
