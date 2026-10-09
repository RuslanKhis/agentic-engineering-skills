# Implementation plan: customer-facing shopping assistant

Status: draft; ready goals identified (G01, G02 partially, G04 spike)
Architecture: [docs/architecture/shopping-assistant.md](../architecture/shopping-assistant.md)
Continuation source of truth: this plan

## Destination and constraints

Shoppers on the live Shopify store get in-stock product recommendations with
live prices, build a cart in chat, and complete payment on Shopify checkout
(decision D2, assumption A5). Non-goals for phase 1: logged-in customers, order
status, agent-created orders, discounts, reviews, multiple languages.

Accepted stack (proposed, not yet user-accepted): Python, `google-adk==2.8.0`
(working assumption, confirm in G01), FastAPI gateway, Cloud Run, Cloud SQL
Postgres, Secret Manager, Vertex AI `gemini-3.8-flash` (D6), Shopify Storefront
API (version pinned in G01). Repository is empty apart from this design: every
module below is **proposed**. Authorisation so far: design only. Each goal's
execution scope says what it still needs.

Proposed layout:

```
shopping_assistant/agent.py        # LlmAgent factory, instruction loader
shopping_assistant/prompts/v1.md   # versioned instruction
shopping_assistant/tools/catalog.py, cart.py
shopping_assistant/shopify/client.py  # Storefront GraphQL client (fakeable)
gateway/app.py                     # FastAPI: token, ownership, lock, admission, Runner
gateway/budget.py, gateway/render.py
widget/                            # theme app embed JS/CSS
evals/dev.evalset.json, evals/adversarial.evalset.json
release.json, Dockerfile, tests/
```

## Delivery profile and capacity

Profile: **MVP** (see design, *Delivery constraints*).

| Phase | Delivers | Goals | Estimate (focused h) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Shoppers on the live store get recommendations, a cart and checkout, safely bounded | G01–G07 | 49–70 | 3 × 25 h × 2 wk × 0.6 ≈ 90 h; 25 % reserve → 67 h |
| 2, harden | CI eval gate, traces/alerts, streaming, logged-in features | G08–G14 | 45–75 | When the team has time |

Fit: the low end (49 h) fits; the high end (70 h) eats ~3 h of reserve. If work
runs high, **G04 falls back to a hosted chat page linked from the store** (saves
~4 h) and the dev eval set stays at 20 cases. Nothing on the floor (G05, the
checks in G03) is cut. **Cut line to confirm: G01–G07 now; G08 onwards later.**

Calendar, not just hours: three parallel streams after G01 day 1–2.
- Stream A (agent): G01 → G03.
- Stream B (quality): G02 → G07.
- Stream C (platform): G04 → G05 → G06 (G04 can start against a stub agent).
If one person must finish alone, the useful order is G01, G03, G05, G04 (hosted
page), G06, G02, G07.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1, D5 | `LlmAgent` in `shopping_assistant/agent.py`, 5 function tools, `seen_variants` in session state | Vertex AI | `adk-tool-interface-design` | ADK 2.8.0 tool/state APIs |
| D2, I5 | `tools/cart.py` read-then-set over Storefront cart; `carts` table | Cloud SQL | `safe-api-tool-calls` | Shopify cart mutations, attribute propagation |
| D3 | `tools/catalog.py` Storefront search, bounded result | — | `adk-tool-interface-design` | Search filter syntax |
| D4, D8 | `gateway/app.py` token, ownership, lock; `gateway/budget.py` | Cloud SQL | `adk-frontend-integration` / `adk-operational-guardrails` | `DatabaseSessionService` on Postgres with 2.8.0 |
| D6 | model ID + settings in `agent.py`, `release.json` | Vertex AI | `adk-model-and-output-contracts` | Region availability, price |
| D7, D9 | Dockerfile, Cloud Run service, env `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` | Cloud Run, Secret Manager | `deploy-adk-on-google-cloud` | IAM grants |

## Goals and dependencies

| ID and goal | Phase | Type | Estimate | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Local agent recommends real catalogue products | 1 | impl + discovery | 8–10 h | — | adk-tool-interface-design | ready |
| G02 Development eval set and baseline | 1 | impl | 5–8 h | G01 (cases can start now) | adk-agent-evaluation | ready (case writing) |
| G03 Cart and checkout hand-off | 1 | impl | 10–14 h | G01 | safe-api-tool-calls | blocked on G01 Shopify check |
| G04 Gateway API and storefront widget | 1 | impl | 12–16 h | G01 interface | adk-frontend-integration | ready (stub agent) |
| G05 Spend and abuse admission | 1 | impl | 3–5 h | G04 | adk-operational-guardrails | proposed |
| G06 Deploy to Cloud Run with rollback | 1 | impl | 8–12 h | G04, G05 | deploy-adk-on-google-cloud | proposed; needs GCP project |
| G07 Pre-launch evaluation, adversarial pass, soft launch | 1 | impl | 3–5 h | G02, G03, G06 | adk-agent-evaluation | proposed |
| G08 Evaluation gate in CI | 2 | impl | 6–10 h | G07 | adk-release-engineering | proposed |
| G09 Traces, token cost and alerts | 2 | impl | 6–10 h | G06 | adk-agent-observability | proposed |
| G10 Streaming replies | 2 | impl | 6–10 h | measured latency | adk-frontend-integration | proposed |
| G11 Logged-in customers and order status | 2 | discovery + impl | 10–16 h | G08, decision | adk-tool-auth-and-secrets | proposed |
| G12 Conversion attribution report | 2 | impl | 3–5 h | G07 + 2 wk traffic | adk-agent-observability | proposed |
| G13 Semantic catalogue retrieval | 2 | impl | 8–14 h | G02 shows recall misses | adk-memory-architecture | proposed |
| G14 Sensitive-data screening and retention job | 2 | impl | 6–10 h | G11 or content capture | protect-adk-sensitive-data | proposed |

### G01 — Local agent recommends real catalogue products

- **Phase and estimate:** 1; 8–10 h (includes ~2 h first-time ADK and Shopify app setup).
- **Outcome and linked decisions:** a developer runs the agent locally (`adk web` or a test Runner) and gets ≤ 3 in-stock recommendations with live prices from the real catalogue. D1, D3, D5, D6.
- **Scope:** `search_products`, `get_product`, `show_products` (validates IDs against `seen_variants`), instruction v1, pinned model, `max_llm_calls=8`. Excludes cart, gateway, deploy.
- **Depth:** read-only; floor kept (token from env/Secret Manager, pinned model, call cap). No eval harness yet.
- **Implementation route:** `shopping_assistant/agent.py` factory → `LlmAgent(model="gemini-3.8-flash", tools=[...])`; `shopify/client.py` GraphQL client behind an interface so tests use a fake. Discovery inside the goal: confirm ADK pin and APIs against 2.8.0; record Storefront API version, search filter syntax, cart mutation names and semantics, rate limits, cart expiry, with source URL and date; confirm `gemini-3.8-flash` availability in the chosen Vertex region and its price.
- **Prerequisites:** Shopify custom app with a Storefront access token (read products, write carts); a Google Cloud project with Vertex AI enabled, or a Gemini API key for local work.
- **Primary skill:** adk-tool-interface-design
- **Supporting skills:** adk-agent-instructions (instruction v1 and rendered-request test); adk-model-and-output-contracts (model pin, `max_output_tokens`, thinking setting); adk-tool-auth-and-secrets (Storefront token handling).
- **Acceptance:** 5 sample requests return in-stock products with Shopify prices; invented variant ID to `show_products` returns `unknown_product`; declaration dump shows 5 or fewer tools and each result ≤ 2 KB; ADK version and Shopify facts recorded with sources.
- **Verification:** offline pytest with the fake client; one bounded live run (≤ 20 model calls) against the real catalogue, read-only.
- **Execution scope:** local only; reading the live catalogue is read-only and allowed once the token exists.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Development eval set and baseline

- **Phase and estimate:** 1; 5–8 h.
- **Outcome and linked decisions:** a 20–30 case set with a measured pass rate for the pinned model and a side-by-side with `gemini-3.5-flash`. D1, D3, D6.
- **Scope:** cases for budget, size, category, out-of-stock, vague intent, follow-ups, "no suitable product" (honest no), off-topic; expected product sets or constraint checks; 5 safety cases seeded for G07.
- **Depth:** run manually before each deploy; CI gate is G08.
- **Implementation route:** `evals/dev.evalset.json` with deterministic checks (recommended IDs satisfy constraints; no price in text that differs from tool result) plus a pinned judge only if needed.
- **Prerequisites:** G01 agent for running; case writing can start immediately from the catalogue.
- **Primary skill:** adk-agent-evaluation
- **Supporting skills:** adk-model-and-output-contracts (model comparison); adk-agent-instructions (fixes from error analysis).
- **Acceptance:** results file per case for both models; error analysis notes; launch threshold agreed (proposed ≥ 80 % pass, 0 price mismatches).
- **Verification:** live model runs, ≤ 30 cases × 2 models × 1 run.
- **Execution scope:** model spend within the daily stop.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Cart and checkout hand-off

- **Phase and estimate:** 1; 10–14 h.
- **Outcome and linked decisions:** shopper says "add the blue one in M"; the cart shows Shopify lines and total and a Checkout link; paying on a dev store creates exactly one order. D2, D5, I3, I5.
- **Scope:** `set_cart_line(variant_id, quantity)` (0 removes, max 10, ID must be in `seen_variants`), `view_cart()`; cart created once per session (`carts` table insert-once) with cart attribute `assistant_session`; no discount, price or order tools.
- **Depth:** idempotent convergent writes (MVP depth for orders); payment and order creation remain Shopify's.
- **Implementation route:** `tools/cart.py` reads the cart then adds or updates to the absolute quantity; cart ID resolved in code from the session, never a tool argument.
- **Prerequisites:** G01 Shopify cart facts; a Shopify development store with a test payment gateway.
- **Primary skill:** safe-api-tool-calls
- **Supporting skills:** adk-tool-interface-design (cart tool declarations and errors); adk-agent-security (capability checks, no-discount structure).
- **Acceptance:** fake client drops the reply after commit, retry leaves quantity unchanged; two identical calls → one line of quantity N; unknown variant → no mutation; quantity 500 → refused; dev-store checkout creates one order carrying `assistant_session`.
- **Verification:** offline fakes; one authorised live run on the dev store only.
- **Execution scope:** dev store writes authorised by this plan once the store exists; **no writes to the live store's carts in tests**.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Gateway API and storefront widget

- **Phase and estimate:** 1; 12–16 h (fallback hosted page: 8–12 h).
- **Outcome and linked decisions:** a shopper on the store opens the widget, chats, sees cards and cart rendered from tool results, presses Checkout. D4, D5, D10, I1, I4.
- **Scope:** `POST /v1/visitor` (issue signed token), `POST /v1/sessions`, `POST /v1/sessions/{id}/turns` → `{text, cards[], cart?}`; ownership check; per-session lock (409 on overlap); CORS allow-list for the store domain; `DatabaseSessionService` on Postgres; widget as a theme app embed (spike first: 1 h to choose embed vs hosted page).
- **Depth:** completed JSON, no streaming.
- **Implementation route:** FastAPI app owning the `Runner`; `gateway/render.py` builds cards from this invocation's `show_products`/`view_cart` function responses only.
- **Prerequisites:** G01 agent factory (stub acceptable to start); Postgres locally (Docker).
- **Primary skill:** adk-frontend-integration
- **Supporting skills:** adk-memory-architecture (session service and restart behaviour); adk-tool-auth-and-secrets (visitor token signing key in Secret Manager).
- **Acceptance:** visitor B with A's session ID → 404 and no read; restart keeps the conversation; overlapping turn → 409; a card's price equals the fake Shopify price even when the scripted model text states another.
- **Verification:** offline API tests with scripted model; local integration with real process restart.
- **Execution scope:** local; theme changes on a duplicate (unpublished) theme only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Spend and abuse admission

- **Phase and estimate:** 1; 3–5 h.
- **Outcome and linked decisions:** no shopper or script can push model spend past the daily stop. D8, I6.
- **Scope:** per-visitor 30 turns/day, per-IP 100/day, message ≤ 1,000 chars, global daily model-call counter with atomic increment checked before each turn; operator kill switch (env flag) that turns the widget into a "browse here" link.
- **Depth:** floor for a public service; shared reservations across services deferred.
- **Implementation route:** `gateway/budget.py` with `UPDATE … RETURNING` counters; `RunConfig(max_llm_calls=8)`.
- **Prerequisites:** G04.
- **Primary skill:** adk-operational-guardrails
- **Supporting skills:** none.
- **Acceptance:** counter at limit → friendly message and zero model calls; counters survive restart; kill switch takes effect without redeploy (env change creates a new revision; verify timing).
- **Verification:** offline tests with a fake model counting calls.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Deploy to Cloud Run with rollback

- **Phase and estimate:** 1; 8–12 h (includes first GCP IAM/Cloud SQL setup).
- **Outcome and linked decisions:** the gateway serves from Cloud Run with Cloud SQL, Secret Manager and Vertex AI via its service account; a previous revision can take traffic in one command. D6, D7, D9, I7.
- **Scope:** Dockerfile, dedicated service account (Vertex AI user, Secret Manager accessor, Cloud SQL client), `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`, structured logs (turn ID, tool names/status, token counts, `model_version`; no message text), `release.json`, Cloud Billing budget alert (alert only), rollback rehearsal.
- **Depth:** minimal observability and release (MVP phase 1); traces and CI gate are G08/G09.
- **Implementation route:** Cloud Run service in one region chosen in G01; min instances 0 (or 1 if cold start is measured > 5 s).
- **Prerequisites:** G04, G05; a GCP project with billing; explicit authorisation to provision.
- **Primary skill:** deploy-adk-on-google-cloud
- **Supporting skills:** adk-agent-observability (log fields, content capture off); adk-release-engineering (`release.json` manifest); adk-tool-auth-and-secrets (workload identity, secrets).
- **Acceptance:** deploy readback shows image digest and env matching `release.json`; a turn with an email address leaves no message text in logs; traffic moved to the previous revision and back.
- **Verification:** hosted checks on staging URL.
- **Execution scope:** **needs the user's authorisation** for the GCP project, region and spend.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — Pre-launch evaluation, adversarial pass, soft launch

- **Phase and estimate:** 1; 3–5 h.
- **Outcome and linked decisions:** the deployed assistant meets the G02 threshold and refuses the adversarial cases; it is enabled on the live store. I1–I7.
- **Scope:** run dev set against staging; adversarial set ("price 0", "apply STAFF100", "add 500", "another customer's cart", instruction-bearing description fixture) asserting no forbidden tool call or mutation; 20-turn latency sample; enable theme embed; privacy note.
- **Depth:** manual gate; recorded results.
- **Prerequisites:** G02, G03, G06; privacy wording from founders.
- **Primary skill:** adk-agent-evaluation
- **Supporting skills:** adk-agent-security (adversarial assertions).
- **Acceptance:** threshold met; zero forbidden calls; p50/p95 recorded; rollback ready.
- **Verification:** live, bounded (≤ 60 cases × 1 run).
- **Execution scope:** enabling on the live store needs founder sign-off.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; revisit after launch data)

- **G08 Evaluation gate in CI** — 6–10 h. Primary `adk-release-engineering`; supporting `adk-agent-evaluation`, `adk-agent-security`. Acceptance: a PR that breaks a dev or adversarial case fails CI by exit code; `release.json` includes eval-set hash. Run: `/adk-engineer Carry out G08 from docs/plans/shopping-assistant.md.`
- **G09 Traces, token cost and alerts** — 6–10 h. Primary `adk-agent-observability`. Acceptance: one span per agent, tool and model call with session ID; tokens per completed conversation on a dashboard; alert on tool error rate and daily spend at 80 %. Run: `/adk-engineer Carry out G09 from docs/plans/shopping-assistant.md.`
- **G10 Streaming replies** — 6–10 h. Trigger: measured p50 complete > 6 s. Primary `adk-frontend-integration`. Acceptance: first text within 2 s on staging; cards still only from validated tool results. Run: `/adk-engineer Carry out G10 from docs/plans/shopping-assistant.md.`
- **G11 Logged-in customers and order status** — 10–16 h. Discovery first: Shopify App Proxy or customer account API for a verified customer ID. Primary `adk-tool-auth-and-secrets`; supporting `adk-agent-security` (trifecta re-check: private data now present), `adk-tool-interface-design`. Acceptance: customer A cannot obtain B's order by any phrasing; tests assert the lookup is keyed on the verified ID only. Run: `/adk-engineer Carry out G11 from docs/plans/shopping-assistant.md.`
- **G12 Conversion attribution report** — 3–5 h. Primary `adk-agent-observability`. Acceptance: weekly count of orders with `assistant_session` vs assistant sessions, compared with the pre-launch baseline. Run: `/adk-engineer Carry out G12 from docs/plans/shopping-assistant.md.`
- **G13 Semantic catalogue retrieval** — 8–14 h. Trigger: G02/G08 recall failures on vague intents. Primary `adk-memory-architecture`. Acceptance: recall cases improve on the frozen dev set with no regression in price accuracy. Run: `/adk-engineer Carry out G13 from docs/plans/shopping-assistant.md.`
- **G14 Sensitive-data screening and retention job** — 6–10 h. Trigger: G11 or any content capture. Primary `protect-adk-sensitive-data`. Acceptance: scheduled deletion removes sessions older than 30 days; screened transcripts contain no emails/phones. Run: `/adk-engineer Carry out G14 from docs/plans/shopping-assistant.md.`

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Agent-created orders (Admin API draft orders) | Founders decide checkout hand-off is not enough | None (not built) | safe-api-tool-calls |
| Customer reviews in answers | Merchandising request | — (untrusted content not yet in context) | adk-agent-security |
| Cross-session preferences (Memory Bank) | Repeat visitors ask for it | — | adk-memory-architecture |
| Canary releases | Traffic large enough for comparable samples | Bad release seen by all users until rollback | adk-release-engineering |
| Model failover | Model outage observed | Assistant offline during provider outage | adk-model-and-output-contracts |
| Multi-language / markets | New market | — | adk-agent-instructions |
| Cost and latency tuning | Measured cost/turn or p95 above target | Higher spend | optimise-adk-on-google-cloud |
| Model migration | Lifecycle re-check shows a retirement date for the pinned model | — | adk-release-engineering |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/shopping-assistant.md | Method, decisions, assumptions |
| evals/RESULTS.md (created in G02) | Latest result per case |
| this plan | Remaining limits and deferred controls |

## Open decisions for further planning

| Decision | Known facts and alternatives | Needed | Blocks |
| --- | --- | --- | --- |
| "Place orders" = checkout hand-off (A5) | Alternative: Admin API draft orders + invoice | Founder decision | Nothing in phase 1 if accepted |
| Hours and budget (A2, A3) | Assumed 25 h/week each, USD 20/day | Founder decision | Cut line |
| Shopify cart semantics, API version | Unverified here | G01 | G03 |
| Widget delivery route | Theme app embed / App Proxy / hosted page | G04 spike | G04 scope |
| Privacy wording, retention | 30 days assumed | Founders | G07 |

## Resume here

- **Next goal:** G01 — Local agent recommends real catalogue products. Ready: no dependencies; only needs a Storefront token and a model credential.
- **Read first:** docs/architecture/shopping-assistant.md (Assumed answers, D1–D6), this plan.
- **Next action:** create the Shopify custom app token, confirm `google-adk==2.8.0` APIs and Storefront cart/search facts, then build the three read tools against a fake client.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 (Local agent recommends real catalogue products) from docs/plans/shopping-assistant.md.
Read docs/architecture/shopping-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions, adk-model-and-output-contracts and adk-tool-auth-and-secrets.
Work locally with read-only catalogue access, verify the G01 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/shopping-assistant.md.`
