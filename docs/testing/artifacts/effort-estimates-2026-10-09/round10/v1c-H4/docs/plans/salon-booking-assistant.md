# Implementation plan: salon booking assistant

Status: draft; ready goals identified (G01 first). Assumptions unconfirmed.
Architecture: [design](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; phase 1 goal scope and acceptance live
in the [tickets](../tickets/salon-booking-assistant/).

## Summary for the reader

- **Profile and phase 1:** MVP. By the end of week 2, signed-in customers of
  the five salons can book, move and cancel their own appointments in a chat
  widget on the website, each change confirmed by a button press and executed
  once through the booking API (G01 to G09).
- **Effort and finish:** phase 1 is 61–96 human hours against 135 hours
  of capacity after a 25 % reserve (fits). Finish is 6.67–10.44 working days
  against 10: **fits at the low end only**. At the high end Dev B's queue (G02,
  G07, G08, all after G01) holds back G09. The one remedy that closed the gap in
  a what-if: Dev B works 7 focused hours a day instead of 6 (finish 6.06–9.49).
  Cutting G05, or moving G05, G07, G08 or G09 to someone else, did not close it
  (what-if table below).
- **Largest risks:** (1) the website login may not give a verifiable token
  (OD1) — G01 finds out on day 1, fallback adds about a day to G03; (2) the
  booking API may lack idempotency keys or atomic reschedule (OD3) — G01
  decides, we own the API so we can add them, at the cost of G04/G05 running
  high; (3) the chain's sign-off on policy and data use (W1) is outside our
  control — requested on day 1.
- **Decisions needed from you:** confirm the Assumed answers in the design,
  especially Q2 (full-time capacity), Q7 (login), Q10/OD2 (data location) and
  Q11 (24-hour rule); confirm or move the cut line below.
- **Next prompt:** the run block in [G01](../tickets/salon-booking-assistant/G01-contracts-and-skeleton.md#run-this-ticket), repeated under Resume here.

## Destination and constraints

Destination: the journey in the design, live for signed-in customers of five
salons. Non-goals in phase 1: guest booking, payments, SMS or phone channels,
staff-facing tools, long-term memory, streaming. Authorization: design only in
this session; implementation, cloud setup and live tests need the team's own
go-ahead per goal. Inherited pins: google-adk 2.8.0 (to confirm in G01),
`gemini-3.8-flash` on Vertex AI (D2), prompt versioned as a file in the repo.

## Delivery profile and capacity

Profile: MVP or pilot (design, Delivery constraints).

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Customers book, move, cancel safely; team sees failures and cost | G01 to G09 | 61–96 | 3 people × 6 focused h/day × 10 days, 25 % reserve = 135 h |
| 2, harden | Graduation conditions (design) | G10 to G14 | 32 to 60 | When the team has time after launch |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify), already multiplied by 1.5 for a team new to ADK, rounded to
whole hours. Calendar waits are scheduled entries, not hours.

Owners by role (names to be filled in by the team):

- **Dev A, booking-API owner:** knows the existing booking API; takes the
  contracts, the write path and the launch.
- **Dev B, agent owner:** takes the agent, its tools, the evaluation and the
  GCP environment.
- **Dev C, web and identity owner:** takes sign-in, the chat API and the widget.

| Person or role | Goals | Hours | Their capacity |
| --- | --- | --- | --- |
| Dev A | G01, G04, G05, G09 | 27–41 | 45 h |
| Dev B | G02, G07, G08 | 19–30 | 45 h |
| Dev C | G03, G06 | 15–25 | 45 h |

Dev C has the most slack: when G06 is done, Dev C reviews G04 and G05 (the
money-like write path benefits from a second reader) inside Dev C's reserve,
and drafts the G09 runbook sections on sign-in and the widget.

Schedule block (the single source of each estimate; tickets copy it):

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: chain operations manager signs off policy, test stylist, data use and go-live date
  wait_days: 3-5
- goal: G01
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [W1]
- goal: G02
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  mentions_only: []
- goal: G03
  phase: 1
  hands_on: 5-9
  review: 2-4
  total: 7-13
  owner: Dev C
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  mentions_only: []
- goal: G04
  phase: 1
  hands_on: 7-10
  review: 3-5
  total: 10-15
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [G02, G06]
- goal: G05
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev A
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [W1]
- goal: G06
  phase: 1
  hands_on: 6-8
  review: 2-4
  total: 8-12
  owner: Dev C
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  mentions_only: [G04]
- goal: G07
  phase: 1
  hands_on: 5-8
  review: 1-2
  total: 6-10
  owner: Dev B
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: []
- goal: G08
  phase: 1
  hands_on: 6-9
  review: 2-3
  total: 8-12
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  mentions_only: []
- goal: G09
  phase: 1
  hands_on: 5-7
  review: 2-3
  total: 7-10
  owner: Dev A
  blocked_by: [G04, G05, G06, G07, G08, W1]
  calendar_waits: W1 sign-off before production switch-on
  wait_days: 0
  handoff: 2
  mentions_only: []
- goal: G10
  phase: 2
  total: 5-9
  owner: Dev B
  blocked_by: [G07, G09]
- goal: G11
  phase: 2
  total: 6-12
  owner: Dev C
  blocked_by: [G09]
- goal: G12
  phase: 2
  total: 8-14
  owner: Dev C
  blocked_by: [G09, G11]
- goal: G13
  phase: 2
  total: 6-12
  owner: Dev B
  blocked_by: [G07]
- goal: G14
  phase: 2
  total: 7-13
  owner: Dev A
  blocked_by: [G09, G11]
```

Longest dependent chain and finish range: longest chain at the high end G01 → G03 → G06 → G09,
9.33 working days; at the low end G01 → G04 → G05 → G09, 6 days. Finish with
these owners: 6.67–10.44 working days against 10. Run on 2026-10-14:

```text
python3.11 -I .claude/skills/adk-system-designer/scripts/check_schedule.py \
  --plan docs/plans/salon-booking-assistant.md \
  --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 \
  --person "Dev A=6" --person "Dev B=6" --person "Dev C=6"
```

If time runs out early, the goals stay useful in this order: G01 → G02 →
G04 → G03 → G06 → G08 → G07 → G09. If G05 is unfinished on launch day, launch
booking only and tell customers to call for changes (the what-ifs show this
does not move the finish, it only removes risk from launch day). G07 is not
cut: launching to customers without a measured evaluation breaks the MVP
depth. If the high end materialises and Dev B cannot add the hour, the launch
moves to day 11; say so to the chain when W1 is requested.

### Changes after schedule runs

| Run | Change | Why it is true of the work |
| --- | --- | --- |
| What-if | Finish (working days) | Closes the gap? |
| --- | --- | --- |
| Plan as written | 6.67–10.44 | no (low end only) |
| Dev B 7 focused h/day | 6.06–9.49 | **yes** |
| Dev C 7 focused h/day | 6.67–10.44 | no |
| Widget split from G06 to Dev B | 7.56–11.78 | no |
| G09 to Dev B, or to Dev C | 6.67–10.44 | no |
| G05 to Dev C (+1 h handoff) | 7.33–11.56 | no |
| G07 to Dev C (+1 h handoff) | 7.33–11.78 | no |
| G08 to Dev C | 7.56–12 | no |
| G08 to Dev A and G05 to Dev C | 7.33–11.56 | no |
| G08 to Dev A and G09 to Dev C | 7.56–11.56 | no |
| G08 without its G01 dependency | 6.67–10.44 | no |
| Cut G05 to phase 2 | 6.67–10.44 | no |

No dependency, wait or review was removed to make the numbers fit; the plan
keeps the original owners. G08 without the G01 dependency was only a what-if:
the environment needs G01's skeleton as its first deployable image.

## Implementation map

| Decision | Component and integration point (all proposed; repo is empty) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D10 | `app/booking/client.py` protocol + `tests/fakes/booking_api.py`; `app/models.py` (Proposal, Operation, Card) | — | `safe-api-tool-calls` | G01: ADK 2.8.0 interfaces, API contract |
| D1, D2 | `app/agent/agent.py` factory returning `App(LlmAgent(...))`; `app/agent/prompt.md`; `app/agent/tools.py` | Vertex AI model access | `adk-tool-interface-design` | Model location (OD2) |
| D3 | `app/api/auth.py` middleware → `customer_id` into session state at `create_session` | Secret Manager for nothing here (public key set) | `adk-tool-auth-and-secrets` | Token format (OD1) |
| D4, D5 | `app/ops/executor.py`, `app/ops/store.py` (Postgres), route `/proposals/{id}/confirm` | Cloud SQL | `safe-api-tool-calls` | Idempotency in API (OD3) |
| D6, D8 | `app/api/chat.py` around `Runner` with `RunConfig(max_llm_calls=12)`; `web/widget/` | Cloud Run | `adk-frontend-integration` | — |
| D7, D9 | `Dockerfile`, `deploy/` scripts, OpenTelemetry setup with content capture off | Cloud Run, Cloud SQL, Secret Manager, Cloud Trace, budget alert | `deploy-adk-on-google-cloud` | Current Vertex pricing and location |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | Ticket / state |
| --- | --- | --- | --- | --- | --- | --- |
| W1 Chain sign-off on policy, test stylist, data use, go-live | 1 | wait | 0 (3–5 days) | — | — | requested in G01 |
| G01 Contracts, skeleton and API facts | 1 | discovery + implementation | 4–7 | — | `safe-api-tool-calls` | [ticket](../tickets/salon-booking-assistant/G01-contracts-and-skeleton.md), ready |
| G02 Agent answers availability and "my appointments" and drafts proposals | 1 | implementation | 5–8 | G01 | `adk-tool-interface-design` | [ticket](../tickets/salon-booking-assistant/G02-read-only-agent-and-proposals.md), proposed |
| G03 Signed-in customer identity and session ownership | 1 | implementation | 7–13 | G01 | `adk-tool-auth-and-secrets` | [ticket](../tickets/salon-booking-assistant/G03-customer-identity.md), proposed |
| G04 Confirmed booking executes exactly once | 1 | implementation | 10–15 | G01 | `safe-api-tool-calls` | [ticket](../tickets/salon-booking-assistant/G04-confirmed-booking-write.md), proposed |
| G05 Confirmed move and cancel with 24-hour rule | 1 | implementation | 6–9 | G04 | `safe-api-tool-calls` | [ticket](../tickets/salon-booking-assistant/G05-move-and-cancel.md), proposed |
| G06 Chat API and website widget with cards and limits | 1 | implementation | 8–12 | G02, G03 | `adk-frontend-integration` | [ticket](../tickets/salon-booking-assistant/G06-chat-api-and-widget.md), proposed |
| G07 Labelled conversation evaluation before launch | 1 | implementation | 6–10 | G02 | `adk-agent-evaluation` | [ticket](../tickets/salon-booking-assistant/G07-evaluation-set.md), proposed |
| G08 Staging environment on Cloud Run with Cloud SQL | 1 | implementation | 8–12 | G01 | `deploy-adk-on-google-cloud` | [ticket](../tickets/salon-booking-assistant/G08-staging-environment.md), proposed |
| G09 End-to-end on staging, runbook and launch | 1 | implementation | 7–10 | G04–G08, W1 | `deploy-adk-on-google-cloud` | [ticket](../tickets/salon-booking-assistant/G09-launch.md), proposed |

### Phase 2 (harden and graduate)

#### G10 Evaluation gate in CI
Primary `adk-release-engineering` (supporting `adk-agent-evaluation`); 5–9 h.
G07 cases run on every prompt, tool-schema or model change; release manifest
records image, prompt hash, model and ADK version. Acceptance: a prompt change
that breaks a labelled case fails CI by exit code.

#### G11 SLOs and alerts on failed or uncertain operations
Primary `adk-agent-observability`; 6–12 h. SLIs: confirmed operations / confirm
clicks, tool-error rate by tool, tokens per completed booking, from the first
pilot week. Acceptance: an injected `uncertain` operation pages the on-call
developer within 5 minutes and links to the session.

#### G12 Guest availability browsing
Primary `adk-operational-guardrails` (supporting `adk-tool-auth-and-secrets`,
`adk-agent-security`); 8–14 h. Unsigned visitors can ask about availability,
read-only, with a per-IP allowance; booking still requires sign-in.
Acceptance: an unsigned session has no proposal tools in its declared tool list.

#### G13 Adversarial suite and threat-model review
Primary `adk-agent-security`; 6–12 h. 15+ scripted attacks (forged IDs,
injected bios, policy evasion) with deterministic no-write assertions.
Acceptance: suite runs in CI and every case asserts zero booking API writes.

#### G14 Latency measurement and streaming decision
Primary `optimise-adk-on-google-cloud` (supporting `adk-frontend-integration`);
7–13 h. Measure p50/p90 complete-reply time from pilot traffic; add streaming
text only if p90 exceeds 6 s. Acceptance: a dated measurement and a recorded
decision.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Session deletion job (30-day retention) | Before 30 days of pilot data exist | Sessions kept slightly longer than intended | `adk-memory-architecture` |
| Remembered preferences ("my usual with Sam") | Customers ask for it in pilot feedback | Customers repeat themselves | `adk-memory-architecture` |
| SMS / WhatsApp channel | Pilot shows demand off the website | Website-only reach | `adk-frontend-integration` |
| Deposits or payments | Chain asks for no-show protection | n/a until added; adds money-movement contracts | `safe-api-tool-calls` |
| Staff-facing reconciliation screen | More than a few uncertain or partial operations a week | Staff use the runbook query | `adk-frontend-integration` |
| `gemini-3.8-flash` migration and re-baseline | Retirement notice (expected around 2027-09) | None until announced | `adk-release-engineering` |
| Canary releases | Second salon chain or more than ~500 conversations a day | Full-traffic deploys with quick rollback | `adk-release-engineering` |
| Cost tuning, context caching | Tokens per booking above target after G11 | Slightly higher spend | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Decisions, invariants, failure handling |
| G07 evaluation summary (created by G07) | Latest result per labelled case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's Open decisions (OD1 to OD5); none blocks G01.

## Resume here

- **Next goal:** G01, because every other goal builds on its contracts and its
  API answers settle OD1 and OD3.
- **Read first:** the design, this plan, the G01 ticket.
- **Next action:** inspect the booking API's endpoints for create, reschedule,
  cancel and appointment lookup, and the website's login token.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-contracts-and-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

After that goal, `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
Dev B and Dev C can start G02, G03 and G08 in parallel as soon as G01 is done.
