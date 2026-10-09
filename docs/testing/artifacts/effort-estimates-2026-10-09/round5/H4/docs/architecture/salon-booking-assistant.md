# System design: salon booking assistant (MVP)

Status: **draft**. Every scope-gate answer below is assumed (the user was not
available); decisions that depend on them are marked provisional. Nothing here
has been implemented or tested.

Plan: [docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md).
Tickets: [docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/).

## Assumed answers

| # | Question | Assumed answer | Decisions that depend on it (provisional) |
| --- | --- | --- | --- |
| A1 | Deadline and afterwards | Given: MVP live in 2 weeks (10 working days), then continued | Phase 1 code is kept; phase 2 written below |
| A2 | Who builds it | Given: 3 developers. Assumed: Python-fluent, new to ADK, have used GCP; about 5 focused hours/day each on this project | Estimates ×1.5 for ADK; capacity; owners |
| A3 | Money | Small allowance: about USD 200/month for models and cloud during the MVP | Model tier (Flash), one small Cloud SQL instance, no paid inspection services in phase 1 |
| A4 | Users and what they read | External salon customers, chatting in a widget on the chain's existing website; salon managers read a daily list of assistant-made changes | Customer identity, public widget, abuse limits |
| A5 | Data and effects | Real customer personal data (name, phone, email, appointment history) and real, reversible writes: create, move, cancel appointments visible to customers and stylists | Confirmation before every write, idempotent operations, no content in logs |
| A6 | How customers prove who they are | The booking platform already has customer accounts; the website's signed-in session yields a token the backend can verify against the booking API | D3; guests (no account) are deferred |
| A7 | Booking API capabilities | Our own HTTP API with: services, stylists, availability search, create, reschedule, cancel, list a customer's appointments; a staging environment; business rules (opening hours, cancellation window) enforced by the API. Idempotency-key support unknown | D4, D5; G01 confirms |
| A8 | Channel and language | Web chat only, English only, each salon's local time zone from API data | Frontend; SMS/WhatsApp and other languages are "later" |
| A9 | Hosting | A GCP project exists or can be created by the team the same day; Vertex AI is permitted | D7 |

## Purpose and constraints

**Journey (running example).** Maya, a signed-in customer of the Northside
salon, opens the chat on the website and types "can I move my Thursday cut to
Saturday morning, ideally with Jo?". Today she must find the booking form,
cancel, and re-book while hoping the slot is still free, or phone during
opening hours. With the assistant she sees her Thursday appointment, two
Saturday slots with Jo, picks 10:30, sees a confirmation card ("Move: Cut with
Jo, Thu 14:00 → Sat 10:30, Northside") and presses **Confirm**; the card turns
into "Moved — reference NS-4821" read from the booking API.

**Outcome to improve (hypothesis, unmeasured):** more bookings, moves and
cancellations completed without a phone call. Baseline: phone/manual changes
per week per salon, to be gathered by the salons (open decision O4).

**What the model decides:** interpreting the request, choosing which read tool
to call, presenting options and proposing one specific change.
**What code controls:** who the customer is, which appointments are theirs,
whether a slot is valid, the confirmation, the write, retries and the
reference shown after a write. The model has no tool that writes.

Non-goals for phase 1: guest booking, payments/deposits, staff-facing chat,
SMS/WhatsApp, multiple languages, memory of preferences across conversations.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due | 10 working days from start; continued afterwards (A1) |
| People and hours | 3 developers, ~5 focused h/day each, new to ADK (A2); the same team runs it |
| Money | ~USD 200/month (A3) |
| Users and what they read | External customers in a website widget; managers read a daily change list (A4) |
| Data and effects | Real personal data; reversible writes visible to customers and stylists (A5) |
| Delivery profile | **MVP or pilot**: first external users doing real bookings; done means real customers book, move and cancel safely at the five salons and the team can see failures and cost |

| Concern | Depth now (phase 1) | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 25–30 case evaluation set run locally against a fake booking API (G07) | CI gate in phase 2 (G12) |
| Customer identity and scope | Build: verified booking-platform token, ownership checks in code, cross-customer tests (G03) | Guest booking requested (G17) |
| Secrets | Build: Secret Manager + service account, nothing in code/prompts (G08) | Rotation in later list |
| External writes | Build: propose → customer confirms → code executes once, durable operation record (G04, G05) | Payments or deposits |
| Sensitive data | Minimal: content kept out of logs and traces; sessions deleted after 30 days by a scheduled job in phase 2 | Phase 2 retention/erasure (G14); a complaint or DSAR |
| Prompt injection / agency | Build (structural): model holds no write tool; writes only via confirm endpoint bound to the verified customer | Adversarial suite in phase 2 (G15) |
| Budgets | Build minimal per-customer allowance: `max_llm_calls`, turns per customer per day, IP rate limit, billing alert (G09) | Phase 2 cost dashboards (G13) |
| Memory | Conversation sessions only (Cloud SQL) | Preference memory in "later" |
| Frontend | Build: small widget, completed JSON per turn, confirmation cards (G06) | Streaming if measured latency hurts |
| Hosting | Cloud Run, staging + production, previous revision kept for rollback (G08 foundation, G09 hosted gateway) | — |
| Observability | Build minimal: structured logs and traces with session/operation IDs and token counts, no content (G09) | SLOs and alerts (G16) |
| Release engineering | Minimal: pinned model and ADK, prompt in repo, evaluation run before each deploy by hand | CI gate (G12) |
| Performance tuning | Defer | Measured p95 turn latency > 8 s (assumed target) |

**Floor kept:** no secrets in code, prompts or logs; spend stop
(`RunConfig.max_llm_calls` plus a billing budget alert on the project); no
booking change without the customer pressing Confirm on the exact details;
personal data scoped to the signed-in customer and out of logs; model ID pinned.

**Who may use it:** signed-in customers of the five salons, on their own
appointments. **Graduation conditions** before wider use (guests, other
channels, more salons): G12 CI evaluation gate, G14 retention and erasure,
G15 adversarial suite, G16 SLOs and alerts.

Capacity and cut line: see the plan's
[delivery profile](../plans/salon-booking-assistant.md#delivery-profile-and-capacity);
phase 1 is G01–G11, phase 2 is G12–G18.

## Guarantees and acceptance

| Invariant | Enforcing component and authority | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 A customer sees and changes only their own appointments | Gateway derives `customer_id` from the verified token (D3); tools read it from trusted session state, never from model arguments; confirm endpoint rechecks ownership via the booking API | 403 / "I can't find that appointment" | G03 cross-customer tests; G05 move/cancel of another customer's appointment ID refused |
| I2 No booking change without an explicit confirm of the exact details | Proposals stored server-side; only `POST /proposals/{id}/confirm` writes, and only for the proposal's owner, unexpired, status `pending` (D4) | Proposal expires; nothing written | G04 tests: model alone cannot write; confirm of expired/altered/foreign proposal rejected |
| I3 One confirmed proposal causes at most one booking change | Operation record keyed by proposal ID, atomic `pending → executing` claim; idempotency key if the API supports it, otherwise lookup-before-retry (D5) | Duplicate click returns the same result | G04 double-confirm and timeout-then-retry tests against the fake |
| I4 The customer is never told a change happened unless the booking API confirmed it | Result card renders only from the operation record's provider reference | "We couldn't confirm this — we're checking" + manager list | G04/G06 uncertain-outcome test |
| I5 Spend is bounded | `max_llm_calls=8` per turn; 40 turns/customer/day; billing alert | Polite refusal; turn ends | G09 test hitting each limit |

## Architecture and decisions

```
Browser widget ──HTTPS──▶ Cloud Run: gateway (FastAPI)
  (signed-in site)          │  verify customer token ─▶ Booking API /me
                            │  Runner(App(booking_agent))
                            │     LlmAgent ──▶ Vertex AI Gemini (pinned)
                            │     read tools + propose_* tools ─▶ Booking API (read)
                            │  POST /proposals/{id}/confirm  (no model)
                            │     ─▶ Booking API (write, idempotent)
                            └─▶ Cloud SQL Postgres: ADK sessions,
                                 proposals, booking_operations
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Interpret free text, use a few capabilities (A4) | One `LlmAgent`, six narrow function tools, no sub-agents | Booking/move/cancel share context and tools; no separate responsibility or credential justifies a second agent | A router + three specialists adds routing errors and evaluation cost for no new boundary | Eval set G07: correct tool trajectory on ≥ 90% of cases (assumed target) | proposed |
| D2 | Model must not write directly (A5, I2) | Tools: `list_services`, `find_availability`, `list_my_appointments` (read); `propose_booking`, `propose_move`, `propose_cancel` (validate, store a proposal, return a summary). No write tool | A write needs a human's click bound to stored details; injection can at most create a proposal the customer must confirm | One extra click per change; ADK's built-in tool confirmation not used (its known limitations with custom runners need checking against the pin) | G04: scripted model calling any tool never mutates the fake API | proposed |
| D3 | I1, identity (A6) | Gateway verifies the booking-platform token on every request, puts `customer_id` in session state at creation and checks session ownership on each turn; tools read `tool_context.state` | Identity comes from code; a session ID is a locator, not permission | Customers without an account cannot use it in phase 1 | G03 tests: other customer's session ID → 403; tampered token → 401 | provisional (A6) |
| D4 | I2 | Proposal record: `id`, `customer_id`, `kind`, canonical payload (salon, service, stylist, start, appointment_id), `expires_at` (+10 min), `status`. Confirm endpoint rechecks owner, expiry, current availability/ownership, then executes | Confirmation binds to stored material details, not to what the model later says | A proposal store to own; expiry may annoy slow customers | G04 tests listed under I2 | proposed |
| D5 | I3, I4 | `booking_operations` row per proposal; claim atomically; send with idempotency key = proposal ID if the API supports it; on timeout mark `uncertain`, reconcile by listing the customer's appointments; unresolved uncertain rows go on the managers’ daily list (G10) | A lost response after commit must not cause a second booking | Reconciliation code and a manual path; depends on G01 | G04 fake that commits then times out → exactly one appointment | provisional (A7) |
| D6 | A3, latency, tool calling | Model `gemini-3.8-flash` on Vertex AI, pinned; ADK `google-adk==2.8.0` as working pin. No `output_schema` (answers are text; structure lives in tool calls) | Stable, no shutdown announced in the lifecycle snapshot checked 2026-10-08; Flash tier fits the allowance | Released 2026-09-02, so less field experience than `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later), the fallback choice | G02 confirms the pin and model ID; G07 measures | provisional |
| D7 | Hosting (A9) | One Cloud Run service (gateway + Runner) in the region nearest the salons; Cloud SQL Postgres for `DatabaseSessionService` and app tables; Secret Manager | Smallest managed footprint the team can operate; sessions survive instance changes | Cloud SQL is a fixed monthly cost; Agent Runtime would remove hosting code but complicates the custom confirm endpoint | G09: restart instance mid-conversation, session continues | provisional |
| D8 | Concurrency in one conversation | Serialize: a turn arriving while one is running for that session gets 409; widget disables input until reply | Avoids two proposals racing in one session | A second tab must wait | G06/G03 test | proposed |

Versions and provider facts are taken from the sibling skills' snapshots
(`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`,
`checked_on` 2026-10-08; `references/compatibility.md`, ADK 2.8.0). No current
provider pages were consulted in this session (network not allowed); G02 and
G08 carry the checks.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Help one signed-in customer of the chain book, move or cancel; always propose before changing; never claim a change happened unless a tool result says so; offer the salon phone number on API errors or out-of-policy requests. Customer ID, date and salon list come from state/code, not prose | `adk-agent-instructions`; rendered-request test in G02 |
| Tools | Six function tools, primitive parameters, results bounded (≤ 10 slots, ≤ 10 appointments), each result a dict with `status` and an actionable `error` | `adk-tool-interface-design`; declaration dump in G02 |
| Output | Free text; proposals are tool results the widget renders as cards from the proposal record, not from model text | `adk-model-and-output-contracts`; pin check in G02 |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, availability, services | Booking API (authoritative) | Booking API / tools, confirm endpoint | Read live each time; never cached | Booking platform's policy |
| Customer identity | Booking platform accounts | Gateway verifies | Per request | — |
| Conversation session | Assistant, per customer | ADK `DatabaseSessionService` | — | 30 days (job in G14; until then manual) |
| Proposals, operations | Assistant, per customer | propose tools / confirm endpoint | Snapshot at proposal; rechecked at confirm | 90 days for reconciliation |
| Logs and traces | Team | Gateway | — | Cloud Logging default retention; no message text, no names or phones |

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking_agent | The customer's own appointments | Customer chat text; service/stylist names from the API (staff-entered) | None from the model; writes only through the confirm endpoint | Leg removed: the model has no write path; a malicious prompt yields at most a proposal its own author must confirm |

Tool tiers: read (3), propose (3, stores a proposal only), write (confirm
endpoint, code only). No code executor. Adversarial suite deferred to G15; G07
includes three injection cases.

## Budgets and capacity

Assumed workload: five salons, up to ~200 conversations/day across the chain,
~6 turns each, typically 2–3 model calls per turn, ceiling 8 (`max_llm_calls`).
Cost per turn ≈ calls × (input tokens × input price + output tokens × output
price); prices were not looked up in this session, so the monthly figure is a
G08 task against the current Vertex price page, compared with A3. Billing
budget alerts notify only; enforcement is the per-turn and per-customer limits.
Cloud Run min instances 0 in staging, 1 in production (cold starts on a
customer chat); concurrency default.

## Failure and recovery

| Failure window | Customer sees | Retained state / possible effects | Safe next action and owner |
| --- | --- | --- | --- |
| Model unavailable / malformed call | "I'm having trouble — you can book at <link> or call <phone>" | Session turn, no proposal | Retry by customer; ADK model retries bounded |
| Booking API read fails | Same message with salon phone | No proposal | Customer retries |
| Confirm: API commits, response lost | "We couldn't confirm this yet — we're checking" | Operation `uncertain`; maybe one appointment | Reconcile by listing appointments on next view or a 5-minute job; unresolved → managers' daily list (owner: on-call dev) |
| Double click / two tabs confirm | Same result card twice | One operation | Atomic claim (D5) |
| Slot taken between propose and confirm | "That time has just gone — here are the nearest options" | Operation `failed`, no effect | Agent proposes again |
| Proposal from another customer's session or forged ID | 403 | Nothing | — |
| Token expired mid-chat | "Please sign in again" | Session kept | Customer signs in; same session if ownership matches |
| Budget exhausted | "You've reached today's limit — call <phone>" | Session kept | Resets next day |
| Release rollback | Conversation continues on previous revision | Sessions, proposals and operations retained; schema changes additive only in phase 1 | Cloud Run traffic back to previous revision (owner: deployer) |

## Verification and implementation handoff

Offline: unit and Runner tests with a scripted model and an in-memory fake
booking API (G02–G05, G07). Local integration: gateway with local Postgres and
a process restart (G03). Live, authorized only on the booking API staging
environment: G01 contract check and G11 rehearsal. Hosted: G08 foundation, G09 staging and production gateway, G11
production launch. Benefit (fewer phone changes) is a hypothesis measured from
the managers' daily list against the baseline in O4.

Release bundle for phase 1: Cloud Run revision, prompt file git SHA,
`gemini-3.8-flash`, `google-adk==2.8.0`, tool declaration hash, secret
versions — recorded in the deploy notes by G09.

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| O1 Does the booking API accept a customer token we can verify, or only a service key? (A6) | Decides D3 and whether the API itself also enforces ownership | Booking API owner; G01 | G03 |
| O2 Idempotency keys and a lookup for "did this request commit"? (A7) | Decides D5 replay vs lookup-before-retry | G01 | G04 final form |
| O3 Is there a staging booking API with test salons? | Live checks before production | G01 | G11 |
| O4 Baseline of phone/manual changes per week | Measures the benefit | Salon managers | Nothing in phase 1 |
| O5 Allow guests to book (phone verification)? | Adds an identity path | User | G17 |
| O6 Model choice gemini-3.8-flash vs gemini-3.5-flash | Quality/latency on the eval set | G07 result | Nothing |
| O7 Launch on working day 10 or 12? | The schedule check fits 10 days only at the low end; 12 days or 6 focused h/day close it | User; assumed: aim for 10, go/no-go at end of day 7 | G11 date |
