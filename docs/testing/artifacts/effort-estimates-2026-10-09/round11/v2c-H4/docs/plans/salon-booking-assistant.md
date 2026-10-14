# Implementation plan: salon booking assistant (MVP)

Status: draft, reviewed once by an independent reviewer (findings settled in
the change table below); ready goals: G01, G02, G03, G06 on day 1.
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; phase 1 goals live in their tickets under
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/).

## Summary for the reader

- **Profile and phase 1:** MVP or pilot. Phase 1 puts the assistant live for
  logged-in customers of **one pilot salon**: book, move and cancel through the
  existing booking API, each change confirmed by the customer in the widget.
- **Effort and finish:** 69.5–109 human hours against 135 h of capacity after a
  25 % reserve: the hours fit. Finish **7.2–11.7 working days**. That fits a
  12-working-day date; against the requested 10 days it fits **only at the low
  end**. No owner assignment or tested scope cut brings the high end under 10
  (best found: 10.2 days, see the change table).
- **Cut line:** phase 1 = G01–G09 (pilot salon live). Phase 2 starts with G10
  (other four salons after one clean pilot day). The pre-launch evaluation set
  is 15 cases; the full set runs in CI in phase 2 (G11).
- **Largest risks:** (1) the website token cannot be verified by our backend
  (Q2) and G03 needs a one-time-code login: +8–14 h, finish 9–14.8 days, so
  settle Q2 before day 1; (2) the booking API has no idempotency key or atomic
  reschedule: more reconciliation work, owned by G01 and G04; (3) the salon
  chain's sign-offs (W1, W2) or the GCP approval (W0) take longer than
  assumed: request all of them on day 1.
- **Decisions needed from you:** accept a 12-working-day pilot date or name
  what to drop; confirm Q2, Q7 and Q16 in the design; approve the GCP project
  use (W0) and ask the salon chain for W1 on day 1.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md.`

## Destination and constraints

Destination: a logged-in customer completes book, move or cancel in chat, and
the booking system holds exactly the confirmed change. Non-goals: see the design.
Greenfield: the repository holds no application code yet; every module path
below is **proposed**. Working pins all goals inherit: `google-adk==2.8.0`
(design D11, confirmed in G02/A10), model `gemini-3.8-flash` on Vertex AI
(design D7, re-checked in G01/A3), prompt version `v1` in `assistant/prompts/`.
Authorization: this session was design only; no cloud resources exist or were
created. G07 and G09 wait for the team's GCP approval (W0); G09 also waits for
the salon chain (W1, W2).

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Pilot salon live with safe book/move/cancel | G01–G09, waits W0–W2 | 69.5–109 | 3 × 6 h × 10 days = 180 h; 25 % reserve → 135 h |
| 2, graduate and harden | All five salons, full eval set in CI, retention, SLOs, security suite | G10–G14 | 28.5–48.5 | When phase 1 is live |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify), with the ×1.5 new-to-ADK multiplier already applied to
every goal. Review is heavier on G03 and G04 (authorization and writes).

| Person | Goals | Hours | Capacity after reserve (10 days) |
| --- | --- | --- | --- |
| Dev A (agent, model, deployment) | G02, G07 | 19.5–30 | 45 |
| Dev B (identity and frontend) | G06, G03, G05 | 23.5–39.5 | 45 |
| Dev C (booking API and writes) | G01, G04, G08, G09 | 26.5–39.5 | 45 |

The finish is set by Dev B's serial work (G06, G03, G05) and by the chain
G03 → G07 → G08 → G09. Dev A has the most slack and pairs on G08 when it runs
long.

```yaml
- goal: W0
  phase: 1
  total: 0
  owner: ""
  blocked_by: []
  calendar_waits: GCP resource approval for the existing project (Vertex AI, Cloud Run, Cloud SQL database, secrets); request day 1
  wait_days: 1-3
- goal: W1
  phase: 1
  total: 0
  owner: ""
  blocked_by: []
  calendar_waits: salon chain sign-off on cutoff rules, consultation-only services, privacy notice and pilot salon; request day 1
  wait_days: 3-5
- goal: W2
  phase: 1
  total: 0
  owner: ""
  blocked_by: [G05, G06]
  calendar_waits: salon chain sign-off on customer-facing wording (prompt v1 replies and widget status messages)
  wait_days: 1-2
- goal: G01
  phase: 1
  hands_on: 4.5-6
  review: 1-2.5
  total: 5.5-8.5
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  mentions_only: [G02]
- goal: G02
  phase: 1
  hands_on: 5-7
  review: 3-5
  total: 8-12
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  mentions_only: [G03, G04, G08]
- goal: G03
  phase: 1
  hands_on: 5-8
  review: 3-7
  total: 8-15
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  mentions_only: [G02, G06, G07]
- goal: G04
  phase: 1
  hands_on: 6-9
  review: 6-9
  total: 12-18
  owner: Dev C
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  mentions_only: [G02, G06, G07, wait]
- goal: G05
  phase: 1
  hands_on: 5.5-8.5
  review: 1-2
  total: 6.5-10.5
  owner: Dev B
  blocked_by: [G01, G02, W0]
  calendar_waits: W0
  wait_days: 0
  handoff: 1.5
- goal: G06
  phase: 1
  hands_on: 6-9
  review: 3-5
  total: 9-14
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  mentions_only: [G03, G04]
- goal: G07
  phase: 1
  hands_on: 8-12
  review: 3.5-6
  total: 11.5-18
  owner: Dev A
  blocked_by: [G02, G03, W0]
  calendar_waits: W0
  wait_days: 0
  handoff: 1
  mentions_only: [G04, G08]
- goal: G08
  phase: 1
  hands_on: 6-8
  review: 1.5-2.5
  total: 7.5-10.5
  owner: Dev C
  blocked_by: [G02, G03, G04, G05, G06, G07]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G09
  phase: 1
  hands_on: 1-1.5
  review: 0.5-1
  total: 1.5-2.5
  owner: Dev C
  blocked_by: [G08, W1, W2]
  calendar_waits: W1 and W2
  wait_days: 0
- goal: G10
  phase: 2
  hands_on: 1-1.5
  review: 0.5-1
  total: 1.5-2.5
  owner: Dev C
  blocked_by: [G09]
  calendar_waits: one clean pilot day
  wait_days: 1
```

Schedule check, run 2026-10-15 with Python 3.11 (the system `python3` is 3.9):
`python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --design docs/architecture/salon-booking-assistant.md --days 12 --reserve 0.25 --person "Dev A=6" --person "Dev B=6" --person "Dev C=6"`
→ 69.5–109 h, fits capacity (162 h after reserve over 12 days; 135 h over
10); finish 7.2–11.7 working days; calendar fits (exit 0). Loads: Dev A
19.5–30 h, Dev B 23.5–39.5 h, Dev C 26.5–39.5 h. The same command with `--days 10` reports "low end only"
(exit 1).

### Changes after failing runs and after the independent review

One row per change; finish is the high end in working days. None removes a
review or a wait; scope moved is listed with where it went.

| Change | Why | Finish |
| --- | --- | --- |
| First draft (G04 after G02, G06 after G03 and G04, G07 after G02 and G03, all-salon launch in phase 1) | — | 13 |
| G04 and G06 build against the frozen contracts D5 and D8 with fixtures; integration and 2 h handoff moved into G08 | Removes waiting on another person's code | 11.6 |
| All-salon enablement moved to phase 2 (now G10) | Graduation step after a clean pilot day | 8.9 |
| G08 depends on G03 (found by the helper's mention check) | G08 deploys the gateway | 11.6 |
| Pre-launch eval set cut to 15 cases; 30 or more move to G11 | Scope cut that keeps a measured set per action | 10.2 |
| Runbook writing moved from G08 to G07 (G07 +1 h; G08 −1 h, with the remaining 0.5 h restored after review C5) | Writing does not need the integrated system | 9.9 |
| Review P1: W1 split into W1 (rules, privacy, pilot salon; day 1) and W2 (wording, after G05 and G06); launch split out of G08 as G09 | Wording does not exist on day 1 | see last row |
| Review P2, P3, V3: G07 deploys the gateway, so it waits for G03 (+1 h handoff); alerts fire from synthetic lines in the frozen D4 log schema, and again from the real executor in G08/A2 | Deploy checks must cover the real entrypoint | see last row |
| Review P4, V8: kill switch, salon flags, `GET /config` added to G03 (+2–3 h) as G03/A9 | Nobody built them | see last row |
| Review P5, P8, P11, P13: staging credential, seed script, consultation-only list source, test inbox and audit log added to G01 (+1.5–2.5 h); ADK pin fixed in design D11 and confirmed in G02/A10 instead of a blocking setup step; G05 +1–2 h for case data and now waits for G01 | Prerequisites with no owner | see last row |
| Review P6: GCP approval as wait W0 (1–3 days, assumed) before G05 and G07 | Outside approval had no wait | see last row |
| Review P12: first-real-booking check moved to G10's clean-day window | It waits on a customer | see last row |
| Review V2, V4, V5, V6, V7: G07/A8 (connection limit, +0.5–1 h), G02/A9 adds 429, G02/A10 (malformed and wrong-target arguments), G04/A12 (commit outcome unknown), G03/A8 widened | Grid cells cited items that did not test them | see last row |
| Searched all 2,187 owner assignments of G01–G07 after the review changes, with and without deferring traces and simplifying the move path | Best possible 10.2 days, and only with both cuts and a reshuffle that puts G03 and G07 on other people; with the chosen owners those cuts do not change the finish | 10.2 best |
| Kept full scope; date of 12 working days recorded as open decision Q15 | No cut that keeps the floor gets under 10 at the high end | 11.7 |

Mentions settled: G04's "credential from" is G01/A5, which G04 already waits for, so it is listed as `wait` under `mentions_only`; G01 names G02/A10 only as the place the pin is confirmed.

Review items settled without a schedule change: P7 (the team maintains the
website, assumption Q16; embedding is in G06), P9 (rules are configuration,
values confirmed in W1 before G09), P10 (Q2 must be settled before day 1),
P14 (the missing contract parts, `/config`, CORS and the log schema, are now
in the design), C1–C4 (text corrected).

**If time runs short.** Goals are ordered so each finished one is useful:
G01 + G04 give a tested write path; G02 + G03 a safe read-only assistant;
G06 + G07 make it reachable on staging. What-ifs for slips, from the helper:

| Remedy | Finish (working days) |
| --- | --- |
| None (chosen owners) | 7.2–11.7 |
| G05 moved from Dev B to Dev A | 7.8–12.6 (worse) |
| G06 moved from Dev B to Dev A | 8.3–13.3 (worse) |
| Q2 needs one-time-code login (G03 +8–14 h), chosen owners | 9–14.8 |

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D10 | `assistant/agent.py` `build_agent()` → `LlmAgent` with tools in `assistant/tools/{read,propose}.py`; `assistant/booking_client.py` | Vertex AI model endpoint | `adk-tool-interface-design` | Tool declaration dump on the pin |
| D2, D4, D5 | `assistant/executor.py` `confirm(proposal_id, customer_id)`; `assistant/store.py` (proposals, operations) | Cloud SQL | `safe-api-tool-calls` | Booking API replay contract (G01) |
| D3, D8, D9 | `assistant/gateway.py` FastAPI: token verification, session owner check, allowance, flags and `/config`, CORS; wraps `Runner` with `DatabaseSessionService` | Cloud SQL, website JWKS | `adk-tool-auth-and-secrets` | `DatabaseSessionService` behaviour on 2.8.0 |
| D8 | `web/widget/` embedded in the website's logged-in layout; `/chat`, `/proposals/{id}/confirm`, `/operations/{id}`, `/config` | Same Cloud Run service | `adk-frontend-integration` | Website CSP |
| D7, D11 | `Dockerfile`, CI workflow, `release-manifest.json`, Cloud Run services | Cloud Run, Secret Manager, Cloud Logging and Trace, Billing budget | `deploy-adk-on-google-cloud` | Region, connection limits |
| Instruction, eval | `assistant/prompts/v1.md`, `evals/cases.jsonl`, `evals/run.py`, `scripts/seed_staging.py` | Vertex AI (bounded spend) | `adk-agent-evaluation` | Eval interface on the pin |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | Owner | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W0 GCP resource approval | 1 | wait 1–3 d | 0 | — | — | team lead | request day 1 |
| W1 Salon chain: rules, privacy, pilot salon | 1 | wait 3–5 d | 0 | — | — | team lead | request day 1 |
| W2 Salon chain: wording | 1 | wait 1–2 d | 0 | G05, G06 | — | team lead | after G05, G06 |
| [G01 Booking API write contract, credential, seed data](../tickets/salon-booking-assistant/G01-booking-api-write-contract.md) | 1 | discovery | 5.5–8.5 | — | `safe-api-tool-calls` | Dev C | ready |
| [G02 Agent finds slots and proposes changes](../tickets/salon-booking-assistant/G02-agent-read-and-propose-tools.md) | 1 | implementation | 8–12 | — | `adk-tool-interface-design` | Dev A | ready |
| [G03 Verified customer, owned sessions, kill switch](../tickets/salon-booking-assistant/G03-verified-customer-sessions.md) | 1 | implementation | 8–15 | — | `adk-tool-auth-and-secrets` | Dev B | ready (Q2 assumed) |
| [G04 Confirmed changes reach the booking API once](../tickets/salon-booking-assistant/G04-confirmed-write-executor.md) | 1 | implementation | 12–18 | G01 | `safe-api-tool-calls` | Dev C | after G01 |
| [G05 Instruction and 15-case evaluation set](../tickets/salon-booking-assistant/G05-instruction-and-eval-set.md) | 1 | implementation | 6.5–10.5 | G01, G02, W0 | `adk-agent-evaluation` | Dev B | blocked |
| [G06 Chat widget](../tickets/salon-booking-assistant/G06-chat-widget.md) | 1 | implementation | 9–14 | — | `adk-frontend-integration` | Dev B | ready |
| [G07 Staging and production deployment](../tickets/salon-booking-assistant/G07-deploy-ci-observability.md) | 1 | implementation | 11.5–18 | G02, G03, W0 | `deploy-adk-on-google-cloud` | Dev A | blocked |
| [G08 End to end on deployed staging](../tickets/salon-booking-assistant/G08-integrate-on-staging.md) | 1 | implementation | 7.5–10.5 | G02–G07 | `adk-agent-evaluation` | Dev C | blocked |
| [G09 Pilot salon live](../tickets/salon-booking-assistant/G09-pilot-salon-launch.md) | 1 | implementation | 1.5–2.5 | G08, W1, W2 | `deploy-adk-on-google-cloud` | Dev C | blocked |

### Phase 2 (graduate and harden)

- **G10 All five salons.** After one pilot day with zero unresolved
  uncertain/partial operations, the team reviews the first real bookings
  against the booking system and enables the other four salon flags. Primary
  `deploy-adk-on-google-cloud`; 1.5–2.5 h plus 1 day wait. Check: each
  salon's first confirmed booking matches the booking system.
- **G11 Full evaluation set and live gate in CI.** Extend G05's 15 cases to
  30 or more (more phrasing, all five salons) and run them on prompt, model or
  tool changes with the model pinned; fail by exit code. Primary
  `adk-release-engineering`, supporting `adk-agent-evaluation`; 9–14 h.
  Check: a deliberately broken instruction fails the gate.
- **G12 Retention and erasure.** Daily job deletes sessions older than 30
  days and allowance rows older than 7; an erasure request removes a
  customer's sessions and proposals. Primary `adk-memory-architecture`,
  supporting `protect-adk-sensitive-data`; 4–8 h; **must ship before day 30
  after launch**. Check: a 31-day-old fixture session is gone and no other is.
- **G13 SLOs, dashboards, production samples to eval cases.** Completed
  operations / confirmations, tool-error rate by tool, tokens per completed
  operation; redacted sampled sessions become eval cases. Primary
  `adk-agent-observability`; 8–14 h. Check: an alert test leads to a stored session.
- **G14 Adversarial security suite.** Scripted-model attempts at
  cross-customer access, over-broad cancel and injected tool text, asserting
  no provider write. Primary `adk-agent-security`; 6–10 h. Check: the suite
  runs in CI and fails on a planted capability leak.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Staff reconciliation screen | More than 2 uncertain/partial ops a week | Manual SQL runbook | `safe-api-tool-calls` |
| Guest booking with one-time code | Client asks for logged-out booking | Logged-out customers phone or use the form | `adk-tool-auth-and-secrets` |
| Streaming replies | Measured p90 reply over 6 s | Whole replies only | `adk-frontend-integration` |
| Other channels (SMS, WhatsApp) | Client request after the pilot | Web only | `adk-agent-interoperability` |
| Preferences across conversations ("my usual") | Repeated customer requests | Customer restates preferences | `adk-memory-architecture` |
| Deposits or payments | Salon requires deposits for a service | Those services stay off chat | `safe-api-tool-calls` |
| Cost and latency tuning | Cost per completed operation above assumption | Spend within USD 300 by budget alert and kill switch | `optimise-adk-on-google-cloud` |
| Model migration | Lifecycle page announces a shutdown for `gemini-3.8-flash` | None until announced | `adk-model-and-output-contracts` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Method, decisions, failure coverage |
| `evals/results/` summary written by G05 and G08 | Latest result per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's open decisions. Q2 must be settled before day 1; the others
do not block starting G01, G02, G03 or G06.

## Resume here

- **Next goal:** G01, because the executor (G04), the evaluation set (G05)
  and every staging check depend on its credential, seed data and write
  contract. G02, G03 and G06 start the same day; the team lead requests W0
  and W1 on day 1.
- **Read first:** the design, then the G01 ticket.
- **Next action:** read the booking API's create, reschedule and cancel
  handlers and test idempotency on staging.

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-model-and-output-contracts.
Work against the booking API staging environment only, verify A1–A6, and record
evidence in the ticket.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
