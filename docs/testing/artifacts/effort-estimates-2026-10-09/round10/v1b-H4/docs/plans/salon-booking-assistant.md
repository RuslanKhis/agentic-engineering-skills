# Implementation plan: salon booking assistant (MVP)

Status: draft, ready goals identified
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan. Phase 1 scope and acceptance live in the tickets under
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/).

## Summary for the reader

- **Profile and phase 1:** MVP or pilot. Phase 1 puts **booking** live on
  the website for customers of **one pilot salon**. Every booking needs the
  customer's confirmation click, the commit is idempotent, and uncertain
  outcomes are reconciled. **Move and cancel** come first in phase 2 (G10,
  G11), followed by the roll-out to all five salons (G12). Until then,
  customers move and cancel by phone, as they do today.
- **Effort and finish:** phase 1 is 50–75 human hours against 112.5 h of
  capacity after a 25 % reserve. With these three people and these
  dependencies, it finishes in **6.1–9.1 working days against 10, so it
  fits**. Book, move and cancel together would take 7.7–11.5 days and fit at
  the low end only (see the what-ifs below).
- **Largest risks:**
  1. The booking API may lack idempotency keys or an atomic move (design O1,
     O3). G01 settles this in the first two days; owner Dev A.
  2. Go-live needs the salon owner's approval and privacy wording (W1, 3–5
     days). Dev C requests it on day 1.
  3. Every number rests on assumed hours and budget (design A1, A2). If the
     team has fewer than 5 focused hours a day, the launch slips.
- **Decisions needed from you:**
  - Confirm the cut line, or choose one of the remedies below that keep move
    and cancel in the first two weeks.
  - Confirm or correct A1 to A12.
  - Accept R1 (reference plus phone as proof of ownership) for phase 2, or
    ask for OTP first (O4).
- **Next prompt:** the G01 run prompt under "Resume here" (identical to the ticket's own run block).

## Destination and constraints

The end result: customers of five salons book, move and cancel on the website
without staff. Spend is bounded and no write goes through unconfirmed.
Non-goals and the accepted stack are in the design.

The repository was empty when inspected, so no ADK version is pinned yet.
Working assumption: `google-adk==2.8.0`, the specialists' compatibility
baseline. Confirming it against the chosen pin is an acceptance item of G02.

The model ID is open (design O2) and is pinned in G02. Every later goal
inherits it, and changing it counts as a release.

Authorization: this session is design only. Cloud provisioning (G06) and the
production launch (G09) run later inside their goals, with the team's own GCP
and booking API credentials. Each needs its own go-ahead.

## Delivery profile and capacity

Profile: MVP or pilot (see the design's delivery constraints). The phase 1 code
is kept.

The numbers rest on these assumptions (design A1):

- 3 developers, full time
- 5 focused hours a day each
- 10 working days
- 25 % of each day held in reserve

Every estimate already includes the **×1.5 multiplier for a team new to ADK**,
applied to hands-on and review alike. No GCP setup day is added, because A1
assumes the team has used GCP before.

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Booking live at the pilot salon, with confirmed, idempotent writes | G01 to G09, wait W1 | 50–75 | 3 × 5 h × 10 days = 150 h; 112.5 h after the 25 % reserve |
| 2, complete and graduate | Move and cancel, all five salons, then the graduation conditions | G10 to G17 | 38–61 | Starts as soon as phase 1 frees people. G10 can start in phase 1 slack |

| Person (suggested) | Phase 1 goals | Hours | Capacity after reserve |
| --- | --- | --- | --- |
| Dev A, owns the API and write safety | G01, G03, G08 | 18–27 | 37.5 |
| Dev B, owns the agent and tools | G02, G04 | 10–16 | 37.5 |
| Dev C, owns the platform, chat API and launch | G05, G06, G07, G09 | 22–32 | 37.5 |

Dev B is lightly loaded because the calendar, not the hours, limits phase 1.
I tried 81 owner assignments for the movable goals; none brought the full
scope inside 10 days (best 7.7–11.5). Dev B's remaining time goes to G10
(phase 2), started right after G04. G10 blocks nothing in phase 1.

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: salon owner go-live approval and privacy notice wording (requested day 1)
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
- goal: G02
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  mentions_only: [G05]
- goal: G03
  phase: 1
  hands_on: 4-5
  review: 2-4
  total: 6-9
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev B
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  mentions_only: [G05, G10]
- goal: G05
  phase: 1
  hands_on: 5-7
  review: 2-3
  total: 7-10
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  mentions_only: [G02, G03, G06]
- goal: G06
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G07
  phase: 1
  hands_on: 4-5
  review: 1-2
  total: 5-7
  owner: Dev C
  blocked_by: [G03]
  calendar_waits: none
  wait_days: 0
  handoff: 1
  mentions_only: [G06, W1]
- goal: G08
  phase: 1
  hands_on: 5-7
  review: 1-2
  total: 6-9
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  mentions_only: [G02, G04]
- goal: G09
  phase: 1
  hands_on: 4-5
  review: 1-2
  total: 5-7
  owner: Dev C
  blocked_by: [G04, G05, G06, G07, G08, W1]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G10
  phase: 2
  total: 6-8
  blocked_by: [G02]
- goal: G11
  phase: 2
  total: 5-8
  blocked_by: [G03, G09, G10]
- goal: G12
  phase: 2
  total: 2-4
  blocked_by: [G09]
- goal: G13
  phase: 2
  total: 6-10
  blocked_by: [G10]
- goal: G14
  phase: 2
  total: 5-8
  blocked_by: [G08]
- goal: G15
  phase: 2
  total: 5-9
  blocked_by: [G09]
- goal: G16
  phase: 2
  total: 5-8
  blocked_by: [G08]
- goal: G17
  phase: 2
  total: 4-6
  blocked_by: [G09]
```

The schedule was checked with `check_schedule.py --plan
docs/plans/salon-booking-assistant.md --tickets
docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev
A=5" --person "Dev B=5" --person "Dev C=5"` on 2026-10-14, using Python 3.12.
Results:

- Phase 1: 50–75 h; it fits the capacity.
- Longest dependent chain: G01 → G03 → G04 → G09, 6.1–9.1 working days.
- Finish: 6.1–9.1 working days; it fits the calendar.
- Phase 2 (`--phase 2`): 38–61 h.

### What-ifs run with the helper (same people and reserve unless stated)

| Variant | Phase 1 delivers | Finish (working days) | Fits 10 days? |
| --- | --- | --- | --- |
| **Chosen** (above) | Booking live at the pilot salon | 6.1–9.1 | yes |
| First draft: everything in phase 1, 4 goals on Dev A | Book, move and cancel at five salons | 7.7–12.0 | low end only |
| Full scope, best of 81 owner assignments | Book, move and cancel | 7.7–11.5 | low end only |
| Full scope, draft assignment (G07, G08 on Dev A), Dev A at 6 h a day | Book, move and cancel | 7.5–11.2 | low end only |
| Cut move and cancel only, without splitting the launch | Booking | 8.0–12.0 | low end only |
| **Remedy 1:** full scope, every person at 6 focused h a day | Book, move and cancel | 6.4–9.6 | yes, if the hours are real |
| **Remedy 2:** full scope, 12 working days | Book, move and cancel | 7.7–11.5 | yes, by day 12 |

Only the chosen cut and remedies 1 and 2 close the gap. More owners or
reassignments do not, because the booking chain (G01 → G03 → G04 → launch)
alone takes 9.1–9.6 days at the high end.

### Changes made after failing runs

| Change | Why it is true of the work |
| --- | --- |
| Removed empty `owner:` lines on W1 and phase 2 entries | The helper read them as a fourth person and inflated capacity |
| Split uncertain-outcome reconciliation and the front-desk runbook (G07) out of the operation service (G03) | Reconciliation needs only G03's operation table, and a second person can build it in parallel |
| Built the evaluation runner (G08) against the agent-factory interface with a stub, so it can start on day 1 | The cases come from the service catalogue and the journey, not from the finished agent. The live run happens in G09 |
| Moved ownership verification and move/cancel past the cut line (G10, G11) | They lengthened the chain past 10 days in every assignment tried |
| Moved the roll-out to all five salons out of the launch goal (G12) | It follows the pilot days, so it cannot sit on the phase 1 chain |

If time runs out early, finished goals stay useful in this order:

1. G01 → G02: the read-only assistant can be shown.
2. G03 → G04 → G07: booking is safe end to end, in staging.
3. G05, G06 → G09: live.

If phase 1 runs at its low end, Dev B finishes G10, and G11 (move and cancel
at the pilot salon) can still land inside the two weeks.

## Implementation map

| Decision | Component and integration point (proposed, greenfield) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D3, A5 | `app/booking_client.py` (typed client, timeouts, error mapping) + `app/fake_booking_api.py` | Secret Manager holds the API key | `safe-api-tool-calls` | API idempotency and move semantics (O1, O3) |
| D1, D7, D8 | `app/agent.py` factory → `LlmAgent` with tools in `app/tools/`; `RunConfig(max_llm_calls=8)` | Vertex AI model endpoint | `adk-workflow-design` | ADK 2.8.0 constructor names; model ID (O2) |
| D2, D3 | `app/operations.py` `OperationService.propose/confirm/get` on the `operations` table; `reconcile` in G07 | Cloud SQL | `safe-api-tool-calls` | Real Postgres claim test |
| D4 | `verify_booking` tool writing `app:verified_refs`; check in `OperationService.confirm` (G10) | — | `adk-tool-auth-and-secrets` | That the model cannot write the `app:` prefix in 2.8.0 |
| D5, D8, D9 | `app/api.py` FastAPI: `/chat`, `GET /operations/{id}`, `POST /operations/{id}/confirm`, admission middleware, cookie session, log filter; `web/widget.js` | Cloud Run | `adk-frontend-integration` | `DatabaseSessionService` on Postgres under 2.8.0 |
| D6, D8, D9 | Cloud Run service, Cloud SQL, service account, Secret Manager, budget alert, retention job, log-based alerts, `release.json` | Cloud Run, Cloud SQL, Scheduler, Logging, Billing | `deploy-adk-on-google-cloud` | Region and Cloud SQL price (O5) |
| D10 | Staging run, pilot cutover, rollback drill | Cloud Run revisions | `deploy-adk-on-google-cloud` | — |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | Owner | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W1 Salon owner go-live approval and privacy wording | 1 | wait, 3–5 days | 0 | — | — | Dev C requests it on day 1 | ready to request |
| [G01 Booking API client, fake and contract](../tickets/salon-booking-assistant/G01-booking-api-client-and-fake.md) | 1 | discovery + implementation | 6–9 | — | `safe-api-tool-calls` | Dev A | ready |
| [G02 Assistant finds services and free slots](../tickets/salon-booking-assistant/G02-assistant-finds-slots.md) | 1 | implementation | 4–7 | G01 | `adk-workflow-design` | Dev B | blocked by G01 |
| [G03 Confirmed, idempotent operations](../tickets/salon-booking-assistant/G03-confirmed-idempotent-operations.md) | 1 | implementation | 6–9 | G01 | `safe-api-tool-calls` | Dev A | blocked by G01 |
| [G04 Customer books through the assistant](../tickets/salon-booking-assistant/G04-customer-books.md) | 1 | implementation | 6–9 | G02, G03 | `adk-tool-interface-design` | Dev B | blocked |
| [G05 Chat API and embeddable widget](../tickets/salon-booking-assistant/G05-chat-api-and-widget.md) | 1 | implementation | 7–10 | — | `adk-frontend-integration` | Dev C | ready |
| [G06 Staging environment on GCP](../tickets/salon-booking-assistant/G06-staging-environment.md) | 1 | implementation | 5–8 | — | `deploy-adk-on-google-cloud` | Dev C | ready (needs GCP project access) |
| [G07 Uncertain-outcome reconciliation and front-desk runbook](../tickets/salon-booking-assistant/G07-reconciliation-and-runbook.md) | 1 | implementation | 5–7 | G03 | `safe-api-tool-calls` | Dev C | blocked by G03 |
| [G08 Evaluation set and runner](../tickets/salon-booking-assistant/G08-evaluation-set.md) | 1 | implementation | 6–9 | — | `adk-agent-evaluation` | Dev A | ready |
| [G09 Staging run and pilot launch](../tickets/salon-booking-assistant/G09-staging-and-pilot-launch.md) | 1 | implementation | 5–7 | G04 to G08, W1 | `deploy-adk-on-google-cloud` | Dev C | blocked |

### Phase 2: complete the journey, then graduate (not ticketed; phase 1 results will change these)

- **G10 Customer proves they own a booking and sees it.** `verify_booking` and
  `get_my_booking`, the `app:verified_refs` key and lockouts (D4). Primary
  `adk-tool-auth-and-secrets`, supporting `adk-tool-interface-design`. 6–8 h.
  Acceptance: an unverified reference is refused, 5 failures lock the session
  out, and the model cannot set the state key (I2, I5).
- **G11 Customer moves or cancels at the pilot salon.** `propose_move` and
  `propose_cancel` through the G03 operations. A two-step move, if O3 requires
  one, gets partial-failure rows. Primary `safe-api-tool-calls`, supporting
  `adk-tool-interface-design`. 5–8 h. Acceptance: a confirmed move gives one
  API update, and a staff-cancelled original is refused at confirm.
- **G12 Roll out to all five salons.** Review the pilot data, embed the widget
  on all salon pages, record the baseline. Primary
  `deploy-adk-on-google-cloud`. 2–4 h. Acceptance: each salon's slots are
  bookable on production, with no increase in front-desk corrections over the
  pilot days.
- **G13 One-time-code verification** (ends R1). Primary
  `adk-tool-auth-and-secrets`. 6–10 h. Acceptance: move or cancel without a
  valid code sent to the phone on file is refused.
- **G14 Evaluation gate in CI.** Primary `adk-release-engineering`, supporting
  `adk-agent-evaluation`. 5–8 h. Acceptance: a prompt change below the G08
  baseline fails CI by exit code, with a per-run cost cap.
- **G15 Traces, token cost and SLO alerts.** Primary
  `adk-agent-observability`. 5–9 h. Acceptance: one span per agent, tool and
  model call with the `session_id`, and an alert on the completed-booking
  ratio.
- **G16 Adversarial suite.** Primary `adk-agent-security`. 5–8 h.
  Acceptance: injected service text and attempts on another customer's
  booking produce 0 booking API writes.
- **G17 Abuse controls on new bookings.** Primary
  `adk-operational-guardrails`. 4–6 h. Acceptance: more than N unconfirmed
  bookings per phone per day are refused, with N taken from pilot data.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Streaming replies | Measured p75 for a complete reply > 6 s | Slower perceived replies | `adk-frontend-integration` |
| Model Armor or SDP screening | Free-text notes sent to the API, or abuse seen | Phone numbers typed into chat reach the model | `protect-adk-sensitive-data` |
| Model migration | The G02 model's retirement date within 90 days | — (dated) | `adk-release-engineering` |
| Preferred-stylist memory | > 10 % of conversations ask for "my usual" | Customers repeat their preference | `adk-memory-architecture` |
| Canary releases and joint rollback | > 500 conversations a day, or a bad release | Whole-revision rollback only | `adk-release-engineering` |
| Cost and latency tuning | Cost per completed booking > USD 0.05 | — | `optimise-adk-on-google-cloud` |
| SMS or WhatsApp channel | Salon owners ask for it | Web only | `adk-frontend-integration` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| The design | Method and decisions (D1 to D10, I1 to I7) |
| `evals/README.md` (from G08) | Latest result per evaluation case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See design O1 to O5. O4 (accepting R1) and the cut line can change what phase 1 delivers.

## Resume here

- **Next goal:** G01, booking API client, fake and contract. Nothing blocks
  it, and every build goal on the chain depends on its interface.
- **Read first:** the design, this plan, the G01 ticket.
- **Next action:** read the booking API's routes for availability, create,
  update, cancel and lookup, and how it handles idempotency.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-client-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

On day 1, in parallel:

- Dev A starts G01.
- Dev C starts G05 and G06 and requests W1.
- Dev A takes G08 after G03. Dev B starts G02 as soon as G01's client interface is merged.

After that: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
