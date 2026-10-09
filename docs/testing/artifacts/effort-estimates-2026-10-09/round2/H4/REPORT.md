# REPORT — salon booking assistant design session

## 1. Skills invoked and reference files opened, in order

Skills invoked: `adk-system-designer` (by the user's slash command). No other skill was invoked.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the command)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/implementation-handoff.md`
6. `adk-system-designer/assets/system-design-template.md`
7. `adk-system-designer/assets/implementation-plan-template.md`
8. `adk-system-designer/assets/ticket-template.md`
9. `adk-system-designer/references/gcp-decisions.md`
10. `*/references/compatibility.md` — grep only, for the ADK version line (found 2.8.0 in several; `adk-agent-observability/references/compatibility.md:40` recommends ≥2.10.0 for production)
11. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. `safe-api-tool-calls/references/*` — grep for "confirmation", then `safe-api-tool-calls/references/compatibility.md:74-92` (native confirmation unsupported with `DatabaseSessionService`)
13. `adk-operational-guardrails/references/runtime-bounds.md:9` — grep only, `max_llm_calls` semantics

Not opened: `references/runtime-and-delivery.md`. Its triggers (context limits, downloads, browser streams, continuity during a release) were not central, because replies are non-streaming and short.

## 2. Questions I would have asked, and the answers I assumed

These are also the **Assumed answers** table at the top of the design.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must it be live, and what happens after? | Live in 10 working days; continued, so phase 1 code is kept |
| A2 | How many hours each, and how familiar with ADK and GCP? | 3 devs × ~6 h/day × 10 days, focus 0.6; Python-fluent, already on GCP, new to ADK (×1.5) |
| A3 | Model and cloud budget? | ~USD 300/month, set as a billing alert |
| A4 | Who uses it, and where? | External salon customers, in a chat widget on the existing website, signed in |
| A5 | What data does it touch, and what can it change? | Personal (not special-category) data. It creates, moves and cancels real appointments. No payments or fees |
| A6 | Does the booking API accept idempotency keys, have a staging environment, and enforce slot uniqueness? | The team owns it, it has staging, and it enforces slot uniqueness. Idempotency is unknown and G01 settles it |
| A7 | Can the backend verify the website's customer token? | Yes (JWT/session verifiable, carries customer ID) |
| A8 | Languages and channels? | One language, web only |
| A9 | Region or residency constraints? | None beyond the booking API's existing region |
| A10 | Traffic? | ≤300 conversations/day, <10 concurrent |
| — | Is it MVP or an internal staff pilot? | MVP (external customers) |
| — | What is the cancellation policy (fees, late window), and who approves the assistant's wording? | No fees. The salon operations lead approves (calendar wait on G09) |
| — | Launch at one salon first? | Yes, one salon for 2 days, then all five |
| — | Who takes which goals? | Dev A backend/API, Dev B agent/quality, Dev C web/auth (roles invented; real names unknown) |
| — | Do you accept the cut line? | Assumed accepted, with a written cut order if work runs high |

## 3. Files written or changed, and what was not finished

Written:

- `docs/architecture/salon-booking-assistant.md` — the design: assumed answers, journey, depth table, floor, invariants I1–I5, decisions D1–D9, model-facing contracts, data and authority, security posture, failure table, open decisions. Status is **draft**.
- `docs/plans/salon-booking-assistant.md` — the plan: capacity, per-person load, cut line and cut order, implementation map, goals G01–G16 (phase 1 in full, phase 2 coarse), the Later table and the Resume block.
- `docs/tickets/salon-booking-assistant/G01-…G09-*.md` — 9 phase 1 tickets generated from the plan's goal entries, so the figures match.
- `REPORT.md` (this file).

Not finished, or not possible here:

- No product decision is confirmed by the user. Everything rests on assumptions.
- Prices for the model, Cloud Run and Cloud SQL were not looked up (no network), so cost is a G08 measurement rather than an estimate.
- Current ADK documentation and the confirmation limitations were not re-read online. I relied on the skills' dated compatibility notes.
- The design runs to about 3,300 words, which is longer than the skill's "two to four pages" for an MVP (see the friction log).
- Nothing is committed (no commit was requested).

## 4. Checks run and not run

Run (local Python, no network, no imports of google.adk):

- Sum of goal estimates: phase 1 = 48–79.5 h, which matches the plan; phase 2 = 33–66 h. I corrected a wrong phase 2 total (I had written 37.5–75) after this check.
- Each ticket's `total` matches both the plan's goals table and the goal section: all 9 OK.
- Per-person loads: A 18–28.5, B 13.5–22.5, C 16.5–28.5, which match the load table.
- Relative links and `design:`/`plan:` paths in the design, plan and tickets all resolve.

Not run:

- No tests exist. Any test importing `google.adk` cannot run here because dependencies are not installed.
- No ADK API names were verified against an installed pin.
- No live model, cloud or booking-API checks were run.

## 5. Friction log

- **Unsure: asking vs not asking.** `SKILL.md:54-74` says to open with the scope gate and let the user correct the profile, while `SKILL.md:120-124` says to ask nothing in a headless run and use an Assumed answers table. The second rule was clear and resolved it. **Helpful.**
- **Unsure: the cut-line confirmation.** `SKILL.md:93-94` and `references/delivery-profiles.md:177-178` ask me to have the user confirm the cut line. That isn't possible headless, so I recorded it as an assumed answer. A one-line headless note there would help.
- **Helpful: the capacity method.** `references/delivery-profiles.md:100-156` (hands-on/review split, 1.5× multiplier applied once, longest chain vs busiest person, re-sum the tickets) gave a concrete procedure, and the re-sum caught my phase 2 arithmetic error. The MVP example at `delivery-profiles.md:245-248` matched this case closely.
- **Helpful but easy to miss: confirmation vs session backend.** The fact that changed the core write design (native `require_confirmation` is unsupported with `DatabaseSessionService`) lives in `.claude/skills/safe-api-tool-calls/references/compatibility.md:81-87`, not in the designer. I found it only by grep. `references/implementation-handoff.md:31` says "check native confirmation compatibility". Linking that compatibility line directly would save the search.
- **Helpful: the model lifecycle table.** `SKILL.md:197-201` plus `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:13-15` showed that `gemini-3.6-flash` and `gemini-3.7-flash` retire on Vertex inside the plan horizon. I would otherwise have picked one from memory.
- **Unsure: the ADK version.** `SKILL.md:192-196` says to use the version named in each specialist's `compatibility.md`. They all say 2.8.0, but `adk-agent-observability/references/compatibility.md:40` recommends ≥2.10.0 for production. I recorded both and made the pin choice a G02 acceptance item.
- **Heavier than needed: document length.** `SKILL.md:85` says an internal tool or pilot should be "roughly two to four pages". The full design template (`assets/system-design-template.md`) with all its tables pushed the design to about 3,300 words, and the plan template (`assets/implementation-plan-template.md:56-79`, 12 fields per goal) pushed the plan to about 4,300 words. The tickets then repeat most of each goal. For 3 developers and 2 weeks, a shorter per-goal form would do.
- **Unsure: the ticket `status` field.** `assets/ticket-template.md:17` defaults to `status: ready`, but `SKILL.md:268-270` says "one file per ready goal", while the user asked for tickets for all phase 1 goals. I wrote all 9 and set `status: blocked` with `blocked_by` where a dependency is open (G03, G05, G08, G09).
- **Minor: two run-prompt shapes.** The plan template's run prompt (`assets/implementation-plan-template.md:77-79`) and the Resume block's prompt (`:123-128`) differ in shape from the closing example at `SKILL.md:277-279`. I used all three where each applies.

## 6. The next prompt the skills told the user to type

The skill (`SKILL.md:273-279`, plan template `:121-128`) says to end with the exact prompt for the next ready goal. The prompt written in the plan's Resume block is:

```text
/adk-engineer Carry out G01 Booking API contract and fake from docs/plans/salon-booking-assistant.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-auth-and-secrets.
Work within local code and offline tests, verify the fake reproduces commit-then-timeout
and the contract answers A6 and A7, and update the plan with actual evidence and remaining blockers.
```

The skill's generic form, quoted verbatim from `SKILL.md:278`, is: `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`
