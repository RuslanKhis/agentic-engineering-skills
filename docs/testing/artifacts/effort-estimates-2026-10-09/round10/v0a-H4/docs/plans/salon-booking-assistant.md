# Implementation plan: salon booking assistant (MVP)

Status: draft; ready goals identified (provisional on the design's assumed answers)
Architecture: [../architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; phase 1 goal detail lives in the
[tickets](../tickets/salon-booking-assistant/)

## Summary for the reader

- **Profile and phase 1:** MVP / pilot. Phase 1 lets signed-in customers of
  the pilot salon find, book, move and cancel their own appointments in a chat
  widget on the booking site, each change confirmed by the customer on a card,
  running on Cloud Run with spend caps, measured on a 30-case evaluation set.
- **Effort and finish:** 57–88 human hours, agent-assisted, against 112.5
  hours of capacity after a 25 % reserve (3 people × 5 h/day × 10 days):
  the hours fit. Finish 6.93–10.93 working days against 10: **low end only**
  (`check_schedule.py`, run 2026-10-14; see below). If G02 and G03 both run
  high, go-live (G07) lands on day 11. Of the remedies tried, only 6 focused
  h/day for all three people brings it inside (5.78–9.11 days).
- **Largest risks:** (1) customer token cannot be verified by our backend (O1)
  → D3 changes; G02 checks it on day 1. (2) A write times out and its outcome
  is unknown → D5 reconcile-by-read in G03; idempotency keys in G11.
  (3) Salon chain sign-off on privacy text, region and pilot (W1) arrives late
  → requested on day 1 in G01; G07 waits on it.
- **Decisions needed from you:** O1–O5 in the design, and confirm or move the
  cut line below.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-read-only-assistant.md.`
  G01 (Dev A), G02 (Dev B) and G05a (Dev C) have no prerequisites and start
  together on day 1; each ticket ends with its own prompt.

## Destination and constraints

Destination: the journey in the design, live at the pilot salon, then all
five. Non-goals and accepted stack: see the design's Purpose and D1–D9.
Repository: empty apart from `.claude/skills/`; every module below is
**proposed**. Pins the goals inherit: `google-adk==2.8.0` (working assumption,
confirmed in G01), model `gemini-3.8-flash` on Vertex AI (D2), prompt version
`v1` recorded in code. Changing any of them is a release, not a side effect.
Authorization: design only. No goal is authorized to provision cloud
resources or touch the production booking API until the team says so.

Proposed layout:

```text
assistant/
  agent.py           # LlmAgent factory, instruction v1 (G01)
  tools/booking.py   # read + propose tools (G01, G03)
  booking_client.py  # typed booking API adapter + fake for tests (G01)
  proposals.py       # proposal store, atomic claim, executor (G03)
  gateway.py         # FastAPI: auth, caps, /chat, /proposals/*/confirm (G02, G03, G06)
widget/              # chat widget for the booking site (G04)
evals/               # 30 labelled cases (G05a) + runner (G05)
deploy/              # Cloud Run, Cloud SQL, secrets, release manifest (G06)
```

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Pilot-salon customers change their own bookings safely; failures and cost visible | G01–G07, G05a (+ wait W1) | 57–88 | 3 × 5 h/day × 10 days = 150 h; 25 % reserve → 112.5 h |
| 2, harden and graduate | All five salons; eval gate; durable budgets; retention; idempotent API writes; SLOs | G08–G13 | 32–55 | When the team has time; G13 must ship within 30 days of launch |

Estimates include the 1.5× multiplier for a team new to ADK, applied to
hands-on and review alike, and handoff hours on the receiving goal. Calendar
waits are listed separately.

| Person | Goals | Hours | Their capacity (after reserve) |
| --- | --- | --- | --- |
| Dev A | G01, G03 | 18–27 | 37.5 |
| Dev B | G02, G06 | 15–25 | 37.5 |
| Dev C | G05a, G04, G05, G07 | 24–36 | 37.5 |

Owners are suggestions: Dev A for the agent and booking API work (whoever
knows the booking API best), Dev B for auth and GCP (whoever owns the
website login and the GCP project), Dev C for the widget, evaluation and
launch (whoever owns the booking site frontend).

Schedule block (the single source of each estimate; tickets copy it):

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: salon chain sign-off on privacy text, region (O3), pilot salon (O5) and baseline figures; requested in G01 on day 1
  wait_days: 3-5
- goal: G01
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G02
  phase: 1
  hands_on: 3-6
  review: 3-5
  total: 6-11
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G03
  phase: 1
  hands_on: 7-10
  review: 5-8
  total: 12-18
  owner: Dev A
  blocked_by: [G01, G02]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G04
  phase: 1
  hands_on: 5-8
  review: 2-3
  total: 7-11
  owner: Dev C
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G05a
  phase: 1
  hands_on: 3-5
  review: 1-1
  total: 4-6
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G05
  phase: 1
  hands_on: 4-5
  review: 1-2
  total: 5-7
  owner: Dev C
  blocked_by: [G01, G05a]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G06
  phase: 1
  hands_on: 6-9
  review: 3-5
  total: 9-14
  owner: Dev B
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G07
  phase: 1
  hands_on: 6-9
  review: 2-3
  total: 8-12
  owner: Dev C
  blocked_by: [G03, G04, G05, G06, W1]
  calendar_waits: none
  wait_days: 0
  handoff: 1
```

Schedule check, run 2026-10-14 with
`python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"`
(exit 1 because the calendar fits at the low end only):

- Phase 1: 57–88 h against 112.5 h after reserve; hours fit.
- Longest dependent chain: G01 → G03 → G07 (low, 6.93 days); G02 → G03 → G07 (high, 10.93 days).
- Finish: 6.93–10.93 working days of 10; **fits at the low end only**.
- No ticket/plan mismatches; every cross-person dependency has handoff hours.

Changes after failing runs and what-ifs (same command, owners as above unless stated):

| Change or what-if | Finish (working days) | Adopted? |
| --- | --- | --- |
| First draft (W1 had an empty `owner:`, read as a fourth person) | 7.73–11.73 | Fixed: key removed |
| Split evaluation labelling into G05a (needs only the tool contract D1, so no prerequisite); Dev C was idle until G01/G02 finished | 6.93–10.93 | **Yes** |
| + cut `propose_move` to phase 2 | 6.93–10.93 | No: doesn't move the finish |
| + cut move and evaluation to 15 cases | 7.33–11.33 | No: doesn't close |
| Split launch readiness (rollback, runbook) to Dev B as G07a | 7.2–11.47 | No: worse |
| Give G04 to Dev B | 8–12.8 | No: worse |
| Dev B at 6 h/day | 6.67–10.44 | Doesn't close |
| Dev A and Dev B at 6 h/day | 6.67–10.44 | Doesn't close |
| **All three at 6 focused h/day** | 5.78–9.11 | Closes; needs your confirmation that 6 h/day is real |

**Cut line (confirm or move):** phase 1 ships G01–G07 and G05a in 57–88 of
112.5 hours, live at the pilot salon in 7–11 working days. Scope cuts do not
shorten the critical chain (G02 → G03 → G07), so if G02 and G03 run high the
honest options are go-live on day 11 or 6 focused h/day for all three. The
floor (D4, D6, I1) is not cut. If time runs out early, the order G01 → G02 →
G03 still leaves a tested, confirmed-write agent runnable locally; G04 and G06
then make it reachable on staging.

## Implementation map

| Decision | ADK or application component and integration point | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D2 | `LlmAgent` factory in `assistant/agent.py`, invoked by the gateway's `Runner`; instruction templated from state | Vertex AI model endpoint | `adk-tool-interface-design` (G01) | ADK pin and model availability (O2) |
| D3 | Gateway middleware verifies site token → `customer_id` → session state; session owner check before `Runner.run_async` | — | `adk-tool-auth-and-secrets` (G02) | Token verification method (O1) |
| D4, D5 | `propose_*` tools write proposal rows; `/proposals/{id}/confirm` executor claims, re-checks, calls API once, reconciles uncertain outcomes | Cloud SQL table | `safe-api-tool-calls` (G03) | Reschedule semantics (O4) |
| D8 | JSON API + widget cards rendered from proposal status | — | `adk-frontend-integration` (G04) | Browser test on staging |
| D6, D7, D9 | `RunConfig(max_llm_calls=10)`, gateway caps, `DatabaseSessionService`, content capture off, release manifest | Cloud Run, Cloud SQL, Secret Manager, quota, budget alert, Cloud Trace | `deploy-adk-on-google-cloud` (G06) | Region (O3), prices on the day |
| Measured quality | 30 labelled cases (G05a), runner over the fake API (G05) | — (Vertex calls bounded) | `adk-agent-evaluation` (G05a, G05) | Thresholds set from first run |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| W1 Salon chain sign-off | 1 | wait (3–5 days) | 0 | — | — | request day 1 |
| [G01 Read-only assistant answers availability and "my appointments"](../tickets/salon-booking-assistant/G01-read-only-assistant.md) | 1 | implementation + pin check | 6–9 | — | `adk-tool-interface-design` | ready |
| [G02 Verified customer identity and session ownership](../tickets/salon-booking-assistant/G02-verified-customer-identity.md) | 1 | implementation (O1 checked first) | 6–11 | — | `adk-tool-auth-and-secrets` | ready |
| [G03 Book, move and cancel with customer confirmation](../tickets/salon-booking-assistant/G03-confirmed-writes.md) | 1 | implementation | 12–18 | G01, G02 | `safe-api-tool-calls` | blocked by G01, G02 |
| [G04 Chat widget with confirmation cards](../tickets/salon-booking-assistant/G04-chat-widget.md) | 1 | implementation | 7–11 | G02 | `adk-frontend-integration` | blocked by G02 |
| [G05a Label 30 evaluation conversations](../tickets/salon-booking-assistant/G05a-label-evaluation-cases.md) | 1 | implementation (labelling) | 4–6 | — | `adk-agent-evaluation` | ready |
| [G05 Evaluation runner and first measured result](../tickets/salon-booking-assistant/G05-evaluation-set.md) | 1 | implementation | 5–7 | G01, G05a | `adk-agent-evaluation` | blocked by G01 |
| [G06 Staging and production on Cloud Run with caps](../tickets/salon-booking-assistant/G06-cloud-run-with-caps.md) | 1 | implementation | 9–14 | G02 | `deploy-adk-on-google-cloud` | blocked by G02 |
| [G07 Pilot launch at one salon](../tickets/salon-booking-assistant/G07-pilot-launch.md) | 1 | implementation + release | 8–12 | G03–G06, W1 | `adk-release-engineering` | blocked |

### Phase 2 (coarse; phase 1 results will change these)

- **G08 Enable all five salons.** `adk-release-engineering`; 2–4 h. Accept:
  five trading days at the pilot with zero duplicate or wrong-customer writes,
  then config flip; eval pass rate unchanged.
- **G09 Evaluation gate in CI.** `adk-release-engineering` (+
  `adk-agent-evaluation`); 5–9 h. Accept: a PR that breaks a write-tool case
  fails CI by exit code; judge/model IDs pinned in the manifest.
- **G10 Durable per-customer token budget.** `adk-operational-guardrails`;
  6–10 h. Accept: budget survives restart and two instances; exhausted
  customer gets the call-the-salon reply without a model call.
- **G11 Idempotency keys on booking API writes.** `safe-api-tool-calls`;
  8–14 h (API change). Accept: replaying a confirm with the same proposal ID
  after a commit-then-timeout returns the original receipt and no second
  appointment.
- **G12 SLOs and alerts.** `adk-agent-observability`; 5–9 h. Accept:
  completed-change ratio and tool-error rate by tool on a dashboard with a
  burn-rate alert, from two weeks of baseline.
- **G13 Session retention and erasure.** `adk-memory-architecture`; 6–9 h.
  Accept: sessions and proposals older than 30 days are gone after the
  scheduled job; a customer erasure request removes theirs. **Due within 30
  days of launch.**

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Model Armor / SDP screening | Free-text notes reach the model, or an incident | Customer could paste sensitive data into chat; kept 30 days, not logged | `protect-adk-sensitive-data` |
| Streaming replies | Measured reply time hurts completion | Slower perceived replies | `adk-frontend-integration` |
| Canary releases | > ~200 conversations/day | Whole-traffic releases; rollback by revision | `adk-release-engineering` |
| SMS/WhatsApp channel | Customer demand | Web only | `adk-system-designer` (new identity design) |
| "My usual" preferences (Memory Bank) | Repeat customers ask | Customers restate preferences | `adk-memory-architecture` |
| Model migration | `gemini-3.8-flash` gets a shutdown date | — | `adk-model-and-output-contracts` |
| Production samples → eval cases | After G12 | Eval set drifts from real traffic | `adk-agent-observability` |
| Cost/latency tuning | p95 reply > 8 s or cost over A3 | — | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Decisions, guarantees, failures |
| `evals/summary.md` (created in G05) | Latest result per case |
| This plan | Schedule, remaining limits, deferred controls |

## Open decisions for further planning

Open decisions O1–O5 live in the design. Blocking: O1 → G02, O4 → G03,
O3 → G06/G07, O5 → G07.

## Resume here

- **Next goal:** G01, G02 and G05a in parallel (no prerequisites). G01 and
  G02 both feed the critical chain through G03.
- **Read first:** the design, then the ticket.
- **Next action (G01):** send the W1 request to the salon chain; confirm the
  ADK pin; write the booking client against the staging API docs.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
