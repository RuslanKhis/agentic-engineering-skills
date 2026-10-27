# System design: warranty answers and return requests (ADK on Cloud Run)

Status: **draft**. Nothing here is user-accepted yet. The request was a non-interactive design and plan, so every scope-gate question is answered by an assumption (table below) and every decision that rests on one is provisional. The plan is `docs/plans/warranty-returns.md`; capacity, finish range and risks live there.

No repository, discovery brief or practice profile exists. The use case was given, not chosen through discovery; its outcome measure and baseline are unknown (O7).

## Purpose and constraints

**Journey.** A signed-in customer asks "is my X still under warranty, and what does it cover?". The agent finds the customer's own product in the product database and answers from the record. If the customer wants to return it, the agent proposes a return request (product, reason, remedy). The customer confirms on a card the server renders; the backend files the request once in the return system and shows its reference.

**Friction and outcome.** Today the customer reads policy pages or contacts support (assumed; no baseline given, O7). The outcome to improve is warranty questions resolved without an agent contact and return requests filed correctly the first time. Neither has a baseline yet.

**Model decides:** which tool to call, how to phrase a grounded answer, whether the customer's words amount to a return intent. **Code controls:** identity, which records are in scope, warranty status and eligibility, the confirmation, the write, retries, limits.

**Non-goals (phase 1):** refunds or payments, inbound email or voice, other product lines than those in the product database, proactive messages, a multi-agent design.

### Assumed answers (nobody could answer; every dependent decision is provisional)

| Scope-gate question | Assumed answer | Decisions that depend on it |
| --- | --- | --- |
| Deadline and afterwards | Six weeks from Mon 2026-11-02 (30 working days, to 2026-12-11); launched and continued | Cut line in the plan; phase 2 |
| Who builds, hours, familiarity | Two developers, about 4.8 focused hours a day each (8 h at focus 0.6); new to ADK, comfortable with GCP; ×1.5 on ADK goals | Every estimate; G02 |
| Money | Unknown; a sponsor-set monthly ceiling is needed (O4) | C8, D8, G10, G11 sizing |
| Users and judge | External customers, daily. Judged by a business sponsor plus security and privacy reviewers, who read a go-live memo and evidence | G01, G13, G18 |
| Own web interface, reach, handover | A baseline single-page app from [web application defaults](../../.claude/skills/adk-system-designer/references/web-app-defaults.md), reachable on the internet behind customer sign-in; later embedded in the organisation's portal (O8); other developers will continue it | D1, D9, web security tiers 1–6 |
| Data and effects | Real personal data (name, contact, purchase, product serial) in production; staging uses synthetic data only. Effect: files a return request, which the return system may act on (labels, notifications, assumed) | Floor, C3–C5, C7, governance goal |
| Reviews | Go-ahead before the build (G01); go-live approval (G18) for the business audience, with security and privacy reviewers reading the evidence directly (O11); results review after launch is phase 2 | Presentation goals, W7 |
| Contract or lock-in | No statement of work; no lock-in concern, so no portability goal | Nothing |
| Hosting | Cloud Run (given) | D1 |
| Organisation foundation | A landing zone exists; the project, billing link, IAM grants and policy exceptions are an administrator's calendar waits (W1), not team hours | G11, W1 |
| Jurisdictions and residency | Unknown (O5) | Model and database regions, D7, G13 |

### Profile and depth

**Production.** Real customers and real data set the risk, and the floor and tiers follow. Six weeks and two people do not carry every production control, so the plan cuts the later part of production (ramp to 100 percent, full ASVS Level 2 review, rollout pack, tuning) into phase 2 with triggers, and keeps the floor. The user should confirm or move that cut line; phase 1 ends in a controlled launch to a small share of customers, not general availability.

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Identity and per-customer scope | Build | none; at the floor |
| Grounded answers, evaluation | Build: labelled set, gate in CI | New product line or policy change |
| Confirmed write, idempotency, reconcile | Build | New remedy type (refund or payment) |
| Sensitive data, retention, erasure | Build | New data class or jurisdiction |
| Prompt injection and agency | Build: structural split, adversarial suite | New tool or new untrusted source |
| Budgets and abuse | Build: per-customer allowance, kill switch, cost contract | Volume above the assumed range |
| Observability | Build: traces, SLIs, alerts on the contracts | First incident |
| Release engineering | Build: gate, manifest, canary, rollback rehearsal | Model retirement date |
| Web security | Tiers 1–6, with SB23's ASVS Level 2 review deferred | Ramp past 25 percent of customers |
| Hosting | Cloud Run, load balancer, Cloud Armor, Cloud SQL | Measured latency or cost targets |
| Memory beyond sessions | Defer: none needed for the journey | A requirement for cross-session recall |
| Performance tuning, model-mix review | Defer until measured | First bill and first load data |

**Floor kept:** no secrets in source, prompts or logs; a spend stop that acts without a person (C8); a human confirms the one outside-visible effect (C3); real data scoped to the journey and out of logs (C7); nothing reachable without sign-in and ADK's own routes never exposed; pinned model ID.

**Graduation conditions** (what phase 2 must add before general availability): ASVS Level 2 review, ramp gates on measured SLIs, support-team rollout pack, first live bill read against C8, results review.

## Requirements and contracts

| ID | Requirement | Need it serves | Status |
| --- | --- | --- | --- |
| R1 | A customer gets correct warranty answers about their own products | Fewer contacts, trust | assumed |
| R2 | Every warranty statement comes from the product database, never from the model | Correctness | assumed |
| R3 | A return request is filed only on the customer's explicit confirmation, once, for the right product | No accidental or duplicate returns | assumed ("once the customer confirms" is stated) |
| R4 | Customer data is protected and not exposed to other customers, logs or tools beyond need | Privacy, law | assumed |
| R5 | Spend and abuse are bounded | Production cost | assumed |
| R6 | The service is operable and recoverable by a small team | Production | assumed |

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R4 | Every read and write the agent causes concerns only the verified customer; the customer key comes from the verified token and never from a model argument or request body | Per customer, per request | Identity provider token; the product database's customer key | Auth dependency sets trusted session state; tools read the key from `tool_context`; every query filters by it; the confirm endpoint and executor re-derive it at the effect | Request denied or "not found" (same body as unknown); no model call; denial logged | planned: two-customer denial tests, offline and local, G04/A3, G04/A4, G05/A5, G07/A4 |
| C2 | R1, R2 | Every statement about warranty status, expiry or coverage is rendered from a product record fetched in this turn, carries the record ID and as-of date, and the status is computed by code | Per answer | Product database record | Tool returns computed status and evidence ID; output schema requires them; the application validates the answer against the turn's tool results before release | "I can't find that product" or a handoff offer; never an invented term | planned: scripted-model cases offline G05/A1–A3, A8; labelled evaluation G06/A1–A3 |
| C3 | R3 | A return request is filed only by an authenticated customer action on a stored proposal; the action carries the proposal ID and hash; it is refused when the hash, ownership, eligibility or expiry no longer holds; the model holds no tool that files | Per proposal | The stored proposal row and the product database at the effect | Proposal tool writes a draft only; a separate confirm endpoint runs the executor, rechecking at the effect | Refusal with the reason; the customer is offered a fresh proposal | planned: offline and local, G07/A1–A3, A6–A8 |
| C4 | R3 | Eligibility (within warranty, product class, no open return, allowed remedy) is decided by deterministic code from current records, at proposal and again at filing | Per proposal | Product database; return system for open returns | Eligibility function in the application, not the prompt | Proposal not created, or confirm refused, with a reason code | planned: offline G07/A3, A9; rules pending O6 |
| C5 | R3 | One confirmed proposal produces at most one return request in the return system; an uncertain outcome is reconciled by lookup before any resend; the customer sees a reference only after the return system returned one | Per operation ID | Return system record, found by idempotency key | Durable operation record with unique constraint; idempotency key from operation ID; reconcile worker; status endpoint renders receipts | Status `unknown` shown as "we are checking", a support-queue entry, no second request | planned: local with a sandbox, G07/A5, A10, A11; G08/A1–A3, A7; depends on O2 |
| C6 | R3, R4 | No agent both reads untrusted content and holds an unconfirmed write or egress tool; customer text and database free-text fields are data | The one agent | Design | The only model-callable write is a draft with no external effect; filing is outside the model's reach; tool results are bounded typed projections | The injected instruction has no effect; the forbidden call does not run | planned: scripted-model adversarial tests offline, G05/A4, G07/A1, G07/A8, G14/A2 |
| C7 | R4 | Prompts, replies, tokens and personal data are absent from logs, traces and metrics; sessions and drafts expire after the retention period (assumed 30 days, O5) and are erased on request; card numbers typed into the chat are refused before storage or model | Per customer, per store | Retention policy from governance (G13) | Logging filter and exporter gates set at the single telemetry owner; scheduled deletion job; input detector before storage and model | Message refused with an explanation; nothing stored | planned: local, G10/A1–A3, G12/A2, G11/A9 |
| C8 | R5 | The application spends under a stated ceiling at a stated volume: `max_llm_calls` per run, a per-customer daily allowance, one active run per customer, maximum instances, an operator kill switch outside agent authority; the model project has a quota backstop. Ceiling and volume: provisional, O4 | Per run, customer, day, project | Cloud Billing export (evidence); admission store (enforcement) | Admission control in the application before the model is called; fail closed when its store is unavailable; budget alert is observation only | New runs refused with a message; read-only status still works; owner alerted | planned: local G10/A4–A8; hosted G11/A5; first live bill is phase 2 |
| C9 | R1, R6 | When the model, product database, session store, identity provider or return system fails, the customer sees a bounded honest message; nothing is stated as filed unless the return system confirmed; the system fails closed on authority checks | Per request | Receipts from each system | Timeouts inside the request deadline, one retry owner, typed failure shapes | Customer sees a retry or handoff message; state remains consistent | planned: offline and drills, G05/A2, A6, A7, A10, A11; G08/A3, A4; G15/A5, A6 |
| C10 | R6 | One release unit (image digest, prompt version, model and judge IDs, tool schema hash, eval-set hash, secret versions) is recorded, gated by the evaluation, and rolls forward and back together | Per release | Release manifest | CI gate fails by exit code; manifest has no alias; Cloud Run revisions with traffic split | Promotion blocked; previous revision still serving | planned: hosted rehearsal G12/A4, A5, A7; G11/A7 |

## Architecture and decisions

```text
Customer browser ──► External ALB + Cloud Armor ──► Cloud Run: warranty-agent (single process)
   (CIAM sign-in)        (ingress: LB only)           FastAPI: SPA assets, /api/*, auth dependency
                                                       Runner in-process ─► LlmAgent ─► Gemini (Vertex, region O5)
                                                          tools: list_my_products, get_warranty, propose_return(draft)
                                                       POST /api/returns/{id}/confirm ─► executor ─► Return system API
                                                       reconcile worker (Cloud Scheduler → private endpoint)
   Stores: Product DB (read only, existing) · App DB Cloud SQL (sessions, proposals, operations, usage)
   Platform: Secret Manager · Cloud Logging/Trace · Cloud Build → Artifact Registry → revisions
```

Trust boundaries: browser (untrusted), the agent's model output (untrusted until validated), product database free-text and customer text (data), the return system (authority for filed requests). Identities: end customer (token), serving service account (workload identity, no keys), deployer (pipeline), reconcile caller (scheduler identity).

| ID | Enforces | Design choice | Reason | Tradeoff and alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | C1, C8, C10 | One Cloud Run service running FastAPI with the Runner in process; ADK's own routes are never mounted publicly; ingress limited to the load balancer; public edge is an external ALB with Cloud Armor | Cloud Run is given, and one process keeps identity, run lock and confirm endpoint in one trusted place; the default `run.app` URL must not bypass the armor | Agent Runtime would host the agent with managed sessions, but the confirm endpoint, auth and limits still need an application in front, so two services for a two-person team. GKE is operational weight for no stated need | G11/A2: default URL refused, ADK paths return nothing (G09/A5) | proposed |
| D2 | C2, C6 | One `LlmAgent`, three tools: `list_my_products`, `get_warranty` (read tier) and `propose_return` (draft tier). Ordinary code for everything else | Fixed ordering of eligibility and filing is not a language problem; one agent has no extra boundary to defend | A reader/writer pair of agents: rejected, since the writer here is not an agent at all | G05/A9 declaration dump and rendered-request test | proposed |
| D3 | C1, C2, C6 | Product database accessed with a read-only identity through typed projections (columns named, free-text columns excluded or length-bounded); the customer key is a trusted argument from state; warranty status computed in code from dates | Removes the model from dates and ownership; shrinks the injection surface | Less flexible answers than letting the model read raw records; more mapping work | G05/A1, A4, A5 | proposed; access path pending O1 |
| D4 | C3, C4, C6 | Proposal and confirmation are separate: the model only creates a draft (stored, hashed over customer, product, reason, remedy, eligibility snapshot, 30-minute expiry, assumed); the UI renders the confirm card from the stored draft; the customer's click calls the confirm endpoint | A sentence typed in chat cannot file anything, so injected text cannot either. ADK's native tool confirmation is not used because its fit with a streamed, multi-replica, reloadable UI needs checking and the stored draft needs to exist anyway | Extra endpoint and UI state instead of one tool; the customer cannot confirm by typing "yes" | G07/A1, A2, A6, A8; G09/A7 | proposed |
| D5 | C5, C9 | Operation record in the app database with a unique key per proposal and a state machine (`pending`, `sent`, `filed`, `rejected`, `unknown`); idempotency key to the return system; reconcile worker looks up by key before any resend | Provider-backed replay is the only safe recovery from a lost response | If the return system lacks an idempotency key or lookup, C5 weakens to "own table is the system of record and fulfilment reads it"; decided in G03 (O2) | G08/A2, A3, A7 | provisional on O2 |
| D6 | C1, C9 | Customer sign-in through the organisation's customer identity provider (Identity Platform or the existing one, O3); a library verifies signature, audience, issuer, expiry; the server overwrites `user_id` on every ADK call; revocation checked before confirm | Managed sign-in; session ID only locates a conversation | A custom login: rejected | G04/A1–A6 | provisional on O3 |
| D7 | C1, C2, C7 | Sessions in Cloud SQL (PostgreSQL) via `DatabaseSessionService`; the same instance holds application tables, kept apart from ADK's; model ID chosen in G02 from the dated lifecycle table that `adk-model-and-output-contracts` ships (not installed here, so no ID is named); the model region follows O5 | Database transactions give the unique operation constraint; sessions need persistence across replicas | A separate store for operations is more isolation than two people can run; Firestore is credible but gives up the unique constraint with the same transaction | G09/A9, G07/A5, G15/A4 | provisional |
| D8 | C8 | Admission in the app database before any model call: per-customer daily counter, one active run lock, global kill switch read from a store the agent cannot write; `max_llm_calls` on the `RunConfig`; model-project quota as backstop | A budget alert only notifies; the stop must act without a person | A shared admission store adds a failure mode, so it fails closed | G10/A4–A8 | proposed |
| D9 | C3, C7 | Baseline SPA served by the same service: text and sanitised markdown only, bearer token via `fetch`, confirm card from stored draft | Same origin removes CORS and cookie risk | Embedding in the portal is phase 2 (O8) | G09/A3, A6, A7 | proposed |
| D10 | C7, C10 | One telemetry owner per process; prompt and response content capture off in deployed environments; trace, invocation and session IDs on every hop; SLIs below; eval gate in Cloud Build | Defaults capture prompts, which would put customer data in traces | Debugging needs the session store, not traces | G12/A1–A4 | proposed |

### Model-facing interfaces

| Surface | Interface | Implementing skill and verification |
| --- | --- | --- |
| Instructions | Scope (warranty questions and return intent only), refusal to guess, handoff wording; customer identity and dates stay in code | `adk-agent-instructions`; rendered-request test (G05/A9) |
| Tools | Three tools, primitive parameters, bounded result dicts with a status and actionable errors; `propose_return` returns a draft ID and display data, never filing status | `adk-tool-interface-design`; declaration dump (G05/A9) |
| Output and model | Schema with `answer`, `evidence_ids`, `as_of`, and a first-class `cannot_answer` shape; bounded repair budget; pinned model ID with retirement date | `adk-model-and-output-contracts`; scripted invalid-output test (G05/A3, A8) |

ADK pin: working assumption is the baseline the deploy specialist was checked against (`google-adk==2.8.0`, September 2026), not a fresh lookup; G02/A3 confirms against the chosen pin and records any move to 2.12 or later.

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Product, purchase and warranty terms | Product database owner; customer sees own rows | Read only by the serving identity | Fetched each turn; as-of shown | Not copied; no cache in phase 1 |
| Session events | App database; the owning customer | Runner (via `DatabaseSessionService`) | n/a | Assumed 30 days; deleted by job and on request |
| Return proposal | App database; the owning customer | Proposal tool writes; confirm endpoint reads | Eligibility snapshot, rechecked at the effect | Expires in 30 minutes; purge after retention |
| Return operation and receipt | App database mirrors the return system | Executor, reconcile worker | Return system is authoritative | Retention per governance (G13) |
| Usage counters, kill switch | App database | Admission control; operator | n/a | Daily reset; operator flag independent of resets |
| Logs and traces | Cloud Logging and Trace | One telemetry owner | No content | Default retention; custom retention only with an owner |

Identities: session (conversation, locates only), invocation (one run, `max_llm_calls`), business operation (proposal ID, survives retries and restarts).

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| warranty agent | Yes: the customer's products | Yes: customer messages, product-database free text | A draft write with no external effect; filing is not model-callable | A leg removed: the agent has no filing or egress tool (C6); injection tests assert it (G14/A2) |

Tool tiers: read (`list_my_products`, `get_warranty`), draft (`propose_return`, no confirmation, no external effect), irreversible (filing: code only, customer click). No code executor. No outbound fetch tools.

#### Web security baseline

Components: SPA, `/api` routes, agent run route, confirm endpoint, ADK runtime, Cloud Run, load balancer. Tiers 1–6 apply (production). Each rule is recorded here only.

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | `/api` routes | Build | G04/A1 |
| SB02 | Identity | Build | G04/A2 |
| SB03 | Agent routes | Build | G04/A3 |
| SB04 | Records and tools | Build | G04/A4 |
| SB05 | ADK runtime | Build | G09/A5, G11/A2 |
| SB06 | API configuration | Build | G09/A6 |
| SB07 | API configuration | Build | G09/A5 |
| SB08 | Browser credentials | n/a | n/a: bearer tokens sent by fetch, no cookies, so no CSRF surface |
| SB09 | API inputs | Build | G09/A2 |
| SB10 | Browser app | Build | G09/A3 |
| SB11 | Uploads | n/a | n/a: the journey has no uploads |
| SB12 | Outbound fetch | n/a | n/a: no tool or route fetches a user or model supplied URL; return system host is fixed configuration |
| SB13 | Errors | Build | G09/A4, G04/A6 |
| SB14 | Logging | Build | G10/A1 |
| SB15 | Supply chain | Build | G02/A1 |
| SB16 | Secrets | Build | G02/A1, G08/A6 |
| SB17 | Agents with tools | Build | G05/A4, G14/A1 |
| SB18 | Tools with external effects | Build | G07/A2 |
| SB19 | Cost and abuse | Build | G09/A1, G10/A4 |
| SB20 | Identity | Build | G04/A5 |
| SB21 | Deployment | Build | G15/A1 |
| SB22 | Whole application | Build | G15/A2 |
| SB23 | Whole application | Minimal | G14/A1, G14/A2 for the threat model and adversarial suite; deferred: ASVS Level 2 review (G20) before ramp past 25 percent |
| SB24 | Whole application | Build | G15/A3 |
| SB25 | Public endpoints | Build | G11/A4 |

## Budgets and capacity

Workload (illustrative, no figure was supplied, O4): 20,000 conversations a month, about 6 model calls each (read tools plus one answer), `max_llm_calls` per run set at 12; peak concurrency from arrival rate × time in flight, measured in G15/A7.

Provisional targets (assumed, to be measured): first streamed text p95 3 s; complete answer p95 12 s; confirm to reference p95 8 s; availability 99.5 percent monthly; session store RPO 24 h, RTO 4 h; operation records RPO 5 minutes (point-in-time recovery), RTO 4 h.

Cost (C8): `cost per conversation ≈ (input tokens × p_in + output tokens × p_out) × model calls + database and egress work`, `monthly ≈ that × conversations + fixed`. Prices not looked up (no network); `p_in`, `p_out` and the idle rates below are placeholders to fill in G11/A1 and G02, with the pricing date. Fixed part: while-provisioned rows of the resource cost ledger (ledger rows dated 21 October 2026): Cloud Run minimum instance (idle rate), Cloud SQL instance with HA and backups, external ALB forwarding rule, Artifact Registry images, Secret Manager versions. All carry labels `env`, `team`, `app`, set in deployment code. Stop: D8. Evidence: first live bill read against C8 in phase 2 (G21).

Environments: staging scales to zero, single-zone database, synthetic data only. Production: regional database, minimum one instance.

## Failure and recovery

Coverage grid, one row per external system:

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model endpoint | G05/A6 | G05/A8 | n/a: model calls change no state | n/a: model calls change no state | G15/A5 | G05/A6 | G09/A1 | G05/A8 |
| Product database | G05/A7 | G05/A10 | n/a: read only | n/a: read only | G05/A11 | G15/A7 | n/a: read only | G05/A4 |
| App database (Cloud SQL) | G15/A6 | G07/A5 | G07/A10 | G07/A11 | G15/A6 | G15/A7 | G07/A5 | n/a: typed fields validated |
| Return system | G08/A3 | G08/A4 | G08/A2 | G08/A2 | G08/A6 | G08/A5 | G08/A7 | G08/A9 |
| Customer identity provider | G04/A6 | G04/A2 | n/a: verification only reads | n/a: verification only reads | G04/A5 | G04/A6 | n/a: stateless verification | G04/A2 |
| Secret Manager | G11/A7 | G11/A7 | n/a: read at startup | n/a: read at startup | G08/A6 | n/a: startup reads only | n/a: read only | n/a: values never rendered |

Action grid:

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| File a return request | G07/A7 | G08/A2 | G07/A3 | G08/A3 | G07/A5 |
| Create a return proposal (draft) | G07/A4 | n/a: single row insert | n/a: a draft needs no confirmation | G07/A10 | n/a: duplicate drafts have no external effect |

Cross-cutting scenarios:

| Failure window | User-visible outcome | Retained state and possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Return system accepts, response lost | "We are checking your request" | Operation `unknown`; a request may exist | Reconcile worker looks it up by key; support queue after a threshold; support owns manual closure |
| Process restarts between proposal and confirm | Card still valid until expiry | Draft persisted | Customer confirms; executor rechecks |
| Browser disconnects mid-answer | Nothing marked complete | Partial text not stored as a finished turn | Customer resends; one active run lock released on close |
| Customer's warranty changes or product is returned while the card is open | Confirm refused with reason | No request | Fresh proposal if still eligible |
| Kill switch or budget exhausted | New runs refused | Existing operations still reconcile | Operator clears the switch; allowance resets daily |
| Bad release | Canary shows burn or eval regression | Previous revision still ready | `adk-release-engineering` rollback: image, prompt, model, schema, secrets together |
| Erasure request | Sessions and drafts removed | Operation receipts retained per policy | Privacy owner (G13) |

## Verification and implementation handoff

Checks run in four tiers: offline deterministic (scripted model, fake return system, real policy code), local integration (process restart, real database, Playwright journey, sandbox return system), bounded live (Vertex and the sandbox, with declared request and cost limits), and hosted (staging, drills, canary). No check has run; every Evidence cell is `planned`.

Observability (D10), SLIs as good/total ratios tied to contracts, targets from the first measured week, none at 100 percent: answers completed without an error shape (C9); answers passing the sampled grounding check (C2); returns confirmed that reach `filed` or a documented `rejected` within 10 minutes (C5); `unknown` operations older than 15 minutes, which must be zero (C5, alert); p95 latency (budgets). Telemetry owner: the service process, one provider; content gates off (C7). Release bundle: image digest, prompt version, model and judge IDs, tool schema hash, eval-set hash, secret versions, recorded in a manifest by G12. Gate: the evaluation set in Cloud Build fails by exit code. Rollback unit: the revision with its bundle; the previous one stays ready until the canary has soaked.

### Implementation routes and Google product skills

| Choice | Primary skill | Google product skills (`google/skills:<name>`) |
| --- | --- | --- |
| D1, D6 hosting and identity | `deploy-adk-on-google-cloud`, `adk-fastapi-backend`, `adk-tool-auth-and-secrets` | `cloud-run-basics`, `google-cloud-global-frontend-configuration`, `iam-helper-for-policy-management`, `gcloud` |
| D7 sessions and app database | `adk-memory-architecture` for sessions; `safe-api-tool-calls` for operations | `cloud-sql-basics` |
| D4, D5 confirm and write | `safe-api-tool-calls`, `adk-operational-guardrails` | none |
| D10 telemetry and alerts | `adk-agent-observability`, `adk-release-engineering` | `cloud-run-alert-configuration`, `google-cloud-slo-alert-configuration`, `cloud-build-basics`, `cloud-logging-configuration-basics` |
| Production pillars | the team | `google-cloud-waf-reliability`, `-security`, `-cost-optimization`, `-operational-excellence` |

These names come from the designer's handoff table, read from the published catalogue on 21 October 2026. Google's router `finding-google-skills` is installed, but I did not run it in this session (no network, and a design-only task), so each name is **unconfirmed against the live catalogue**. Confirm every name through the router before a goal first uses it. None of these product skills is installed; installing them and the specialists the plan names is a setup step. The design records the need and runs no recipe.

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner or evidence | Blocks |
| --- | --- | --- | --- | --- |
| O1 | Product database engine, access path (direct or an API), freshness, free-text columns | D3 and C2 mechanics; injection surface | Database owner; G03 | G05 |
| O2 | Return system: API, idempotency key, status lookup, sandbox | C5 and D5 hold or weaken | Return-system owner; G03 | G07, G08 |
| O3 | Customer identity provider and the mapping from token to the product database's customer key | C1 and D6 | Identity owner; G03, W3 | G04 |
| O4 | Volume, monthly ceiling, who owns the budget | C8 numbers, sizing, the stop thresholds | Sponsor | G10 numbers, G11 sizing |
| O5 | Jurisdictions, residency, retention period; effective org policies (`gcp.resourceLocations`, `sql.restrictPublicIp`) | Model and database regions, model choice, C7 | Privacy and platform owners; G13, G11/A6 | G02 model choice, G11 |
| O6 | Eligibility and remedy rules (warranty periods, reason codes, repair, replace, refund) | C4 function | Warranty policy owner | G07/A9 |
| O7 | The outcome measure and its baseline | Whether the benefit can be claimed | Sponsor; G03/A4 | G18 claims |
| O8 | Standalone SPA or the organisation's portal | G09 size, SB07, phase 2 | Product owner | G09 scope |
| O9 | Who is on call and who handles `unknown` returns | G17, alert routing | Operations lead | G17 |
| O10 | Team hours and start date (4.8 h a day each, 2026-11-02) | Every figure in the plan | Engineering lead | Finish range |
| O11 | Does the security or privacy review need its own technical deck | Extra presentation goal | Reviewers | G18 |

Design completion and implementation authorization are separate facts: nothing is approved, and no cloud action has been authorised.
