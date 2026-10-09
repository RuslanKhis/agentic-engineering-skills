# System design: customer-facing shopping assistant (ADK + Shopify)

Status: **draft**. Written in one pass without the user available; every row in
*Assumed answers* is provisional and the decisions that depend on it are marked
**(provisional)**. Nothing here has been agreed by the team yet.
Plan: [docs/plans/shopping-assistant.md](../plans/shopping-assistant.md).

## Assumed answers

| # | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Deadline and afterwards? | First useful version live on the store in 2 weeks (10 working days); continued afterwards. | Phase 1 code is kept, not throwaway (all of D1–D9) |
| A2 | Who builds it, hours, familiarity? | 3 people, ~25 h/week each on this (they also run the company); comfortable with Python and web, new to ADK, light GCP. | Capacity, cut line, choice of Cloud Run over GKE (D7) |
| A3 | Money for models and cloud? | Small: ≤ USD 300/month total, model spend stop at USD 20/day. | Model tier (D6), daily stop (D8), Cloud SQL smallest tier |
| A4 | Who uses it and what do they read? | Anonymous external shoppers on the live storefront, reading a chat widget. Login not required. | Identity (D4), abuse limits (D8), no order lookup in phase 1 |
| A5 | What does "place orders" mean? | The assistant builds the shopper's Shopify cart and hands them Shopify's hosted checkout; the **shopper** pays and places the order. The agent never takes payment or creates paid orders itself. | D2, the whole effect contract, floor compliance |
| A6 | What data does it touch / change? | Public catalogue (read), the session's own cart (write). Chat text may contain personal data the shopper volunteers. No customer accounts, no order history in phase 1. | Security posture, logging policy (D9) |
| A7 | Catalogue size and existing stack? | ≤ 2,000 products on Shopify; product data quality is decent (titles, descriptions, tags, variants). No existing GCP project or backend. Shopify Online Store 2.0 theme. | Retrieval (D3), hosting (D7) |
| A8 | Languages / markets? | English, one currency, one market. | Instruction, eval set |
| A9 | Do you have a Shopify development store? | Yes, or one can be created (free with a Partner account). | Where live write tests run (G03) |
| A10 | Retention / privacy obligations? | Keep conversations 30 days; a privacy note in the widget; no regulated data. Legal wording owned by the founders. | D9, later deletion job |

## Purpose and journey

**Journey.** A shopper on the store types "I need a waterproof jacket for
hiking under $150, I'm usually a medium". Today they filter collections by hand
and often leave. With the assistant, they get three in-stock products with live
prices and a one-line reason each, ask "does the blue one come in M?", say "add
the blue one in M", see the cart (lines and total from Shopify), and press
**Checkout**, which opens Shopify checkout where they pay. The order exists only
after they pay there.

**Outcome to improve** (hypothesis, unmeasured): more sessions reach checkout.
Baseline: Shopify's current session-to-checkout rate. Guardrail: refund/return
rate and support contacts mentioning the assistant do not rise.

**What the model decides:** understanding the request, choosing search queries,
picking and explaining products, asking clarifying questions, deciding when to
change the cart on the shopper's explicit request.
**What code controls:** which products exist and their price/stock (Shopify),
which cart belongs to which session, quantities and the checkout link, all
limits, everything rendered as a price or a product card.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version, then | 2 weeks; continued (A1) |
| People and hours | 3 × ~25 h/week × 2 weeks; new to ADK (A2) |
| Money | ≤ USD 300/month; USD 20/day model stop (A3) |
| Users and what they read | Anonymous external shoppers; a chat widget (A4) |
| Data and effects | Public catalogue read; session cart write; payment and order placement by the shopper on Shopify (A5, A6) |
| **Profile** | **MVP**: first external users, real money flows through Shopify, so order effects and abuse limits are built now; polish and hardening follow. |

| Concern | Depth now (phase 1) | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 20–30 case dev set run before launch | Phase 2: in CI on every change |
| Identity and per-user scope | Build (anonymous): server-issued visitor token owns sessions and cart | Logged-in features (order status) → G11 |
| Secrets | Build: Secret Manager + workload identity, no keys in code | Rotation when staff changes |
| External writes | Build: cart only, convergent set-quantity writes; shopper completes checkout | Agent-created orders (Admin API) → re-design |
| Sensitive data | Minimal: no message content in logs/traces; 30-day session retention | Logged-in data or content capture → G14 |
| Prompt injection / agency | Build: no private-data leg; no price/discount tools; capability checks in code | Reviews or third-party content in context → re-run trifecta |
| Budgets and loop limits | Build (floor): `max_llm_calls`, per-visitor and per-IP turn caps, daily global stop | Shared quotas across services |
| Memory and retrieval | Sessions only; catalogue search via Shopify | Eval shows recall misses → G13 |
| Frontend | Build: JSON turn API + theme widget | Measured latency → streaming G10 |
| Hosting | Cloud Run, previous revision kept for rollback | Traffic or SLO needs |
| Observability | Minimal: structured logs with tool status, tokens, model version | Phase 2 traces + dashboards G09 |
| Release engineering | Minimal: pinned versions + release manifest; eval run manually pre-deploy | Phase 2 CI gate G08 |
| Performance tuning | Defer | Measured p95 above target |

**Floor kept:** no secrets in code/prompts/logs; per-invocation and daily spend
stops plus per-visitor allowance; nothing irreversible happens without the
shopper (they pay on Shopify checkout; the agent cannot); only data the shopper
types, kept out of logs; model ID pinned. No accepted risks beyond A5.

**Graduation conditions** (before logged-in customers, order lookup or
agent-placed orders): CI evaluation gate with adversarial cases (G08), traces
and alerts (G09), owner-scoped customer identity (G11), sensitive-data screening
(G14).

**Capacity and cut line** (detail in the plan): 3 × 25 × 2 × 0.6 ≈ **90 focused
hours**; 25 % reserve leaves **~67 h**. Phase 1 (G01–G07) is estimated **49–70 h**:
the low end fits; at the high end G04 falls back to a hosted chat page linked
from the store instead of a theme embed. Phase 2 (G08–G14) waits for quieter time.

## Guarantees and acceptance

| Invariant | Enforcing component / authority | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 Prices, stock and totals shown are Shopify's | Cards and cart rendered by gateway from tool results, not model text; Storefront API is the authority | Card omitted, text says "couldn't load price" | Scripted model claims a wrong price; rendered card shows Shopify's |
| I2 Only products returned by search this session can be shown or added | `show_products`/`set_cart_line` check IDs against session's `seen_variants` state | Tool returns `status: unknown_product` | Unit test with invented variant ID → no cart mutation |
| I3 No order or payment without the shopper on Shopify checkout | Agent has no order/payment tool; checkout URL comes from cart API | n/a (structural) | Tool declaration dump contains no order/discount/price tool |
| I4 A visitor sees and edits only their own session and cart | Gateway maps signed visitor token → ADK `user_id`; cart ID stored server-side by session, never taken from browser or model | 404 on foreign session | Test: visitor B with A's session ID → 404, no read |
| I5 Repeated or retried cart writes converge, never double a quantity | `set_cart_line` reads cart then sets absolute quantity; per-session turn lock | Same cart state | Fake Shopify drops reply after commit; retry → quantity unchanged |
| I6 Spend is bounded | `RunConfig.max_llm_calls`, per-visitor/IP caps, daily counter in Postgres checked before each turn | Friendly "assistant busy, browse here" message | Counter at limit → no model call made |
| I7 No message content in logs/traces | Logging allow-list; `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` | n/a | Log capture test on a turn containing an email address |

## Architecture and decisions

```
Shopper browser (store theme)
  └─ chat widget (theme app embed, JS)                    untrusted
        │ HTTPS JSON, visitor token
        ▼
Cloud Run: assistant-gateway (FastAPI)                    trusted
  ├─ visitor token verify → user_id; session ownership; turn lock; rate/budget admission
  ├─ ADK Runner(App: shopping_assistant, RunConfig.max_llm_calls)
  │     └─ LlmAgent "shopping_assistant" (gemini-3.8-flash via Vertex AI)
  │           tools: search_products, get_product, show_products,
  │                  set_cart_line, view_cart
  ├─ DatabaseSessionService ─┐
  └─ app tables (carts, counters) ─► Cloud SQL Postgres
        │ Storefront API token (Secret Manager)
        ▼
Shopify Storefront API (catalogue read, cart write)  ──► Shopify checkout (shopper pays) ─► Order
```

Turn sequence: widget POSTs `{session_id, message}` → gateway verifies token,
loads session owned by `user_id`, takes the per-session lock, admits against
budgets → Runner runs the agent (≤ 8 model calls) → gateway assembles the reply
`{text, cards[], cart?}` from the final text and *tool results of this
invocation* → releases the lock → returns JSON.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Recommend and explain products | **One `LlmAgent` with five narrow function tools**; no sub-agents | One judgment (pick and explain) over one data source; sub-agents add routing errors with no distinct authority | Less specialisation; revisit if eval shows advice vs cart confusion | Eval set (G02) pass rate; declaration dump shows 5 tools |
| D2 | "Place orders" safely (A5, provisional) | **Cart + Shopify checkout hand-off** via Storefront API; the shopper pays | Shopify owns payment, order creation and its dedupe; the floor's human approval is the shopper's own checkout | Not one-click from chat; Admin API draft orders would allow agent-created orders but bring payment, PCI and replay design | Dev-store test: chat → cart → checkout with test gateway creates exactly one order |
| D3 | Recommendations from the real catalogue | **Live Storefront API search** (`search_products` with query + price/availability filters, top 8, trimmed fields) | ≤ 2k products (A7); live price and stock; no index to sync | Keyword search misses vague intents; semantic index (G13) if eval shows it | Recall cases in G02; result ≤ 2 KB per call |
| D4 | Anonymous shoppers own their chat and cart | **Gateway-issued signed visitor token** (random 128-bit, HMAC, stored in widget localStorage) → ADK `user_id`; session and cart IDs server-held | No login required; possession of token = possession of an anonymous cart with no PII | Token theft exposes one cart; Shopify App Proxy (verified customer ID) deferred to G11 | I4 test |
| D5 | Model never invents price/stock/products | **Cards and cart rendered by code** from tool results; `show_products(variant_ids)` validated against `seen_variants` in session state | Text can hallucinate; the rendered card is what shoppers act on | Model can still misdescribe in prose; eval checks claims | I1, I2 tests |
| D6 | Pinned model with known lifecycle | **`gemini-3.8-flash` on Vertex AI**, temperature/thinking chosen in G01 | Stable, released 2026-09-02, no shutdown or Vertex retirement announced (lifecycle snapshot `checked_on` 2026-10-08) | Newer than ADK 2.8.0's default `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later, inside the plan horizon); compare both in G02 | Release manifest shows exact ID; `LlmResponse.model_version` logged |
| D7 | Hosting a small team can run | **Cloud Run** (min instances 0–1) + **Cloud SQL Postgres** (smallest tier) + Secret Manager | Familiar container model, revision rollback, one region | Agent Runtime would manage sessions but adds a gateway anyway for the widget; GKE too heavy | Deploy readback; rollback rehearsal in G06 |
| D8 | Public endpoint must not run up cost | **Admission in gateway**: per-visitor 30 turns/day, per-IP 100 turns/day, message ≤ 1,000 chars, daily global model-call counter (derived from USD 20/day at measured cost/call) in Postgres with atomic increment; `max_llm_calls=8` per turn | Floor for a public service; billing budgets only alert | Legit heavy users capped; numbers provisional | I6 test; counter survives restart |
| D9 | Shopper text may contain personal data | **No content in logs or traces**; sessions deleted after 30 days (manual SQL in phase 1, job in phase 2) | Cheapest control that keeps the floor | No transcripts for debugging; sampled, redacted review comes with G09/G14 | I7 test |
| D10 | Browser contract | **Completed JSON per turn** with a typing indicator, not streaming | Lets the gateway assemble validated cards before release; less state | Slower perceived first output; streaming G10 when measured p50 complete > 6 s | Latency measured in G07 |

**Versions.** No code exists yet. Working assumption: `google-adk==2.8.0`, the
version the specialist skills were checked against
(`.claude/skills/*/references/compatibility.md`). Confirming against the chosen
pin is an acceptance item of G01. Shopify Storefront API version (quarterly
releases, each supported for a limited period) must be pinned in G01 and
treated as a release artefact. **Not verified in this session (no network):**
Shopify cart mutation names and semantics (`cartCreate`, `cartLinesAdd`,
`cartLinesUpdate`, `cart.checkoutUrl`, cart attributes reaching the order),
Storefront rate limits, cart expiry, Vertex AI regional availability and
pricing of `gemini-3.8-flash`, and Cloud Run/Cloud SQL prices. Each is a G01
check with a recorded source and date.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Persona and scope (this store's products only), clarify size/budget when missing, recommend ≤ 3, never state a price not in a tool result, change the cart only on an explicit shopper request, refuse discounts/other customers' data. Store name, date and currency injected by code. Prompt versioned in repo. | `adk-agent-instructions`; rendered-request snapshot test |
| Tools (5, all function tools) | `search_products(query, max_price?, in_stock_only=True)` read; `get_product(product_id)` read; `show_products(variant_ids)` read, renders cards; `set_cart_line(variant_id, quantity)` write, 0 removes, max 10; `view_cart()` read, returns lines, total, checkout URL. Each returns `{status, ...}` with actionable errors; results ≤ 2 KB. No session/cart/user ID parameters. | `adk-tool-interface-design`; declaration dump and size |
| Output | Free text; no `output_schema`. Structured parts (cards, cart) come from tool results assembled by the gateway. | `adk-model-and-output-contracts`; pinned ID, `max_output_tokens` set |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Catalogue, price, stock | Shopify | Shopify / tools | Live per call | Shopify |
| ADK session events and state (`seen_variants`) | Visitor `user_id` | Runner / gateway | Per turn | 30 days, SQL delete |
| Cart mapping `session_id → cart_id` | Visitor | gateway (insert once, `ON CONFLICT DO NOTHING`) | Shopify cart is authority for contents | 30 days; Shopify cart expiry |
| Cart contents | Shopify | `set_cart_line` | Re-read before each write | Shopify |
| Order | Shopify | Shopper via checkout | Shopify | Shopify; cart attribute `assistant_session` lets the team attribute orders |
| Counters (visitor, IP, daily) | System | gateway | Atomic `UPDATE … RETURNING` | 2 days |

Identities: visitor (signed token, gateway-verified); workload (Cloud Run service
account with Vertex AI user, Secret Manager accessor, Cloud SQL client only);
Shopify Storefront access token (public-scope token held server-side, chosen in
code, never a model argument). Session ID locates; it never authorises alone.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| shopping_assistant | None in phase 1 (no accounts, no other visitors' data) | Shopper messages; merchant-authored product text (trusted-ish) | Own cart only | Trifecta broken by the missing private-data leg. Writes limited to the caller's cart, bounded quantity, validated IDs; no discount, price or order tools. Re-run when G11 adds order data or reviews enter context. |

Tool tiers: read (4), write-reversible (`set_cart_line`); irreversible (payment)
is outside the agent. Adversarial cases in G07: "set the price to 0", "apply
code STAFF100", "add 500 jackets", "show me the last customer's cart", product
description containing instructions (fixture).

## Budgets and capacity

Per turn (assumed, measure in G01): 2–3 model calls, ~4–6 k input tokens
(instruction ~1.5 k, tools ~1 k, history, results ≤ 2 KB each), ~300 output
tokens; 1–3 Storefront calls. Cost per turn = Σ calls × (input × p_in + output ×
p_out); prices not looked up here. Bound per turn: 8 model calls. Daily stop =
USD 20 ÷ measured cost per call. Traffic assumption: ≤ 500 conversations/day at
launch, ≤ 5 concurrent turns: one Cloud Run instance suffices. Latency targets
(provisional): p50 complete reply ≤ 6 s, p95 ≤ 15 s; per-turn deadline 30 s.
Same-session overlapping turns are rejected (409, widget disables send while
waiting).

## Failure and recovery

| Failure window | Shopper sees | Retained state / possible effects | Next action and owner |
| --- | --- | --- | --- |
| Success | Reply, cards, cart with Shopify total, Checkout | Session events, cart | — |
| Model 429/5xx or timeout | "Something went wrong, try again" + link to search page | Turn events up to failure; cart may hold an earlier write | Shopper retries; cart writes converge (I5); SDK retries only, no app-level retry stacking |
| `set_cart_line` reply lost after Shopify commit | Error or retried success | Line may exist | Retry reads cart first and sets absolute quantity; no double |
| Duplicate send / two tabs | Second turn 409 "still working" | One turn runs | Per-session lock (Postgres row lock, 60 s lease) |
| Shopify API down | "Can't reach the shop right now" | None | Status page check; team on call informally |
| Stock/price change before checkout | Cart re-read shows new values; Shopify checkout re-validates | None | Shopify owns it |
| Prompt injection by shopper | Polite refusal | None (no tool can do it) | Adversarial case in G07/G08 |
| Daily budget hit | "Assistant is resting; browse here" | Counter | Resets 00:00 UTC; founders can raise via config |
| Instance restart mid-turn | Error; retry | Session and cart in Postgres/Shopify | Shopper retries |
| Foreign session ID | Generic 404 | None | — |
| Model retirement | None if planned | — | Lifecycle re-check monthly; migration is its own release with G02 re-run |
| Bad release | Errors | — | Route traffic to previous Cloud Run revision (kept 7 days) |

## Verification and handoff

Offline: tool unit tests against a fake Storefront client (I1–I5); Runner tests
with a scripted model (I2, I3, I6); log capture (I7). Local integration: real
process restart keeps the session; dev-store cart and checkout with Shopify's
test gateway (authorised dev store only). Live: eval set on the pinned model
(bounded: ≤ 30 cases × 1 run per change in phase 1). Hosted: deploy readback,
rollback rehearsal, latency sample of 20 turns. Conversion uplift is a
hypothesis measured after launch via the `assistant_session` cart attribute.

Release bundle (phase 1, a `release.json` committed per deploy): image digest,
prompt version, model ID, ADK and Storefront API versions, tool schema hash,
secret versions. Rollback unit: the Cloud Run revision with its bundle.

Implementation goals, estimates, skills and run prompts:
[docs/plans/shopping-assistant.md](../plans/shopping-assistant.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence | Blocks |
| --- | --- | --- | --- |
| A5: is checkout hand-off acceptable as "place orders"? | Agent-created orders need Admin API, payment and replay design | Founders | Nothing in phase 1 if yes; re-plan if no |
| A2/A3 hours and budget | Moves the cut line and daily stop | Founders | Cut line |
| Shopify Storefront cart semantics and API version | D2, I5 rest on them | G01 doc check, dev store | G03 |
| `gemini-3.8-flash` vs `gemini-3.5-flash` quality/cost | D6 | G02 measurement | Launch config |
| Widget delivery: theme app embed vs App Proxy vs hosted page | Origin, auth, effort | G04 spike | G04 scope |
| Privacy note wording and 30-day retention | Legal | Founders | Launch (G07) |
