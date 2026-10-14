# REPORT: home-insurance claim intake agent, design session

Date: 2026-10-14. Mode: headless (no user answers). Design and plan only; nothing implemented.

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer`, via the user's `/adk-system-designer` command. No other skill
was invoked. Specialist files were opened only to read version and model facts.

Files opened, in order:

1. `.claude/skills/adk-system-designer/SKILL.md` (loaded by the command)
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
7. `.claude/skills/adk-system-designer/assets/system-design-template.md`
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
9. `.claude/skills/adk-system-designer/assets/ticket-template.md`
10. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md`
11. `.claude/skills/adk-system-designer/scripts/check_schedule.py` (read in full, then run)
12. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
13. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md`, first 30 lines
14. A grep over every specialist's `references/compatibility.md` for the ADK version. This included one line from `adk-agent-observability/references/compatibility.md:40`.
15. `.claude/skills/adk-system-designer/tests/test_check_schedule.py`, imports only, before running it

## 2. Questions I would have asked, and the answers I assumed

These are recorded as rows A1–A15 in `docs/architecture/home-claim-intake.md`, together with the
decisions that depend on each.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | What is the GA date, and which EU markets? | 2027-03-15, Germany only. The product continues after GA. |
| A2 | Which languages? | German and English |
| A3 | How familiar is the team with ADK and GCP, and how many hours can each person give? | They know GCP and Python but are new to ADK, so estimates use a ×1.5 multiplier. Each person has about 5 focused hours a day. The security reviewer works about 1 day a week (≈1.2 h/day). Roles are Lead, Integration, Platform, Frontend, Agent, ML and Security. |
| A4 | What is the budget for models and cloud? | About €3k a month for non-production. In production, at most €0.50 of model cost per completed claim (illustrative). |
| A5 | Who uses it, and how do they sign in? | Policyholders sign in to the existing web portal through its OIDC CIAM, which provides a stable customer ID. Web only. |
| A6 | What data does it touch, and what may it change? | Personal data and home photos. The only external effect is creating an FNOL claim with photos in ClaimCenter. It makes no coverage or payment decisions. |
| A7 | How is Guidewire reached? | Through the ClaimCenter Cloud API, behind the company API gateway, using OAuth2 client credentials. A sandbox is available on request. Idempotency is unknown. |
| A8 | Where do policy details come from? | A read-only policy-summary API, keyed by customer ID |
| A9 | Is there an existing GCP organisation? | Yes. An EU location org policy applies, and a platform team creates the projects. |
| A10 | May Gemini on Vertex AI in the EU process claim data? | Yes, subject to the DPIA |
| A11 | What must the assistant never do? | Never state coverage, liability or amounts. Never act for anyone other than the signed-in policyholder. |
| A12 | How is success measured, and is there a baseline? | Fewer adjuster callbacks, less time to file and lower abandonment. The baseline is not known, so it is measured during the pilot. |
| A13 | How long is data retained? | 30 days for our copies after submission or abandonment |
| A14 | What availability and traffic should it handle? | 99.5 % availability, about 3,000 claims a month, and storm peaks of 1,000 a day (illustrative) |
| A15 | Who operates it after GA? | The same team in business hours. The platform team covers infrastructure 24/7. |
| O7 | Should the spare capacity pull phase 2 items into phase 1? | No. The cut line stays as written and the question is left open for the user. |

## 3. Files written or changed, and what was not finished

Written (all new, inside the current directory):

- `docs/architecture/home-claim-intake.md`: the design (status **draft**)
  - Assumed answers, journey, depth table, invariants I1–I8 and T1–T2, a component diagram and confirm sequence
  - Decisions D1–D15, model-facing contracts, data/authority, security posture, budgets, failure table, open decisions O1–O7
- `docs/plans/home-claim-intake.md`: the plan
  - Summary, capacity, the load table and the checked `yaml` schedule (27 goals and 7 waits), the change log from failing runs, and the implementation map
  - A goals table linking to the tickets, a wait table, phase 2 (P2-01 to P2-06), the Later list and "Resume here"
- `docs/tickets/home-claim-intake/G01-…md` to `G27-…md`: 27 phase 1 tickets
  - I generated them with a throwaway script at `/tmp/ticketgen/gen.py`, outside the repository.
  - The script copies each ticket's estimate, owner, waits and dependencies from the plan's schedule block.
- `REPORT.md` (this file)

Temporary files outside the repository: `/tmp/sched_draft*.md`, `/tmp/sched_g16_*.md`, `/tmp/finish_detail.py`
and `/tmp/ticketgen/`. I also removed the `__pycache__` folders that my runs created under
`.claude/skills/adk-system-designer/`. No skill files were changed.

Not finished, or not possible:

- **No provider fact was verified.** The session had no network access. Unverified items include model and Model Armor availability in EU regions, Cloud Tasks and region facts, the Guidewire Cloud API contract, prices and CIAM claims. Each is marked provisional in the design and assigned to G01 or G02.
- **No assumption was confirmed by the user.** That includes the cut line. The design stays draft.
- **Cost estimate:** only a symbolic formula. No prices were looked up.
- **No implementation, provisioning or cloud commands**, as instructed.

## 4. Checks run, and checks not run

Run:

- **`check_schedule.py` drafts 1–6:** each run before the final one exited 1. The high-end finish was 158, 135, 124, 119, 114, then 102.5 working days against 100. Each change is logged in one table row in the plan.
- **Final schedule check** (Python 3.11, plan and tickets, `--days 100 --reserve 0.25`, six people at 5 h/day, Security at 1.2): **exit 0**.
  - 668–1,122 h against 2,340 h of capacity, so it fits.
  - Finish in 58–95 working days of 100, so it fits.
  - The longest chain (high) is 91.7 days.
  - No mismatches between tickets and plan, and no handoffs missing hours.
- **What-ifs run:**
  - G16 owned by Integration instead of Frontend: finishes at 110.5 days.
  - Security at 2 h/day: finishes at 60.9–101.7 days, which is worse than 58–95. This remedy was **not** offered (see friction).
- **Helper-internal check:** I wrote `/tmp/finish_detail.py`. It imports `check_schedule.read_plan` and repeats the helper's own scheduling loop to print each goal's start and finish day. I used it to find the bottlenecks.
- **Designer skill's own tests:** `python3.11 -I -m unittest discover -s tests` in `adk-system-designer` passed 11 tests. `pytest` is not installed; `unittest` worked.
- **Working-day count:** a Python date calculation gave 102 working days from 2026-10-15 to 2027-03-12, after removing 5 assumed holidays. The plan uses 100.

Not run:

- **No application tests exist.** Nothing was implemented, so there is nothing to run. Every acceptance check in the tickets is planned, not executed.
- **Tests that import `google.adk`:** not run, because google-adk is not installed. None exist in this repository anyway.
- **Other skills' tests and scripts:** not run. That includes `adk-model-and-output-contracts/scripts/audit_model_config.py`, because there is no project configuration to audit.
- **Live, cloud or network checks:** none, as instructed.

## 5. Friction log

- **Helpful: the scope gate and the headless rule.**
  - `adk-system-designer/SKILL.md:54` and `:125` together say exactly what to do when nobody can answer: an Assumed answers table, with dependent decisions marked provisional.
  - The rule removed any doubt about whether to stop and ask.
- **Helpful: the model lifecycle table.**
  - `SKILL.md:200` points to `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`.
  - The table showed that `gemini-3.7-flash` retires on Vertex on 2027-01-28, before GA, and that `gemini-3.6-flash` retires on 2026-11-19.
  - From memory alone I might have picked one of those.
- **Helpful: the schedule helper found real plan errors.**
  - I had left G12 (data protection) out of the pilot's prerequisites. The finish range exposed that.
  - The handoff check at `check_schedule.py:301` flagged a missing G16→G22 handoff.
  - Quoting the helper's figures, as `delivery-profiles.md:184-187` requires, kept the plan honest.
- **Unsure: which Python to use.**
  - `delivery-profiles.md:212` says "If Python 3.11 or later is not available…". The default `python3` here is 3.9.13, but `python3.11` exists.
  - It was unclear whether 3.11 is required. Nothing in the script looked 3.11-specific.
  - I used 3.11 to be safe.
- **Unsure / heavier than needed: "phase 1" for a production profile with a fixed GA date.**
  - `delivery-profiles.md:238-250` defines phase 1 as "fits the capacity, ships".
  - With a 5-month GA deadline, the natural phase 1 is all of GA. That produced 27 goals, 27 tickets and 7 waits.
  - A "pilot first, GA second" split was possible, but the user's deadline is GA.
  - The guidance does not say which to choose when the deadline is the production launch itself.
- **Unsure: chain-bound plans with lots of spare hours.**
  - `delivery-profiles.md:215-236` covers only overruns. Here the plan uses 29–48 % of capacity while the calendar is chain-bound.
  - The skill gives no guidance on presenting spare capacity: pull scope forward, or treat it as a hedge against underestimation?
  - I recorded it as open decision O7.
- **Unsure: the helper's greedy scheduling.**
  - `check_schedule.py:240` (`node = max(ready, key=lambda n: remaining[n])`) assigns goals greedily.
  - So adding hours to Security made the finish *worse* (101.7 against 95 days). The scheduler changed which goal each person took first.
  - In the same way, it scheduled Lead's G13 before the identity goal G05.
  - `delivery-profiles.md:196-201` asks for what-ifs on every remedy. The guidance does not warn that a what-if can mislead this way.
  - To see why, I had to re-implement the loop (`/tmp/finish_detail.py`), because the helper prints no start or finish per goal.
- **Heavier than needed: the route field in tickets.**
  - `delivery-profiles.md:298-306` makes the ticket the home of each goal's scope, route and acceptance.
  - But `assets/ticket-template.md:27-34` has no Route section, so I put the route inside "Scope – In".
  - `implementation-plan-template.md:110` agrees the ticket is the home, so the two sources are consistent. Only the template lacks the field.
- **Heavier than needed: overlapping tables.**
  - The SKILL's Assumed answers table (`SKILL.md:125`) and the design template's scope-gate table (`system-design-template.md:17`) restate the same facts in two places.
  - That cuts against "one home per fact" (`delivery-profiles.md:298`). I kept both, with the scope-gate table referring to A-rows.
- **Heavier than needed: design length.**
  - The design came out at about 5,500 words. `delivery-profiles.md:312` rightly forbids a word count, but no guide length exists for production either.
  - I trimmed by referring to IDs, but a reviewer will need more than 10 minutes.
- **Unsure: the ADK pin.**
  - The specialists say 2.8.0. `adk-agent-observability/references/compatibility.md:40` recommends ≥2.10.0 for a new production deployment.
  - `SKILL.md:199` says to record the specialists' version and confirm it in the first goal, so I did. The disagreement is open decision O3.
- **Unsure: no network.** `gcp-decisions.md:35-41` requires dated official sources for provider facts. Without network access every such fact is provisional, so two discovery goals (G01, G02) carry that weight.
- **Not run as written: cut-line confirmation.** `SKILL.md:96` says to show the cut line and ask the user to confirm it. The user was unavailable, so it is recorded as needing a decision in the plan summary.

## 6. The next prompt the skills told the user to type

The SKILL's generic example (`SKILL.md:278-282`), quoted verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Because tickets were written, I gave the ticket template's run prompt for the next ready goal on the
critical path. It is the prompt in the plan's "Resume here", quoted verbatim:

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

G01 and G02 are also ready and can run in parallel. Each ticket file ends with its own run prompt in the same form.
