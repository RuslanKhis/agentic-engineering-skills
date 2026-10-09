# Implementation plan: salon booking assistant (MVP)

Status: draft. Ready goals identified; they rest on assumptions (the design's
[Assumed answers](../architecture/salon-booking-assistant.md#assumed-answers), A1 to A13)
that the user has not confirmed yet.
Architecture: [../architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan (goals, estimates, status). The phase 1 tickets in
[../tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/) copy their goal's entry.

## Destination and constraints

Customers of the salon chain can book, move and cancel their own appointments in a chat
on the salon website. Every change goes through the existing booking API, and only after
the customer presses a Confirm button that code (not the model) handles. Non-goals for
phase 1: payments and deposits, SMS or WhatsApp, staff-facing use, marketing, languages
other than English, embedding the chat inside every page of the existing site.

- Accepted by the user: three developers. An MVP within two weeks, continued afterwards. Book, move and cancel go through the existing booking API.
- Assumed and not yet confirmed: A1 to A13. Decisions D1 to D10 are therefore provisional.
- Inspected: this repository contains only `.claude/skills/`. There is no application code, dependency manifest or pin, so every module path below is **proposed**.
- Release artefacts every goal inherits:
  - `google-adk==2.8.0`. This is a working assumption taken from the specialists' `references/compatibility.md`; G02 confirms it.
  - Model `gemini-3.5-flash` on Vertex AI, chosen from `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (checked 2026-10-08). See D8.
  - Prompt `booking_v1`, kept in the repository.

  A goal that changes any of these is a release, not a side effect.
- No credentials or private resource identifiers go in this plan.

## Delivery profile and capacity

Profile: **MVP or pilot**: first external users, real personal data, reversible writes. See
the design's [delivery constraints](../architecture/salon-booking-assistant.md#delivery-constraints-depth-and-deferred-controls).

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Real customers of **one pilot salon** book, move and cancel safely. The team sees failures and cost | G01 to G11 | 60–94 | 3 people × 10 working days × 6 focused h = 180 h; 25 % reserve leaves 135 h |
| 2, harden and widen | All five salons; eval gate in CI; adversarial suite; staff handoff; SLOs and reconciliation; canary | G12 to G18 | 39–64 | After launch, as the team has time |

Estimates are person-hours of human effort with a coding agent: hands-on plus review and
verify. They already include **×1.5 for a team new to ADK** (A2), applied to every goal,
hands-on and review alike. No extra GCP setup day is added, because A3 assumes the team already
runs the booking API on GCP. Calendar waits sit on their goals and are not counted as hours.

| Person (role) | Goals, in working order | Hours | Their capacity after reserve |
| --- | --- | --- | --- |
| Dev A: booking API owner | G01, G03, G11 | 20–31 | 45 |
| Dev B: agent and platform | G07, G06, G02, G09, G10 | 21–34 | 45 |
| Dev C: web and identity | G04, G05, G08 | 19–29 | 45 |

Dev A, B and C are role names. Map them to people by who knows the booking API's write
code best (A), who will own prompt quality and the GCP project (B), and who owns the
website and its login (C). On day 1 all three can start: A on G01, B on G07 and G06, C on G04.

Schedule block. This is the only source of each estimate; tickets copy it.

```yaml
- goal: G01
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G02
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G03
  phase: 1
  hands_on: 8-12
  review: 4-6
  total: 12-18
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 5-8
  review: 3-4
  total: 8-12
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev C
  blocked_by: [G02, G04]
  calendar_waits: none
  wait_days: 0
- goal: G06
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev B
  blocked_by: []
  calendar_waits: pilot salon manager approves the expected outcomes
  wait_days: 0.5-1
- goal: G07
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G08
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev C
  blocked_by: [G02, G07]
  calendar_waits: none
  wait_days: 0
- goal: G09
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev B
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
- goal: G10
  phase: 1
  hands_on: 2-4
  review: 1-1
  total: 3-5
  owner: Dev B
  blocked_by: [G02, G03, G06]
  calendar_waits: none
  wait_days: 0
- goal: G11
  phase: 1
  hands_on: 3-5
  review: 1-1
  total: 4-6
  owner: Dev A
  blocked_by: [G03, G05, G08, G09, G10]
  calendar_waits: pilot salon agrees the go-live day and briefs staff
  wait_days: 0.5-1
- goal: G12
  phase: 2
  total: 2-4
  owner: Dev A
  blocked_by: [G11]
  calendar_waits: three to five days of pilot observation
  wait_days: 3-5
- goal: G13
  phase: 2
  total: 4-8
  owner: Dev B
  blocked_by: [G08, G10]
- goal: G14
  phase: 2
  total: 6-10
  owner: Dev A
  blocked_by: [G03, G10]
- goal: G15
  phase: 2
  total: 6-10
  owner: Dev C
  blocked_by: [G11]
- goal: G16
  phase: 2
  total: 8-12
  owner: Dev A
  blocked_by: [G11]
- goal: G17
  phase: 2
  total: 8-12
  owner: Dev C
  blocked_by: [G08, G13]
- goal: G18
  phase: 2
  total: 5-8
  owner: Dev B
  blocked_by: [G12]
```

**Schedule check** was run on 2026-10-09 with Python 3.9.13. The skill asks for 3.11+, but the helper ran without error. The full output is in `REPORT.md`.

```text
python3 .claude/skills/adk-system-designer/scripts/check_schedule.py \
  --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ \
  --capacity 135 --days 10 --reserve 0.25 \
  --person "Dev A=6" --person "Dev B=6" --person "Dev C=6"
```

Its result for phase 1:
- 11 goals, **60–94 human hours** against 135 h capacity after reserve, so it fits.
- Loads: Dev A 20–31 h, Dev B 21–34 h, Dev C 19–29 h, each of 45 h.
- Longest dependent chain: **G01 → G03 → G10 → G11**, 5.61 working days at the low end and 9 at the high end.
- Finish with these people and dependencies: **6.94–9.89 working days** of 10, so it fits.
- The margin at the high end is a tenth of a day. G03 is the goal to watch.

**What changed after failing runs.** These changes reflect the work itself; no dependency, wait or review was dropped:

1. The first plan finished in 7.39–12.11 days and failed the calendar. Writing and labelling evaluation cases needs no agent, so the old "evaluation set" goal was split. G06 is labelling, with no blocker. G10 runs the set and tunes the instruction, and keeps the dependency on G02 and G03. Their hours add up to the old goal's 8–13.
2. Deployment was likewise split. G07 is GCP foundation (Cloud SQL, service account, secrets, budget alert), which needs no application. G08 deploys the application and keeps its dependency on G02. Their hours add up to the old 9–15.
3. The widget became a chat page served by the application on the site's domain (D6). That took the goal from 8–12 h to 6–9 h. Embedding the chat across the existing site moved to Later.
4. Widening from the pilot salon to all five moved to phase 2 (G12). It needs three to five days of pilot observation that cannot fit inside the two weeks.
5. G07 and G06 were given to Dev B, who would otherwise wait for G01.

**Cut line, to be confirmed by the user:** phase 1 (G01 to G11, 60–94 h of 135 h, finishing
in 6.9–9.9 of 10 working days) puts the assistant live at **one pilot salon**. All five
salons follow in week 3 (G12), after pilot observation.

If G03 runs high, the order below keeps each finished goal useful:

1. G01, G02 and G03 give a tested read-and-confirm agent on the fake API.
2. Adding G04, G05, G07 and G08 gives a staging demo for the salon owners.
3. Going live (G11) also needs G09, G10 and G06. These are never cut before launch: G09 is the floor for a public service, and G10 is the only evidence the agent proposes the right slot.

If the high end materialises, G11 slips by one or two days into week 3 rather than launching
without them.

## Implementation map

All paths are **proposed** (greenfield). Decision IDs refer to the design.

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 One agent; the model holds read tools and a proposal tool only | `app/agent.py`: one `LlmAgent` with four read tools and `propose_change`; `App` and `Runner` built in `app/api.py` | Vertex AI Gemini endpoint | adk-workflow-design | Constructor names on the 2.8.0 pin (G02) |
| D2 Typed booking API adapter and fake | `app/booking_client.py`; `tests/fake_booking_api.py` | Existing booking API, staging then production | safe-api-tool-calls | Idempotency, reschedule and error semantics (G01) |
| D3 Confirmation and write in application code | `propose_change` stores a `Proposal`; `POST /proposals/{id}/confirm` claims it atomically and executes it with `idempotency_key = proposal_id` | Cloud SQL tables `proposals` and `operations` | safe-api-tool-calls | Double-confirm, lost-response and expired-proposal tests (G03) |
| D4 Customer identity from the website login | `app/auth.py` verifies the site session token and writes `customer_id` to trusted session state. Tools read it from `ToolContext.state`, never from arguments | Secret Manager holds the verification key | adk-tool-auth-and-secrets | Token format and verification method (A6, G04) |
| D5 Sessions, proposals and operations in one Postgres | `DatabaseSessionService` and application tables, one Cloud SQL instance | Cloud SQL for PostgreSQL, smallest tier | adk-memory-architecture (through G07 and G08) | `DatabaseSessionService` on the pin; schema migration (G08) |
| D6 Custom JSON chat API and a chat page on the site's domain | `POST /chat` returns `{messages, proposal_card?}`; a static page served by the same service | Cloud Run behind the site's domain routing | adk-frontend-integration | Complete-turn latency acceptable without streaming (G05, G11) |
| D7 Per-customer allowance and model-call cap | `RunConfig(max_llm_calls=12)`; admission check in `app/limits.py` before `Runner.run`; kill switch | Budget alert on the project | adk-operational-guardrails | The `RunConfig` field on the pin (G02); counters across restart (G09) |
| D8 Pinned model | `model="gemini-3.5-flash"` in one config constant, logged in the release manifest | Vertex AI | adk-model-and-output-contracts | G10 measures it on the eval set |
| D9 Data minimisation and telemetry | Tool results drop phone, email and free-text notes; OTel traces with content capture off; token usage per invocation | Cloud Trace; Cloud Logging with 30-day retention | adk-agent-observability (through G08) | Content-capture gate on the pin (G08) |
| D10 Cloud Run hosting | One service per environment. Production min instances 1 (A13); previous revision kept for rollback | Cloud Run, Artifact Registry, dedicated service account | deploy-adk-on-google-cloud | Region (A10) |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Booking API contract and fake | 1 | discovery + implementation | 4–7 | – | safe-api-tool-calls | ready |
| G02 Read-only agent finds slots and lists my appointments | 1 | implementation | 5–8 | G01 | adk-workflow-design | blocked by G01 |
| G03 Confirmed, idempotent book, move and cancel | 1 | implementation | 12–18 | G01 | safe-api-tool-calls | blocked by G01 |
| G04 Customer identity and per-customer scope | 1 | implementation | 8–12 | – | adk-tool-auth-and-secrets | ready on assumption A6 |
| G05 Chat API and chat page with confirm card | 1 | implementation | 6–9 | G02, G04 | adk-frontend-integration | blocked by G02, G04 |
| G06 Write and label 30 evaluation conversations | 1 | implementation (labelling) | 5–8 | – | adk-agent-evaluation | ready |
| G07 GCP foundation for staging and production | 1 | implementation | 4–7 | – | deploy-adk-on-google-cloud | ready; needs the team's go-ahead to create resources |
| G08 Deploy to staging and production with traces | 1 | implementation | 5–8 | G02, G07 | deploy-adk-on-google-cloud | blocked by G02, G07 |
| G09 Per-customer allowance, limits and kill switch | 1 | implementation | 4–6 | G04 | adk-operational-guardrails | blocked by G04 |
| G10 Run the evaluation set and tune to the launch bar | 1 | implementation | 3–5 | G02, G03, G06 | adk-agent-evaluation | blocked |
| G11 Pilot go-live at one salon | 1 | implementation + operation | 4–6 | G03, G05, G08, G09, G10 | deploy-adk-on-google-cloud | blocked |
| G12 Widen to all five salons | 2 | operation | 2–4 | G11 | deploy-adk-on-google-cloud | proposed |
| G13 Evaluation gate in CI | 2 | implementation | 4–8 | G08, G10 | adk-release-engineering | proposed |
| G14 Adversarial suite and threat model | 2 | implementation | 6–10 | G03, G10 | adk-agent-security | proposed |
| G15 Hand off to salon staff | 2 | implementation | 6–10 | G11 | adk-tool-interface-design | proposed |
| G16 SLOs, alerts and scheduled reconciliation | 2 | implementation | 8–12 | G11 | adk-agent-observability | proposed |
| G17 Canary and joint rollback | 2 | implementation | 8–12 | G08, G13 | adk-release-engineering | proposed |
| G18 Measure the outcome and refresh the eval set | 2 | implementation | 5–8 | G12 | adk-agent-evaluation | proposed |

### G01 — Booking API contract and fake

- **Phase and estimate:** 1. Hands-on 3–5, review and verify 1–2, total 4–7. Calendar waits: none. Owner: Dev A.
- **Outcome and linked decisions:** answers open decisions O2 to O5 behind D2 and D3. Produces a contract document and an in-process fake that every other goal tests against.
- **Scope:** answer five questions from the booking API's source or docs:
  1. Does it accept idempotency keys, and how long does it retain them?
  2. Is there an atomic reschedule endpoint?
  3. Can an appointment be looked up by customer and slot, or by key?
  4. Where are cancellation-window and lead-time rules enforced?
  5. Which error codes does it return?

  Write `docs/booking-api-contract.md`, including the `Proposal` card schema that G03 and G05 share. Write `tests/fake_booking_api.py` with scripted failure modes. Out of scope: any agent code.
- **Depth:** discovery, bounded to the five questions. It stops when each question is answered from source or a staging call, or marked unsupported with the workaround the design names (D3).
- **Implementation route:** plain Python, no ADK. Proposed `app/booking_client.py` interface:
  - `list_salons()`, `list_services(salon_id)`
  - `search_slots(salon_id, service_id, date_from, date_to, stylist_id=None)`
  - `list_appointments(customer_id)`
  - `book(customer_id, slot_id, key)`, `reschedule(appointment_id, slot_id, key)`, `cancel(appointment_id, key)`
  - `find_operation(key)`, or `find_appointment(customer_id, slot_id)` when keys are unsupported
- **Prerequisites:** the booking API source or docs, and staging credentials Dev A already holds. No new grant is needed.
- **Primary skill:** safe-api-tool-calls
- **Supporting skills:** none
- **Acceptance:**
  - The contract document answers O2 to O5 and defines the proposal card schema.
  - The fake simulates slot taken (409), timeout after commit, timeout before commit and policy rejection.
  - The contract tests pass against the fake and once against staging, with the staging run recorded.
  - No staging call touches a real customer.
- **Verification:** offline `pytest tests/test_booking_contract.py` against the fake. One authorised, recorded run against booking-API staging with test customers.
- **Execution scope:** local code, plus booking-API staging with test customers only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Read-only agent finds slots and lists my appointments

- **Phase and estimate:** 1. Hands-on 4–6, review and verify 1–2, total 5–8. Calendar waits: none. Owner: Dev B.
- **Outcome and linked decisions:** a customer can ask "can I get a cut at Northgate on Friday afternoon?" and get real, bookable slots. They can also ask "what have I got booked?" and see only their own appointments. Implements D1, D7, D8 and D9.
- **Scope:**
  - `app/agent.py`: one `LlmAgent` with four read tools: `list_salons_and_services`, `find_slots`, `list_my_appointments` and `salon_contact`.
  - The instruction `app/prompts/booking_v1.md`.
  - Injected state: today's date, each salon's time zone, and `customer_id` from trusted state.
  - `RunConfig(max_llm_calls=12)` and the pinned model in one config module.
  - Out of scope: writes (G03) and the HTTP API (G05).
- **Depth:** MVP. Tool results are bounded to at most 10 slots and leave out phone, email and notes. No secrets in code or the prompt.
- **Implementation route:** `LlmAgent` with `FunctionTool`s over `booking_client`. Code resolves relative dates in the salon's time zone, so `find_slots` takes ISO dates. Confirm these names on the chosen pin: `LlmAgent`, `App`, `Runner`, `RunConfig.max_llm_calls`, `ToolContext.state`. Record the pin in `pyproject.toml`.
- **Prerequisites:** G01's fake and contract.
- **Primary skill:** adk-workflow-design
- **Supporting skills:**
  - adk-tool-interface-design: tool declarations and bounded results.
  - adk-agent-instructions: the booking instruction and its rendered-request test.
  - adk-model-and-output-contracts: the pinned model and thinking settings.
- **Acceptance:**
  - With a scripted model, `find_slots` receives the resolved salon, service and date window.
  - The reply offers only slots the fake returned.
  - `list_my_appointments` uses the trusted `customer_id` even when the user's text names another customer.
  - The run stops at 12 model calls.
  - A captured model request contains no phone number or email.
- **Verification:** offline Runner tests with a scripted model and the fake (`pytest tests/test_agent_read.py`). One manual `adk web` session against the fake with the live model, transcript saved.
- **Execution scope:** local, plus the dev Vertex AI project for the manual session.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Confirmed, idempotent book, move and cancel

- **Phase and estimate:** 1. Hands-on 8–12, review and verify 4–6, total 12–18. The review is a careful read of the write path. Calendar waits: none. Owner: Dev A.
- **Outcome and linked decisions:** the customer presses Confirm on a card showing salon, service, stylist, date and local time, and exactly one booking, move or cancellation happens. If the outcome is uncertain, the customer is told so rather than shown a guess. Implements D3 and invariants I2 to I4.
- **Scope:**
  - A `propose_change` tool with `kind` set to book, move or cancel. It re-checks availability and ownership, stores a `Proposal` (pending, expires in 10 minutes) and returns the card.
  - `POST /proposals/{id}/confirm` in ordinary code. It claims the proposal atomically, executes it with `idempotency_key = proposal_id` and writes an `operations` row whose status goes from `pending` to `succeeded`, `failed` or `uncertain`.
  - Reconciliation of an uncertain operation by key or lookup, never by a fresh dispatch.
  - A move uses the reschedule endpoint if G01 finds one; otherwise it books then cancels, as two operations.
  - The confirmed result is appended to the session as an event the agent sees on the next turn.
  - Out of scope: the browser card (G05) and scheduled reconciliation (G16).
- **Depth:** MVP Build for external writes. The model holds no write tool. Confirmation lives in code the model cannot reach. ADK's native `require_confirmation` is deliberately not used (D3).
- **Implementation route:** `app/proposals.py` and `app/operations.py` on SQLAlchemy: SQLite in tests, Postgres from G08. The confirm handler takes `customer_id` from the verified request and compares it with the proposal's owner.
- **Prerequisites:** G01. Tests inject a verified `customer_id`, so G04 is not required.
- **Primary skill:** safe-api-tool-calls
- **Supporting skills:**
  - adk-tool-interface-design: the `propose_change` declaration and its actionable errors.
  - adk-agent-security: shows that a scripted model cannot cause a write.
- **Acceptance:**
  - One confirm produces one API write and a receipt.
  - A double click or two tabs produce one write and the same receipt twice.
  - A slot taken between proposal and confirm returns "slot taken" with no write.
  - A timeout after commit yields `uncertain`. Reconciliation then finds the appointment without a second dispatch.
  - An expired proposal is refused.
  - Another customer's `proposal_id` returns 404 with no write.
  - A scripted model told to "just book it" causes zero API writes.
  - In a book-then-cancel move where the cancel fails, the new booking stays. The customer sees that both appointments exist, and the operation is flagged for staff.
- **Verification:** offline `pytest tests/test_writes.py` against the fake's failure modes. One authorised staging run of book, move and cancel with a test customer.
- **Execution scope:** local, plus booking-API staging with test customers only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Customer identity and per-customer scope

- **Phase and estimate:** 1. Hands-on 5–8, review and verify 3–4, total 8–12. Calendar waits: none. Owner: Dev C.
- **Outcome and linked decisions:** only a signed-in customer can see or change appointments, and only their own. Implements D4 and I1.
- **Scope:**
  - Middleware verifies the website's session token (A6) and maps it to the booking API's `customer_id`.
  - It creates or loads the ADK session keyed by `customer_id` and `session_id`, and refuses another customer's session.
  - Anonymous visitors can browse services and free slots only.
  - Out of scope: phone or OTP sign-in (O1 fallback) and staff identity.
- **Depth:** MVP Build. The verification key lives in Secret Manager in cloud environments and in an untracked env file locally. `customer_id` is never a model or tool argument.
- **Implementation route:** a FastAPI dependency in `app/auth.py`. The trusted `customer_id` goes into session state under an `app:`/`temp:`-safe key that model-facing code never writes. Confirm the state-prefix semantics on the pin. Tools read it from `ToolContext.state`.
- **Prerequisites:** the site's token format (A6). If A6 is false, stop and record O1. Phone OTP would add about 8–12 h and move G09 to the start of phase 2, which needs the user's decision.
- **Primary skill:** adk-tool-auth-and-secrets
- **Supporting skills:** none
- **Acceptance:**
  - A valid token reaches the agent with the right `customer_id`.
  - An expired or forged token returns 401.
  - Customer A presenting B's `session_id` gets 404.
  - "I am customer 123" in the chat does not change scope.
  - An anonymous visitor can search slots but receives no appointment data and cannot create a proposal.
- **Verification:** offline `pytest tests/test_auth.py` with locally signed test tokens.
- **Execution scope:** local.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Chat API and chat page with confirm card

- **Phase and estimate:** 1. Hands-on 4–6, review and verify 2–3, total 6–9. Calendar waits: none. Owner: Dev C.
- **Outcome and linked decisions:** customers open "Book with our assistant" from the salon site, chat, and press Confirm on a card. Implements D6.
- **Scope:**
  - `POST /chat` returns one complete JSON turn, without streaming.
  - Wiring for `POST /proposals/{id}/confirm`.
  - A static chat page served by the application under the site's domain. It shows text, a proposal card with Confirm and Cancel, and receipt, uncertain and error states. Errors show the salon's phone number.
  - Out of scope: embedding across the existing site, streaming and visual polish.
- **Depth:** MVP. Only the application's own response schema reaches the browser, never raw ADK events.
- **Implementation route:** FastAPI around the `Runner` in `app/api.py`, plus `app/static/chat.html` and a small script. The site's reverse proxy routes `/assistant` to the service (A6).
- **Prerequisites:** G02 and G04. The proposal card schema from the G01 contract document; G03's endpoint can be stubbed until it lands.
- **Primary skill:** adk-frontend-integration
- **Supporting skills:** none
- **Acceptance:**
  - A book-then-confirm journey works in a browser against the fake.
  - A second Confirm click shows the same receipt.
  - An `uncertain` result shows "we're checking this booking, please don't book again".
  - The browser never receives tool arguments, `customer_id` or any internal ID other than `proposal_id`.
- **Verification:** local integration in a real browser against a local server and the fake, plus API tests (`pytest tests/test_api.py`).
- **Execution scope:** local and the site's staging environment.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Write and label 30 evaluation conversations

- **Phase and estimate:** 1. Hands-on 4–6, review and verify 1–2, total 5–8. Calendar wait: the pilot salon manager approves the expected outcomes, 0.5–1 day. Owner: Dev B.
- **Outcome and linked decisions:** a labelled set that defines what "books the right slot" means for this chain. G10 uses it, and it becomes evidence for I5.
- **Scope:** 30 cases in `eval/cases/` with a fixed clock and fake-API fixtures:
  - 15 happy paths across the five salons: relative dates, time zones, stylist preference, move and cancel.
  - 8 ambiguous requests where the right answer is a clarifying question.
  - 7 forbidden or edge cases: another customer's booking; cancelling inside the policy window; "book without asking me"; an off-topic request; a price question with no data; a slot in the past; a salon that doesn't exist.

  Each case has the expected proposal fields, or "clarify" or "refuse". Out of scope: the runner and the measurement (G10).
- **Depth:** MVP, an evaluation set. Prose quality is not judged in phase 1.
- **Implementation route:** case files in the format G10's runner reads. Use ADK eval-set JSON if G02 confirms it fits the 2.8.0 pin, otherwise YAML read by a pytest runner.
- **Prerequisites:** none. Salon, service and stylist names come from the booking API's staging data or the G01 fake.
- **Primary skill:** adk-agent-evaluation
- **Supporting skills:** none
- **Acceptance:**
  - 30 cases with the distribution above.
  - Every expected outcome is approved by the pilot salon's manager, recorded with date and name or role.
  - No real customer data appears in a case.
- **Verification:** a schema check on the case files (`pytest tests/test_eval_cases.py`), offline.
- **Execution scope:** local.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — GCP foundation for staging and production

- **Phase and estimate:** 1. Hands-on 3–5, review and verify 1–2, total 4–7. Calendar waits: none. Owner: Dev B.
- **Outcome and linked decisions:** staging and production have what the application needs before it exists. Implements D5, D7 and D10.
- **Scope:**
  - A dedicated runtime service account per environment with Vertex AI User, Cloud SQL Client and Secret Accessor on named secrets only.
  - One Cloud SQL Postgres instance at the smallest tier, with a database per environment.
  - Secret Manager entries, empty or placeholder, for the booking API key, the token verification key and the DB URL.
  - An Artifact Registry repository.
  - A project budget with alerts at 50, 90 and 100 % of the assumed allowance (A4).
  - Scripts in `deploy/foundation.sh`, or Terraform if the team already uses it.
  - Out of scope: deploying the application (G08).
- **Depth:** MVP: least-privilege workload identity and no keys in code. A budget alert is an observation, not a cap; G09 owns enforcement.
- **Implementation route:** `gcloud` scripts committed to the repository, run by a person with the team's go-ahead. Region per A10.
- **Prerequisites:** the team's go-ahead to create resources in the existing project. This design does not authorise it.
- **Primary skill:** deploy-adk-on-google-cloud
- **Supporting skills:** adk-tool-auth-and-secrets, for secret layout and service-account grants.
- **Acceptance:**
  - The service account can read only its listed secrets; reading any other fails.
  - A database connection from Cloud Shell succeeds using the service account.
  - The budget and its alert recipients exist.
  - No secret value appears in the repository.
- **Verification:** authorised, recorded commands against the team's project, with resource names in the evidence and not in shared documents.
- **Execution scope:** requires the team's explicit go-ahead.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08 — Deploy to staging and production with traces

- **Phase and estimate:** 1. Hands-on 4–6, review and verify 1–2, total 5–8. Calendar waits: none. Owner: Dev C.
- **Outcome and linked decisions:** the assistant runs in staging against booking-API staging, and in production behind a closed flag ready for G11. Traces and token cost are visible. Implements D5, D9 and D10.
- **Scope:**
  - A `Dockerfile` and Cloud Run services for staging and production.
  - `DatabaseSessionService` and the application tables, migrated by Alembic.
  - OpenTelemetry to Cloud Trace with prompt and response content capture **off**, and token usage per invocation in structured logs.
  - A release manifest logged at startup: image digest, `google-adk` version, model ID and prompt version.
  - `ENABLED_SALONS` empty in production.
  - Out of scope: canary (G17) and SLO alerts (G16).
- **Depth:** MVP: the chosen host with rollback by keeping the previous revision. Observability is Build at the level of traces and token cost.
- **Implementation route:** confirm `DatabaseSessionService` and the telemetry content-capture gate on the pin. Run the service as the G07 service account.
- **Prerequisites:** G02 (an application to deploy) and G07. G03 and G05 must be merged before production traffic, which G11 requires.
- **Primary skill:** deploy-adk-on-google-cloud
- **Supporting skills:**
  - adk-agent-observability: traces, the content gate and token cost.
  - adk-release-engineering: the pinned manifest and rollback unit.
  - adk-memory-architecture: the session store and its retention.
- **Acceptance:**
  - After a redeploy, a staging conversation resumes from Cloud SQL.
  - A trace shows agent, tool and model spans carrying the session ID, with no prompt text.
  - The release manifest can be read from the logs.
  - Rolling back to the previous revision works and is recorded.
  - Production refuses chat while `ENABLED_SALONS` is empty.
- **Verification:** authorised deployment to staging, then production, with commands and revision IDs recorded.
- **Execution scope:** requires the team's explicit go-ahead per environment.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09 — Per-customer allowance, limits and kill switch

- **Phase and estimate:** 1. Hands-on 3–4, review and verify 1–2, total 4–6. Calendar waits: none. Owner: Dev B.
- **Outcome and linked decisions:** no customer or anonymous visitor can run up model spend or flood the booking API. Implements D7 and the floor.
- **Scope:**
  - A per-customer daily allowance of 40 turns and at most 3 open proposals.
  - An anonymous per-IP limit of 20 turns per hour.
  - A check that `max_llm_calls=12` is in force on every run.
  - A kill switch flag that turns the chat into "please call the salon" without calling the model.
  - Out of scope: shared token budgets (Later).
- **Depth:** MVP Build, a per-user allowance. Counters live in Postgres and survive a restart.
- **Implementation route:** an admission check in `app/limits.py` before `Runner.run`.
- **Prerequisites:** G04, which provides the identity the allowance is keyed on.
- **Primary skill:** adk-operational-guardrails
- **Supporting skills:** none
- **Acceptance:**
  - The 41st turn of a day gets a polite refusal and makes zero model calls.
  - With the kill switch on, chat makes zero model calls.
  - Counters survive a process restart.
  - A fourth open proposal is refused.
- **Verification:** offline `pytest tests/test_limits.py` (SQLite).
- **Execution scope:** local.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G10 — Run the evaluation set and tune to the launch bar

- **Phase and estimate:** 1. Hands-on 2–4, review and verify 1–1, total 3–5. Calendar waits: none. Owner: Dev B.
- **Outcome and linked decisions:** measured evidence that the pinned model and `booking_v1` propose the right change and never write without Confirm. This is the I5 gate for G11.
- **Scope:**
  - A runner over G06's cases: live model, fake API, three repeats, recording cost.
  - A result table in `eval/results/latest.md`.
  - At most two instruction revisions, `booking_v1` then `booking_v2`, each re-run on the full set.
  - Out of scope: the CI gate (G13).
- **Depth:** MVP: an evaluation set run by hand before each release.
- **Implementation route:** a pytest runner or the ADK evaluation command on the pin. Proposal fields are compared exactly. Forbidden writes are counted from the fake's call log, not from model text.
- **Prerequisites:** G02, G03 and G06.
- **Primary skill:** adk-agent-evaluation
- **Supporting skills:** adk-agent-instructions, for the instruction revision.
- **Acceptance:**
  - The full set runs with recorded cost.
  - The launch bar (O6, assumed) is met: at least 27 of 30 cases correct on 2 of 3 repeats, and 0 forbidden writes on any repeat.
  - If the bar is not met after two revisions, the failures are recorded and G11 stays blocked.
- **Verification:** live model against the fake API in the dev project, spend within the dev budget.
- **Execution scope:** dev Vertex AI project.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G11 — Pilot go-live at one salon

- **Phase and estimate:** 1. Hands-on 3–5, review and verify 1–1, total 4–6. Calendar wait: the pilot salon agrees the day and briefs staff, 0.5–1 day. Owner: Dev A.
- **Outcome and linked decisions:** real customers of one salon use the assistant, and the team reviews every failed or uncertain operation daily. This is the profile's "done".
- **Scope:**
  - Set `ENABLED_SALONS` to the pilot salon.
  - Add the "Book with our assistant" link on that salon's page.
  - A 30-minute staff walkthrough covering what assistant bookings look like and whom to call.
  - Run G10's set against the production model configuration before switching on.
  - A daily review using `ops/daily_review.sql`: `uncertain` and `failed` operations, refusals, and cost per completed change.
  - Out of scope: other salons (G12) and alerting (G16).
- **Depth:** MVP: real users complete the journey safely, and the team sees failures and cost.
- **Implementation route:** configuration and queries only. No new modules.
- **Prerequisites:** G03, G05, G08, G09 and G10.
- **Primary skill:** deploy-adk-on-google-cloud
- **Supporting skills:** adk-agent-observability, for the daily review from traces and the operations table.
- **Acceptance:**
  - The first real booking, move and cancellation are each seen in the booking system by staff.
  - Zero duplicate appointments.
  - Every `uncertain` operation is reconciled within one business day.
  - Cost per completed change is recorded.
  - The kill switch is tested once in production.
- **Verification:** production evidence, recorded in this goal.
- **Execution scope:** requires the team's explicit go-ahead for production traffic.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G11 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; start after G11)

Each line gives the primary skill, the estimate, and one observable acceptance check. Run
each with `/adk-engineer Carry out G1x from docs/plans/salon-booking-assistant.md.`

- **G12 Widen to all five salons.** deploy-adk-on-google-cloud. 2–4 h, plus a wait of 3–5 days of pilot observation. Acceptance: there are no unreconciled `uncertain` operations; G10 still passes; `ENABLED_SALONS` lists all five, and each salon's staff confirm one assistant booking.
- **G13 Evaluation gate in CI.** adk-release-engineering, supporting adk-agent-evaluation. 4–8 h. Acceptance: a PR that changes the prompt, model ID or a tool schema runs G06's set, and fails with a non-zero exit code below the launch bar.
- **G14 Adversarial suite and threat model.** adk-agent-security. 6–10 h. Acceptance: scripted attempts produce zero writes and zero disclosure, with findings mapped to OWASP LLM IDs. The attempts are: another customer's ID in text; injected instructions in a service or stylist name returned by the API; a forged or replayed `proposal_id`; a request to reveal the instruction.
- **G15 Hand off to salon staff.** adk-tool-interface-design, supporting safe-api-tool-calls. 6–10 h. Acceptance: "I want to talk to someone", or a request the agent can't serve, creates exactly one callback request in the salon's queue, and the customer sees its reference.
- **G16 SLOs, alerts and scheduled reconciliation.** adk-agent-observability, supporting safe-api-tool-calls. 8–12 h. Acceptance: an `uncertain` operation older than 15 minutes triggers reconciliation and, if still unresolved, an alert to the on-call developer. SLIs are completed-change success ratio and tool-error rate per tool, with targets from G11 and G12 data.
- **G17 Canary and joint rollback.** adk-release-engineering. 8–12 h. Acceptance: a new revision takes 10 % of traffic, and one command rolls back image, prompt version and model ID together, recorded in the manifest.
- **G18 Measure the outcome and refresh the eval set.** adk-agent-evaluation, supporting adk-agent-observability. 5–8 h. Acceptance: report the share of signed-in chats ending in a completed change, salon phone-call volume against the baseline (O8), and add 10 eval cases from redacted production sessions.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Model migration off `gemini-3.5-flash` | Vertex retirement "2027-05-19 or later" (lifecycle table checked 2026-10-08), or a newer stable model wins on G06's set | None until the date; put a reminder for 2027-03 in the team calendar | adk-release-engineering |
| Phone or OTP sign-in for customers without website accounts | O1 shows many customers lack accounts | Those customers phone the salon | adk-tool-auth-and-secrets |
| Chat embedded on every site page; SMS or WhatsApp channel | Pilot usage shows demand, or low discovery of the link | Lower reach | adk-frontend-integration |
| Deposits or prepayment | The business introduces deposits | None now; money is out of scope | safe-api-tool-calls |
| Model Armor or SDP screening | Free-text fields reach the model, or a privacy review asks | Tool results are already minimised to non-sensitive fields | protect-adk-sensitive-data |
| "My usual stylist" preference | Repeat customers ask | None; booking history already answers it | adk-memory-architecture |
| Languages other than English | A salon serves customers in another language | English-only replies | adk-agent-instructions |
| Streaming replies | p90 complete-turn latency over 6 s measured in G11 or G12 | Slower perceived reply | adk-frontend-integration |
| Shared token budget across customers | Spend approaches the allowance in G16 data | The per-customer allowance and budget alert only | adk-operational-guardrails |
| Performance and cost tuning | Cost per completed change above target, or latency complaints | Higher spend within the budget alert | optimise-adk-on-google-cloud |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Method, decisions, invariants and assumptions |
| `eval/results/latest.md` (created by G10) | Latest result per evaluation case |
| This plan | Status, remaining limits and deferred controls |

## Open decisions for further planning

The full list is in the design's [Open decisions](../architecture/salon-booking-assistant.md#open-decisions). These block goals:

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| O1 Does the website have customer sign-in that the server can verify? | Assumed yes (A6). The alternative is phone OTP, about 8–12 h more | The team confirms | G04 scope, and through it G05 and G09 |
| O2–O5 Booking API idempotency, reschedule, lookup, policy errors | Unknown. D3 names a workaround for each | G01 | Details of G03 |
| O6 Launch quality bar | Assumed at least 27 of 30, and 0 forbidden writes | Salon owner and team agree | G10, G11 |
| Cut line | Phase 1 goes live at one pilot salon; all five follow in G12 | User confirms or moves it | G11, G12 |

## Resume here

- **Next goal:** G01, Booking API contract and fake. It has no blockers and most goals depend on it. G04 (Dev C), G06 and G07 (Dev B) are also ready on day 1.
- **Read first:** the design, this plan, and the booking API's source or docs.
- **Next action:** answer G01's five API questions from the booking API code.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls.
Work within local code and booking-API staging with test customers only, verify
the contract tests against the fake and one recorded staging run, and update
the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next ready one:
`/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
