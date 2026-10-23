# kubernetes-sigs/agent-sandbox and GKE Agent Sandbox alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/agent-sandbox-comparison-2026-10-22.md).
In the repository: the controller, version floor, flag, admission policy, GA
figures, examples and stale ADK example in the security skill's agency
reference; Google's Terraform identity layout in the deploy skill's GKE
reference; warm pools as provisioned capacity in the optimise skill. After
the trial (23 October): the paragraph restructured with the admission
policy as a table and the 2.12.0 executor's sandbox parameters and the
`google-adk[extensions]` extra; the deploy reference naming the file and
section it points to, the feature-floor rule, the provider facts (gVisor
`sandbox_config` on `google-beta`; no attribute for the enable flag on the
provider schema the trial read) and where warm pools bill; the engineer's
routing row splitting executor from cluster. **One scenario case** shared
with the ADK source review (`security-code-execution-environment-selection`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. No helper changed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no cloud
access, no ADK installed, on a synthetic project, without the expected
answers; interrupted once by a usage limit and resumed. One disclosure: a
probe `terraform init` the agent ran in its scratch area downloaded the
`hashicorp/google` provider from the registry, so the session's no-network
rule was breached once by that tool; nothing was applied or deployed.

### Deploy: moving a data helper to the GKE Agent Sandbox executor

The project: an ADK 2.12 agent with `GkeCodeExecutor` in Job mode on a
1.35 cluster managed in Terraform, a request for sandbox mode with
Workload Identity and a finance question about warm pools.

What the agent did: an SDK-free executor configuration selecting sandbox
mode with a rollback switch; Terraform raising the cluster to the feature
floor with a validation rule, a gVisor node pool, cost labels, a service
account with one role and the Workload Identity binding; manifests for the
namespace, the agent, a default-deny-except-DNS network policy, a
`SandboxTemplate` carrying every admission-policy field and an optional warm
pool with apply and delete scripts written together; a cost note explaining
that warm sandboxes bill as node VM and disk SKUs, with prices left as
placeholders; 24 offline tests run, SDK tests and `terraform validate`
reported as not run.

Ease rating: **3 of 5**. Routing to the deploy skill was immediate; the
three facts the task hinged on sat in two other skills and were found by
search.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The deploy reference pointed at "the security skill's executor table" without a file | File and section named |
| Where warm pools bill lived in the optimise and designer skills only | One sentence in the deploy reference |
| The Agent Sandbox prose was one 25-line paragraph | Restructured; admission policy as a table |
| The executor's sandbox parameters and the client's distribution were unstated | `executor_type`, `sandbox_template`, `sandbox_gateway_name`, the `SandboxClient` call and the `google-adk[extensions]` extra, from the 2.12.0 source |
| A hard feature floor against a stated cluster version had no rule | Raise it as a recorded decision |
| gVisor `sandbox_config` is `google-beta` only; the enable flag has no provider attribute | Stated, with the trial's provider version and a confirm note |
| The engineer's table routed all sandboxing to security | The row splits executor from cluster |
| The deploy skill's helper path convention differs from `$SKILL_DIR` | Left: cosmetic |

## What this does not establish

Nothing was applied to a cluster; the CRD field names and the sandbox
client's distribution were not confirmed; prices were not read.
