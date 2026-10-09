# Implementation plan: customer-facing shopping assistant

Status: draft, ready goals identified (D01, G01, G03), and all assumptions are provisional
Architecture: [docs/architecture/shopping-assistant.md](../architecture/shopping-assistant.md)
Continuation source of truth: this plan

## Destination and constraints

Phase 1 delivers a chat widget on the live Shopify store. It recommends
in-stock products, builds the customer's cart and hands them to Shopify
checkout, where they pay (design D3, assumption A4). Non-goals for phase 1
are listed in the design. Stack: Python, `google-adk==2.8.0` (working
assumption, confirmed in G01), FastAPI on Cloud Run, Cloud SQL PostgreSQL,
Vertex AI `gemini-3.8-flash`, and the Shopify Storefront API. Greenfield:
there is no application code in the repository yet, so every module path
below is **proposed**. Goals inherit the pinned model ID, ADK pin and prompt
version. A goal that changes one of them is a release, not a side effect.
Authorization so far is **design only**. Each goal states what it still needs.

## Delivery profile and capacity

Profile: **MVP**. See the design's delivery constraints.

Capacity (assumption A2): 3 people × 25 h/week × 2 weeks = 150 h × 0.6 focus
≈ **90 focused hours**. Keeping a 25 % reserve for setup surprises and launch
leaves **≈ 68 h** for goals. First-time setup (GCP project, IAM, Shopify app)
is inside the estimates below.

| Phase | Delivers | Goals | Estimate (focused h) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship (by 2026-10-23) | Customers on the live store get recommendations and a verified cart with a Checkout button; spend is bounded; the team sees errors and token use | D01, G01–G07 | **57–79** | ≈ 68 h of 90 after a 25 % reserve. The upper end eats the reserve; see the cut rule |
| 2, harden (when quieter) | Eval in CI, traces and SLIs, measured outcome, then the graduation conditions for logged-in customers | G08–G14 | ≈ 70–110 (coarse) | No date |

**Cut line:** phase 1 is D01 and G01–G07. **Cut rule at the day-6 checkpoint
(2026-10-16):** if G01–G04 are not done, G05 ships as a standalone chat page
linked from the store header instead of an embedded widget (saves about 5 h).
If that is still short, the launch moves. The floor is never cut: G04's limits
and G07's eval run always stay.
**Order of usefulness if time runs out:** G01 → G02 → G03 (a demoable local
agent that builds real carts on the dev store), then G04 → G06 (a hosted,
bounded API), then G05 → G07 (customer-facing).

Suggested split: person A takes D01 → G02 → G04; person B takes G01 → G06;
person C takes G03 (from day 1) → G05 → G07.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D2 | `app/agent.py` builds `LlmAgent` + `App`; `app/tools/catalog.py` | Vertex AI endpoint | `adk-workflow-design` | ADK 2.8.0 constructor names |
| D3, D4 | `app/tools/cart.py` over `app/shopify/storefront.py` adapter | — | `safe-api-tool-calls` | Storefront cart mutation semantics (D01) |
| D5, D7, D9 | `app/api/main.py` (FastAPI): `/session`, `/chat`, limit middleware; `Runner` with `DatabaseSessionService` | Cloud SQL | `adk-frontend-integration` | `DatabaseSessionService` URL/driver on 2.8.0 |
| D6, D10 | `app/config.py`: model ID, prompt version, limits | — | `adk-model-and-output-contracts` | Vertex price and lifecycle re-check |
| D8 | `Dockerfile`, Cloud Run service, Secret Manager | Cloud Run, Cloud SQL, Secret Manager, Billing budgets | `deploy-adk-on-google-cloud` | Region, quotas, pricing (dated) |
| Widget | `widget/` (JS) as theme app embed or snippet | — | `adk-frontend-integration` | O5 spike |

## Goals and dependencies

| ID and goal | Phase | Type | Estimate | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| D01 Verify Shopify Storefront contracts | 1 | discovery | 2–3 h | — | `safe-api-tool-calls` | ready |
| G01 Local agent recommends real products | 1 | impl | 8–11 h | — | `adk-workflow-design` | ready |
| G02 Agent builds a verified cart with a checkout link | 1 | impl | 8–11 h | D01, G01 | `safe-api-tool-calls` | blocked on D01, G01 |
| G03 Evaluation set and runner | 1 | impl | 6–9 h | G01 for running (cases can start on day 1) | `adk-agent-evaluation` | ready (case writing) |
| G04 Bounded, owner-checked chat API | 1 | impl | 10–13 h | G01 | `adk-frontend-integration` | blocked on G01 |
| G05 Storefront chat widget with cards | 1 | impl | 9–13 h | G04 contract | `adk-frontend-integration` | blocked on G04 contract |
| G06 Staging and production on Cloud Run | 1 | impl | 10–13 h | G04 | `deploy-adk-on-google-cloud` | blocked on G04 and a GCP project |
| G07 Launch check and soft launch | 1 | impl | 4–6 h | G02, G03, G05, G06 | `adk-agent-evaluation` | blocked |
| G08–G14 | 2 | see below | — | phase 1 | — | proposed |

### D01: Verify the Shopify Storefront contracts

- **Phase and estimate:** 1; 2–3 h.
- **Outcome and linked decisions:** settles open decision O2 for D1, D3 and D4.
- **Scope:** read the current Shopify Storefront API docs and exercise the dev store. Questions to answer: product search query syntax and price filter; cart create and line update with an **absolute quantity**; how to update an existing line by variant; `checkoutUrl`; cart expiry; rate or cost limits; token type and minimal scopes (read products, read/write carts); API version to pin. Stop when every answer is recorded with a URL and date, or marked unknown.
- **Depth:** discovery only; no production store access.
- **Implementation route:** a notes file `docs/architecture/shopify-contracts.md` (proposed) plus a scratch script against the **dev store** only.
- **Prerequisites:** a Shopify dev store and a custom app with a Storefront token.
- **Primary skill:** `safe-api-tool-calls`.
- **Supporting skills:** `adk-tool-auth-and-secrets` (token type and storage).
- **Acceptance:** each question has a sourced answer. D4 is confirmed, or replaced with the reconcile approach the docs support.
- **Verification:** links and a dated transcript of the dev-store calls, with no tokens in the file.
- **Execution scope:** needs network access and dev-store credentials, which this design session did not have.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out D01 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, record sourced answers and evidence here.`

### G01: Local agent recommends real products from the dev store

- **Phase and estimate:** 1; 8–11 h (includes first ADK setup).
- **Outcome and linked decisions:** running `adk web` locally, "waterproof jacket under €150" returns ≤ 3 in-stock picks with reasons (D1, D2, D6, D10).
- **Scope:** `LlmAgent` with the instruction; `search_products`, `get_product`; Storefront adapter; config with the pinned model and `max_llm_calls=8`. Excludes cart, API and UI.
- **Depth:** floor only: token from env or Secret Manager, pinned model, call cap.
- **Implementation route:** `app/agent.py`, `app/tools/catalog.py`, `app/shopify/storefront.py`, `app/config.py` (proposed); `App`/`Runner` per ADK 2.8.0.
- **Prerequisites:** dev store token; Vertex AI access in a GCP project (or a Gemini API key, used for local work only).
- **Primary skill:** `adk-workflow-design`.
- **Supporting skills:** `adk-tool-interface-design` (tool declarations, bounded results); `adk-agent-instructions` (instruction scope, no prices from memory); `adk-model-and-output-contracts` (model pin).
- **Acceptance:** `google-adk==2.8.0` installs and the named APIs exist (or the pin is changed and recorded); the declaration dump shows 2 tools with results ≤ 8 items; a no-match query returns an honest "nothing found"; the rendered request contains no secrets.
- **Verification:** pytest with a fake Storefront adapter (offline); one manual `adk web` session on the dev store (live, bounded).
- **Execution scope:** local only; dev store.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02: Agent builds a verified cart and offers checkout

- **Phase and estimate:** 1; 8–11 h.
- **Outcome and linked decisions:** "add the M in blue" produces a cart whose quantity is right under retry, and `get_cart` returns the checkout URL (D3, D4; I1, I4).
- **Scope:** `set_cart_line` (absolute quantity 0–10, variant validated) and `get_cart`; cart ID kept in session state by tool code; read-back after each write; one bounded retry that re-reads first. Excludes Admin API and discounts.
- **Depth:** MVP build for reversible writes; payment stays with Shopify.
- **Implementation route:** `app/tools/cart.py` with `ToolContext.state` for the cart ID (proposed).
- **Prerequisites:** D01, G01.
- **Primary skill:** `safe-api-tool-calls`.
- **Supporting skills:** `adk-tool-interface-design` (write-tool declaration and errors).
- **Acceptance:** with a fake adapter, a lost response after commit followed by a retry gives quantity 2, not 4; an unknown variant or quantity 11 makes zero Shopify calls; the cart ID never appears in a tool's parameters; read-back failure returns the "couldn't confirm" status.
- **Verification:** offline pytest; one live dev-store cart through to the checkout page (no payment).
- **Execution scope:** dev store only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03: Evaluation set and runner

- **Phase and estimate:** 1; 6–9 h.
- **Outcome and linked decisions:** a 30–40-case set measuring recommendation relevance and the I2/I6 behaviours.
- **Scope:** cases for clear needs, vague needs, no match, out of stock, add to cart, quantity change, off-topic, discount demand, injection ("ignore your rules"), price-in-prose and "is my order placed?". A script runs them against the pinned model and writes a results table. Expected products are chosen by a founder from the dev-store catalogue.
- **Depth:** MVP: a manual run before each release; CI comes in G08.
- **Implementation route:** `eval/cases.jsonl`, `eval/run.py` (proposed), with deterministic checks first and a judge only where needed (pin it if used).
- **Prerequisites:** writing cases needs nothing; running them needs G01 (G02 for the cart cases).
- **Primary skill:** `adk-agent-evaluation`.
- **Supporting skills:** `adk-agent-security` (adversarial cases with forbidden-action assertions).
- **Acceptance:** the runner reports pass, fail and missing results per case; every forbidden-action case asserts that no tool was called; the run records model ID, prompt version and cost.
- **Verification:** one recorded run on the dev store (≤ US$5).
- **Execution scope:** dev store, bounded spend.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04: Bounded, owner-checked chat API

- **Phase and estimate:** 1; 10–13 h.
- **Outcome and linked decisions:** `/session` and `/chat` serve the D9 response contract with ownership and limits (D5, D7, D9; I3, I5).
- **Scope:** FastAPI around `Runner` with `DatabaseSessionService` (local Postgres in docker for tests); HMAC-signed session token; message cap, turn cap, per-IP bucket, daily counter, kill switch; response builder that copies cards from tool results; one structured log line per turn with no content; CORS restricted to the store domains.
- **Depth:** MVP build for identity and budgets; no login.
- **Implementation route:** `app/api/main.py`, `app/api/limits.py`, `app/api/cards.py` (proposed).
- **Prerequisites:** G01 (G02 for cart cards).
- **Primary skill:** `adk-frontend-integration`.
- **Supporting skills:** `adk-operational-guardrails` (limits and daily stop); `adk-tool-auth-and-secrets` (signing key, Secret Manager); `adk-memory-architecture` (session backend and 30-day retention).
- **Acceptance:** a foreign token gets 404 with no Shopify or model call; at the daily limit, or with the kill switch on, there are zero model calls and the `limited` status is returned; prices in cards equal the tool results; a session survives an API restart; logs contain no message text.
- **Verification:** offline pytest with a fake model and adapter; local restart test against Postgres.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05: Storefront chat widget with product and cart cards

- **Phase and estimate:** 1; 9–13 h (start with a 1 h spike on O5).
- **Outcome and linked decisions:** Maya's journey works in the theme on the dev store (D9; I2).
- **Scope:** launcher, chat panel, typing indicator, product cards (image, title, price, link), cart card with a Checkout button that opens `checkoutUrl`, `limited` and `error` states, an AI-assistant disclosure line, and "prices confirmed at checkout".
- **Depth:** MVP; no streaming.
- **Implementation route:** `widget/` as a theme app embed or snippet, decided in the O5 spike.
- **Prerequisites:** G04 response contract (a stub server is enough to start).
- **Primary skill:** `adk-frontend-integration`.
- **Supporting skills:** none.
- **Acceptance:** the journey completes in a browser on the dev store up to Shopify checkout; a rendered price equals the API card; the error state shows when the API is down.
- **Verification:** a manual browser run with screenshots; a contract test against the stub.
- **Execution scope:** dev store theme only. The live theme is changed in G07.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06: Staging and production on Cloud Run

- **Phase and estimate:** 1; 10–13 h (includes first GCP setup).
- **Outcome and linked decisions:** a staging service on the dev store and a production service on the live store, with rollback (D8, D10).
- **Scope:** Dockerfile; Cloud Run service per environment with its own service account (Vertex user, Cloud SQL client, Secret accessor); Cloud SQL; Secret Manager; Cloud Billing budget alerts; dated Vertex and Cloud SQL prices to set the daily stop (O6); deploy notes recording image digest, prompt version, model ID and ADK pin; the previous revision kept.
- **Depth:** MVP; no canary, no CI gate.
- **Implementation route:** `deploy/` scripts or a README (proposed).
- **Prerequisites:** G04; a GCP project and billing (O3); explicit authorization to provision.
- **Primary skill:** `deploy-adk-on-google-cloud`.
- **Supporting skills:** `adk-agent-observability` (structured logs and token fields reach Cloud Logging, content off); `adk-release-engineering` (pin and rollback notes).
- **Acceptance:** staging answers the G01 query; a redeploy keeps the session; rolling back to the previous revision works; log entries carry session ID and token counts with no content; the budget alert exists.
- **Verification:** hosted checks on staging; production smoke test with the widget hidden.
- **Execution scope:** **needs cloud authorization**, which this session did not have.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

### G07: Launch check and soft launch

- **Phase and estimate:** 1; 4–6 h.
- **Outcome and linked decisions:** the founders decide go or no-go on evidence (O4, A10).
- **Scope:** run G03 on staging; a manual checkout on the dev store (test payment); p50 latency over ≥ 50 turns; disclosure and privacy text in place; enable the widget on the live theme; a one-page runbook (kill switch, rollback, who watches the logs).
- **Depth:** MVP.
- **Prerequisites:** G02, G03, G05, G06.
- **Primary skill:** `adk-agent-evaluation`.
- **Supporting skills:** `adk-operational-guardrails` (kill-switch drill).
- **Acceptance:** the eval pass rate is recorded and the founders accept it; zero forbidden-action failures; the kill switch is tested in production; rollback is rehearsed once.
- **Verification:** hosted; the results table is linked here.
- **Execution scope:** needs founder approval to change the live theme.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

### Phase 2 goals (coarse; refine after launch data)

| ID | Goal | Estimate | Primary skill | Supporting | Trigger or reason |
| --- | --- | --- | --- | --- | --- |
| G08 | Eval set in CI as an exit-code gate; release manifest (image, prompt, model, ADK pin, tool-schema hash); refresh cases from sampled sessions | 8–12 h | `adk-release-engineering` | `adk-agent-evaluation` | First week after launch |
| G09 | Traces (content off), SLIs (completed turns, tool error rate by tool, tokens per turn), dashboard, 30-day deletion job, outcome measurement against the conversion baseline | 10–14 h | `adk-agent-observability` | `protect-adk-sensitive-data` | First week after launch |
| G10 | Streaming replies (SSE) | 8–12 h | `adk-frontend-integration` | `optimise-adk-on-google-cloud` | p50 complete reply > 6 s |
| G11 | Semantic catalogue retrieval (embeddings index refreshed from the Shopify catalogue) | 12–20 h | `adk-memory-architecture` | `adk-tool-interface-design` | No-match or irrelevant rate > 15 % in G09 data |
| G12 | Signed-in customers and order-status lookup (separate tool set, per-customer authorization in code, trifecta re-check) | 20–30 h | `adk-tool-auth-and-secrets` | `adk-agent-security`, `protect-adk-sensitive-data` | Customers ask for order status in > 10 % of sessions |
| G13 | Abuse hardening (reCAPTCHA Enterprise or Cloud Armor) and per-visitor budgets | 6–10 h | `adk-operational-guardrails` | `deploy-adk-on-google-cloud` | Bot traffic or the daily stop reached by abuse |
| G14 | PII screening of input and logs (SDP or Model Armor) | 6–10 h | `protect-adk-sensitive-data` | — | PII found in sampled sessions, or G12 starts |

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| In-chat order creation (Admin API) with durable operation record | Founders reject the checkout handoff (O1) or conversion data shows drop-off at the handoff | The customer leaves the chat to pay | `safe-api-tool-calls` |
| Discount codes and promotions | Marketing request | No promotions in chat | `adk-tool-interface-design` |
| Multi-language | Non-English traffic > 20 % | English only | `adk-agent-instructions` |
| Personalised picks from purchase history | After G12 and consent design | Generic recommendations | `adk-memory-architecture` |
| Canary releases and joint rollback | > 1 release/week or an incident from a release | Rollback is manual | `adk-release-engineering` |
| Model migration | Vertex retirement notice for `gemini-3.8-flash` (re-check the lifecycle table monthly) | — | `adk-model-and-output-contracts` |
| Cost and latency tuning (context caching, smaller model) | Monthly spend > 70 % of budget | — | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/shopping-assistant.md | Method, assumptions and decisions |
| eval results table (from G03, proposed `eval/results/latest.md`) | Latest quality per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's [open decisions](../architecture/shopping-assistant.md#open-decisions).
O1 (checkout handoff) blocks G02's scope; O2 is answered by D01; O3 blocks G06
and the cut line; O4 blocks G07; O5 is settled inside G05.

## Resume here

- **Next goal:** G01, the local agent that recommends real products. It needs only a dev-store token and model access. D01 and G03 case writing can run in parallel on day 1.
- **Read first:** docs/architecture/shopping-assistant.md (Assumed answers, D1, D2, D6, D10).
- **Next action:** confirm the founders' answers to O1 and O3, then create the dev store app token and start G01.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 (local agent recommends real products) from docs/plans/shopping-assistant.md.
Read docs/architecture/shopping-assistant.md and preserve its accepted decisions.
Use adk-workflow-design with adk-tool-interface-design, adk-agent-instructions and adk-model-and-output-contracts.
Work locally against the Shopify dev store only, verify G01's acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

After that goal, `/adk-engineer Continue the next ready goal in docs/plans/shopping-assistant.md.`
