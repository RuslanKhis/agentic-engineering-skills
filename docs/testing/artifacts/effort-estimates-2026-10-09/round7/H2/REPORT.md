# Report: helpdesk assistant design session (2026-10-14)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer`. No other skill was invoked.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
6. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
7. `.claude/skills/adk-system-designer/assets/system-design-template.md`
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
9. `.claude/skills/adk-system-designer/assets/ticket-template.md`
10. `.claude/skills/adk-system-designer/scripts/check_schedule.py` (read, then run)
11. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. `.claude/skills/adk-workflow-design/references/compatibility.md` (first 30 lines),
    plus a grep for the `google-adk` pin across every `*/references/compatibility.md`

I did not open `references/runtime-and-delivery.md`. Its trigger
(SKILL.md:184) covers context limits, downloads, browser streams, concurrent
sessions and release continuity, and none of these is material at 25 users
with request/response chat.

## 2. Questions I would have asked, and the answers I assumed

The same questions appear as A1–A10 and O1–O5 in the design. All dependent
decisions are marked provisional.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first version exist, and is it continued? | Within the 2 weeks; kept and continued |
| A2 | How many focused hours is "half their time"? | 6 h day × 0.5 × 0.6 focus = 1.8 h/day each, 25% reserve, no learning multiplier |
| A3 | Model and cloud budget? | Small internal allowance (tens of USD/month); existing GCP org and billing |
| A4 | Atlassian Cloud or Data Center? | Cloud (REST APIs, API tokens) |
| A5 | How do staff sign in? | Google Workspace or Cloud Identity, with a helpdesk Google group |
| A6 | Which spaces and project? Is it customer-facing JSM? | 1–2 runbook spaces every helpdesk member can read; one internal project `ITHD`; not a customer portal |
| A7 | Must the reporter be the real user? | No, not in phase 1. The bot is the reporter and the user is recorded in a label and footer |
| A8 | Do runbooks contain secrets or PII? | Possibly. Keep content out of logs; no screening in phase 1 |
| A9 | Region or residency requirement? | None beyond the org's usual region |
| A10 | How is success measured? | 20 gold questions from the helpdesk lead; adoption from weekly active users |
| O1 | Accept that a restart loses chats and pending drafts? | Assumed yes, still open |
| O2 | Accept a rare duplicate issue on a quick manual retry after an uncertain create? | Assumed yes, open (only matters for G06) |
| O3 | Accept the bot as reporter? | Assumed yes, open |
| O5 | hit@5 target and latency targets? | 80%; first text under 5 s, full answer under 20 s at p90 (assumed) |
| Cut line | Ship ticket drafts now and API creation in G06, or extend the date or hours? | Assumed: drafts now. G06 can be pulled in if work runs low |

## 3. Files written or changed, and what was not finished

Written. They're untracked; nothing is committed.
- `docs/architecture/helpdesk-assistant.md`: design (draft) with the assumed-answers table, depth, invariants I1–I8, decisions D1–D10, security posture, failure table and open decisions.
- `docs/plans/helpdesk-assistant.md`: summary, capacity, schedule YAML, what-if table, implementation map, goals table, phase 2 outline (G06–G11), later list, resume prompt.
- `docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md`, `G02-ticket-drafts.md`, `G03-authenticated-chat-page.md`, `G04-cloud-run-behind-iap.md`, `G05-gold-set-measurement.md`.
- `REPORT.md` (this file).
- I created `.scratch/` for what-if plan variants and removed it. The results are kept in the plan's what-if table.

Not finished or not done:
- **No implementation**, as requested. There is no code, dependency or cloud change.
- **The user's ask is cut.** Phase 1 drafts Jira tickets for the user to copy. Creating the issue through the API on click is G06, in phase 2, because the full scope only fits at the low end (finish 8.15–12.59 of 10 days). The user must confirm or move this cut line.
- I didn't look up provider facts: Vertex price for `gemini-3.8-flash`, regional availability, the IAP JWT audience format for direct IAP on Cloud Run, Confluence CQL and Jira label-search behaviour. These are recorded as checks in G01 and G04 and in the plan's implementation map.
- The ADK pin `google-adk==2.8.0` is a working assumption taken from the specialists' compatibility files. G01 confirms it.
- **Reading budget:** design plus plan is about 4,780 words against a budget of about 4,000. Tickets are about 230–260 words each, including front matter and the run block, against about 150. I didn't trim further, to keep failure rows, tests and acceptance intact (the rule at delivery-profiles.md:310-313).
- Phase 2 goals have no tickets. Only G06 has a schedule entry. The phase 2 hour total (29–53) is a hand sum.

## 4. Checks run and not run

Run:
- `/opt/homebrew/bin/python3.12 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/helpdesk-assistant.md --tickets docs/tickets/helpdesk-assistant/ --days 10 --reserve 0.25 --person "Dev A=1.8" --person "Dev B=1.8"`
  exited **0**: 17–24 h of 27 h, fits. Dev A 8–11 h and Dev B 9–13 h, each of 13.5 h. Chain G01 → G02 → G04, 6.67–9.63 days. Calendar fits. The plan and tickets agree.
- What-ifs with the same script: the full request exited 1 (low end only, 8.15–12.59 days). Moving G05 out exited 1. Deploying without the Jira path and enabling it afterwards exited 1, as did the same with Dev B as owner. Thirteen days exited 0. Both engineers at 2.4 h/day exited 0. Only Dev A at 2.4 h/day exited 1. All are quoted in the plan.
- A word count with grep and wc.

Not run:
- Any test that imports `google.adk`. None exists, and the dependencies aren't installed.
- The skill's own `tests/test_check_schedule.py`, which wasn't needed for this deliverable.
- All network or cloud lookups (forbidden this session).
- Default `python3` is 3.9.13. The script ran under the Homebrew 3.12 interpreter (the skill asks for 3.11 or later).

## 5. Friction log

- **Unsure: how many hours "half their time" is.** The example at delivery-profiles.md:175 uses `Dev A=3.6` for a full-time person, and the worked example at delivery-profiles.md:327-331 uses a 6 h day × 0.5 × 0.6. I used 1.8 h/day. The cut line hinges entirely on this assumption: 2.4 h/day fits the full request. It would help if the skill said which day length to assume for "half time".
- **Unsure: headless versus "ask them to confirm".** SKILL.md:52 says to let the user answer, and SKILL.md:96-98 says to show the cut line and ask. SKILL.md:125-128 (the Assumed answers table) resolved this well: I recorded the cut line as an open decision.
- **Genuinely helpful: check_schedule what-ifs.** The rule at delivery-profiles.md:189-201 says to run every remedy as a what-if and not fudge dependencies. That stopped me from trimming estimates to fit. The "low end only" result on the full scope forced an honest cut.
- **Helpful:** delivery-profiles.md:124-127 showed waits modelled as `W1` entries with `total: 0`, and the script handled them cleanly.
- **Helpful:** the lethal-trifecta guidance at design-decisions.md:182-197 led directly to D4: the model holds no Jira tool, so the write leg is removed rather than prompt-hardened. That made native-confirmation compatibility (implementation-handoff.md:59) moot.
- **Helpful:** the lifecycle JSON (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:13-14`) flagged that the 3.6 and 3.7 flash models retire on Vertex within the plan's horizon. Without it I'd probably have picked from memory.
- **Unsure: tickets for blocked goals.** SKILL.md:272-273 says "one file per ready goal", but the user asked for tickets for all phase 1 goals, and G04 and G05 are blocked by waits. I followed the user. The ticket template hard-codes `status: ready` (ticket-template.md:17), so I changed it to `blocked` or `proposed` as appropriate.
- **Unsure: ticket length.** delivery-profiles.md:275 says about 120 words (compact form) and delivery-profiles.md:308-309 says about 150. The template's front matter and run block alone take about 100 words, so either target is hard to meet with three acceptance cases.
- **Heavier than needed:** the full design template (system-design-template.md) for an internal tool with one read path and one human-gated write. Even after collapsing sections, the design is about 3,200 words. The budget check (delivery-profiles.md:306) flagged it, but nothing told me which sections to drop for an internal tool, only for a POC (delivery-profiles.md:254-280).
- **Minor:** the plan template's schedule example (implementation-plan-template.md:49-59) doesn't show a wait entry or `phase` on waits. I took that from delivery-profiles.md:124-127 instead.
- **Minor:** SKILL.md:205-208 asks to check service availability and prices with cited sources. With no network, these all became named verification items. The skill allows that ("keep those decisions provisional"), so it worked.

## 6. The exact next prompt

The skill's own wording (SKILL.md:282), quoted verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Instantiated for this plan (also in the plan's "Resume here"):

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```
