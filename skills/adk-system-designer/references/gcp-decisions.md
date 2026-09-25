# Map responsibilities to ADK and Google Cloud

Use this when a design needs service choices, capacity or costs. Favor the
project's existing stack where it satisfies the contracts. A design can name a
provisional product and its verification task without provisioning it.

## Make independent choices

| Responsibility | Decision to justify |
| --- | --- |
| Application compute | Compare managed Agent Runtime, Cloud Run or GKE against required interfaces, deployment control, networking, existing operations and workload behavior. |
| Model inference | Choose model/backend from quality, latency, privacy, availability and cost evidence; hosting the app and serving the model are separate. |
| Conversation state | Choose a supported ADK session backend; verify persistence, tenant scope, concurrency and compatibility with the actual serving entrypoint. |
| Business operations and exact profiles | Keep the authoritative service/store and required uniqueness/transaction semantics explicit. |
| Memory and retrieval | Choose semantic recall and knowledge retrieval only for the facts that need them; evaluate governance and erasure independently of search quality. |
| Artifacts | Decide file/object ownership, access, versions and retention separately from conversation metadata. |
| Public API and identity | Reuse verified login where possible; define gateway/agent trust and workload identity independently of end-user identity. |
| Telemetry and delivery | Specify permitted signals/content, access and retention, release/rollback ownership and environment boundaries. |

Compare credible hosting alternatives without attaching a universal “production”
label to one product. Include team operational capacity. Additional application
replicas require suitable shared state and do not remove model, database or
protection-service quotas. A managed service does not automatically implement
the application's business invariants.

Trace residency across inference, sessions, artifacts, logs, backups and external
tools. The application host's region alone does not establish where all data goes.

Separate deployer, builder, serving workload and end-user identities; include node
identity when that platform needs it. Record their distinct grants and owners.
Define evidence linking reviewed source and dependencies, inspected upload/image
contents, and the revision actually serving requests. Check required modules are
included, private files excluded, and policy settings reach their real consumers.

## Verify the deciding facts

Before a recommendation depends on a provider fact, consult current official
sources and record URL, access date, relevant service/region and API/SDK version.
Check supported session/memory interfaces, deployment/transport constraints,
identity and networking requirements, runtime/request duration, quotas, lifecycle
operations and feature availability. Treat undocumented assumptions as unresolved.

Starting points:

- [Google Cloud component selection](https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components)
- [ADK conversational context](https://google.github.io/adk-docs/sessions/)
- [ADK runtime event loop](https://google.github.io/adk-docs/runtime/event-loop/)
- [Cloud Run and GKE comparison](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/gke-and-cloud-run)
- [Google Cloud pricing calculator](https://cloud.google.com/products/calculator)
- [Cloud Billing budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets)

These are lookup entrypoints, not a frozen compatibility baseline. The intended
application's version, provider contract and dated evidence control the decision.

## Cost and capacity assumptions

Estimate per-request cost as the sum of the model input/output work, tool/API
work, retrieval/screening and storage/network work that the design actually uses.
State model mix, token sizes, expected calls, retry bounds, region, currency and
pricing date. Separate fixed/minimum capacity and recurring storage from request
cost. Include failures and background memory/evaluation/cleanup work.

If prices or traffic are unknown, provide a symbolic estimate and a sensitivity
range; label illustrative inputs. Never present that as a validated bill or a
hard spending cap. Alerts-only Cloud Billing budgets notify about spend and do
not automatically cap usage. Verify current coverage and limitations before
relying on a provider spend-cap feature. Admission checks, durable accounting when required,
restricted concurrency and staged shutdown need their own application design.

Plan a bounded load/quality experiment with the measurement boundary and limits
specified. A few successful calls cannot establish latency percentiles, capacity
or a production cost forecast.
