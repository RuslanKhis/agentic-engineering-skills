# System design: Card Dispute Assistant

Status: **draft**. Written in one pass without the user available. Every row of
the Assumed answers table below is unconfirmed, and the decisions that depend on
it are marked *provisional*. No decision in this document has been accepted by
the user yet.

Implementation plan: [docs/plans/card-dispute-assistant.md](../plans/card-dispute-assistant.md)

## Assumed answers

The request fixed the profile (production, external customers, regulated EU
bank), the team (six engineers plus a security reviewer), the deadline (general
availability in four months) and the effect (opening dispute cases in core
banking). The rest is assumed.

| # | Question I would have asked | Assumed answer | Decisions that depend on it (provisional) |
| --- | --- | --- | --- |
| A1 | Which channel: existing mobile/online banking app, public website, contact centre? | Chat panel inside the existing authenticated mobile and web banking app, behind the bank's existing API gateway. No anonymous access. | D1, D8, G08 |
| A2 | How do customers authenticate, and what reaches the backend? | Existing bank IdP (OIDC) with PSD2 strong customer authentication at login. The gateway forwards a signed access token whose subject maps to one customer ID. | D2, G02 |
| A3 | What does core banking expose for disputes: API, idempotency key or client reference, lookup by reference, sandbox? | A synchronous REST/SOAP "create dispute case" operation through the bank's integration layer. It accepts a client reference but **its deduplication and lookup semantics are unknown**. A test environment exists. | D6, D7, G00 (discovery), G05 |
| A4 | Who decides eligibility, liability, provisional credit and chargeback reason codes today? | The dispute operations back office and existing core-banking rules. The assistant only opens a correctly categorised, complete case. It never decides or promises a refund. | D4, D5, Guarantees I4/I5 |
| A5 | Which dispute types are in scope at GA? | Card (debit and credit) transactions settled or pending in the last 13 months. Categories: unauthorised/fraud, duplicate charge, wrong amount, goods or service not received, cancelled subscription still charged, refund not received. Out of scope: ATM cash disputes, SEPA/credit transfers, business cards. | D4, G03 |
| A6 | Languages at GA? | One language at GA (the bank's primary customer language, written here as "L1"). A second language follows in phase 2. | G03 estimate, cut line |
| A7 | Evidence uploads (receipts, screenshots) at GA? | Not at GA. Back office requests evidence through its existing channel. Uploads arrive in phase 2 behind a quarantined reader. | D9, security posture, phase 2 |
| A8 | Volume and peak? | ~5,000 assistant conversations/month at GA, peak ~30 concurrent conversations. Illustrative only, to be replaced by the bank's dispute-volume data. | Budgets, G13 |
| A9 | Cloud footprint and regions? | Bank already runs regulated workloads on Google Cloud: an organisation with VPC Service Controls, Interconnect to the on-premise integration layer, an approved EU region (written here as `europe-west3`), and Terraform owned by a platform team. | D3, D10, G01, G11 |
| A10 | Retention of conversations? | Raw ADK session events are kept 90 days. The confirmed dispute summary becomes part of the case record under the bank's records policy. **Requires DPO/records-management confirmation.** | D11, G06 |
| A11 | Team familiarity and focus? | Experienced Python and GCP engineers, new to ADK. One of the six is the app's frontend engineer. Security reviewer ~25% time. About 0.6 focus factor. | Capacity, estimates |
| A12 | Budget for models and cloud? | No hard figure given. Assumed: a monthly model and cloud ceiling set by the product owner before the pilot, enforced by application allowances plus billing alerts. | D12, G09 |
| A13 | Compliance gates before GA? | DPIA (GDPR Art. 35), the bank's model-risk/AI governance sign-off, EU AI Act Art. 50 transparency (customers told they are talking to AI), DORA ICT third-party register entry for the model provider, an external penetration test. These run on the bank's calendar, not the team's hours. | G15, timeline |
| A14 | Human handoff? | "Talk to a person" is always available. It hands off to the existing secure-messaging or contact-centre queue with the conversation summary. | D8, G08 |

## Purpose and constraints

**Journey (running example).** Anna opens her banking app and sees
`ACME*DIGI 8841 €89.99` that she does not recognise. Today she either phones
the contact centre (queue, then an agent fills a form) or fills a static web
form that asks her to pick a reason code she does not understand. Disputes
arrive miscategorised or missing facts. Back office then contacts her again,
and scheme deadlines are at risk. **With the assistant**, Anna taps "Something
wrong with a payment?". The assistant shows her recent card transactions
(only hers) and helps her identify the charge. It explains what the merchant
descriptor usually means, and through a few questions establishes whether
she made the payment. Here she did: she cancelled a subscription last month.
It records a structured dispute draft and shows a confirmation card: transaction,
amount, category "cancelled subscription still charged", her statement and
the cancellation date. When she presses **Confirm**, exactly one dispute case
is opened in core banking and she gets the case reference. If she had not made
the payment, the assistant would point her to the app's existing "freeze card"
control and open a case marked unauthorised. Fraud operations then handle it
under their existing PSD2 process.

**Outcome to improve (hypothesis, unmeasured).** Higher first-time-right
dispute cases (correct category, required facts present) and fewer contact-
centre calls for disputes, without increasing complaint rate or back-office
rework. Baseline needed from dispute operations: current rework rate and
call volume (open decision O7).

**Non-goals.** Deciding eligibility, liability or provisional credit. Promising
outcomes. Blocking cards. Changing any record other than creating a dispute
case. Disputes on non-card payments. Advice on unrelated products.

**What the model contributes:** interpreting the customer's account of what
happened, helping identify the transaction, and choosing a category from a closed
list with the facts that category needs. **What code controls:** who the
customer is, which transactions they may see, eligibility windows and
deadlines, duplicate-dispute checks, the confirmation, the write, its retry
and reconciliation, and all outcome messages after confirmation.

**Repository facts observed:** the repository is empty apart from skill files
(`git ls-files` at commit `1450f0f`). Everything below is proposed.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | GA in four months from start (assumed start 2026-10-12 → GA target ~2027-02-08); continued and operated afterwards |
| People and hours | Six engineers full time (assumed new to ADK, experienced with Python/GCP), one security reviewer ~25%; the team runs it after GA with the bank's SRE on-call (assumed) |
| Money | Not stated; ceiling to be set by product owner (A12) |
| Users or judge, and what they read | External retail customers of an EU bank, using the running service; dispute operations staff read the cases it opens; security, DPO and model-risk reviewers read this design |
| Data touched and effects allowed | Personal financial data (GDPR personal data, banking secrecy); one effect: create a dispute case in core banking, which starts a regulated process with money consequences |
| Delivery profile | **Production service**: external customers, regulated personal data, and a write that starts a money-relevant process. Every concern is built, with depth set below. |

Depth per concern:

| Concern | Depth now (to GA) | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: labelled development set with dispute-ops SMEs, CI evaluation gate | Second language, new category, model migration |
| Identity and per-customer scope | Build: verified token → customer ID in middleware; tools take no customer argument | n/a (already maximum) |
| Secrets and credentials | Build: workload identity, no API keys, Secret Manager for core-banking client cert, rotation | n/a |
| External writes | Build: durable operation record, idempotent submission, reconciliation, manual queue | Core banking adds a status lookup → automate more reconciliation |
| Sensitive data | Build: PAN/IBAN detection before storage and model, masked projections, telemetry content off; Model Armor/SDP if available in region (G01) | New input type (uploads, voice) |
| Prompt injection and agency | Build: threat model, no write tools on the model, capability checks, adversarial suite | Uploads (A7) or any new egress |
| Budgets and loop limits | Build: `max_llm_calls`, per-customer daily allowance, global admission limit, operator kill switch | Measured abuse or cost overrun |
| Memory and retrieval | Minimal: ADK sessions only; no long-term memory, no RAG (dispute rules are code, help text is in the instruction) | Help content outgrows the instruction → governed RAG |
| Frontend | Build: chat panel in existing app, completed-JSON turns, confirmation card | Measured latency complaints → streaming |
| Hosting | Build: Cloud Run in EU region, multi-zone, rollback | Platform mandates GKE (O4) |
| Observability | Build: traces, SLIs, alerts, runbook | n/a |
| Release engineering | Build: release manifest, CI gate, canary, joint rollback | n/a |
| Performance and cost tuning | Defer until measured in G13 load test and pilot | p95 latency or cost per case above target |

**Floor kept:** no secrets in code, prompts or logs; `RunConfig.max_llm_calls`
plus application allowances; nothing reaches core banking without the
customer's explicit confirmation on a code-rendered summary; personal data
scoped to the customer and kept out of telemetry content; model IDs pinned.
No accepted risks are recorded yet. The user has not been asked.

**Who may use it before GA:** synthetic data only until G11 staging. Bank staff
with their own real accounts in the staff pilot (G14a). Then a limited customer
cohort (≈5% of app users, assumed) in the customer pilot (G14b).

**Graduation conditions to GA:** all invariants I1–I8 have passing tests. External
pentest has no open high findings. DPIA and model-risk sign-off are recorded.
The pilot meets the SLO targets below for two consecutive weeks.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Evidence uploads with quarantined reader | Adds untrusted documents, malware scanning and a second agent; not needed to open a case | Back-office rework due to missing evidence > agreed threshold |
| Second language | Each language needs its own labelled set and SME review | Product decision; GA scope change |
| Dispute status queries ("where is my case?") | A second read integration with case-management | Contact-centre data shows status calls dominate |
| Model failover | `FallbackModel` is absent in ADK 2.8.0; static-form fallback covers outages | ADK pin moves to a version with failover and outage data justifies it |
| BigQuery agent analytics | Traces and logs answer pilot questions | Product analytics needs beyond dashboards |
| Streaming responses | Buffered turns allow output checks before release | Measured p95 time-to-answer above target |

**Capacity and cut line:** capacity ≈ 6 × 17 weeks × 40 h × 0.6 ≈ **2,450
focused hours** (plus ~100 h of security review). Keeping 25% in reserve leaves
≈ 1,840 h for goals. Phase 1 (G00–G15) is estimated at **1,440–2,180 h**,
mid ≈ 1,810 h. It fits at mid-range with no slack beyond the reserve. The
cut already made: one language, no uploads, no status queries. If phase 1 runs
over, the next things cut are, in order: G13 load test reduced to one
soak run; per-customer allowance reduced to a global limit; dashboards reduced to
alerts only. The floor and the pilot are never cut. If they don't fit, GA slips.
Phase 2 and Later are in the plan.

## Guarantees and acceptance

| ID | Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | An authenticated customer sees and disputes only their own card transactions | Auth middleware verifies the token and derives `customer_id` into trusted session state. Tools read it from `ToolContext.state`, never from model arguments. Core-banking read API is queried with that ID. | 403 / tool returns `not_found`; no data reaches the model | Offline: cross-customer tests with a scripted model that passes another customer's transaction ref; assert no read of foreign data and no draft |
| I2 | One confirmed draft produces at most one dispute case in core banking | `dispute_operations` row with unique `operation_id` and unique active `(customer_id, transaction_ref)`. Submission uses `operation_id` as client reference. Reconciliation looks up by reference before any resend (contract from G00). | Duplicate confirm returns the existing operation; uncertain write → status `uncertain`, no fresh dispatch | Offline: double-click, two tabs, lost response, worker restart mid-submit; assert one adapter create call per operation (or a lookup then no create) |
| I3 | Nothing is submitted without the customer confirming the exact rendered summary | Confirm endpoint requires `draft_id` and `draft_hash` of the summary the UI rendered. Hash is over the canonical payload. The model has no submit tool. | Hash mismatch → 409, re-render | Offline: model text "yes, submit" creates no case; stale hash rejected |
| I4 | The assistant never decides eligibility or promises a refund/outcome | Eligibility windows and deadlines computed in `dispute_rules` code. Post-confirmation messages are code templates. Instruction forbids promises. Output check flags promise phrases before release. | Flagged reply replaced with a safe template; event logged | Eval: forbidden-promise metric = 0 on dev set and adversarial suite |
| I5 | Category and required facts come from a closed contract | `record_dispute_draft` tool validates enum category and per-category required fields. Code maps category → internal dispute type and scheme reason code. | Tool returns actionable error; after 2 repairs → handoff to human | Offline: scripted invalid args; Eval: category exact-match accuracy ≥ target (O7) |
| I6 | Full card numbers (PAN) and other credentials never enter model context, session storage or telemetry | Ingress detector (pattern + Luhn) on customer text before the Runner. Tools return masked projections (last 4). Telemetry content capture is off. | Detected PAN replaced with `[card number removed]`, customer told why | Offline: PAN in input → absent from captured model request, stored events, exported spans and logs |
| I7 | Confirmed cases reach a terminal known state | Reconciler job resolves `submitting`/`uncertain` operations; after N attempts or 30 min → manual reconciliation queue with alert | Customer sees "received, reference pending"; ops sees queue item | Offline: forced timeouts; Local integration: restart during submit |
| I8 | Customer is told they are talking to an AI assistant and can reach a person at any turn | UI banner and first-turn template (code); "Talk to a person" is a UI control, not a model decision | n/a | UI test; content review in G15 |
| T1 | Availability: ≥ 99.5% of conversation turns succeed or degrade to the static form (assumed target) | Cloud Run multi-zone + static-form fallback | Fallback banner | SLI from G10; pilot data |
| T2 | Latency: p95 time to complete reply ≤ 8 s, p95 confirm-to-reference ≤ 10 s (assumed) | Model choice, bounded tools, deadlines | Typing indicator; on deadline, honest failure | G13 load test |
| T3 | ≥ 99% of confirmed cases have a core-banking reference within 15 min (assumed) | Submission + reconciler | Manual queue | SLI from G10 |

## Architecture and decisions

```mermaid
flowchart LR
  subgraph Customer device
    APP[Banking app chat panel]
  end
  subgraph Bank edge
    GW[API gateway\nOIDC token]
  end
  subgraph GCP EU region (VPC-SC perimeter)
    API[Dispute Assistant service\nCloud Run\nFastAPI + ADK Runner]
    AG[LlmAgent dispute_assistant\nread tools + draft tool]
    DB[(Cloud SQL PostgreSQL\nADK sessions\ndrafts + dispute_operations\nallowances)]
    REC[Reconciler\nCloud Run job + Scheduler]
    VX[Vertex AI Gemini\nEU endpoint]
    OBS[Cloud Trace / Logging / Monitoring\ncontent off]
  end
  subgraph On-prem via Interconnect
    IL[Integration layer]
    CB[(Core banking\ncards + disputes)]
  end
  APP --> GW --> API
  API --> AG --> VX
  AG -- read tools --> IL
  API -- confirm: submit --> IL --> CB
  REC --> IL
  API --> DB
  REC --> DB
  API --> OBS
```

Trust boundaries: the device and gateway are untrusted until the service
verifies the token. The model is untrusted, so its outputs are proposals. Core
banking is authoritative for transactions and cases. Merchant descriptors and
customer text are untrusted content.

**Sequence: successful dispute (Anna).**

```mermaid
sequenceDiagram
  participant A as Anna (app)
  participant S as Assistant service
  participant M as Gemini (Vertex)
  participant D as Cloud SQL
  participant C as Core banking
  A->>S: POST /turns (token, session_id, text)
  S->>S: verify token → customer_id; PAN screen; allowance check; session lock
  S->>M: Runner turn (instruction, tools)
  M-->>S: call list_recent_card_transactions()
  S->>C: read txns for customer_id (trusted)
  C-->>S: masked txns
  M-->>S: call record_dispute_draft(txn_ref, category, facts)
  S->>D: validate (owner, window, no active dispute) → draft + hash
  S-->>A: reply + confirmation card (rendered from draft record)
  A->>S: POST /drafts/{id}/confirm (hash)
  S->>D: INSERT operation (unique) status=submitting
  S->>C: create case (client_ref=operation_id), deadline 8 s
  C-->>S: case_ref
  S->>D: status=submitted, case_ref
  S-->>A: "Case DSP-… opened" (code template)
```

### Decision record

All decisions are **proposed** (the user has not reviewed them). "Prov." marks
those that depend on an Assumed answer.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification and expected result |
| --- | --- | --- | --- | --- | --- |
| D1 | Interpret free-text accounts and guide identification (A1) | **One `LlmAgent`** with five narrow tools, run by ordinary FastAPI code that owns auth, confirmation and submission | Only the conversation needs language judgment. Every other step has known ordering and rules. | Multi-agent triage (fraud/merchant sub-agents) rejected: same data, same tools, same credentials, so no security or context gain. Costs more routing evals. | Tool count = 5. Eval shows category accuracy per category. |
| D2 | I1 customer scope (A2, prov.) | Middleware verifies the gateway token (issuer, audience, expiry, signature) and writes `customer_id` into session state at session creation. Session ownership is rechecked on every request. Tools read scope from state only. | A conversation ID locates a session but is not permission. Keeping scope out of model arguments removes a whole class of injection. | Requires gateway token forwarding (O1). Alternative "trust gateway header" is rejected without mTLS between gateway and service. | Cross-customer and stolen-session-ID tests deny with no foreign read |
| D3 | EU residency, regulated data (A9, prov.) | Vertex AI Gemini on an EU regional endpoint, no API keys. Cloud Run, Cloud SQL, logs and traces in the same region, inside the bank's VPC-SC perimeter. | Hosting region alone doesn't establish where inference, logs and backups live. Each is pinned. | Regional model availability may lag the global endpoint. G01 verifies it. | G01 evidence: model ID served in region; log bucket and trace region recorded |
| D4 | I4, I5: closed categories, no outcome decisions (A4, A5) | `record_dispute_draft(transaction_ref, category: enum, statement, facts)` with per-category required facts. `dispute_rules` code computes eligibility window, deadline and priority. Code maps category → internal type/reason code. | The model chooses among six categories, a judgment it can be measured on. Liability stays with code and people. | Less flexibility for edge cases, which go to the `other_needs_human` category → handoff | Offline validation tests; dev-set accuracy |
| D5 | Unauthorised transactions need fast fraud handling (A4) | Category `unauthorised` sets priority = fraud in code. The reply template directs the customer to the app's freeze-card control (deep link). The agent has no card-blocking tool. | Card blocking is an effect with its own existing, audited flow. Linking to it adds no new write path. | One extra tap for the customer vs. agent-initiated block | UI test: deep link present; no block tool in declarations |
| D6 | I2, I3, I7: exactly-once case creation (A3, prov.) | Application-owned `drafts` and `dispute_operations` tables. Confirm endpoint is plain code (not ADK tool confirmation). Submission uses `operation_id` as client reference. A reconciler job resolves uncertain outcomes by lookup, else a manual queue. | Confirmation must survive reconnect and bind to rendered details. ADK conversation state isn't a durable operation record. | More tables and a reconciler vs. relying on chat state. Depends on G00 for the lookup contract. | Lost-response, double-confirm, restart tests (G05) |
| D7 | Core banking may lack lookup-by-reference (A3, prov.) | If G00 shows no lookup: before any resend, query open cases by `(account, transaction_ref)` and match on our reference in a free-text field. If that's not possible, every uncertain outcome goes to the manual queue and is never resent automatically. | A later rejected attempt can't prove an earlier one had no effect | Manual work for every timeout in the worst case | G00 decision record; G05 tests for the chosen branch |
| D8 | Honest degradation, human access (A14, I8) | Kill switch and model/dependency failures route to the existing static dispute form and "talk to a person". Handoff passes a code-generated summary (no raw transcript). | Customers keep a working path whatever the assistant's state | Static form loses guidance | Fault-injection test: model 503 → fallback response |
| D9 | No untrusted documents at GA (A7, prov.) | No upload or document reading in phase 1 | Keeps the agent free of document-borne injection while it holds private data | Back office requests evidence separately | Declaration dump shows no file tool |
| D10 | Hosting (A9, prov.) | **Cloud Run** service (min 2 instances, multi-zone), Direct VPC egress to Interconnect, Cloud SQL via private IP | Custom auth middleware, confirm/submit endpoints and VPC egress fit a container service. The team knows Cloud Run. | Agent Runtime rejected for now: the non-agent endpoints and network path still need a service. GKE if the platform mandates it (O4). | G11 deploy readback; revision serving verified |
| D11 | Retention and erasure (A10, prov.) | Sessions purged at 90 days by a scheduled job. Drafts not confirmed are purged at 30 days. Operations kept with the case per records policy. No long-term memory. | Minimises personal data in the assistant. The case record is the system of record. | Purging can't reach data already exported to the case (intended) | Purge test; DPIA review |
| D12 | Spend and abuse control (A12) | `RunConfig.max_llm_calls = 10` per invocation. Per-customer allowance (20 turns/day, 3 drafts/day, assumed) in Cloud SQL with atomic increment. Global concurrency limit per instance. Operator kill switch flag outside agent reach. | Billing budgets only alert. Admission must be in the application. | A legitimate heavy user may hit the limit → handoff message | Offline: allowance exhaustion, kill switch tests |
| D13 | Completed-turn replies (T2) | Each turn returns completed JSON `{reply, card?, status}`. No token streaming at GA. | Allows the promise check (I4) before release. Simpler failure handling. | Slower perceived response than streaming | G13 latency measurement against T2 |
| D14 | Comparable releases | Pinned `gemini-3.8-flash` agent model, pinned judge, versioned prompt, tool-schema hash and image in one release manifest | Alias drift would change behaviour in a regulated flow | Planned migrations instead of silent upgrades | Manifest has no alias. Calendar holds the retirement checks. |

**Versions (working assumptions).** ADK `google-adk==2.8.0` (released
2026-08-25; the version the specialist skills were checked against; upstream
main is at 2.11.0). G02's first acceptance item is "confirm against the chosen
pin". In 2.8.0, `FallbackModel` and `ADK_MAX_TOOL_ROUNDS` are absent (from
`adk-model-and-output-contracts` compatibility notes), hence D8 instead of
model failover.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Owns: helping the customer identify a transaction, asking for the category's required facts, choosing a category, being plain and brief in L1. Must not: promise outcomes, give legal advice, discuss other customers, ask for card numbers/PINs/OTPs. Customer ID, date, eligibility windows and the transaction list are injected by code (state templating) or fetched by tools, never claimed by the model. Prompt is versioned in `prompts/dispute_assistant/vN.md`. | `adk-agent-instructions`; rendered-request snapshot test |
| Tools (5, all read or draft) | `list_recent_card_transactions(days≤400, query?)` → ≤20 masked rows. `get_transaction_detail(transaction_ref)`. `check_existing_disputes(transaction_ref)`. `get_dispute_requirements(category)` → required facts and deadline computed by code. `record_dispute_draft(...)` → `{status, draft_id, missing_facts?}`. Every result is bounded (≤ 4 KB) with a `status` and an actionable error. Tiers: four read, one draft (local, reversible). **No write or irreversible tool is exposed to the model.** | `adk-tool-interface-design`; declaration dump and size test |
| Output contract and model | Free-text replies. Structured data travels only through `record_dispute_draft` arguments (validated in code), which avoids `output_schema`+tools interplay. Repair budget: 2 invalid draft calls, then handoff. Agent model `gemini-3.8-flash` (stable, released 2026-09-02, no shutdown announced; lifecycle table `model-lifecycle-2026-10-01.json`, checked_on 2026-10-08). Avoid `gemini-3.7-flash` (Vertex retirement 2027-01-28, before GA) and `gemini-3.6-flash` (2026-11-19). No preview models in production. Judge: `gemini-3.8-flash` pinned separately, used only for secondary rubric metrics (tone, clarity). Primary gates are deterministic (category exact match, required-fact completeness, forbidden-promise detector). Self-preference bias is accepted because the judge doesn't gate on correctness (revisit O9). Thinking level and temperature are set in G03 from dev-set measurement. | `adk-model-and-output-contracts`; scripted invalid-output tests |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | Bank IdP. One customer per token. | Middleware writes `customer_id` into session state; tools read it | Token per request; session ownership checked on each request | Not stored beyond session |
| Card transactions | Core banking, customer's own cards | Read tools only | Live read per call. No cache at GA. | Not persisted except masked refs in session events (90 days) |
| ADK session events | Service; owner = `customer_id` | Runner; purge job | `DatabaseSessionService` on Cloud SQL | 90 days (A10) |
| Dispute draft | Service; owner = `customer_id` | `record_dispute_draft` tool writes, confirm endpoint reads | Canonical JSON + SHA-256 hash; expires 30 min after creation for confirmation | Unconfirmed purged at 30 days |
| Dispute operation | Service; owner = `customer_id` | Confirm endpoint, reconciler | States: `submitting → submitted / uncertain → submitted / failed_permanent / manual` | Retained with case per records policy |
| Dispute case | Core banking / dispute ops | Created once by submission adapter | Authoritative | Bank records policy |
| Allowances, kill switch | Service operators | Middleware (atomic increment); operators (flag) | Cloud SQL / config | Daily rollover |

Identities: **session** (one conversation, many invocations), **invocation**
(one turn, ADK), **business operation** (`operation_id`, created at confirm,
survives retries and restarts). Credentials: the service's workload identity
calls Vertex and Cloud SQL. A client certificate from Secret Manager calls the
integration layer. Credentials are chosen in code, never from model arguments.
The service account's rights do not establish the customer's authority. That
always comes from the verified token.

**Public output policy:** the model's reply text is released after the
promise/PII check (D13). Confirmation cards and post-confirmation messages
are rendered from records by code. Tool arguments, stack traces and raw
events are never forwarded to the client.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| `dispute_assistant` | Yes: customer's transactions | Yes: customer free text, merchant descriptors from card networks | Draft record only (no submit, no email, no external call with model-chosen destination). Reply goes to the same authenticated customer. | **Write leg removed from the model.** Submission is code behind a UI confirmation bound to a hash. A `before_tool_callback` checks each tool's `transaction_ref` belongs to the session's customer (I1). Injection via a merchant descriptor can at worst mislead the draft, which the customer sees before confirming. |

Adversarial cases (G07): merchant descriptor containing instructions; the customer
asks for another customer's data or supplies a foreign transaction ref; the customer
coerces a refund promise; the customer pastes a PAN; the customer asks the agent to
"submit now" in text; tool returns malformed or oversized data. Each asserts
the forbidden effect is absent (no foreign read, no draft for foreign ref, no
case without confirm, no PAN in stored events). No code executor is used.

Screening: deterministic PAN/IBAN detector at ingress (always). Model Armor
prompt-injection/jailbreak screening and SDP inspection as an extra layer, if
G01 confirms EU-region availability and the DPO accepts them as processors.
If screening is unavailable, the turn proceeds with the deterministic
detector only and the event is logged. This fail-open choice is provisional
(open decision O6), because the structural controls above don't depend on
screening.

## Budgets and capacity

Per turn (expected / bounded): model calls 2–3 / 10 (`max_llm_calls`).
Core-banking reads 1–2 / 5. Input tokens ≈ 4–8 k per call (instruction ~2 k,
tools ~1.5 k, history, ≤ 4 KB tool results). A conversation is ~5–8 turns.
Model retries: SDK `retry_options` max 2 attempts on 429/5xx, inside the
turn's 20 s deadline (application owns the overall budget).

Concurrency ≈ arrival × time in flight. At A8 peak (30 concurrent
conversations, one active turn per ~30 s each, ~6 s per turn) that is about 6
in-flight turns, comfortably handled by 2 instances with concurrency 20. G13
measures it, and model quota (requests/tokens per minute in region) is
checked in G01.

Cost per dispute conversation (symbolic, no prices looked up):
`turns × calls_per_turn × (in_tokens × p_in + out_tokens × p_out) +
Cloud Run + Cloud SQL fixed`. With 6 × 2.5 × (6 k in, 0.4 k out) ≈ 90 k input
and 6 k output tokens per conversation. Prices must be looked up dated in G01.
This is not a bill or a cap.

Exhaustion: per-customer allowance → message + handoff. Global limit → 429 with
static-form fallback. Kill switch → static form for everyone, existing operations
continue reconciling. The reconciler has reserved capacity unaffected by turn
admission.

Same-conversation concurrency: one turn at a time per session (row lock on
the session's turn record; a second send gets 409 "still answering"). Confirm
is independent of turns and idempotent.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Successful request | Case reference shown | Operation `submitted` with `case_ref` | None |
| Another customer's session ID or transaction ref | 403 / "I can't find that transaction" | Denial logged with invocation ID | None; security alert if repeated |
| Model unavailable / 429 after retries | "The assistant is unavailable" + static form + handoff | Session up to last turn | Customer uses form; on-call if SLO burns |
| Model returns invalid draft args twice | "Let me pass you to a colleague" + handoff | Session; no draft | Human agent |
| Draft created, customer leaves | Nothing | Draft expires (30 min), purged at 30 days | None |
| Confirm double-click / two tabs | Same reference or "already submitted" | One operation (unique constraint) | None |
| Core banking commits, response lost (timeout) | "We've received your dispute; your reference will appear in the app shortly" | Operation `uncertain` | Reconciler: lookup by client reference (or D7 branch), else manual queue (dispute ops), alert |
| Worker crashes between INSERT and submit | Same as above on the customer's next view | Operation `submitting` with stale lease | Reconciler treats it as uncertain. It never sends fresh without the lookup. |
| Core banking rejects (validation, account closed) | Code template explaining next step + handoff | Operation `failed_permanent` with reason code | Dispute ops if pattern repeats |
| Transaction already disputed via another channel between draft and confirm | "A dispute for this payment already exists (ref …)" | Recheck at confirm finds existing case; no create | None |
| Entitlement changes while draft waits (card closed, customer logged out) | Confirm rejected; re-authenticate | Draft unchanged | Customer |
| PAN screening detector fails (exception) | Turn rejected with generic error (fail closed for this deterministic step) | Nothing stored | On-call |
| Telemetry exporter down | None | Spans dropped; logs buffered | On-call; SLIs show a gap, which is reported as missing evidence |
| Kill switch on during reconciliation | Static form for new users | Reconciler keeps running | Operators |
| Model retirement announced | None | Pinned ID still served until date | Release owner runs planned re-baseline (`adk-release-engineering`) |
| Bad release | Canary metrics breach | Previous revision ready | Joint rollback of image + prompt + model pin + tool schema |
| Customer requests erasure (GDPR Art. 17) | Per DPO process | Sessions/drafts purged on request. Cases kept under legal obligation. | DPO process + purge job |

Rollback rehearsal: the session schema and the `drafts`/`dispute_operations` tables
are migrated forward-compatibly (expand → migrate → contract). The previous
revision must read rows written by the candidate. This is tested in G12.

## Verification and implementation handoff

Evidence ladder (all **planned**; none executed):

- **Offline deterministic** (every change, CI): auth/scope, tool validation,
  draft hashing, operation state machine, lost response/duplicate/restart,
  PAN removal across model request, events, spans and logs, adversarial
  suite with scripted model, allowance and kill switch.
- **Local integration:** Postgres in a container, process restart during
  submit, fake core-banking server with injected latency and loss.
- **Bounded live (authorised staging only):** Vertex model in EU region
  (dev-set evaluation runs with a declared request/cost limit), core-banking
  test environment for the G00 contract.
- **Release/operation:** G13 load test, external pentest, pilot SLIs, rollback
  and purge rehearsal.

Business outcome (hypothesis): first-time-right rate and dispute call volume vs.
the dispute-ops baseline (O7). Guardrails: complaint rate, back-office rework,
handoff rate. Model quality (category accuracy) and valid transactions (I2)
are measured separately.

Observability and release:

- SLIs: turn success ratio (T1); p95 turn latency (T2); confirmed→reference
  within 15 min (T3); tool error rate by tool; tokens per completed case;
  handoff rate; promise-check trigger rate. Targets are provisional until pilot
  baselines exist. Alerts on error-budget burn go to the team's on-call.
- One telemetry owner per process (ADK OTel setup to Cloud Trace/Monitoring in
  region). Message content capture is off
  (`ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`, no GenAI content capture).
  Logs are structured with `session_id`, `invocation_id`, `operation_id`, and
  no customer text.
- Release bundle: image digest, prompt version, agent and judge model IDs,
  tool-schema hash, eval-set hash, secret versions. Recorded in
  `release/manifest.json` and attached to the Cloud Run revision as labels.
- Promotion gate: deterministic suite + dev-set evaluation (category accuracy,
  completeness, zero forbidden promises) with a fixed repeat count and a cost
  ceiling. A missing run is a fail.
- Canary: 5% of pilot traffic via revision tags. Thresholds are set before traffic
  moves. The previous revision stays ready ≥ 7 days.

Implementation goals, estimates and run prompts are in the
[implementation plan](../plans/card-dispute-assistant.md).

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- | --- |
| O1 | Gateway token forwarding and claims (A2) | D2 trust model | Bank IAM/gateway team | G02 live wiring (local work proceeds with a test issuer) |
| O2 | Core-banking dispute API: dedup and lookup semantics, timeouts, test env (A3) | D6/D7 branch; I2 strength | Core banking team; G00 | G05 live adapter |
| O3 | Gemini model availability, quotas, data-retention terms in the EU region; Model Armor/SDP availability (A9) | D3, D14, screening layer | Platform team + Google account team; G01 | G03 live eval runs, G06 screening layer |
| O4 | Hosting mandate: Cloud Run vs. bank GKE platform | D10 | Platform team | G11 |
| O5 | Retention periods for sessions and drafts (A10) | D11, DPIA | DPO / records management | G15; purge job values |
| O6 | Screening fail-open vs. fail-closed | Availability vs. defence in depth | Security reviewer + DPO | G06 |
| O7 | Baselines and targets: category accuracy, first-time-right, call volume, SLO numbers | Gates and SLOs | Dispute ops + product owner | G03 gate threshold, G10 alerts |
| O8 | Languages at GA (A6) | Eval set size, cut line | Product owner | G03 scope |
| O9 | Judge independence: same-family judge acceptable for secondary metrics? | Eval validity | Model-risk team | G12 |
| O10 | Monthly spend ceiling (A12) | Allowance values | Product owner | G09 values |
