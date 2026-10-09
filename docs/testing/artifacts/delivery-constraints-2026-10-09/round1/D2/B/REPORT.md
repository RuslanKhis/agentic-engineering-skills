# Report: finance expense assistant design session (2026-10-09)

## 1. Skills invoked and reference files opened, in order

Skills invoked: `adk-system-designer` (through the `/adk-system-designer`
command). No other skill was invoked; specialists are named in the plan for
later goals but were not loaded.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the command)
2. `adk-system-designer/references/delivery-profiles.md` (full)
3. `adk-system-designer/references/design-decisions.md` (full)
4. `adk-system-designer/references/failure-review.md` (full)
5. `adk-system-designer/references/gcp-decisions.md` (full)
6. `adk-system-designer/references/implementation-handoff.md` (full)
7. `adk-system-designer/assets/system-design-template.md` (full)
8. `adk-system-designer/assets/implementation-plan-template.md` (full)
9. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full)
10. `*/references/compatibility.md` for all 19 specialists: only the first
    three lines matching "adk/version" via grep, to find the ADK pin (2.8.0)
11. `adk-system-designer/references/runtime-and-delivery.md` (full; trigger:
    session continuity across releases and the browser contract)
12. Small re-reads with `sed`/`grep` for line pointers: `SKILL.md:76-84`,
    `adk-agent-evaluation/references/compatibility.md:5-9`,
    `adk-memory-architecture/references/compatibility.md:5-12`

Not opened: `assets/ticket-template.md` (no tickets requested) and every
specialist `SKILL.md`.

## 2. Questions I would have asked, and the answers I assumed

These are also the **Assumed answers** table at the top of the design (A1–A10).

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first useful version exist, and is it continued afterwards? | End of the three weeks; kept and continued |
| A2 | How familiar are the engineers with ADK/GCP? Who runs it afterwards? | New to ADK; comfortable with GCP, Python, PostgreSQL; the same two engineers run it |
| A3 | What is the model and cloud budget? | About USD 100/month, with a billing alert at 50/90/100 % |
| A4 | Do finance staff only see their own claims, or also other employees' claims (often their job)? | Own claims only in phase 1; reviewer access goes on the Later list |
| A5 | What data does it touch and what can it change? | Real internal personal data (own claims) plus policy text; read only |
| A6 | Where does PostgreSQL run? Is there an email → employee mapping? Is IAM DB auth available? | Cloud SQL for PostgreSQL in the company GCP project; an `employees` table keyed by work email; IAM DB auth can be enabled (falls back to Secret Manager otherwise) |
| A7 | Where do the expense policies live and who approves changes? | A few Google Docs/PDFs (< ~50 pages) owned by the finance controller |
| A8 | Region or data-residency constraint? | Same region as the Cloud SQL instance |
| A9 | What improvement counts as success? | Fewer policy/status questions to the finance mailbox; no numeric target |
| A10 | Existing CI and Git host? | GitHub with GitHub Actions |

I also assumed the caps N = 6 model calls per turn and M = 60 turns per user
per day, and a Google Group named `finance-assistant-users`. I did not ask
whether the cut line is acceptable; the design and plan mark it "for the
user to confirm or move".

## 3. Files written or changed; what was not finished

Written (new):

- `docs/architecture/expense-assistant.md`: draft system design (assumed
  answers, profile, depth table, guarantees I1–I7, decisions D1–D10,
  diagram, data/authority, security posture, budgets, failure table,
  verification, open decisions).
- `docs/plans/expense-assistant.md`: implementation plan with phase 1 (D01,
  G01–G05, 32–43 h of about 54 h capacity), phase 2 (G06–G10, coarse), the
  Later list, and a run prompt for each phase-1 goal.
- `REPORT.md`: this file.

Nothing else was changed. No code, dependencies, tickets or cloud resources.

Not finished, or not done:

- **Every decision is provisional.** The user did not confirm the profile, the cut line or any assumption.
- **Provider facts were not looked up** because network access was not allowed. These are: Vertex availability of `gemini-3.8-flash` in the region, Vertex prices (the cost stays a symbolic formula), the IAP JWT and IAP-on-Cloud-Run setup path, and Cloud SQL IAM DB auth. Each is a named acceptance check in G01, G03 or D01. The design does not cite dated provider URLs as `gcp-decisions.md:37-41` asks.
- **The ADK API names were not checked against the 2.8.0 source.** This is an acceptance item of G01.
- **The design runs longer than the profile's guidance.** It is about 3,900 words; `SKILL.md:81-83` asks for "roughly two to four pages" for an internal tool. I did not trim it.
- **No tickets.** None were requested.

## 4. Checks run and checks not run

Run:

- Relative-link check on both documents (Python, `-I`): all four links resolve. **Pass.**
- Sum of the phase-1 estimates from the plan's goal table: 32–43 h, which matches the stated cut line. Capacity is 54 h (2 × 0.5 × 15 d × 6 h × 0.6). **Pass.**
- Word counts: design 3,900, plan 3,082. **Over the 2–4 page guidance** for the design (see §3).

Not run:

- No unit tests, ADK tests or evaluations. No code exists, and `google-adk` is not installed, so anything importing `google.adk` could not run.
- No network or cloud checks: model availability, prices, IAP and Cloud SQL docs.
- No Markdown lint or rendering check.

## 5. Friction log

- **Helpful: the headless rule settled how to proceed.** The scope gate tells me to ask questions (`adk-system-designer/SKILL.md:54-69`), but the user was unavailable. `SKILL.md:117-120` ("keep asking nothing further: put an **Assumed answers** table…") resolved this clearly.
- **Helpful but slightly odd: the delivery-profiles example matches this request almost word for word.** `adk-system-designer/references/delivery-profiles.md:147-152` already gives the profile, the ≈ 54 h capacity and what to defer. That saved time. It also pre-decides the answer, and its "6 hours/day" for half-time work is not part of the general formula at `delivery-profiles.md:101-103`, so I reused it without an independent basis.
- **Unsure: whether the runtime trigger applied.** The trigger at `SKILL.md:176-179` (runtime-and-delivery) is phrased around requirements that *depend on* streams or concurrent sessions. My design *chose not* to stream and to keep sessions in memory, so it was unclear whether that trigger applied. I read the file anyway. It contributed the "reject overlapping turns" policy and the completed-JSON choice (`runtime-and-delivery.md:23-27, 37-41`).
- **Unsure: the model lifecycle table has no Vertex entry for the newest model.** `SKILL.md:193-197` says to choose from it. In `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12`, `gemini-3.8-flash` has no `vertex_retirement` field, while every older Flash has one. I could not tell whether that means "no retirement announced" or "not on Vertex". I chose it, made Vertex availability a G01 acceptance check, and named `gemini-3.5-flash` as the fallback (line 15).
- **Helpful: the lifecycle table steered the model choice.** It showed that `gemini-2.5-*` retires on Vertex on 2026-10-20 (lines 21-23), which is 11 days from today. A default from memory would have walked into that.
- **Heavier than needed: finding the ADK pin.** `SKILL.md:188-192` says each specialist's `references/compatibility.md` names the ADK version. Finding it took a grep over 19 files. Some state it in prose further down: `adk-agent-evaluation/references/compatibility.md:5-9` and `adk-memory-architecture/references/compatibility.md:5-12` are dated companion environments, not one-line pins. All files that name it agree on 2.8.0. A single pin in the designer skill would have been enough.
- **Heavier than needed: the template pushes the design past the size target.** `SKILL.md:81-83` asks for 2–4 pages for an internal tool. Filling `assets/system-design-template.md` (12 sections, plus the Assumed answers table from `SKILL.md:118`) produced about 3,900 words. The template does not say which sections to compress at this profile.
- **Heavy to scan: `references/design-decisions.md` is 343 lines.** `SKILL.md:93-95` makes it mandatory. Its sections are selectable, but the obligations are spread through prose rather than a checklist. The useful parts here were identity (`design-decisions.md:168-196`), structured output (306-313) and analytical results (327-343). The external-effects material (228-259) did not apply.
- **Helpful: failure-review allows "not applicable".** `references/failure-review.md:4-5` ("do not invent write machinery for a read-only product") let me collapse the write, approval and erasure rows into one sentence.
- **Helpful: three tables were directly usable.** The depth table at `delivery-profiles.md:50-64`, the floor at `:76-83`, and the supporting-skill selection rules at `implementation-handoff.md:39-51` turned straight into the design's depth table and the goals' skill lines.
- **Unsure: the reviewer-reads section seems aimed at assignments.** `assets/implementation-plan-template.md:84-95` ("What the reviewer reads") talks about evaluation summaries and raw run records. For an internal tool it was awkward, and I filled it minimally.
- **Repetitive: the per-goal run prompt.** `implementation-plan-template.md:67-69` requires one per goal, and those prompts are nearly identical. It also asks for a separate, longer continuation prompt at `:113-119`.
- **Gap, from my own knowledge rather than the skills: ADK's `app:` state prefix.** None of the references I read warns that `app:`-prefixed ADK session state is shared across users. That matters when designing "identity in trusted state" (`design-decisions.md:170-174`). I wrote a caution into D3; it was not verified against the ADK source.
- **Network ban left provider facts provisional.** `gcp-decisions.md:37-41` requires current official sources with dates. `SKILL.md:199-200` covers the case where lookup is unavailable, so the design names each check instead.

## 6. Exact next prompt the skills told the user to type

The skill's template, verbatim (`adk-system-designer/SKILL.md:273-275`):

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Instantiated for this plan, as given in the closing message and the plan's "Resume here":

```text
/adk-engineer Carry out G01 from docs/plans/expense-assistant.md.
```
