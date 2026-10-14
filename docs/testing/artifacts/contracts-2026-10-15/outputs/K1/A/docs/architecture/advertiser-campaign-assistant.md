# System design: advertiser campaign assistant (pilot)

Status: **draft**. Every decision below is a recommendation, provisional on the
assumed answers. The user was not available to confirm any of them, except
the rights fields: on 2026-10-15 the user confirmed that rights also depend on
territory, flight dates and whether the creative may be modified (revision 2;
see "Revision 2" at the end). Capacity,
finish range and cut line are in the plan's summary
([plan](../plans/advertiser-campaign-assistant.md)) and are not restated here.

## Assumed answers

The user could not be asked, so these answers are assumed. Decisions that
depend on them are provisional.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | After the three weeks, is the pilot continued? | Yes. Phase 1 code is kept and phase 2 builds on it | All. Kept-slice form (configuration over hard-coding) |
| Q2 | Is the engineer full time, and how familiar with ADK and GCP? | Full time for 15 working days, about 4.8 focused hours a day (8 × 0.6, because of meetings with the rights, booking, IdP and sales-ops teams). Knows Python and GCP, new to ADK (×1.5 on every estimate) | Plan capacity, cut line |
| Q3 | Model and cloud budget? | A small pilot allowance (assumed under USD 500 a month for models and cloud, to be confirmed). Billing alert at 50/90/100 % | D9 |
| Q4 | Who uses it? | Five external advertisers, one or two named people each, using a web page. Judged by the pilot owner on completed purchases and on how often advertisers need help | D4, D6, profile |
| Q5 | What does a purchase commit? | A booking order is a binding commercial commitment. Payment teams invoice from it and delivery teams fulfil it. That is money, so it is irreversible for this design | C4, C5, D2, D3 |
| Q6 | How does the IdP identify an advertiser? | OIDC with a stable `sub` and an organisation claim. The pilot owner maintains a reviewed table mapping each org to its brand IDs | C2, D4 |
| Q7 | What do rights depend on? | **Answered by the user (2026-10-15):** owner, brand, channel, territory, flight dates and whether the creative may be modified. Replaces the earlier assumption of owner, brand and channel only | C1, C4, C12, D8, D11, D12 |
| Q8 | Where does asset metadata come from, and how many assets? | The rights system (or the DAM behind it) lists assets by brand and channel, with title, description, format and owner. Under a few thousand assets per brand and channel | D8. No RAG in phase 1 |
| Q9 | Are there staging environments? | The rights system has a read API usable with pilot credentials. The booking system has a staging environment for pricing, inventory and orders | C3, G03, phase-2 G08 |
| Q10 | Is there a team that can place booking orders by hand? | Yes. Sales ops (ad ops) already enters orders into the booking system and can process pilot purchase requests within one business day | D3. **The phase-1 cut line depends on this** |
| Q11 | Is there an existing advertiser portal to embed into? | No. The pilot serves its own minimal page | D6, G04 |
| Q13 | How are rights dates compared? | Grant start and end dates and flight dates are calendar dates, both ends inclusive, with no time-of-day or timezone conversion (O8) | C1, D11; G01/A2 boundary cases |
| Q14 | How are territories expressed? | ISO 3166-1 alpha-2 country codes, in both the rights system and the booking system. No regions such as "EMEA". Common names ("UK") map to codes (GB) through an alias table in code (O8) | C1, D11 |
| Q15 | What does "may be modified" look like, and do pilot campaigns need modification? | A yes/no flag per grant. Pilot campaigns use creatives **as-is**, so phase 1 never requests modification. Modification requests come in phase 2 (G13) (O9) | C1, C12, D12 |
| Q16 | Does the rights API return grant records or a yes/no check? | Grant records (owner, brand, channel, territory, start, end, modification allowed, grant ID). Our code decides coverage (O10) | D11 |
| Q17 | Do booking pricing and inventory take territories? | Yes, quotes are per territory and flight (O12) | C3, G03 |
| Q12 | Data residency, retention, approvals? | Data stays in one EU or US region the company already uses. Conversations are kept for 90 days. A security review of this design and a go-live approval by the commercial owner are needed before external users get access. The security review is assumed to be a design review (O7). Go-live approval is given on G06's evidence | D5, D6, waits W4, W6 |

## Purpose and constraints

**Journey (running example).** Dana, a media buyer at pilot advertiser *Acme
Drinks*, signs in with the company IdP. She asks for "summer outdoor visuals
we can run on social". The assistant asks where and when, and she answers
"UK and Ireland, 1–14 July". She gets only the assets that Acme's brand may
use as-is on social, in both countries, for every day of that flight. She asks
for a price on three of them and sees a quote with an expiry. She confirms the
exact assets, territories, dates, as-is use and price on a card, and later sees
the purchase status. **Current friction (assumed):** she emails an account manager, who checks
rights in one system and prices in another. This takes days, and sometimes an
asset without rights reaches a proposal. **Outcome to improve:** time from
request to placed order, with zero orders on assets without rights. There is no
measured baseline yet, so this is a hypothesis. G06 records the baseline from
the account managers' current turnaround.

**Facts from the request:** existing IdP; a rights system keyed by owner,
brand and channel, whose grants also depend on territory, flight dates and
modification (user update, 2026-10-15); a separate booking system for pricing, inventory and orders,
whose replay and status-lookup behaviour is **undocumented**; payment and
delivery owned by other teams; one engineer; three weeks; five advertisers.
**Repository:** empty except `.claude/skills`. There is no existing code,
manifest or document convention, so this follows the skill's default paths.

**What the model does and what code controls.** The model reads the
advertiser's request, turns it into proposed terms (territories, flight dates)
that the user confirms on the card, chooses search filters, ranks and explains the results
it is given, and asks follow-up questions. Code controls who the advertiser is,
which brands, channels, territories and dates the rights cover, every price, quote, expiry, the
confirmation and the order request. The model never holds a tool that commits
money (D2).

**Non-goals for the pilot:** payment, invoicing, delivery tracking, creative
editing, self-serve onboarding and asset upload.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | 15 working days; continued (Q1) |
| People and hours | One engineer, full time, new to ADK (Q2); runs it during the pilot |
| Money | Small pilot allowance, assumed (Q3) |
| Users or judge, and what they read | Five external advertisers on a web page; pilot owner reads completed purchases, support load and the evaluation summary |
| Data touched and effects allowed | Real rights and pricing data, which is commercially sensitive. Real purchase commitments (money, Q5) |
| Delivery profile | **MVP or pilot.** External users and real money; phase 1 must be safe for them, phase 2 is written |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment (search relevance, asking for missing territory and dates, honest quoting) | Build: labelled set of 20–25 cases (G06) | Gate in CI once the agent changes weekly (G10) |
| Identity and per-advertiser scope | Build (G04) | n/a, already at build depth |
| Secrets and credentials | Build: Cloud Run service account and Secret Manager (G02) | Rotation when production starts |
| External writes (orders) | Build, with an **ops-placed** purchase request in phase 1 (D3). Automated booking writes are phase 2 (G08) | G07 discovery settles booking replay and lookup |
| Sensitive data | Build: no prompt or response content in logs; per-advertiser scope | Model Armor or SDP when free-text personal data appears |
| Prompt injection and agency | Build: the agent has no write or egress tool (C9); one adversarial case | Any write tool given to the agent |
| Budgets and loop limits | Build: `max_llm_calls`, per-advertiser daily allowance, kill switch (C8) | Shared or public access |
| Memory and retrieval | Minimal: persisted sessions only, no semantic memory, no RAG | Catalogue too large for filter-then-rank (O3) |
| Frontend | Build: minimal page with a confirmation card (G04) | Embedding into an advertiser portal |
| Hosting | Build: one Cloud Run service; rollback is the previous revision (G02) | SLOs agreed |
| Observability | Minimal: structured logs with IDs and token counts (G02). Traces and dashboards come in G11 | More than 5 advertisers or the first incident |
| Release engineering | Minimal: pinned model and ADK, unit tests run before each deploy | G10 |
| Performance tuning | Defer | Measured latency complaint |

**Floor kept:** no secrets in code, prompts or logs. A spend stop:
`RunConfig.max_llm_calls`, a per-advertiser daily allowance and a billing budget
alert. No order exists without the advertiser's explicit confirmation of the
exact payload, and in phase 1 a human in sales ops places it. Real data is
scoped to the advertiser's brands and kept out of logs. The model ID is pinned.
**Accepted risks:** none yet.

**Who may use it:** the five pilot advertisers' named users, on their own
brands' data. **Graduation conditions** before more advertisers: G08 automated
booking with a settled replay mode, G09 reconciliation, G10 evaluation gate,
G11 traces and alerts, and G13 (modification requests) if advertisers need modified creatives.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Automated order placement in the booking system | Replay and status lookup are undocumented. A wrong guess means duplicate or lost orders | G07 establishes a supported idempotency key or lookup by client reference |
| Booking status lookup | Same unknown | G07 |
| Evaluation gate in CI | One engineer and weekly changes at most | Second engineer or weekly prompt changes |
| Traces, dashboards, SLO alerts | Five users; logs are enough to diagnose | More advertisers, or an incident that logs could not explain |
| Modification requests (creative changed) | Pilot campaigns are assumed to use creatives as-is (Q15). As-is use keeps the modification right satisfied without modelling modification levels | An advertiser needs a modified creative, or O9 shows modification levels (G13) |
| Content screening (Model Armor, SDP) | No free-text personal data is expected | Advertisers paste personal or confidential data |

## Requirements and contracts

| ID | Requirement | Need it serves | Status |
| --- | --- | --- | --- |
| R1 | Advertisers find media assets they are allowed to use, for the territories, flight dates and use (as-is or modified) of their campaign | Search without rights mistakes | Confirmed (request; fields confirmed 2026-10-15) |
| R2 | Advertisers buy campaigns on those assets | Purchase without an account manager | Confirmed (request); ops-placed in phase 1 is assumed (Q10) |
| R3 | Advertisers see what happened to a purchase | Trust and fewer support emails | Assumed |
| R4 | Advertisers sign in with the existing IdP | Reuse identity | Confirmed (request) |
| R5 | The pilot stays within budget and can be stopped | Spend and incident control | Assumed (floor) |
| R6 | Sales ops and delivery know the rights terms each order was cleared for | No placement or delivery outside the grant | Assumed (follows from the rights fields) |

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | An asset is quoted, proposed or requested only if the rights system's grants for that owner, brand and channel cover **every requested territory for every day of the flight** (inclusive dates) and permit the requested use. In phase 1, use is as-is only, so a grant that forbids modification still qualifies. Search shows only assets whose grants cover the brand, channel, territories and flight it was given, and it does not search before channel, territory and flight dates are known | Verified advertiser's brands; requested channel, territories, flight start and end, use (as-is); time of the call | Rights system grant records | One pure function, `rights.evaluate(grants, terms)`, in code. Used by `search_assets` before the model sees results, and rechecked by `get_quote`, `propose_purchase`, `/confirm` and the ops export (the export is the last check before sales ops places the order) | Denial with a per-field reason ("rights end 31 July; your flight ends 14 August"). A shorter flight or fewer territories may be suggested, never applied silently. At confirm or export: "rights changed, not requested" or request rejected | planned: table-driven cases per field, including date and territory boundaries and fragmented grants, offline (G01/A2, G01/A6); recheck at quote (G03/A2), at confirm (G05/A3) and at export (G05/A10) |
| C2 | R4 | Every session, quote, proposal and request is read or written only by its owning advertiser. Scope comes from the verified IdP token, never from model arguments or caller-supplied IDs | Advertiser org and user; all stored records | IdP token and pilot org-to-brand table | Server middleware verifies the token and sets trusted state. Tools read scope from state. Every store query filters by owner | 401 or 404 with nothing disclosed | planned: cross-advertiser denial for session and quote (G04/A2, G04/A3), proposal, confirm and status (G05/A9), local; real accounts (G12/A1) |
| C3 | R2 | A quote states price and availability from the booking system as of a time, with an expiry. It is not a reservation. The prices shown on the confirmation card come from the quote record, not model text | Quote ID, advertiser, expiry | Booking pricing and inventory | `get_quote` stores the quote and the card renders from the record. Expiry is checked again at confirm | Expired quote: "price expired, re-quote", nothing requested | planned: expired-quote and model-misstated-price cases, offline (G03/A3, G05/A4) |
| C4 | R2 | A purchase request exists only after the advertiser confirms the exact assets, territories, flight dates, use (as-is) and price. A changed payload needs a new confirmation | Proposal ID and canonical payload hash | Stored proposal | Confirm endpoint, which is not a model tool, requires proposal ID and hash. It rechecks C1, C2 and C3 at the effect | Refused, nothing requested; the card asks to confirm again | planned: changed-payload and model-attempted-purchase cases, offline (G05/A2, G05/A5) |
| C5 | R2 | One confirmation produces at most one order in the booking system | Proposal ID as operation ID | Purchase-request table (phase 1); booking receipts (phase 2) | Phase 1: unique constraint on the proposal ID, and sales ops enters the request ID as the booking reference. Phase 2: durable operation record and replay only under the guarantee G07 finds | Duplicate click returns the existing request. Uncertain booking write shows as "pending, being checked" | planned: double-confirm and concurrent-confirm cases, local (G05/A6); phase 2 lost-response case (G08/A2) |
| C6 | R3 | The status shown comes from the authoritative record: request state set by sales ops in phase 1, booking receipts in phase 2. The model never infers it | Advertiser's own requests | Purchase-request table; booking system | `get_request_status` reads the record and returns it verbatim | "Unknown, checking" rather than a guess | planned: status-mismatch case, offline (G05/A7); booking lookup (G09/A1) |
| C7 | R1, R2 | When the rights system, booking system or model fails, the user gets an explicit failure. Scope never broadens and no stale answer is offered as current | Per invocation | Adapter results | Adapters return typed `unavailable` results and the tools pass them through. No fallback to cached rights. At `/confirm`: refuse. At the export: hold the request, neither listed nor rejected | "Rights check unavailable, try again shortly" | planned: unavailable and timeout cases per adapter, offline (G01/A3, G03/A4); at confirm and export (G05/A3, G05/A10) |
| C8 | R5 | Each invocation makes at most N model calls. Each advertiser gets at most M invocations a day. An operator can disable purchases or the whole agent without a deploy | Invocation; advertiser per UTC day; whole service | Config and the usage table | `RunConfig.max_llm_calls`; admission check before the Runner; `PURCHASES_ENABLED` and `AGENT_ENABLED` flags read per request | "Daily limit reached" or "temporarily unavailable"; confirmed requests are kept | planned: limit and kill-switch cases, local (G02/A3, G02/A4) |
| C9 | R2, R5 | Text in asset metadata or tool results cannot cause a purchase or send data anywhere | Agent tool set | Code: the agent's tool list | The agent has only read tools and a proposal tool that creates no effect. The answer renders as plain text, with no links or images fetched | The forbidden effect never runs | planned: injected-metadata case asserts no proposal is confirmed and no unknown tool is called, offline (G05/A5, G06/A3) |
| C10 | R1, R2 | Asset facts and prices in an answer come from this invocation's tool results | Per answer | Tool results | Grounding instruction; card and prices rendered from records (C3) | Measured, not guaranteed: wrong claims are counted | planned: labelled set, grounding rate, live (G06/A1) |
| C12 | R6 | Every purchase request stores the rights terms it was cleared against (grant IDs, territories, flight dates, use: as-is). The ops export shows them, and a request can be marked placed only with booking territories and flight dates equal to the request's | Purchase request | Request record (snapshot of the evaluated grants) | `/confirm` stores the terms snapshot. The export prints it. `set-state placed` refuses booking territories or dates that differ | `set-state` refuses and the engineer corrects the booking. The advertiser sees "being checked" | planned: snapshot and mismatch cases, local (G05/A8) |
| C11 | R5 | No prompt, response, price or token appears in logs | All log sinks | Logging config | Structured logger with an allow-list of fields; ADK content capture off | n/a | planned: log-capture test, local (G02/A5) |

C1 revision note (2026-10-15, revision 2): the user confirmed that rights
also depend on territory, flight dates and modification. C1 now covers all
six fields through one evaluation function, adds a recheck at the ops export,
and forbids searching before territory and dates are known. Changed with it:
C4 (payload), new C12, D8, new D11 and D12, the tool signatures, G01/A2, new
G01/A6, G03/A2, G03/A5, G05/A2, G05/A3, G05/A8, new G05/A10, G06/A1 and the
plan's estimates.

## Architecture and decisions

```text
Browser (minimal page) ──OIDC──> Existing IdP
   │  chat + confirm card
   ▼
Cloud Run: FastAPI app  [trust boundary: verifies IdP token]
   ├─ middleware: token → advertiser org → brands (pilot table) → session state
   ├─ /chat → admission (C8) → ADK Runner(App: LlmAgent "campaign_assistant")
   │        tools: search_assets, get_quote, propose_purchase, get_request_status
   │        model: Vertex AI gemini-3.8-flash (pinned)
   ├─ /confirm (NOT a model tool) → recheck C1-C4 → insert purchase_request + terms snapshot (C5, C12)
   ├─ app.ops export (rechecks C1) / set-state (checks C12) → sales ops places order in booking UI
   ├─ rights.evaluate(grants, terms): pure function used by search, quote, propose, confirm, export
   └─ adapters: RightsClient (grant records, read), BookingClient (pricing/inventory per territory, read)
Cloud SQL Postgres: ADK sessions, quotes, proposals, purchase_requests, usage
Secret Manager: rights/booking API credentials, OIDC client secret
```

Sequence for a purchase: `get_quote`, then the stored quote; `propose_purchase(quote_id)`, then a stored proposal and its payload hash; the page renders the card from the record. The user clicks Confirm, which posts `/confirm {proposal_id, hash}`. The server verifies the token and owner, checks the hash, rechecks rights for every territory and day of the flight, and checks quote expiry and kill switch. It then runs `INSERT ... ON CONFLICT (proposal_id) DO NOTHING` and returns the request. The engineer exports new requests daily. The export re-evaluates rights and rejects any request whose grants no longer cover it. Sales ops places each order with the request ID as reference, and the engineer records `placed` (with the booking order number) or `rejected`. An ops page is a phase-2 option.

| ID | Enforces | Design choice | Reason | Tradeoff / alternative | Verification and expected result |
| --- | --- | --- | --- | --- | --- |
| D1 | C9, C10 | One `LlmAgent` with four function tools; ordinary code for everything deterministic | Language interpretation over a small capability set. No step needs a second agent | Multi-agent search and purchase agents: more routing and evaluation for no distinct authority, since D2 already removes the write leg | Declaration dump shows 4 tools. Rendered-request test (G01/A4) |
| D2 | C4, C9 | Confirmation and purchase are a plain HTTP endpoint behind a card rendered from the stored proposal. The model can only *propose* | Confirmation in code the model cannot reach, bound to a payload hash, so injection cannot buy | ADK tool confirmation keeps the model in the loop, and its documented limitations must be checked against the pin (adk.dev/tools-custom/confirmation). Rejected for the pilot | Changed-hash and model-attempted-confirm cases (G05/A2, G05/A5) |
| D3 | C5, C6 | **Phase 1:** a confirmed purchase becomes a durable purchase request that sales ops places in the booking system by hand. **Phase 2:** automated placement in the mode G07 selects | Booking replay and lookup are undocumented, so automating the write now would promise C5 without a mechanism. Sales ops already places orders, and five advertisers make the volume small | Advertisers wait up to one business day for placement (Q10). Alternative: automate now with at-most-once dispatch and manual reconciliation. It does not fit the capacity (see the plan's what-if) | Double-confirm returns one request (G05/A6). Ops state change shows in status (G05/A7) |
| D4 | C2 | OIDC authorization-code flow in the FastAPI app. The verified `sub` and org map to brands through a reviewed pilot table. The server writes `advertiser_id` and `brand_ids` into session state, and tools read them from `ToolContext.state` | Scope from trusted code. Caller IDs only locate records | IdP claims as brand source: cleaner, but needs IdP-team work (O2) | Cross-advertiser denial tests (G04/A2, G04/A3) |
| D5 | C2, C5, C8 | Cloud SQL for PostgreSQL holds ADK sessions (`DatabaseSessionService`, to be confirmed at the pin) and business tables with owner columns and a unique constraint | One store with transactions and uniqueness for proposals, requests and usage | Firestore: no SQL session service. In-memory sessions: lost on restart while requests must persist | Restart keeps the session and request (G02/A2); concurrent confirm (G05/A6) |
| D6 | C2, C8 | One Cloud Run service with app-level OIDC, max instances bounded (assumed 3), and the previous revision kept for rollback | Smallest host that serves external users with custom endpoints | Agent Runtime: managed, but the custom confirm, ops and auth endpoints need a gateway anyway. GKE: too much operation for one engineer | Deploy readback and revision rollback (G02/A1) |
| D7 | C10 | Model `gemini-3.8-flash` on Vertex AI, pinned. Chosen from `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (checked_on 2026-10-08): stable, released 2026-09-02, no shutdown announced. `gemini-3.7-flash` (Vertex retirement 2027-01-28) and `gemini-3.6-flash` (2026-11-19) retire within the plan horizon | Newest stable model with no announced retirement | The Vertex retirement for 3.8 is not in the snapshot, so G01 verifies it. A Flash-Lite model is cheaper; consider it after G06 measures quality | G01/A1 records pin and lifecycle date |
| D8 | C1, C7 | Rights adapter fetches grant records live per call: the advertiser's brands, the requested channel and territories, with dates overlapping the flight. `rights.evaluate` filters, then keyword filtering in code and model ranking over at most 20 results. No cache or index (revised 2026-10-15) | Rights freshness matters more than search sophistication at pilot scale (Q8) | Semantic search or RAG over the catalogue: better recall but needs ingestion governance. Deferred (O3) | Per-field denial (G01/A2) and empty result without broadening (G01/A5) |
| D11 | C1, C12 | Rights coverage is decided in one pure function: for each requested territory, the union of that territory's grants (same owner, brand and channel, use permitted) must cover every day from flight start to flight end, inclusive. Search, quote, propose, confirm and export all call it. It returns per-field reasons and the grant IDs used | One implementation means the five check points cannot disagree. Union coverage handles fragmented grants (Jan–Jun plus Jul–Dec) | A rights-system check endpoint, if one exists (O10): less code here, but every check becomes a network call, and the reasons may be less specific | Table-driven tests on boundaries, fragmented grants, missing territory and expired grant (G01/A2) |
| D12 | C1, C12 | Phase 1 supports **as-is use only**. Every term set carries `use: as-is`, the card says so, and the request and export record it, so delivery knows not to modify | Keeps the modification right satisfied without modelling modification levels in three weeks | Advertisers who need modified creatives wait for G13. Alternative: support modification now, which adds hours (see the plan's what-if) | Card and export show as-is (G05/A8). A user asking for modification gets "not in the pilot" (G01/A6) |
| D9 | C8, C11 | `max_llm_calls=8` per invocation (assumption), 50 invocations per advertiser per UTC day (assumption), env-flag kill switches, a Cloud Billing budget alert (alerts only, not a cap), and structured logs with allow-listed fields | Cheap floor controls that match the pilot's depth | A shared token budget across workers: not needed for five advertisers | G02/A3, G02/A4, G02/A5 |
| D10 | all | ADK `google-adk==2.8.0` is the working assumption, because every specialist's `references/compatibility.md` was checked against it. Observability guidance prefers 2.10.0 or later for new deployments | A pinned, documented baseline | Choosing 2.10+ needs a re-check of APIs used here | G01/A1 confirms against the chosen pin |

### Model-facing interfaces

| Surface | Interface | Implementing skill and verification |
| --- | --- | --- |
| Instructions | One instruction: find licensed assets, ask for territories and flight dates rather than guessing them, say modified creatives are not in the pilot, quote only through the tool, never state a price not in a tool result, propose rather than promise. Identity, brands, limits and dates come from code, not the prompt | `adk-agent-instructions`; rendered-request test (G01/A4) |
| Tools | `search_assets(query, channel, territories[ISO codes], flight_start, flight_end, max_results≤20)` returns `needs_input` naming the missing fields when territory or dates are absent. Code validates codes and date order. `get_quote(asset_ids, channel, territories, flight_start, flight_end)`, `propose_purchase(quote_id)`, `get_request_status(request_id?)`. Results are bounded dicts with `status` and actionable errors. Tiers: read, read, draft (no external effect), read | `adk-tool-interface-design`; declaration dump |
| Output, model, backend | Free-text answer, no `output_schema`. Structured data reaches the user through records (card, status), not model JSON. Pinned `gemini-3.8-flash` on Vertex | `adk-model-and-output-contracts`; pin check in G01 |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Rights | Rights system | Read by the adapter only | Live per call | Not cached. The grant IDs and terms used at confirm are stored with the request (C12) |
| Asset metadata (untrusted text) | Asset owners, via the rights system or DAM | Adapter, then model | Live per call | Not stored beyond session events |
| Quotes | Advertiser | `get_quote` writes; owner reads | Booking system at `quoted_at`, with expiry | 90 days |
| Proposals, purchase requests | Advertiser; sales ops for state | `/confirm` creates; ops updates state | Authoritative for phase 1 | Kept as commercial records (O4) |
| Sessions | Advertiser user | ADK `DatabaseSessionService` | n/a | 90 days (Q12) |
| Usage counters | Service | Admission check | Per UTC day | 30 days |

Identities: end user (IdP `sub` and org), workload (Cloud Run service account
with Cloud SQL, Secret Manager and Vertex access), and the service credentials
for the rights and booking APIs. These are **service** credentials, so C2 is
enforced by our code, not by those systems (O2). In phase 1, only the engineer's
DB access can change request state.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| campaign_assistant | Yes (prices, the advertiser's requests) | Yes (asset descriptions written by owners) | No. The proposal creates no effect, confirmation is outside the agent (D2), and output is plain text | One leg removed. The adversarial case in G05/A5 and G06/A3 asserts it |

## Budgets and capacity

Workload assumption: 5 advertisers, at most 50 invocations each a day, at most
8 model calls each, which bounds the worst case at 2,000 model calls a day. The
expected load is far lower. Prices were not looked up because this session had
no network, so cost is symbolic: calls × (input + output tokens) × the Vertex
price on a date to be recorded in G02. Restart keeps usage counters (Postgres).
When the allowance is exhausted, new chats are refused, while status and
already-confirmed requests stay readable.

## Failure and recovery

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Existing IdP | G04/A4 | G04/A4 | n/a: read-only token verification | n/a: single verification step | G04/A4 | n/a: login volume is tiny | G04/A6 | G04/A5 |
| Rights system | G01/A3 | G03/A4 | n/a: read only | n/a: read only | G03/A4 | G03/A4 | n/a: read only | G03/A5, G05/A5 |
| Booking system (pricing, inventory read) | G03/A4 | G03/A4 | n/a: phase 1 reads only | n/a: phase 1 reads only | G03/A4 | G03/A4 | n/a: read only | G03/A5 |
| Booking system (order write, phase 2) | G08/A3 | G08/A3 | G08/A2 | G09/A1 | G08/A3 | G08/A3 | G08/A2 | G08/A3 |
| Cloud SQL (sessions, records) | G02/A2 | G05/A6 | G05/A6 | G05/A6 | G02/A2 | n/a: pilot volume is tiny | G05/A6 | G06/A3 |
| Vertex AI model | G01/A3 | G01/A3 | n/a: generation has no external effect | n/a: no multi-step effect | G02/A1 | G02/A3 | n/a: no effect to duplicate | G06/A3 |

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| Confirm purchase (creates purchase request) | G05/A3, G05/A9 | G05/A6 | G05/A2 | G05/A6 | G05/A6 |
| Sales ops places the order (phase 1, manual) | G05/A8, G05/A10 | G05/A8 | G05/A4, G05/A10 | G05/A8 | G05/A8 |
| Automated order placement (phase 2) | G08/A1 | G09/A1 | G08/A1 | G08/A2 | G08/A2 |

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Browser closes after Confirm and before the response | On return, status shows the request | The request row exists or not, and the transaction decides which | The user reopens status. Engineer if the row is missing |
| Rights revoked or narrowed (a territory or dates removed) between quote and confirm | "Rights changed, not requested", with the field | Proposal marked void, no request | User searches again |
| Rights narrowed between confirm and the ops export | Status "rejected: rights changed" | Request rejected at export, no order | Advertiser re-searches. Engineer runs the export (G05/A10) |
| Rights end mid-flight (grant ends before the flight ends) | Denied with the end date and an offer to shorten | Nothing stored | User chooses a shorter flight, which is a new quote |
| Rights revoked during a live flight, after placement | Nothing in the assistant | Order and delivery continue unless someone acts | Outside this system: rights and delivery teams (O11). The request's terms snapshot (C12) shows what was cleared |
| Quote expires before sales ops places the order | Status says "quote expired, please re-confirm" | Request rejected, no order | Advertiser re-confirms a new quote (G05/A4) |
| Sales ops places the order but forgets to set the state | Status says "awaiting placement" past one business day | Order exists in the booking system | Sales ops, through the daily list of requests older than one day (G05/A8) |
| Kill switch on during a chat | "Temporarily unavailable"; confirmed requests are kept | Requests remain for ops | Engineer turns the switch off |
| Model or ADK retirement during the pilot | None, because pins hold | n/a | Engineer. The calendar entry comes from the lifecycle table |
| Rollback | Previous revision serves; schema changes are additive only | DB rows kept | Engineer, through Cloud Run revision traffic |

## Verification and implementation handoff

The ladder: offline tests with fake rights and booking adapters and a scripted
model (G01, G03, G05), local tests against Postgres including restart (G02,
G05), bounded live checks against rights and booking staging and Vertex (G03,
G06), and a hosted staging run before go-live (G06). Benefit claims
(turnaround, support emails) are hypotheses measured in the pilot against the
baseline G06 records. Model quality, valid transactions and outcomes are
separate evidence. Release unit for phase 1: image digest, prompt file
hash, model ID and ADK pin, recorded in the deploy log (G02). Goals,
estimates, run prompts and the implementation map are in the
[plan](../plans/advertiser-campaign-assistant.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| O1: Do rights also depend on territory, dates, modification or approval? | **Resolved 2026-10-15:** territory, flight dates and modification, yes. Approval was not mentioned and is assumed not to apply | User | Closed; see revision 2 |
| O8: Date semantics (inclusive end, timezone) and territory scheme (ISO codes or regions) | Changes the boundary cases in `rights.evaluate`. Regions would need a region-to-country table | Rights team, through W12 | G03 (G01 proceeds on Q13 and Q14 and is adjusted if they differ) |
| O9: Is modification a yes/no flag or levels (resize, overlay, edit)? Do pilot campaigns need it? | Decides whether G13 is needed and how large it is | Rights team (W12) and pilot owner (W9) | G13 |
| O10: Does the rights API return grants, or offer a coverage check? | D11 alternative | Rights team, through W12 | G03 |
| O11: Who acts when rights are revoked during a live flight? | Out of the assistant's scope, but advertisers will ask | Rights and delivery owners | Nothing in phase 1 |
| O12: Do booking pricing and inventory take territories? | Quote shape | Booking team, through W2 | G03 |
| O2: Can the rights and booking APIs take a per-advertiser credential or on-behalf-of header? | Moves C2 enforcement partly into those systems | Rights and booking teams | Nothing; improves defence in depth |
| O3: How large is the asset catalogue per brand and channel? | Filter-then-rank versus a search index | Rights or DAM owner | Nothing below about 2,000 assets |
| O4: Retention of purchase requests and conversations under the commercial terms | Erasure design | Legal or commercial owner, through W6 | G06 go-live |
| O5: Booking replay key, lookup by client reference, timeout semantics | Selects the phase-2 write mode (C5) | Booking team, through W7, then G07 | G08, G09 |
| O6: Does sales ops accept the phase-1 manual placement (Q10)? | If not, the cut line moves (see the plan's what-if) | Sales ops lead, through W3 | G05 |
| O7: Does the security review (W4) need the built system as well as this design? | If yes, W4 follows G05, and go-live moves later | Security reviewer | G06, G12 |

## Revision 2 (2026-10-15): rights depend on territory, flight dates and modification

| Item | Before | After | Removed or weakened? |
| --- | --- | --- | --- |
| C1 | Owner, brand, channel; rechecked at quote and confirm | All six fields through one function; also rechecked at the ops export; no search before territory and dates are known | Strengthened |
| C4 | Assets, dates, price | Adds territories and use (as-is) | Strengthened |
| C12 | — | New: the terms snapshot travels with the request, and placement must match it | Added |
| D8 | Brand and channel query | Grant records filtered by territory and flight | Revised |
| D11, D12 | — | New: one coverage function; as-is only in phase 1 | Added |
| Modification requests | Not modelled | Explicitly deferred to G13, and the pilot is as-is only | **Scope narrowed:** advertisers cannot request modified creatives in phase 1. The rights floor is kept, because no modified use is ever cleared |
| Failure scenarios | One rights-change row | Four rows (narrowed at confirm, narrowed before export, ends mid-flight, revoked during a live flight) | Strengthened. The last row is out of scope (O11) |
| Grid cells | Rights row cites G03/A5 for malformed payloads | Same cell; G03/A5 now also covers malformed dates and territory codes | None removed |
| Open decision O1 | Open | Resolved by the user | Closed |
| C7 (after the independent review) | Behaviour at confirm and export during a rights outage was undefined | Refuse at confirm; hold (neither listed nor rejected) at export | Strengthened |
| Q14 (after the independent review) | ISO codes only | ISO codes plus an alias table ("UK" → GB); an unmapped name asks rather than returning an empty search | Strengthened |
| Ops export | Engineer-run CLI | Cloud Run job from the service image, so the rights recheck reaches the rights API | Revised |
