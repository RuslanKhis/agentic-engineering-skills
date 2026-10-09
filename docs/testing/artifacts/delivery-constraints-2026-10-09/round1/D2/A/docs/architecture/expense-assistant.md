# System design: Finance expense assistant (ADK)

Status: **draft**. Every product decision below is provisional because no user
answers were available (headless run, 2026-10-09). Rows marked *(A#)* depend on the
Assumed answers table. Nothing here has been accepted by the user.

Implementation plan: [docs/plans/expense-assistant.md](../plans/expense-assistant.md)

## Assumed answers

The user could not be asked. Each answer below is an assumption; the listed
decisions are provisional until it is confirmed.

| # | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Time and money: is "two engineers, half-time, three weeks" the whole budget, and is there a cloud/model spend limit? | ~15 engineer-days total. Spend: no fixed limit, but pilot running cost should stay in the "tens of USD per month" range (illustrative). | Size of the plan; D7 budgets; deferred controls |
| A2 | Who judges the result and what will they read? | The finance team lead (product owner) judges a **running service** used by the 40-person team, plus a one-page evaluation summary. | G01 measurement; G05 pilot review |
| A3 | Artifact type? | **Pilot** (internal, 40 users) that may become a production service later. | Depth of controls; deferred-control list |
| A4 | Does "an employee's own claims" mean each signed-in finance-team member sees only claims where they are the claimant? Do finance staff need to look up *other* employees' claims (e.g. as approvers)? | Own claims only. No approver or on-behalf lookups in the pilot. | D3, D4, invariant I1 |
| A5 | Is the assistant read-only, or should it submit, edit or approve claims? | Read-only. No writes to the expense database. | D4; no operation/idempotency machinery; security posture |
| A6 | Where does the PostgreSQL expense database run, and can we get a read-only role? | Cloud SQL for PostgreSQL in the company's GCP organisation; the DBA can create a read-only role limited to a view. | D5, D6, G02/G04 prerequisites (discovery Q1) |
| A7 | How is a Google Workspace identity linked to an employee row? | The expense DB has an `employees` table with a unique, verified work-email column matching the Workspace primary email. | D3, invariant I1 (discovery Q2) |
| A8 | Where are the expense policies, how big, who owns them, how often do they change? | A handful of Google Docs/PDFs, ≲ 30 pages (~20k tokens) total, owned by the finance team lead, changed a few times a year. | D2 (policy in context vs retrieval) |
| A9 | Any data-residency or vendor constraint on sending claim data to a model? | Vertex AI Gemini in a single EU or US region chosen by the org is acceptable; no residency beyond that. | D6 model/backend, region |
| A10 | What UI do people expect — web page, Google Chat, Gemini Enterprise? | A minimal internal web page. Google Chat is a later option. | D8, G03 |
| A11 | How long may conversations (which contain claim details) be retained? | 30 days, then deleted. Users need no conversation history beyond that. | D5 session retention |
| A12 | What does "good" mean for policy answers, and is there a baseline (e.g. emails/tickets to finance)? | Correct, cited answers on a labelled set written by the finance lead; baseline = current count of policy questions emailed to the finance inbox (to be measured). | G01 acceptance, G05 |

## Purpose and constraints

**Users:** 40 finance-team employees, signing in with Google Workspace.

**Running journey.** Aigerim, a finance analyst, returns from a client trip. She
wants to know whether a €65 team dinner is reimbursable and whether last month's
taxi claim was paid. Today she searches the policy PDF and opens the expense
system, filtering her claims by hand, or emails the finance inbox. Intended
outcome: in one chat she gets (a) the policy answer with a section citation
and (b) the status of *her* taxi claim, read live from PostgreSQL. She can never
see a colleague's claim, even if she asks for one by ID.

**Fixed constraints (given):** ADK (Python), Google Workspace sign-in, existing
PostgreSQL expense database, ~15 engineer-days. **Non-goals:** submitting,
editing or approving claims; looking up other employees' claims; analytics
across the team; general finance chat.

**Model contributes:** interpreting the question, choosing between policy text
and claim lookup, choosing filter arguments, composing a cited answer.
**Ordinary code controls:** who the user is, which employee's claims can be read,
which SQL runs, which columns leave the database, how many rows and model calls
are allowed, and which policy version is served.

Observed facts: the repository is empty apart from `.claude/skills` (inspected
2026-10-09). There is no existing code, manifest, pin or doc convention, so this
design uses `docs/architecture/` and `docs/plans/`.

## Scope, evaluator and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| Time and money available | ~15 engineer-days (2 × 50 % × 3 weeks) *(A1)*; pilot spend kept small, no hard cap given |
| Who judges the result and what they read | Finance team lead; a running internal service plus a one-page evaluation summary *(A2)* |
| Artifact type | Pilot *(A3)* |

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Vector/RAG retrieval for policies | Assumed corpus fits in the prompt (D2) | Corpus > ~50k tokens, or measured citation accuracy below target |
| Postgres row-level security in addition to the scoped view | Code-level scoping (D4) plus a column-limited view is enough for a read-only 40-user pilot | Approver/on-behalf access (A4 changes), a second app using the role, or a security review asking for it |
| Model Armor / Sensitive Data Protection screening | No free-text egress, column minimisation and owner-only data; adds cost and latency | Bank/IBAN or health data in scope, or a broader audience |
| Response streaming (SSE) | Answers are short; buffered JSON is simpler to secure | Measured p95 time-to-answer > ~8 s |
| Durable per-user budgets / shared admission store | 40 users; per-turn `max_llm_calls` and a Cloud Run instance cap bound spend | Spend anomaly, or audience beyond the finance team |
| Online monitors, BigQuery agent analytics, eval-set refresh from production | Pilot volume is low; manual weekly review of feedback is enough | Production decision after G05 |
| Canary/traffic-split releases | One small user group; Cloud Run revision rollback is enough | Production |
| Google Chat / Gemini Enterprise surface | Web page is fastest to secure *(A10)* | User demand in pilot feedback |

## Guarantees and acceptance

| Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| **I1** A signed-in user only ever sees claims where they are the claimant. | `identity` middleware verifies the IAP JWT, maps email → `employee_id` from the expense DB; claim tools read `employee_id` from server-set session state, never from model arguments; SQL has `WHERE claimant_id = %(employee_id)s` bound by code. | Request for another's claim returns "not found among your claims" (no existence oracle). | Offline: scripted-model test calls `get_my_claim` with another employee's claim ID → empty result, SQL param = caller's ID. Prompt-injection case in a claim description. Local: two fixture users. |
| **I2** Unauthenticated or non-Workspace requests reach no agent or data. | IAP on the load balancer + Cloud Run ingress `internal-and-cloud-load-balancing` + app-side JWT audience check. | 401/403 before Runner. | Offline: missing/forged/wrong-audience JWT → 401, Runner never invoked. Hosted (G04): direct `run.app` URL refused. |
| **I3** A conversation is readable only by its owner. | Session `user_id` = verified IAP subject; API looks sessions up by `(app, user_id, session_id)` only. | 404 for others' session IDs. | Offline API test with two users. |
| **I4** Policy answers cite a section of the currently published policy version, or say the policy does not cover it and point to the finance inbox. | Instruction contract + policy bundle with section IDs and `policy_version`; answer schema includes `citations`. | "Not covered" answer, never an invented rule. | G01 labelled set: citation correctness ≥ 90 % and zero invented rules on "not covered" cases *(provisional target, A12)*. |
| **I5** "No claims" is only said when the query succeeded and returned zero rows. | Tool result has `status: ok / empty / unavailable / truncated`. | DB down → "I can't reach the expense system right now". | Offline: DB error fixture → `unavailable`, answer contains no "you have no claims". |
| **I6** No write to the expense DB is possible from the assistant. | DB role has `SELECT` on one view only; tools issue fixed SELECTs. | Permission error, logged. | G02: role grant review; test that the role cannot `INSERT`/`UPDATE` (fixture DB). |
| **I7** Per turn: ≤ 6 model calls, ≤ 50 claim rows returned to the model. | `RunConfig.max_llm_calls`, tool-side `LIMIT 51` + truncation flag. | Turn ends with an honest "too many steps / narrow your filter". | Offline: scripted loop hits the cap; 200-row fixture returns 50 + `truncated`. |

## Architecture and decisions

```text
Browser (Workspace user)
   │ HTTPS
   ▼
External HTTPS LB + IAP ──(Google Workspace OIDC; only @company.com group "finance-assistant-users")
   │ x-goog-iap-jwt-assertion
   ▼
Cloud Run service "expense-assistant"   (service account: sa-expense-assistant)
  ├─ FastAPI app
  │    ├─ identity middleware: verify IAP JWT → email → employee_id (expense DB)
  │    ├─ /api/sessions, /api/chat  (owner-scoped)
  │    └─ static minimal chat page
  ├─ ADK Runner(App) ── LlmAgent "expense_assistant"
  │    ├─ instruction: rules + policy bundle vN (static, cacheable prefix)
  │    ├─ tool list_my_claims(status?, date_from?, date_to?, text?)   [read]
  │    └─ tool get_my_claim(claim_ref)                                 [read]
  ├─ DatabaseSessionService ──► Cloud SQL Postgres, DB "expense_assistant" (sessions, 30-day TTL)
  └─ claims repository ──► existing expense Postgres, role expense_assistant_ro, view v_assistant_claims
       │
Vertex AI Gemini (gemini-3.5-flash, chosen region) ◄── model calls from Runner
Cloud Trace / Logging (metadata only, no prompt/response content)
```

Sequence for the running journey: IAP authenticates → middleware verifies JWT,
resolves `employee_id` (cached 5 min) → API loads or creates the session owned by
`sub`, writes `employee_id` into session state as an app-only key → Runner calls
Gemini with instruction + policy text → model answers the dinner question from
the policy and calls `list_my_claims(text="taxi", date_from=…)` → tool runs a
fixed parameterised SELECT scoped to state `employee_id` → bounded result → model
composes answer → API returns final text + citations as JSON.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Interpret questions over two small capabilities *(A4, A5)* | **One `LlmAgent` with two read tools**; policy in instruction. No sub-agents. | One judgment, one data scope, no write path: nothing for a second agent to own. | Router + policy agent + claims agent adds routing errors and handoffs for no new boundary. | G01/G02 eval cases cover tool choice. |
| D2 | Cited, current policy answers *(A8)* | **Policy bundle in the instruction**: policy docs exported to Markdown with stable section IDs, versioned in the repo, rendered into a static instruction prefix. | ~20k tokens fits easily; highest recall; no retrieval infra; stable prefix enables context caching. | Every call pays policy tokens (mitigated by caching); doesn't scale past ~50k tokens → RAG then. | Rendered-request test shows one policy version; G01 citation score. |
| D3 | User = employee, from Workspace *(A7)* | **IAP** for sign-in; app verifies the IAP JWT and maps verified email → `employee_id` by lookup in the expense DB. | IAP gives Workspace SSO with no app OAuth code; JWT check stops header spoofing. | Ties hosting to an HTTPS LB (small fixed cost); alternative: app-run Google OIDC flow (more code, own session cookies). | I2/I3 tests; unmapped email → policy-only mode with a clear message. |
| D4 | Own claims only, read-only *(A4, A5)* | **Two fixed parameterised queries** (no text-to-SQL) over a column-limited view; `employee_id` from trusted session state via `ToolContext`, never a tool parameter. | The model cannot express "another employee" at all; the whole query surface is reviewable. | Less flexible than generated SQL (no ad-hoc analytics) — a non-goal. | I1, I5, I6 tests. |
| D5 | Conversations survive instance restarts; 30-day retention *(A11)* | **`DatabaseSessionService`** on a **separate** small Cloud SQL Postgres database `expense_assistant`; nightly delete of sessions older than 30 days. | Cloud Run can run >1 instance; never writes into the business DB. | A second database to run; alternative `InMemorySessionService` + `max-instances=1` loses chats on deploy. | Local restart test (G03); deletion job test. |
| D6 | Model with known lifecycle; residency *(A9)* | **Vertex AI `gemini-3.5-flash`**, pinned, in the org's chosen region; temperature low (0.2), default thinking. | ADK 2.8.0 default model; stable; Vertex retirement "2027-05-19 or later" (lifecycle table checked_on 2026-10-08) — beyond the pilot. `gemini-3.8-flash` (newest, no Vertex retirement date in the table) is the candidate for a later side-by-side. | Avoid 3.6-flash (Vertex retirement 2026-11-19) and 2.5-* (2026-10-20). | G01 confirms the ID is available in the region; release manifest has no alias. |
| D7 | Bounded spend and loops | `RunConfig.max_llm_calls=6`; tool row cap 50; Cloud Run `max-instances=3`, concurrency 20; one in-flight turn per session (reject overlap with 409). | 40 users never need more; caps bound runaway cost without a control store. | No per-user daily budget (deferred). | I7 tests; G04 load smoke of 20 concurrent turns. |
| D8 | Simple, safe UI *(A10)* | Minimal static page + JSON API returning the **final** response only (no raw event forwarding); markdown rendered with images and remote links disabled. | Prevents leaking tool args/diagnostics and image-URL exfiltration. | No token streaming (deferred). | API contract test: response contains only `text`, `citations`, `status`. |
| D9 | Hosting | **Cloud Run** + external HTTPS LB + IAP. | Fits a FastAPI wrapper, Cloud SQL connector, IAP; team-friendly. | Agent Runtime: managed sessions but per-user IAP identity propagation to our DB is more work; GKE: too heavy for 15 days. | G04 deployment readback. |

Versions: working assumption **google-adk 2.8.0** (the version every installed
specialist's `references/compatibility.md` was checked against). Confirming the
interfaces used (`App`, `Runner`, `RunConfig.max_llm_calls`,
`DatabaseSessionService`, `ToolContext.state`, `output_schema` with tools on the
Vertex variant) against the chosen pin is an acceptance item of G01. Region,
Cloud SQL tier, IAP setup and Gemini prices were **not** looked up (no network in
this session) and remain provisional.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | Owns: answer expense-policy questions only from the bundled policy, cite section IDs, say "not covered — contact finance inbox" otherwise; use tools for the user's own claims; never claim to see others' data. Stays in code: identity, employee ID, date "today", row limits, policy version. | `adk-agent-instructions`; rendered-request snapshot test |
| Tools (2, both read tier) | `list_my_claims(status: enum?, date_from: date?, date_to: date?, text: str?)` → `{status, claims:[{claim_ref, date, merchant, amount, currency, category, state, last_updated}], truncated}`; `get_my_claim(claim_ref: str)` → `{status, claim?}` with line items. No employee parameter. Errors are actionable dicts (`invalid_date`, `unavailable`). | `adk-tool-interface-design`; declaration dump + size check |
| Output | `output_schema`: `{answer: str, citations: [section_id], used_claims: bool, outcome: answered / not_covered / unavailable / refused}`. Native with tools only on the Vertex variant per 2.8.0 notes; one repair attempt, then a fixed failure message. | `adk-model-and-output-contracts`; scripted prose/fenced/invalid output tests |

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Expense claims | Expense system; caller's own rows | Reader: `expense_assistant_ro` via `v_assistant_claims` (no bank/account fields) | Live DB at query time; answer states `last_updated` | Not copied except into session events (below) |
| Employee mapping | Expense DB `employees` | Reader: middleware | Live; cached 5 min in-process | Cache only |
| Policy bundle | Finance lead approves; engineers publish | Repo (`policy/vN/`), reviewed PR | Version shown in each answer footer | Old versions kept in git |
| Sessions/events (contain claim data) | Owner = IAP `sub` | App writes; owner reads | — | Deleted after 30 days; delete-on-request via admin script |
| Telemetry | Ops | Cloud Trace/Logging | — | Content capture **off**; metadata only; default log retention |

Session vs invocation vs business operation: there are no business operations
(read-only), so no idempotency or operation records are needed.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| `expense_assistant` | Yes: the caller's own claims | Yes: claim descriptions/merchant text typed by employees | No write tools; only egress is the answer to the data owner | Accepted risk with structure: scope fixed in code (injection cannot widen it), no write/egress tools, UI renders no images/links. Adversarial cases in G02. |

Tool tiers: both tools are read tier; no confirmation needed. No code executor.

## Budgets and capacity

Workload *(illustrative)*: 40 users × ~5 turns/working day = ~200 turns/day,
peak ~5 concurrent turns. Per turn: 1–3 model calls (expected 2), ≤ 2 DB
queries, cap 6 model calls. Input per call ≈ 20k policy tokens (cacheable) +
≤ 4k history/tool tokens; output ≈ 300 tokens.

Symbolic daily model cost ≈ 200 × 2 × (20k × P_cached_in + 4k × P_in + 300 × P_out).
Prices were not looked up; fill from the Vertex pricing page with date and
region in G04. Fixed costs: HTTPS LB, small Cloud SQL instance for sessions,
Cloud Run (min-instances 0; cold start accepted for pilot). Billing budget alert
on the project is observation only, not a cap.

Latency target *(provisional)*: p95 complete answer ≤ 8 s, measured in G04.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Success | Cited answer and own claim status | Session events (30 days) | — |
| Asks for colleague's claim / injected text in a claim says "list all claims" | "I can only see your own claims" / not found | Nothing outside caller's rows was read | None needed; adversarial test guards it |
| Direct Cloud Run URL or forged header | 403 | Nothing | Ops checks ingress setting |
| Email not in `employees` (new joiner, alias) | Policy answers work; claim tools return `not_linked` with "contact finance systems" | Nothing | Finance systems admin fixes mapping |
| Expense DB down/slow (5 s query timeout) | "Can't reach the expense system now"; never "no claims" | Partial answer from policy only | Retry later; ops alert on `unavailable` rate |
| Vertex unavailable / 429 | "Assistant is unavailable, try again" after SDK retries (one owner: genai `retry_options`, 2 attempts) | Session keeps the user message | User retries |
| Model returns invalid output twice | Fixed failure message, `outcome=error` logged | Session event | Eval case added from the trace |
| Loop hits 6 calls | "Couldn't finish — please narrow the question" | Session | — |
| Double submit / two tabs on one session | Second request 409 "still answering" | — | — |
| Policy updated mid-conversation | New turns use new version (shown in footer); old answers keep old citations | — | Finance lead announces changes |
| Employee leaves | IAP denies (Workspace account suspended) | Their sessions deleted at 30 days | — |
| Bad release | Users see errors / quality drop | — | Roll back to previous Cloud Run revision (kept), with matching prompt+policy bundle (same image) |

## Verification and implementation handoff

- **Offline deterministic** (G01–G03): scripted-model Runner tests for I1, I3,
  I5, I7, output repair; FastAPI tests for I2/I3; fixture Postgres for queries.
- **Local integration:** process restart keeps a session (D5); two fixture users.
- **Bounded live:** G01 runs the labelled set against Vertex with a call cap,
  once authorised; G04 hosted smoke and 20-turn concurrency check.
- **Outcome measurement** (hypothesis, not a technical claim): fewer policy
  emails to the finance inbox and pilot satisfaction ≥ 4/5, guardrail: no
  reported wrong-policy answers that led to a rejected claim. Baseline must be
  counted before launch (A12).
- **Observability (pilot depth):** ADK OpenTelemetry → Cloud Trace with content
  capture off; one telemetry owner (the app); SLIs: answered-without-error
  ratio, tool `unavailable` ratio, p95 latency, tokens per turn; thumbs up/down
  stored with session ID. Alert owner: the two engineers.
- **Release bundle:** image digest, prompt version, policy version, model ID,
  tool-schema hash, eval-set hash, recorded in `release.json` in the image.
  Gate: offline tests + labelled-set threshold. Rollback unit: Cloud Run
  revision (previous one kept for 14 days).

Goals G01–G05 and discovery questions are in the
[implementation plan](../plans/expense-assistant.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| A4: do finance staff need others' claims (approver view)? | Turns I1 into role-based scope; adds RLS and audit | Finance lead | Nothing now; would reshape G02 |
| A6: DB location, network path and read-only role | Cloud SQL connector vs VPC/peering; who creates the view | DBA / platform team (discovery Q1) | G02 live data, G04 |
| A7: email ↔ employee mapping column | I1 depends on it | DBA (discovery Q2) | G02 live data |
| A8: policy corpus size/format | > 50k tokens switches D2 to retrieval | Finance lead provides docs | G01 |
| A9: region / residency | Model and Cloud SQL region | Security/compliance | G04 |
| A11: retention of chats containing claim data | Session TTL, deletion job | Finance lead + privacy | G03 deletion job |
| Prices and region availability of `gemini-3.5-flash` | Cost estimate, D6 | Engineer, Vertex docs, dated | G04 |
