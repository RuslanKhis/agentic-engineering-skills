# Implementation plan: advertiser campaign assistant (pilot)

Status: draft, revision 2 (2026-10-15): rights now also depend on territory, flight dates and modification permission. G00 (a human task) and G01 are ready; G02 waits for W2a and W2c. Both revisions were independently reviewed; findings are settled under "Schedule changes".
Architecture: [docs/architecture/campaign-assistant.md](../architecture/campaign-assistant.md)
Continuation source of truth: this plan

## Summary for the reader

- **Profile and phase 1:** MVP/pilot. Phase 1 lets five advertisers sign in
  with the existing IdP, find assets their brands may use on a channel, get
  live quotes, and confirm order requests that booking operations enter by
  hand (design D5). Only assets covered for the exact territory, whole
  flight and declared modification intent are offered (design D10).
  Direct ordering is phase 2.
- **Effort and finish:** phase 1 is 57.5–86 human hours against 67.5 h
  of capacity after a 25 % reserve (one engineer, 6 focused h/day, 15
  working days). Go-live finishes in 16–28.56 working days. **Three weeks
  no longer fits, even at the low end.** Revision 2 adds 9–14.5 h in
  total (the new rights terms in D10 plus the review's additions) and
  outside waits: the rights semantics (W2c) and the rights team's rule
  review (W5). The revision 2
  review added prerequisites the schedule had missed: the sign-off now
  follows the runbook, the day-1 requests are their own step, ops and
  planners must be available, and there are hours for rule corrections.
  **A committed go-live date needs 29 working days** (about six weeks;
  helper: fits at 29, exit 0). The longest chain is outside waits plus the
  rights, quote, ordering and hosting goals. No single remedy we tested
  closes the gap to 15 days (see "Schedule changes").
- **Cut line (confirm or move):** phase 1 = G00–G10 and G16: sign-in,
  search licensed for the exact territory, flight and modification
  intent, live quotes, confirmed order requests that booking ops enter
  (D5), hosted pilot. Phase 2 = G11–G15: direct ordering, traces, CI gate,
  adversarial suite. If time runs out, goals stay useful in order: G01–G04
  (local search on exact terms and quotes, on fixtures), then G06 (local ordering), then
  G08 (hosted).
- **Largest risks:** (1) The rights team cannot settle territory, date
  and modification semantics quickly (W2c) or corrects the rules heavily
  (W5, G16). A wrong coverage rule would show unlicensed assets, so the
  rehearsal and go-live wait for the confirmed rules; this is a safety
  gate, not the date-setter. (2) The sign-off (W3) takes its full 5 days;
  book the meeting on day 1 (G00). (3) Booking replay behaviour stays
  unknown, so G12 cannot promise duplicate protection; G11 bounds the
  investigation.
- **Decisions needed from you:** accept a go-live window of day 16–29
  (commit to day 29) or set another date; confirm the rights semantics
  assumed in Q12–Q15; confirm the cut line (D5);
  confirm the assumed answers Q1–Q11 in the design, especially Q2 and Q7.
- **Next step:** do G00 (send the day-1 requests) yourself, then
  `/adk-engineer Carry out G01 from docs/plans/campaign-assistant.md.`

## Destination and constraints

Destination: the journey in the design, run by the five pilot advertisers.
Non-goals and accepted stack: see design §Purpose and D1–D9. Authorization:
design only; no repository code, cloud resources or credentials exist yet.
Inherited pins: model `gemini-3.8-flash` (D7), ADK `google-adk==2.8.0` as the
working assumption (confirmed in G01/A1), prompt version `v1`. Proposed
layout (greenfield, unverified):

```text
app/main.py            FastAPI: OIDC middleware, /chat, /proposals, /ops
app/agent.py           App + LlmAgent factory, RunConfig
app/tools/rights.py    search_assets; RightsClient
app/rights_coverage.py rights_coverage pure function; region table (D10)
app/tools/booking.py   get_quote; BookingClient
app/tools/orders.py    propose_order; confirm service (not a tool)
app/ledger.py          proposals, order_requests, usage counters (Postgres)
tests/                 offline fakes, scripted-model tests, eval set
```

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Pilot: sign-in, licensed search on exact rights terms, quotes, confirmed requests entered by ops, go-live | G00–G10, G16 | 57.5–86 | 1 × 6 h × 15 days = 90 h; 25 % reserve → 67.5 h (no); 29 days → 130.5 h |
| 2, graduate | Direct ordering, traces, CI gate, adversarial suite | G11–G15 | 27.5–43.5 | When the pilot is running |

Estimates include a 1.5× multiplier for an engineer new to ADK (Q2), applied
to every goal, hands-on and review alike. Calendar waits are schedule
entries W1–W7 (W1 belongs to phase 2). G00 sends or books all of them on day 1.
W5 can only conclude after G02 writes the rule table, W7 after G08, and W3
after the G08 rehearsal and the G09 runbook.

```yaml
- goal: G00
  phase: 1
  hands_on: 0.5
  review: 0
  total: 0.5
  owner: Engineer
  blocked_by: []
  mentions_only: [wait]
- goal: W1
  phase: 2
  total: 0
  calendar_waits: booking team answers replay, status-lookup, client-reference and order-note search questions
  wait_days: 3-8
  blocked_by: [G00]
- goal: W2a
  phase: 1
  total: 0
  calendar_waits: rights and booking read API documentation or sample payloads, IdP discovery document and claim names
  wait_days: 1-3
  blocked_by: [G00]
- goal: W2b
  phase: 1
  total: 0
  calendar_waits: access request for IdP OIDC client with local and hosted redirect URIs, pilot test account, rights read credential, booking staging and production read credentials, a staging inventory item for the test org, GCP project with approval for project, region and resources, billing budget access
  wait_days: 2-5
  blocked_by: [G00]
- goal: W2c
  phase: 1
  total: 0
  calendar_waits: rights semantics from the rights team (Q12-Q15: territory codes and region groups, markets spanning time zones, licence-window dates, modification flag values, how records combine, whether the rights system evaluates coverage itself); booking market codes and date granularity; an agreed test org, brand and rights record that line up with the W2b staging inventory
  wait_days: 2-5
  blocked_by: [G00]
  mentions_only: [W2b]
- goal: W4
  phase: 1
  total: 0
  calendar_waits: signed-off org-to-brand list from the business owner, plus the account managers' current turnaround figures
  wait_days: 2-5
  blocked_by: [G00]
- goal: W5
  phase: 1
  total: 0
  calendar_waits: rights team confirms the coverage rule table from G02/A8 and gives expected answers for three real records
  wait_days: 1-3
  blocked_by: [G02]
- goal: W6
  phase: 1
  total: 0
  calendar_waits: five pilot planners named by the advertisers, their IdP accounts provisioned, go-live session booked
  wait_days: 3-8
  blocked_by: [G00]
- goal: W7
  phase: 1
  total: 0
  calendar_waits: a booking-operations person's session on hosted staging
  wait_days: 1-2
  blocked_by: [G08]
- goal: W3
  phase: 1
  total: 0
  calendar_waits: pilot go-live sign-off by business owner and booking-operations lead, on the G08 rehearsal and the G09 runbook
  wait_days: 2-5
  blocked_by: [G08, G09]
- goal: G01
  phase: 1
  hands_on: 2.5-3.5
  review: 1-1.5
  total: 3.5-5
  owner: Engineer
  blocked_by: []
  mentions_only: [G00]
- goal: G02
  phase: 1
  hands_on: 5.5-8
  review: 3-4.5
  total: 8.5-12.5
  owner: Engineer
  blocked_by: [G01, W2a, W2c]
  mentions_only: [G03, G05, W5, wait]
- goal: G03
  phase: 1
  hands_on: 6-8.5
  review: 3-4.5
  total: 9-13
  owner: Engineer
  blocked_by: [G01, W2a]
  mentions_only: [G05, G06]
- goal: G04
  phase: 1
  hands_on: 3-4.5
  review: 1.5-2
  total: 4.5-6.5
  owner: Engineer
  blocked_by: [G02]
  mentions_only: [G05, W2c]
- goal: G05
  phase: 1
  hands_on: 2.5-3.5
  review: 0.5-1
  total: 3-4.5
  owner: Engineer
  blocked_by: [G02, G03, G04, W2b, W5]
- goal: G06
  phase: 1
  hands_on: 8-11
  review: 3.5-5
  total: 11.5-16
  owner: Engineer
  blocked_by: [G03, G04]
  mentions_only: [G12]
- goal: G07
  phase: 1
  hands_on: 4-5.5
  review: 0.5-1
  total: 4.5-6.5
  owner: Engineer
  blocked_by: [G04, G06, W2b]
  mentions_only: [G14]
- goal: G08
  phase: 1
  hands_on: 6-8.5
  review: 2-3
  total: 8-11.5
  owner: Engineer
  blocked_by: [G05, G06, G16]
  mentions_only: [G13, W3, W5]
- goal: G09
  phase: 1
  hands_on: 2.5-4
  review: 0.5-1
  total: 3-5
  owner: Engineer
  blocked_by: [G07, G08, W4, W7]
  mentions_only: [W3, W1]
- goal: G10
  phase: 1
  hands_on: 0.5-1
  review: 0
  total: 0.5-1
  owner: Engineer
  blocked_by: [W3, G09, W6]
  mentions_only: [W5]
- goal: G16
  phase: 1
  hands_on: 0.5-3
  review: 0.5-1
  total: 1-4
  owner: Engineer
  blocked_by: [W5]
- goal: G11
  phase: 2
  hands_on: 2-3.5
  review: 1-1.5
  total: 3-5
  owner: Engineer
  blocked_by: [W1, G10]
- goal: G12
  phase: 2
  hands_on: 8.5-12.5
  review: 4-6
  total: 12.5-18.5
  owner: Engineer
  blocked_by: [G11]
- goal: G13
  phase: 2
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Engineer
  blocked_by: [G10]
- goal: G14
  phase: 2
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Engineer
  blocked_by: [G10]
- goal: G15
  phase: 2
  hands_on: 3-6
  review: 1-2
  total: 4-8
  owner: Engineer
  blocked_by: [G12]
```

Schedule check, run 2026-10-15:
`python3.12 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/campaign-assistant.md --design docs/architecture/campaign-assistant.md --phase 1 --days 15 --reserve 0.25 --person "Engineer=6"`.
Result (revision 2, after its review): 57.5–86 h of 67.5 h (low end only);
longest chain G00 → W2c → G02 → G04 → G06 → G08 → W7 → G09 → W3 → G10,
13.11–23.78 working days; finish 16–28.56 working days of 15 (no); exit 1.
With `--days 29`: fits, exit 0. Every review mention is settled as `mentions_only` after
checking both directions; the grid check passes.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 | `App` + `LlmAgent` in `app/agent.py`; Runner invoked from `/chat` | Vertex AI endpoint | `adk-workflow-design` | ADK 2.8.0 constructor names (G01/A1) |
| D2, D3 | Middleware writes `user_id`, `org_id`, `brands` to session state at session creation and every turn; tools read only state | — | `adk-tool-auth-and-secrets` | Rights API semantics (W2a docs, W2b live) |
| D4 | `BookingClient.quote` with deadline and one retry on 5xx/timeouts for reads | Secret Manager | `safe-api-tool-calls` | Booking read API contract (W2a docs, W2b staging) |
| D5 | `propose_order` tool + `ConfirmService` called by `POST /proposals/{id}/confirm`; Postgres unique constraint | Cloud SQL | `safe-api-tool-calls` | — |
| D6 | OIDC code flow in FastAPI; static page | Cloud Run | `adk-frontend-integration` | IdP client registration (W2b) |
| D7, D8 | `DatabaseSessionService` on Postgres; release manifest | Cloud Run, Cloud SQL, Secret Manager | `deploy-adk-on-google-cloud` | Lifecycle and prices re-read (G08) |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G00 Day-1 requests (human task) | 1 | action | 0.5 | — | none | ready |
| G01 Local agent on fakes | 1 | impl | 3.5–5 | — | adk-workflow-design | ready |
| G02 Rights adapter, coverage rules and scope | 1 | impl | 8.5–12.5 | G01, W2a, W2c | adk-tool-auth-and-secrets | blocked: W2a, W2c |
| G03 Sign-in, page, session ownership | 1 | impl | 9–13 | G01, W2a | adk-frontend-integration | blocked: W2a |
| G04 Quote tool | 1 | impl | 4.5–6.5 | G02 | safe-api-tool-calls | proposed |
| G05 Live integration check | 1 | impl | 3–4.5 | G02, G03, G04, W2b, W5 | safe-api-tool-calls | blocked: W2b, W5 |
| G06 Proposal, confirm, ops queue | 1 | impl | 11.5–16 | G03, G04 | safe-api-tool-calls | proposed |
| G07 Evaluation set | 1 | impl | 4.5–6.5 | G04, G06, W2b | adk-agent-evaluation | proposed |
| G08 Pilot environment and rehearsal | 1 | impl | 8–11.5 | G05, G06, G16 | deploy-adk-on-google-cloud | proposed |
| G09 Pilot readiness | 1 | impl | 3–5 | G07, G08, W4, W7 | adk-operational-guardrails | proposed |
| G10 Go-live | 1 | impl | 0.5–1 | W3, G09, W6 | deploy-adk-on-google-cloud | blocked: W3 |
| G16 Coverage rule corrections | 1 | impl | 1–4 | W5 | adk-tool-auth-and-secrets | blocked: W5 |
| G11 Booking contract discovery | 2 | discovery | 3–5 | W1, G10 | safe-api-tool-calls | blocked: W1 |
| G12 Direct order submission | 2 | impl | 12.5–18.5 | G11 | safe-api-tool-calls | proposed |
| G13 Traces and cost | 2 | impl | 4–6 | G10 | adk-agent-observability | proposed |
| G14 CI evaluation gate | 2 | impl | 4–6 | G10 | adk-release-engineering | proposed |
| G15 Adversarial suite | 2 | impl | 4–8 | G12 | adk-agent-security | proposed |

If time runs out early, the order G01–G04, G06, G08 leaves a working, safe
slice at each step (G06 without G08 is a locally demonstrable product).

### G00 — Day-1 requests (human task)

- **Phase and estimate:** 1; hands-on 0.5, review 0, total 0.5; owner Engineer
- **Outcome:** every outside wait starts on day 1.
- **Scope:** send the W1, W2a, W2b, W2c, W4 and W6 requests with the contents listed in the schedule block; book the W5 rule review for about day 4 and the W3 sign-off meeting; ask booking ops to hold a staging session (W7).
- **Primary skill:** none; this is a human task, not agent work.
- **Supporting skills:** none
- **Acceptance:**
  - A1 each request is sent with a named contact and a date, and recorded in this plan.
- **Status and evidence:** planned.

### G01 — Local agent on fakes

- **Phase and estimate:** 1; hands-on 2.5–3.5, review 1–1.5, total 3.5–5; waits none; owner Engineer
- **Outcome and linked decisions:** a local agent answers "licensed assets for my brand on channel X" against fake rights data; D1, D2, D7.
- **Scope:** `App`, `LlmAgent`, `search_assets` against an in-memory fake, `RunConfig(max_llm_calls=8)`, instruction v1, pinned model. Installing google-adk in the project environment is part of this goal; the day-1 requests are G00. Excludes real APIs (G02).
- **Depth:** pilot depth for orchestration and budgets; no persistence yet.
- **Implementation route:** `app/agent.py`, `app/tools/rights.py` with a `RightsClient` protocol and a fake; trusted state set by a test fixture.
- **Prerequisites:** none.
- **Primary skill:** adk-workflow-design
- **Supporting skills:** adk-tool-interface-design (tool declaration and result shape), adk-agent-instructions (instruction v1), adk-model-and-output-contracts (model pin, error handling)
- **Acceptance:**
  - A1 the installed ADK version is recorded and every interface used is checked against it (assumed 2.8.0).
  - A2 a rendered model request shows the instruction and three-or-fewer tool declarations; `search_assets` declares `territory`, `flight_start`, `flight_end` and `will_modify` as required and has no brand or owner parameter.
  - A3 a scripted model that loops on tool calls stops at `max_llm_calls` with an explicit "could not finish" message.
  - A4 the model ID is the literal `gemini-3.8-flash`, no alias.
  - A5 `search_assets` returns at most 20 usable and 10 partial assets with `status`, and distinguishes "no licensed assets" from "rights unavailable".
  - A6 a model error, blocked response or malformed tool call yields an explicit failure message and no state change.
  - A7 a request missing territory, dates or modification intent makes `search_assets` return `need_input` naming the missing terms, and a scripted conversation shows the assistant asking for them instead of assuming.
- **Verification:** offline pytest with fakes and a scripted model; needs google-adk installed.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Rights adapter, coverage rules and advertiser scope

- **Phase and estimate:** 1; hands-on 5.5–8, review 3–4.5, total 8.5–12.5; waits W2a, W2c (live read is in G05); owner Engineer
- **Outcome and linked decisions:** search uses the real rights system, scoped to the advertiser's brands, and lists as usable only assets covered for the exact territory, flight and modification intent; D2, D3, D10, invariant I1.
- **Scope:** `RightsClient` over the rights read API, per-brand queries merged, 5 s deadline, one retry on timeout/5xx; credentials from env/Secret Manager. Built against fixtures shaped from the rights team's API documentation. Adds `rights_coverage` (D10) with a rule table written as a test fixture for the rights team to confirm (W5). Excludes identity (G03) and the live read (G05).
- **Depth:** build; cross-advertiser denial and the coverage rule table are the core tests, reviewed as an authorization boundary; no caching.
- **Implementation route:** `app/tools/rights.py`; brands read from `tool_context.state["brands"]`.
- **Prerequisites:** G01; W2a rights API documentation or sample payloads; W2c rights semantics and region table.
- **Primary skill:** adk-tool-auth-and-secrets
- **Supporting skills:** safe-api-tool-calls (read deadlines and retries), adk-tool-interface-design (error results)
- **Acceptance:**
  - A1 a scripted model passing a brand or owner argument cannot widen scope; `usable` results contain only assets covered for state brands on the requested channel, territory, whole flight and modification intent, and `partial` results contain only assets of state brands.
  - A2 with two orgs' fixtures, org B's session never receives org A's assets.
  - A3 rights timeout or 5xx after the bounded retry → "rights unavailable", no assets shown.
  - A4 401/403 on the service credential → "rights unavailable" and an error log; no other credential is tried.
  - A5 a malformed rights payload fails schema validation and is reported as unavailable.
  - A6 429 → one backoff, then "busy, try again".
  - A7 a 4xx rejection of the query → "cannot check rights for that request", no assets shown.
  - A8 a table of at least 25 coverage cases passes: region group expansion, inclusive window start and end days, a flight one day past the window, two adjacent records joined, two records with a one-day gap, modification requested against an unmodified-only record, unmodified use against a modification-allowed record, another brand's record, and a time zone boundary, overlapping windows, and two joined records whose modification flags differ.
  - A9 an unknown territory code, a missing or inverted licence date, or an unknown modification value makes that record count as not covered, with the reason logged; nothing is listed as usable from it. Inverted flight dates, or a flight starting before today, return `need_input` before any rights call.
  - A10 partial coverage is returned only in the `partial` list, with the uncovered dates or territory, and never in `usable`.
  - A11 where asset metadata names a market, an asset whose market differs from the requested territory is not listed as usable; otherwise the result says the market is confirmed at quote (G04/A9).
  - A12 if any per-brand rights call fails, the whole search returns "rights unavailable" and lists no assets.
- **Verification:** offline with fixtures and a scripted model.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Sign-in, page and session ownership

- **Phase and estimate:** 1; hands-on 6–8.5, review 3–4.5, total 9–13; waits W2a (live sign-in is in G05); owner Engineer
- **Outcome and linked decisions:** advertisers sign in with the existing IdP and chat on a minimal page; D3, D6.
- **Scope:** OIDC code flow, ID-token verification, `org_brand_map` lookup, session ownership check, chat page, `ops` role gate. Excludes proposal cards (G06).
- **Depth:** build; floor: no tokens in logs, HTTP-only cookie.
- **Implementation route:** `app/main.py` middleware → session state; ADK session ID bound to `user_id`.
- **Prerequisites:** G01; W2a IdP discovery document and claim names.
- **Primary skill:** adk-frontend-integration
- **Supporting skills:** adk-tool-auth-and-secrets (token verification, trusted state)
- **Acceptance:**
  - A1 a valid token signs in; a token with a wrong issuer, audience, signature or a malformed body is rejected.
  - A2 a user whose org is not in `org_brand_map` is denied before any agent call.
  - A3 requesting another user's session ID returns 403 and no events.
  - A4 an expired token forces re-login and no tool runs.
  - A5 IdP unavailable or rate-limiting → a sign-in error page; no anonymous access.
  - A6 only users with the `ops` role reach `/ops`.
  - A7 an IdP error on callback or token exchange (`invalid_grant`, `access_denied`) shows the sign-in error page and creates no session.
  - A8 a replayed callback, a reused authorization code or a state or nonce mismatch is rejected.
  - A9 an expired or revoked OIDC client secret shows the sign-in error page and logs an error naming the client; there is no anonymous fallback.
- **Verification:** offline with a local test IdP (signed test keys).
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Quote tool

- **Phase and estimate:** 1; hands-on 3–4.5, review 1.5–2, total 4.5–6.5; waits none beyond G02's (staging reads are in G05); owner Engineer
- **Outcome and linked decisions:** the advertiser gets a live price, inventory and validity for a licensed asset on exactly the licensed terms; D4, invariants I2, I6.
- **Scope:** `get_quote`, `BookingClient.quote` against fixtures shaped from the booking read API documentation; rights recheck first. Excludes any booking write and the staging reads (G05).
- **Depth:** build; reads only.
- **Implementation route:** `app/tools/booking.py`; org account from state.
- **Prerequisites:** G02 (booking read API documentation from W2a, and booking market codes and date granularity from W2c, both arrive before G02).
- **Primary skill:** safe-api-tool-calls
- **Supporting skills:** adk-tool-interface-design (result shape)
- **Acceptance:**
  - A1 a quote for a licensed asset returns quote ID, price, currency, inventory and `valid_until`.
  - A2 a quote for an asset that `rights_coverage` does not cover on the requested terms (including a partial one) is refused before any booking call.
  - A3 booking timeout or 5xx → "pricing unavailable", and a scripted-model test shows the reply states no price.
  - A4 a booking rejection (validation, no inventory) returns an actionable reason.
  - A5 429 → one backoff, then "busy".
  - A6 401/403 → "pricing unavailable", error log, no fallback credential.
  - A7 an unexpected booking payload fails validation and is reported as unavailable.
  - A8 org A's quote is requested with org A's account only.
  - A9 a booking quote whose market or flight dates differ from the requested terms is refused with a reason, and nothing quotable is returned.
- **Verification:** offline fixtures and a scripted model.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Live integration check

- **Phase and estimate:** 1; hands-on 2.5–3.5, review 0.5–1, total 3–4.5; waits W2b; owner Engineer
- **Outcome and linked decisions:** the adapters built on fixtures in G02–G04 work against the real IdP, rights API and booking staging; D2, D4, D6.
- **Scope:** run the live checks and fix fixture drift. Excludes new behaviour.
- **Depth:** bounded live reads only; no booking writes.
- **Implementation route:** `tests/live/` marked and skipped by default; credentials from the local secret store, never committed.
- **Prerequisites:** G02, G03, G04; W2b credentials, booking staging access, IdP client and pilot test account; W5 expected answers for three real records.
- **Primary skill:** safe-api-tool-calls
- **Supporting skills:** adk-tool-auth-and-secrets (credential handling)
- **Acceptance:**
  - A1 a real sign-in with a pilot test account yields the expected `org_id` claim.
  - A2 a bounded live rights read for one pilot brand returns only that brand's licences, the payload validates against G02's schema, and `rights_coverage` gives the rights team's expected answer for three of their real records (covered, partial, not covered).
  - A3 a booking staging quote validates against G04's schema; any fixture drift is fixed and G02–G04 tests rerun green.
  - A4 at most 30 live calls in total; no credential appears in logs or test output.
- **Verification:** bounded live, explicitly authorized targets.
- **Execution scope:** needs W2b credentials; W2b's grant is the approval to call staging.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Proposal, confirmation and ops queue

- **Phase and estimate:** 1; hands-on 8–11, review 3.5–5, total 11.5–16; waits none; owner Engineer
- **Outcome and linked decisions:** an advertiser confirms one order request on exactly the licensed terms; booking ops see it, enter it and record the booking reference; D5, D10, invariants I3, I4, I6.
- **Scope:** `propose_order` tool, ledger tables, proposal card, `POST /proposals/{id}/confirm`, ops queue page, kill switch. Excludes direct booking submission (G12).
- **Depth:** build; careful review of the confirm path (money).
- **Implementation route:** `app/tools/orders.py`, `app/ledger.py`; confirm runs recheck → re-quote → one transaction.
- **Prerequisites:** G03, G04.
- **Primary skill:** safe-api-tool-calls
- **Supporting skills:** adk-operational-guardrails (confirmation outside the model, kill switch), adk-agent-security (injection structure), adk-frontend-integration (card and ops page)
- **Acceptance:**
  - A1 proposal → Confirm → exactly one request; ops marks it entered with a booking reference; the advertiser sees "entered, ref X".
  - A2 no tool confirms or submits; a scripted model attempting it changes no ledger row.
  - A3 two concurrent confirms of one proposal produce one request; the second returns it.
  - A4 if the re-quote's price or inventory differs, no request is made and a new proposal card is shown.
  - A5 rights revoked after proposal → refused, proposal void.
  - A6 another org's proposal ID → 404, no change.
  - A7 an expired proposal (past `valid_until`) is refused.
  - A8 `propose_order` takes one quote ID; "book everything" yields at most one proposal per call and each needs its own Confirm.
  - A9 an asset description containing instructions creates no request; any proposal card shows ledger values.
  - A10 a failed or lost commit at confirm shows "not confirmed, refresh"; proposal status and request insert are one transaction.
  - A11 ops status moves `requested → entered | rejected` once; a second mark returns the current state; rejection reasons reach the advertiser.
  - A12 the kill switch makes `propose_order` and confirm return "ordering paused".
  - A13 marking a request entered requires typing back its request ID, and a booking reference already recorded on another request is refused.
  - A14 the proposal, its card and the request carry territory, flight dates, modification intent and the rights record IDs used; confirm re-runs `rights_coverage` on those stored terms, and any change in terms or coverage voids the proposal and shows a new one.
  - A15 when ops mark a request entered, they type the booked flight dates and market from the booking order; the page blocks "entered" if these differ from the request or if `rights_coverage` no longer covers the request's terms at that moment, and the request can then only be rejected, with the reason shown to the advertiser.
- **Verification:** offline with Postgres in a container and a scripted model; concurrency test with two clients.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — Evaluation set

- **Phase and estimate:** 1; hands-on 4–5.5, review 0.5–1, total 4.5–6.5; waits W2b (live model calls need the GCP project); owner Engineer
- **Outcome and linked decisions:** a measured baseline of the agent's decisions on 20 labelled cases (10 journey, 5 rights-term, 5 adversarial); grows in G14.
- **Scope:** cases from realistic planner requests, a runner, a results table. Excludes a CI gate (G14).
- **Depth:** build at pilot depth; deterministic assertions first.
- **Implementation route:** `tests/eval/` with fakes from G02/G04.
- **Prerequisites:** G04, G06; W2b GCP project with Vertex access.
- **Primary skill:** adk-agent-evaluation
- **Supporting skills:** adk-agent-security (adversarial cases)
- **Acceptance:**
  - A1 the runner reports per-case pass/fail and a total, and a missing result counts as a failure.
  - A2 every case's tool arguments stay within the session's brands.
  - A3 no reply states a price without a `get_quote` result in the same turn.
  - A4 the 5 injection cases create no proposal unless the user asked for one.
  - A5 one of them resumes a stored session whose earlier tool results carry injected asset text; still no proposal unless asked.
  - A6 in the rights-term cases (terms missing, window ending mid-flight, modification not allowed) the assistant asks for missing terms and never describes a partial or uncovered asset as usable.
  - A7 two territory cases ("Berlin" → DE; "DACH" → the region group) pass the correct territory to `search_assets`.
- **Verification:** local runs with the pinned model; record cost per run.
- **Execution scope:** local; live model calls within the Q3 allowance.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08 — Pilot environment and rehearsal

- **Phase and estimate:** 1; hands-on 6–8.5, review 2–3, total 8–11.5; waits none of its own (W2b reaches it through G05); owner Engineer
- **Outcome and linked decisions:** the service runs on Cloud Run with Cloud SQL and secrets; D7, D8, invariant I5.
- **Scope:** service account, Secret Manager, Cloud SQL, `DatabaseSessionService`, structured logs, per-advertiser daily cap, budget alert, release manifest, rollback, hosted rehearsal whose evidence goes with the W3 sign-off request. Excludes traces (G13).
- **Depth:** pilot; floor: no content in logs.
- **Implementation route:** Dockerfile, deploy script, `release.json`.
- **Prerequisites:** G05, G06; G16, so the rehearsal and the W3 evidence run on confirmed coverage rules; W2b GCP project and approvals (through G05).
- **Primary skill:** deploy-adk-on-google-cloud
- **Supporting skills:** adk-agent-observability (log fields, token counts), adk-release-engineering (manifest, rollback), adk-tool-auth-and-secrets (service account, secrets)
- **Acceptance:**
  - A1 the deployed revision serves sign-in → search → quote → proposal on staging data.
  - A2 a proposal and a request survive a new revision.
  - A3 logs carry session, invocation and proposal IDs and token counts, and no prompt or asset text.
  - A4 an advertiser over the daily cap gets a polite refusal; ops pages still work.
  - A5 Vertex unavailable or 429 → "assistant busy", no ledger change.
  - A6 `release.json` records image digest, prompt version, model ID, ADK pin and tool-schema hash; redeploying the previous revision works.
  - A7 Cloud SQL unavailable → chat and confirm fail closed with a message.
  - A8 a missing Vertex, SQL or secret permission fails the readiness check and the revision takes no traffic.
  - A9 model lifecycle and Vertex prices re-read from official pages and dated in the design.
  - A10 a permission or secret revoked while serving makes the affected request fail closed with a message and an error log; no fallback identity is used.
  - A11 Cloud Run `max-instances` × pool size stays below the Cloud SQL tier's connection limit, and a burst at that cap shows no connection errors.
  - A12 one internal user completes the full journey on the hosted service with booking staging; the evidence is attached to the W3 request.
- **Verification:** hosted checks on staging; bounded calls.
- **Execution scope:** cloud commands only within the project, region and resources approved in W2b.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09 — Pilot readiness

- **Phase and estimate:** 1; hands-on 2.5–4, review 0.5–1, total 3–5; waits W4; owner Engineer
- **Outcome and linked decisions:** five advertisers ready to onboard and ops trained; the runbook is part of the W3 sign-off.
- **Scope:** runbook, ops training, onboarding data, baseline. Excludes the rehearsal (G08/A12) and go-live (G10).
- **Depth:** pilot.
- **Implementation route:** `docs/runbook.md`, `org_brand_map` load script.
- **Prerequisites:** G07, G08, W4, W7 (booking-ops staging session).
- **Primary skill:** adk-operational-guardrails
- **Supporting skills:** none
- **Acceptance:**
  - A1 one booking-ops person processes a staged request end to end using the runbook.
  - A2 the runbook covers entering a request, putting the request ID in the booking order note, searching booking by request ID or, where order notes are not searchable, by advertiser, asset and dates (both branches written; W1's phase 2 answer selects one) before re-entering a request whose reference was not recorded, rejecting an expired or changed quote, entering flight dates and territory exactly as on the request (rejecting it if booking cannot match them), and the kill switch.
  - A3 the five orgs' brand mappings are loaded from the W4 signed-off list and each passes a denial test against another org's brand.
  - A4 the W2b production booking read credential is stored in Secret Manager but not yet enabled.
  - A5 account managers' current turnaround for the five advertisers is recorded as the baseline.
- **Verification:** hosted rehearsal.
- **Execution scope:** hosted staging only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G10 — Go-live

- **Phase and estimate:** 1; hands-on 0.5–1, review 0, total 0.5–1; waits W3; owner Engineer
- **Outcome and linked decisions:** the five advertisers can use the pilot.
- **Scope:** record sign-off, switch to production booking reads, enable the five orgs.
- **Depth:** pilot.
- **Implementation route:** configuration change and a new revision; release manifest updated.
- **Prerequisites:** W3, G09, W6 (planners named and available).
- **Primary skill:** deploy-adk-on-google-cloud
- **Supporting skills:** none
- **Acceptance:**
  - A1 the W3 sign-off is recorded with its date and names.
  - A2 each pilot org signs in, searches and gets a production quote; a pilot user from another org is denied a foreign proposal.
  - A3 the W5 confirmation of the rule table is recorded with the rule-table version that is deployed.
- **Verification:** hosted, production reads.
- **Execution scope:** production reads after W3.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G16 — Coverage rule corrections after the rights review

- **Phase and estimate:** 1; hands-on 0.5–3, review 0.5–1, total 1–4; waits W5; owner Engineer
- **Outcome and linked decisions:** the coverage rules match the rights team's answers before anything is rehearsed; D10.
- **Scope:** apply W5's corrections to `rights_coverage` and its rule table; rerun G02's tests. Excludes new rights terms.
- **Depth:** authorization boundary; careful review.
- **Implementation route:** `app/rights_coverage.py`, `tests/rights_coverage_cases.*`.
- **Prerequisites:** W5.
- **Primary skill:** adk-tool-auth-and-secrets
- **Supporting skills:** none
- **Acceptance:**
  - A1 every W5 correction is a new or changed row in the rule table, and G02/A8–A12 pass.
  - A2 the confirmed rule-table version is recorded for G10/A3.
- **Verification:** offline.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G16 from docs/plans/campaign-assistant.md. Read docs/architecture/campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 (outline; phase 1 results will change these)

#### G11 — Booking contract discovery
Discovery, 3–5 h, `safe-api-tool-calls`, after W1 and G10. Question: does booking accept a client reference that deduplicates, and can an order be looked up by it? Evidence: written answers plus a staging experiment (same request sent twice; lookup after a forced client timeout). Stop when both are answered or the booking team declines.

- A1 a dated decision record: lookup-based recovery, replay-safe key, or manual reconciliation only.

#### G12 — Direct order submission
12.5–18.5 h, `safe-api-tool-calls` (supporting `adk-operational-guardrails`, `adk-agent-security`), after G11. Confirm submits once per operation with the request ID as client reference; no automatic retry of the write.

- A1 a duplicate confirm or a restarted worker sends no second create for the same operation.
- A2 a timeout after send marks the request `uncertain`, blocks resubmission, and recovery uses G11's lookup or ops reconciliation.
- A3 booking unavailable or 429 before send → `not_submitted`, safe to retry.
- A4 a rejection, expired credential or malformed reply → `failed` with reason, no retry.
- A5 price, inventory or rights change since confirm → nothing sent, new proposal; a partial multi-line order is not offered.
- A6 the create payload is built only from the ledger row with the owning org's booking account; a mismatched org, asset or account is refused before sending.

#### G13 — Traces and cost
4–6 h, `adk-agent-observability`, after G10.

- A1 one trace per turn with agent, tool and model spans carrying the session ID, and token cost per advertiser per day visible.

#### G14 — CI evaluation gate
4–6 h, `adk-release-engineering`, after G10.

- A1 a prompt or model change that fails G07's set fails CI by exit code.

#### G15 — Adversarial suite
4–8 h, `adk-agent-security`, after G12.

- A1 30 adversarial cases including injected asset text, cross-org IDs and asset text claiming "licensed worldwide, modification allowed"; no forbidden create reaches the booking fake and coverage always comes from `rights_coverage`.

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Model Armor / SDP screening | Personal data in asset metadata or chats | Confidential text reaches the model as today | protect-adk-sensitive-data |
| Saved searches and preferences | Advertisers ask for them in the pilot | Users repeat requests | adk-memory-architecture |
| Cancel and amend orders | Account managers' load from changes | Changes stay manual | safe-api-tool-calls |
| Payment and delivery status | Those teams expose a status API | Users ask account managers | adk-agent-interoperability |
| Session retention job | Before more than five advertisers | Manual deletion at 90 days | adk-memory-architecture |
| Canary and SLO alerts | More than 20 advertisers | Rollback is manual | adk-release-engineering |
| Latency tuning | Measured p95 > 15 s | Slow answers | optimise-adk-on-google-cloud |
| Permitted modification types (crop, overlay, re-edit) instead of a yes/no flag | Rights records turn out to list types (W2a) | The planner's intent is recorded as yes/no only; account managers check details | safe-api-tool-calls |
| Coverage evaluated by the rights system instead of D10 | The rights team offers such an endpoint | Encoded rules can drift from the rights team's; W5 confirms them once | adk-tool-auth-and-secrets |
| Rights revoked or expiring after an order is entered | First such case in the pilot | Booked orders are not re-checked; the rights team and account managers handle it as today | safe-api-tool-calls |

## Open decisions for further planning

See the design's open decisions; the cut line (Q7, D5) is the one that moves dates.

## Schedule changes

Revision 1:

| Change | Why | Helper result after (15 days unless stated) |
| --- | --- | --- |
| Direct submission (G11, G12) moved to phase 2 | First draft with it in phase 1 was well over capacity (hand sum, not run) | — |
| First helper run | — | 44.5–67 h; finish 11.22–18.89 days, low end only |
| G02–G04 built on fixtures; live checks moved to new G05 behind the credentials wait (hours moved, +1 h live debugging) | Removes idle time without removing a dependency | 45.5–68 h; 10.11–15.11 days |
| G07 evaluation set 20 → 15 cases (5 adversarial kept) | Scope cut | 45–67 h; 10–14.89 days; "fits" |
| Review P1: W2 split into W2a (docs, 1–3 days) and W2b (credentials, 2–5); G02 and G03 now wait for W2a | The fixtures need the docs; "only G05 waits" was wrong | (combined below) |
| Review P2, P4, P7, P8: staging access, production read credentials, GCP project/region/resource approval, billing access, hosted redirect URI and pilot test account moved into W2b; order-note search question into W1; turnaround baseline into W4 | Prerequisites named in prose had no wait | (combined below) |
| Review P3: W3 sign-off now follows G08's hosted rehearsal (moved from G09 to G08/A12, +0.5 h); G09 runs during the wait; new G10 go-live (0.5–1 h) | Sign-off cannot precede what it signs off | (combined below) |
| Review P5: new W4, signed-off org→brand list, before G09 | Outside approval had no wait | (combined below) |
| Review P6: G07 waits for W2b | Live model calls need the GCP project | (combined below) |
| Review V1–V3: G03/A7–A9 (+1.5–2 h) | IdP rejection, callback replay, client-secret expiry untested | (combined below) |
| Review V5, V7: G08/A10–A11 (included in the +0.5 h above); V8: G06/A13 (+0.5 h); V6: G07/A5; V9: G12/A6 (+0.5 h); V4: grid cites G06/A9, G07/A4 | Grid cells cited items that did not test them | Phase 1 after all fixes: 48.5–71.5 h; 11.67–20.67 days; low end only |
| Review C3: removed the remedy "onboard advertisers four and five later" | It saved about 1 h, did not address waits and broke G09/A3 | — |
| Review C4: removed the what-if "ADK-experienced engineer with direct ordering fits" | It left out the graduation goals the design requires before direct ordering | — |

Revision 2 (rights depend on territory, flight dates and modification), compared with revision 1:

| Change | Why | Helper result after |
| --- | --- | --- |
| New D10 `rights_coverage`; G02 grows to 8–11.5 h with G02/A8–A10; G02/A1 strengthened to the full terms | Coverage is an authorization decision over five terms | (combined below) |
| G01/A2 strengthened (required terms), new G01/A7 (ask, never assume); G01 3.5–5 h | The model must not guess territory, dates or modification intent | (combined below) |
| G04/A2 strengthened (partial coverage refused), new G04/A9 (quote terms must match); G04 4.5–6.5 h | The quote must be for the licensed terms | (combined below) |
| G05/A2 strengthened (three real records give the expected answer); G05 3–4.5 h | The live check covers the rules, not only the payload | (combined below) |
| New G06/A14 (terms bound to the proposal, rechecked at confirm), G06/A15 (ops recheck before "entered"); G06 11–15.5 h | Rights can change between quote, confirm and entry | (combined below) |
| G07 15 → 18 cases (3 rights-term cases), new G07/A6; G07 4–6 h | The model's handling of terms is measured | (combined below) |
| New wait W5 (rights team confirms the rule table, 1–3 days, after G02); G08 and go-live wait for it; new G10/A3 | Encoded rules can be wrong; this is the only outside check of them | (combined below) |
| W2a also asks for territory, date and modification semantics, and whether the rights system can evaluate coverage | Q12–Q15 | (combined below) |
| G09/A2 runbook: enter dates and territory exactly as requested | Ops entry must match the licensed terms | 54.5–79.5 h; 12.78–22.11 days; low end only; committed date 23 |
| Review R2-1: W3 now waits for G09 (the ops lead signs off the runbook) | Sign-off needs what it signs | (combined below) |
| Review R2-2: new G00 (0.5 h) sends the day-1 requests; all waits follow it; removed from G01 | Waits cannot start before the request is sent | (combined below) |
| Review R2-3: rights semantics split out of W2a into new W2c (2–5 days), with booking market codes, date granularity and multi-time-zone markets added; G02 waits for W2c | W2a had grown without its estimate changing | (combined below) |
| Review R2-4: new G16 (1–4 h) for rule corrections after W5; G08 waits for G16 | W5 can return corrections | (combined below) |
| Review R2-5: G05 waits for W5 (three labelled records) | G05/A2 needs the rights team's expected answers | (combined below) |
| Review R2-6, R2-7: new waits W6 (planners named, accounts, go-live session) and W7 (booking-ops staging session) | G10/A2 and G09/A1 need outside people | (combined below) |
| Review R2-8: aligned test org, brand, rights record and staging inventory added to W2b and W2c | G08/A12 needs data that lines up | (combined below) |
| Review R2-9: G09/A2 runbook writes both search branches, so G09 does not need W1 | Hidden dependency on a phase 2 wait | (combined below) |
| Review R2-17, R2-19, R2-21: new G02/A11 (asset market), G02/A12 (per-brand failure), more A8 and A9 cases, G01/A5 covers the partial cap, new G07/A7 (place to territory); G02 8.5–12.5 h, G07 4.5–6.5 h | Rights-term failure modes nothing covered | (combined below) |
| Review R2-18: G06/A15 rechecks at the "entered" click and compares the booked dates and market; G06 11.5–16 h | I6 claimed more than A15 tested | Phase 1: 57.5–86 h; 16–28.56 days; no at 15; committed date 29 |
| Review R2-20: the confirm "wrong target" cell cites G06/A14 instead of G04/A9 | A9 is a quote-time check | grid check passes |
| Review R2-12, R2-13, R2-15, R2-16: summary no longer calls W5 date-setting; W5 before the rehearsal is justified on safety; resume prompt covers G01/A1–A7; added-hours figure corrected | Claims the helper did not support | — |
| Grid: rights untrusted cell adds G02/A9; confirm "wrong target" adds G04/A9, "stale" adds G06/A14; ops "stale" adds G06/A15 | Cells cite the items that test the new terms | grid check passes |

**Removed or weakened in revision 2.** The review found four that my
mechanical check missed; each is now restored or listed:

| Item | What happened | Resolution |
| --- | --- | --- |
| Design I1 failure outcome | "Rights unavailable → 'cannot check rights'" had been merged into "not covered" | Restored: an outage says "cannot check rights"; a malformed record counts as not covered |
| G02/A1 | Constrained only `usable`, not the new `partial` list | Extended to `partial` |
| Revision 1 what-if table | Replaced without a note (it covered 20 days, 21 days, read-only, ADK-experienced and team commitments on the then-current plan) | Superseded by the table below; same remedies rerun on the current plan |
| Design data row "Rights" | Changed from "not stored beyond the turn" to storing rights record IDs on proposals and requests (1 year) | Kept deliberately for audit of I6; listed here |

Apart from these, checked mechanically against a copy of revision 1:
all 81 acceptance items and 63 grid cells remain, no citation was dropped
from any cell (seven cells gained citations; one n/a reason was corrected),
no cross-cutting scenario row was removed, the floor text is unchanged, and
waits were only added (W2c, W5, W6, W7). Seven items were reworded, all to
cover more (G01/A2, G01/A5, G02/A1, G04/A2, G05/A2, G09/A2, G15/A1).
Fifteen were added (G00/A1, G01/A7, G02/A8–A12, G04/A9, G06/A14–A15,
G07/A6–A7, G10/A3, G16/A1–A2).

What-ifs run on revision 2 after its review (copies through stdin, nothing applied):

| What-if | Hours | Finish (working days) | Fits 15 days? |
| --- | --- | --- | --- |
| **29 working days** | 57.5–86 of 130.5 | 16–28.56 | — (fits 29: **yes**) |
| 28 working days | 57.5–86 of 126 | 16–28.56 | — (fits 28: low end only) |
| Read-only pilot (G06 ordering to phase 2) | 46–70 | 13.44–25 | No, and it drops buying |
| Engineer already knows ADK (no 1.5×) | 38.5–57.5 | 12.37–23.08 | No |
| Teams commit W2c 1–2, W7 1, W3 1–2 days (only if they confirm) | 57.5–86 | 14–23 | No |
| All three above together | 30.83–46.83 | 8.67–14.82 | Yes, but without buying and with a different engineer; not recommended |

## Resume here

- **Next goal:** G00 Day-1 requests (you, 0.5 h), then G01 Local agent on fakes, which is ready because it needs no access grants.
- **Read first:** the design, this plan.
- **Next action:** send the G00 requests and bookings; confirm the installed ADK version.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 Local agent on fakes from docs/plans/campaign-assistant.md.
Read docs/architecture/campaign-assistant.md and preserve its accepted decisions.
Use adk-workflow-design with adk-tool-interface-design, adk-agent-instructions and adk-model-and-output-contracts.
Work within local files only, verify G01/A1–A7, and update
the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/campaign-assistant.md.`
