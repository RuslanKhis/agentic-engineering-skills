# System design: home-insurance claim intake agent (EU)

Status: **draft**. Nobody was available to answer questions during this design session, so every
decision marked *provisional* depends on an assumed answer in the table below.
Nothing here has been implemented, provisioned or tested.

Decisions and their rationale live here. The [plan](../plans/home-claim-intake.md)
holds the estimates, owners, schedule, capacity and cut line. The
[tickets](../tickets/home-claim-intake/) hold each phase 1 goal's scope and acceptance.

## Assumed answers

Every row is a question that would normally have gone to the product owner. Decisions that depend on a row are
provisional until someone confirms it.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | What does "GA in the EU" mean: which date, which markets? | GA on **2027-03-15** for one market, **Germany**, open to all home-policy customers in the web portal. After GA the service keeps running and gets new features. | D15, plan calendar (100 working days) |
| A2 | Which languages at GA? | German and English | D15, G09 eval set, G11 |
| A3 | How familiar is the team with ADK and GCP? | Experienced with Python and GCP, **new to ADK**. The ×1.5 multiplier is already in every estimate. About 5 focused hours a day per full-time person. The security reviewer works about one day a week (≈1.2 focused h/day). | Plan capacity |
| A4 | What money is available for models and cloud? | About €3,000 a month for non-production during the build. In production, a target of at most €0.50 in model cost per completed claim. This is an *illustrative assumption*, not a budget the user gave. | D8, D11, G20 |
| A5 | Who uses it and how do they sign in? | Authenticated policyholders in the existing customer web portal. The portal's OIDC identity provider (CIAM) issues tokens that contain a stable customer ID. Web only at GA. | D6, D9 |
| A6 | What data does it touch, and what may it change? | Personal data: name, address, contact details, policy number, loss description. Home photos, which may show people or documents, so special-category data can appear by accident. The only external write is a new FNOL claim, with its photos, in Guidewire ClaimCenter. No payments and no coverage decisions. | Profile, D3, D4, D10 |
| A7 | How is Guidewire reached? | ClaimCenter on Guidewire Cloud through its Cloud API (REST): draft claim, then submit, then documents. The calls go through the company API gateway with OAuth2 client credentials. A sandbox tenant is available on request (wait W2). The idempotency and lookup semantics are **unknown** and are discovery goal G02. | D4, G02, G10, G23 |
| A8 | Where do policy details come from? | A read-only policy-summary API behind the same gateway that returns a customer's home policies by customer ID | D6, G05 |
| A9 | Is there an existing GCP organisation? | Yes. An org policy restricts resource locations to the EU, and a platform team creates projects and org-level IAM (wait W5). | D7, G04 |
| A10 | May Gemini on Vertex AI in an EU region process claim data? | Yes, subject to the DPIA (wait W1). Customer data is not used for model training. | D7, D8, W1 |
| A11 | What should the assistant never do? | Never assess coverage, liability or payout amounts. Never act for anyone other than the signed-in policyholder. | I4, D12 |
| A12 | What does success look like, and what is the baseline? | The share of digital first notices of loss (FNOLs) that need no adjuster callback for missing information, the time to file, and the abandonment rate. The baseline is unknown and is measured on the existing web form during the pilot (G27). | Outcome measurement |
| A13 | How long is data kept? | Drafts, sessions and our copies of photos: 30 days after confirmed submission or abandonment. Guidewire's retention then governs the claim. | D10, G12 |
| A14 | What availability and traffic should it handle? | 99.5 % monthly availability for the submission path. About 3,000 home claims a month in the market, with storm peaks of 1,000 a day. *Illustrative assumptions.* | Budgets, G20 |
| A15 | Who operates it after GA? | The same team in business hours. The platform team covers infrastructure around the clock. Submissions are durable, so a night-time outage delays a claim but does not lose it. | D4, G22 |

## Purpose and constraints

**Journey (running example).** Anna, a policyholder in Cologne, finds water
coming through her kitchen ceiling from a burst pipe upstairs. Today she either
phones the claims line, which means a queue and about 20 minutes, or fills in
a long web form and emails photos separately. An adjuster then often calls her back for a missing
date, cause or room list. With this product she opens "Report damage" in the
portal and chats with the assistant, which asks only what is still missing.
She uploads four photos, and the assistant describes the visible damage back to her.
She checks a summary rendered from the claim draft and confirms it. A claim with
the photos attached appears in ClaimCenter, and she sees her claim number. If
she says water is still pouring or mentions a gas smell, she is first shown the emergency
numbers.

**Model contributes:** a natural conversation, extraction of structured FNOL
fields from free text, follow-up questions for missing fields, a descriptive
summary of visible damage in photos, and German/English phrasing.

**Ordinary code controls:** identity and policy scope, draft validation and
completeness, the emergency rule, confirmation, the Guidewire write and
reconciliation, photo storage and limits, budgets, retention and the public
review screen.

**Non-goals at GA:** coverage or payout statements, fraud scoring,
contents/inventory claims, claim status follow-up, mobile app, video, live
handoff to a human chat agent, other markets.

**Observed repository facts:** the repository has no application code. It
contains only `.claude/skills/`, so this is a greenfield design. No ADK version
is installed.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | GA 2027-03-15 (A1). A limited-customer pilot comes first. The service continues after GA. |
| People and hours | Five engineers (roles Lead, Integration, Platform, Frontend, Agent), one ML engineer, a part-time security reviewer (A3). They operate it afterwards (A15). |
| Money | Illustrative allowance in A4 |
| Users or judge, and what they read | External customers use the running service. Adjusters read the claims it creates. The DPO, security and the business read the DPIA, pen test and pilot results. |
| Data touched and effects allowed | Personal, insurance-regulated data and photos. It creates one record in the system of record, which starts a claims process (A6). |
| Delivery profile | **Production service.** External customers, regulated personal data and writes to the system of record. Phase 1 = GA. |

Depth per concern now (*Build* means phase 1 implements and tests it):

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: labelled DE/EN eval set, gated in CI (G09, G17, G19) | New market or model → re-baseline |
| Identity and per-customer scope | Build (G05) | Delegated access (brokers, co-insured) |
| Secrets and credentials | Build: workload identity, Secret Manager, rotation of the Guidewire client secret (G04, G24) | — |
| External writes | Build: confirmation-bound, idempotent, reconciled (G10, G23) | Provider replay contract proves stronger or weaker (G02) |
| Sensitive data | Build: minimisation, no content in telemetry, retention, erasure (G12) | DPIA conditions (W1) |
| Prompt injection and agency | Build: structural split, threat model, adversarial suite, two security reviews, pen test (G13, G14, G25, W3) | New tool or data source |
| Budgets and loop limits | Build: per invocation, session, customer and global kill switch (G15) | Storm-peak cost measured above A4 |
| Memory and retrieval | Minimal: sessions plus an application draft record only. No long-term memory and no RAG. | Claim status follow-up (phase 2) |
| Frontend | Build: widget in the existing portal (G11) | Mobile app (phase 2) |
| Hosting | Build: Cloud Run with rollback, separate prod (G04, G24, G22) | Second region needed for RTO |
| Observability | Build: SLIs, alerts, runbooks (G16, G22) | — |
| Release engineering | Build: manifest, eval gate, canary and joint rollback (G17, G21) | — |
| Performance and cost tuning | Defer until measured (G20 measures) | Measured p95 or cost per claim above target |

**Floor:** no secrets in code, prompts or logs. A spend stop (D11). No
Guidewire write without the customer's explicit confirmation of the exact draft
(D3). Real customer data only after the DPIA (W1) and only in the EU. Pinned model ID (D8).

**Who may use it before GA:** the team and internal staff on synthetic data in
staging (G18). Then a limited-customer pilot behind a feature flag (G21), only
after DPIA sign-off, both security reviews and the eval gate pass.

**Graduation conditions for GA (G26):** pilot quality and safety thresholds met (G27),
pen-test critical/high findings fixed (W3), operational readiness rehearsed (G22),
legal wording approved (W6).

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Context caching and cost tuning | No measured traffic yet | G20 or production cost per claim above A4 |
| Multi-region failover | Durable outbox means outages delay but do not lose claims | RTO requirement below 4 h |
| Production-to-eval sampling pipeline | Needs DPIA terms for reuse of production content | DPIA allows it; first post-GA release |
| Claim status in chat | Requires a second, read-only Guidewire scope | Phase 2 (P2-01) |

Capacity, finish range and cut line: see the [plan summary](../plans/home-claim-intake.md#summary-for-the-reader).

## Guarantees and acceptance

| ID | Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer reads or changes only their own sessions, drafts, photos and submissions | Request middleware derives `customer_id` from the verified OIDC token. Every repository query and signed-URL issue is keyed on it. A session ID only locates a session and grants nothing. | 404 (not 403) for someone else's IDs. Nothing is disclosed. | G05/G07 cross-customer denial tests. G13 adversarial cases. |
| I2 | A Guidewire claim is created only for a draft version the customer confirmed | The confirm endpoint stores `(draft_id, version, sha256(canonical payload))`. The worker re-loads the draft and refuses on a hash mismatch. The model has no submit tool. | A changed draft needs a new confirmation | G10 tests: edit-after-confirm and a scripted model that tries to submit |
| I3 | One confirmed draft produces at most one ClaimCenter claim | `SubmissionOperation` row is unique on `draft_id`. Our operation ID is written to a Guidewire reference field, and a lookup runs before any re-create. *Provisional until G02 confirms the lookup semantics.* | `uncertain` state is shown to the customer as "being confirmed". It is reconciled, never blindly re-sent. | G10 fake-provider tests (timeout after commit, duplicate click, worker restart). Sandbox replay in G10. |
| I4 | The assistant never states coverage, liability or payout amounts | Instruction plus an output check in `after_model_callback`. The eval set has refusal cases. The review screen shows draft fields only. | A neutral "an adjuster will assess this" message | G09/G19 eval metric = 0 violations on the refusal subset. G27 pilot sample. |
| I5 | Photo or text content cannot cause any effect outside the customer's own draft | Structural (D5): the photo analyser has no tools. The intake agent's only write tool is scoped to the session's draft. Submission is not a tool. | The injected instruction is ignored or recorded as data | G13 suite: text-in-image injection, a hostile description, and a cross-draft argument. The forbidden call is asserted absent. |
| I6 | Customer content never reaches logs or traces, and all stored and processed data stays in EU regions | Content capture off (D14). Structured logs carry IDs only. Org location policy. EU Vertex endpoint (D7). | — | G16 exporter test with sentinel PII. G12 data-flow residency checklist. G25 review. |
| I7 | Spend and work are bounded | `RunConfig.max_llm_calls`, a session turn cap, a per-customer daily allowance in Cloud SQL, and a global kill switch (D11) | Polite stop that points to the web form or phone line. Drafts are kept. | G15 tests. G20 load test. |
| I8 | Every uploaded photo is attached to the claim exactly once, or the claim is flagged for an adjuster | `PhotoAttachment` rows keyed `(operation_id, photo_sha256)` with per-row state (D4) | The customer sees the claim number plus "photos still uploading". After the retry budget, the claim gets a note for the adjuster. | G23 tests. Partial failure. Restart. |
| T1 | Submission success ≥ 99 % of confirmed drafts within 15 min (provisional) | SLI in G16 | Alert, then runbook in G22 | G21 pilot measurement |
| T2 | Time to first streamed token p95 ≤ 4 s; review screen ready ≤ 2 s after the last answer (provisional) | Measured in G20 | — | G20 |

## Architecture and decisions

```text
Browser (portal widget, G11)
   │ OIDC bearer token (portal CIAM)            ┌───────── trust boundary: our GCP project (EU) ─────────┐
   ▼                                            │                                                        │
Company API gateway ──► Cloud Run "claim-intake-api" (FastAPI around ADK Runner)                         │
                         │ middleware: verify token → customer_id (trusted state)                        │
                         │ ├─ /chat (SSE)  → Runner(App: intake LlmAgent)                                │
                         │ │      tools: get_my_home_policies (read, scoped)                             │
                         │ │             update_claim_draft (write to own draft only)                    │
                         │ │             request_photo_analysis (calls quarantined analyser, no tools)   │
                         │ ├─ /photos     → signed upload URL → GCS bucket (EU, CMEK optional)           │
                         │ ├─ /draft      → render review from ClaimDraft record                         │
                         │ └─ /confirm    → SubmissionOperation(PENDING) + Cloud Tasks enqueue            │
                         ▼                                                                               │
   Cloud SQL Postgres: ADK sessions │ claim_drafts │ submission_ops │ photo_attachments │ allowances     │
   Cloud Tasks ─► Cloud Run "claim-submit-worker" ──(OAuth2 client creds, Secret Manager)──► API gateway ─► Guidewire ClaimCenter Cloud API
   Vertex AI Gemini (EU region) ◄── intake agent, photo analyser                                         │
   Cloud Trace / Monitoring / Logging (no content)                                                       │
                                                                                                         └─┘
```

**Confirm sequence:** the customer presses Confirm on the review screen. The API
re-validates the draft and computes its canonical hash. It inserts
`SubmissionOperation{op_id, draft_id, version, hash, state=PENDING}`, which is
unique on `draft_id`, so a second click returns the same `op_id`. It enqueues a
Cloud Tasks task named by `op_id` and returns `202 {op_id}`. The browser polls
`/submissions/{op_id}`. The worker:

1. Claims the row with a version check.
2. Looks up a claim by external reference = `op_id`.
3. If none exists, creates the draft claim and submits it.
4. Records `claim_number`, then `state=CREATED`.
5. Enqueues photo attachments (G23).

A timeout or ambiguous 5xx sets `state=UNCERTAIN`, and the reconciler repeats
the lookup. It never sends a fresh create without a lookup that came back empty.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Conversational intake with a few capabilities | **One `LlmAgent`** (intake) plus deterministic code. The photo analyser is a separate tool-less model call (D5), not a sub-agent. | Language work needs one agent. Everything else is rules. Fewer routing contracts to test. | Multi-agent (triage, intake, summariser) adds routing failures for no distinct authority | Captured request shows 3 tools and one instruction | Proposed |
| D2 | The submitted claim must be what the customer saw | An **application-owned `ClaimDraft` record** (versioned, typed fields, completeness computed in code). The model edits it only through `update_claim_draft`. The transcript is not the source. | One authority for the review screen and submission | Extra schema and migration work compared with parsing the chat | G06: restart mid-conversation, and the draft and its completeness survive | Proposed |
| D3 | No claim without informed consent (I2) | **Submission is not a model tool.** The UI Confirm action hits `/confirm`, which is bound to the draft version and hash. | The model cannot be talked or injected into submitting. ADK tool confirmation is unnecessary. | One extra click, and the agent cannot "just file it" | G10 scripted-model test: the model asks to submit and no operation row appears | Proposed |
| D4 | At most one claim, no lost claims (I3, I8) | **Durable outbox**: `SubmissionOperation` plus Cloud Tasks worker, lookup-before-create on an external reference, `UNCERTAIN` state with reconciler, and per-photo attachment rows | Survives browser close, worker restart and a Guidewire outage | Asynchronous UX ("we're filing your claim") and a lookup call per attempt. Alternative: a synchronous call in the chat request loses claims on timeout. | G10/G23 fake-provider matrix, sandbox replay | **Provisional** on G02 (A7) |
| D5 | Photos are untrusted content (I5) | **Quarantined photo analyser**: a model call with `output_schema` (damage types, rooms, visible-severity band, quality issues, `not_damage_photo` refusal), no tools and no draft access. Code copies the validated result into the draft as data. | Removes the write leg from the agent that reads images | Extra model call per photo batch, and the analysis cannot ask questions | G08 schema tests (prose, fenced JSON, wrong-but-valid). G13 text-in-image case. | Proposed |
| D6 | Per-customer scope (I1) | Verify the portal OIDC token in middleware. Set `customer_id` in trusted session state at session creation and check it on every request. Tools read scope from `tool_context.state`, never from arguments. A `before_tool_callback` checks that the draft belongs to the session's customer. | Authority stays in code the model cannot reach | Depends on CIAM token claims (A5) | G05 denial tests with two customers | Provisional on A5 |
| D7 | EU residency, team's GCP skills | **Cloud Run** (europe-west3 assumed) for API and worker. **Vertex AI** Gemini in an EU region. **Cloud SQL Postgres** for ADK `DatabaseSessionService` and app tables. **GCS** EU bucket. **Cloud Tasks**, **Secret Manager**. | Cloud Run gives us our own middleware, SSE and traffic splitting. One Postgres keeps drafts, operations and sessions transactional together. | Agent Runtime would manage sessions but makes custom auth middleware and the outbox worker separate pieces. GKE is too much to operate for 5 people. | G01 confirms region availability of each service and model. G18 readback. | Provisional on G01 |
| D8 | Stable, pinned model that outlives the plan | **`gemini-3.8-flash`** for intake and photo analysis. Stable since 2026-09-02, no Gemini API shutdown announced, no Vertex retirement listed in the 2026-10-08 snapshot. Judge pinned to the same ID with a separate prompt. Avoid `gemini-3.7-flash` (Vertex retirement 2027-01-28, before GA) and `gemini-3.6-flash` (2026-11-19). Fallback candidate `gemini-3.5-flash` (Vertex retirement "2027-05-19 or later": a migration two months after GA). | Longest expected life inside the horizon | The newest model has the least field history. Its EU regional availability is unverified. | G01: model listed in an EU region with image input and `output_schema`. Release manifest has no alias. | **Provisional** (source: `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`, checked_on 2026-10-08) |
| D9 | Customer UX in the existing portal | **Custom JSON API + SSE** for assistant text. Tool activity is shown as status chips. The **review screen is rendered from the draft record**, not model text. | The review must show exactly what is submitted | Building our own widget rather than adopting AG-UI. The portal stack is unknown. | G11 browser test: a streamed reply, then a review screen that matches the stored draft | Proposed |
| D10 | GDPR minimisation and residency (I6) | Strip EXIF GPS and device data from the copy sent to the model and keep the original for Guidewire. No content in logs or traces. 30-day retention jobs. An erasure path covers sessions, drafts, photos and operations. Screen user text with **Model Armor** (injection/jailbreak) as a layer behind D3/D5. *Model Armor EU availability is unverified.* | Least data at each boundary | Screening adds latency and a dependency that can fail. It **fails closed** for that turn ("please rephrase / call us"). | G12 data-flow table and erasure test. G16 sentinel test. | Provisional on W1 |
| D11 | Spend bounded (I7) | `max_llm_calls=12` per invocation, 40 turns per session, ≤10 photos of ≤15 MB, ≤3 new drafts per customer per day in Cloud SQL, and a global kill switch flag read per request. Billing budget alerts only *observe* spend. | Admission is enforced in code | Legit heavy users can hit limits. They are routed to the phone line. | G15 tests for each limit and the kill switch | Proposed (numbers are assumptions) |
| D12 | Safety and fallback | A deterministic emergency rule (keywords plus a model flag) shows emergency numbers before anything else. "Call us" is always visible. The agent never states coverage (I4). The AI disclosure is shown (EU AI Act Art. 50 transparency, *to be confirmed by legal, W6*). | Life safety must not depend on model judgment alone | Some false-positive emergency banners | G09 emergency subset recall = 100 % on labelled cases | Proposed |
| D13 | Comparable, reversible releases | Release manifest (image digest, prompt version, model and judge IDs, tool-schema hash, eval-set hash, secret versions). Deterministic gate on every PR, model eval gate before promotion. Cloud Run traffic split for pilot and canary, with joint rollback. | A prompt and the model it was tested with move together | CI cost per eval run | G17 gate fails by exit code. G21 rollback rehearsal. | Proposed |
| D14 | Diagnose incidents without content | One OpenTelemetry owner per process → Cloud Trace/Monitoring. ADK content capture **off**. Session, invocation and op IDs on every span and log. SLIs: submission success, uncertain-operation age, turn latency, tool error rate by tool, tokens per completed claim. | An alert leads to a session ID without exposing PII | Debugging needs a separate, audited session read | G16 in-memory exporter test | Proposed |
| D15 | German market at GA | DE and EN instructions plus eval cases. Answer in the customer's language. Field values are normalised by code. | Scope limited to A1/A2 | Another market = new eval cases and legal wording (P2-02) | G09 per-language metrics | Provisional on A1/A2 |

**Versions.** No ADK version is installed. The working assumption is
`google-adk==2.8.0`, the version the specialist skills were checked against
(each specialist's `references/compatibility.md`). The observability
specialist recommends ≥2.10.0 for a new production deployment. Confirming the
pin is an acceptance item of G03. Provider facts (regions, Model Armor, Cloud
Tasks, Guidewire API) could not be looked up in this session (no network). G01
and G02 verify them and record their sources and dates.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | Intake agent: gather the FNOL fields still missing from the draft, one question at a time. Describe photos only via the analyser result. Never assess coverage. Answer in the customer's language. Identity, date, policy list and limits come from code via state templating, not the prompt text. | `adk-agent-instructions`; rendered-request test (G06) |
| Tool interfaces | `get_my_home_policies()` (read, no args, scope from state). `update_claim_draft(fields)` (write, own draft only, returns `{status, missing_fields, errors}`). `request_photo_analysis(photo_ids)` (read, photo IDs validated against the draft). Three tools in total. No submit tool. Results capped at 2 KB. | `adk-tool-interface-design`; declaration dump (G06, G08) |
| Output contracts | Photo analyser `output_schema` with refusal shape `not_damage_photo`/`unreadable`. Repair budget of 1, then "couldn't analyse; an adjuster will review the photo". Intake agent: free text plus tool calls, with the I4 check in `after_model_callback`. | `adk-model-and-output-contracts`; scripted invalid-output test (G08) |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | CIAM | Middleware reads it | Token, verified per request | Not stored beyond `customer_id` |
| Policy summary | Policy API (authoritative) | Read tool | Per session, not cached across sessions | Session lifetime |
| ADK session events | Our Cloud SQL, per customer | Runner | — | 30 days (A13), then erased |
| ClaimDraft | Our Cloud SQL, per customer, versioned | `update_claim_draft`, photo analyser result (code), review API | Authoritative until submission | 30 days after submission or abandonment |
| Photos | GCS EU bucket, object path `customer/draft/photo` | Upload URL (customer), analyser (model copy), worker | — | Lifecycle rule 30 days after confirmed attachment. Erasure job. |
| SubmissionOperation / PhotoAttachment | Our Cloud SQL | API, worker, reconciler | Guidewire is authoritative for claim existence | 1 year for audit (assumption; DPIA) |
| FNOL claim | Guidewire ClaimCenter | Worker (service identity via gateway) | Authoritative | Insurer's retention |

Three identities: the customer (OIDC subject), the workload (Cloud Run service
accounts: `intake-api`, `submit-worker`, each with least privilege), and the
Guidewire API client (client credentials, used only by `submit-worker`). The
intake service account cannot read the Guidewire secret.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Intake agent | Yes (policy, draft) | Customer text (the customer acts on their own claim) | Writes only its own draft. No egress and no submit. | The external-write leg is removed (D3). The draft-write scope is checked in `before_tool_callback` (D6). |
| Photo analyser | Photo content | Yes (images can carry text) | None | Tool-less, schema-validated output (D5) |
| Submit worker (code) | Yes | Draft fields (validated) | Guidewire write | Not an agent. Bound to the confirmed hash (I2). |

Tool tiers: read (policies, analysis) and scoped write (draft). The
irreversible effect (claim creation) is code-only behind customer confirmation.
There is no code executor. The adversarial suite (G13) asserts that the
forbidden calls never run. OWASP LLM01/LLM06 mapping is in G13.

## Budgets and capacity

- **Per completed claim (symbolic):** turns ≈ 12–20. Each turn is ≤2 model
  calls with a stable instruction and tool prefix of about 3–4k tokens plus
  history, with a 1 photo-analysis call per batch of ≤5 images. Cost =
  Σ(input tokens × in-price + output tokens × out-price) for
  `gemini-3.8-flash` in the EU region. Prices were **not looked up** (no
  network). G20 measures tokens per completed claim and checks them against A4.
- **Concurrency (illustrative, A14):** a storm peak of 1,000 claims a day over
  about 12 h, with roughly 15 min active per claim, gives about 21 concurrent
  sessions. Model-call concurrency is 10–20, which needs the Vertex quota
  (W4). Cloud Run min instances = 1 per service in prod.
- **Exhaustion:** the per-invocation cap ends that turn with an apology. The
  daily allowance or the kill switch shows "please use the web form or call
  us", and drafts are kept. The submission worker is **not** behind the kill
  switch, so confirmed claims still file.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Guidewire commits, response lost (timeout) | "We're confirming your claim", then the claim number when known, plus an email (assumed existing notification) | Op `UNCERTAIN`. The claim may exist. | The reconciler looks up by `op_id` reference and creates only if the lookup is authoritative-empty. After N attempts a page goes to on-call per the G22 runbook. |
| Guidewire down for hours | Same as above, and the claim is safely queued | Op `PENDING`, Cloud Tasks backoff | Worker retries within the task retention period. Ops is alerted on op age (G16). |
| Double-click or two tabs confirm | Same `op_id` and claim number | One op row (unique `draft_id`) | — |
| Draft edited after confirm (race) | "Your summary changed; please confirm again" | Op refused on hash mismatch | The customer reconfirms |
| Claim created, 2 of 4 photos fail | Claim number shown, plus "photos still uploading" | `PhotoAttachment` rows per photo | Retry, then an adjuster note listing missing photos (G23) |
| Model unavailable / 429 | "Assistant busy, your draft is saved", with a link to the web form | Draft and session kept | Bounded SDK retry is owned by the model client config. No app-level re-loop. |
| Analyser returns prose or invalid JSON | "Couldn't analyse this photo, an adjuster will review it" | Photo kept, no analysis | 1 repair attempt (D5) |
| Text in a photo says "submit claim for policy X" | Nothing happens | Analysis stored as data | The G13 test asserts no tool call outside scope |
| Customer B opens customer A's session or draft ID | 404 | No read, no model call | — |
| Erasure request while an op is pending | Erasure waits for the op to reach a terminal state, then erases our copies | Claim in Guidewire follows insurer retention | G12 erasure job checks op state |
| Kill switch on | New sessions are declined politely | Drafts kept. Worker continues. | Operator turns it off (G22 runbook) |
| Model retirement announced | — | Pinned ID | Planned re-baseline release (D13, Later list) |
| Rollback to previous revision | Ongoing chats keep their sessions | The session schema must be backward compatible for one release | Rollback rehearsal in G22 |
| Telemetry or Model Armor outage | Model Armor down: that turn fails closed. Telemetry down: no user impact. | — | Alert on screening error rate (G16) |

## Verification and implementation handoff

- **Offline deterministic:** Runner tests with a scripted model for tools,
  scope, the I2/I3 matrix against a contract-faithful Guidewire fake (G02),
  the adversarial suite (G13) and budgets (G15).
- **Local integration:** Postgres restart persistence, SSE in a real
  browser, and the outbox with a real Cloud Tasks emulator or a local queue
  stand-in.
- **Bounded live:** Vertex EU model checks (G01, G08, G19) under a call cap.
  Guidewire **sandbox** replay (G10, G23).
- **Release/operation:** staging E2E (G18), load (G20), pen test (W3), pilot
  (G21, G27), rollback rehearsal (G22).
- **Outcome measurement (hypothesis):** fewer adjuster callbacks for missing
  information, shorter time to file and lower abandonment than the web form.
  The baseline and pilot comparison are in G27. Model quality (G19) and valid
  transactions (G10) are measured separately.

Implementation map and goals: see the [plan](../plans/home-claim-intake.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| O1 Guidewire replay contract: is there idempotency or a searchable external reference on claims? | Decides whether I3 is a guarantee or "at most one, reconciled manually" | Integration + Guidewire team. Sandbox test (G02, W2). | G10 final design |
| O2 `gemini-3.8-flash` (or the fallback) in the chosen EU region with image input and `output_schema` | D8 and residency | G01 lookup on the official Vertex model and region pages | G08, G19 |
| O3 ADK pin: 2.8.0 versus ≥2.10.0 | Telemetry fixes and API names | G03 | — |
| O4 CIAM token claims and the portal's frontend stack | D6, D9 | Portal team (G01, G11) | G05, G11 |
| O5 Model Armor availability and terms in the EU | D10 screening layer | G01 | G12 |
| O6 All assumed answers A1–A15 | Scope, calendar, budgets | Product owner | Plan confirmation |
| O7 Should phase 1 absorb some of the spare engineering hours? See the plan summary. | Cut line | Product owner | — |

None of the decisions above has been accepted by the user yet. Design review
and implementation authorisation are separate. This document authorises no
implementation or cloud work.
