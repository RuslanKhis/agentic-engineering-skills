# Session report: helpdesk assistant design

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's `/adk-system-designer`; SKILL.md loaded).
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/assets/ticket-template.md`
8. `.claude/skills/adk-system-designer/assets/system-design-template.md`
9. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
10. `.claude/skills/*/references/compatibility.md` — grep of the first lines only, to find the ADK version (2.8.0) the specialists were checked against.
11. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md` (trigger: long runbook pages vs context limits; browser contract)
13. `.claude/skills/adk-engineer/SKILL.md`, lines 1–40 only, to check how it consumes ticket `primary_skill` fields.

No other skill was invoked; specialist skills are named in the plan for later goals.

## 2. Questions I would have asked, and the answers assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first version exist; thrown away or continued? | End of the two weeks; kept and continued |
| A2 | Who runs it afterwards? | Helpdesk team lead, with the two engineers on call |
| A3 | Budget for models and cloud; which GCP project? | Small internal allowance (tens of USD/month); an existing project the engineers may deploy to (not yet authorised) |
| A4 | Who uses it and through what? | The 25 helpdesk staff daily, all in one Google Workspace group |
| A5 | Confluence/Jira Cloud or Data Center; which data; which effects? | Cloud; internal runbook spaces (may contain secrets); creates issues in one Jira project only |
| A6 | Can every helpdesk member read every page in the runbook spaces? | Yes, no narrower page restrictions (verified in G01) |
| A7 | Whose name goes on created tickets? | Assistant service account creates; requesting engineer set as reporter or named in a field |
| A8 | Sign-in method? | Google Workspace via IAP |
| A9 | Web page, or Slack/Google Chat bot? | A simple web page in phase 1 |
| O4 | How will the helpdesk lead judge success? | Unknown; proposed thumbs feedback + count of tickets created through the assistant |
| O6 | Daily per-user cap and budget alert value? | 40 turns/user/day, `max_llm_calls=8`, alert at the allowance |
| — | Confirm the profile ("internal tool") and the cut line (G01–G04, 19–27 h of 27 h)? | Accepted as proposed; fallback for G04 recorded |

All are recorded at the top of the design as "Assumed answers"; dependent decisions are marked proposed/provisional.

## 3. Files written or changed; what is not finished

Written (nothing else changed):

- `docs/architecture/helpdesk-assistant.md` — design (draft): assumed answers, profile, depth table, floor, cut line, invariants I1–I6, decisions D1–D7, model-facing contracts, data/authority, trifecta table, budgets, failure table, open decisions O1–O6.
- `docs/plans/helpdesk-assistant.md` — plan: capacity, implementation map, G01–G04 (phase 1, full), G05–G09 (phase 2, coarse), later list, resume prompt.
- `docs/tickets/helpdesk-assistant/G01-confirm-contracts.md` (ready)
- `docs/tickets/helpdesk-assistant/G02-cited-runbook-answer.md` (ready, offline)
- `docs/tickets/helpdesk-assistant/G03-hosted-behind-iap.md` (blocked: G02, project authorisation)
- `docs/tickets/helpdesk-assistant/G04-confirmed-jira-ticket.md` (blocked: G01, G02)
- `REPORT.md` (this file)

Not finished / limitations:

- No implementation (as instructed). Nothing committed.
- Provider facts not verified (no network): Jira create idempotency, label-search consistency, reporter permission, Confluence page restrictions, Vertex availability of `gemini-3.8-flash` in a region, prices. All routed to G01 or marked symbolic.
- The design is ~3,360 words, longer than the "roughly two to four pages" the skill sets for an internal tool; I did not trim it further.
- Every decision is "proposed"; none is user-accepted.
- Tickets G03 and G04 are written although blocked (the user asked for all phase 1 goals; the skill says one file per *ready* goal — see friction log).

## 4. Checks run and not run

Run:

- Relative Markdown link check over `docs/**/*.md` plus ticket front-matter `design`/`plan` paths (`python3 -I` script): **0 broken links**.
- Ticket front matter parsed for all four tickets: goal, estimate, status, blocked_by present.
- Arithmetic: phase 1 = 19–27 h; capacity 2 × 0.5 × 10 × 6 × 0.6 = 36 h; after 25% reserve = 27 h. High end equals capacity minus reserve.
- `grep` for secret-like strings (`password`, `token=`, `apikey`) in `docs/`: none.

Not run:

- Any test importing `google.adk` (no application code exists, and google-adk is not installed).
- The skills' own test suites (`.claude/skills/*/tests`) — not relevant to a design-only change.
- Any network, cloud, Atlassian or model lookup (forbidden in this session).

## 5. Friction log

- **Unsure: tickets for blocked goals.** `adk-system-designer/SKILL.md:266-267` says "write one file per ready goal", while the user asked for tickets for all phase 1 goals and `assets/ticket-template.md:12` defaults `status: ready`. I wrote all four and set `status: blocked` with `blocked_by` for G03/G04; the template gives no guidance on blocked tickets.
- **Unsure: scope gate vs headless.** `SKILL.md:49` and the scope gate say to ask and wait; `SKILL.md:119` (headless → Assumed answers table, ask nothing further) resolved it cleanly. Helpful.
- **Unsure: confirming the cut line.** `SKILL.md` ("ask them to confirm or move it") and `references/delivery-profiles.md:117-121` want user confirmation; with no user, I recorded it as an assumed answer. Fine, but the skill never says so explicitly for the cut line.
- **Unsure: high end equals capacity exactly.** `references/delivery-profiles.md:112-114` ("fits when the high end … is within capacity minus the reserve") — 27 ≤ 27 technically fits but leaves no slack; I added a named fallback for G04 as the low-end rule suggests (`:113`).
- **Heavier than needed: document length.** Following the full `assets/system-design-template.md` (151 lines, many tables) for an internal tool produced ~3,360 words, above the "two to four pages" in `SKILL.md:85`. The template has no internal-tool compact form, only the POC one (`references/delivery-profiles.md:144-166`).
- **Heavier than needed: plan duplicates tickets.** The plan's per-goal fields (`assets/implementation-plan-template.md:48-69`) and the ticket (`assets/ticket-template.md`) carry nearly the same content; writing both doubled the work for four goals.
- **Mildly unclear: `runtime-and-delivery.md` trigger.** `SKILL.md:178-181` lists triggers broadly ("context limits … concurrent sessions"); nearly any agent hits one. I read it; it changed little (confirmed completed JSON over streaming).
- **Genuinely helpful: model lifecycle table.** `SKILL.md:196-197` pointing to `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` steered the pin away from `gemini-3.6-flash` (Vertex retirement 2026-11-19) and 2.5 models (2026-10-20), which memory would have suggested.
- **Genuinely helpful: version pin rule.** `SKILL.md:190-195` plus each specialist's `references/compatibility.md` gave a defensible ADK 2.8.0 working assumption with a G01 acceptance item.
- **Genuinely helpful: trifecta check.** `references/design-decisions.md:182-196` led directly to D3 (model only proposes; creation in an app route on click), the central safety decision.
- **Genuinely helpful: capacity example.** `references/delivery-profiles.md:180-185` was almost this exact team shape, making the 36 h figure quick.
- **Genuinely helpful: failure scenarios.** `references/failure-review.md:30` ("provider commits, reply is lost") produced the reconcile-by-label, no-blind-retry design for Jira.
- **Small gap:** `references/implementation-handoff.md:59` cites ADK confirmation limitations by URL only; I could not open it offline, so D3's "native confirmation not used" rests on design preference, not the documented limitation.
- **cwd pitfall (mine, not the skill's):** a `cd` inside a Bash call persisted and broke three later relative-path calls; harmless re-run.

## 6. Next prompt the skills told the user to type

The skill (`SKILL.md:270-276`) says to end with the exact prompt for the next ready goal. Given to the user, verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```

Its template example (`SKILL.md:276`) is `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`
