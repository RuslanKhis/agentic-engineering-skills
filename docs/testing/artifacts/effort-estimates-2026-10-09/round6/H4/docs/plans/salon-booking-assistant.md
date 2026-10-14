# Implementation plan: salon booking assistant (MVP)

Status: draft. Ready goals have been identified; none has started.
Architecture: [../architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
(decisions D1–D7, invariants I1–I6, assumed answers A1–A13)
Continuation source of truth: this plan; tickets in `docs/tickets/salon-booking-assistant/`

## Summary for the reader

- **Profile and phase 1:** MVP or pilot. Signed-in customers of the chain can
  book, move and cancel real appointments through a chat widget in the
  existing booking web app. Every change waits for the customer to press
  Confirm, and each confirmed change runs once against the booking API. Go-live
  starts with one pilot salon and extends to all five on the last day (G10).
- **Effort and finish:** 57–90 human hours, agent-assisted. Capacity after the
  25% reserve is 112.5 h, so the **hours fit**. The finish is **6.9–11.9
  working days** against 10: it **fits only at the low end**. Two remedies
  close the gap (see "What-if runs"): add 2 working days, or launch only the
  pilot salon while every developer gives 6 focused h/day.
- **Largest risks:**
  1. The customer token or idempotency support may not exist (A7, A8).
     G01 settles both in its first hours.
  2. A booking API timeout could leave a change uncertain. G04 reconciles it;
     G13 automates the rest later.
  3. The model could propose wrong slots or intents. G07 and G08 measure this
     before go-live.
- **Decisions needed from you:** confirm the assumed answers (design §Assumed
  answers), especially A2 (hours per day), A7, A8 and A11. Choose a cut-line
  remedy. Name the pilot salon, and the person at the chain who approves
  go-live.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md.`

## Destination and constraints

Repository state: greenfield. It has no application code, no manifests and no
document convention, so this plan uses the skill's default paths. Working pins
come from D6: google-adk 2.8.0 and `gemini-3.8-flash` on Vertex AI. G01
confirms both. Changing either later is a release (G11), not a side effect.
The prompt is versioned with the code. Authorization: design only. Goals may
run locally and against the booking API's **staging** environment. Production
go-live in G10 needs the chain owner's approval and the user's explicit
go-ahead. No credentials appear in this repository.

Proposed layout (not yet created): `assistant/agent.py` (App and LlmAgent),
`assistant/tools/` (read and propose tools), `assistant/booking_client.py` and
`tests/fakes/booking_api.py`, `assistant/operations.py` (record and executor),
`gateway/app.py` (FastAPI), `web/widget/`, `evals/`, `deploy/`.

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Customers at five salons book, move and cancel safely; the team sees failures and token cost | G01–G10 | 57–90 | 3 × 5 h/day × 10 days, minus 25% = 112.5 h |
| 2, harden | Evaluation in CI, alerts on SLOs, automated reconciliation, human handoff, security review, baseline | G11–G16 | 22–40 | When the team has time after go-live |

Estimates are person-hours of human effort with a coding agent (hands-on, plus
review and verify). They include **1.5×** for a team new to ADK (A2), applied
to every figure. No extra GCP-setup day is added, because the team already
knows GCP (A12). Review is heaviest on G04 and G05 (writes and authorization)
and lightest on G06 and G09.

| Person | Suggested strengths | Goals | Hours | Capacity |
| --- | --- | --- | --- | --- |
| Dev A | Knows the booking API backend | G01, G03, G04, G10 | 21–33 | 37.5 |
| Dev B | Python, likes testing and data | G07, G02, G08 | 16–25 | 37.5 |
| Dev C | Frontend and web auth, some GCP | G05, G06, G09 | 20–32 | 37.5 |

Dev B has the most slack. If someone falls behind, B helps first with G09
(staging) or with G10's acceptance run, and the hours move with the work.
Names are roles: assign real people by these strengths.

```yaml
- goal: G01
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G02
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G03
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev A
  blocked_by: [G03, G05]
  calendar_waits: none
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 6-9
  review: 3-4
  total: 9-13
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G06
  phase: 1
  hands_on: 5-8
  review: 1-2
  total: 6-10
  owner: Dev C
  blocked_by: [G05]
  calendar_waits: none
  wait_days: 0
- goal: G07
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G08
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev B
  blocked_by: [G02, G03, G07]
  calendar_waits: none
  wait_days: 0
- goal: G09
  phase: 1
  hands_on: 4-7
  review: 1-2
  total: 5-9
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G10
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev A
  blocked_by: [G04, G06, G08, G09]
  calendar_waits: chain owner go-live approval, requested on day 1 in G01
  wait_days: 0-1
```

The schedule was checked on 2026-10-14 with:

```text
python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py \
  --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ \
  --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"
```

Result: 10 goals and 57–90 h. Hours fit: yes. Longest chain
G01 → G03 → G04 → G10, 5.6–9.8 working days. Finish 6.93–11.93 working days.
Calendar fits: **low end only**. Exit status 1, because the high end slips.
The binding constraint is Dev C's 32 h at the high end, followed by G10.

**What-if runs** (same command with the change shown):

| Change | Finish (working days) | Fits 10 days? |
| --- | --- | --- |
| Plan as written | 6.93–11.93 | Low end only |
| All three at 6 focused h/day | 5.78–10.11 | Low end only |
| Dev A and Dev C at 6 h/day | 6.49–11.22 | Low end only |
| Deadline 12 working days | 6.93–11.93 | **Yes** |
| Pilot salon only in phase 1, rest move to phase 2 (G10 −1 h), and all at 6 h/day | 5.56–9.89 | **Yes** |
| Pilot salon only, at 5 h/day | 6.67–11.67 | Low end only |

The 6 h/day remedies assume the developers clear other duties. Splitting the
goals on the longest chain was tried (see the change log) and did not close
the gap on its own.

**Changes made after failing runs:**

| Change | Why it is true of the work |
| --- | --- |
| Split the evaluation work into labelling (G07, no dependencies) and running and tuning (G08) | The cases use the tool names fixed in the design; only running them needs G02 and G03 |
| Split proposals (G03) from confirmed execution (G04) | Tuning (G08) needs only the propose tools, not the executor |
| Moved the evaluation gate in CI to phase 2 (G11) | A scope cut: phase 1 runs G08 by hand before go-live instead |
| Moved the first-week review and baseline to phase 2 (G16) | A scope cut: monitoring after go-live is not launch work |

**Cut line, if work runs high:** at the end of day 6, if G04 or G06 is not
done, G10 goes live at the pilot salon only. The other four salons then become
the first step of phase 2. To keep the value if time runs out early, complete
goals in this order: G01, G02 (read-only answers on staging), G03 and G04
(changes), G05 and G06 (customer-facing), G10.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1 | `assistant/agent.py`: one `LlmAgent` in an `App`, with 6 tools | Vertex AI | adk-workflow-design | ADK 2.8.0 constructor names |
| D2, I1 | `gateway/app.py`: verify the token, then `user_id` and state `customer_id`, then the Runner | — | adk-tool-auth-and-secrets | A7 token contract |
| D3, I2 | `assistant/tools/propose.py` writes an operation row; `POST /operations/{id}/confirm` | Cloud SQL | safe-api-tool-calls | — |
| D4, D5, I3 | `assistant/operations.py`: atomic claim, idempotency key, reconcile | Cloud SQL | safe-api-tool-calls | A8 key and reschedule semantics |
| D6 | `DatabaseSessionService`; `RunConfig(max_llm_calls=10)` | Cloud Run, Cloud SQL, Secret Manager | deploy-adk-on-google-cloud | Prices and region on the day |
| D7 | `web/widget/`: chat, proposal card, status poll | — | adk-frontend-integration | Host app embedding |

## Goals and dependencies

| ID and goal | Type | Hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- |
| G01 Booking API contract, client and fake | Discovery and implementation | 4–7 | — | safe-api-tool-calls | Ready |
| G02 Read-only assistant | Implementation | 6–9 | G01 | adk-tool-interface-design | Blocked by G01 |
| G03 Change proposals | Implementation | 5–8 | G01 | safe-api-tool-calls | Blocked by G01 |
| G04 Confirmed execution | Implementation | 6–9 | G03, G05 | safe-api-tool-calls | Blocked |
| G05 Gateway: identity, sessions, allowance | Implementation | 9–13 | — | adk-tool-auth-and-secrets | Ready (A7 provisional) |
| G06 Chat widget with proposal cards | Implementation | 6–10 | G05 | adk-frontend-integration | Blocked by G05 |
| G07 Labelled evaluation set and runner | Implementation | 5–8 | — | adk-agent-evaluation | Ready |
| G08 Evaluation run and instruction tuning | Implementation | 5–8 | G02, G03, G07 | adk-agent-evaluation | Blocked |
| G09 Staging on Cloud Run | Implementation | 5–9 | — | deploy-adk-on-google-cloud | Ready (needs the GCP project) |
| G10 Staging acceptance and go-live | Implementation and release | 6–9 | G04, G06, G08, G09 | adk-release-engineering | Blocked |

Each phase 1 goal has its complete record in its ticket under
`docs/tickets/salon-booking-assistant/`: outcome, scope, depth, skills,
acceptance and run prompt. Estimates and dependencies come from the schedule
block above. The routes are in the implementation map, and the rationale is
in the design. Each goal's verification is offline (`pytest` against the fake
booking API with a scripted model) unless its ticket says otherwise. Every
goal runs in the order its run prompt gives and records evidence in its
ticket.

## Phase 2: harden

| ID | Outcome | Primary skill | Hours | Acceptance |
| --- | --- | --- | --- | --- |
| G11 | The evaluation gate runs in CI. It records a release manifest (image, prompt hash, model ID, tool-schema hash) | adk-release-engineering | 4–9 | A deliberately broken instruction fails CI by exit code |
| G12 | SLIs (completed changes / proposals, tool errors by tool, uncertain operations) with alerts and a dashboard; traces carry the session ID | adk-agent-observability | 4–7 | An uncertain operation injected on staging pages the on-duty developer within 5 min |
| G13 | A reconciliation job resolves `uncertain` operations by lookup on a schedule | safe-api-tool-calls | 4–7 | A simulated lost response becomes `succeeded` without a second write |
| G14 | "Talk to the salon" handoff: the assistant passes the case to staff with a summary | adk-workflow-design | 4–8 | Out-of-scope requests reach the staff inbox; no booking change |
| G15 | Adversarial suite and security review (cross-customer IDs, injection, abuse) | adk-agent-security | 4–6 | 20 hostile cases; no operation is created outside the customer's scope |
| G16 | First-week review: real transcripts become evaluation cases; the phone-reschedule baseline is compared | adk-agent-evaluation | 2–3 | Report with completed changes per day versus the baseline |

## Later

| Item | Trigger | Risk accepted while it waits | Likely skill |
| --- | --- | --- | --- |
| SMS or WhatsApp channel | Customers ask, or web usage is low | Web only | adk-frontend-integration |
| Guest booking without an account (one-time code) | A7 fails, or demand appears | Account holders only | adk-tool-auth-and-secrets |
| Deposits or cancellation fees | The chain introduces them | None now: no money moves | safe-api-tool-calls |
| Remembering preferences ("my usual") | Repeated requests in G16 transcripts | Customers repeat themselves | adk-memory-architecture |
| Streaming replies and latency tuning | Measured p95 above 8 s | Slower replies | optimise-adk-on-google-cloud |
| Model migration | A retirement date is announced for `gemini-3.8-flash` | Pinned model | adk-model-and-output-contracts |
| More languages | A salon serves non-English customers | English only | adk-agent-instructions |

## Open decisions for further planning

See the design §Open decisions (A7, A8, A11, baseline). Also: the cut-line
remedy (a later date, or pilot-only with 6 h/day), and who is on duty for
uncertain operations after go-live.

## Resume here

- **Next goal:** G01. It has no dependencies, and it settles A7 and A8, which
  shape G03–G05. G05, G07 and G09 can start the same day.
- **Read first:** the design, then this plan, then the G01 ticket.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md.
```

After that: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
