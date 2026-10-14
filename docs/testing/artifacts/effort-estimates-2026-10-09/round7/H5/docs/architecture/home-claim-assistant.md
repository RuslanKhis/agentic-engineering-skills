# System design: home-insurance claim assistant (FNOL with photos → Guidewire)

Status: **draft**. Written in one pass on 2026-10-14 without the user's answers;
every decision that rests on an assumed answer is marked *provisional*.
Nothing here has been implemented or executed.

Decisions and their rationale live here (IDs `D1`…). Estimates, owners,
dependencies, capacity and the finish range live in the
[implementation plan](../plans/home-claim-assistant.md); goal scope and
acceptance live in the [tickets](../tickets/home-claim-assistant/).

## Assumed answers

The user was not available. Each row is a question I would have asked, the
answer assumed, and what depends on it. Decisions citing these rows are
provisional until the row is confirmed.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | What exactly is "GA in five months"? | All home-insurance retail customers of **one EU market (Germany)** can use it from **Mon 2027-03-15**; work must finish by Fri 2027-03-12 (98 working days from Mon 2026-10-19, with 2026-12-24 to 2027-01-01 off). | Plan calendar, D15 |
| A2 | Which languages? | German and English at GA; more markets later. | D15, G12, G13 |
| A3 | Which Guidewire product and API? | ClaimCenter on Guidewire Cloud Platform, reached through its Cloud API (REST) by a service client; a dev/sandbox tenant exists or can be requested from the Guidewire integration team. Version unknown. | D5, G01, G09, G10, W1 |
| A4 | How do customers sign in today? | An existing customer portal with a CIAM provider issuing OIDC tokens; the policyholder's customer number is a verified claim or one lookup away. | D3, G04, W5 |
| A5 | Team familiarity and hours? | Five engineers and one ML engineer, full time, about 6 focused hours a day; experienced with Python and GCP, **new to ADK** (×1.5 applied to every estimate); security reviewer about **2 hours a day**. | Plan capacity |
| A6 | Model and cloud budget? | A production budget exists but no figure was given; a monthly model-spend ceiling must be set before the beta (open decision O3). | D10 |
| A7 | Claim volume and peaks? | Illustrative: 40,000 home claims a year, 25 % filed through the assistant in year 1 (about 30 a day), storm peaks of about 300 new conversations an hour. | Budgets and capacity, G22 |
| A8 | May the assistant indicate coverage or payout? | **No.** It collects facts and files a first notice of loss (FNOL); coverage is the adjuster's decision. | D11, I5 |
| A9 | Can the claim be created without staff review once the customer confirms? | Yes. The customer's explicit confirmation of the displayed summary is the human approval; an FNOL is the customer's own statement and adjusters handle it as today. | D5, I3 |
| A10 | What happens to photo metadata (EXIF, GPS)? | Originals go to Guidewire unchanged (claims and fraud teams use timestamps); the model sees only a re-encoded copy without metadata. DPO to confirm in the DPIA. | D6, D9 |
| A11 | Retention? | Unsubmitted drafts and their photos: 30 days. Conversation sessions: 90 days after submission. Our photo copies: deleted 30 days after confirmed transfer. Guidewire keeps the claim under its own schedule. | D9, G15 |
| A12 | Existing malware scanning for uploads? | None known; a scanning decision is open (O5). | D6 |
| A13 | Call-centre handoff at GA? | A phone number and a draft reference shown to the customer; call-centre agents cannot open drafts until phase 2. | D12 |
| A14 | Accessibility? | WCAG 2.1 AA in the portal. | G12 |
| A15 | GCP organisation? | An existing organisation and platform team; Cloud Run, Cloud SQL, Cloud Tasks and Vertex AI are permitted; EU resource-location org policy can be applied. | D2, W4 |

## Purpose and constraints

**Journey (running example).** Maria, a policyholder in Cologne, finds water
from a burst pipe under her kitchen floor on a Saturday. Today she phones the
claims line, waits, describes the damage, then e-mails photos to an address
that is matched to her claim by hand; missing details mean a callback. With
the assistant she opens the portal she already uses, chats in German, uploads
six photos, answers a few targeted questions (when, where, cause, what she
has done to stop it), reviews a summary, presses **Submit claim** and gets a
ClaimCenter claim number with her photos attached.

**Outcome to improve.** Fewer incomplete FNOLs and callbacks, faster time from
loss discovery to a claim number, without more adjuster corrections. Baseline
unknown: the claims team's current callback rate and time-to-FNOL are a
measurement task in G13 (hypothesis until measured).

**Non-goals at GA.** Coverage or payout statements; claim status queries;
contents inventory; motor or other lines; call-centre access to drafts;
markets other than Germany; voice or video.

**Model versus code.** The model interprets the customer's language, asks
for missing facts, describes visible damage in photos as *suggestions*, and
writes a neutral summary. Code owns identity, which policies the customer
holds, the required-field checklist, validation, the confirmation, the
Guidewire write, retries, budgets and what is released to the browser.

**Facts versus proposals.** There is no existing code in this repository
(observed: an empty project with only the skills under `.claude/`). Every
module named below is a proposal.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | GA 2027-03-15 (A1); continued and extended afterwards |
| People and hours | 5 engineers + 1 ML engineer full time, security reviewer part time (A5); the same team runs it after GA with the existing claims-IT on-call |
| Money | Production budget, figure unknown (A6, O3) |
| Users and what they read | External retail customers using a live service; claims handlers read the resulting Guidewire claims |
| Data touched and effects | Personal data (name, address, policy, photos of homes, possibly people and health details if injuries are mentioned); creates claims in the system of record |
| Delivery profile | **Production service**: external customers, personal data and writes to the system of record, under GDPR, the EU AI Act transparency duty and insurer ICT-risk rules (DORA). |

Depth per concern (production column of the delivery profiles, adjusted):

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build, gated evaluation (G13, G14, G20) | Second market or model migration → re-baseline |
| Identity and per-customer scope | Build (D3, G04) | Delegated access for brokers or family members |
| Secrets | Build, Secret Manager with rotation for the Guidewire client (G03) | — |
| External writes | Build: idempotent, reconciled (D5, G09–G11) | — |
| Sensitive data | Build: data map, telemetry gates, retention, erasure, screening layer (D9, G15) | A new data sink or market |
| Prompt injection and agency | Build: split readers, adversarial suite, pen test (D1, G17, G23) | New tool with write or egress |
| Budgets and loop limits | Build: per-invocation, per-customer, operator stop (D10, G18) | Measured abuse or spend near ceiling |
| Memory and retrieval | **Not needed**: no cross-session memory, no RAG at GA; the draft is an application record | A help-article Q&A feature |
| Frontend | Build inside the existing portal (D8, G12) | — |
| Hosting | Cloud Run with recovery and rollback (D2, G21) | — |
| Observability | Build: SLOs and alerts (D13, G19) | — |
| Release engineering | Build: manifest, CI eval gate, canary, joint rollback (D14, G20) | — |
| Performance and cost tuning | Defer until measured in the pilot | p95 turn latency or cost per claim above target |

**Floor kept:** no secrets in code, prompts or logs; `RunConfig.max_llm_calls`
plus a per-customer allowance and an operator stop; no claim is created without
the customer pressing Submit on the exact summary shown; real personal data
only after DPIA sign-off (W2) and never in logs; pinned model ID. No accepted
risks are recorded; any would need an owner and an end condition.

**Who may use it before GA:** developers on synthetic data (G02–G22);
employees filing test claims against Guidewire sandbox and then real-employee
pilot claims (G25); a controlled share of real customers in the beta (G27)
only after W2, G23 and G24.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Call-centre access to drafts | Needs a second integration (CRM or Guidewire draft) and its own authorisation | Callback rate from abandoned drafts above an agreed level |
| Multi-region failover | Single EU region with backups meets the provisional 99.5 % target | Availability target above 99.5 % or a regional incident |
| Context caching and latency tuning | No measurements yet | Pilot p95 turn latency above 6 s or cost per claim above ceiling |
| Memory across sessions | Journey completes in one sitting or resumes the same draft | Customers asking to reuse earlier claim details |

Capacity, finish range and cut line: see the plan's summary.

## Guarantees and acceptance

| ID | Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer can file only against a policy they hold that covers the loss address and was in force on the loss date | Submission worker re-reads policy from Guidewire for the verified customer immediately before creating the claim (D5); the draft's policy choice is only a proposal | Submission refused with "we couldn't match this policy — call us"; no claim | Offline: forged policy number, other customer's policy, cancelled policy → no Guidewire call (G11); sandbox check (G10) |
| I2 | One confirmed draft produces at most one ClaimCenter claim | Operation ledger unique on `draft_id`, named Cloud Task, and Guidewire reconciliation by our external reference before any re-dispatch (D5) | Duplicate confirm returns the existing operation's status | Offline: double click, worker crash after send, lost reply → one claim (G09, G11); sandbox replay (G10) |
| I3 | No claim without explicit confirmation of the exact summary shown | `POST /drafts/{id}/submit` requires the draft version hash rendered on the summary; there is no model tool that submits (D1, D5) | Stale hash → 409, summary re-rendered | Offline: scripted model tries to "submit"; edit after render → 409 (G11, G17) |
| I4 | Sessions, drafts and photos are visible only to their owner | Gateway verifies the OIDC token, binds `customer_id` to session and draft rows, checks owner on every route (D3) | 404 for another owner's IDs | Offline cross-customer tests on every route (G04, G07) |
| I5 | The assistant never states coverage, liability or a payout amount | Instruction plus output check on the final turn text; measured in evaluation (D11) | Turn replaced with neutral wording and logged as an event (no content) | Eval metric target 0 violations on the dev set; adversarial prompts (G13, G17) |
| I6 | Personal data is processed and stored in the EU | Org policy on resource locations, regional Vertex endpoint, EU log buckets (D2, D9) | Deploy fails policy | Inventory check of every sink in G15; Vertex region verification (O1) |
| I7 | No conversation text or photo content in logs or traces | Telemetry content capture off; structured logs carry IDs only (D9, D13) | — | In-memory exporter test shows no content attributes (G19); log scan in G15 |
| I8 | Model work and spend are bounded per turn, per customer and globally | `max_llm_calls`, per-customer daily allowance in Cloud SQL, operator stop flag (D10) | Polite refusal with phone number; draft kept | Offline: loop-forcing model stops at the cap; allowance exhausted → refusal (G18) |
| I9 | Emergency cues (ongoing flooding, gas, fire, injury) show emergency instructions at once | Deterministic keyword rules plus a model flag in the turn output; the banner is rendered by code (D11) | Banner shown even if the model turn fails | Eval recall target ≥ 0.95 on emergency cases (provisional) (G13) |
| I10 | Erasure request removes drafts, sessions and our photo copies within 30 days | Erasure job keyed on `customer_id` with tombstones that block late writers (D9) | Pending submission completes first, then erasure | Offline race test: erase during queued submission (G15) |
| T1 | Submission path availability 99.5 % monthly (provisional) | Cloud Run + Cloud SQL HA + Cloud Tasks retries | Customer told to retry later or call | SLO in G19, measured from pilot |
| T2 | p95 time from Submit to claim number ≤ 60 s (provisional) | Worker latency budget | Status page shows "processing" and later the number | Pilot measurement (G25) |
| T3 | p95 chat turn ≤ 6 s text-only, ≤ 15 s with photo analysis (provisional) | Model choice, bounded context | Typing indicator; no partial text | Pilot measurement (G25) |

## Architecture and decisions

```text
 Browser (customer portal, existing CIAM login)
   │  HTTPS JSON: /sessions, /turns, /photos (signed URL), /drafts/{id}/submit, /status
   ▼
 claim-assistant-api  (Cloud Run, europe-west3, SA: api-sa)          trust boundary: verified OIDC → customer_id
   ├─ Runner + intake LlmAgent (tools: list_my_policies, update_claim_draft, get_draft_checklist)
   ├─ photo reader: single-turn model call, no tools, output_schema  ◄── photos (re-encoded copy)
   ├─ Cloud SQL Postgres: ADK sessions, claim_drafts, operations, allowances, tombstones
   ├─ GCS quarantine bucket (originals) + derived bucket (model copies)
   └─ enqueue Cloud Tasks (task name = operation_id)
                │
                ▼
 claim-submit-worker  (Cloud Run, SA: worker-sa, only identity holding the Guidewire client secret)
   ├─ re-check policy (I1) → create FNOL with external reference → attach photo documents
   └─ record receipts in operations; reconcile on uncertainty
                │  egress to Guidewire Cloud API (allow-listed host)
                ▼
 Guidewire ClaimCenter (system of record for claims and policies)
 Vertex AI Gemini (EU endpoint) · Model Armor (screening layer, if available in region) · Cloud Trace/Monitoring/Logging (EU)
```

Sequence for Maria: portal token → `POST /sessions` (owner bound) → turns
update the draft through `update_claim_draft` → photos uploaded by signed URL,
validated, re-encoded, described by the reader, suggestions shown to Maria →
checklist complete → code renders the summary with version hash → Maria
presses Submit → API writes operation `pending` and enqueues the task → worker
re-reads her policy, creates the claim, attaches photos, records the claim
number → browser polls `/status` and shows the number.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Language understanding over customer text and photos, with a write to the system of record | One intake `LlmAgent` with three narrow tools that touch only the customer's own draft; a separate single-turn photo reader with no tools; **submission is ordinary code** triggered by a button, never a model tool | Breaks the private-data + untrusted-content + write combination structurally: the agents that read untrusted input cannot create claims | One extra model call per photo and a typed handoff, versus one agent with a `create_claim` tool and a "don't submit unless confirmed" sentence | Scripted model calls a non-existent submit tool / injection text in a photo → no operation row, no Guidewire call (G17) | Proposed |
| D2 | EU residency, control over identity middleware, egress to Guidewire, background submission | Two Cloud Run services from one image (API and worker) in `europe-west3`; Vertex AI EU endpoint for the model | Owning the Runner lets the gateway verify identity before any model call and set `max_llm_calls`; Cloud Run gives revisions for canary and rollback | Managed Agent Runtime would remove server code but puts the identity check and submission worker elsewhere; GKE adds operations the team need not carry | Deploy readback shows region, revision and SA per service (G03, G21) | Provisional (A15, O1) |
| D3 | Customer sees only their own data | Gateway verifies the portal's OIDC token (issuer, audience, expiry), derives `customer_id`, writes it to session state under an app-only key; tools read scope from `tool_context.state`, never from model arguments | Model-supplied IDs cannot select authority; one check point for every route | Couples the API to the CIAM token format; needs a new CIAM client (W5) | Cross-customer tests on all routes (G04) | Provisional (A4) |
| D4 | Drafts, operations and sessions must survive restarts and replicas, with unique constraints | One Cloud SQL for PostgreSQL instance (regional HA, PITR) holding ADK `DatabaseSessionService` tables and application tables | Unique keys and transactions for the ledger; one backup and erasure story | Firestore needs no instance but makes unique claims and joins harder; Cloud SQL has a fixed monthly cost | Restart test: draft and pending operation survive (G05, G11) | Proposed |
| D5 | Exactly one claim per confirmed draft, despite retries, crashes and lost replies | Confirm binds `draft_id` + `version_hash`; operation row inserted with unique `draft_id`; Cloud Task named after `operation_id`; worker writes our `operation_id` into a ClaimCenter external-reference field and **searches by it before any re-send**; uncertain outcomes stay `uncertain` until reconciled; photos are separate child operations | The provider's replay contract is unknown (O2), so deduplication must not depend on it; a search-before-send rule works whether or not Guidewire supports idempotency keys | Extra search call per retry; needs a searchable custom field that the Guidewire team must configure (W1) | Fake-Guidewire tests: commit-then-timeout, 5xx, worker restart → one claim (G09); sandbox confirmation (G10) | Provisional (A3, O2) |
| D6 | Photos are evidence and model input, and are untrusted files | Signed-URL upload to a quarantine bucket; server validates type by content, size (≤ 15 MB) and count (≤ 20); creates a re-encoded, metadata-free, downscaled copy for the model; originals transfer to Guidewire as documents | Re-encoding removes EXIF/GPS and malformed payloads before the model; originals keep evidential value | Two copies to govern; scanning decision open (O5) | Polyglot/oversized/wrong-type files rejected; model request contains no EXIF (G07) | Provisional (A10, A12) |
| D7 | Reliable structured reading of photos and turns; stable behaviour to GA and after | `gemini-3.8-flash` on Vertex AI, pinned; photo reader uses `output_schema` with an explicit `unusable` / `no_damage_visible` result; one repair attempt then a typed failure ("we couldn't read this photo") | Newest stable entry in the skill's lifecycle table (checked 2026-10-08), no announced retirement; `gemini-3.7-flash` retires on Vertex on 2027-01-28, inside this plan | Newest model has least field history; EU availability unverified (O1) | Scripted prose / fenced JSON / wrong-but-valid outputs handled as designed (G08, G14); model comparison on dev set (G14) | Provisional (O1) |
| D8 | Customers in the existing portal; no partial unsafe text | Custom JSON API returning completed turns (no token streaming), typing indicator, message and tool-result IDs; summary and status rendered from application records, not model text | Completed turns can be checked (I5) before release; simpler than AG-UI for one widget | Slower perceived response than streaming | API contract tests; browser test of summary/confirm (G12) | Proposed |
| D9 | GDPR minimisation, residency, retention and erasure | Data map below; telemetry content capture off; logs carry IDs; Model Armor (or SDP) screening on customer text as a layer, failing closed to "we can't process this message"; retention per A11; erasure job with tombstones | Structural controls first, screening second | Screening adds latency and a regional dependency | Sink inventory, log scan, erasure race test (G15) | Provisional (A10, A11, O4) |
| D10 | Spend and abuse bounded under storm peaks | `max_llm_calls=8` per invocation; ≤ 40 turns per session; ≤ 3 new drafts and ≤ 60 photos per customer per day; global operator stop and degrade mode ("save draft and we'll call you"); concurrency limit on Cloud Run | Each limit is enforced in code with a defined outcome | Limits may frustrate a genuine heavy-loss customer; phone path stays open | Offline cap tests (G18); load test (G22) | Provisional (A6, A7) |
| D11 | No coverage statements; emergencies handled | Instruction forbids it; final-turn check for coverage/payout language replaces the turn; emergency banner from code rules plus model flag | A probabilistic model needs a measured guard; the banner must not depend on the model | Final-turn check can over-trigger; measured in eval | I5, I9 eval metrics (G13) | Proposed (A8) |
| D12 | Customer must always reach a person | Every screen shows the claims phone line; drafts carry a short reference | Cheap and robust | Call-centre cannot open the draft at GA (deferred) | UI test (G12) | Provisional (A13) |
| D13 | Incidents must be attributable without content | OpenTelemetry from ADK to Cloud Trace; one telemetry owner per process; session, invocation and operation IDs on every span and log; SLIs below | Alert → session → reproduction | Trace storage cost | Exporter test (G19) | Proposed |
| D14 | Behaviour comparable across releases | Release manifest (image digest, prompt version, model and judge IDs, tool-schema hash, eval-set hash, secret versions); CI eval gate; Cloud Run traffic-split canary; joint rollback | Prompt, model and image move together | Slower releases | Gate fails by exit code on a seeded regression (G20) | Proposed |
| D15 | AI Act transparency; German and English | Disclosure line at chat start ("You are chatting with an AI assistant…"); language follows the portal locale; instruction and eval cases in both languages | Legal duty for chatbots interacting with people (legal review to confirm, O6) | Doubles eval labelling | Eval runs per language (G13) | Provisional (A2, O6) |

**Versions.** No ADK version is installed here. Working assumption:
`google-adk` **2.8.0**, the version the specialist skills were read against
(e.g. `.claude/skills/adk-agent-security/references/compatibility.md:3`, read
2026-10-07, main branch at 2.11.0). G02 confirms the chosen pin and reruns the
named interface checks (`DatabaseSessionService`, `RunConfig.max_llm_calls`,
`output_schema` with tools, `tool_context.state`). Model IDs come from
`.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
(`checked_on` 2026-10-08). Service regions, quotas and prices were **not**
checked (no network in this session); each is a named verification in O1, O3
and G03.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | Intake agent owns: understanding the loss, asking for what the checklist says is missing (one question at a time), neutral summary wording, emergency flag. Code owns: identity, policy list, required fields, dates/time zone, limits, confirmation. Versioned prompt files in DE/EN source with one instruction. | `adk-agent-instructions`; rendered-request snapshot test (G06) |
| Tools | `list_my_policies()` (read, scope from state, returns ≤ 5 policies with masked numbers and addresses); `update_claim_draft(field, value)` (write to own draft only, validated enums/dates/lengths, returns checklist status); `get_draft_checklist()` (read). Three tools; results ≤ 2 KB; errors are actionable dicts. No submit, e-mail or search tool. | `adk-tool-interface-design`; declaration dump and size test (G06) |
| Output contracts | Photo reader schema: `{status: ok | unusable | no_damage_visible, rooms[], damage_types[] (enum), visible_hazards[] (enum), description ≤ 400 chars}`; IDs copied by code. Intake turn: free text + `emergency_flag` from a structured side channel. Model `gemini-3.8-flash`, temperature low, thinking low; no failover at GA (a single region outage shows the phone line). Judge `gemini-3.8-flash` pinned separately; most metrics are deterministic. | `adk-model-and-output-contracts`; scripted invalid-output tests (G08, G14) |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | CIAM | Gateway reads token | Verified per request | Not stored beyond `customer_id` |
| Policy list | Guidewire (authoritative) | Tool and worker read for verified customer | Read live; worker re-reads at submit (I1) | Not cached beyond the session |
| ADK session events | Customer | Runner writes; owner reads | Current | 90 days after submission, 30 days if unsubmitted (A11) |
| Claim draft (versioned) | Customer | Tools and API write; owner and worker read | Version hash per change | As session |
| Operation ledger | Application | API inserts; worker updates receipts | Authoritative for *our* attempts, not for Guidewire state | 2 years for audit (assumed, O4); IDs only |
| Photos (original, derived) | Customer | Upload by owner; worker reads originals; reader reads derived | Immutable once validated | Derived: deleted after draft closes; originals: 30 days after confirmed transfer |
| Claim in ClaimCenter | Insurer | Worker creates; adjusters | System of record | Guidewire retention; outside this erasure job |
| Telemetry | Operations | Services write IDs, timings, token counts | — | Cloud Logging/Trace EU buckets, 30 days (assumed) |

Identities: end user (`customer_id` from OIDC), `api-sa` (Vertex, Cloud SQL,
GCS write, Cloud Tasks enqueue; **no** Guidewire secret), `worker-sa` (Cloud
SQL, GCS read, Guidewire client secret from Secret Manager), deployer SA in CI.
The Guidewire service client acts for the insurer; customer authority comes
only from I1's check.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Intake agent | Customer's own policies and draft | Customer text; reader output (validated enums, ≤ 400 chars) | Writes only the customer's own draft (reversible) | No irreversible tool; submit outside the model (D1); capability check in `before_tool_callback` that the draft belongs to `state.customer_id` |
| Photo reader | None beyond the photo | Photos, including text in images | None | No tools; schema-only output |
| Submit worker | Policy, draft | Draft text written by the customer | Creates claim, uploads documents | Ordinary code; only acts on a confirmed operation; free text is length-bounded and sent as plain text — Guidewire must render it escaped (checked in G10) |

Tool tiers: read (`list_my_policies`, `get_draft_checklist`), write-own-draft
(`update_claim_draft`), irreversible (claim creation) — the last is not
reachable by any model. No code executor. Adversarial cases (G17): injected
instructions in photo text and customer text, attempts to name another
customer's policy, tool-argument smuggling of IDs, requests to "submit now",
oversized/looping turns; each asserts the forbidden effect never runs.

## Budgets and capacity

Illustrative per completed claim (A7): about 12 intake turns × about 8k input
and 300 output tokens, plus 6 photos × one reader call (about 1–2k input
tokens per image after downscaling, 200 output). Expected about 110k input
and 5k output tokens per claim; bounded by D10 at 40 turns × 8 calls. Cost
per claim = tokens × the Vertex AI EU price for the pinned model on the
pricing date — **not looked up** (O3). At 300 conversations an hour peak and
about 15 minutes in flight, roughly 75 concurrent conversations; each turn
holds a request for seconds, so concurrent requests stay in the tens. Model
quota (W6) and Guidewire API rate limits (O2) are the binding limits; G22
measures them. Cloud SQL, two Cloud Run services with minimum instances and
storage are fixed monthly costs separate from per-claim cost. A Cloud Billing
budget alerts only; enforcement is D10.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Success | Claim number, photos listed as attached | Operation `succeeded` with receipt | None |
| Another customer's session or draft ID | 404 | Nothing read or written | — (I4) |
| Model unavailable or slow | "I'm having trouble — your draft is saved" + phone | Draft intact; no turn persisted as success | Customer retries; on-call if SLO burns (G19) |
| Reader returns prose or invalid JSON | "We couldn't read this photo"; photo still attached as evidence | Photo stored; no suggestion | One repair, then typed failure (D7) |
| Double click / two tabs submit | Same status page | One operation row (unique `draft_id`) | — (I2) |
| Guidewire commits, reply lost | "Processing" | Operation `uncertain` | Worker searches by external reference, then records receipt or re-sends only if absent; after N tries → manual queue owned by claims-IT (G09) |
| Claim created, a photo upload fails | Claim number shown with "2 photos still uploading" | Child operations per photo | Worker retries photo children; never re-creates the claim |
| Worker crash mid-dispatch | "Processing" | Task redelivered with same name | Reconcile before send (D5) |
| Policy cancelled or address mismatch at submit | "We couldn't match this policy — call us" with reference | Operation `rejected`; no claim | Customer calls; no retry |
| Draft edited after summary shown | Summary refreshes; Submit must be pressed again | Old hash rejected | — (I3) |
| Injection text in photo or message | Normal conversation | No effect outside own draft | Adversarial suite (G17) |
| Screening service unavailable | "We can't process this message right now" | Turn not sent to model | Fails closed; alert (G15) |
| Storm burst or budget exhausted | Degrade: "save draft, we'll call you" or phone | Drafts kept; no new expensive work | Operator stop independent of resets (G18) |
| Erasure request while submission queued | Claim still created; then local data erased | Tombstone blocks later writes | Erasure job waits for terminal operation state (G15) |
| Model retirement announced | None | — | Planned re-baseline release (G20; phase 2 G31) |
| Bad release | Canary rolled back | Sessions schema backward compatible for one release | Joint rollback of image, prompt, model (G20) |
| Region outage | Portal shows phone line | Cloud SQL backups, PITR | Restore per runbook (G21, G26); no automatic failover at GA |

## Verification and implementation handoff

Ladder: offline deterministic tests with fake Guidewire, fake CIAM and
scripted models for every invariant (G04–G11, G17, G18); local integration
with a real Postgres restart (G05, G11); bounded live checks against the
Guidewire sandbox and Vertex AI EU with request and cost limits (G10, G14);
hosted evidence in staging and production — load, recovery drill, pen test,
pilot and beta (G21–G27). None of these has been run yet.

Product outcome (hypothesis): share of assistant FNOLs needing a callback for
missing information, and time from first message to claim number, against
the phone baseline measured in G13; guardrail: adjuster correction rate does
not rise. Model quality (field accuracy), valid transactions (I2) and user
outcome are reported separately.

Observability and release:

- SLIs: submission success ratio (good = claim number recorded / confirmed
  submissions), reconciliation backlog age, tool-error rate by tool, turn
  latency p95, tokens per completed claim, emergency-banner rate. Targets from
  pilot baselines; alert owner: claims-IT on-call (G19, G26).
- Telemetry: one OTel provider per process; content capture off; EU sinks,
  30-day retention (assumed).
- Release bundle per D14, stored with the Cloud Run revision label.
- Promotion gate: deterministic tests on every change, eval set on every
  prompt/model change with the pinned judge, cost ceiling per run; canary at
  5 % of beta traffic with thresholds set before traffic moves.
- Rollback unit: the whole bundle; previous revision kept ready for 7 days.

Implementation routes per decision, goals and the next prompt are in the
[plan](../plans/home-claim-assistant.md) and its tickets.

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- | --- |
| O1 | Is `gemini-3.8-flash` served on Vertex AI in an EU region, with what quotas and lifecycle date? | D2, D7, I6 | ML Eng: Vertex model page and region table, dated | G14 decision; G22 quotas (W6) |
| O2 | Guidewire Cloud API contract: FNOL fields for homeowners, idempotency or search on a custom external-reference field, document upload limits, rate limits, error semantics | D5, I2 | Eng B with the Guidewire integration team | G09 design detail, G10 |
| O3 | Monthly model-spend ceiling and Vertex price on the pricing date | D10 thresholds | Product owner + finance | G18 thresholds, G27 |
| O4 | Retention periods and audit retention for the ledger | D9, I10 | DPO in the DPIA (W2) | G15 final values |
| O5 | Malware scanning of uploads (product or not) | D6 | Security reviewer | G07 scope, G23 |
| O6 | Legal reading: AI Act transparency wording, and confirmation that home claims intake is not a high-risk use | D15 | Legal / compliance | G12 copy, G27 |
| O7 | GA date and cut line remedy: half-time security reviewer or GA on 2027-03-17 | Calendar fits only at the low end otherwise | Delivery lead | Plan |

No decision in this document has been accepted by the user yet. Design
completion and implementation authorisation are separate: this session was
design-only.
