# System design: card-transaction dispute assistant

Status: **draft**. Written in one pass without the user available. Every row
in *Assumed answers* is provisional until the bank confirms it, and so is every
decision that depends on one. No decision here is user-accepted yet.
Design date: 2026-10-09. Plan: [docs/plans/card-dispute-agent.md](../plans/card-dispute-agent.md).

## Assumed answers

These are the questions I would have asked. Decisions that depend on them are
marked *(provisional: Qn)* where they appear.

| # | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | Time and money for this work? | Six engineers and one security reviewer for about 17 weeks to GA (target GA in week 17, early February 2027). There is no fixed cloud budget, but there is a small non-production model spend allowance (see Budgets). | Plan sequencing, deferred controls |
| Q2 | Who judges the result, and what do they read? | Internal launch gates: the security reviewer, bank Compliance/DPO, Model Risk Management and the disputes operations lead. They review this design, the threat model, the evaluation report and pilot metrics. After that, customers use a running service. | Evaluation and evidence goals |
| Q3 | What kind of artifact is this? | A production service at GA. A staff and limited-customer pilot comes first. | Every control is in scope. See Deferred controls |
| Q4 | Which channels? | Authenticated web and mobile banking only, using the bank's existing OIDC identity provider and existing app shell. No voice, no unauthenticated use. | Identity, frontend, D-04 |
| Q5 | Which languages? | English plus one local language, using German as a placeholder. | Instructions, eval set size, D-03 |
| Q6 | What may the agent change? | It may open a dispute case for one settled or pending card transaction owned by the signed-in customer, after explicit customer confirmation. It may not refund, block cards, change limits, or promise an outcome or deadline. | Tool tiers, security posture |
| Q7 | How do we reach the core banking dispute API? | Through an internal REST API on the bank's integration layer, reached privately from GCP (Interconnect or VPN). Authentication is mutual TLS plus a system credential. Its idempotency and lookup behavior is **unknown**. | D-02, G04 |
| Q8 | Does the bank already run workloads on GCP, and what is its platform standard? | Yes. There is an EU landing zone with an org policy restricting resource locations to the EU. Cloud Run is approved. GKE also exists. | Hosting choice (D-05) |
| Q9 | Is step-up authentication required to confirm a dispute? | Yes. The bank's existing in-app step-up (SCA-style re-authentication) runs at confirmation. | Confirmation design |
| Q10 | Can customers upload evidence such as receipts or merchant emails? | Yes, but in v1 the files are stored and attached to the case only. The model never reads their contents. | Security posture (removes the untrusted-content leg) |
| Q11 | What is the retention period for chat transcripts? | 90 days for the conversation, then deletion. The case and the confirmed dispute summary are kept as the bank's business record under its own retention schedule. | Data table, erasure |
| Q12 | What volume do we expect? | About 20,000 dispute conversations a month, with a 10x burst during a merchant incident (for example a mass duplicate charge). This is an illustrative assumption. | Capacity, cost |
| Q13 | What baseline and outcome should improve? | Assumed baseline: disputes are filed through the contact centre or a web form, and about 30% need a follow-up contact for missing information. Target: fewer follow-ups with no increase in wrongly classified cases. **The baseline is unknown**, so measure it in D-03. | Success metrics |
| Q14 | Which model hosting is acceptable? | Vertex AI in an EU region, under the bank's existing Google Cloud contract and DPA. No consumer Gemini API. | Model and region (D-01) |
| Q15 | Who owns the dispute rules (reason codes, time windows, required facts)? | Disputes operations and Compliance. They supply a versioned rule table. The agent team does not write the rules. | Eligibility engine, D-03 |

Regulatory context, assumed and to be confirmed by bank Compliance (not
legal advice): GDPR (DPIA, retention, erasure), PSD2 rules on notifying and
refunding unauthorised transactions, card-scheme chargeback time limits, DORA
(ICT third-party register, exit plan, incident classification), EBA outsourcing
guidelines, the EU AI Act transparency duty to tell customers they are talking
to an AI system, and the bank's internal model-risk policy. The design keeps
every regulated decision (eligibility, refund, fraud handling) in deterministic
code or in the existing back office, and keeps it out of the model.

## Purpose and constraints

**Running journey.** Anna signs in to mobile banking and sees an
unrecognised charge, "€89.99 XYZ\*DIGITAL", from last week. Today she would
call the contact centre or fill in a long form, and she often picks the wrong
reason, so the back office calls her back. With the assistant, she opens
"Dispute a transaction" and describes the problem in her own words. The
assistant finds the transaction among her own recent card transactions and
asks the two or three questions that the reason requires. Did she still have
the card? Did she contact the merchant? Deterministic code then checks
eligibility. Anna sees a structured summary, confirms with step-up
authentication, and receives a case reference from the core banking system.
If the reason suggests fraud, she is shown the existing "freeze card" control.
The assistant never freezes the card itself.

**What the model contributes:** it interprets free text, identifies the
transaction, classifies the reason, and asks for missing facts in the
customer's language.
**What ordinary code controls:** identity and scope, transaction lookup,
eligibility and time limits, the case payload, confirmation, submission,
idempotency, retries, reconciliation, budgets, PII screening and everything
the customer is told about case status.

**Non-goals for GA:** refunds, card blocking, merchant contact, chargeback
outcome tracking in chat, reading uploaded documents, voice, and
unauthenticated use.
**Existing systems (assumed, not inspected):** the bank's identity provider,
mobile and web app shell, API gateway, core banking dispute API, and GCP EU
landing zone. This repository is greenfield. It contains only
`.claude/skills/`.

**Outcome to improve** *(provisional: Q13)*: the share of filed disputes that
the back office accepts without a follow-up contact. Guardrails: the rate at
which the back office reclassifies a case's reason, complaint rate, and
handoff rate. These are measured separately from model quality and from
technical success.

## Scope, evaluator and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| Time and money available | 6 engineers + 1 security reviewer, about 17 weeks to GA *(assumed, Q1)*. Cloud spend: not fixed. Non-production model spend is capped by the application budget in G08 |
| Who judges the result and what they read | Security reviewer, Compliance/DPO, Model Risk Management and the disputes ops lead read this design, the threat model, the eval report and pilot metrics. Customers then use a running service *(assumed, Q2)* |
| Artifact type | Production, with a pilot before GA *(assumed, Q3)* |

This is production, so the proportionality rule does not remove controls. It
does shape the order of work: classification quality is measured early (G03),
before hardening work grows around it.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Model reads uploaded evidence (OCR or vision) | Adds an untrusted-content leg and a new evaluation surface. Not needed to open a case | Back office shows that evidence summaries cut handling time; needs a quarantined reader agent (see Security posture) |
| Cross-session memory or personalisation | No journey needs it. Each dispute is self-contained | A repeat-dispute journey with consent |
| Contact-centre live handoff with transcript transfer | It is a second write integration. v1 shows contact options and stores a handoff marker | The pilot handoff rate is above about 10% |
| Token streaming to the browser | Buffered, screened turns are safer for a bank. Latency target is achievable without streaming *(provisional)* | Pilot p95 time to complete a turn misses target |
| Multi-region active-active serving | Single EU region with zonal redundancy. The core banking system is the real availability bound | A bank availability requirement above the core system's own |
| Model failover to a second model | A second model doubles the evaluation and release surface. On outage we degrade to the existing form | Model availability SLI breaches in pilot |

## Guarantees and acceptance

| Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1. An authenticated customer sees and disputes only transactions on cards they hold | Request middleware derives `customer_id` from the verified OIDC token. Tools read it only from trusted invocation context, never from model arguments. The core banking API re-checks card ownership | 403, a generic message, nothing disclosed to the model | Offline: scripted model passes another customer's transaction ref → tool returns `not_found`, no core call made. Integration: token for A with session of B → 404 |
| I2. A session belongs to one customer. Knowing its ID is not permission | Session lookup is keyed by `(customer_id, session_id)` in the gateway API | 404 | Cross-customer session test (G01) |
| I3. One confirmed draft produces at most one core banking case | Durable `dispute_operation` row with a unique `operation_id`, used as the idempotency key or client reference toward core. State machine in Cloud SQL. Reconciler. **Depends on D-02** | The customer sees "submitted", "being confirmed" or "failed, nothing filed". Never a second case | Offline: lost-response, double-click, worker restart and timeout tests against a fake core with replay semantics (G04) |
| I4. Nothing is filed without explicit confirmation of the exact summary shown | Confirmation endpoint (application code, not a model tool) binds `draft_id + draft_version + payload_hash + step_up_ref` | Stale or changed draft → "summary changed, review again" | Offline: confirm v1 after the model edits to v2 → rejected (G04) |
| I5. Eligibility, time limits and the reason-code mapping come from the versioned rule table and never from the model | `eligibility` module (ordinary code). Rule version is stored on the draft and the operation | Ineligible → the deterministic explanation and the alternative channel are shown | Table-driven unit tests per rule, plus an eval case where the model argues for eligibility (G02) |
| I6. The full PAN, CVV, PIN and one-time codes never reach the model, session storage or logs | Tools return a masked card (last four digits) and an opaque token. SDP inspection on customer text before storage and the model call. Telemetry content capture off | Message containing a CVV or PIN → blocked, the customer is told not to share it, nothing stored | Offline: seeded PAN/CVV inputs, assert the stored events and the captured model request are clean (G05) |
| I7. The assistant never promises a refund, outcome or deadline | Instruction plus an output check. Unresolved: the check is model-judged, so it is a measured rate, not a guarantee | Turn replaced by a safe template, and the event is counted | Eval metric with a threshold in the release gate (G03, G11) |
| I8. Bounded work per turn and per session, with an operator stop | `RunConfig.max_llm_calls` plus application turn and session caps plus a global kill switch in the control table | "Use the dispute form or call us", with a link | Offline exhaustion tests (G08) |
| T1. Turn p95 complete response ≤ 8 s, excluding step-up and core submission | *(provisional assumption)*, measured in G12 | — | Load test (G12) |
| T2. Submission p95 ≤ 10 s, with the uncertain state shown afterwards | Depends on the core SLA (D-02) | "Being confirmed", with the reference to come | G04 and G12 |
| T3. Availability SLO 99.5% monthly for the assistant API, excluding the core system | *(provisional)*. The bank sets the real target | The existing form stays available as fallback | SLI in G10 |

## Architecture and decisions

```text
 Customer (mobile/web app shell, existing)
   │  OIDC access token (existing IdP)          ── trust boundary: internet
   ▼
 API gateway (existing)  ──►  Dispute Assistant service  [Cloud Run, EU region]
                              ├─ HTTP API: /sessions, /turns, /drafts/{id}/confirm, /uploads
                              ├─ AuthN middleware → trusted customer_id
                              ├─ Ingress screening (SDP inspect, Model Armor)  ─► SDP / Model Armor (EU)
                              ├─ ADK Runner + App
                              │    └─ LlmAgent "dispute_intake" (one agent)
                              │         tools: find_card_transactions, get_transaction,
                              │                list_open_disputes, save_dispute_draft
                              │         ─► Vertex AI Gemini (EU region)
                              ├─ eligibility (rule table, ordinary code)
                              ├─ confirm + submit (ordinary code, NOT a model tool)
                              └─ budgets / kill switch
                                   │
            Cloud SQL Postgres (EU) ◄┘  sessions (ADK), drafts, dispute_operation,
                                        control table, rule-table versions
            Cloud Storage (EU, CMEK)    uploaded evidence (never read by the model)
                                   │ private connectivity, mTLS  ── trust boundary: bank DC
                                   ▼
            Core banking: card transactions (read), dispute case API (write)
 Reconciler [Cloud Run job + Cloud Scheduler] ─► core lookup for UNCERTAIN operations
```

**Happy-path sequence:**

1. The app sends a turn with a bearer token. The middleware verifies it and
   loads the session by `(customer_id, session_id)`.
2. Ingress screening runs on the text. It blocks CVV and PIN, masks a PAN,
   and flags injection. This happens before the turn is stored or sent to the
   model.
3. The Runner calls the agent. Tools read the trusted `customer_id` and
   return masked, bounded results.
4. The agent calls `save_dispute_draft(typed fields)`. Code runs
   eligibility, stores draft version N and returns a status to the agent.
5. The turn response carries the assistant text plus a `draft` card rendered
   from the stored draft, not from model text.
6. The customer taps Confirm. The app performs step-up and calls
   `/drafts/{id}/confirm` with the draft version and the step-up reference.
7. Code re-checks ownership, eligibility (current rule version) and
   transaction state. It then claims `dispute_operation` (`SUBMITTING`) and
   calls core with `operation_id`. It records the case reference and returns
   `SUBMITTED`. The app shows the case reference from the operation row.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification and expected result | Status |
| --- | --- | --- | --- | --- | --- | --- |
| DD-01 | Interpret free text and gather facts. Regulated decisions must be deterministic | **One `LlmAgent` with four narrow tools.** Eligibility, payload construction and submission are ordinary code | One conversational responsibility. A second agent would add routing and evaluation surface without a separate credential or trust boundary | Less modular than per-reason sub-agents. If per-reason prompts grow large, revisit with sub-agents | Captured request shows 4 tool declarations. Eval routing accuracy (G03) | proposed |
| DD-02 | Filing a case is a consequential write (Q6) | **The submit is not a model tool.** The model can only save a draft for the current customer. Confirm and submit is an application endpoint called by the app after step-up | The model cannot cause a filing, even under injection. Confirmation binds to the stored payload (I4) | No "just do it" conversational flow. Adds one UI step, which is acceptable for a bank | Scripted model tries every tool sequence and no core write occurs (G06) | proposed *(provisional: Q9)* |
| DD-03 | At most one case per confirmation (I3) | **Durable operation record + idempotency key toward core + reconciler** | A timeout can leave a remote write uncertain. Session storage is not a durable operation ledger | Needs core idempotency or a lookup-by-reference. Without either, uncertain outcomes go to manual reconciliation | G04 fault-injection suite | proposed, **blocked on D-02** for the live contract |
| DD-04 | Identity scoping (I1, I2) | `customer_id` comes from the verified token in middleware. It is placed in invocation context under a key the model cannot set, and `before_tool_callback` re-asserts it. Tool parameters never include customer or card identifiers beyond opaque per-session transaction refs | Knowing an ID grants nothing. Refs are mapped server-side to the customer's own transactions | Indirection table per session | I1/I2 tests | proposed |
| DD-05 | EU residency, private reach to core, bank ops (Q8, Q14) | **Cloud Run** in one EU region with Direct VPC egress to the private link. **Vertex AI Gemini** in an EU region. Cloud SQL Postgres and GCS in the same region with CMEK | Cloud Run is approved and gives revision traffic splitting and a simple ops model. Managed Agent Runtime adds less value here because we own sessions in Cloud SQL and need private egress | GKE would give more networking control at more ops cost. Choose GKE if the bank's standard requires it | D-01 verifies region availability of every service | proposed *(provisional: Q8, Q14)* |
| DD-06 | Conversation persistence and per-session concurrency | ADK `DatabaseSessionService` on Cloud SQL (own schema). A turn lease row per session rejects overlapping turns with 409 | Survives replica restart and keeps a single datastore | Session schema migrations are tied to the ADK version. Rehearse them in G09 | Restart test. Concurrent-turn test returns 409 for one of the two | proposed. Confirm the API against the chosen pin |
| DD-07 | Model choice and lifecycle | **`gemini-3.8-flash`** (status stable, released 2026-09-02, no published shutdown in the lifecycle table checked 2026-10-08). The judge is pinned separately to the same ID, with a different prompt and frozen config. Rejected: `gemini-3.7-flash` (Vertex retirement 2027-01-28, before GA) and `gemini-3.6-flash` (2026-11-19). | No retirement inside the build horizon. Flash-class latency fits T1 | Same-family judge risks correlated errors. Mitigate with human-labelled calibration in G03 | Release manifest has no alias. EU-region availability is unverified (D-01) | proposed |
| DD-08 | PII never reaches model or logs (I6) | Minimise at tools (masked PAN, no CVV ever). SDP inspection at ingress before storage. Model Armor as an added prompt-injection screen. Content capture disabled in telemetry | Fields minimised at source cannot leak. Screening covers what the customer types | SDP and Model Armor add latency and are additional data recipients that need DPIA coverage. Screening service down → **fail closed**: the turn is refused with the form fallback | G05 tests. Screening-outage test | proposed |
| DD-09 | Customer-visible output safety (I7) | **Buffered turns, no token streaming.** The full turn is checked by deterministic patterns (PAN, IBAN, other refs) before release | Streaming cannot retract a disclosed sentence | Higher perceived latency, mitigated by a typing indicator | Seeded unsafe output is replaced before reaching the client | proposed |
| DD-10 | Bounded spend and an operator stop (I8) | Per-invocation `max_llm_calls`=8. Per-session 25 turns. Per-customer 5 sessions a day. Global daily model-token budget with atomic reservation in Cloud SQL. Kill switch row read on admission | Billing alerts only notify. Admission is the application's job | Caps can frustrate an edge-case customer. The fallback form remains | G08 exhaustion tests | proposed (numbers illustrative) |

Versions: there is no installed ADK. Working assumption: **`google-adk==2.8.0`**,
the version every specialist's `references/compatibility.md` was checked
against. Upstream is at 2.11.0 (2026-10-01). Confirming the pin is a G01
acceptance item. Provider facts in this document (regions, quotas, prices,
Model Armor and SDP regional availability) are **not verified**, because the
session had no network access. D-01 carries the lookups.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions and routing descriptions | One agent: identify the transaction, classify the reason into the rule table's reason set, ask only for the facts the table lists as missing, save the draft, and never state eligibility, refund timing or outcome. Customer identity, the date, the rule text and eligibility results come from code (injected state or tool results), not the prompt. AI disclosure is a fixed UI banner plus the first-turn template, not model text. Prompt is versioned in the repo | `adk-agent-instructions`. Rendered-request snapshot test |
| Tool interfaces and budgets | 4 function tools, no MCP or OpenAPI import. `find_card_transactions(description_hint, date_from, date_to, amount)` → ≤ 10 masked rows with opaque `txn_ref`. `get_transaction(txn_ref)`. `list_open_disputes()`. `save_dispute_draft(txn_ref, reason_code, facts{…typed per reason}, customer_statement)` → `{status: saved / needs_facts / ineligible, missing: [...], draft_version}`. Tiers: three read, one write to the customer's own draft only. No irreversible tool | `adk-tool-interface-design`. Declaration dump size test and selection accuracy on the dev set |
| Output contract, model and backend | The structured contract is the `save_dispute_draft` arguments, validated with pydantic. Invalid → actionable error to the model, at most 2 repairs, then the `cannot_complete` path (handoff). A first-class "unclear" reason exists so a valid "cannot classify" survives. Final chat text is free text and passes the release check. Vertex AI backend, `gemini-3.8-flash`, low thinking level, temperature low (to be tuned in G03). No failover (deferred) | `adk-model-and-output-contracts`. Scripted prose, invalid and wrong-but-valid tests |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | IdP | Middleware (reader) | Token per request | Not stored beyond `customer_id` |
| Card transactions | Core banking | Tools read via core API, scoped by `customer_id` | Live read per call. Pending vs settled shown | Not persisted. Opaque refs kept in session state for the session's life |
| Conversation (ADK session events) | Customer, via the assistant service | Runner (writer), customer and the service (readers) | — | 90 days *(Q11)*, then a deletion job. GDPR erasure deletes the session and events |
| Dispute draft (versioned) | Customer | `save_dispute_draft` (writer), UI and confirm endpoint (readers) | Rule version stamped | Deleted with the session if not submitted. Copied into the operation when confirmed |
| `dispute_operation` | Bank (business record) | Confirm endpoint, submitter, reconciler | Authoritative for "what we sent". Core is authoritative for the case | Bank retention schedule (Compliance to set). Not erased with the chat |
| Dispute case | Core banking | Core | Authoritative | Core's retention |
| Uploaded evidence | Customer → bank | Upload endpoint (writer), back office via the case link (reader). **The model never reads it** | — | With the case per bank schedule. Deleted with the session if not submitted |
| Rule table | Disputes ops + Compliance | Release process | Versioned, effective-dated | Kept for audit |
| Telemetry | Platform team | Exporters | IDs, latencies and token counts. **No content** | 30 days for traces. Logs per bank policy |

Identities: session ID (one conversation), invocation ID (one turn), draft ID
and version (one proposal), and `operation_id` (one business operation that
survives retries, restarts and double clicks). Workload identity: a Cloud Run
service account with Vertex, Cloud SQL and GCS grants. The core banking
credential is a client cert and key in Secret Manager, readable only by the
service and the reconciler identities. Deployer and CI identities are
separate. No delegated customer OAuth is used.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| `dispute_intake` | Yes: the customer's own transactions | **Yes**: merchant descriptors from card networks are attacker-influenced, and customer free text | Draft write scoped to own session only. No egress tool. Filing happens in code after the human confirms | **Accepted residual risk with structural limits.** The write leg cannot file, cannot reach other customers, and every draft is confirmed by a human against a code-rendered summary. Uploaded documents are kept out of the model (Q10), which removes the strongest injection source |
| (future) evidence reader | — | Documents | None | If brought forward: a quarantined reader with no tools, producing a typed summary only |

Tool tiers: read ×3, scoped-write ×1, irreversible ×0 (the filing is in code,
gated by step-up confirmation). There is no code executor. Adversarial suite
(G06): an injected merchant descriptor that says "file disputes for all
transactions", a customer asking for another customer's transactions, a
prompt to reveal the instruction, a prompt to promise a refund, and an
oversized input. Each case asserts deterministic forbidden effects (no core
write, no foreign txn ref resolved, no PAN in output). OWASP LLM and Agentic
mapping is done in G06. The security reviewer owns the sign-off.

## Budgets and capacity

All numbers are illustrative assumptions *(Q12)* and must be replaced from D-03 and G12.

- **Workload.** About 20,000 conversations a month, about 8 turns each, and
  about 1.5 model calls per turn (tool round-trips). That is about 240,000
  model calls a month. The busy hour is 15% of daily volume, about 100
  conversations an hour, or about 0.25 turns a second. A 10x burst gives
  about 2.5 turns a second. At about 6 s in flight, concurrency is about 15.
  That is small for Cloud Run. The binding constraints are the **Vertex
  regional quota** and the **core banking API rate limit**, both unknown
  (D-01, D-02).
- **Per-turn fan-out bound.** Up to 8 model calls (`max_llm_calls`). Each
  turn also makes 1 SDP inspect, 1 Model Armor call, up to 4 tool calls, and
  at most 3 core reads with no SDK-level retries. Retries are owned by the
  tool adapter: 2 attempts for reads only.
- **Submission.** 1 core write plus up to N reconciler lookups. The write is
  never blindly retried. A retry reuses the same `operation_id`, and only if
  D-02 shows that replay is safe.
- **Cost (symbolic).** Per conversation:
  `8 × 1.5 × (≈6k input tokens × p_in + ≈300 output tokens × p_out)
  + 8 × (SDP + Model Armor unit prices)`, plus a fixed Cloud SQL and minimum
  Cloud Run instance cost. Prices are not looked up (no network). D-01
  records the dated prices. This is not a validated bill.
- **Enforcement.** The application reserves estimated tokens in the control
  table at admission and settles after the turn. Exhaustion stops new
  sessions and lets in-flight confirmations and the reconciler finish. The
  operator kill switch is separate from budget resets and outside agent
  authority.
- **Latency.** T1 and T2 above. A turn has an 8 s budget, with each
  dependency deadline nested inside it. Cleanup time is reserved.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Token for customer A, session or txn ref of B | Not found | Nothing is disclosed to the model | None. A security alert fires if repeated |
| Model unavailable or returns invalid output 3 times | "I can't continue. Use the dispute form", with a prefilled link if a draft exists | Session events. Draft if one was saved | Customer retries later. Model SLI alert to on-call |
| Screening service unavailable | Turn refused, with the form fallback (fail closed) | The unscreened text is **not** stored | Platform on-call |
| Customer confirms, core times out | "We're confirming your dispute. You'll see the reference shortly." | Operation is `UNCERTAIN` with its payload hash | Reconciler looks up by `operation_id` or reference (D-02). If lookup is unsupported, the disputes back office reconciles manually from a queue. **Never a fresh dispatch** |
| Core commits, response lost, worker crashes | As above when the customer reopens the app | `SUBMITTING` row with an expired lease | The reconciler treats it as `UNCERTAIN`. An expired lease does not prove the request stopped |
| Double tap or two devices confirm | One case. The second request returns the same operation status | One operation row (unique `draft_id + version`) | None |
| Draft edited by the model after the summary was shown | "The summary changed. Please review." | New draft version | Customer reviews again |
| Eligibility or rule table changes between draft and confirm | Re-check at confirm. If now ineligible, the explanation and the channel are shown | Draft kept | Customer or contact centre |
| Card or transaction state changes (for example, already refunded) | Re-check at confirm → message | — | — |
| Browser disconnects mid-turn | On reconnect, the last completed turn is shown | Turn completes server-side. The lease is released | — |
| Injected merchant descriptor | Normal behavior. The forbidden action is structurally unavailable | Event flagged | Security review of flagged events |
| Budget exhausted or kill switch on | "Use the dispute form or call us" | Confirmations and reconciler continue | Operator |
| Erasure request while a submission is in flight | Chat deleted after the operation is terminal. The operation and case are kept as business records (lawful basis per Compliance) | Operation row | DPO process. The deletion job waits for terminal states |
| Model retirement announced | No customer impact | — | Planned re-baseline release (G11 calendar) |
| Rollback | Previous revision serves. Drafts stay readable if the session schema is compatible | Operations untouched | Release owner. Schema compatibility rehearsed in G09 |
| Incident needs attribution | Trace ID → session ID → stored events reproduce the turn | Content-free telemetry plus session store | On-call runbook (G10) |

## Verification and implementation handoff

- **Offline deterministic** (most invariants): fake model scripts, fake core
  with configurable replay, timeout and lookup semantics, and real
  eligibility, tools and confirm code. Assertions cover attempted calls,
  stored rows and the absence of forbidden effects.
- **Local integration:** a real Postgres process restart. Concurrent turns.
  The gateway contract tested with a real HTTP client.
- **Bounded live:** Vertex EU model calls in an isolated non-prod project with
  a declared call and cost cap. The core banking **test** environment (D-02).
- **Release and operation:** load test (G12), a staff pilot, then a 1–5%
  customer pilot with SLIs, a rollback rehearsal and an erasure check.
- **Product outcome** (separate from model quality): follow-up contact rate on
  filed cases versus the D-03 baseline, back-office reclassification rate,
  handoff rate and complaints. This is a hypothesis until the pilot data
  exists.
- **Observability:** SLIs are completed-dispute ratio (sessions that reach
  `SUBMITTED` out of sessions with a saved eligible draft), tool error rate by
  tool, `UNCERTAIN` age, tokens per completed dispute, and turn latency.
  There is one telemetry owner per process, content capture is off, and trace,
  invocation, session and operation IDs are carried on every hop.
- **Release bundle:** image digest, prompt version, model ID, judge ID, tool
  schema hash, eval-set hash, rule-table version and secret versions, recorded
  in a release manifest. The gate is deterministic tests plus eval thresholds
  by exit code. The canary is a Cloud Run traffic split, with thresholds set
  before traffic moves. The previous revision is kept for 7 days.

Goals, routes and run prompts are in the [implementation plan](../plans/card-dispute-agent.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| D-01 EU-region availability and quota of `gemini-3.8-flash` on Vertex, SDP, Model Armor and Cloud SQL. Dated prices | Region choice, residency claim, cost estimate | Platform engineer: official docs lookup with URLs and dates | G09 (deploy). Local goals are not blocked |
| D-02 Core banking dispute API: idempotency key support, lookup by client reference, fields, error codes, rate limit, SLA, test environment | I3 is only as strong as the provider replay contract | Core banking integration team: written API contract plus a test in their test environment | Live part of G04. Offline G04 proceeds against a fake |
| D-03 Rule table (reason codes, time windows, required facts per reason, languages), a baseline follow-up rate, and about 60–100 anonymised labelled historical disputes | The classification target and eval set | Disputes ops + Compliance | G02 rules content, G03 |
| D-04 Step-up mechanism and app-shell embedding (web view or native) | Confirmation binding and frontend contract | Mobile and identity teams | G07 |
| D-05 Cloud Run vs bank-standard GKE | Deployment goal shape | Platform architecture board | G09 |
| D-06 Retention periods and lawful basis for keeping operation records after chat erasure | Data table, deletion job | DPO | G13 |
| D-07 Whether the AI Act transparency wording and model-risk classification need formal MRM approval before pilot | Pilot gate | Compliance / MRM | G12 |

No decision in this document has been accepted by the user. Design completion
and implementation authorization are separate. This session was design-only.
