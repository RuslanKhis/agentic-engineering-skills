# System design: home-insurance claim intake agent (EU)

Status: **draft**. Written in one pass without the user; every answer marked
*assumed* in [Assumed answers](#assumed-answers) is provisional, and the
decisions that depend on it are marked provisional too. Nothing here is
user-accepted yet.

Decisions and their rationale live here. Estimates, owners, the finish range,
the cut line and the largest risks live in the
[plan](../plans/home-claim-intake.md#summary-for-the-reader); goal scope and
acceptance live in the [tickets](../tickets/home-claim-intake/).

## Assumed answers

| # | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Which EU countries and languages at GA? | One market, two languages (the local language and English) | D8, eval set size (G07, G24) |
| A2 | Which Guidewire product and interface? | ClaimCenter on Guidewire Cloud, Cloud API (REST, `claim/v1`), OAuth client credentials via Guidewire Hub; a non-prod tenant exists and access must be requested | D3, D4, G01 |
| A3 | Is there a customer portal and login to reuse? | Yes: an existing web portal with an OIDC customer-identity (CIAM) provider; the agent is a panel inside it. Mobile app later | D5, D8 |
| A4 | Does the agent decide or state coverage, liability or payout? | No. First notice of loss (FNOL) intake only; coverage and settlement stay with claims handlers | D1, D10, I1–I4 below |
| A5 | Volume and peaks? | About 60,000 home claims a year (~250 a working day); a storm day can bring 10×; design for 200 concurrent conversations | Budgets, G20 |
| A6 | Model and cloud budget? | Model spend target ≤ €0.40 per submitted claim; non-prod cloud ≤ €3,000/month; prod budget set by finance after G20 | D11 |
| A7 | Must every processing step, including model inference, stay in the EU? | Yes, strictly: regional EU endpoints only, never a global endpoint | D6, D7, open O1 |
| A8 | Team familiarity? | Strong Python, GCP through an existing landing zone, new to ADK (×1.5 on estimates) | Plan estimates |
| A9 | May historic claim photos be used for evaluation? | Not before the DPIA: staged and synthetic photos plus consented employee photos; real pilot data only after DPIA sign-off | G07, G24, G22 |
| A10 | Who signs off DPIA, pen test and go-live? | DPO signs the DPIA; an external vendor runs the pen test; the internal change board approves go-live | Plan waits W6–W8 |
| A11 | Is there a fallback channel? | Yes: the existing web claim form and the phone line | D11, failure rows |
| A12 | Is there a malware-scanning service for uploads? | No; uploads are decoded and re-encoded server side, and only JPEG, PNG and HEIC are accepted | D9 |
| A13 | Accessibility and AI-transparency requirements? | WCAG 2.1 AA; a visible notice that the customer is talking to an AI (EU AI Act Art. 50); legal approves wording | G12, W4 |
| A14 | GA service targets? | Provisional: agent API available 99.5% monthly; ≥ 99% of confirmed drafts reach a Guidewire claim number within 5 minutes outside Guidewire outages; p95 agent turn ≤ 8 s | Guarantees, G16 |
| A15 | Retention? | Sessions 90 days; our photo copies deleted 30 days after successful attachment; submission ledger 2 years (IDs and hashes only); DPO confirms in the DPIA | D12, G13 |
| A16 | Where do claim documents live? | Attached through the ClaimCenter Cloud API documents endpoint, which stores them in the insurer's document system | D3, G01 |
| A17 | Submitted claim or draft for triage? | A submitted FNOL claim, flagged with channel "digital assistant" and an AI-summary note kept separate from the customer's own statement | D3 |
| A18 | Is a pen test required before real customers use it? | Required before GA; an invite-only pilot may run during the pen test after the internal security review passes (open O3) | Plan cut line |

## Purpose and constraints

**Journey (running example).** Maria, a signed-in policyholder, finds water
coming through her kitchen ceiling. Today she fills in a long web form or waits
on the phone; photos go by email and are matched by hand, and handlers often
call back for missing facts. With the agent she describes what happened in her
own words, uploads four photos, answers two follow-up questions, reviews a
summary card, presses **Submit**, and sees claim number `HC-…` in under ten
minutes. The handler receives a complete FNOL with photos attached.

**Outcome to improve (hypothesis, measured in G22):** fewer handler
call-backs for missing information and higher digital completion, without a
rise in handler corrections. Baseline: the current web form's completion rate
and call-back rate, to be supplied by claims operations (open O6).

**Non-goals:** coverage decisions, settlement estimates, fraud scoring, claim
status follow-up, other lines of business, mobile app, voice.

**What the model contributes:** understanding the customer's account, asking
for missing facts, describing visible damage in photos, and drafting a
structured claim. **What code controls:** who the customer is and which
policies they hold, which fields are required, emergency signposting, the
summary the customer confirms, the Guidewire write, idempotency, budgets and
release.

**Repository facts.** The repository is empty apart from the skills; there is
no existing code, convention or dependency pin. Everything below is proposed.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | GA in the EU five months from start (assumed start 2026-10-19; 95 working days); launched and continued |
| People and hours | Five engineers and one ML engineer full time (≈5 focused h/day each), one security reviewer part time (≈2 h/day); new to ADK (A8); the same team runs it after GA with on-call |
| Money | A6 (assumed) |
| Users or judge, and what they read | External customers using it to file real claims; claims handlers reading the resulting claims |
| Data touched and effects allowed | Personal data of policyholders, policy details and home photos (may incidentally show people or health items); creates claim records in Guidewire that start a payout process |
| Delivery profile | **Production service**: external customers, personal data and a write to the system of record that leads to money |

Depth per concern (production column of the delivery profiles, adjusted):

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: eval set (G07, G24) with CI gate (G17) | — |
| Identity and per-customer scope | Build: OIDC in middleware, policy entitlement from Guidewire (G04) | — |
| Secrets | Build: workload identity, Secret Manager, rotation of the Guidewire client secret (G03) | — |
| External writes | Build: confirmation in UI, durable ledger, idempotency, reconciliation (G09, G10) | — |
| Sensitive data | Build: field minimisation, no content in telemetry, retention and erasure (G13) | Model Armor screening added if G14 or the pen test shows a bypass |
| Prompt injection and agency | Build: structural split, capability checks, adversarial suite (G14) | — |
| Budgets | Build: per-invocation cap, per-customer allowance, operator kill switch (G11) | Shared token budget across replicas if G20 shows cost spikes |
| Memory | Minimal: session plus a resumable claim draft; no cross-session memory | A customer need for "continue another claim" |
| Frontend | Build: panel in the existing portal (G12) | — |
| Hosting | Build: Cloud Run in one EU region with rollback (G03, G17) | Multi-region if A14 availability is raised above 99.5% |
| Observability | Build: traces, SLIs, alerts (G16) | — |
| Release | Build: manifest, CI gate, canary, joint rollback (G17) | — |
| Performance and cost tuning | Defer until G20 measures | p95 turn > 8 s or cost > A6 |

**Floor kept:** no secrets in code, prompts or logs; `max_llm_calls` per
invocation plus an application allowance and an operator stop; nothing reaches
Guidewire without the customer pressing Submit on a summary rendered from the
stored draft; real customer data only after DPIA sign-off, kept out of logs;
pinned model ID. No accepted risks yet; O3 would add one.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Model Armor input screening | The structural split already prevents injected writes; adds latency and an EU-availability check | Adversarial suite or pen test finds a bypass |
| Multi-region failover | 99.5% target met by one region plus the form fallback | A higher availability target |
| Context caching and cost tuning | No measured traffic yet | G20 cost or latency over target |
| Semantic memory across claims | No journey needs it | Product asks for "your previous claims" |

## Guarantees and acceptance

| ID | Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer reads and files only against policies they hold | Auth middleware derives `customer_id` from the verified OIDC token; entitlement lookup in Guidewire; tools receive scope from trusted state, never from arguments | 403 and no model call | Cross-customer tests in G04; adversarial cases in G14 |
| I2 | One confirmed draft produces at most one Guidewire claim | Submission ledger keyed by `operation_id` with unique constraint; Guidewire request carries the same ID (replay contract from G01); reconciliation by external reference | Customer sees "being registered" until reconciled | Lost-response and double-click tests in G09/G10 |
| I3 | Nothing is written to Guidewire without the customer confirming the exact summary | Confirm endpoint checks the draft version hash shown to the customer; the agent has no Guidewire write tool | Changed draft → 409, re-review | Tests in G09; forbidden-call assertion in G14 |
| I4 | The agent never states coverage, liability or payout | Instruction plus a deterministic release check on every agent reply | Reply replaced with a neutral handler-will-assess message | Eval metric in G24 (target 0 occurrences); unit tests in G06 |
| I5 | Emergency situations get the emergency number at once | Deterministic keyword and model flag; fixed text from configuration | Shown even if the model fails | Tests in G06 |
| I6 | Customer data and photos never leave the EU | Regional endpoints and EU-only resource locations (org policy) | Deployment blocked | Readback in G03; residency trace in G13 |
| I7 | A confirmed draft reaches a claim number within 5 min (≥ 99%, A14) | Executor plus reconciler; SLI in G16 | Ops queue after 1 h | G18 staging, G20 load test |

## Architecture and decisions

```text
 Browser (existing portal, OIDC session)
   │ JSON API (per-turn), signed upload URLs
   ▼
 Cloud Run: claim-intake-api  (europe-west, one region)  ── service account sa-intake
   ├─ Auth middleware: verify OIDC → customer_id, policy entitlements (trusted state)
   ├─ ADK App/Runner
   │    ├─ intake_agent (LlmAgent, gemini pinned)   tools: get_policy_summary [read],
   │    │                                            update_claim_draft [draft-only write]
   │    └─ release check (after_model_callback): coverage-promise + emergency rules
   ├─ Photo service: validate → re-encode, strip EXIF → photo_reader (model call, no tools,
   │                  output_schema PhotoObservation)
   ├─ Confirm endpoint (code): draft hash check → submission ledger → executor
   └─ Allowance + kill switch
 Cloud SQL (Postgres, EU): ADK sessions │ claim_drafts │ submission_ledger │ allowances
 GCS (EU): photos-quarantine → photos-clean (retention rules)
 Vertex AI (EU regional endpoint): agent + photo model
 Cloud Run job (scheduled): reconciler ──► Guidewire ClaimCenter Cloud API (create, documents, submit, lookup)
 Ops queue (table + dashboard) for unresolved submissions
```

Sequence for Maria: OIDC → session → agent turns update `claim_drafts` →
photos uploaded by signed URL, sanitised, described by `photo_reader` into the
draft → summary card rendered from `claim_drafts` (version *v*) → Submit
(`draft_id`, *v*) → ledger row `PENDING` → Guidewire create (with
`operation_id`) → attach documents → submit → ledger `SUBMITTED` with claim
number → card shows the number. Any break leaves the ledger row for the
reconciler.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Understand free text, ask for gaps (A4) | One `LlmAgent` for intake; photo description is a separate tool-less model call from code; submission is ordinary code. No sub-agent routing | Each part has a different authority; a router adds a probabilistic hop for no new responsibility | Less "agentic" flexibility; adding a claim-status agent later needs routing | Captured request shows two tools only | proposed |
| D2 | I3: customer approves the write | The agent proposes; the customer confirms a summary rendered from the stored draft; the confirm endpoint writes. The model has no Guidewire tool | Injection or a model error can at worst change a draft the customer sees | One extra click; ADK tool-confirmation not used (not needed) | G09, G14 | proposed |
| D3 | I2: one claim per confirmation | `submission_ledger` with `operation_id` (UUID per confirmed draft version), states `PENDING → CREATED → DOCS_ATTACHED → SUBMITTED / FAILED / UNCERTAIN`; Guidewire external-reference field carries `operation_id`; reconciler resolves `UNCERTAIN` by lookup, never by blind retry | A lost response cannot be distinguished from failure without a lookup | Needs a Guidewire extension field and its lookup (W1, G01) | G09 fake-provider tests; G10 against non-prod | provisional on A2, G01 |
| D4 | I1 | Identity from OIDC in middleware; `customer_id` and entitled policy IDs placed in session state by code; tools read them from `ToolContext` state; tool arguments never carry identity | A conversation ID or a model argument is not authority | Policy lookup adds one Guidewire read per session | G04 | provisional on A3 |
| D5 | Drafts survive disconnects | `claim_drafts` is an application record (versioned) referenced by the session; resumable for 7 days | ADK session events are not the business record | Revision handling | G06 restart test | proposed |
| D6 | Hosting with control of routes and region (A7) | Cloud Run in one EU region (europe-west4 or europe-west3, O1), Cloud SQL Postgres, GCS EU buckets | Custom routes (uploads, confirm, reconciler), region control and simple traffic splitting | Agent Runtime would manage sessions but we need app routes and a ledger anyway; GKE is more to run | G03 readback | provisional on A7, O1 |
| D7 | Pinned model with a lifecycle beyond GA | `gemini-3.8-flash` on Vertex AI regional EU endpoint for agent and photo reader; judge pinned separately (`gemini-3.8-flash`, its own manifest entry). Avoid `gemini-3.7-flash` (Vertex retirement 2027-01-28) and `gemini-3.6-flash` (2026-11-19) | Stable, released 2026-09-02, no shutdown announced in the lifecycle table `checked_on` 2026-10-08 (adk-model-and-output-contracts `assets/model-lifecycle-2026-10-01.json`) | Newest model has the least field history; EU regional availability not yet verified (O1) | G02 confirms availability and pin; G17 manifest | provisional |
| D8 | Customer sees a trustworthy reply and summary | Completed JSON per turn (no token streaming); summary card from the server record, not model text; AI notice; two languages | Lets the release check (I4) run before anything is shown | 2–4 s without progressive text; typing indicator instead | G12 browser tests | proposed |
| D9 | Photos are untrusted content | Signed upload to a quarantine bucket; server validates type and size, decodes and re-encodes, strips EXIF for the model copy; original kept for Guidewire; `photo_reader` has no tools and a `PhotoObservation` schema | Photo text cannot reach a tool; re-encoding removes most file-borne payloads | No AV scanner (A12); EXIF timestamps kept only on the original | G05, G08, G14 | provisional on A12 |
| D10 | I4 | Deterministic release check (per-language phrase rules) in `after_model_callback`; eval metric | A guarantee needs code, not a sentence | Rules can miss paraphrases; eval measures misses | G06, G24 | proposed |
| D11 | Spend and abuse | `RunConfig.max_llm_calls=10` per invocation; per customer 3 new claims/day, 40 turns/session, 20 photos/claim; operator kill switch that routes to the web form | Admission in code; billing alerts only observe | A real customer with many claims hits a limit → form | G11 | provisional on A6 |
| D12 | GDPR retention and erasure | Retention per A15 enforced by GCS lifecycle rules and a nightly purge; erasure job by `customer_id` across sessions, drafts and photos; ledger keeps IDs and hashes only | Data minimisation | Purge must not delete unresolved submissions | G13 | provisional on A15 |
| D13 | Release safety | Release manifest (image, prompt version, model and judge IDs, tool-schema hash, eval-set hash, secret versions); CI gate; Cloud Run canary 5% → 25% → 100% with thresholds; joint rollback | One unit rolls forward and back | Slower releases | G17 | proposed |
| D14 | ADK version | Working assumption google-adk 2.8.0 (all specialists' `references/compatibility.md` read against it), Python 3.11 | Matches the guidance used | Newer releases (2.11.0 on main) unexamined | "Confirm against the chosen pin" is an acceptance item of G02 | provisional |

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | `intake_agent`: collect FNOL facts (what, when, where in the home, cause if known, ongoing danger, contact preference), ask one question at a time, never discuss coverage or amounts, hand off to the form on request. Date, customer name and policy list come from code-injected state | `adk-agent-instructions`; rendered-request test in G06 |
| Tool interfaces | Two function tools: `get_policy_summary()` (read; no arguments; returns the entitled policies' address and cover type only) and `update_claim_draft(fields)` (writes only the draft; validated per field; returns missing required fields). Result ≤ 2 KB each | `adk-tool-interface-design`; declaration dump in G06 |
| Output contract | `photo_reader`: `PhotoObservation{room, damage_types[], visible_extent, quality_issue, refusal}`; repair budget 1, then "could not describe photo". `intake_agent` replies are text; the draft is structured through the tool | `adk-model-and-output-contracts`; scripted invalid-output test in G08 |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | CIAM | Middleware / tools via state | Token per request | Not stored beyond session |
| Policy entitlement | Guidewire | Middleware / `get_policy_summary` | Read at session start, rechecked at confirm | Session |
| ADK session events | Application, per customer | Runner | — | 90 days (A15) |
| `claim_drafts` | Application, per customer | `update_claim_draft`, photo service / summary card, confirm endpoint | Versioned | 90 days or erased |
| Photos (original, clean) | Application, per customer | Upload, sanitiser / photo reader, executor | — | 30 days after attachment (A15) |
| `submission_ledger` | Application | Confirm endpoint, executor, reconciler / ops | Authoritative for our attempts; Guidewire authoritative for claims | 2 years, IDs and hashes only |
| Claim in Guidewire | Insurer | Executor / handlers | Authoritative | Insurer policy |
| Telemetry | Application | All / on-call | — | 30 days; no prompt or photo content |

Identities: `operation_id` (one per confirmed draft version, survives retries
and restarts) ≠ ADK `invocation_id` ≠ session ID. Workload identities: deployer,
`sa-intake` (Cloud Run), `sa-reconciler` (job); the Guidewire client secret is
readable only by those two.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| `intake_agent` | Yes (policy summary, draft) | Customer text; photo observations derived from untrusted images | Draft-only write; no Guidewire, email or URL tools | Write leg removed: the effect happens only through the confirm endpoint after the customer reviews (D2) |
| `photo_reader` | Minimal (the photo itself) | Yes (image may contain text) | None | No tools; schema-validated output stored as data |

Tool tiers: read (`get_policy_summary`), draft write (`update_claim_draft`),
irreversible (Guidewire create/submit) only in code behind the confirm
endpoint. No code executor. Adversarial cases (G14): text in a photo asking to
change the address or submit; customer asking for another customer's policy;
asking the agent for a payout figure; a tampered `draft_version` at confirm.

## Budgets and capacity

Per completed claim (assumed): ~8 agent turns × ≤ 2 model calls, plus one
photo-reader call per photo (≤ 20), plus 0–1 repair. Bound per invocation:
`max_llm_calls=10`. At A5's storm peak of 200 concurrent conversations and
~6 s per turn, about 35 model calls per second at the peak; the Vertex quota
request and Guidewire rate limit are checked in G20. Cost per claim is a
symbolic estimate until G02 measures tokens: (turns × tokens/turn + photos ×
tokens/photo) × the price on the date checked; no price is quoted here
because none was looked up (no network). Exhaustion: per-customer allowance →
web form; kill switch → web form; Guidewire unavailable → drafts confirmed and
queued, customer told "registered shortly".

## Failure and recovery

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Guidewire ClaimCenter (writes) | Ledger stays `PENDING`, executor retries with backoff ≤ 15 min, then ops queue (G10) | Validation error → `FAILED`, customer shown what to fix or the form (G09) | `UNCERTAIN` → reconciler lookup by `operation_id` (G10) | `CREATED` without documents or submit → reconciler continues from the recorded step (G10) | Secret refresh; alert; executor pauses, ledger retained (G10, G16) | Backoff, shared concurrency cap on executor (G20) | Unique `operation_id`; second click returns the existing row (G09) | Unexpected payload → `UNCERTAIN`, never parsed as success (G10) |
| Guidewire (policy reads) | Session start fails closed → form fallback (G04) | No entitlement → polite refusal (G04) | n/a: read only | n/a: read only | As above | Cache entitlement for the session (G04) | n/a: read only | Schema-validated (G04) |
| Vertex AI model | Timeout per call; one retry; then "try again or use the form" (G06) | Safety block → neutral reply (G06) | n/a: no external effect | n/a | Workload identity; alert (G16) | Quota → kill-switch path (G11, G20) | n/a | Release check, schema repair once (G06, G08) |
| CIAM / OIDC | Fail closed (G04) | 401 (G04) | n/a | n/a | Token expiry → re-login; draft kept (G04, G12) | n/a | n/a | Invalid token rejected (G04) |
| Cloud SQL | 503, no model call; executor pauses (G03, G09) | n/a | Ledger write before Guidewire call; if ledger commit fails, no call made (G09) | Transactions per state change (G09) | IAM auth (G03) | Connection pool cap (G20) | Row lock on `operation_id` (G09) | n/a |
| GCS photos | Upload retry in browser (G12) | Type or size rejected with message (G05) | n/a: re-upload is idempotent per photo ID | Sanitise failure → photo marked unusable (G05) | Signed URL expiry → new URL (G05) | n/a at this volume | Same photo ID overwrites (G05) | Re-encode; reject undecodable (G05) |

Cross-cutting scenarios:

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Guidewire creates the claim, reply lost | "Your claim is being registered" | Ledger `UNCERTAIN`; claim may exist | Reconciler looks up `operation_id`; ops queue after 1 h (G10) |
| Customer clicks Submit twice / two tabs | Same claim number | One ledger row | Confirm endpoint returns existing row (G09) |
| Draft changed after the summary was shown | "Your details changed, please review" | No write | Customer re-confirms (G09) |
| Policy lapsed between session start and Submit | Explanation and phone number | No write | Recheck at confirm (G09) |
| Browser disconnect mid-conversation | Draft resumes on return | Draft and session | Customer (D5) |
| Model returns invalid photo observation | "We couldn't describe this photo" | Photo kept, attached anyway | None needed (G08) |
| Text in a photo instructs the agent | No effect beyond the draft the customer reviews | Draft only | G14 asserts no forbidden call |
| Kill switch or budget exhausted | Web form link | Draft kept | Operator (G11) |
| Erasure request with a pending submission | Erasure waits for the submission to resolve | Ledger row | G13 purge rules |
| Model retirement announced | None | — | Planned re-baseline release (G17 calendar) |
| Rollback | Previous revision serves; drafts and ledger compatible | Schema migrations backward-compatible for one release | G17, G23 rehearsal |

## Verification and implementation handoff

Planned only; nothing has been executed. Offline tests with fake Guidewire and
a scripted model (G02–G14); local integration with Postgres and a real process
restart (G06, G09); bounded live checks against Guidewire non-prod and Vertex
in an EU region (G01, G10, G18); release evidence from load, canary and
rollback rehearsal (G17, G20, G23). The business-outcome hypothesis is
measured separately in the pilot (G22) against the form baseline (O6).

Observability and release: SLIs are I7's success ratio, tool-error rate by
tool, tokens per submitted claim, p95 turn latency and the count of
`UNCERTAIN` rows older than 1 h; one OpenTelemetry owner per process; content
capture off; trace, session and `operation_id` on every span (G16). Release
manifest, gate and canary per D13 (G17); previous revision kept ready 7 days.

Implementation routes, estimates and ordering: see the
[plan](../plans/home-claim-intake.md).

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- | --- |
| O1 | Is `gemini-3.8-flash` served from an EU regional Vertex endpoint, and which region? | A7 forbids the global endpoint; region choice sets Cloud Run/SQL region | Platform lead; Vertex model-locations page, dated | G02 acceptance, G03 region |
| O2 | Does Guidewire Cloud API offer a replay-safe header or must we rely on an external-reference field and lookup? | Decides D3's mechanism | Eng B with the Guidewire team; sandbox evidence | G10 |
| O3 | May an invite-only pilot run while the external pen test is in progress? | Moves GA by about 12 working days if not (see plan) | Security reviewer and CISO | Plan cut line, G22 |
| O4 | All assumed answers A1–A18 | Each row lists what depends on it | Product owner | Marked provisional decisions |
| O5 | Does the AI-summary note in Guidewire need handler-side UI changes? | May add Guidewire configuration work | Claims operations | G10 scope |
| O6 | Baseline completion and call-back rates for the web form | Without it the pilot cannot show improvement | Claims operations analytics | G22 conclusion |
