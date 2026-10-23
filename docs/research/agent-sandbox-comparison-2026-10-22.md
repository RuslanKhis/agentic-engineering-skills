# kubernetes-sigs/agent-sandbox and GKE Agent Sandbox compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
at commit `f62190c` (2026-10-21), latest tag v1.0.7, cloned on 22 October
2026 and read, never run (Apache-2.0, no NOTICE), together with the
`ai-ml/adk-vertex` sample of
[GoogleCloudPlatform/kubernetes-engine-samples](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples)
at commit `b632e55` (Apache-2.0, sparse clone), and two Google pages read the
same day: the GKE Agent Sandbox install guide
(https://docs.cloud.google.com/kubernetes-engine/docs/how-to/how-install-agent-sandbox,
updated 2026-10-14) and the Google Cloud blog announcing general
availability (2026-05-21). Files read: the repository `README.md`
(`Sandbox`, `SandboxTemplate`, `SandboxClaim`, `SandboxWarmPool`; gVisor or
Kata as the isolation runtime; install and uninstall), the `examples/`
listing and the READMEs of `sandbox-ksa`, `composing-sandbox-nw-policies`,
`containarium-execution-scoped-token` and `code-interpreter-agent-on-adk`;
the sample's three-line README and its Terraform (`main.tf`, `network.tf`,
`workload_identity.tf`, `artifact_registry.tf`, `variables.tf`) and
`app/requirements.txt`.

**Conclusion.** The project is what `GkeCodeExecutor(executor_type="sandbox")`
imports, so the security skill now names it with the version floor, the
flag, the admission policy and the examples a design can cite as checks;
the deploy skill gains Google's own Terraform layout for the GKE identity
table; the optimise skill gains the warm pool as provisioned capacity. The
ADK example in the repository is stale (ADK 1.19.0) and is cited for cluster
setup only.

## Method

Facts verified on Google's pages took precedence over the repository's
README and the blog; each is cited with its date. One scenario case for the
sandbox-selection journey is shared with the ADK source review
(`security-code-execution-environment-selection`); a dedicated fresh-agent
trial on the GKE deployment journey is in the
[testing record](../testing/agent-sandbox-alignment-2026-10-22.md).

## Drift corrected

- The memo's GA date ("20 May 2026") is the blog's publication date of
  21 May 2026; the figures (300 sandboxes per second per cluster, 90 percent
  of allocations within 200 milliseconds) are as the blog states them.
- The GKE install page does not label the feature GA or Preview; the blog
  does. The skill cites both.

## Imported, by specialist

- **adk-agent-security.** The CRDs and runtimes, the GKE version floor and
  flag, the Validating Admission Policy's required and prohibited settings,
  the GA announcement and its figures, the three examples as acceptance
  checks (no-IAM service account, default-deny network policy composed with
  KRO, per-execution token), and the stale ADK example.
- **deploy-adk-on-google-cloud.** The sample's Terraform layout for the
  identity table: private network and cluster through Connect Gateway, an
  Artifact Registry reader binding, a workload-identity module with one
  custom role holding only `aiplatform.endpoints.predict`; its stale app pin.
- **optimise-adk-on-google-cloud.** Warm pools as provisioned capacity that
  charges while idle under the designer's GKE ledger row.

## Routed, not copied

Nothing new: the GKE product skills in google/skills remain the operating
route; the executor table names the controller.

## Vendored assets

None.

## Left out, with reasons

- The Go and Python SDKs, the sandbox router, Kata and Firecracker
  runtimes, the many non-GKE examples: no decision here depends on them.
- A separate ledger row for warm pools: the GKE row already covers scheduled
  Pods; the optimise reference says so.
- A spike creating a sandbox: needs a cluster.

## Limits

Read, not run. The admission policy and version floor come from one page on
one day; the controller's behaviour on a cluster was not exercised.
