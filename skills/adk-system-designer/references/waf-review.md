# Well-Architected review: design checks per pillar

Read before a design at MVP, pilot or production profile is called ready, after
the failure review. Google's Well-Architected Framework (WAF) states each pillar
as principles and a validation checklist for a whole cloud workload; the checks
below are the ones that change an ADK application's design, rewritten against
this skill's vocabulary: each check names a contract, a decision or a goal, or
it does not belong here. A proof of concept skips this file; its floor already
covers spend and secrets. A tick means the design cites the ID that satisfies
the check; a cross means the gap is recorded in the design's open decisions.

Routing: when the profile is production or MVP and a concern's depth is "build
now", consult the installed Google skill for that pillar
(`google-cloud-waf-security`, `google-cloud-waf-reliability`,
`google-cloud-waf-cost-optimization`, `google-cloud-waf-operational-excellence`
or `google-cloud-waf-performance-optimization`, from google/skills) for the
product-level recommendations behind each check; if it is not installed,
`adk-engineer` explains how to get it. This file keeps only the design-level
checks so the designer does not depend on those skills.

Sources: the pillar pages under
[docs.cloud.google.com/architecture/framework](https://docs.cloud.google.com/architecture/framework),
fetched 21 October 2026 (reliability, cost optimization, operational
excellence and performance optimization overview pages, plus the principle
pages linked below), and the checklists in Google's `google-cloud-waf-*`
skills (google/skills, Apache-2.0, read 21 October 2026).

## Reliability

Principles: [define reliability from user experience](https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals),
[set targets](https://docs.cloud.google.com/architecture/framework/reliability/set-targets),
[build highly available systems](https://docs.cloud.google.com/architecture/framework/reliability/build-highly-available-systems),
[horizontal scalability](https://docs.cloud.google.com/architecture/framework/reliability/horizontal-scalability),
[observability](https://docs.cloud.google.com/architecture/framework/reliability/observability),
[graceful degradation](https://docs.cloud.google.com/architecture/framework/reliability/graceful-degradation),
[test recovery from failures](https://docs.cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-failures),
[test recovery from data loss](https://docs.cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-data-loss),
[conduct postmortems](https://docs.cloud.google.com/architecture/framework/reliability/conduct-postmortems).

| Check | Satisfied by |
| --- | --- |
| Each SLI is a good/total ratio over what the user experiences (completed tasks, time to first useful output), with a target below 100 percent and an error-budget alert | the observability block in the verification section; `adk-agent-observability` owns the signals |
| No single point of failure the journey depends on: the host runs in more than one zone, and the session store, the model endpoint and each external tool have a row in the coverage grid with "unavailable or slow" cited | failure grids; the hosting decision in [GCP decisions](gcp-decisions.md) |
| Capacity grows by adding instances, and the shared state those instances need is named; replica count alone does not shorten a model generation or raise a model quota | [runtime and delivery](runtime-and-delivery.md#preserve-contracts-through-startup-and-release) |
| Readiness, liveness and graceful shutdown have separate responsibilities; a shared-dependency outage does not trigger restarts | same section |
| Degradation is designed: timeouts inside the request deadline, retries with exponential backoff and jitter only for safe repeats, a circuit breaker or admission limit in front of a saturated dependency, and a stated reduced-function result ("Dropping some requests prevents global failures and enables the system to recover more gracefully", graceful-degradation page, fetched 21 October 2026) | the budgets section of [design decisions](design-decisions.md#latency-capacity-budgets-and-operations); `safe-api-tool-calls` and `adk-operational-guardrails` implement it |
| RTO and RPO are stated per store (sessions, business records, artifacts, memory), the backup interval is at most the RPO, and a restore into a non-production environment is a scheduled goal, not an assumption | the data and authority table; a goal with a restore acceptance case |
| Failure recovery is rehearsed: a release rollback and, at production profile, a regional or dependency failover are exercised before the first shared deployment | a release goal; `adk-release-engineering` |
| Incidents end in a blameless postmortem whose actions become goals or deferred items with triggers | the plan's Later table; `I<n>` incident records cited by the presenter |

## Cost optimization

Principles: [align spending with business value](https://docs.cloud.google.com/architecture/framework/cost-optimization/align-cloud-spending-business-value),
[foster cost awareness](https://docs.cloud.google.com/architecture/framework/cost-optimization/foster-culture-cost-awareness),
[optimize resource usage](https://docs.cloud.google.com/architecture/framework/cost-optimization/optimize-resource-usage),
[optimize continuously](https://docs.cloud.google.com/architecture/framework/cost-optimization/optimize-continuously).

| Check | Satisfied by |
| --- | --- |
| Every owned resource carries labels for environment, team and application, so the bill can be attributed to the journey; the labels are set in the deployment code, not by hand | the deployment goal; `deploy-adk-on-google-cloud` |
| Billing export to BigQuery and a budget with alerts exist for the project before the first live week, and the design says who reads them (a budget alert warns; the application's own admission control is what stops spend) | the cost assumptions in [GCP decisions](gcp-decisions.md#cost-and-capacity-assumptions) |
| Per-request cost is estimated as model, tool, retrieval and storage work, with a goal that reads the actual bill in the first live week and compares it with the estimate | same section; a `M<n>` measurement record |
| Environments are sized to their purpose: high availability and a multi-zone store in production only; development and staging scale to zero and share infrastructure where the security boundary allows (optimize-resource-usage page, fetched 21 October 2026) | the delivery constraints table; a deferred control with its trigger |
| Steady, predictable capacity is reviewed for committed-use discounts and burst or batch work for Spot or scale-to-zero serverless; model cost is reviewed for the smallest model that passes the evaluation set, with simple steps routed to it | a `Later` item with a review trigger; `adk-model-and-output-contracts` for the model choice |
| Idle resources (test deployments, disks, static IPs, old revisions) are inventoried and removed by an owned cleanup goal, never by inference from an empty listing | the cleanup acceptance of each goal that creates resources |
| Serverless or managed hosting is the default for a new workload unless a named constraint (GPU, long-lived sockets beyond the host limit, custom networking) requires otherwise | the hosting decision |

Sustainability's two design-relevant lines sit in the rows above: scale to
zero when idle, and route simple tasks to a small model (Google's
`google-cloud-waf-sustainability` skill, read 21 October 2026); the rest of
that pillar is organisational and is not reviewed here.

## Operational excellence

Principles: [operational readiness with CloudOps](https://docs.cloud.google.com/architecture/framework/operational-excellence/operational-readiness-and-performance-using-cloudops),
[manage incidents and problems](https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-incidents-and-problems),
[manage and optimize cloud resources](https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-and-optimize-cloud-resources),
[automate and manage change](https://docs.cloud.google.com/architecture/framework/operational-excellence/automate-and-manage-change),
[continuously improve and innovate](https://docs.cloud.google.com/architecture/framework/operational-excellence/continuously-improve-and-innovate).

| Check | Satisfied by |
| --- | --- |
| Production readiness is a listed set of criteria (who is on call, which runbook, which dashboards, which approvals) checked by the goal that precedes the first external users, not a feeling | the graduation conditions in [delivery profiles](delivery-profiles.md) |
| SLOs and error budgets are monitored where alerts lead to a stored session (trace, invocation and session identifiers preserved at every hop) | [runtime and delivery](runtime-and-delivery.md#observe-what-the-design-promises) |
| Incident roles, the escalation path and the communication channel are named before the first shared deployment; each incident gets an `I<n>` record and a review | the operations paragraph of the budgets section; the plan |
| Every infrastructure change is code in version control; the release unit (image, prompt version, model and judge IDs, tool schema hash, secret versions) moves and rolls back together through a pipeline with an evaluation gate that fails by exit code | the release bundle in the verification section; `adk-release-engineering` |
| Resource utilisation is reviewed on a schedule against the measured baseline, and right-sizing is a goal with a measurement, not a one-off | a `Later` item with a date trigger; `optimise-adk-on-google-cloud` |
| The architecture itself has a review date: model retirements, SDK pins and the deferred-controls table are revisited at the phase boundary | the presentation goal at each phase boundary |

## Performance optimization

Principles: [plan resource allocation](https://docs.cloud.google.com/architecture/framework/performance-optimization/plan-resource-allocation),
[elasticity](https://docs.cloud.google.com/architecture/framework/performance-optimization/elasticity),
[promote modular design](https://docs.cloud.google.com/architecture/framework/performance-optimization/promote-modular-design),
[continuously monitor and improve performance](https://docs.cloud.google.com/architecture/framework/performance-optimization/continuously-monitor-and-improve-performance).

| Check | Satisfied by |
| --- | --- |
| Initial capacity (instances, concurrency per instance, model quota, database connections) comes from a bounded load experiment or recorded history, not a guess; the experiment states its measurement boundary | the budgets section; a discovery goal with a stopping condition |
| Latency targets name both time to first meaningful output and time to a complete correct result, and the design says which component each target constrains | [runtime and delivery](runtime-and-delivery.md#account-for-work-through-completion-and-cancellation) |
| Caching is deliberate: a stable instruction and tool prefix for provider caching, bounded tool results, and an application cache only where reuse was measured, each with owner, freshness and expiry | the context-window decision in [design decisions](design-decisions.md#state-knowledge-and-freshness) |
| Components scale independently: the gateway, the agent host and any worker for long or deferred work are separate units, and a blocking call cannot stall the event loop | the component diagram; the concurrency paragraph in runtime and delivery |
| Autoscaling rules and their limits are set and tested against a burst, with downstream saturation (model quota, database connections) stated | the burst scenario in [failure review](failure-review.md#choose-revealing-scenarios) |
| Tracing covers one span per agent, tool and logical model call so a slow request can be attributed before production | the exporter test named in runtime and delivery; `adk-agent-observability` |

## Security

Security is reviewed through this skill's own tables (security posture, data
and authority, tool tiers) and `adk-agent-security`, `protect-adk-sensitive-data`
and `adk-tool-auth-and-secrets`; the WAF security pillar adds product-level
IAM, network and data-protection recommendations. Consult the installed
`google-cloud-waf-security` skill (google/skills) when the profile is
production and the design touches IAM bindings, perimeters or customer-managed
keys; if it is not installed, `adk-engineer` explains how to get it.
