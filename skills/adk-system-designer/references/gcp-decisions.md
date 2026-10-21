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

The gateway topology implies the host's ingress setting, and the design records
it as a decision rather than leaving it to the deployment: a public agent
behind an external Application Load Balancer accepts only
`INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER` traffic (so the default `run.app` URL
cannot bypass the gateway's authentication and Cloud Armor policy), and an
internal agent or tool service accepts `INGRESS_TRAFFIC_INTERNAL_ONLY`
([Cloud Run ingress settings](https://docs.cloud.google.com/run/docs/securing/ingress),
fetched 21 October 2026; the bypass argument is from Google's
`google-cloud-solution-n-tier-serverless-web-app` skill, read 21 October 2026).
`deploy-adk-on-google-cloud` carries the egress, private DNS and database
connection rules that follow from this choice.
Define evidence linking reviewed source and dependencies, inspected upload/image
contents, and the revision actually serving requests. Check required modules are
included, private files excluded, and policy settings reach their real consumers.

## Verify the deciding facts

Before a recommendation depends on a provider fact, consult current official
sources and record URL, access date, relevant service/region and API/SDK version.
Check supported session/memory interfaces, deployment/transport constraints,
identity and networking requirements, runtime/request duration, quotas, lifecycle
operations and feature availability. Treat undocumented assumptions as unresolved.

Check that a product or feature the design relies on is not deprecated,
retired or in a preview that excludes production use; a search for
"<product> release status" or the product's release-notes page settles it, and
the design cites the date (Google's `google-cloud-solution-architecture` skill
makes this a hard rule before any product recommendation, read 21 October 2026).
For each component where a credible alternative exists, record the
alternative considered and its pros and cons beside the choice; the decisions
table has room for that in its tradeoff column.

Google's Developer Knowledge API serves official documentation to agents, as
the `developer-knowledge` MCP server (`answer_query` for a conceptual
question, `search_documents` for exact flags, permissions and limits,
`get_documents` for a full page) or as REST at
`https://developerknowledge.googleapis.com/v1` with a gcloud access token or
an API key ([quickstart](https://developers.google.com/knowledge/quickstart),
fetched 21 October 2026). When it is available, use it for the dated source
this section asks for and cite the returned page. A lookup counts only when it
returned documentation: `PERMISSION_DENIED`, an HTTP 401, 403 or 429, an empty
result or an error payload is a failed lookup, and the decision stays
provisional with the exact lookup still needed (Google's
`retrieving-developer-knowledge` skill, read 21 October 2026). Never present
a recalled page as a retrieved one. When the host offers Google's
`finding-google-skills` skill, it fetches the current index of google/skills
and names the product skill that covers a provisioning question; the design
records that skill's name beside the decision for `adk-engineer`.

Starting points:

- [Google Cloud component selection](https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components)
- [ADK conversational context](https://google.github.io/adk-docs/sessions/)
- [ADK runtime event loop](https://google.github.io/adk-docs/runtime/event-loop/)
- [Cloud Run and GKE comparison](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/gke-and-cloud-run)
- [Google Cloud pricing calculator](https://cloud.google.com/products/calculator)
- [Cloud Billing budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets)

These are lookup entrypoints, not a frozen compatibility baseline. The intended
application's version, provider guarantee and dated evidence control the decision.

## Project foundation the first goal needs

The first goal that touches a project inherits constraints the design should
know before it chooses components. Record them in the delivery constraints
table, as facts when inspected and as asks when not; `adk-engineer` and
`deploy-adk-on-google-cloud` do the inspection and the enablement, under the
approval rules those skills state.

- **Who owns the foundation.** `gcloud organizations list` tells whether the
  account sits in an organisation: an entry with `owner.directoryCustomerId`
  is a domain-verified Google Workspace or Cloud Identity organisation whose
  folders, billing and policies someone else administers, so project
  creation, billing links and policy exceptions are calendar waits on that
  administrator, not goals for the team; an empty list or a self-owned
  organisation without that field is a personal account the developer
  controls (Google's `google-cloud-recipe-onboarding` skill, read 21 October
  2026). A new organisation that needs a landing zone (folders per
  environment, baseline policies, central audit logging) is the
  administrator's project; when the team must build it, consult the installed
  Google skill `google-cloud-recipe-foundation-builder` (from google/skills);
  if it is not installed, `adk-engineer` explains how to get it. When the first
  project, billing link and local credentials are the team's own first step,
  the installed `google-cloud-recipe-onboarding` and `google-cloud-recipe-auth`
  skills carry that path.
- **Effective organisation policies.** Inherited policies can forbid a design
  choice silently. Read the effective value with
  `gcloud org-policies describe <constraint> --project=<id> --effective`
  ([reference](https://docs.cloud.google.com/sdk/gcloud/reference/org-policies/describe),
  fetched 21 October 2026) for the constraints that bite an agent deployment,
  and design around the result instead of planning an exception:

  | Constraint | What it changes in the design |
  | --- | --- |
  | `iam.disableServiceAccountKeyCreation` | No downloaded keys: workload identity, impersonation and ADC only, which this toolkit prefers anyway |
  | `iam.allowedPolicyMemberDomains` | External testers, a consultant's account or a vendor service account cannot be granted roles; identity for demos and reviews comes from the organisation's domain |
  | `gcp.resourceLocations` | Region choice for hosting, sessions, artifacts, logs and the model endpoint is constrained; residency tracing starts from this list |
  | `gcp.restrictServiceUsage` | A product the design names may be unusable in this project; check each one before the components table is final |
  | `sql.restrictPublicIp` | A Cloud SQL session store needs private connectivity (Private Service Connect or private IP) and the Auth Proxy, not a public address |
  | `storage.publicAccessPrevention` and `storage.uniformBucketLevelAccess` | Artifact or download buckets serve through signed URLs or the application, never a public bucket; ACL-based sharing is unavailable |
  | `compute.vmExternalIpAccess` | GKE nodes and any VM-hosted tool need Cloud NAT or Private Google Access for egress |
  | `iam.automaticIamGrantsForDefaultServiceAccounts` | Default service accounts carry no Editor role; the serving identity needs explicit, narrow grants |

  Constraint names verified against the
  [organization policy constraints list](https://docs.cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints)
  on 21 October 2026; the selection follows the baseline that Google's
  `google-cloud-recipe-foundation-builder` skill enforces (read 21 October
  2026), so an enterprise project often has most of them on.
- **Billing.** `gcloud billing projects describe <id>` must show
  `billingEnabled: true` before any paid call; a denied read is unknown
  billing state, not disabled billing. Budgets and alerts are observation
  (see the cost section); the application's admission control is the stop.
- **APIs per goal.** Each goal that first uses a service names the API it
  enables (`run`, `aiplatform`, `sqladmin`, `secretmanager`, `logging`,
  `monitoring`, `cloudtrace` and so on) as a prerequisite in its execution
  scope, so enablement is an approved, recorded step of that goal rather than
  an implicit side effect of a command (Google's onboarding skill leaves API
  enablement to the product skill that needs it, read 21 October 2026).
- **VPC Service Controls as an input.** A service perimeter "blocks
  communication to Google Cloud services across the perimeter" by default,
  with ingress and egress rules for exceptions
  ([overview](https://docs.cloud.google.com/vpc-service-controls/docs/overview),
  fetched 21 October 2026). When the project sits in one, or regulated data
  requires one, every cross-boundary call in the design is a perimeter
  decision: the model endpoint, the session store, Secret Manager, the
  Developer Knowledge MCP server, external tool APIs and the browser gateway.
  Record the perimeter owner and treat each exception as a calendar wait.
  For data-residency or compliance frameworks, consult the installed Google
  skills `assuredworkloads-frameworks-navigator` and
  `assuredworkloads-environment-assessor` (from google/skills); if they are not
  installed, `adk-engineer` explains how to get them.
- **Application Design Center.** Where the organisation designs
  infrastructure in Application Design Center, its Terraform plan assessment
  is a free pre-deployment check the deployment goal can cite as evidence
  (Google's `application-design-center-design-deploy` skill, read 21 October
  2026); it does not replace the contracts and grids in this design.

## Cost and capacity assumptions

Estimate per-request cost as the sum of the model input/output work, tool/API
work, retrieval/screening and storage/network work that the design actually uses.
State model mix, token sizes, expected calls, retry bounds, region, currency and
pricing date. Separate fixed/minimum capacity and recurring storage from request
cost. Include failures and background memory/evaluation/cleanup work.

If prices or traffic are unknown, provide a symbolic estimate and a sensitivity
range; label illustrative inputs. The symbolic form, filled with what is
known, is a result the presenter can put on a cost slide:

```text
cost per request ≈ (input tokens × p_in + output tokens × p_out) × model calls
                   + tool and storage work per request
monthly ≈ cost per request × requests per month
```

Fill the token counts (measure one representative request offline), the
calls per request (from the workflow) and the volume (from the brief); leave
`p_in` and `p_out` symbolic with the pricing date to check, give the spend
ceiling the sponsor accepted, and name the goal that reads the actual bill
in the first live week. Never present that as a validated bill or a
hard spending cap. Alerts-only Cloud Billing budgets notify about spend and do
not automatically cap usage. Verify current coverage and limitations before
relying on a provider spend-cap feature. Admission checks, durable accounting when required,
restricted concurrency and staged shutdown need their own application design.

Plan a bounded load/quality experiment with the measurement boundary and limits
specified. A few successful calls cannot establish latency percentiles, capacity
or a production cost forecast.
