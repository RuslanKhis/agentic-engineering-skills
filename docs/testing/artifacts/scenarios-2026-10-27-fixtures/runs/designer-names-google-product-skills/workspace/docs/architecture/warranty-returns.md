# System design: warranty answers and return requests (ADK on Cloud Run)

Status: **draft, unreviewed.** Written in a non-interactive session: nobody could answer the scope-gate questions, so every answer below is an assumption (see Assumed answers) and every decision that depends on one is provisional. Nothing here has been accepted by the user. Capacity, finish range and cut line are in the plan's summary ([plan](../plans/warranty-returns.md)), not restated here.

## Assumed answers

Questions I would have asked, the answer I proceeded on, and what depends on it. Correct any row and the dependent decisions change.

| # | Question | Assumed answer | Depends on it |
| --- | --- | --- | --- |
| Q1 | When must the first version exist; continued afterwards? | Six weeks from 2026-11-02 (ends 2026-12-11), then continued and operated | Phase 1 size, cut line |
| Q2 | Who builds it, hours, familiarity? | Two developers (Dev A, Dev B), about 30 h/week each on this at a 0.6 focus factor = 3.6 focused h/day each; strong Python and GCP, new to ADK (×1.5 on ADK goals) | Every estimate; capacity |
| Q3 | Money for models and cloud? | Unknown. Spend ceiling and expected volume are placeholders the sponsor sets (O7) | C9, hosting sizing |
| Q4 | Who uses and judges it? | External customers on the web; the support team and the business sponsor judge it. Phase 1 reaches an **allowlisted cohort** of real customers (O1) | Identity, SB tiers, SB24 timing |
| Q5 | Own web interface, who reaches it, who continues it? | Own single-page chat UI at a public URL behind a load balancer; the two builders run it in phase 1, IT hand-over in phase 2 | D1, D9, G08, hand-over goal |
| Q6 | Data touched, what can change? | Personal customer data (identity, purchase history, serial numbers). Reads the product database; writes one return request per confirmed proposal, which a real person at the company will act on | Floor, C4–C8 |
| Q7 | Which reviews need a presentation? | Go-ahead before build (business), launch decision before go-live (business plus the platform and security reviewers), results review in phase 2. Dates unknown | G01, G18, phase 2 |
| Q8 | Client contract or statement of work? | No, internal build | No SoW goal |
| Q9 | Lock-in concern? | No | No portability goal |
| Q10 | Residency and jurisdiction? | Unknown. Region comes from the effective `gcp.resourceLocations` policy (read in G02); jurisdiction is screened in G14 | Region, G14 |

## Purpose and constraints

**Journey.** A customer signs in and asks "is my blender still under warranty?" The agent finds their purchase, reports the warranty status computed from the product database, and, if the customer wants a return, drafts a return request. The customer reviews the exact details and presses Confirm; only then is the request filed with the returns system and a reference shown.

**Friction and outcome.** Today (assumed) a customer reads policy pages or waits for support. The outcome to improve is the share of warranty questions answered correctly without a support contact and the time to file a valid return. **No baseline exists; measuring one is a phase 2 goal** (the discovery brief that would hold it was not supplied; if one exists, read it first and treat its confirmed answers as settled).

**What the model decides and what code controls.** The model interprets the question, chooses tools and words the answer. Code decides: who the customer is, which purchases they may see, warranty status (a deterministic rule function over database fields), whether a proposal is valid, confirmation, and filing. The model can draft a proposal; it cannot confirm or file one.

**Non-goals (phase 1).** Refund or payment actions, uploads (photos), human-ticket creation, other languages, memory across sessions, unstructured policy retrieval.

**Existing systems (assumed, not inspected: no repository, no cloud access).** Product database (read-only access, engine unknown, O2), a returns system with an API (O3), a landing zone with folders, policies and billing owned by an administrator (the project, billing link and policy exceptions are calendar waits, W1), no customer identity provider known (O4).

## Delivery constraints, depth and deferred controls

**Profile (one line, correct it):** production service **launched in phases**. Phase 1 reaches production go-live for an allowlisted customer cohort at MVP/pilot depth (security tiers 1 to 5); phase 2 reaches production depth (tier 6, canary, full SLOs, hand-over) before the service opens to all customers. I chose this because production depth for every concern does not fit six weeks for two people (plan summary); it is the first decision for you to confirm (O1).

Depth per concern the journey touches:

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment (warranty answers) measured | Build: 30+ labelled cases, gate | Production depth: gated in CI with judge schedule (phase 2) |
| Identity and per-customer scope | Build | — |
| External write (return request) | Build: confirmation, idempotency, recheck, reconcile | Refund or payment effect appears (O3): full replay and reconciliation |
| Secrets | Build: Secret Manager, workload identity | Rotation schedule at production |
| Sensitive data | Build: minimal fields, no content in logs, erasure | Regulated jurisdiction or new data class |
| Injection and agency | Build: structural split (D5), scripted-model suite | Uploads, URL fetch or a second write tool |
| Budgets and abuse | Build: per-customer allowance, admission, kill switch, cost contract with a stop | Opening beyond the cohort |
| Hosting | Build: Cloud Run behind external load balancer, staging and production | Regional failover at production |
| Observability | Minimal: traces, token cost, two alerts | Full SLOs, dashboards, analytics (phase 2) |
| Release engineering | Minimal: pinned release unit, manual-run eval gate plus CI audit, rollback rehearsal | Canary and joint rollback automation (phase 2) |
| Web security baseline | Tiers 1 to 5; SB25 Minimal | SB23, SB24 before opening beyond the cohort |
| Performance and cost tuning | Defer | Measured traffic from the first live week |

**Floor kept:** no secrets in source, prompts or logs; spend stop (`max_llm_calls`, admission, kill switch); no irreversible or outside-visible effect without the customer's confirmation (the customer is the approver; support staff are not in the loop in phase 1); real personal data scoped and out of logs; nothing reachable without sign-in; pinned model ID.

**Accepted risk, not yet accepted by anyone:** launching to a cohort before the penetration test (SB24) and ASVS Level 2 (SB23). Proposed owner: the sponsor (O1). Ends when the service opens beyond the cohort; phase 2 builds both first.

**Environments:** staging uses a masked or synthetic copy of the product data, never real customers (floor: real personal data only where the journey needs it). Only production touches real data. Staging scales to zero; production holds the always-on cost.

## Requirements and contracts

| ID | Requirement | Status |
| --- | --- | --- |
| R1 | Answer warranty questions about the customer's own products from the product database | User request |
| R2 | File a return request only after the customer confirms | User request |
| R3 | Real customer data is protected end to end | User request ("real customer data") |
| R4 | Operable in production: failures are honest, spend is bounded, releases are reversible | Assumed from "production" |
| R5 | Built by two developers in six weeks | User request |

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R3 | Every `/api` call and tool call runs as the customer in the verified token; a session id or a model argument never selects another customer | Every request | Identity provider token | Principal dependency fails closed; server overwrites `user_id`; session ownership checked before any model call | 401, or the same 404 body for unknown and foreign sessions; no model call | planned: G05/A1–A3, G12/A6, local then live |
| C2 | R1, R3 | A customer reads only their own purchases and returns; an empty authorised result never widens the query | Purchases, drafts, operations | Product database ownership; application tables filtered by owner | Tools take `customer_id` from trusted session state; queries filtered in code; owner filter on every record route | "No purchase found"; nothing disclosed | planned: G05/A4, G06/A3, local then live |
| C3 | R1 | Warranty status shown (covered, expired, not determinable, end date) is computed by the rule function from the product record and cited fields; it is never produced from model memory; missing data yields "cannot determine" | Each answer | Product database fields; versioned rule function owned by the warranty policy owner (O6) | Rule function in code; answer composed from the tool result; output checked against the result | Honest "I can't determine this" plus the contact route | planned: G04/A1–A2, G06/A1, G09/A1–A2 |
| C4 | R2 | A return request is filed only after the same signed-in customer confirms the exact stored proposal (line, reason, resolution); the model holds no filing tool; reject runs the filing zero times | Each proposal | Stored proposal hash | Confirm is an API route, not a model action; confirm checks owner and hash | Refusal naming what changed; draft stays | planned: G07/A1, A2, A9 |
| C5 | R2 | One confirmed proposal yields at most one returns-system request, including under double click, retry, restart and a lost response; an unknown outcome is reconciled, not re-filed | Each business operation | Durable operation record; returns-system status lookup or idempotency key (O3) | Atomic claim of the operation; same key on replay; reconcile before any new dispatch | "Pending" status visible; recovery by reconcile job | planned: G07/A4, A5, A7, A11, A13; G17/A4 |
| C6 | R2 | At confirm time, warranty status, line ownership and absence of an open return are rechecked against current data; a stale confirmation is refused | Each confirm | Product database, returns system | Recheck inside the confirm route immediately before dispatch | Customer sees "this changed", must re-propose | planned: G07/A3 |
| C7 | R2, R3 | Text from the customer, the product database or tool results never causes a filing, an out-of-scope read or a disclosure; the structure (no write tool for the model, capability checks in code) prevents it, not an instruction | Every agent run | Code | Tool tiers; `before_tool_callback` capability checks keyed on trusted state | Forbidden call never runs | planned: G07/A9, G11/A1 |
| C8 | R3 | Personal data stays out of logs, traces and evaluation sets unless redacted; a customer's erase request removes sessions and drafts and late retries cannot resurrect them | Logs, traces, sessions, drafts, eval data | Sensitive-data policy (G14, O13) | Logging allowlist; telemetry content capture off; erase route and delete job | Erase confirmed or refused with reason | planned: G11/A2–A4 |
| C9 | R4 | Spend stays under the sponsor's ceiling at the stated volume (placeholder, O7); looping runs, concurrent runs and per-customer overuse are refused | Project and environment | Cloud Billing export; application usage counters | `max_llm_calls`, admission control with per-customer allowance, one active run per customer, maximum Cloud Run instances, operator kill switch (a budget alert only observes) | New sessions refused first; cohort and team told | planned: G10/A1–A5, G13/A3; bill read in the first live week (phase 2) |
| C10 | R4 | When the model, product database, returns system or session store fails, the customer gets an honest message and a contact route; nothing is filed without a stored, confirmed operation | Every failure | Code | Bounded timeouts and retries with a single retry owner; error results from tools | "Can't check right now"; state retained | planned: G06/A2, G07/A6–A7, G10/A2 |
| C11 | R4 | Image, prompt version, model ID, tool-schema hash, eval-set hash and secret versions move and roll back together; a regression fails the gate by exit code | Each release | Release manifest | CI gate; Cloud Run revision rollback | Previous revision serving | planned: G09/A2, G17/A2 |

Deferred contract detail: availability and latency targets are provisional until measured (see Budgets).

## Architecture and decisions

```text
Browser SPA ──HTTPS──> External ALB + Cloud Armor ──(internal LB ingress only)──> Cloud Run: one FastAPI process
                                                                         │  verified principal (Identity Platform token)
                                                                         ├─ ADK Runner in process ──> Vertex AI model (pinned)
                                                                         │     tools: lookup_purchases, get_warranty_status,
                                                                         │            search_policy_text (later), propose_return
                                                                         ├─ /api/returns/{id}/confirm  (not a model action)
                                                                         │     └─ executor: recheck → operation record → returns system
                                                                         ├─ Cloud SQL: ADK sessions + application tables (own schema)
                                                                         └─ Product database (read-only, workload identity)
```

| ID | Enforces | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | C1, C2 | Cloud Run, one FastAPI process serving the SPA, `/api` and the in-process ADK Runner; ADK's own routes never exposed | User chose Cloud Run; one process is the smallest shape for two developers; avoids exposing ADK's unauthenticated server (SB05) | Agent Runtime would move session state to a managed service but adds a gateway hop and migration; GKE adds operations the team lacks | G12/A1 | proposed |
| D2 | C1 | Identity Platform (or the organisation's existing customer login, O4) with bearer tokens sent by `fetch`; ownership via verified `sub` | External users need managed sign-in (SB02); same-origin, no cookies, no CSRF surface | Cookie sessions rejected for CSRF cost | G05/A1–A3 | proposed |
| D3 | C3 | Warranty status is a pure rule function over product fields, unit-tested; the model explains the result and never derives dates | The answer is a business fact; code makes it testable and signable by the policy owner | A pure-prompt answer is cheaper and wrong at boundaries | G04/A1 | proposed |
| D4 | C4, C5, C6 | **Propose, confirm, file** split: `propose_return` writes a draft with a canonical hash; confirm is a backend route the browser calls; the executor re-checks, writes an operation record, then calls the returns system with an idempotency key | A confirmation the model cannot reach is a control; ADK's native confirmation has documented limits for cross-request approval | More code than a single tool with native confirmation | G07/A1–A13 | proposed |
| D5 | C7 | The agent reads untrusted text (customer messages, database free-text) and holds a write tool only to the **draft** table, which has no outside effect; the effectful path has no model access. This removes the trifecta leg | Splitting readers from writers by structure, not prompt | A second agent adds nothing here because the executor is not an agent | G07/A9, G11/A1 | proposed |
| D6 | C2, C3 | Four function tools, each one declaration with primitive parameters, a bounded result dict with status and actionable errors; `customer_id` from trusted state, never an argument | Tool interface is the model's only view; bounded results protect context and cost | MCP/OpenAPI toolsets rejected: no remote tool server is needed | G04/A3, G06/A4 | proposed |
| D7 | C8 | Cloud SQL (PostgreSQL, private connectivity) holds ADK sessions via `DatabaseSessionService` and the application tables (proposals, operations) in a separate schema, with migrations as a job | Sessions must survive restarts and replicas; operation records need transactions | In-memory sessions rejected (restart loses state); Firestore rejected (ADK database service targets SQL) | G17/A4 | proposed |
| D8 | C9, C11 | Pinned model ID chosen from the dated lifecycle table (**not read: `adk-model-and-output-contracts` is not installed here**); pinned ADK version, prompt as versioned code | Behaviour must stay comparable across releases; a retirement is a planned re-baseline | Alias drift rejected | G04/A4, G09/A2 | provisional: model ID and ADK pin open (O12) |
| D9 | C9, R4 | External Application Load Balancer with Cloud Armor rate limiting; Cloud Run ingress `INTERNAL_LOAD_BALANCER` so `run.app` cannot bypass it | Public customer endpoint needs an abuse control in front; floor requires one (SB25 Minimal) | An ALB bills hourly while provisioned (ledger row); direct `run.app` exposure rejected | G12/A2, A4 | proposed |
| D10 | C5 | Durable operation record is the recovery owner; a reconcile job looks up status in the returns system for operations stuck in "dispatched" | A restart or lost response must not re-file | An in-process background task is not a queue; Cloud Tasks only if reconcile latency matters (phase 2) | G07/A5, G17/A4 | proposed |

Versions: ADK and Google specialists were checked against different releases (deploy skill `google-adk==2.8.0`; observability 2.11.0; read from the installed skills' compatibility files). Greenfield, no pin exists: G04 picks one and confirms each interface against it (acceptance item). Nothing was run or fetched, so no provider price, quota, region or model lifecycle fact is verified; each is stated as an open check.

### Model-facing interfaces

| Surface | Interface | Skill and verification |
| --- | --- | --- |
| Instructions | One agent: answer warranty questions from tool results only, never state dates it did not receive, propose returns through `propose_return`, refuse out-of-scope requests; all facts the application knows (customer id, today's date) come from state, not prompt text | `adk-agent-instructions`; rendered-request test |
| Tools | `lookup_purchases` (read), `get_warranty_status` (read), `propose_return` (write-draft); fourth slot reserved for policy text, deferred | `adk-tool-interface-design`; declaration dump, result-size test |
| Output and model | Free text plus a structured status block the UI renders (covered / expired / unknown / proposal); invalid shape gets a bounded repair then an explicit failure | `adk-model-and-output-contracts`; scripted invalid-output test |

## Data and authority

| Data | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | Identity provider; the signed-in customer | Provider / backend verifier | Token validated per request; revocation checked before confirm (SB20) | Per provider policy |
| Purchases, warranty fields | Product data owner; read by the owning customer only | Source systems / read tools | Read at question time and again at confirm (C6) | Not copied; only the answer's cited fields persist in the session |
| Warranty rule | Warranty policy owner (O6) | Developers via review / rule function | Versioned in code; business sign-off per version | Versioned |
| Sessions | The customer | ADK Runner / Runner | Cloud SQL | Retention assumed 30 days (O13); erase route |
| Proposals and operations | The customer; support read access later | Backend only | Cloud SQL application schema; the returns system is authoritative after filing | Audit retention to be set (O13) |
| Telemetry | Operators | Platform | Content capture off; identifiers only | Retention to be set (O13) |
| Evaluation data | Developers and SMEs | Humans | Redacted or synthetic | Per G14 |

Identities: session (a conversation, located by id, never authority), invocation (one run), operation (one confirmed return; the idempotency key). Workload identities: separate service accounts for the serving process, the executor's returns-system credential, the product-database reader and the deployer.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Warranty agent | Customer purchases | Customer text; database free text | Draft write only; no egress tool; no filing tool | Leg removed by structure (D5); scripted-model injection test asserts no filing, no foreign read (G11/A1) |

Tool tiers: read (`lookup_purchases`, `get_warranty_status`), write-draft (`propose_return`), irreversible (filing, executed by the backend executor after the customer's confirm; never a model tool).

#### Web security baseline

Component abbreviations: API = `/api` routes; AG = agent routes; RT = ADK runtime; UI = browser app.

| Rule | Component | Depth now | Proved by (G/A), n/a or deferred |
| --- | --- | --- | --- |
| SB01 | API | Build | G05/A1 |
| SB02 | Identity | Build | G05/A2; live audience check G12/A6 |
| SB03 | AG | Build | G05/A3 |
| SB04 | Records and tools | Build | G05/A4 |
| SB05 | RT | Build | G12/A1 |
| SB06 | API | Build (same origin) | G12/A3 |
| SB07 | API | Build | G12/A3 |
| SB08 | UI | n/a: bearer tokens, no cookies | — |
| SB09 | API | Build | G05/A7 |
| SB10 | UI | Build | G08/A2 |
| SB11 | Uploads | n/a: no uploads in phase 1 (deferred item has a trigger in Later) | — |
| SB12 | Outbound fetch | n/a: no URL-fetching tool or route | — |
| SB13 | Errors | Build | G05/A5 |
| SB14 | Logging | Build | G11/A2 |
| SB15 | Supply chain | Build | G15/A3 |
| SB16 | Secrets | Build | G12/A5 |
| SB17 | Agents with tools | Build | G11/A1 |
| SB18 | Tools with effects | Build | G07/A2 |
| SB19 | Cost and abuse | Build | G10/A1, A3 |
| SB20 | Identity | Build | G05/A6 |
| SB21 | Deployment | Build | G15/A1 |
| SB22 | Whole application | Build | G15/A2 |
| SB23 | Whole application | deferred: before opening beyond the cohort (phase 2) | — |
| SB24 | Whole application | deferred: before opening beyond the cohort (phase 2, outside party) | — |
| SB25 | Public endpoints | Minimal: Cloud Armor rate rule | G12/A4 |

## Budgets and capacity

**Workload (illustrative inputs, owner: sponsor, O7):** cohort of a few hundred customers, about 2,000 conversations a month, about 6 turns each, one model call per turn plus at most one repair and tool-call round trips. Concurrency is about arrival rate × time in flight; measure in G10 and G13 rather than guess.

```text
cost per conversation ≈ (input tokens × p_in + output tokens × p_out) × model calls per conversation
                        + Cloud SQL and Cloud Run work attributable per conversation
monthly ≈ cost per conversation × conversations per month
fixed monthly ≈ Σ idle cost per day (ledger rows) × days
```

`p_in`, `p_out`, region price and idle costs are symbolic: **no pricing page was fetched.** G12 records each provisioned resource's idle cost with the pricing date before creating it.

**Allowances (C9):** `max_llm_calls` per run (value set in G10 from a measured representative run); per-customer daily conversation and run allowance; one active run per customer and conversation; global concurrent-run cap; Cloud Run maximum instances. Enforcement is admission in the application, persisted in Cloud SQL so it survives a restart; control-store failure fails closed for new runs. The operator kill switch is a separate setting outside agent authority and independent of budget resets. A Cloud Billing budget and alert is evidence only. Resources carry `env`, `team` and `app` labels set in deployment code.

**Latency targets (provisional, owner: sponsor; measure first):** time to first meaningful content and time to a complete correct answer are separate targets; a filing is asynchronous-tolerant (status pending is acceptable).

**SLIs (good over total, targets from the first live week):** answered warranty turns without error; confirmed proposals that reach a recorded receipt; time to first content within target. Alerts: error ratio, stuck operations older than the reconcile window.

**Recovery targets (assumed, owner: sponsor, O13):** Cloud SQL RPO under 15 minutes through point-in-time recovery, RTO under 4 hours; the restore into a non-production environment is G17/A1.

## Failure and recovery

Coverage grid (rows are external systems; cells cite acceptance items in the plan):

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model (Vertex AI) | G10/A2 | G10/A2 | n/a: model call has no write effect | n/a: no model-driven writes | n/a: platform-managed workload identity | G10/A2 | G10/A3 | G09/A3 |
| Product database | G06/A2 | G06/A5 | n/a: read only | n/a: read only | G06/A6 | G06/A4 | n/a: read only | G11/A1 |
| Returns system | G07/A7 | G07/A6 | G07/A5 | n/a: one request per operation | G07/A12 | G07/A7 | G07/A4 | G07/A11 |
| Cloud SQL (sessions, operations) | G07/A13 | G07/A13 | G07/A5 | G07/A5 | n/a: platform-managed workload identity | G10/A5 | G07/A4 | G05/A7 |
| Identity provider | G05/A5 | G05/A2 | n/a: read only | n/a: read only | G05/A2 | n/a: provider-managed quota | n/a: stateless verification | G05/A2 |
| Secret Manager | G12/A5 | G12/A5 | n/a: read only | n/a: read only | G12/A5 | n/a: provider-managed quota | n/a: read only | n/a: platform-delivered values |

Action grid (rows are actions that change something):

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| File a return request | G07/A10 | G07/A5 | G07/A3 | G07/A5 | G07/A4 |
| Save a draft proposal | G07/A10 | n/a: single local transaction | G07/A3 | n/a: local transaction outcome known | G07/A4 |

Cross-cutting scenarios:

| Failure window | Customer sees | Retained state and possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Returns system accepts, response lost | "Pending" | Operation record `dispatched`; a request may exist | Reconcile job looks up by key; no re-dispatch (G07/A5) |
| Customer confirms after the product record changed | "This changed, please review" | Draft retained, no filing | Customer re-proposes (G07/A3) |
| Stream or browser dies mid-run | Incomplete turn marked as such | Session persisted; no filing implied | Customer re-opens; status read from the operation record (G08/A4) |
| Process restart or overlapping instances | Possible retry | Operation record and allowances in Cloud SQL | Claim is atomic (G07/A4, G17/A4) |
| Model or judge retirement lands mid-release | None if planned | Pinned IDs and a dated calendar | Re-baseline release (G09/A2) |
| Burst traffic or exhausted budget | New sessions refused with a reason | Existing runs finish | Cloud Armor and admission (G10/A3, G12/A4) |
| Erase request races queued work | Confirmation after delete job | Late writers refused | G11/A4 |
| Document or DB free text carries instructions | Normal answer | No filing, no foreign read | Structure (D5); G11/A1 |
| Rollback | Previous revision serves | Release unit moves together | G17/A2 |

The WAF checks (reliability, cost, operations, performance) were not run beyond the contracts above; product-level recommendations come from the Google WAF skills when installed (G12, G17).

## Verification and implementation handoff

Tiers: offline (scripted model, fake product DB and returns system), local integration (real process restart, real sockets), live on staging with masked data and the returns system's test target, release (rollback, restore). Every critical contract is cited by a goal in the plan's implementation map; none is yet evidenced. Outcome claims (fewer contacts, faster returns) are hypotheses until phase 2 measures a baseline.

Release bundle: image digest, prompt version, model ID, tool-schema hash, eval-set hash, secret versions in one manifest; promotion gate is the evaluation run's exit code plus audits in `make check`.

Implementation plan: [docs/plans/warranty-returns.md](../plans/warranty-returns.md).

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner / evidence | Blocks |
| --- | --- | --- | --- | --- |
| O1 | Accept cohort launch at pilot depth in phase 1, with SB23/SB24 before opening wider; or require full production depth for launch | Sets phase 1 scope and the accepted-risk owner; full depth does not fit six weeks | Sponsor | G18, G19, phase 2 |
| O2 | Product database engine, access path, freshness, masked staging copy | Tool design, IAM, cost | Data owner, G03 | G06 |
| O3 | Returns system: API, idempotency key support, status lookup, what a return triggers (refund, label) | Idempotency vs reconcile-only (C5); a money effect raises depth | Returns owner, G03 | G07 |
| O4 | How customers sign in and map to purchases (existing login, or order number plus email) | C1 and C2 could change fundamentally | Identity owner, G03 | G05 |
| O5 | Residency, jurisdiction, region | Region, transfer assessment | Counsel, G14, `gcp.resourceLocations` in G02 | G02, G14 |
| O6 | Who owns the warranty rule; are policy documents unstructured (would add retrieval) | C3 authority; scope | Policy owner, G03 | G04 sign-off |
| O7 | Spend ceiling and volume | C9 numbers | Sponsor | G10 |
| O8 | Human hand-off route when the agent cannot answer | C10 failure outcome (assumed: a contact link, no ticket creation) | Support lead | G08 |
| O9 | Languages and channels (assumed English, web) | Evaluation, UI | Sponsor | G09 |
| O10 | Who is on call after launch; start date and holidays | Operations, calendar | Sponsor | G17, G18 |
| O11 | Pen test lead time and whether cohort customers count as "external users" for SB24 | Go-live date | Security owner | G19 |
| O12 | Model ID and ADK pin | D8 | G04 | G04 |
| O13 | Retention for sessions, proposals, operations, telemetry; RPO and RTO | Erasure, restore goals | Counsel and sponsor | G11, G17 |

No decision above is user-accepted. Design review is not complete: contracts have planned checks but no run evidence.
