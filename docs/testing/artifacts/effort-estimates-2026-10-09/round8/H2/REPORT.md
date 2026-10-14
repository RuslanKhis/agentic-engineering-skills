# Report: IT helpdesk ADK assistant, design and phase 1 tickets

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's `/adk-system-designer`).
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/assets/ticket-template.md`
8. `.claude/skills/adk-system-designer/assets/system-design-template.md`
9. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
10. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
11. Grep (not full reads) over every `.claude/skills/*/references/compatibility.md` for the ADK version (2.8.0).
12. `.claude/skills/adk-system-designer/scripts/check_schedule.py` (read, then run).
13. Grep over the specialist skills for confirmation, Jira and IAP; read
    `.claude/skills/adk-tool-interface-design/references/function-tool-contract.md:155-195` (Confirmation)
    and the matching lines of `deploy-adk-on-google-cloud/references/production.md:21-26`.

Not opened: `references/runtime-and-delivery.md` (its triggers — context limits,
downloads, browser streams, release continuity — were judged not central for a
25-user internal tool). No other skill was invoked.

## 2. Questions I would have asked, and the answers assumed

The full table with dependent decisions is at the top of
`docs/architecture/helpdesk-assistant.md` ("Assumed answers").

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first version exist; continued afterwards? | Pilot-usable after the two weeks (10 working days); continued |
| A2 | How many focused hours a day do the engineers really have? | 1.8 h/day each (half of 6 focused hours × 0.6 focus), 25 % reserve |
| A3 | Money for models and cloud? | A few hundred USD a month; budget alert |
| A4 | Who uses it, and through what? | The 25 helpdesk agents daily, via a web page; no end users |
| A5 | Which Confluence spaces; any pages restricted to a subset of staff? | 1–3 runbook spaces, all readable by all 25 |
| A6 | Atlassian Cloud or Data Center? | Cloud |
| A7 | Do runbooks hold secrets or personal data? | Hostnames and procedures only |
| A8 | Staff identity? | Google Workspace; a helpdesk Google group can be created |
| A9 | Existing GCP platform? | Existing project with Cloud Run, Artifact Registry, CI; engineers may enable direct IAP |
| A10 | Jira project, issue types, reporter, may it assign or add watchers? | One "IT Helpdesk" project; Incident, Service Request, Task; reporter = requesting agent; no assignee/watchers |
| A11 | Must ticket creation be in phase 1? | No: search first, ticketing first in phase 2 (forced by capacity) |
| A12 | How is success judged; baseline? | 15-case gold set + pilot feedback; no baseline, time saved is a hypothesis |
| A13 | Region / residency? | The existing project's single region; no residency rule |
| — | Confirm or move the cut line? | Assumed confirmed: G03 drafting and G07 Jira creation in phase 2 |

## 3. Files written or changed; what was not finished

Written (nothing else in the repository was changed):

- `docs/architecture/helpdesk-assistant.md` — draft design: assumed answers, journey, depth table, floor, guarantees I1–I8, decisions D1–D11, model-facing contracts, data, failure table, open decisions.
- `docs/plans/helpdesk-assistant.md` — summary, capacity, schedule block (phase 1 and 2), what-if table, implementation map, goals table, phase 2 goals, later list, resume prompt.
- `docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md`, `G02-gold-set-measurement.md`, `G04-identity-bound-chat.md`, `G05-deploy-behind-iap.md`, `G06-pilot.md` — one per phase 1 goal.
- `REPORT.md` — this file.

Not finished / limitations:

- **Jira ticket creation is not in phase 1.** The user asked for it; at the assumed
  1.8 h/day it does not fit (see the plan's what-if table). This is the main thing for the
  user to confirm or override. At 2.4 h/day, ticket drafting (G03) fits; confirmed creation (G07, 5–8 h) still would not.
- Nothing implemented (by instruction). No tickets for phase 2 (G03, G07–G09), per the skill.
- Provider facts not verified (no network): Gemini 3.8 Flash availability on Vertex in the region, IAP JWT audience format for direct IAP, Jira entity-property JQL lookup, Confluence CQL behaviour, prices. Each is a named check in a goal.
- Reading budget exceeded: design + plan ≈ 4,600 words against ~4,000 (design ≈ 2,800, above the "at most half"); tickets ≈ 240–290 words each including front matter against ~150. I did not trim further.
- All decisions are provisional; the design is marked draft.

## 4. Checks run and not run

Run:

- `python3 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/helpdesk-assistant.md --tickets docs/tickets/helpdesk-assistant/ --days 10 --reserve 0.25 --person "Dev A=1.8" --person "Dev B=1.8"` → exit 0: phase 1 15.5–24.5 h vs 27 h, fits; Dev A 7.5–13.5 of 13.5 h, Dev B 8–11 of 13.5 h; longest chain G04 → G05 → G06, 10 working days; finish 7.04–10 of 10 days; tickets match the plan.
- Four what-ifs with the same helper on scratch copies in `/tmp/sched/` (outside the repo, scratch only): ticket drafting in phase 1 → 18.5–28.5 h, finish 8.52–12.22 days (low end only, exit 1); G06 moved to Dev B + 15 cases → low end only; G03 to phase 2 with 20 cases → calendar low end only; same as first at 2.4 h/day → fits (6.39–9.17 days). Quoted in the plan.
- Relative-link check over `docs/**/*.md` (inline Python) → 0 broken links.

Not run:

- The helper's environment note: Python here is 3.9.13, below the 3.11 the skill names (`delivery-profiles.md:212`); the script ran without error, but the skill's stated requirement was not met.
- Any project tests: none exist, and tests importing `google.adk` cannot run here (not installed).
- No live checks (Confluence, Jira, Vertex, IAP, Cloud Run); no cloud, network or install commands.
- The skill's own test suites were not run (not part of this task).

## 5. Friction log

Unsure:

- **Focused hours per day.** `delivery-profiles.md:335-337` computes a similar team as "6 hours × 0.6", while `delivery-profiles.md:219-221` says people × available hours × focus and `delivery-profiles.md:178-179` says give "full focused hours per day". Whether 6 h is already "focused" (then × 0.6 double-counts) is unclear, and this single number decided whether Jira creation fits. I followed the worked example and showed the 8-hour what-if.
- **Cut scope against the explicit request.** `SKILL.md:96-98` and `delivery-profiles.md:232-236` say cut scope and ask the user; headless, `SKILL.md:126` says assume. Cutting a feature the user named felt heavy-handed; I chose it, recorded it as A11, and put it first in the summary's decisions.
- **Where does the W1 request step live?** `delivery-profiles.md:124-127` says waits get their own entry with no owner, and `:192-193` says "add a goal or first step that requests it today". I put the request into G01's scope (Dev A); not obvious which goal should own it.
- **Handoff hours.** `delivery-profiles.md:204-207` says add handoff hours to the receiving goal and record `handoff:`; unclear whether the figure is included in `hands_on` or extra. I included it.
- **Ticket run prompt for a live goal.** `assets/ticket-template.md:53-57` says "run its verification locally", which contradicts G05's authorised live verification; I kept the template text verbatim.
- **Status for blocked tickets.** `assets/ticket-template.md:17` hard-codes `status: ready`; G02/G05/G06 are blocked, so I set `blocked`.
- **Which phase-1 goal leads retrieval.** The handoff table (`implementation-handoff.md:19-37`) has no row for "live search of an external knowledge API as a tool"; I picked `adk-memory-architecture` over `adk-tool-interface-design`.

Heavier than needed:

- Reading budget plus template sections: following `assets/system-design-template.md` section by section produced a design over the half-budget (`delivery-profiles.md:312-316`); guarantees and decisions tables overlap on verification.
- Ticket ~150 words (`delivery-profiles.md:316`) is hard to meet with the template's front matter (~90 words) plus a run prompt block (`assets/ticket-template.md:1-18, 51-57`).

Genuinely helpful:

- `scripts/check_schedule.py` exposed that the calendar, not hours, was binding (chain G01 → G02 → G06 at 10.74 days), which I would not have caught by hand; the ticket/plan comparison is a good guard.
- The what-if instruction (`delivery-profiles.md:196-201`) made the cut-line options concrete and honest.
- The model lifecycle file (`SKILL.md:202-205`; `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`) flagged that `gemini-3.6-flash` retires on Vertex on 2026-11-19, inside the plan.
- The headless rule (`SKILL.md:124-128`) gave a clear format for assumptions.
- `function-tool-contract.md:162-175` in `adk-tool-interface-design` gave the exact `require_confirmation` behaviour for D5.
- The floor list (`delivery-profiles.md:76-86`) kept "no write before confirmation" from being traded away when cutting.

## 6. The exact next prompt the skills told the user to type

From the G01 ticket's run section (template `assets/ticket-template.md:53-57`), as written in the plan's "Resume here":

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

The skill's generic form (`SKILL.md:282`) is `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`
