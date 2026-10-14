# REPORT: IT helpdesk ADK assistant, design-only session (2026-10-14)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user as `/adk-system-designer`.
   It loaded `.claude/skills/adk-system-designer/SKILL.md`.
2. `adk-system-designer/references/delivery-profiles.md`, read in full.
3. `adk-system-designer/references/design-decisions.md`, read in full.
4. `adk-system-designer/references/failure-review.md`, read in full.
5. `adk-system-designer/references/implementation-handoff.md`, read in full.
6. `adk-system-designer/references/gcp-decisions.md`, read in full.
7. `adk-system-designer/assets/implementation-plan-template.md`
8. `adk-system-designer/assets/ticket-template.md`
9. `adk-system-designer/assets/system-design-template.md`
10. `adk-system-designer/scripts/check_schedule.py`, read and then run.
11. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`.
    SKILL.md:203 says to choose the model from this file.
12. Every specialist's `references/compatibility.md`, grepped only for the ADK
    pin. All of them say `google-adk==2.8.0`.
13. `adk-system-designer/references/runtime-and-delivery.md`, first 30 lines
    only. I judged its triggers (SKILL.md:184) not to apply to a single-instance
    tool for 25 users.
14. `adk-operational-guardrails/references/*.md`, grepped only for the caveats
    on ADK tool confirmation (`human-review.md:66-68`).

No other skill was invoked. I did not hand off to `adk-engineer`, because the
user asked me not to implement.

## 2. Questions I would have asked, and the answers I assumed

These are the same as the **Assumed answers** table (A1 to A14) in
`docs/architecture/helpdesk-assistant.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first useful version exist, and is it continued? | Pilot group using it at the end of the 2 weeks (10 working days); continued |
| A2 | Who runs it afterwards? Should a novice multiplier apply? | The same two senior engineers; no multiplier |
| A3 | What can be spent on models and cloud? | About US$200 a month, with a budget alert at that level |
| A4 | Who uses it, and how do they sign in? | All 25 helpdesk staff daily, after a 3–5 person pilot; they have Google identities, so IAP works |
| A5 | What data does it touch, and what can it change? | Internal runbooks, which may hold sensitive configuration, and caller personal data in the chat. The only write is a Jira issue in one project. |
| A6 | Atlassian Cloud or Data Center? | Cloud (Confluence REST v2 with CQL, Jira REST v3) |
| A7 | Which Confluence spaces? | One or two IT runbook spaces that every helpdesk member can read, so no per-user scoping |
| A8 | Jira project, issue types and required fields? Does creation notify the reporter? | Placeholder project `ITHELP`, issue types Incident and Service Request, fields summary, description and priority; it may notify |
| A9 | Is a bot creator with the verified email in the issue acceptable? | Yes for phase 1; G08 improves it |
| A10 | Is there a Jira sandbox and a bot account? | Requestable on day 1, delivered in 1–3 working days (wait W1) |
| A11 | Is there an existing GCP project? | Yes, with Vertex AI, in the team's existing region |
| A12 | Is there a preferred frontend, such as Slack or Google Chat? | No; a simple web page |
| A13 | Can the helpdesk lead supply about 20 gold questions? | Yes, about 1 hour in week 1 |
| A14 | What is the success measure and baseline? | Time to find a runbook and file a ticket; no baseline yet, so it is measured in G05 and G06 |
| — | Do you accept the cut line? | Assumed yes: durable proposals and reconciliation move to phase 2 (G07). Two alternatives that keep them in phase 1 were tested and are listed in the plan. |

## 3. Files written or changed, and what was not finished

Written. All are new files.

- `docs/architecture/helpdesk-assistant.md`: the design, marked draft. It
  covers assumed answers, journey, profile and depth, guarantees I1 to I6,
  decisions D1 to D9, the security posture, the failure table and open
  decisions.
- `docs/plans/helpdesk-assistant.md`: the plan. It holds the summary, capacity,
  the yaml schedule block, the change log from the failing runs and its
  what-ifs, goals G01 to G05 in full, phase 2 goals G06 to G10, the Later list,
  and the resume prompt.
- Five tickets under `docs/tickets/helpdesk-assistant/`:
  - `G01-runbook-search-agent.md`
  - `G02-confirmed-ticket-creation.md`
  - `G03-iap-page-and-sessions.md`
  - `G04-cloud-run-behind-iap.md`
  - `G05-integrated-pilot.md`
- `REPORT.md`: this file.

Not finished, or deliberately not done:

- **No implementation and no cloud work,** as instructed.
- **Prices, regions and model availability were not looked up** (no network).
  D2's model choice rests only on the bundled lifecycle snapshot (checked_on
  2026-10-08). The cost estimate is symbolic, and the quota is set in G04.
- **Atlassian API behaviour is unverified.** This covers CQL `siteSearch`,
  whether a label search finds a just-created issue, and the bot permission
  schemes. Each is listed as a check in the implementation map.
- **The documents are over the reading budget.** Design and plan together come
  to about 7,100 words by `wc -w`, including tables and yaml, against about
  4,000 for an internal tool. The tickets are about 250 words each against
  about 150. I did not trim further. Most of the length is the plan's complete
  phase 1 goals, which the tickets copy.
- All decisions are proposed or provisional. None is user-accepted.

## 4. Checks run and not run

| Check | Result |
| --- | --- |
| `python3.11 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/helpdesk-assistant.md --days 10 --reserve 0.25 --person "Dev A=1.8" --person "Dev B=1.8"`, run 1 (first draft) | Exit 1. 16–25 hours fit the 27-hour capacity, but the finish was 8.41–11.11 days, so the calendar fit at the low end only. |
| Run 2: access request folded into G02, wait kept as W1 | 6.67–10.37 days; calendar at the low end only |
| What-if on run 2: `--days 12` | Fits (6.67–10.37 days) |
| What-if on run 2: Dev B at 2.3 hours a day | Fits (5.93–9.63 days) |
| Run 3: durable record moved to G07, so G02 is 3–5 hours | Fits (5.93–9.63 days) |
| Final run with `--tickets docs/tickets/helpdesk-assistant/` | **Exit 0.** Phase 1 is 14–23 hours against 27 hours; finish 5.93–9.63 of 10 days. The longest chain at the high end is G01 → G03 → G05. The tickets match the plan, with no PROBLEM lines. |

The what-ifs piped the helper's output through `grep`, so the `exit=` values
printed for those runs were grep's status, not the helper's. The fits and
finish lines are the helper's own output. Only the final run's exit status (0)
was read directly.

Not run:

- No project tests exist, and none could run: `google-adk` is not installed and
  nothing was implemented.
- No live Confluence, Jira, Vertex or GCP checks; network and cloud commands
  were forbidden.
- The skill packages' own `tests/` were not run, because that was not part of
  the task.

## 5. Friction log

- **Python version.** The default `python3` is 3.9.13, and
  `adk-system-designer/references/delivery-profiles.md:201` says to report the
  schedule as unchecked without 3.11 or later. I found
  `/opt/homebrew/bin/python3.11` and used it. *Helpful:* the explicit fallback
  rule. A one-line hint to look for `python3.11` would have saved the search.
- **The helper scheduled the access request too late.** The plan template
  (`assets/implementation-plan-template.md:50-58`) puts waits on goals, and
  `check_schedule.py:239` adds `wait_days` *after* a goal's work. A separate
  1-hour "G00 request access" goal was therefore scheduled by remaining-work
  priority (`check_schedule.py:232`), which put it late, so its wait landed at
  the end. That pushed run 1 to 11.1 days. `delivery-profiles.md:187-188` says
  to "add a goal or first step that requests it today", but the helper cannot
  express "today". My workaround was a zero-hour, ownerless item `W1` that
  carries the wait. It works, but the report then shows a spurious
  "(unassigned): 0-0 h of 45 h available" line, from `check_schedule.py:246`
  using the default 6 hours a day. I was unsure whether this counted as
  "shortening a wait" (`delivery-profiles.md:184-187`), and decided it did not:
  the wait stays at 1–3 days.
- **Whole-hour rounding** (`delivery-profiles.md:113`) forced a 15-minute
  access request into a 1-hour goal, which caused the problem above.
- **Unsure which numbers to use for capacity.** The worked example
  (`delivery-profiles.md:317-319`, 6 h × 0.5 × 0.6) and the command example
  (`delivery-profiles.md:170`, `Dev A=3.6`) together implied 1.8 hours a day for
  half time. That was clear enough once I put them side by side. *Helpful.*
- **Unsure whether durable idempotency is part of the floor or the depth.** The
  depth table row "External writes" (`delivery-profiles.md:55`, internal tool:
  "confirmation for writes") settled that it could move to phase 2. This was
  the cut that made the schedule fit, and the most useful line in the skill
  for this task.
- **Reading budget against goal completeness.** `delivery-profiles.md:292-303`
  asks for complete phase 1 goals in the plan, tickets that copy acceptance,
  and about 4,000 words. With five full goals plus the design, I could not meet
  the budget without cutting acceptance, which line 302 forbids. The budget
  felt heavier than needed for this profile. The ticket length guidance is also
  inconsistent: about 120 words at `delivery-profiles.md:270` (compact form)
  and about 150 at `delivery-profiles.md:299`.
- **Ticket status.** `assets/ticket-template.md:17` hard-codes `status: ready`.
  G03 and G05 are blocked, so I wrote `blocked (…)`. It was not clear whether
  only ready goals should get tickets (SKILL.md "one file per ready goal")
  while the user asked for "phase 1 goals". I wrote all five, with status set
  accordingly.
- **Model choice.** SKILL.md:201-205 and the lifecycle JSON made the choice
  quick. `gemini-3.6-flash` retires on Vertex on 2026-11-19, within the plan's
  horizon, which I would have missed choosing from memory. *Genuinely helpful.*
- **Headless mode.** SKILL.md:124-128 ("keep asking nothing further … Assumed
  answers table") removed the ambiguity of having no user to ask. *Helpful.*
- **Which ADK pin.** SKILL.md:197-201 together with every specialist's
  `compatibility.md` gave the working assumption, `google-adk==2.8.0`.
  *Helpful.*
- **Three run-prompt formats.** The plan template (lines 105 and 152), the
  ticket template (line 54) and SKILL.md:282 each give a different prompt
  format. I was unsure which to put in the closing message, and chose the
  SKILL.md form for the plan goal.
- **Heavier than needed.** The full system-design template with
  security-posture and model-facing contract tables, for a 3-tool single
  agent. I kept each to a few rows, as `delivery-profiles.md:274-275` allows.

## 6. Next prompt the skills told the user to type

The skill's closing instruction (SKILL.md:279-283) gives this form, which I
filled in for the plan:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```

The ticket form from `assets/ticket-template.md:54` is also written into each
ticket and into the plan's summary.
