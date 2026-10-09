# Implementation plan: customer-facing shopping assistant

Status: draft — ready goals identified (G01 ready; D-01 runs alongside)
Architecture: [../architecture/shopping-assistant.md](../architecture/shopping-assistant.md)
Continuation source of truth: this plan

## Destination and constraints

**MVP (2 weeks):** an anonymous shopper on the Shopify storefront chats with an
assistant that recommends in-stock products from the live catalogue, adds the
chosen variant to a Shopify cart and opens Shopify's hosted checkout, where the
order is placed. Running on Cloud Run with spend caps, a kill switch and a
measured development-set score.

**After the MVP (when quieter):** regression gate in CI, better retrieval if
measured, signed-in order status, reviews behind a security split, streaming,
sensitive-data screening, and only then any in-chat order creation.

**Non-goals:** taking payment, Admin-API order creation in the MVP, discounts,
refunds, multilingual.

**Authorization:** design only so far. Local implementation of a goal is
authorized when the user runs that goal's prompt. Cloud provisioning, Shopify
app/token creation, deployment and paid live runs need the founders' explicit
go-ahead for the named target (G04 and live parts of G01/D-01).

**Inherited pins (provisional):** google-adk 2.8.0 working assumption (confirm in
G01); model `gemini-3.8-flash` on Vertex AI; judge `gemini-3.5-flash`; prompt
version `v1` in `app/prompts/`. Changing any of these later is a release.

**Inspected:** greenfield; only `.claude/skills/` exists. Everything below
under `app/` is a **proposed** layout.

Proposed layout:

```text
app/
  agent.py            # LlmAgent "shopper", App, RunConfig
  prompts/shopper_v1.md
  tools/catalogue.py  # search_products, get_product
  tools/cart.py       # update_cart, view_cart
  shopify/storefront.py  # GraphQL client, timeouts, one retry
  api/main.py         # FastAPI: /chat, /history, cookie session, caps
  api/assemble.py     # reply → cards + checkout button (I1, I2)
  limits.py           # rate limit, turn cap, daily counter, kill switch
widget/               # theme app embed / script-tag chat widget
evals/dev_set.jsonl   # ~40 labelled shopper requests
evals/run_dev_set.py
tests/                # offline: tools with fixtures, scripted-model Runner, API
release/manifest.json
```

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 one agent | `LlmAgent` in `app/agent.py`, invoked by `Runner` from `api/main.py` | Vertex AI model endpoint | `adk-workflow-design` | ADK 2.8.0 `App`/`Runner` names |
| D2 catalogue tools | `tools/catalogue.py` over `shopify/storefront.py` | — | `adk-tool-interface-design` | Storefront search filters (D-01) |
| D3 cart + checkout | `tools/cart.py`; `cart_id` in session state | — | `safe-api-tool-calls` | Cart mutations, `checkoutUrl`, expiry (D-01) |
| D4 structured reply, I1/I2 | `output_schema` on the agent; `api/assemble.py` | — | `adk-model-and-output-contracts` | Schema-with-tools on pinned ADK + model |
| D5 sessions | `DatabaseSessionService` (local Postgres, then Cloud SQL); signed HttpOnly cookie | Cloud SQL for PostgreSQL | `adk-memory-architecture` | Session-service constructor on pin |
| D6 hosting | Container with `api/main.py` entrypoint | Cloud Run, Secret Manager, service account | `deploy-adk-on-google-cloud` | Region, pricing (D-01) |
| D7 model pin | `release/manifest.json`, `agent.py` | Vertex AI | `adk-model-and-output-contracts` | Region availability |
| D8 caps | `RunConfig.max_llm_calls`; `limits.py` middleware | Cloud Billing budget alert (observation) | `adk-operational-guardrails` | — |
| D9 eval | `evals/` + pinned judge | Vertex AI (paid, bounded) | `adk-agent-evaluation` | Founder labels |
| D10 widget | `widget/` calling `/chat` with CORS for store domain | — | `adk-frontend-integration` | Theme app embed vs script tag on the store's theme |

## Goals and dependencies

| ID and goal | Type | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- |
| D-01 Verify Shopify Storefront + GCP facts | discovery | — | `safe-api-tool-calls` | ready (needs store access and network; runs in parallel with G01's offline part) |
| G01 Assistant recommends real products, measured | implementation | — (live run uses D-01's token) | `adk-tool-interface-design` | **ready** |
| G02 Add to cart and hand off to Shopify checkout | implementation | G01, D-01 | `safe-api-tool-calls` | proposed (blocked on D-01 cart facts for the live part) |
| G03 Chat widget and session-owning API | implementation | G01 | `adk-frontend-integration` | proposed (can start day 3 in parallel with G02) |
| G04 Launch on Cloud Run with caps, telemetry and release manifest | implementation | G02, G03 | `deploy-adk-on-google-cloud` | proposed (needs GCP project, region, spend allowance) |
| G05 CI regression gate + production sample → eval cases | implementation | G04 | `adk-release-engineering` | post-MVP |
| G06 Model migration drill | implementation | G05 | `adk-release-engineering` | post-MVP (triggered by lifecycle check) |
| G07 Semantic product retrieval | implementation | G01 score below T1 | `adk-memory-architecture` | post-MVP, conditional |
| G08 Signed-in customers: order status and reorder | implementation | G04, decision on Customer Account API | `adk-tool-auth-and-secrets` | post-MVP |
| G09 Reviews and Q&A content behind a reader/writer split | implementation | G04 | `adk-agent-security` | post-MVP |
| G10 Streaming replies and latency work | implementation | G04 latency measurement | `optimise-adk-on-google-cloud` | post-MVP, conditional |
| G11 Sensitive-data screening | implementation | G08 or PII seen in samples | `protect-adk-sensitive-data` | post-MVP, conditional |
| G12 In-chat order creation (Admin API / draft orders) | discovery → implementation | founders re-decide A4 | `safe-api-tool-calls` | not planned; requires a design revision |

Suggested two-week calendar for three people (provisional): days 1–4 G01 + D-01
(person A agent/tools, person B dev set labels + D-01); days 3–8 G03 (person C);
days 5–8 G02 (person A); days 9–10 G04 on a hidden page / small traffic share;
days 11–14 fix list from the dev set and first real transcripts, then full launch.

### D-01 — Verify Shopify Storefront and GCP facts

- **Question:** Can the Storefront API (version pinned) search the catalogue with
  price/option filters well enough; what are the cart create/add/update mutations,
  `checkoutUrl` behavior, cart expiry, rate limits and token type for a server
  caller? Which Vertex region serves `gemini-3.8-flash`, and what are current
  prices for it, Cloud Run and the smallest Cloud SQL tier?
- **Bounded investigation:** official Shopify and Google docs, dated; ≤ 20 calls
  against the store's development storefront; record fixtures for G01/G02 tests.
- **Expected evidence:** `docs/architecture/shopping-assistant-facts.md` with URLs,
  access dates, API version, and recorded JSON fixtures under `tests/fixtures/`.
- **Stops when:** each question has a cited answer or is marked "not available",
  with the design row it affects.
- **Primary skill:** `safe-api-tool-calls` · **Supporting:** `deploy-adk-on-google-cloud` (region and pricing facts)
- **Unblocks:** G01 live run, G02, G04 sizing.
- **Execution scope:** needs network and a Storefront token created by a founder.
- **Run this goal:** `/adk-engineer Carry out D-01 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, record cited facts and fixtures, and update the plan.`

### G01 — Assistant recommends real products, measured

- **Outcome and linked decisions:** in a local run, a shopper request returns ≤ 3
  real, in-stock products with reasons, and we know how good it is. D1, D2, D4, D7, D9; I1, T1.
- **Scope:** agent, instruction v1, `search_products`/`get_product` tools, reply
  schema and assembler, dev set (~40 cases) and runner. Excludes cart, browser, cloud.
- **Implementation route:** `LlmAgent` with two tools and `output_schema`
  (or tagged-trailer fallback if schema+tools is unsupported on the pin);
  `Runner` with `InMemorySessionService` locally; Storefront client with fixtures
  for offline tests and the real token for the live run. Confirm ADK pin and API names first.
- **Prerequisites:** Python env with the chosen ADK pin; Storefront fixtures (or
  hand-written ones until D-01 lands); founder labels for the dev set.
- **Primary skill:** `adk-tool-interface-design`
- **Supporting skills:** `adk-agent-instructions` (instruction v1, state injection);
  `adk-model-and-output-contracts` (reply schema, repair, model pin);
  `adk-agent-evaluation` (dev set, judge, error analysis);
  `adk-workflow-design` (agent/Runner wiring).
- **Acceptance:** offline — scripted model returning an unseen product ID yields no
  card (I1); prose and fenced-JSON replies follow the repair/fallback path; tool
  results ≤ 8 items and bounded size; declaration dump recorded. Live (bounded,
  ≤ 400 model calls) — dev-set score recorded against T1; hallucinated-ID rate 0.
- **Verification:** `pytest tests/` offline; `python evals/run_dev_set.py --limit-calls 400` live.
- **Execution scope:** local code authorized by running this prompt; the live dev-set run needs the Storefront token and Vertex credentials.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Add to cart and hand off to Shopify checkout

- **Outcome:** "add the blue one in M" puts exactly that variant in a Shopify
  cart and the reply carries a Checkout button with Shopify's `checkoutUrl`. D3, D4; I2, I3, I6.
- **Scope:** `update_cart`, `view_cart`, session-state `cart_id`/`shown_variant_ids`,
  assembler checkout button, adversarial cases. Excludes order status, discounts.
- **Implementation route:** Storefront cart mutations from D-01; variant must be
  in `shown_variant_ids`; quantity 1–10; one retry on timeout then `view_cart`.
- **Prerequisites:** G01; D-01 cart facts and fixtures.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-interface-design` (cart tool declarations, errors);
  `adk-agent-security` (adversarial suite: discount, fake URL, unseen ID, 500 units).
- **Acceptance:** cart lines equal the confirmed variant/quantity; unseen variant
  refused without a Shopify call; timeout path never charges and shows the cart;
  no anchor from model text; dev set extended with ~10 cart cases.
- **Verification:** offline pytest with fixtures; bounded live run on the dev store.
- **Execution scope:** local; live cart calls only against the development store.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Chat widget and session-owning API

- **Outcome:** on the dev theme a shopper chats, reloads and keeps the
  conversation; another browser cannot read it. D5, D10; I4, I5 (per-session part).
- **Scope:** FastAPI `/chat` and `/history`, signed HttpOnly cookie, overlap 409,
  per-session turn cap, `DatabaseSessionService` on local Postgres, widget rendering
  text, cards and checkout button. Excludes streaming and sign-in.
- **Prerequisites:** G01 (agent); G02 for the checkout button (can stub).
- **Primary skill:** `adk-frontend-integration`
- **Supporting skills:** `adk-memory-architecture` (session service, retention);
  `adk-operational-guardrails` (turn cap, overlap rule).
- **Acceptance:** restart the process → history and cart persist; foreign session ID
  → new session; second concurrent send → 409; widget shows cards only from data.
- **Verification:** offline API tests; local integration with Postgres and a browser.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Launch on Cloud Run with caps, telemetry and release manifest

- **Outcome:** the assistant runs on the live store (first a hidden page, then all
  pages) within a spend ceiling, observable, with a rollback path. D6, D7, D8; I5.
- **Scope:** container, Cloud Run service (max-instances 3), Cloud SQL, Secret
  Manager token, service account grants, per-IP limit, daily counter + kill switch,
  OpenTelemetry to Cloud Trace with content capture off, release manifest, 30-day
  session deletion job, privacy-notice line, baseline metrics.
- **Prerequisites:** G02, G03; founders' GCP project, region, spend allowance.
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-operational-guardrails` (daily cap, kill switch);
  `adk-agent-observability` (SLIs, content gates); `adk-release-engineering` (manifest, rollback).
- **Acceptance:** deployed revision answers 5 dev cases; kill switch returns the
  fallback without model calls; trace shows one span per agent/tool/model call with
  session ID and no prompt text; rollback to previous revision rehearsed once.
- **Execution scope:** **not yet authorized**: needs explicit approval to provision and deploy.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/shopping-assistant.md. Read docs/architecture/shopping-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

### Post-MVP goals (coarse until their trigger)

- **G05 CI regression gate** — deterministic checks every PR, dev set with pinned
  judge nightly within a call ceiling, real transcripts (redacted) promoted to eval
  cases weekly. Primary `adk-release-engineering`; supporting `adk-agent-evaluation`, `adk-agent-observability`.
- **G06 Model migration drill** — side-by-side on the frozen dev set when the
  monthly lifecycle check shows a retirement or a better model. Primary `adk-release-engineering`; supporting `adk-model-and-output-contracts`.
- **G07 Semantic retrieval** — only if G01/G05 show search recall below T1: catalogue
  sync to an embedding index with release identity and freshness. Primary `adk-memory-architecture`.
- **G08 Signed-in order status/reorder** — Shopify customer accounts (delegated
  OAuth), owner-scoped order lookup; opens private data, so redo the trifecta check.
  Primary `adk-tool-auth-and-secrets`; supporting `adk-agent-security`, `protect-adk-sensitive-data`.
- **G09 Reviews/Q&A** — third-party content; reader agent without tools hands
  structured summaries to the shopper agent. Primary `adk-agent-security`; supporting `adk-workflow-design`.
- **G10 Streaming + latency** — if p50 > ~6 s. Primary `optimise-adk-on-google-cloud`; supporting `adk-frontend-integration`.
- **G11 Sensitive-data screening** — after G08 or PII in samples. Primary `protect-adk-sensitive-data`.
- **G12 In-chat order creation** — only if founders reverse A4; needs a design
  revision for durable operation records, idempotency and reconciliation.

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/shopping-assistant.md) | Method, assumptions, decisions |
| `evals/README.md` (created in G01) | Latest dev-set result per case, linked to raw runs under `evals/runs/` |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| Checkout handoff = "place orders" (A4) | Alternative: Admin API orders (G12) | Founders | G02 scope, G12 |
| Storefront API capabilities | Unverified | D-01 | G01 live, G02 |
| Spend allowance and region | Unknown | Founders + D-01 pricing | G04 |
| Session store (Cloud SQL vs Agent Runtime sessions) | Cloud SQL proposed | Founders after pricing | G04 (local Postgres unaffected) |
| Dev-set labels | Founders' judgment | ~2 hours founder time | G01 acceptance |

## Resume here

- **Next goal:** G01 — Assistant recommends real products, measured. Ready because
  its offline part needs no external decision; the live run needs only a Storefront token.
- **Read first:** `docs/architecture/shopping-assistant.md`, this plan.
- **Next action:** confirm the ADK pin and the `LlmAgent`/`Runner`/`output_schema`
  names against it, then write the two catalogue tools against fixtures.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 — Assistant recommends real products, measured from docs/plans/shopping-assistant.md.
Read docs/architecture/shopping-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions, adk-model-and-output-contracts, adk-agent-evaluation and adk-workflow-design.
Work within local code changes and a bounded live dev-set run (≤ 400 model calls), verify the offline I1/repair cases and the dev-set score, and update
the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/shopping-assistant.md.`
