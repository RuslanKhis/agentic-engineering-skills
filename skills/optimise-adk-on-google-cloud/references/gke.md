# GKE workload optimisation

Read for an ADK service's startup, capacity, rollout, resource or identity issue.
Produce a targeted change or review with a measurable acceptance boundary.
For sessions, access, telemetry or streaming use [gke-serving.md](gke-serving.md).
For any cloud mutation, capacity retry or cleanup also read
[gke-lifecycle.md](gke-lifecycle.md).
For source packaging, provider response or recovery failures, use
[deployment troubleshooting](gke-deployment-troubleshooting.md). When changing
server/session startup, use [application integration](gke-application-integration.md).
For actual-boundary tests, use [GKE verification](gke-verification.md).

## Find the running configuration

1. Trace the delivery command through Helm/Kustomize, a manifest generator or
   the selected YAML to the actual Deployment. Record its namespace, immutable
   selector, Pod labels, service account, ports and Service exposure. Inspect
   build staging, Docker entrypoint and agent exports as well as source files.
2. Render the selected configuration locally. Compare replicas, quota, rollout,
   probes, resources, session URI and optional controllers as one system. Keep
   unknown values explicit. Editing an unused example is not implementation.
3. When cluster inspection is available, bind the exact project/location/cluster
   and namespace to an authorised context. Inspect admitted Pods, injected
   containers, image IDs and current-generation conditions. File presence and
   a successful dry-run do not establish these runtime facts.

The retained private lab generates its manifests: two fixed Pods; quota for two
Pods, two requested CPUs and 4 GiB requested memory; `maxSurge: 0` and
`maxUnavailable: 1`; 1 CPU/2 GiB memory/1 GiB ephemeral storage per Pod;
ClusterIP on port 80 targeting 8080; shared managed sessions. No HPA, PDB or
topology spread is applied. Separate reference YAML includes different rollout
settings and public exposure. These are evidence distinctions, not templates to
replace a target's architecture. Never apply an entire example directory over
an existing workload to obtain one optimisation.

## Locate the delay

| Observation | Inspect next | Candidate only after evidence |
| --- | --- | --- |
| Pending before scheduling | Events, placement constraints, resource requests, quota and node provisioning operations | Capacity/placement plan or resource correction |
| Scheduled but waiting for image | Image size/layers, pull errors, node identity, registry/network access | Build slimming, cache or eligible image streaming |
| Process starts but stays unready | Import/initialisation timing, probe failures, credentials and session startup | Wired lifecycle and a realistic startup allowance |
| Warm Ready Pods queue requests | Active runs, queue age, concurrency slots, CPU/memory, upstream quotas | Admission/scaling or application work reduction |
| First call slow, later calls normal | Same-client credentials, DNS, connections and pool acquisition | Per-process client reuse or bounded initialisation |

Separate external completion, platform transitions and monotonic application
spans. Pod first-ready includes scheduling and image work; node startup and HPA
recommendation timing describe different intervals. HPA recommendation latency
is not time until serving capacity exists. Confirm dashboard/metric prerequisites
before relying on [GKE startup metrics](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/monitor-startup-latency-metrics).
Keep prompts, exception text and session identities out of operational output.

Record baseline/candidate source revision and image digest, resolved packages,
model/backend, cluster mode/version/channel/location, service locations,
Pod/node/cache/session state, workload, concurrency, sample count and failures.
Choose one mechanism. Preserve complete authorised answers and recovery before
claiming improvement; a functional smoke result supplies no latency distribution.

## Probes and initialisation

- Startup permits necessary local initialisation before readiness/liveness begin.
  Derive its allowance from observed startup, including a slow eligible node.
- Readiness controls traffic eligibility. Expose completion of essential local
  preparation; a shallow `/health` response proves HTTP responsiveness only.
- Liveness should detect conditions a restart can repair. A shared remote outage
  should not restart every replica. Keep probes free of model calls and jobs.
- Set endpoint, port and timeout deliberately. The Kubernetes timeout default is
  one second; a busy event loop can miss it. Raising thresholds avoids premature
  restarts but does not shorten initialisation.

Verify probe changes against the real serving endpoint and loaded conditions;
test slow startup separately from deadlock. See
[probe semantics](https://kubernetes.io/docs/concepts/workloads/pods/probes/).
Client construction belongs in each worker's lifecycle, using the same clients
that requests use. A discarded credential refresh or a separate warm-up client
does not warm ADK's client. Close transports on shutdown. Bound each network
operation and the complete initialisation, including backoff; retry transient
failures, surface permanent permission/configuration failures. Cancelling an
await around a thread does not stop its blocking network operation.

## Capacity and controllers must agree

Inspect requests, limits and QoS after admission, including sidecars. Autopilot
can default or adjust resources. Omitted CPU limits allow a different burst
policy only on supporting configurations; available bursts are opportunistic.
Container-level Guaranteed QoS needs positive equal CPU and memory requests and
limits for every container. Equal memory alone does not establish it. Keep
Autopilot ephemeral-storage requests and limits equal. Verify the target's
[resource rules](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/autopilot-resource-requests).

Use CPU saturation/throttling, memory peaks/OOM, restart and queue observations
under startup and representative concurrency. Extra CPU cannot remove remote
waiting. A CPU-utilisation HPA divides usage by requests, so changing a request
changes the meaning of its target.

Calculate a capacity envelope before proposing controller edits:

- Warm floor and HPA maximum, multiplied by per-Pod requests including sidecars.
- Rollout surge and continuing resource use by terminating Pods.
- Namespace quota, eligible node/zone capacity and remaining-replica load.
- Database connections and downstream admission/quotas at that capacity.

An HPA capped at ten inside a two-Pod quota cannot serve ten Pods. A zero-unavailable,
one-surge rollout needs room for a replacement. Preserve the existing cap if that
is the user's constraint; choose a compatible rollout or report the unresolved
availability trade-off. Do not raise quota or relax exposure as a silent repair.
Once HPA owns replicas, ensure ordinary delivery stops resetting `.spec.replicas`.
Terminating Pods can consume resources beyond replicas plus surge; see
[Deployment behaviour](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

A PDB governs voluntary Eviction API disruptions, not normal Deployment rolling
updates or node failure. Choose its selector and allowance against the intended
replica range. Soft topology spread is a preference; two Ready Pods may still
share a node. Strict separation can make replacement unschedulable. Verify actual
placement and a controlled disruption before claiming node/zone resilience.
See [disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
and [topology spread](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).

For remote-I/O-heavy agents, compare CPU against active runs, occupied slots and
queue depth/age. A useful pressure metric rises with demand; free slots need
transformation. Establish the metric-to-HPA adapter/API, aggregation, missing-data
behaviour and permissions. Publishing Prometheus metrics alone does not wire an
HPA. Test recommendation, desired replicas, scheduling and Ready capacity as
separate outcomes. Scaling cannot remove a shared provider quota.

Use VPA recommendation-only mode first when sizing is uncertain. Coordinating
VPA resource changes with CPU/memory-utilisation HPA requires an explicit design;
both controllers can change the same denominator. Load-test scale-down and
restart behaviour, not just creation of the HPA/VPA object.

## Build and identity

Keep stable dependency layers before source, omit runtime-unused dependencies,
and run as a supported non-root identity. Verify each new module is in both the
staging allowlist and Docker copy inputs. Record tested resolution, base/build
images and output digest. A deployed digest identifies bytes; ranged dependencies
and tagged build inputs do not make a future rebuild reproducible. Preserve the
target package manager and lock strategy; no silent pin changes.

Distinguish build identity, node image-pull identity and the exact namespace/KSA
workload principal. Workload Identity Federation authenticates the Pod to Google
services; it does not grant node image access or authenticate end users. Choose
direct federated access versus service-account impersonation deliberately and
grant only the required resource permissions. Follow the target's
[Workload Identity setup](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/workload-identity).

Only add a metadata init wait if traces justify it. Bound connect, transfer,
retry and total execution separately; discard token responses. An init container
proves token-path availability, not application-client readiness or API access.
Check actual dataplane/mesh metadata routing and DNS before changing egress rules
or metadata host settings. Also account for session/model/tool destinations.

## Advanced proposals stay conditional

| Identified need | Additional evaluation |
| --- | --- |
| Image access dominates | Eligible image streaming/preloading; registry and node permissions, uncached start, full first-use time, storage cleanup |
| Infrastructure wait dominates | Current fast-starting-node/capacity-buffer support; available capacity is not a guarantee; additional capacity costs |
| Long stable initialisation | Current snapshot support; sensitive captured state; recreate clients, pools, credentials and unique IDs before readiness after restore |
| Non-CPU pressure | Supported adapter or direct metric feature, release/channel restrictions, stale/missing measurements and bounded admission |
| Untrusted code execution | Separate sandbox isolation, identity/egress, claim limits, trust boundaries, warm-pool cost and storage cleanup |

Check current official feature documentation and cluster support before proposing
these; do not change release channels or install controllers speculatively. None
was established by the historical private lab. Predefined trusted routing tools
do not imply a need for a code sandbox.

## Finish the selected experiment

Local acceptance: rendered effective configuration, compatible selectors/ports,
capacity arithmetic, pinned dependencies, shipped code and meaningful tests.
With separately approved live scope: inspect admission and bounded rollout,
exercise complete outputs and relevant failure/recovery, retain all observations,
then verify owned cleanup. Report pending capacity as pending/blocked, optional
production design as untested, and the exact boundary any successful test proves.
