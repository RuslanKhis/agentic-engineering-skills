# System design: salon booking assistant (MVP)

Status: **draft**. The user was not available, so every scope-gate answer below is
assumed and every decision that depends on one is **provisional** until the team
confirms it. Nothing here has been implemented or tested.

Plan: [docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md).
Tickets: [docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/).

## Assumed answers

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Deadline, and what follows? | Live for real customers 10 working days from start; continued and improved afterwards, so phase 1 code is kept | Phase split, kept-code form, D8 |
| A2 | Who builds it, hours, familiarity? | 3 developers, about 6 hours a day on this for 10 days, focus factor 0.6; fluent in Python and already run the booking API on GCP; **new to ADK** (1.5× multiplier) | Capacity, cut line, owner split |
| A3 | Money for models and cloud? | About USD 300 a month for the MVP (model plus Cloud Run plus Cloud SQL), set as a billing budget alert | D7, model tier |
| A4 | Who uses it? | External customers of the five salons, in a chat widget on the chain's existing booking website, signed in with the website's existing customer account | D3, D6, MVP profile |
| A5 | Data and effects? | Customer names, contact details and appointment history (personal, not special-category); the assistant creates, moves and cancels real appointments, which trigger the booking system's existing confirmation messages to the customer and salon. No payments, deposits or fees through the assistant | Floor, D4, D5 |
| A6 | Booking API contract | The team owns it; it has a staging environment, customer-scoped reads, and slot uniqueness enforced server side. Whether it accepts an idempotency key is **unknown** (G01 settles it) | D4, D5, G03 |
| A7 | Customer sign-in | The website issues a verifiable session token (JWT or session cookie the backend can validate) carrying the booking-system customer ID | D3, G04 |
| A8 | Languages and channel | One language (the website's), web only; no SMS, WhatsApp or phone | Scope; later list |
| A9 | Region and residency | No residency constraint beyond running in the booking API's existing GCP region | D9, G08 |
| A10 | Traffic | Up to about 300 conversations a day across five salons, peaks under 10 concurrent | D7, D9 sizing |

Delivery profile: **MVP** — first external users completing a journey that changes
real records; the team must see failures and cost. Correct me if this is really an
internal pilot for salon staff, which would lower identity and abuse depth.

## Purpose and journey

**Running example.** Priya, a signed-in customer, opens the chat on the chain's
site and types "Can I move my Thursday cut at Northside to Saturday morning?".
Today she has to find the appointment, cancel, and rebook through a multi-step form
or phone the salon during opening hours. The assistant finds her Thursday
appointment, lists Saturday-morning slots for the same stylist and service,
and shows a card: "Move *Cut & finish with Sam* from **Thu 15 Oct 14:00** to
**Sat 17 Oct 10:30**, Northside — Confirm / Keep current". She presses Confirm; the
booking API moves the appointment and the card shows the receipt.

**Outcome to improve (hypothesis).** Share of book/move/cancel requests completed
without a phone call, with no rise in salon corrections. Baseline: unknown; G09
records the salon's current phone volume for these requests as the baseline.

**Model vs code.** The model interprets the request, asks clarifying questions and
chooses read and proposal tools. Code owns identity, the current date and salon
timezone, ownership checks, policy checks, the proposal record, the confirmation,
the write to the booking API and the rendered receipt.

**Non-goals for phase 1.** Payments or deposits, staff-side use, other channels,
other languages, recommendations, remembering preferences across sessions.

## Delivery constraints, depth and deferred controls

Capacity: 3 people × 60 hours × 0.6 = **108 focused hours**; 25% reserve leaves
**81 hours** for phase 1. Phase 1 (G01–G09) estimates **48–79.5 hours**, so it fits
at the high end. Cut line and per-person load are in the plan.

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 20-case labelled set, run before launch | Any prompt/model change → phase 2 CI gate (G10) |
| Identity and per-customer scope | Build: verified website token, customer ID only from code, cross-customer denial tests (G04) | — |
| Secrets | Build: workload identity for Vertex AI and Cloud SQL; booking-API credential in Secret Manager | Rotation in phase 2 when a second environment shares it |
| External writes | Build: no model write tool, proposal + confirm in code, one operation identity per proposal, reconciliation (G03) | — |
| Sensitive data | Minimal: tool results trimmed to needed fields; no message content in application logs; sessions kept 30 days | Erasure request, or a regulator/DPA question → G13 |
| Prompt injection and agency | Minimal by structure (see Security posture); a few injection cases in the eval set | Any new untrusted source (staff notes, reviews, email) → G12 |
| Budgets and loop limits | Build: `max_llm_calls` per turn, per-customer daily turn allowance, billing alert | Abuse or spend above 50% of A3 → stricter admission |
| Memory | Minimal: persistent conversation sessions only | Customers ask for "my usual" → G15 |
| Frontend | Build: plain-text chat widget with proposal cards | Streaming wanted after measuring latency → later |
| Hosting | Build: one Cloud Run service, staging + prod, previous revision kept for rollback | — |
| Observability | Minimal: structured logs with session/invocation IDs, token counts, write outcomes | First incident not attributable, or >1 salon complaint/week → G11 traces and SLOs |
| Release | Minimal: pinned model and ADK versions, release manifest, eval run before deploy (manual) | Second prompt change → G10 CI gate |
| Performance tuning | Defer | Measured p90 turn latency above 8 s |

**Floor kept:** no secrets in code, prompts or logs; spend stop (`max_llm_calls`,
per-customer allowance, budget alert); **no booking change without the customer
pressing Confirm on a card rendered from the stored proposal**; personal data scoped
to the signed-in customer and kept out of logs; model ID pinned.

**Graduation conditions** before staff use, another channel or a public
(non-signed-in) entry point: G10 (eval gate), G11 (traces, SLOs), G12 (adversarial
suite), G13 (retention/erasure). Deferred controls and their triggers are listed in
the plan's Later table.

## Guarantees and acceptance

| Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 A customer sees and changes only their own appointments | Gateway verifies the website token and writes `customer_id` into session state; tools read it from state, never from arguments; booking API calls are customer-scoped; confirm endpoint checks proposal owner | Read: "I can't find that appointment"; confirm: 404 | G04 tests: forged token, other customer's appointment ID in the message, other customer's proposal ID on confirm → zero reads/writes |
| I2 No booking change happens without the customer confirming that exact change | The model has only propose tools; only `POST /proposals/{id}/confirm` (ordinary code) writes; it executes the stored canonical payload, not anything the model says | Missing/expired/changed proposal → no API call | G03 scripted-model tests: model "claims" success, injected "confirm now" text, expired proposal → zero booking-API writes |
| I3 One confirmed proposal causes at most one booking change | Proposal row claimed atomically `pending→executing`; operation key = proposal ID; moves and cancels are absolute ("set to T", "cancel"), creates rely on API slot uniqueness plus reconciliation; idempotency key if G01 finds support | Lost response → status `uncertain`, card says "checking", reconciler resolves | G03: double click, retry after lost response, two workers → one fake-API effect |
| I4 Times shown are the salon's local times and match what is written | Code resolves salon timezone; card renders from the canonical payload with weekday | Ambiguous date → clarifying question | G02/G06 cases across a DST change and "next Saturday" |
| I5 A turn is bounded in model calls and a customer in daily turns | `RunConfig(max_llm_calls=8)`; allowance counter in Cloud SQL checked at the gateway | Polite stop message; no further model calls | G05 tests: 9th call stops; 51st turn rejected before the Runner |

## Architecture

```text
Browser (existing site, signed in)
  │  chat widget: POST /chat {session_id, text}   POST /proposals/{id}/confirm|decline
  ▼
Cloud Run service "booking-assistant" (FastAPI gateway + ADK Runner, one container)
  ├─ auth middleware: verify site token → customer_id (trusted)          [G04]
  ├─ admission: daily turn allowance (Cloud SQL)                         [G05]
  ├─ ADK Runner → LlmAgent "booking_assistant" (Vertex AI, pinned)       [G02]
  │     read tools: list_salons_and_services, find_availability, list_my_appointments
  │     propose tools: propose_booking, propose_move, propose_cancellation  [G03]
  ├─ confirm executor (no model): claim → recheck → booking API → receipt [G03]
  └─ DatabaseSessionService + proposals + allowance tables (Cloud SQL Postgres) [G05]
        │
        ▼
Existing booking API (team-owned; staging and prod)  ── sends its own confirmations
```

Trust boundaries: browser ↔ gateway (customer token); gateway ↔ Vertex AI and Cloud
SQL (Cloud Run service account); gateway ↔ booking API (service credential from
Secret Manager, every call carries the trusted `customer_id`).

### Decisions

All decisions are proposals awaiting the team; those marked † depend on assumed answers.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Understand free-text requests over a small capability set | One `LlmAgent` with six narrow function tools; no sub-agents | Book, move and cancel share the same context and data; nothing needs a separate identity or tool set | Multi-agent routing would add descriptions to maintain and evaluate, with no boundary to justify it | Eval set (G06) task-completion and tool-choice per case |
| D2 | Real effects need human approval (floor) | Propose-then-confirm: tools create a stored proposal; the widget's Confirm button calls ordinary code that executes it | ADK's native tool confirmation is listed as unsupported with `DatabaseSessionService` ([safe-api-tool-calls compatibility](../../.claude/skills/safe-api-tool-calls/references/compatibility.md), citing adk.dev confirmation known limitations); a code-path confirmation also keeps the write out of the model's reach | An extra table and endpoint versus a one-line `require_confirmation=True`; conversation must learn the outcome from state | I2 tests |
| D3† | Customers act only on their own records | Reuse the website login; gateway derives `customer_id`; tools have no customer parameter | A session ID is a locator, not permission; the model cannot name another customer | Depends on A7; if the site has no verifiable token, phase 1 needs an email one-time code (adds ~8–12 h, would push G07 or G06 to phase 2) | I1 tests |
| D4† | A confirmed change happens once, even on retries | Proposal ID is the operation identity; absolute operations; reconciliation by status lookup or by listing the customer's appointments; never re-dispatch an `uncertain` proposal with a new identity | Retries, double clicks and restarts refer to the same business operation | Uncertain outcomes are visible to the customer for a short time; needs G01's answer on idempotency keys | I3 tests |
| D5 | Recheck before effect | Confirm re-reads slot availability and ownership; proposals expire after 10 minutes | The slot or appointment may change while the card is open | A second API read per confirm (~100–300 ms, assumed) | G03 "slot taken while card open" case → no write, alternatives offered |
| D6 | Conversation survives instance changes | `DatabaseSessionService` on Cloud SQL Postgres (new database on the booking API's instance if it is Postgres, else a small new instance) | Cloud Run may route turns to different instances; in-memory sessions would lose context | A managed DB dependency; sharing an instance couples maintenance windows | G05: restart the process mid-conversation, next turn keeps context |
| D7† | Cost bounded for A3 | `gemini-3.8-flash` on Vertex AI, pinned; `max_llm_calls=8`; 50 turns/customer/day; budget alert at 50/90/100% of A3 (alerts only, not a cap) | Flash tier is enough for slot-finding dialogue; the lifecycle table ([model-lifecycle-2026-10-01.json](../../.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json), checked 2026-10-08) lists it stable with no shutdown; `gemini-3.6-flash` (Vertex retirement 2026-11-19) and `gemini-3.7-flash` (2027-01-28) would retire inside the plan horizon | Newest model has the shortest track record; fallback candidate `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later). Prices not looked up (no network): cost per conversation is a G08 measurement | Release manifest shows the exact ID; G08 records tokens per conversation |
| D8 | Phase 1 code is kept | FastAPI gateway around the Runner (not `adk web`), custom JSON contract, non-streaming replies | Custom contract lets the widget render proposal cards from the database, not from model text; non-streaming avoids partial-text retraction issues | Slower perceived first output; streaming later if measured latency needs it | G07 renders cards only from `/chat` response `proposals[]` |
| D9† | Hosting the team can run | One Cloud Run service per environment (staging, prod) in the booking API's region; prior revision retained | The team already runs GCP; one container is the smallest operable unit | Agent Runtime would remove gateway code but the custom confirm endpoint and auth would still need a host | G08 deploy readback and rollback rehearsal |

**ADK version.** Greenfield, nothing installed. Working assumption `google-adk==2.8.0`,
the version the specialist skills were checked against; the observability specialist
recommends 2.10.0 or later for a new production deployment
([adk-agent-observability compatibility](../../.claude/skills/adk-agent-observability/references/compatibility.md)).
G02's acceptance includes choosing and confirming the pin.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Owns: interpreting the request, clarifying ambiguous date/salon/service, choosing tools, explaining outcomes. Never states that a change is done; says "press Confirm on the card". Current date and salon list injected from state by code | `adk-agent-instructions`; rendered-request test |
| Tools (6, all function tools) | Read: `list_salons_and_services()`, `find_availability(salon_id, service_id, date_from, date_to, stylist_id?)` (≤10 slots), `list_my_appointments(include_past=False)` (≤10). Propose: `propose_booking(salon_id, service_id, slot_id)`, `propose_move(appointment_id, slot_id)`, `propose_cancellation(appointment_id)`. Each returns `{status, ...}` with actionable errors; none takes a customer ID | `adk-tool-interface-design`; declaration dump, bounded result test |
| Output and model | Plain text reply; no `output_schema` (cards come from the proposals table). `gemini-3.8-flash`, temperature low, thinking at the default low level (verify in G02) | `adk-model-and-output-contracts`; pinned-ID check |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, slots, services | Booking API (authoritative) | Booking API; assistant reads via tools, writes only via confirm executor | Live per call; never cached across turns | Booking system's own policy |
| Conversation session | Assistant, per customer | ADK Runner | Cloud SQL | 30 days, then deleted by a daily job (G13 formalises erasure) |
| Proposal | Assistant, per customer | Propose tools create; confirm/decline endpoints update | Cloud SQL; canonical payload + expiry | 90 days for reconciliation evidence |
| Daily turn allowance | Assistant, per customer | Gateway | Cloud SQL counter keyed by customer and salon-local date | 7 days |

Identities: **session** (one chat, many turns), **invocation** (one turn), **business
operation** (one proposal, possibly several confirm attempts). Logs carry all three.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking_assistant | The signed-in customer's own appointments | The customer's messages; free-text fields from the booking API (service descriptions, appointment notes) | None directly: propose tools only create pending records; replies go only to the same customer | Write leg removed from the agent: execution needs the customer's click on a card rendered from the stored payload. The widget renders plain text only (no links or images) to close an exfiltration path. Tool results strip notes fields in phase 1 |

Tool tiers: read (3), propose (3, write to the assistant's own table only). The
booking-API write is reachable only from the confirm executor.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and owner |
| --- | --- | --- | --- |
| Model unavailable or 8-call limit reached | "Sorry, I couldn't finish that — please try again or call the salon" | Session events up to the failure; no proposal or a pending one | Customer retries; pending proposal still confirmable until expiry |
| Model claims "booked!" without a proposal | Text says so but no card | Nothing written | Instruction forbids it; eval case checks it; widget shows only DB-backed cards |
| Slot taken between proposal and confirm | Card shows "That time was just taken"; agent offers alternatives on next turn | Proposal `rejected_stale`; no write | Customer picks another slot |
| Booking API commits, response lost / timeout | Card shows "Checking…" then final status | Proposal `uncertain` with operation key | Confirm executor reconciles (status lookup or appointment list) within the request, then a scheduled reconciler; never a fresh dispatch. Owner: Dev A |
| Double click / two tabs | Same receipt in both | One `executing` claim wins | Second request returns the first's result |
| Instance restart mid-turn | Turn fails; next turn has context | Session in Cloud SQL | Customer resends |
| Token expired or another customer's ID | Sign-in prompt / "can't find that appointment" | Nothing | — |
| Budget alert fires | No customer change; team notified | — | Team lowers allowance or disables widget via feature flag. Owner: Dev C |
| Bad release | Errors or wrong behaviour | — | Route traffic to previous Cloud Run revision; prompt and model ID roll back with the image (one release unit). Owner: Dev A |

## Verification and implementation handoff

Offline deterministic (all phase 1 goals): fake booking API with scripted outcomes,
scripted model for Runner tests, assertions on fake-API call counts. Local
integration: Postgres container restart (G05), widget against local gateway (G07).
Bounded live: the 20-case eval set against staging with the real model, capped at
about 200 model calls per run (G06, G09). Hosted: staging deploy readback, rollback
rehearsal, one-salon soft launch (G08, G09).

Release unit recorded in `release.json`: image digest, prompt version, model ID,
tool-schema hash, eval-set hash, secret versions. Rollback unit: previous Cloud Run
revision, retained 30 days.

Goals and owners are in the [plan](../plans/salon-booking-assistant.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| A6: does the booking API accept an idempotency key or offer operation status lookup? | Sets how I3 is enforced on creates | G01 (Dev A), reading the API code | G03 final reconciliation path |
| A7: can the backend verify the website's customer token? | If not, a one-time-code login enters phase 1 and something moves out | G01 + website owner | G04 |
| Cancellation policy (late-cancel window, fees) and who approves the assistant's wording | Fees would make cancellation a money effect | Salon operations lead | G09 launch (calendar wait) |
| A9 residency / A3 budget | Region and model tier | Founders | G08 |
| Launch shape: one salon first, then five? | Limits blast radius | Team | G09 |
