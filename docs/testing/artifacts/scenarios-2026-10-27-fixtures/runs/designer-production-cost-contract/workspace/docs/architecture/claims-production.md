# Design: claims triage assistant, production version

Status: **draft**, not yet accepted. Nothing here is a user decision except what the brief and the PoC design record.
Brief: [docs/discovery/claims.md](../discovery/claims.md) · PoC design: [claims.md](claims.md) · Plan: [docs/plans/claims-production.md](../plans/claims-production.md)
Written 2026-10-27 without network or cloud access: every price, quota and ADK behaviour below is a labelled assumption with a named check.

Summary, capacity and finish range live in the plan. This document holds requirements, contracts, decisions and failure coverage, each once.

## Assumed answers

Nobody could be asked, so each question is written down with the answer this design proceeds on. A change to an answer makes the decisions in the last column provisional.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | What is a "request" in "20,000 requests a month"? The PoC saw 62 claims in a week, so 14 handlers produce roughly 1,000 claims a month, not 20,000. | One request is one agent invocation: a handler's message through to the final reply (draft, re-draft or follow-up), about 20 per claim. | C9 volume, D7 caps, the per-request budget |
| Q2 | Is the $1,500 only the production project's run cost? | Yes. Staging and evaluation (including the judge model) sit in `fm-claims-pilot` under their own stop, set by the sponsor; placeholder $100 a month. If they must fit inside $1,500, the variable allowance A falls by that amount. | C9 split |
| Q3 | Capacity of the two developers | Both close to full time: 3.6 focused hours a day each (6 h × 0.6), 40 working days, no leave, 25 % reserve. Both know ADK and GCP from the PoC, so no learning multiplier. | The plan's cut line |
| Q4 | Does "production in eight weeks" mean all 14 handlers live? | No: eight weeks builds and proves the production service on the four PoC handlers, with the cost contract read against a live bill. The 14-handler rollout follows that reading (plan G15, phase 2). | Cut line, staged ceiling |
| Q5 | Who runs it afterwards? | Larkspur in hypercare, then Fenwick Mutual IT, who need a handover (phase 2). | Observability, runbooks |
| Q6 | Is a statement of work or change request needed for the production phase? | Existing engagement covers it. If not, a change request must be signed before G02 starts. | Start date |
| Q7 | Lock-in a concern? | No. No portability goal. | none |
| Q8 | Reviews needing a presentation | Go-live approval for Helen Okafor (business, G12); results review after four live pilot weeks (phase 2). Fenwick IT and security read this design and the staging evidence through review W9, not a deck. | G12, W7, W9 |
| Q9 | Retention of sessions and handler decisions | Sessions 90 days, decisions per Fenwick's claims retention policy (unknown to us). | G05/A8, G07 |
| Q10 | When the allowance runs low, what goes first? | Follow-up turns are refused first; first drafts keep running; handlers can always triage by hand as they do today. Helen to confirm. | D7 tiers |

## Profile, constraints and depth

**Profile: production**, for 14 internal handlers, phased: four PoC handlers first. Chosen because the sponsor set a spend ceiling, the service handles real claimant personal data, and the brief sets a continue/stop threshold on live use.

| Item | Value | Source |
| --- | --- | --- |
| Users, judge | 14 Leeds handlers; Helen Okafor decides on median triage ≤ 15 min and re-routing ≤ 9 % after four live weeks | brief |
| Volume and ceiling | 20,000 requests a month (Q1); $1,500 a month, enforcement not yet defined | sponsor |
| Data and effects | real claim notifications and policy data; the assistant changes nothing in the claims or policy systems | brief, C3 |
| Stack, kept from the PoC | Python 3.12, google-adk 2.12.0 (confirm in G03/A9), Gemini via Vertex AI europe-west2, Cloud Run behind IAP, Cloud SQL for PostgreSQL sessions, BigQuery claim history, Sensitive Data Protection | PoC D2, D5 |
| Environments | production `fm-claims-prod` (new, wait W1); staging is the PoC project `fm-claims-pilot` with its non-HA Cloud SQL retained | D13 |

| Concern | Depth now | Raised or built when |
| --- | --- | --- |
| Core judgment, measured | Build: gold set, CI gate | G10 |
| Identity and data scope | Build: IAP, per-handler sessions, team scope | G05 |
| Sensitive data | Build: SDP on inputs, tool results, every reply | G04 |
| Budgets and cost contract | Build: admission ledger, ratchet, reconciliation, operator stop | G03, G14, G15 |
| Observability, SLOs | Build | G09 |
| Release, recovery | Build: pinned bundle, canary, rollback, restore test | G08 |
| Regional failover, game day | Defer | availability target above 99.5 % or a region incident |
| ASVS L2 review, pen test, Cloud Armor (SB23–SB25) | Defer, accepted risk (see security table) | external users, a public endpoint, or Fenwick security requires it at W9 |
| Model-mix and committed-use review | Defer | first monthly bill, then quarterly |
| Motor claims | Out of scope | home pilot meets its threshold |

## Requirements

R1–R4 as the PoC design. **R5 is superseded by R7.**

- R6 Sensitive Data Protection is applied to every reply, so no reply, stored session event or log line carries sensitive data the agreed list names.
- R7 Spend stays under $1,500 a month at 20,000 requests a month, and something enforces it without a person.
- R8 Sessions and handler decisions survive a zone failure and can be restored (assumed RPO 5 min and RTO 60 min for decisions).
- R9 A handler sees and continues only their own sessions.

## Architecture

```text
Handler browser ── IAP ──> Cloud Run `claims-assistant` (FastAPI, ADK Runner in process, max 5 instances)
                              │ 1 verify principal (IAP assertion), team scope            [C1, C7]
                              │ 2 admission: control read, caps, reserve in ledger        [C8, C9]
                              │ 3 notes ──> SDP de-identify ──> Runner (non-streaming)    [C4]
                              │ 4 tools: get_policy (API, read-only) · claim_history (BigQuery)
                              │         · search_wording ── each result ──> SDP            [C3, C4]
                              │ 5 model reply ──> SDP ──> screened marker ──> session     [C6]
                              │ 6 validator (clause cited) ──> release gate ──> browser   [C2, C6]
                              └ 7 settle ledger with actual usage
Cloud SQL PostgreSQL (regional HA): ADK sessions · decisions · usage_ledger · control
Budget ──> Pub/Sub ──> ratchet handler (private Cloud Run service) ──> control tier       [C9 backstop]
Billing export (BigQuery) ──> scheduled reconciliation query ──> drift tier / alert        [C9 authority]
```

One service, one Postgres instance and one pipeline, because 20,000 requests a month is about 900 a working day (peak well under one a second, a handful in flight at once). A separate gateway, queue or worker would add idle cost and failure modes with no load to justify them. ADK's own routes are never exposed (SB05). The ratchet handler is a separate private service so a fault in the agent service cannot loosen its own cost tier.

Journey, kept from the PoC: a handler opens a new escape-of-water claim, sees urgency "high" and cover citing section 3.2, accepts it, and the claim routes to the property team. In production the same handler's request is first admitted against the month's allowance, every free-text field is screened on the way in and out, and a handler from another team cannot open it.

## Contracts

R→C: R1→C4; R2→C2; R3→C1; R4→C3, C11; R6→C6; R7→C8, C9; R8→C10; R9→C7. Status column says what is proven today; the plan's goals record the actual evidence.

| ID | Invariant (scope) | Authority | Enforcement, and recheck at the effect | Failure outcome | Evidence (planned) |
| --- | --- | --- | --- | --- | --- |
| C1 | A handler reads only claims in their team's queue (team). | claims queue | API dependency filters by the verified handler's team; `get_policy` and `claim_history` take the claim ID from trusted session state and re-read its team | 404 | PoC evidenced locally; regression G05/A4, G06/A1 |
| C2 | Every cover position cites a clause from the policy's own wording, or says none found; if the policy API cannot be read, the draft is withheld as "cover not checked" (claim). | policy wording | output validator rejects uncited output | draft withheld, handler triages by hand | G10/A6, G10/A7 |
| C3 | The assistant never changes a claim, policy or status (all). | claims system | no write tool bound; policy API credential read-only; BigQuery service account read-only | refusal | G06/A4, G10/A3 |
| C4 | **Revised.** Claim notes **and every tool result** reach the model only after de-identification (detected infoTypes masked). Residual: undetected text. It is measured, not claimed zero. | SDP, infoType list agreed with the DPO (W3) | `app/deidentify.py` before the Runner; `after_tool_callback` on each tool; a failed screen withholds | draft withheld | G04/A3, G04/A5 |
| C6 | **New.** No reply, stored session event or log line carries an unmasked infoType from the agreed list; a reply is screened before it is persisted or shown (reply). | SDP, same list | `after_model_callback` replaces the response with screened text and sets a marker; the Runner runs non-streaming; the release gate refuses any event without the marker; an SDP error or timeout fails closed | fixed message "Draft withheld: triage by hand"; no raw text persisted | G04/A1, A2, A6, A7, A8 |
| C7 | A handler reads and continues only sessions they own; one active run per handler and conversation (handler). | verified IAP principal | `user_id` overwritten from the token on every ADK call; a session ID only locates; Postgres advisory lock for the run | same 404 as an unknown session, no model call | G05/A3, G05/A10 |
| C8 | One request makes at most N model calls, T tokens and S seconds, and each BigQuery query bills at most B bytes (request). N, T, S, B are fixed by G01. | RunConfig and tool config | `RunConfig.max_llm_calls`, output token cap, input truncation, request deadline, `maximum_bytes_billed` | fixed message; ledger settles actual usage | G03/A6, G06/A2 |
| C9 | **Cost.** At 20,000 requests a month, spend in `fm-claims-prod` stays under $1,500: fixed ≤ $300 (assumed split), variable allowance A = $1,000, reserve $200. Average request ≤ $0.05 and p95 ≤ $0.15 (placeholders until G01). Scope: project, billing month; during the cohort phase a staged ceiling of $300 on A applies. | Cloud Billing export (the ledger is an estimate) | see "Cost contract" below: admission ledger with reserve and settle, tiers, per-user, daily and request-count caps, operator stop; quotas and max instances as backstops; budget ratchet and export reconciliation as the second line | new model work refused with a fixed message; reads and decision recording still work; Helen's team and the owner are notified | G03/A1–A8, G14/A1–A4, G08/A7, G15/A1–A4; **live bill unproven until G15** |
| C10 | Decisions: RPO ≤ 5 min, RTO ≤ 60 min. Sessions: loss means re-draft, RPO 24 h (assumed, R8). | Cloud SQL | regional HA, PITR 7 days, automated backups; restore tested into non-production | read-only mode, handlers triage by hand | G08/A5, G08/A6 |
| C11 | A handler's accept or change is recorded once, attributable to the verified handler and bound to the draft version (decision). | decisions table | unique key on draft ID; refused if the draft was superseded; principal from the token | second submit returns the first result | G05/A7 |

C5 (PoC: daily quota and max bytes billed) is **superseded by C8 and C9**; its evidence was configuration only and its "no live overrun" gap is closed by G08/A7.

## Cost contract (C9) in detail

**Enforcement.** The Cloud Billing export reports spend hours to a day late, and a budget alert only notifies, so neither can stop a request. The stop is the application's own admission control; the billing signals ratchet it tighter and prove it.

| Layer | Mechanism | Acts when | Stops or observes |
| --- | --- | --- | --- |
| 1 Per request (C8) | `max_llm_calls`, token caps, deadline, `maximum_bytes_billed` | inside one request | stops |
| 2 Admission (D7) | One Postgres transaction per request: read control (operator stop, tier), check per-handler daily cap, daily and monthly request counts and daily and monthly dollar caps, then reserve the worst-case request cost from the price table; settle with actual `usage_metadata`, SDP and bytes-billed on completion; an unsettled reservation expires into a conservative settle | before any model call | stops |
| 3 Operator stop | A `control.operator_stop` latch set by a CLI role the agent never holds; survives month rollover; out-of-band twin: remove the runtime service account's Vertex AI role | on demand | stops |
| 4 Backstops | Vertex AI quota override; BigQuery daily custom quota; Cloud Run `max-instances` 5 | rate and capacity, not money | stops runaway rate if layers 1–2 fail |
| 5 Ratchet (G14) | Billing budget on total project spend ($1,500; 50, 70, 85, 100 % and forecast) → Pub/Sub → private handler → monotonic tier within the month | hours late | tightens only |
| 6 Reconciliation (G14) | Daily scheduled query over the billing export, sliced by project and the `env/team/app` labels, against the ledger; drift above 15 % tightens one tier and alerts | a day late | tightens, proves |

**Tiers on A (and on total spend through the ratchet; the stricter wins).** T0 below 70 %. T1 at 70 %: notify. T2 at 85 %: refuse follow-up turns, keep first drafts (Q10). T3 at 100 % of A: no new model work. Daily dollar cap 2.5 × the average working day (A ÷ 22, about $113); monthly request cap 22,000 (110 % of volume); per-handler daily cap 200 (about 3× the average of 65). All are assumptions G01 confirms. If the control store is unreadable, admission denies; a read error is never "normal".

**Budget algebra at the ceiling.**

| Part | Amount | Basis |
| --- | --- | --- |
| Fixed F | ≤ $300 | allocation, not a price: Cloud SQL HA, Artifact Registry, Secret Manager, logging, BigQuery storage, Scheduler, Pub/Sub. Min instances 0, no load balancer, no NAT. G02 and G08 fill each row from the pricing page |
| Variable allowance A | $1,000 | model, SDP, BigQuery scan, Cloud Run compute, as metered by the ledger |
| Reserve R | $200 | unmetered variable cost and ledger drift; not spendable by admission |
| Total | $1,500 | the sponsor's ceiling |

Per-request average = A ÷ 20,000 = **$0.05**.

```text
cost per request ≈ (input tokens × p_in + output tokens × p_out) × model calls
                   + SDP calls (≈ 4: notes, two tool results, reply) × size × p_sdp
                   + bytes billed × p_bq + Cloud Run vCPU-s and GiB-s × p_run
p_in, p_out, p_sdp, p_bq, p_run: list prices, not retrieved (no network); G01 fills them with the pricing date.
```

**Feasibility is not established, and the largest known risk.** The PoC's M2 recorded £38.20 of model and BigQuery spend for 62 claims in a week, about £0.62 a claim. At an illustrative $1.30 per £ (my assumption) that is about $0.80 a claim. If a claim was one request, the production budget is 16 times lower than what was observed; it holds only if a claim averages 16 or more requests or the cost per request falls by that factor. M2 may also include evaluation runs, and it does not say. G01 settles this from the billing report by SKU before G03 sizes anything: which unit M2 measured, expected and p95 cost per request, and the levers if it is over (smaller model for the classification step, retrieval of the applicable clause instead of full wording, a stable prefix for provider caching, fewer model calls, lower output cap). If no lever closes the gap, the sponsor chooses between a higher ceiling and a lower volume; the design does not assume either.

**Staged ceiling.** The four-handler cohort runs under a $300 cap on A (about 4/14 of $1,000, rounded). G15 reads the bill; only then does an operator-approved change raise the cap. This limits the loss if the estimate is wrong.

**Labels and attribution.** Every owned resource carries `env`, `team`, `app` labels set in the deployment code (G02/A1), and production is its own project, so the export can be sliced and the contract proved.

**Provider spend-cap budgets** can pause eligible usage but are delayed and scope-limited; eligibility could not be looked up here. Optional extra, never relied on (OD8).

### Resources that charge while provisioned

Ledger rows checked against [resource-costs](../../.claude/skills/adk-system-designer/references/resource-costs.md). Prices were not retrievable; the PoC figure is cited, the rest are placeholders the creating goal fills as its first acceptance item. Owner of each lifetime: this cost contract (C9) and the Later decommission item.

| Resource (created by) | Configuration | Idle cost per day | Cleanup | Verify absent |
| --- | --- | --- | --- | --- |
| Cloud SQL `fm-claims-prod-sql` (G08) | PostgreSQL regional HA, europe-west2, PITR 7 days, private IP | placeholder; the PoC non-HA instance was about £1.60 a day (pricing page read 2026-10-05) and HA is assumed to be about twice that | `gcloud sql instances delete fm-claims-prod-sql --project fm-claims-prod`, then delete its backups | `gcloud sql instances list` and `gcloud sql backups list` empty |
| Cloud SQL `fm-claims-pilot-sql` (retained from PoC, staging) | db-custom-1-3840, 10 GB, no HA | about £1.60 a day (PoC, 2026-10-05) | `deploy/delete_sql.sh --project fm-claims-pilot --instance fm-claims-pilot-sql` | `gcloud sql instances list --project fm-claims-pilot` |
| Cloud Run `claims-assistant`, `claims-ratchet` | min instances 0, max 5 and 1 | none at min 0 | `gcloud run services delete` | `gcloud run services list` empty |
| Artifact Registry `claims` | one repository per project | placeholder (per GiB above the free tier) | `gcloud artifacts repositories delete` | list empty |
| Secret Manager secrets | per active version | placeholder | `gcloud secrets delete` | list empty |
| BigQuery `claims_history`, `cost_ops` datasets | storage only; no reservations | placeholder | `bq rm -r -d` | `bq ls` |
| Cloud Scheduler, Pub/Sub topic | reconciliation job, budget topic | negligible, confirm | delete each | lists empty |

Not used, so no idle charge: load balancer, Cloud NAT (Private Google Access and Direct VPC egress instead), Agent Runtime, Vector Search, RAG Engine, Provisioned Throughput.

## Decisions

D1–D5 stand from the PoC design with these revisions: **D2** model IDs `gemini-3.5-flash-001` and judge `gemini-3.5-pro-001` stay pinned, but their retirement dates were not checked (the dated lifecycle table is not installed here); G01/A4 records them. **D5** now reads: production runs in `fm-claims-prod`, staging in `fm-claims-pilot`, both europe-west2.

| ID | Requirement → contract | Choice | Alternative and tradeoff | Check |
| --- | --- | --- | --- | --- |
| D6 | R7 → C9 | Cloud Run single service, request-based billing, min instances 0, max 5, FastAPI with the ADK Runner in process | Agent Runtime would manage sessions, but sessions must be Cloud SQL, and the ledger and decisions sit beside them. Cost: cold starts of a few seconds; raise min instances to 1 if p95 cold start exceeds 10 s | G05, G09 latency SLI |
| D7 | R7 → C8, C9 | Admission ledger in Postgres with atomic reserve and settle, tiers, caps, operator stop; billing signals only tighten | Budget-triggered shutdown alone reacts hours late and billing unlink is a project-wide outage; rejected as the primary. Cost: custom code to build and test, a price table to keep current | G03/A1–A8 |
| D8 | R6 → C4, C6 | SDP in ADK callbacks so the session stores screened text, plus a release gate that needs the marker; model runs non-streaming; fail closed | Screening only at the API route would persist raw text in sessions. Streaming tokens would release text before screening. Cost: handlers wait for the whole reply, and an SDP outage means no drafts (they triage by hand); the callbacks' behaviour on 2.12.0 must be confirmed (G04/A9); a screened session-service wrapper is the fallback | G04/A1–A9 |
| D9 | R8, R9 → C7, C10, C11 | One regional-HA Cloud SQL instance, private IP, PITR; separate schemas and database roles for ADK sessions, decisions, ledger and control | A second instance isolates blast radius but doubles idle cost; the roles limit it instead. HA about doubles instance cost (inside F) and is chosen because the decisions table is a business record | G08/A5, A6 |
| D10 | R1 → C1, C3, C8 | `claim_history` is a reviewed parameterised template over a BigQuery table partitioned by claim date and clustered by policy ID; claim ID from trusted state; `maximum_bytes_billed`; read-only service account | Free-form SQL by the model rejected (injection, cost). Cost: new questions need a new template. Loader owner and freshness: OD9 | G06/A1–A6 |
| D11 | R7 → C9 | Evaluation judge runs offline in CI under the staging allowance, never in the request path | An online judge doubles per-request model cost | G10, Q2 |
| D12 | R6, R7 → C6, C9 | Telemetry to Cloud Trace and structured logs with prompt and reply content capture off; token usage feeds the ledger and the cost SLIs | Content logging would copy personal data into a second store. Cost: debugging uses session IDs and screened events only | G09/A1, A2 |
| D13 | R7 → C9 | Production in its own project; the PoC project becomes staging, with its own quota-limited allowance | Reusing one project mixes evaluation spend into the contract's bill. Cost: new project wait W1 and a second IAM setup | G02, G08 |

## Security baseline

Components: `/api` routes, agent routes, ADK runtime, handler decisions and sessions, SPA, deployment. Tiers 1–6 apply to production; rows marked deferred are an accepted risk that Fenwick security must accept at W9: internal users behind workforce SSO, no write tools, no uploads.

| Rule | Component | Depth | Proved by, `n/a:` or `deferred:` |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G05/A1 |
| SB02 | IAP, workforce SSO | Build | G05/A2 |
| SB03 | agent routes | Build | G05/A3 |
| SB04 | records and tools | Build | G05/A4, G06/A1 |
| SB05 | ADK runtime | Build | G05/A5 |
| SB06, SB07, SB09, SB10, SB13 | API configuration, SPA | Build | G05/A6 |
| SB08 | IAP session cookie on state-changing requests | Build | G05/A6 (Origin check) |
| SB11 | uploads | n/a: notes arrive as text from the claims queue, no uploads | |
| SB12 | outbound fetch | n/a: no tool fetches a URL | |
| SB14 | logging | Build | G09/A2, G09/A5 |
| SB15 | supply chain | Build | G08/A9 |
| SB16 | secrets | Build | G02/A2, G08/A9 |
| SB17 | untrusted content with write tools | Build: structurally no write tool | G10/A3 |
| SB18 | external effects | n/a: the agent has no effect tool; the handler's decision is their own action (C11) | |
| SB19 | cost and abuse | Build | G03/A7, G05/A10 |
| SB20 | token revocation | Build | G05/A9 |
| SB21 | ZAP baseline on staging | Build | G08/A8 |
| SB22 | ASVS L1 review | Build | G10/A4 |
| SB23 | ASVS L2 review and full adversarial programme | deferred: external users, or Fenwick security requires it at W9 | |
| SB24 | penetration test | deferred: external users, or required at W9 | |
| SB25 | Cloud Armor | deferred: a load balancer or non-IAP endpoint is added | |

## Failure coverage

Every cell cites an acceptance item in the plan or says why it cannot occur.

| Integration | Unavailable or slow | Rejects | Write outcome unknown | Partial multi-step | Credential expired or revoked | Rate limited or quota | Duplicate or concurrent | Untrusted or malformed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini on Vertex AI | G03/A6 | G03/A6 | G03/A3 | n/a: one draft flow, no partial release (G04/A7) | G03/A6 | G03/A6 | G05/A10 | G10/A3, G10/A6 |
| Sensitive Data Protection | G04/A2 | G04/A2 | n/a: stateless transform | G04/A3 | G04/A2 | G04/A8 | n/a: idempotent transform | G04/A2 |
| Cloud SQL | G03/A5, G08/A5 | G05/A7 | G05/A7 | G03/A3 | G03/A5 | G03/A5 | G03/A2, G05/A7 | n/a: rows written only by this service |
| BigQuery claim history | G06/A3 | G06/A2 | n/a: read only | n/a: single query | G06/A3 | G06/A6 | n/a: read only | G06/A5 |
| Policy API | G10/A7 | G10/A7 | n/a: read only | n/a: single read | G10/A7 | G10/A7 | n/a: read only | G04/A3, G10/A3 |
| IAP and identity | G05/A9 | G05/A2 | n/a: no write | n/a: no write | G05/A2, G05/A9 | n/a: managed by IAP | n/a: stateless | G05/A2 |
| Budget Pub/Sub and ratchet | G14/A5 | G14/A2 | G14/A2 | n/a: one compare-and-write | G14/A2 | n/a: a few messages a day | G14/A2 | G14/A2 |
| Billing export | G14/A4 | n/a: read only | n/a: read only | G14/A4 | G14/A4 | n/a: one daily query | n/a: read only | G14/A4 |

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| Handler records a decision (own table) | n/a: one claim per request, principal from token | n/a: one row | G05/A7 (superseded draft refused) | G05/A7 | G05/A7 |
| Agent change to a claim | n/a: no such tool (C3, G10/A3) | n/a | n/a | n/a | n/a |

## Recovery, reliability and operations

- **Recovery targets** are C10. The backup interval (PITR continuous) is within the RPO. G08/A6 restores into non-production and measures RTO; an untested backup is a hypothesis.
- **Rehearsed before the first shared deployment:** release rollback (G08/A4), zonal Cloud SQL failover (G08/A5), operator stop drill (G13/A3). Regional failover is deferred (table above), accepted risk: a region loss is a rebuild from code plus a restore.
- **SLIs (good ÷ total, targets from the staging baseline, never 100 %).** Drafts that are screened and cited, or deliberately withheld, inside 30 s (assumed target, measure); SDP withhold rate; tokens and dollars per request against C9; tool error rate by tool. Alerts go to a named Larkspur channel until handover, then to Fenwick IT (G09/A3).
- **Capacity:** about 100 requests an hour at peak, 5 or fewer in flight at an assumed 25 s each; 5 instances × concurrency 8 is ample. A bounded load test sets the actual figures (G08, with the staging overrun test); the numbers above are not measurements.
- **Release unit:** image digest, prompt version, model and judge IDs, tool schema hash, price table version, infoType template version and secret versions move and roll back together (G08/A2, A4).

## Compared with the PoC design

| Item | Change | Reason |
| --- | --- | --- |
| C5 daily quota and max bytes billed | replaced by C8 and C9, stronger | the PoC's "no live overrun tested" gap closes in G08/A7 |
| C4 | widened from notes to tool results | session store and BigQuery data carry names |
| SB05 | deferred → Build | production |
| Later: recurring cost review, decommission, production hardening | carried into the plan | none removed |
| Nothing removed or weakened | | |

## Open decisions and unproven items

| ID | Question or gap | Who settles | Blocks |
| --- | --- | --- | --- |
| OD1 | Is $0.05 average and $0.15 p95 per request reachable? | G01 measurement, then the sponsor | sizing in G03; the ceiling or the volume if not |
| OD2 | Meaning of "request" (Q1) | sponsor | C9 numbers |
| OD3 | Staging and evaluation spend inside or outside $1,500 (Q2) | sponsor | A |
| OD4 | infoType list, mask or token, and an acceptable miss rate for C4 | Fenwick DPO (W3) | G04 |
| OD5 | Retention of sessions and decisions (Q9) | Fenwick DPO | G05/A8 |
| OD6 | Change request needed? Who operates after handover? (Q5, Q6) | Larkspur engagement lead | start; phase 2 |
| OD7 | Fenwick security accepts SB23–SB25 deferral | W9 | go-live |
| OD8 | Cloud Billing spend-cap eligibility and scope | check with network access | optional extra only |
| OD9 | Who loads claim history into BigQuery, freshness (assumed ≤ 24 h) | Raj Mehta (W4) | G06 |
| OD10 | Follow-ups refused first at T2 (Q10) | Helen Okafor | D7 tiers |
| U1 | ADK 2.12.0 callback and `usage_metadata` behaviour as assumed | G03/A9, G04/A9 | D7, D8 |
| U2 | All prices, quotas and model retirement dates | G01, G02, G08 | C9 numbers |
