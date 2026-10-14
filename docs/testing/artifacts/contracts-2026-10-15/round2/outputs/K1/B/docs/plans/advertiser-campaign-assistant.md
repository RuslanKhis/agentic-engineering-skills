# Implementation plan: advertiser campaign assistant (pilot)

Status: draft, revision 2 (2026-10-15: rights depend on territory, flight dates and modification); ready goals identified (G01). Nothing is implemented.
Architecture: [design](../architecture/advertiser-campaign-assistant.md)
Continuation source of truth: this plan

## Summary for the reader

- **Profile and phase 1:** MVP or pilot. Phase 1 lets five advertisers sign
  in, find assets their brand may use on a channel, get live quotes and confirm
  a purchase. Each confirmed purchase becomes a request that sales ops places in
  the booking system (D3). Automated booking writes wait for phase 2, because
  the booking system's replay and status-lookup behaviour is undocumented.
- **Effort and finish:** the build (phase 1, G01–G06) is 38–63 human hours
  against 54 hours after reserve, so the hours fit at the **low end only**. It
  finishes in 10.6–18.5 working days against 15. Go-live (W6 approval on G06's
  evidence, then G12 onboarding) follows; end to end, advertisers start after
  13.8–24.3 working days. The helper's remedies: a **19-day** build window fits
  (17 did before revision 2), or 17 days if the engineer confirms 0.7 focus. No
  15-day option exists without cutting the rights checks, the evaluation or the
  staging run, which are the core contract and its evidence. Only modification
  *requests* move to phase 2 (G13); pilot campaigns use creatives as-is.
  Figures from `check_schedule.py`, run 2026-10-15, after the revision-2 review.
- **Largest risks:** (1) Booking replay and lookup are unknown. Phase 1 avoids
  automated writes, and G07 settles the question for phase 2. (2) Access waits
  (W1 IdP client, which needs W5's project URL; W2 API credentials; W4 security
  review) gate the chain. All except W1 and W6 are requested on day 1, and G01
  needs none of them. (3) Rights may depend
  on more than owner, brand and channel. Resolved: territory, dates and
  modification are now in C1. Their exact semantics (date inclusivity, territory
  codes, modification levels; O8–O10) arrive with W12, and G01 builds on
  assumptions Q13–Q15 that may need adjusting.
- **Decisions needed from you:** confirm or move the cut line (manual placement
  by sales ops in phase 1, Q10/O6, and go-live after the build window). Choose
  a 15- or 19-day build window. Confirm that pilot campaigns use creatives
  as-is (Q15); if not, G13 moves into phase 1 and the window becomes 21 days. Say whether the security review needs the built
  system (O7). Confirm the assumed answers Q1–Q12 in the
  design, especially full-time capacity (Q2) and what an order commits (Q5).
- **Next prompt:** `/adk-engineer Carry out G01 from docs/plans/advertiser-campaign-assistant.md.`

## Destination and constraints

The destination is the design's journey, with ops-placed orders in phase 1
and automated orders in phase 2. Stack (proposed, nothing installed): Python
3.11, `google-adk==2.8.0` (D10, confirm in G01), FastAPI, Cloud SQL for
PostgreSQL, Cloud Run, Vertex AI `gemini-3.8-flash` (D7). No LLM judge in
phase 1. Evaluation uses human labels and deterministic checks. A goal that
changes the model, prompt or ADK pin is a release and is recorded as one.
Authorization: this session wrote design documents only. No cloud project,
credentials or deployment are authorized yet. Each goal names what it needs.

Proposed layout (greenfield, not inspected): `app/agent.py` (App and agent),
`app/tools/` (four tools), `app/adapters/{rights,booking}.py`, `app/server.py`
(FastAPI: OIDC, `/chat`, `/confirm`), `app/ops.py` (export CLI), `app/store.py`,
`app/static/` (page), `tests/` (offline fakes and scripted model).

## Delivery profile and capacity

Profile: MVP or pilot (see the design's delivery constraints). Capacity: one
engineer × 15 working days × 8 h × 0.6 focus = 72 focused hours, with a 25 %
reserve, leaving 54 hours for goals. Every estimate already includes the ×1.5
multiplier for a developer new to ADK, on hands-on and review alike.

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship (build) | The full journey proven on staging with real rights (territory, flight, as-is use), quotes, sign-in and sales-ops placement, evaluated; failures and cost visible in logs | G01–G06 | 38–63 | 72 h; 54 h after reserve |
| 1b, go-live | Five advertisers onboarded after the go-live approval (W6) on G06's evidence | G12 | 1–3 | inside the reserve or the week after |
| 2, harden or graduate | Automated booking, reconciliation, CI gate, traces, modification requests | G07–G11, G13 | 25–46 | when the team has time |

Calendar waits are scheduled as `W` entries. They do not consume hours. All are
requested on day 1, except W1 (once W5 gives the Cloud Run URL), W6 (with
G06's evidence) and W11 (pilot data accumulates after G12).

```yaml
- goal: W5
  phase: 1
  total: 0
  calendar_waits: GCP project with billing; Vertex AI, Cloud Run, Cloud SQL and Secret Manager enabled; permission to create a service account and a budget alert; the user's deploy authorization
  wait_days: 1-3
- goal: W1
  phase: 1
  total: 0
  blocked_by: [W5]
  calendar_waits: IdP client registration by the identity team (redirect URIs for localhost and the pilot Cloud Run URL, org claim)
  wait_days: 3-5
- goal: W2
  phase: 1
  total: 0
  calendar_waits: access request for rights read API and booking pricing and inventory staging credentials, reachable from Cloud Run (service and export job); booking team answer on territory pricing (O12)
  wait_days: 3-5
- goal: W3
  phase: 1
  total: 0
  calendar_waits: sales ops agreement to place pilot requests within one business day, only within the cleared territories and flight dates, and to report the booking's territories and dates for set-state
  wait_days: 2-5
- goal: W4
  phase: 1
  total: 0
  calendar_waits: security review of this design before external access
  wait_days: 5-10
- goal: W12
  phase: 1
  total: 0
  calendar_waits: rights team written answers on date semantics, territory codes, modification levels and grant-record API shape (requested day 1)
  wait_days: 3-5
- goal: W13
  phase: 1
  total: 0
  calendar_waits: aligned test data from the rights and booking teams (staging assets whose grants cover the test territories and flights, with matching booking staging inventory), requested day 1
  wait_days: 3-5
- goal: W8
  phase: 1
  total: 0
  calendar_waits: external advertiser user accounts created in the IdP (requested day 1)
  wait_days: 3-5
- goal: W9
  phase: 1
  total: 0
  calendar_waits: pilot inputs from the pilot owner: org-to-brand table, 20-25 real briefs with territories and flight dates, account-manager turnaround figures, confirmation that pilot campaigns use creatives as-is (Q15)
  wait_days: 2-5
- goal: G01
  phase: 1
  hands_on: 4-7
  review: 3-4
  total: 7-11
  owner: Engineer
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  contracts: [C1, C7, C9, C10]
  mentions_only: [W12]
- goal: G02
  phase: 1
  hands_on: 3-6
  review: 2-3
  total: 5-9
  owner: Engineer
  blocked_by: [G01, W5]
  calendar_waits: none beyond W5
  wait_days: 0
  contracts: [C8, C11]
- goal: G03
  phase: 1
  hands_on: 5-9
  review: 2-4
  total: 7-13
  owner: Engineer
  blocked_by: [G01, G02, W2, W12, W13]
  calendar_waits: none beyond W2
  wait_days: 0
  contracts: [C1, C3, C7]
- goal: G04
  phase: 1
  hands_on: 4-7
  review: 4-6
  total: 8-13
  owner: Engineer
  blocked_by: [G02, G03, W1]
  calendar_waits: none beyond W1
  wait_days: 0
  contracts: [C2]
- goal: G05
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Engineer
  blocked_by: [G03, G04, W3]
  calendar_waits: none beyond W3
  wait_days: 0
  contracts: [C1, C2, C3, C4, C5, C6, C9, C12]
- goal: G06
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Engineer
  blocked_by: [G05, W4, W9]
  calendar_waits: sales ops places the staging request within one business day
  wait_days: 0-1
  contracts: [C1, C4, C5, C9, C10]
- goal: W6
  phase: 1b
  total: 0
  blocked_by: [G06]
  calendar_waits: go-live approval from the commercial owner (pilot terms, retention), given on the G06 evidence
  wait_days: 3-5
- goal: G12
  phase: 1b
  hands_on: 1-2
  review: 0-1
  total: 1-3
  owner: Engineer
  blocked_by: [W6, W8]
  calendar_waits: none beyond W6 and W8
  wait_days: 0
  contracts: [C2]
- goal: W7
  phase: 2
  total: 0
  calendar_waits: booking team written answers on replay key, lookup by client reference and timeouts (requested day 1)
  wait_days: 5-10
- goal: W10
  phase: 2
  total: 0
  calendar_waits: access request for booking staging order-write credentials
  wait_days: 3-5
- goal: W11
  phase: 2
  total: 0
  blocked_by: [G12]
  calendar_waits: two weeks of pilot sessions to sample evaluation cases from
  wait_days: 10
- goal: G07
  phase: 2
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Engineer
  blocked_by: [W7, W10]
  calendar_waits: none
  wait_days: 0
  contracts: [C5]
- goal: G08
  phase: 2
  hands_on: 5-8
  review: 3-6
  total: 8-14
  owner: Engineer
  blocked_by: [G07, G05]
  calendar_waits: none
  wait_days: 0
  contracts: [C5, C4, C1]
- goal: G09
  phase: 2
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Engineer
  blocked_by: [G08]
  calendar_waits: none
  wait_days: 0
  contracts: [C6, C5]
- goal: G10
  phase: 2
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Engineer
  blocked_by: [G06, W11]
  calendar_waits: none
  wait_days: 0
  contracts: [C10]
- goal: G13
  phase: 2
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Engineer
  blocked_by: [G05, W12]
  calendar_waits: none
  wait_days: 0
  contracts: [C1, C12]
- goal: G11
  phase: 2
  hands_on: 2-4
  review: 1-2
  total: 3-6
  owner: Engineer
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  contracts: [C11]
```

Longest dependent chain and finish range (phase 1): G01 → G02 → G03 → G04 →
G05 → G06, at 10.6 days (low) and 18.5 days (high). Finish 10.6–18.5 working
days with one person, 4.8 focused h/day and a 25 % reserve. Including go-live
(W6, G12): 13.8–24.3 days. Command:
`python3.11 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/advertiser-campaign-assistant.md --design docs/architecture/advertiser-campaign-assistant.md --days 15 --reserve 0.25 --person "Engineer=4.8"`,
run 2026-10-15 after the revision-2 review. Exit 1: hours and calendar fit at
the low end only. Grid citations are valid, and all 12 contracts are cited.
With `--days 19`, exit 0.

What-ifs for moving the cut line (helper output, see "Schedule check runs"):

| What-if (on a copy of the schedule, revision 2 after review) | Phase-1 hours | Finish (working days) | Fits? |
| --- | --- | --- | --- |
| Plan as written: build G01–G06, as-is use only, go-live after | 38–63 of 54 | 10.6–18.5 | 15 days: low end only |
| Same, 18-day build window | 38–63 of 64.8 | 10.6–18.5 | low end only |
| Same, 19-day build window | 38–63 of 68.4 | 10.6–18.5 | yes |
| Same, engineer confirms 0.7 focus (5.6 h/day), 16 days | 38–63 of 67.2 | 9.2–16.4 | low end only (chain W5 → G02 → … → G06) |
| Same, 0.7 focus, 17 days | 38–63 of 71.4 | 9.2–16.4 | yes |
| Modification requests in phase 1 (G13 moved in, and G06 waits for G13 so it is evaluated) | 41–69 of 54 | 11.4–20.2 | 20: low end only; 21 days: yes |
| Go-live (W6, G12) inside phase 1 | 39–66 of 54 | 13.8–24.3 | 24: low end only; 25 days: yes |
| Automated booking in phase 1 (W7, W10, G07, G08 moved in) | 49–83 of 54 | 13.6–24.1 | 24: low end only; 25 days: yes |

If time runs out early, the goals are ordered to stay useful. G01 and G02
give a hosted read-only demo on fake rights. G03 adds real rights and quotes.
G04 makes it usable by advertisers. G05 adds purchasing.

## Implementation map

| Contract / decision | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| C1, D8 | `search_assets` reads `brand_ids` from `ToolContext.state` and calls `RightsClient`. Filter in code before return; `rights.evaluate` (D11) rechecked in `get_quote`, `propose_purchase`, `/confirm` and the export job | none | `adk-tool-interface-design` | Rights API shape and semantics (W12; O8, O10) |
| C2, D4 | FastAPI OIDC middleware writes trusted state at session creation and per turn. Store queries filter by owner | Secret Manager for the client secret | `adk-tool-auth-and-secrets` | IdP claim names (W1) |
| C3, C4, D2 | Quote and proposal tables. `/confirm` endpoint with hash check and rechecks; card rendered from the record | Cloud SQL | `safe-api-tool-calls` | none beyond tests |
| C5, C6, D3 | `purchase_requests` unique on `proposal_id`; `app.ops` export and set-state command, run by the engineer with DB access (no ops UI in phase 1) | Cloud SQL | `safe-api-tool-calls` | Sales ops process (W3) |
| C8, C11, D9 | `RunConfig(max_llm_calls=8)`; admission check before `Runner.run_async`; env-flag kill switches; JSON logger with an allow-list | Cloud Run env, Billing budget alert | `adk-operational-guardrails` | `RunConfig` name at the pin (G01/A1) |
| C9, D1, D2 | Agent tool list has no write tool. Plain-text rendering in the page | none | `adk-agent-security` | Adversarial case (G06/A3) |
| D5, D6, D10 | `DatabaseSessionService` on Cloud SQL; one Cloud Run service with a service account | Cloud Run, Cloud SQL, Secret Manager, Vertex AI | `deploy-adk-on-google-cloud` | Session service constructor at the pin |
| D7, C10 | Pinned model in `app/agent.py`; instruction kept as a versioned file | Vertex AI | `adk-model-and-output-contracts` | Vertex lifecycle row for 3.8 |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Licensed-asset search, local | 1 | implementation | 7–11 | none | `adk-tool-interface-design` | ready |
| G02 Hosted skeleton with guardrails | 1 | implementation | 5–9 | G01, W5 | `deploy-adk-on-google-cloud` | blocked: W5 |
| G03 Real rights and live quotes | 1 | implementation | 7–13 | G01, G02, W2, W12, W13 | `safe-api-tool-calls` | blocked: W2, W12, W13 |
| G04 Advertiser sign-in and page | 1 | implementation | 8–13 | G02, G03, W1 | `adk-tool-auth-and-secrets` | blocked: W1 |
| G05 Confirmed purchase request | 1 | implementation | 6–9 | G03, G04, W3 | `safe-api-tool-calls` | blocked: W3 |
| G06 Evaluation and staging end-to-end | 1 | implementation | 5–8 | G05, W4, W9 | `adk-agent-evaluation` | blocked: W4, W9 |
| G12 Pilot onboarding (go-live) | 1b | implementation | 1–3 | W6, W8 | `adk-tool-auth-and-secrets` | blocked: W6, W8 |
| G07 Booking replay discovery | 2 | discovery | 3–6 | W7, W10 | `safe-api-tool-calls` | proposed |
| G08 Automated order placement | 2 | implementation | 8–14 | G07, G05 | `safe-api-tool-calls` | proposed |
| G09 Booking status and reconciliation | 2 | implementation | 3–6 | G08 | `safe-api-tool-calls` | proposed |
| G10 Evaluation gate in CI | 2 | implementation | 5–8 | G06, W11 | `adk-release-engineering` | proposed |
| G13 Modification requests | 2 | implementation | 3–6 | G05, W12 | `adk-tool-interface-design` | proposed |
| G11 Traces and cost alerts | 2 | implementation | 3–6 | G02 | `adk-agent-observability` | proposed |

**Day-1 requests (no hours):** W2, W3, W4, W5, W7, W8, W9, W10, W12 and W13. Send the
design to the identity team (W8), the rights and booking teams (W2, W7, W10, W12, W13),
sales ops (W3), the security reviewer (W4), the cloud admins (W5) and the pilot
owner (W9). Request W1 as soon as W5 gives the Cloud Run URL. Request W6 with
G06's evidence.

### G01 — Licensed-asset search, local

- **Phase and estimate:** 1; hands-on 4–7, review 3–4, total 7–11; no waits; owner Engineer
- **Outcome, contracts and decisions:** a local agent answers "what can Acme
  run on social in the UK and Ireland, 1–14 July" from a fake rights adapter,
  showing only assets licensed for every territory and day, as-is.
  Proves C1 (search), C7, C9 (tool list) and C10 (instruction). Implements D1,
  D7, D8, D10, D11 and D12.
- **Scope:** agent, `search_assets` tool, `rights.evaluate` (D11),
  `RightsClient` interface and fake built from grant fixtures (owner, brand,
  channel, territory, start, end, modification allowed), scripted-model tests.
  Date and territory semantics follow Q13 and Q14 until W12 answers.
  Excludes the real API (G03), identity (G04) and hosting.
- **Depth:** trusted scope is set directly in test state, and the floor is a
  pinned model and `max_llm_calls`. The adversarial suite waits for G06.
- **Implementation route:** `LlmAgent` in an `App`, invoked by `Runner` with
  `RunConfig(max_llm_calls=8)`. The tool reads `brand_ids` from
  `tool_context.state`, never from arguments. It takes territories, flight
  dates and channel as arguments, validated in code, and returns `{status,
  assets[≤20], filtered_reason}`, or `needs_input` with the missing fields.
- **Prerequisites:** none. Python 3.11 and `google-adk==2.8.0` installed locally.
- **Primary skill:** `adk-tool-interface-design`
- **Supporting skills:** `adk-agent-instructions` (instruction and rendered
  request); `adk-model-and-output-contracts` (pin and lifecycle check)
- **Acceptance:**
  - A1 → D10, C10: the ADK pin and the model ID are recorded with the lifecycle date. `RunConfig`, `ToolContext.state` and `App` are confirmed at the pin. The Vertex lifecycle row for `gemini-3.8-flash` is checked
  - A2 → C1: table-driven `rights.evaluate` cases. **Deny:** another brand, another channel, an owner without a grant, one of two territories uncovered, a flight starting one day before the grant, a flight ending one day after it, a gap between two grants, and a fragment from another owner, brand or channel that must not count towards the union. **Allow:** flight start equal to grant start, flight end equal to grant end, two adjacent grants, overlapping grants, and GB covered by one grant with IE covered by another. The result lists every grant ID used. A grant that forbids modification is allowed for as-is use. Denied assets never appear in the model request or the answer. The boundary rows are **provisional** on Q13 and Q14, and G03/A6 reruns them on W12's answers
  - A3 → C7: the rights fake returns unavailable or times out, and the user gets an explicit failure with no assets. The scripted model returns an error or malformed reply, and the answer is a bounded failure
  - A4 → C9, C10: the captured request shows one instruction and four declarations (stubs are allowed for the three later tools). No identity, brand or limit appears in the prompt
  - A5 → C1: an empty authorised search returns "none licensed for social" and does not retry with a wider channel, brand, territory set or date range
  - A6 → C1: a request without territory or flight dates gets `needs_input`, and the assistant asks instead of guessing. Invalid codes or a reversed date range are rejected in code. Common names map through an alias table in code ("UK" → GB, "Ireland" → IE), and an unmapped name is returned as `needs_input`, never as an empty search. A request for a modified creative gets "not in the pilot" and no search
- **Verification:** `pytest tests/offline` with a scripted model, offline tier.
- **Execution scope:** local only; no credentials.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/advertiser-campaign-assistant.md. Read docs/architecture/advertiser-campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Hosted skeleton with guardrails

- **Phase and estimate:** 1; hands-on 3–6, review 2–3, total 5–9; waits W5; owner Engineer
- **Outcome, contracts and decisions:** the G01 agent runs on Cloud Run
  against Cloud SQL, still on fake rights, reachable only by the engineer
  (IAM invoker). Proves C8 and C11. Implements D5, D6 and D9.
- **Scope:** FastAPI wrapper, `DatabaseSessionService`, usage table and
  admission check, kill switches, JSON logging, Secret Manager, service
  account, budget alert, deploy log with the release unit. Excludes the public
  sign-in, which G04 adds. Traces are left for phase 2 (G11).
- **Depth:** minimal observability (logs and token counts); rollback to the previous revision.
- **Implementation route:** Cloud Run service; Cloud SQL Postgres with a
  connector; `RunConfig.max_llm_calls`; admission before the Runner.
- **Prerequisites:** G01; W5 (GCP project). Deploy authorization from the user at that time.
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-operational-guardrails` (allowance, kill switch); `adk-release-engineering` (release unit, pins)
- **Acceptance:**
  - A1 → D6: the deployed revision reads back its image digest, model ID and ADK pin. Traffic rolls back to the previous revision. A Vertex permission or credential error surfaces as an explicit failure
  - A2 → D5: a session and a usage counter survive a service restart. Cloud SQL unavailable, or the service account's database access revoked, gives an explicit "unavailable", and nothing is half-written
  - A3 → C8: the ninth model call in one invocation is stopped. The 51st invocation of the day is refused. Vertex quota exhaustion (simulated as 429) gives a bounded failure
  - A4 → C8: `AGENT_ENABLED=false` refuses chat and `PURCHASES_ENABLED=false` refuses `/confirm`, both without a redeploy, while reads of status still work
  - A5 → C11: captured log lines from a full turn contain no prompt, response, price or token text, only allow-listed fields
- **Verification:** local Postgres tests, then one bounded live deploy to the pilot project.
- **Execution scope:** needs the user's authorization for the GCP project, deploy and budget alert.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/advertiser-campaign-assistant.md. Read docs/architecture/advertiser-campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Real rights and live quotes

- **Phase and estimate:** 1; hands-on 5–9, review 2–4, total 7–13 (includes 0–2 h of rework if W12 overturns Q13 or Q14); waits W2, W12, W13; owner Engineer
- **Outcome, contracts and decisions:** search uses the real rights system,
  and `get_quote` returns a stored, expiring quote from booking staging.
  Proves C1 (recheck at quote), C3 and C7. Implements D8.
- **Scope:** real `RightsClient` and `BookingClient` (pricing and inventory
  read only), quote table, `get_quote` tool, typed error results. Excludes
  proposals, which G05 adds.
- **Depth:** read-only integrations with a bounded timeout and at most one
  retry on idempotent reads.
- **Implementation route:** HTTP adapters with deadlines. The quote record
  holds `quoted_at`, `expires_at`, territories, flight dates, the price lines
  and the owner. Grant records map to D11's input.
- **Prerequisites:** G01; G02 (project, Secret Manager, Postgres); W2 credentials; W12 rights field semantics (adjust G01's fixtures if they differ from Q13 and Q14).
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-interface-design` (quote tool declaration and result bound)
- **Acceptance:**
  - A1 → C3: a live staging quote for three licensed assets (W13 test data) for two territories is stored and returned with its expiry
  - A2 → C1: a quote is refused with the field named when, after search, the fake revokes the grant, removes one territory, or moves the grant end before the flight end
  - A3 → C3: after expiry, the quote is reported as expired and re-quoted on request, never honoured. The answer's price matches the stored record, and a scripted model that misstates the price does not change the record
  - A4 → C7: for each adapter, unavailable, 4xx rejection, expired credential and 429 give a typed result and an honest message. Nothing is cached or broadened
  - A5 → C7: a malformed booking payload (missing price, wrong currency) or a malformed rights payload (missing brand or channel, unknown owner, unparseable or reversed dates, unknown territory code) is rejected at the adapter. Grant dates sent as timestamps with an offset are converted to calendar dates by the rule W12 confirms, and a test shows a near-midnight timestamp does not shift a day. No quote is stored and no asset is shown
  - A6 → C1: G01/A2's boundary table is rerun with W12's confirmed date, territory and modification semantics. Any differences are fixed and recorded here
- **Verification:** offline adapter tests with recorded fixtures; one bounded live staging run (at most 20 calls).
- **Execution scope:** staging read credentials only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/advertiser-campaign-assistant.md. Read docs/architecture/advertiser-campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Advertiser sign-in and page

- **Phase and estimate:** 1; hands-on 4–7, review 4–6, total 8–13; waits W1 (after W5); owner Engineer
- **Outcome, contracts and decisions:** an advertiser signs in with the IdP
  and chats on a minimal page, seeing only their own sessions. Proves C2.
  Implements D4.
- **Scope:** OIDC code flow, org-to-brand pilot table, trusted state, owner
  filters on every store query, minimal page with plain-text rendering.
  Excludes the confirm card, which G05 adds.
- **Depth:** build. The authorization boundary gets a careful review and adversarial tests.
- **Implementation route:** FastAPI middleware verifies the ID token
  (issuer, audience, expiry, signature through JWKS) and maps the org to brands.
  The session is created with the user as `user_id`, with state from the server.
- **Prerequisites:** G02 (Cloud Run URL for the redirect), G03 (quotes exist to deny); W1.
- **Primary skill:** `adk-tool-auth-and-secrets`
- **Supporting skills:** `adk-frontend-integration` (page and session ownership)
- **Acceptance:**
  - A1 → C2: Dana signs in and searches, and results are limited to Acme's brands
  - A2 → C2: a second advertiser's user cannot open Dana's session or quote by ID (404), and the model never sees them. Proposals and status are covered by G05/A9
  - A3 → C2: a brand ID or advertiser ID supplied in a chat message or request body does not change scope
  - A4 → C2: an expired user token, the IdP being unavailable, a token-endpoint rejection (`invalid_grant`, user not allowed) or a rejected OIDC client secret each gives a sign-in prompt or an explicit error, and no access
  - A5 → C2: a token with a wrong audience, a bad signature or an unknown org is refused
  - A6 → C2: a reused authorization code, or a replayed or mismatched `state`/`nonce` (double submit, back button), is refused with a clean sign-in restart
- **Verification:** local tests with a fake IdP (signed test keys); one live sign-in on the pilot project.
- **Execution scope:** IdP pilot client only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/advertiser-campaign-assistant.md. Read docs/architecture/advertiser-campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Confirmed purchase request

- **Phase and estimate:** 1; hands-on 4–6, review 2–3, total 6–9; waits W3; owner Engineer
- **Outcome, contracts and decisions:** Dana confirms an exact quote on a
  card. One purchase request is created, sales ops places it, and Dana sees
  the status. Proves C1 (recheck at confirm and export), C3, C4, C5, C6, C9 and C12.
  Proves C2 for proposals and status. Implements D2 and D3.
- **Scope:** `propose_purchase` and `get_request_status` tools, proposal
  table with a canonical payload hash, `/confirm` endpoint, `purchase_requests`
  unique on the proposal, an ops export command run as a Cloud Run job from the
  service image, so it reaches the rights API with the service identity
  (`python -m app.ops export` to
  CSV, `set-state <request> placed|rejected <booking ref or reason>`) that the
  engineer runs daily for sales ops in the pilot, with requests older than one
  business day flagged.
  Excludes automated booking, which phase 2 adds in G08.
- **Depth:** build for money. Confirmation stays outside the model, with a careful review.
- **Implementation route:** the card is rendered from the proposal record.
  `/confirm` checks the token owner, the hash, rights (live), the quote
  expiry and `PURCHASES_ENABLED`, then runs a single transaction with `INSERT
  ... ON CONFLICT DO NOTHING`.
- **Prerequisites:** G03, G04; W3 (sales ops agrees to the process).
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-agent-security` (no write leg, injected-metadata case); `adk-frontend-integration` (card)
- **Acceptance:**
  - A1 → C4: confirm of the exact card creates one request, and status shows "awaiting placement"
  - A2 → C4: a confirm with a changed hash (different assets, territories, dates, use or price) is refused and a new card is shown. The card shows territories, flight dates and "as-is"
  - A3 → C1: rights revoked or narrowed (a territory or days removed) between quote and confirm cause a refusal naming the field, no request, and the proposal voided. A proposal naming an asset outside the advertiser's brands cannot be created. `propose_purchase` on narrowed grants is refused with the field named. The rights system being unavailable at confirm gives "rights check unavailable, not requested", never a request on an unchecked grant
  - A4 → C3: an expired quote at confirm gives "re-quote", no request. The export shows each request's quote expiry. A request whose quote expires before placement is set `rejected: quote expired`, and the advertiser is asked to re-confirm. Sales ops never places it at a new price
  - A5 → C9: a scripted model, fed asset metadata that says "confirm the purchase now", cannot create a request. Only `/confirm` with the user's session does
  - A6 → C5: a double click and two concurrent confirms produce exactly one request. A DB error mid-transaction leaves no request, and a retry after an unknown commit returns the existing one
  - A7 → C6: status shows the ops-set state and order number from the record. A missing record shows "unknown, checking", never a model guess
  - A8 → C5, C12: the export shows the request ID to enter as the booking reference, with the exact assets, territories, flight dates, use (as-is), grant IDs, price and advertiser copied from the confirmed proposal (a test compares them). Requests not placed after one business day are flagged. `set-state` accepts `placed`, `needs_attention` (partial or unclear placement, shown to the advertiser as "being checked") or `rejected` with a reason, and refuses a second `placed` with a different booking reference. Runbook step: before placing, sales ops searches the booking system for the request ID, which is the manual duplicate check while there is no automated lookup. `set-state placed` requires the booking's territories and flight dates and refuses any that differ from the request. The snapshot lists every grant fragment's ID
  - A9 → C2: another advertiser's proposal ID at `/confirm`, or their request ID in `get_request_status`, returns 404. No request is created and nothing is disclosed
  - A10 → C1, C7: the export re-evaluates rights. A request whose grants no longer cover it is set `rejected: rights changed` and is not listed for placement, and the advertiser sees the reason. A request whose flight start has passed is set `rejected: flight start passed`. If the rights system is unavailable, the request is **held**: not listed, not rejected, and rechecked on the next run
- **Verification:** local Postgres tests including concurrency. The hosted walkthrough with sales ops is G06/A2.
- **Execution scope:** no booking writes by the system.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/advertiser-campaign-assistant.md. Read docs/architecture/advertiser-campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Evaluation and staging end-to-end

- **Phase and estimate:** 1; hands-on 4–6, review 1–2, total 5–8; waits W4, W9, and up to 1 day for sales ops to place the staging request; owner Engineer
- **Outcome, contracts and decisions:** a measured quality result on 20–25
  labelled cases, one adversarial case and a hosted staging run of the whole
  journey. This is the evidence the go-live approval (W6) is asked for. Proves
  C1, C4, C5, C9 and C10.
- **Scope:** labelled cases from real pilot briefs (W9) covering search
  relevance, correct refusals, asking for missing territory and dates, alias names such as "UK", modification requests refused as not in the pilot, turning "summer" or "UK and Ireland" into terms the user then confirms, and quote relay; a runner; a baseline of current
  turnaround; a go-live checklist. Excludes onboarding (G12) and the CI gate,
  which G10 adds in phase 2.
- **Depth:** an evaluation set run by hand. No judge model.
- **Implementation route:** ADK eval-style runner or pytest over a cases
  file; results summary in `docs/eval/summary.md` (proposed).
- **Prerequisites:** G05; W4 security review; W9 pilot inputs.
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** `adk-agent-security` (adversarial case)
- **Acceptance:**
  - A1 → C10, C1: the rate of correct term extraction and of asking when terms are missing is recorded, along with the grounding rate (asset and price claims backed by tool results) and refusal correctness are recorded per case, and failures are listed
  - A2 → C1, C4, C5: a hosted end-to-end run on staging covers sign-in, search, quote and confirm, then a sales-ops colleague places the request from the export and the status shows the booking reference
  - A3 → C9: hostile asset metadata and malformed model output (prose where a tool call was expected) leave no request and no unknown tool call. This includes a later turn of a session restored from Cloud SQL that still holds the hostile metadata
  - A4: a rehearsal of the journey with one internal user
  - A5: a baseline of current request-to-order turnaround recorded from account managers
- **Verification:** live bounded evaluation (at most 25 cases × 3 runs); hosted staging run.
- **Execution scope:** pilot project, internal users only. Advertisers get access only through G12, after W6.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/advertiser-campaign-assistant.md. Read docs/architecture/advertiser-campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G12 — Pilot onboarding (go-live)

- **Phase and estimate:** 1b; hands-on 1–2, review 0–1, total 1–3; waits W6 (on G06's evidence), W8; owner Engineer
- **Outcome, contracts and decisions:** the five advertisers' named users are in the org-to-brand table and can sign in. Proves C2 for real accounts.
- **Scope:** table entries from W9, a welcome note with the support route, `AGENT_ENABLED` turned on for them.
- **Prerequisites:** W6 go-live approval; W8 IdP accounts.
- **Primary skill:** `adk-tool-auth-and-secrets`
- **Supporting skills:** none
- **Acceptance:**
  - A1 → C2: each advertiser's first user signs in and sees only their brands. A user from an org not in the table is refused
- **Execution scope:** production pilot access; needs W6.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G12 from docs/plans/advertiser-campaign-assistant.md. Read docs/architecture/advertiser-campaign-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases and record evidence here.`

### G07 — Booking replay discovery (phase 2)

Question: does the booking system accept an idempotency key or client
reference, support lookup by it, and what happens on a timeout? Run a bounded
staging experiment: send the same order twice with the same reference, kill
the connection mid-request, then look up by reference. Stop after one day or
when the answers arrive. Decision: mode A (replay or lookup supported) or mode
B (at-most-once dispatch, with sales ops reconciling by hand). Primary
`safe-api-tool-calls`; 3–6 h; needs W7 and W10 (staging write access); feeds G08 and G09.
- A1 → C5: a written finding per behaviour, with the staging evidence, and the selected mode recorded in the design (O5)

### G08 — Automated order placement (phase 2)

`/confirm` dispatches the order to the booking system from a durable
operation record keyed by proposal ID, under the G07 mode. Sales ops placement
becomes the fallback. Primary `safe-api-tool-calls`; 8–14 h.
- A1 → C1, C4: rights and quote are rechecked immediately before dispatch. An order for a stale or wider payload is refused
- A2 → C5: provider commits and the response is lost, or a duplicate confirm arrives. Exactly one order exists, the status is pending until reconciled, and no fresh dispatch happens without the guarantee
- A3 → C5: a rejection, unavailability, expired credential, 429 or malformed receipt each gives a typed outcome. A retry happens only when G07 proved it safe

### G09 — Booking status and reconciliation (phase 2)

Status reads booking receipts where lookup exists. A daily job flags requests
whose booking state disagrees with ours. Primary `safe-api-tool-calls`; 3–6 h.
- A1 → C6: a seeded mismatch (order placed and receipt lost, or a partial order) appears on the reconciliation report, and status shows "checking"

### G10 — Evaluation gate in CI (phase 2)

Run the G06 set in CI on prompt, model or tool changes. Fail on a grounding
drop. Add cases from pilot sessions (W11). Primary `adk-release-engineering`; 5–8 h.
- A1 → C10: a deliberately degraded prompt fails the gate by exit code

### G13 — Modification requests (phase 2)

Let advertisers request modified creatives where the grant allows it. Adds
`use: modified` (or levels, per O9) to terms, the card, the snapshot and the
export. Primary `adk-tool-interface-design`; 3–6 h; needs G05 and W12.
- A1 → C1, C12: a modification request on a grant that forbids it is denied with the reason. An allowed one carries `use: modified` through the card, request and export

### G11 — Traces and cost alerts (phase 2)

Cloud Trace through ADK OpenTelemetry with content capture off, token cost per
advertiser, and an alert on error rate and on spend. Primary
`adk-agent-observability`; 3–6 h.
- A1 → C11: an in-memory exporter test shows one span per agent, tool and model call with the session ID, and no content attributes

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Takedown when rights are revoked during a live flight | O11 names an owner who wants the assistant involved | The order keeps running until the rights or delivery team acts | `safe-api-tool-calls` |
| Catalogue search index or RAG | O3 shows more than about 2,000 assets per brand and channel | Lower recall | `adk-memory-architecture` |
| Per-advertiser API credentials | O2 answer allows it | C2 rests on our code alone | `adk-tool-auth-and-secrets` |
| Payment and delivery status | Those teams expose an API | Advertisers ask their account manager | `adk-agent-interoperability` |
| Content screening (Model Armor, SDP) | Personal data appears in chats | Sensitive text in sessions | `protect-adk-sensitive-data` |
| Ops page for sales ops (IdP-group gated) | Engineer's daily export takes more than 15 minutes a day, or more advertisers join | Placement depends on the engineer running the export | `adk-frontend-integration` |
| Canary and joint rollback | More than five advertisers | Revision rollback only | `adk-release-engineering` |
| Model migration off `gemini-3.8-flash` | A retirement date is announced | n/a until announced | `adk-model-and-output-contracts` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/advertiser-campaign-assistant.md) | Method, contracts and decisions |
| `docs/eval/summary.md` (G06, proposed) | Latest result per case |
| This plan | Remaining limits, deferred controls and evidence per goal |

## Open decisions for further planning

See the design's open decisions O1–O12 (O1 resolved). O6 (sales ops manual placement)
moves the cut line, and O5 decides G08's scope.

## Schedule check runs and changes

| Change after a failing run | Why it is true of the work |
| --- | --- |
| First run: 33–55 h, finish 9.4–16.1 days (exit 1) | Baseline |
| G05 ops page replaced by an engineer-run export and set-state command (G05 5–8 → 4–7) | Five advertisers make a CSV a day enough. An ops page moves to the later list |
| G05's own staging walkthrough with sales ops removed (4–7 → 4–6; finish 9.1–15.8 → 9.1–15.5). Covered by G06/A2, which now names the ops placement and C5 | It was the same hosted run done twice |
| Not done: shortening W5 or any other wait, dropping review, removing dependencies | Not allowed without the wait's owner confirming |


Independent plan review (fresh-context subagent using `assets/plan-review-prompt.md`, 2026-10-15). 18 findings, each settled:

| # | Finding | Settlement |
| --- | --- | --- |
| 1 | G04/A2 needs quotes (G03) and proposals (G05) | G04 blocked by G03. G04/A2 is limited to sessions and quotes. New G05/A9 covers proposals, `/confirm` and status. G05 4–6 → 5–7 |
| 2 | W1 needs the Cloud Run URL | W1 blocked by W5 |
| 3 | Sales-ops placement in G06/A2 is not scheduled | G06 `wait_days: 0-1`. Staging access for sales ops is part of W3 |
| 4 | Go-live approval comes before the evidence | G06 split: W6 follows G06, then new G12 onboarding (phase 1b) |
| 5 | Security review may need the built system | Kept as a design review (assumption Q12). Recorded as O7 with its effect |
| 6 | External IdP accounts not requested | New day-1 wait W8 before G12 |
| 7 | G03 needs G02's project and store | G03 blocked by G02 (no effect on finish) |
| 8 | Pilot inputs and GCP permissions not scheduled | New day-1 wait W9 (org-to-brand table, briefs, turnaround) before G06. W5 text widened. W2 includes network reachability |
| 9 | G07 needs booking staging write access | New phase-2 wait W10 before G07 |
| 10 | `mentions_only` entries redundant; G10 needs pilot data | Entries removed. New wait W11 (two weeks of pilot sessions) before G10 |
| 11 | No C2 test for proposals and status | G05/A9; action grid cites it |
| 12 | IdP duplicate n/a was wrong | G04/A6 (reused code, state or nonce) |
| 13 | IdP rejects and credential cells cited the wrong item | G04/A4 widened (`invalid_grant`, client secret) and cited |
| 14 | Cloud SQL untrusted-content n/a was wrong | G06/A3 widened to a restored session. Cell cites it |
| 15 | No malformed-rights-payload test | G03/A5 widened |
| 16 | Manual placement row under-tested | G05/A4 (expiry before placement), G05/A8 (payload check, `needs_attention`, manual duplicate check). G02/A2 covers revoked database access |
| 17 | The automated-booking what-if figures were wrong | Recomputed on the revised schedule. The what-if table now quotes the helper |
| 18 | The remedies no longer close the gap | Cut line moved: go-live (W6, G12) follows the build. The summary now says no 15-day go-live exists without cutting substance |

Rerun after the fixes: 33–53 h of 54 h, fits; build finish 9.4–16.5 days, 15-day calendar fits at the low end only; go-live 12.7–22.3 days.

### Revision 2 (2026-10-15): territory, flight dates, modification

The user reported that asset rights also depend on territory, flight dates and
whether the creative may be modified. Rows of one change each:

| Change | Why | Effect |
| --- | --- | --- |
| G01 5–8 → 7–10: `rights.evaluate` (D11), grant fixtures, boundary cases; new G01/A6 (missing terms, invalid codes, modification refused) | Coverage over territories × days is new logic, with a careful review | +2 h |
| G03 6–10 → 7–11: grant-record mapping, territories in quotes; G03/A2 and G03/A5 widened; blocked by new wait W12 | Real API shape and semantics are unknown | +1 h; W12 (3–5 days, requested day 1) |
| G05 5–7 → 6–8: terms in payload and card, terms snapshot (C12), export recheck (new G05/A10), `set-state` term match | Rights can narrow between confirm and placement; sales ops must place within the cleared terms | +1 h |
| G06 4–6 → 5–7: labelled set 15–20 → 20–25 cases with term extraction | The model now turns "summer, UK and Ireland" into terms | +1 h |
| New phase-2 G13 (modification requests, 3–6 h) | Pilot is as-is only (D12, Q15) | Phase 2 +3–6 h |
| Later list: the "territory, date and modification rights" row removed (now built). "Takedown when revoked during a live flight" added (O11) | The removed row is done, not dropped | — |
| Settled mention: G01 names W12 but does not depend on it (it builds on Q13–Q15) | `mentions_only: [W12]` | — |

Independent review of revision 2 (fresh-context subagent, 2026-10-15). 16 findings, each settled:

| # | Finding | Settlement |
| --- | --- | --- |
| 1 | G01's boundary cases rest on Q13 and Q14, and rework has no hours | Boundary rows marked provisional. New G03/A6 reruns them on W12's answers. G03 7–11 → 7–13. G01 still does not wait for W12 (`mentions_only` kept, with rework in G03) |
| 2 | No wait asks the O12 territory-pricing question | Added to W2's text |
| 3 | No aligned rights and booking test data | New day-1 wait W13 (3–5 days, assumed) blocks G03 |
| 4 | W9 not updated | W9 asks for 20–25 briefs with terms, and for Q15 confirmation |
| 5 | Evaluation cap of 20 below the 20–25 set | Cap raised to 25 × 3 |
| 6 | Export may not reach the rights API; W3 is silent on terms | Export runs as a Cloud Run job from the service image. W3 widened |
| 7 | No rights test at `propose_purchase` | Added to G05/A3. Map row updated |
| 8 | Rights outage at confirm or export undefined | Defined (refuse at confirm; hold at export) in C7. Tested in G05/A3 and G05/A10 |
| 9 | Start-equals-start allow, timestamp offsets and a started flight untested | G01/A2, G03/A5 and G05/A10 widened |
| 10 | Overlapping and per-territory grants, foreign fragments, snapshot of all IDs untested | G01/A2 and G05/A8 widened |
| 11 | "UK" is not ISO; modification refusal only scripted | Alias table (G01/A6, Q14). Alias and modification cases in the G06 set. G01 +0–1, G05 +0–1, G06 +0–1 h |
| 12 | Prompt said A1–A5; Resume listed W1–W7 | Fixed (A1–A6; W2–W5, W7–W10, W12, W13) |
| 13 | Map still named O1; the plan said O1–O6; the summary sentence was dropped | Map points at W12, O8 and O10. O1–O12 listed. The sentence is restored, reworded for revision 2 |
| 14 | The modification what-if said 19 days without G06 depending on G13 | Remodelled with G06 waiting for G13: 21 days |
| 15 | The 0.7-focus claim said 17, the reviewer found 16 | After the settled hours, the helper gives 17 (16 is low end only). Both rows are in the table |
| 16 | Automated booking not rerun | Rerun: 49–83 h, 13.6–24.1 days, 25 days |

Removed or weakened in revision 2, including the review fixes: **no** failure
row, grid cell, test, acceptance case, wait or floor item was removed. Weakened
in scope (not in safety): advertisers cannot request modified creatives in
phase 1. Acceptance items were changed only by widening them (G01/A2, G01/A5,
G01/A6, G03/A1, G03/A2, G03/A5, G05/A2, G05/A3, G05/A8, G05/A10, G06/A1).
One summary sentence was removed and then restored.

## Resume here

- **Next goal:** G01, licensed-asset search on a fake rights adapter. It needs no access or cloud.
- **Read first:** the design, then this plan's G01.
- **Next action:** on day 1, send W2–W5, W7–W10, W12 and W13 (people, not code), then start G01. Send W1 once W5 gives the Cloud Run URL.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 (Licensed-asset search, local) from docs/plans/advertiser-campaign-assistant.md.
Read docs/architecture/advertiser-campaign-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions and adk-model-and-output-contracts.
Work locally only, verify G01 acceptance A1-A6, and update
the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/advertiser-campaign-assistant.md.`
