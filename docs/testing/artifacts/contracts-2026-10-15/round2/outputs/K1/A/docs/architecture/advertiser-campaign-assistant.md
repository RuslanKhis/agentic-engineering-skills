# System design: advertiser campaign assistant (pilot)

Status: **draft**. Every product decision below is a designer recommendation
built on assumed answers (the user was not available). Nothing here is
user-accepted yet. Plan: [docs/plans/advertiser-campaign-assistant.md](../plans/advertiser-campaign-assistant.md).

Revision 2 (2026-10-15): the user confirmed that asset rights also depend on
territory, flight dates and whether the creative may be modified. C1 is
revised in place; C3 and C4 widen their payload; C9 is new; D4 and D6 change;
D13 and D14 are new. The plan's change table lists every goal and test this
touches.

## Assumed answers

The user could not be asked. Each row is the answer assumed; decisions that
depend on it are provisional until the user confirms.

| # | Question that would have been asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | Is the engineer full time on this for the three weeks, and how familiar with ADK and GCP? | Full time, about 6 focused hours a day for 15 working days; experienced in Python and GCP, new to ADK (estimates ×1.5) | Plan capacity, cut line |
| Q2 | After the pilot, is the code continued or thrown away? | Continued: phase 1 code is kept | Kept-slice choices (D7, D9) |
| Q3 | What is the model and cloud allowance? | Small: about US$300 a month for the pilot project (labelled assumption) | D8, D9 |
| Q4 | Do pilot advertisers place real orders with real money, or test orders? | Real orders for the five advertisers, on their normal commercial terms | C4, C5, D5; makes the floor apply in full |
| Q5 | Does the booking system's create-order call accept a client reference or idempotency key, and can an order be looked up by it? | Unknown; the request says replay and status lookup are undocumented | **D5** (ops-placed orders in phase 1), G02, G10 |
| Q6 | How does a signed-in user map to an advertiser account and its brands? | The IdP token carries a stable subject and an advertiser organisation claim; the brand list per organisation sits in a pilot account table (five rows) the engineer maintains and each advertiser confirms | D3, C1, C2 |
| Q7 | Do rights also depend on territory, flight dates or modification? | **Answered by the user (revision 2):** yes; rights depend on owner, brand, channel, territory, flight dates and modification permission | C1, C4, C9, D4, D13 |
| Q8 | Does the rights system expose asset metadata that can be searched? | Yes: it lists assets with title, description, owner, format and channel for a brand; keyword matching runs in the tool over that list | D4 |
| Q9 | Does the booking system offer a quote or a hold, or only price and availability reads? | Read-only price and availability; no hold | C3, D6 |
| Q10 | Who can place and reconcile orders in the booking system during the pilot? | A named ad-ops contact places confirmed requests within one business day | **D5**, W5, G09 |
| Q11 | Is there an existing advertiser portal to embed into? | No; a minimal page is built | D10 |
| Q12 | Which GCP project and region, and who grants IAM and Cloud SQL? | An existing organisation project; region chosen with the platform team to match the booking and rights systems; the platform team grants access | D7, W4 |
| Q13 | Can advertisers cancel or change orders through the assistant? | No; through their account manager as today | Non-goal; no cancel action |
| Q14 | Which data is sensitive? | Per-advertiser prices and orders are commercially confidential; user name and email from the token are the only personal data | D3, logging policy |
| Q15 | Can one purchase hold several assets, and is a booking order atomic? | Up to five assets per request, placed as one booking order; partial placement is treated as a rejection | C5, G06 |
| Q16 | Who approves pilot order placement through this channel? | The booking system owner and ad-ops lead agree before the first real request (W5) | G09 |
| Q17 | What territory vocabulary do rights use, and are regions expanded to countries? | ISO 3166-1 alpha-2 country codes; a region ("EMEA", "Nordics") counts only if the rights API itself expands it; otherwise the advertiser is asked to name countries | D13, G02, G04 |
| Q18 | How are grant validity dates compared with a flight? | Calendar dates, both ends inclusive; the grant must cover every day from flight start to flight end; a flight that has already started cannot be proposed | C1, D13 |
| Q19 | What counts as modifying the creative, and does format adaptation by delivery count? | Any change to the creative as supplied (crop, resize, overlay, edit, translation) counts; the advertiser declares the intent; whether delivery's own format adaptation counts is for the delivery team to answer | C1, C9, open decision |
| Q20 | Can coverage be stitched from several grants (one grant for 1–10 March, another for 11–14)? | No: one grant must cover the whole request; stitching is refused in the pilot, which may under-offer | D13 |
| Q21 | Must one proposal span several territories? | No: one territory per proposal in phase 1; an advertiser wanting two countries confirms two proposals | D14 (scope cut) |
| Q22 | Does booking price or availability vary by territory? | Yes; the quote is per territory | C3, D6 |

## Purpose and constraints

**Journey.** A media buyer at advertiser "Acme" signs in, asks "outdoor and
social assets for the Acme Cola brand in Germany for 1–14 March, used as
supplied", sees only assets Acme Cola may use on those channels in Germany for
every day of that flight, asks for prices, picks two assets and confirms a
proposal showing assets, channels, territory, dates, modification ("none")
and price. Today this
takes emails between the buyer, the rights team and ad-ops to check rights,
get prices and book. The intended outcome: the buyer gets a rights-checked,
priced proposal in one sitting and a booking order ID within one business day.

**Non-goals.** Payment, invoicing and delivery (other teams). Cancellation
and amendment (account manager, Q13). Creative upload or approval.

**Model versus code.** The model interprets the request (channel, territory,
flight dates, whether the creative will be modified, keywords), asks for any
of these that are missing, chooses which read tools to call and explains
results. Whether a grant covers the request is decided in code (D13). Code
owns identity, the rights filter, prices, the proposal payload, confirmation,
the order-request record and every status shown.

**Observed facts.** The repository holds no application code; only the skills
directory. Version facts come from the specialists' compatibility notes and
the model lifecycle snapshot (dates below).

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | 15 working days; continued (Q2) |
| People and hours | One engineer, full time, new to ADK (Q1); runs it during the pilot with an ad-ops contact (Q10) |
| Money | Small allowance (Q3) |
| Users or judge | Five external advertisers using it for real purchases; the user's team judges the pilot |
| Data and effects | Internal commercial data (rights, prices); creates real orders that move money (Q4) |
| Delivery profile | **MVP or pilot**: first external users, real orders. Phase 1 fits the deadline; phase 2 is written |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 12-case evaluation set (G07) | CI gate when a second person changes prompts (G13) |
| Identity and per-advertiser scope | Build (C1, C2) | — |
| Secrets | Build: Secret Manager, service account | Rotation at production |
| External writes | Build: confirmation and one order request per proposal; **booking orders placed by ad-ops** (D5) | G02 documents replay and lookup → automated dispatch (G10) |
| Sensitive data | Minimal: account-scoped reads, no prompt or result content in logs | More advertisers or personal data |
| Prompt injection and agency | Build: the model holds no write tool (D2); injection cases in G06 and G07 | New write tool or untrusted source |
| Budgets | Build: per-call cap, per-account daily allowance, project quota (C7) | Traffic beyond five accounts |
| Memory | Conversation sessions only; no long-term memory | Advertisers ask for saved briefs |
| Frontend | Build minimal: non-streaming page (D10) | Feedback that latency hurts (G12) |
| Hosting | One Cloud Run service, Cloud SQL (D7) | — |
| Observability | Minimal (cut in revision 2): structured logs with session ID, tool status and token counts per invocation; no content capture; traces wait for G14 | An incident that logs cannot attribute, or phase 2 (G14) |
| Release | Minimal: pinned model, ADK and prompt versions in a manifest | G13 |

**Floor kept:** no secrets in source, prompts or logs (C8); spend stop (C7);
no order without the advertiser's confirmation and a person placing it (C4,
D5); real commercial data scoped per account (C2); pinned model (D8).
Accepted risks: none yet (the user has not been asked).

**Who and what:** five allowlisted advertiser organisations and one ad-ops
contact, on live rights data and production pricing reads; orders placed by
ad-ops. **Graduation conditions** before more advertisers: G10 (automated
dispatch with documented replay) or an explicit decision to keep ad-ops
placement; G11 status lookup; G13 evaluation in CI; a measured pilot result
(R7).

Capacity, finish range and cut line: see the plan's summary.

## Requirements and contracts

| ID | Requirement | Status |
| --- | --- | --- |
| R1 | Advertisers sign in with the existing identity provider | confirmed |
| R2 | Advertisers find media assets they are allowed to use (rights by owner, brand, channel, territory, flight dates and modification) | confirmed; widened in revision 2 |
| R3 | Advertisers buy campaigns on those assets | confirmed; ops-placed in phase 1 is assumed (D5) |
| R4 | Advertisers see what happened to a purchase | assumed |
| R5 | Pilot for five advertisers, one engineer, three weeks | confirmed |
| R6 | Spend and agency stay bounded | floor |
| R7 | The pilot shows less effort than today's email loop | assumed; measured in G09 |

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R2, R3 | An asset is shown, quoted or proposed only when a single rights grant for that asset covers one of the account's brands, the requested channel, the requested territory, every day of the flight (inclusive), and modification when the advertiser intends to modify the creative; a field that is missing, unparseable or unknown counts as not granted. *Revised in revision 2: territory, flight dates and modification added (were brand and channel only).* | Verified advertiser account and its brands; per channel, territory, flight and modification intent | Rights system | One coverage function (D13) used by `search_assets` before the model sees results, rechecked at confirmation and again when ad-ops claims the request | Fewer results with counts per reason (territory, dates, modification); "rights unavailable" when the system cannot answer, never an empty list presented as "none" | planned: offline per-field denial cases G01/A1, G01/A2, G01/A11; staging G04/A1, G04/A6; recheck G06/A4, G06/A17 |
| C2 | R1 | Every read, proposal, request and session is reachable only by users of the advertiser organisation in the verified IdP token; IDs supplied by the caller or model never select another account | Organisation from token claim; pilot allowlist | IdP token and pilot account table | Request middleware verifies the token and sets trusted context; every store query filters by account | 401/403 or "not found"; no data disclosed | planned: G03/A1, G03/A2, G03/A3, G05/A7, G06/A9, local; G08/A9 hosted |
| C3 | R3 | The price and availability a proposal shows are those of a stored quote read from the booking system for its territory, with its read time and expiry; a quote is not a reservation | Quote ID, account, territory, 15-minute validity (assumed) | Booking system pricing and inventory | `get_quote` writes the quote record; the proposal card renders from the record, not model text | Expired or unavailable: requote, never honour silently | planned: G05/A1, G05/A3, offline; G06/A3 |
| C4 | R3 | An order request exists only after the advertiser confirms the exact proposal (assets, channels, territory, flight dates, modification intent, price) and its payload hash matches; rights and price are rechecked at confirmation and at ad-ops claim | Proposal ID and payload hash | Stored proposal | Confirm endpoint outside the agent (D2); claim endpoint rechecks (D5); ordering pause flag refuses both | Refused, nothing queued; a new proposal and confirmation are needed | planned: G06/A1–A4, G06/A8, G06/A13, offline |
| C5 | R3 | One confirmed proposal yields at most one order request and at most one booking order ID recorded against it | Proposal ID | Order-request table (unique on proposal ID) | Unique constraint; single active claim; mark-placed idempotent on booking order ID. Ad-ops placing twice in the booking UI is outside code: residual risk | Duplicate confirm returns the existing request; second claim refused | planned: G06/A5, G06/A10, G06/A11, G08/A7 |
| C6 | R4 | The status shown (awaiting placement, placed with booking order ID, rejected with reason) comes from the order-request record, never from model text | Order request | Order-request record; booking order ID entered by ad-ops | Status page and `get_order_status` read the record | "Awaiting placement" until ad-ops records an outcome | planned: G06/A12. Post-placement booking status: deferred: G11 when lookup is documented |
| C7 | R6 | One invocation makes at most 12 model calls; one account starts at most 200 invocations a day; project model spend stops at a quota | Invocation; account per UTC day; project | Application counters; Vertex AI quota | `RunConfig.max_llm_calls`; allowance check before the Runner; project quota | "Limit reached" reply; no model call | planned: G01/A3, G08/A3 |
| C9 | R2, R3 | Every order request carries the rights conditions checked at confirmation (grant ID, territory, flight, whether modification is permitted and whether it was declared) and ad-ops sees them before placing | Order request | Rights grant as read at confirmation | The request record copies the evaluated grant conditions; the ops page shows them; the claim recheck compares them with the current grant | Claim refused if the current grant no longer matches | planned: G06/A16, G09/A1. What happens to the creative after placement (delivery, advertiser) is outside this system: gap: no enforcement point after placement |
| C8 | R6 | Rights and booking credentials and prompt or result content never appear in model context, source or logs | Whole service | Secret Manager | Tools read credentials in backend code; logging config disables content capture | Fail closed on missing secret | planned: G04/A3, G08/A1, G08/A4 |

## Architecture and decisions

```text
Browser (pilot page) ──OIDC──> Existing IdP
   │  JSON (chat, confirm)                    Ad-ops user ──> /ops queue page
   ▼                                                   │
Cloud Run service: FastAPI ── auth middleware (C2) ────┤
   ├─ /chat ──> ADK Runner ──> LlmAgent (gemini, 3 read tools + propose)
   │                              ├─ search_assets ──> Rights system (read)
   │                              ├─ get_quote ──────> Booking system (read)
   │                              └─ propose_order ──> proposal record
   ├─ /confirm  (not a tool) ──> recheck ──> order-request record
   └─ /ops/claim, /ops/placed, /ops/reject ──> order-request record
Cloud SQL Postgres: ADK sessions, quotes, proposals, order requests, allowances
Ad-ops places the order in the booking system UI and records its ID.
```

| ID | Enforces | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | C1, C3 | One `LlmAgent` with four function tools: `search_assets`, `get_quote`, `propose_order`, `get_order_status` | The journey is one conversation over a few capabilities; no step needs a separate context or credential | Multi-agent split adds routing and handoffs without a distinct responsibility | Declaration dump shows four tools; G07 selection accuracy |
| D2 | C4, C5 | The model can only create proposals; confirmation is a browser button posting to `/confirm`, an endpoint no tool reaches | Asset descriptions are untrusted text written by media owners; removing the write leg from the agent breaks the injection path structurally | ADK native tool confirmation not used; one extra endpoint | G06/A8: injected description, no request created |
| D3 | C2, C1 | FastAPI middleware verifies the IdP ID token (issuer, audience, expiry, signature via JWKS), maps the org claim to the pilot account table, and writes account ID and brands into session state under a server-owned key the tools read | Scope comes from the verified token, never model arguments | Pilot account table is manual (five rows) | G03/A1–A3 |
| D4 | C1 | `search_assets(keywords, channel, territory, flight_start, flight_end, modify_creative=False)` takes no brand or account argument; territory and both dates are required parameters; it queries rights for the trusted brands, applies D13, matches keywords in code and returns at most 10 assets with their grant ID and conditions, plus counts of assets excluded per reason. *Revised in revision 2.* | Model cannot widen scope or skip a rights dimension; required parameters make the model ask for missing ones | Keyword match is crude versus semantic search; the advertiser must state territory and dates before seeing anything | G01/A1–A2, G01/A11, G04/A1 |
| D5 | C4, C5, C6 | **Phase 1 orders are placed by ad-ops**: a confirmed proposal becomes an order request; ad-ops claims it on `/ops` (claim rechecks rights and price), places the order in the booking UI, records the booking order ID or a rejection | Booking replay and status lookup are undocumented, so an automated create cannot promise at most one order after a lost response; five advertisers make manual placement affordable | Up to one business day to placement; ad-ops effort per order. Alternative: automated single-dispatch with manual reconciliation of unknowns, deferred to G10 after G02 | G06/A1–A13 |
| D6 | C3 | `get_quote` reads price and availability for one territory (Q22), stores a quote record with read time and a 15-minute expiry (assumed), returns its ID; proposals reference quote IDs | Price the advertiser sees is a stored fact, not model output | Quote can go stale before ad-ops places: recheck at claim | G05/A1–A3 |
| D7 | C2, C5, C7 | One Cloud Run service (FastAPI around the ADK `Runner`, static page) with a dedicated service account; Cloud SQL for PostgreSQL holding `DatabaseSessionService` tables and application tables; Secret Manager for rights and booking credentials | One deployable for one engineer; Postgres gives the unique constraint and durable records | Agent Runtime would host the agent but the confirm and ops endpoints need a gateway anyway | G08/A1–A7 |
| D8 | C7 | Model `gemini-3.5-flash` on Vertex AI, pinned. Lifecycle snapshot `checked_on` 2026-10-08: stable, Vertex retirement 2027-05-19 or later | Outlives the pilot and phase 2. `gemini-3.6-flash` (Vertex retirement 2026-11-19) and `gemini-3.7-flash` (2027-01-28) retire within the horizon; `gemini-3.8-flash` has no Vertex entry in the snapshot | Not the newest model; revisit 3.8-flash once its Vertex lifecycle is confirmed | G08/A5 manifest; refresh the snapshot before G01 |
| D9 | C7 | `RunConfig(max_llm_calls=12)`; per-account daily invocation counter in Postgres checked before the Runner; Vertex AI request quota on the project; budget alert (observes only) | A quota stops calls; the alert only informs | Counters are per invocation, not per token | G01/A3, G08/A3 |
| D10 | C3, C4 | Minimal page: chat with non-streaming JSON replies; proposal card rendered from the proposal record with a Confirm button; order list from records | Least frontend work that keeps price and payload out of model text | No streaming; slower perceived replies | G03/A4, G06/A12 |
| D11 | C6 | Status after placement (live, delivered, paid) is not shown; the page names the account manager | Booking status lookup is undocumented; payment and delivery belong to other teams | Advertisers check elsewhere after placement | deferred: G11 |
| D12 | C4 | An ordering pause flag in configuration makes `/confirm` and `/ops/claim` refuse while search and quotes continue | Operator stop outside agent authority | One config change and a redeploy or env update | G06/A13 |
| D13 | C1, C9 | One pure function `rights_cover(grants, request)` decides coverage for search, confirmation and claim. A single grant must match brand, channel, territory (after the alias table from G02), cover flight start to end inclusive, and permit modification when declared; missing or unknown values deny; returns the grant ID and a reason code | One implementation cannot diverge between the three checks; table-driven tests cover each field | No stitching across grants (Q20) can refuse a campaign a person would approve | G01/A11, G04/A6, G06/A4, G06/A17 |
| D14 | C1, C3, C4 | One territory per proposal in phase 1 (scope cut in revision 2) | Keeps coverage, quotes and the confirmation card to one territory each, which fits the three weeks | Multi-country campaigns need one confirmation per country | Later list: multi-territory proposals |

**Versions.** ADK: google-adk 2.8.0, the version the specialists'
`references/compatibility.md` record; confirm against the chosen pin in G01.
`DatabaseSessionService`, `RunConfig.max_llm_calls` and function-tool
signatures are version-dependent and are checked there. GCP service limits,
regions and prices were **not** checked (no network in this session); G08
records the sources and dates.

### Model-facing interfaces

| Surface | Interface | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Interprets brief into channel, territory, flight dates, modification intent and keywords; asks for territory, dates and modification intent when missing and never assumes them; never states a price outside a quote; explains rights refusals by reason; does not claim an order is placed. Account, brands, date and limits stay in code | `adk-agent-instructions`; rendered-request test in G01 |
| Tools | Four function tools (D1); results bounded to 10 assets and 300 characters of description each; each returns `status` and an actionable error; tiers: read (search, quote, status), draft (propose). No write or irreversible tool | `adk-tool-interface-design`; declaration dump in G01 |
| Output | Free text; structured data lives in tool results and records, so no `output_schema` | `adk-model-and-output-contracts` for D8 only |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Rights | Rights system; per brand, channel, territory, validity window and modification permission | Rights system / `search_assets`, recheck | Read live each search and recheck | Not stored beyond the tool result |
| Quote | Account | `get_quote` / proposal, claim | Booking read, 15-minute expiry | Pilot duration |
| Proposal | Account | `propose_order` / confirm, page | Built from quote records; payload hash | Pilot duration |
| Order request | Account; ad-ops | `/confirm`, `/ops/*` / page, `get_order_status` | Authoritative for phase 1 status | Retained for audit after pilot (owner to decide) |
| Session events | User within account | ADK Runner / Runner | Conversation only; never authority | 30 days (assumed) |
| Allowance counter | Account, UTC day | Middleware | Postgres | 7 days |

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Campaign assistant | Account's prices, proposals, requests | Asset titles and descriptions from media owners | Draft proposals only; no order, message or external write | Write leg removed (D2); the proposal is inert until the user confirms in code; injection cases G06/A8, G07/A2 |

## Budgets and capacity

Five accounts, assumed at most 30 conversations a day in total, each about
6 model calls (expected) and 12 (bounded) with around 6k input tokens per
call. Cost is symbolic until prices are checked: daily cost ≈ 30 × 6 × (6k ×
input price + 0.5k × output price). One Cloud Run instance minimum 0, maximum
3; one small Cloud SQL instance is the fixed cost. No latency target given:
G09 measures time to a complete reply.

## Failure and recovery

Coverage grid (the booking system is read-only in phase 1; order creation
happens in its UI, by a person):

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Identity provider | G03/A5 | G03/A1 | n/a: verification only, no writes | n/a: single verification step | G03/A6 | n/a: JWKS cached, five pilot users | n/a: stateless token verification | G03/A1 |
| Rights system | G04/A2 | G04/A7 | n/a: read only | n/a: read only | G04/A3 | G04/A4 | n/a: reads are repeatable | G04/A5, G06/A8 |
| Booking system (price and availability reads) | G05/A2 | G05/A4 | n/a: reads create nothing (Q9) | n/a: read only | G05/A5 | G05/A6 | n/a: reads are repeatable | G05/A8 |
| Cloud SQL (sessions, records) | G08/A6 | G06/A5 | G06/A5 | G06/A11 | G08/A6 | n/a: bounded pool, five accounts | G08/A7 | n/a: application-owned schema only |
| Vertex AI model | G01/A5 | G01/A8 | n/a: model has no write tool | n/a: replies are not streamed | G08/A8 | G01/A6 | n/a: model calls have no effects | G01/A7, G06/A8 |

Action grid:

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| Advertiser confirms a proposal (creates an order request) | G06/A6 | G06/A11 | G06/A2, G06/A3, G06/A4, G06/A17 | G06/A5 | G06/A5 |
| Ad-ops places the order and records its outcome | G06/A9, G06/A14 | G06/A15 | G06/A3, G06/A16, G06/A17 | n/a: ad-ops sees the booking result directly | G06/A10 |

Cross-cutting scenarios:

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Price changes between confirmation and ad-ops claim | Request shown as rejected "price changed, please reconfirm" | Request rejected; no booking order | Advertiser requotes; ad-ops |
| Rights revoked, narrowed (territory, dates, modification) or expired while a request waits, or the flight start passes before placement | Rejected with the reason, e.g. "grant no longer covers 1–14 March in DE" | No booking order | Advertiser picks another asset or flight; ad-ops (G06/A17) |
| Ad-ops places the order but the browser fails before recording the ID | Request stays "claimed" | Booking order exists; record incomplete | Ad-ops reopens the claimed request and records the ID; runbook check of requests claimed over 1 hour (G09/A2) |
| Process restart mid-conversation | Conversation resumes; pending proposals and requests unchanged | Postgres state | None; G08/A2 |
| Daily allowance or model quota exhausted | "Daily limit reached" | No model call | Next UTC day; engineer raises the limit |
| Rollback | Previous revision serves; records untouched | Schema migrations are additive in phase 1 | Engineer, Cloud Run revision rollback |

## Verification and implementation handoff

Offline checks use fake rights and booking adapters and a scripted model
(G01, G04–G06). Local integration uses staging rights and booking (G04, G05,
G06). Hosted checks run on the Cloud Run staging deployment (G08, G09).
R7 is a hypothesis: G09 records, per pilot order, minutes from first question
to confirmed request and the number of emails needed, against the
advertisers' own estimate of today's loop.

Release unit (G08): image digest, prompt version, model ID, ADK pin and tool
declaration hash in one manifest. Rollback: previous Cloud Run revision kept.

Goals, estimates and the next prompt: see the plan.

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| Ops-placed orders in phase 1 (D5) | Product choice: advertisers wait up to a day for placement | User | G06 scope; G10 timing |
| Booking create replay and lookup semantics (Q5) | Decides whether G10 can promise at most one order automatically | Booking team; G02 | G10, G11 |
| Territory vocabulary, date semantics and modification encoding (Q17, Q18, Q20) | Unresolved values deny (D13), so a wrong assumption under-offers rather than over-offers | Rights team; G02 | G04 alias table |
| Does delivery's format adaptation count as modification (Q19)? | If yes, every unmodified-only grant forbids formats that need adaptation | Delivery team, rights team | C9 wording; G09 |
| One territory per proposal (D14) | Scope cut; multi-country campaigns take several confirmations | User | Later list item |
| Org claim and brand mapping (Q6) | Scope source for C1, C2 | IdP team, advertisers | G03 |
| Quote validity 15 minutes (D6) | Recheck rejects and requote frequency | Pricing owner | G05 |
| GCP project, region, Cloud SQL (Q12) | Hosting and residency | Platform team; W4 | G08 |
