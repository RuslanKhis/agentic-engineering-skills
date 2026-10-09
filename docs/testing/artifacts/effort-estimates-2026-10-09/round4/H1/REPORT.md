# Report: HR policy Q&A proof of concept (design only)

Paths are relative to this directory. The skill paths are under
`.claude/skills/`.

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer`
   command. Its `SKILL.md` was loaded by the invocation.
2. `adk-system-designer/references/delivery-profiles.md` (all of it)
3. `adk-system-designer/references/design-decisions.md` (all of it)
4. `adk-system-designer/references/failure-review.md` (all of it)
5. `adk-system-designer/references/implementation-handoff.md` (all of it)
6. `adk-system-designer/assets/implementation-plan-template.md`
7. `adk-system-designer/assets/ticket-template.md`
8. `adk-system-designer/scripts/check_schedule.py` (source read, then run)
9. `adk-system-designer/references/gcp-decisions.md`
10. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
11. `adk-memory-architecture/references/compatibility.md`, first 40 lines
12. `*/references/compatibility.md` across all specialists, searched with grep
    for the google-adk version only (every one says 2.8.0)

Not opened: `runtime-and-delivery.md` (no trigger: no streaming, release
continuity or concurrency requirement) and `system-design-template.md` (the
compact form replaces it). No other skill was invoked. Specialist skills were
named in the tickets but not loaded, because nothing was implemented.

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| 1 | Which Friday is the demo? Today is Friday 2026-10-09. Is the POC thrown away or continued? | Friday 2026-10-16. Continued if the demo lands, so the code is written to be kept |
| 2 | How familiar are you with ADK and GCP? Do you already have a GCP project with Vertex AI? | New to ADK (the skill's default, ×1.5), comfortable with Python. Has a company GCP project with Vertex AI enabled |
| 3 | What does the 6 hours look like? | Two dedicated 3 h blocks, focus 0.8, so 2.4 focused h a day |
| 4 | What is the budget for model spend? | A small allowance, ≤ USD 20 for the week, with a budget alert |
| 5 | Who judges the demo, and how? | HR leadership watches you drive `adk web`. They read the answers and citations and may suggest questions |
| 6 | What is in the PDFs? Are they scanned? Superseded? Country-specific? Is there personal data? | Current policies with a text layer, internal-confidential, no employee records, English, one policy set |
| 7 | May these PDFs be sent to Vertex AI (or the Gemini API), and in which region? | Yes, to Vertex AI in the company project. The region is a config value |
| 8 | Is `adk web` acceptable as the demo UI? | Yes |
| 9 | Who can say what a correct answer is? | You can label 5 gold questions. An HR expert labels the larger set in phase 2 |
| 10 | Does the agent do anything besides answer (email HR, open tickets)? | No. It is read-only |
| 11 | Must answers be in languages other than English? | No |

These assumptions appear as the "Assumed answers" table at the top of
`docs/architecture/hr-policy-qa.md`. Questions 1, 2, 6 and 7 are repeated
there as open decisions.

## 3. Files written or changed, and what was not finished

Written:

- `docs/architecture/hr-policy-qa.md`: the design and plan in one file
  (compact form), including the yaml schedule block for G01–G07.
- `docs/tickets/hr-policy-qa/G01-index-policies.md`
- `docs/tickets/hr-policy-qa/G02-cited-answers.md`
- `docs/tickets/hr-policy-qa/G03-gold-check.md`
- `REPORT.md`

Changed: nothing else. I removed one `tests/__pycache__/` directory that my own
pytest run created inside the skill directory.

Not finished, by design:

- No implementation, and no tickets for phase 2 goals G04–G07 (the request
  asked only for phase 1 tickets).
- No provider facts were looked up online: model availability on Vertex in a
  region, prices, Gemini free-tier data terms, and `adk web`'s default
  `max_llm_calls`. They are marked provisional or as checks in G01.
- The design is about 1,880 words including the yaml block and tables. The
  compact-form target is about 1,200, so it is over (see the friction log).

## 4. Checks run and checks not run

Run:

- `python3.13 -I .claude/skills/adk-system-designer/scripts/check_schedule.py
  --plan docs/architecture/hr-policy-qa.md --tickets docs/tickets/hr-policy-qa/
  --capacity 3.6 --days 2 --reserve 0.25 --person "You=2.4"` exited 0.
  Phase 1 is 3 goals and 2.5–3.5 h, which fits 3.6 h. The longest chain is
  G01 → G02 → G03, 1.39–1.94 working days, which fits 2 days. The tickets
  agree with the plan. I also ran it once under Python 3.9.13 with the same
  result.
- The same script with `--phase 2 --person "You=2.4"` exited 0: 22.5–42 h,
  finishing in 14.5–28.33 working days (no capacity given).
- `python3 -m pytest -q -p no:cacheprovider .claude/skills/adk-system-designer/tests`
  (Python 3.9.13; pytest is not installed for 3.13): 9 passed.
- I re-ran the schedule check after the final edits (the plan still fits).
  Only the first two output lines were captured; the exit status was lost to
  zsh's `PIPESTATUS`, so I relied on the earlier exit-0 run. The yaml block
  did not change between the runs.

Not run:

- Any test that imports `google.adk`: there is no code, and the dependencies
  are not installed.
- The planned acceptance checks for G01–G03, including the live Vertex call,
  the `adk web` run and the gold run. They wait for implementation.
- No network, cloud or package-install command was run.

## 5. Friction log

- **Unsure: which Friday.** Today is a Friday, and the request says "the demo
  is on Friday". I assumed next week. The skill's scope gate
  (`adk-system-designer/SKILL.md:59`) handles a deadline but not an ambiguous
  date. This was a judgement call.
- **Unsure: capacity arithmetic.** `delivery-profiles.md:161-171` says to give
  `--person` "full focused hours per day", while `:195-197` defines capacity as
  hours × focus factor and `:200` adds a separate reserve. I used 3 h × 0.8 =
  2.4 as "focused hours" and `--capacity 3.6` (4.8 × 0.75). The worked example
  at `:261-263` (5 h × 0.8 = 4, "roughly 3 after reserve") confirmed it. The
  example was genuinely helpful.
- **Unsure: honest estimates against the starting table.**
  `delivery-profiles.md:137` gives 3–6 h for "retrieval over a small document
  set, checked against a few gold questions", and `:144` says ×1.5 for new to
  ADK. That is 4.5–9 h for retrieval alone, more than all the capacity. I cut
  scope rather than shading numbers (lexical BM25, no tuning loop, 5 questions
  instead of a set; tuning moved to G05) and gave smaller per-goal figures.
  `:181-187` ("change the plan only in ways that are true of the work") was
  the right guard, but there is no guidance on when it is legitimate to come
  in under the starting table. A reviewer may question the figures.
- **Heavier than needed: the 1,200-word compact form.** `SKILL.md:84` and
  `delivery-profiles.md:237`. I came in about 1,880 words. The parts the
  skills require (assumed-answers table, six decisions with tradeoff and
  check, depth table, graduation conditions, failure notes, the yaml schedule
  that `check_schedule.py` needs, phase 2 goals, later table, open decisions)
  do not fit in 1,200 words when every answer is assumed. The yaml block alone
  is about 130 words.
- **Unsure: one file or two.** `SKILL.md:246-247` names `docs/plans/<topic>.md`
  for a multi-goal effort, and the run-prompt example at `SKILL.md:279`
  points at `docs/plans/`. But the compact form (`delivery-profiles.md:237-238`)
  says design and plan go in one file. I used one file under
  `docs/architecture/`. Tickets point their `design:` and `plan:` fields at
  the same file.
- **Unsure: Python version.** `delivery-profiles.md:188` says to report the
  schedule as unchecked without Python 3.11+. Default `python3` here is 3.9.13
  and the script ran fine on it. I re-ran with 3.13 to comply. The
  `$SKILL_DIR` variable in `delivery-profiles.md:165` is not defined anywhere,
  so I used the literal path.
- **Unsure: spend stop under `adk web`.** `delivery-profiles.md:77-80` was
  helpful: put the cap on the project when you do not own the Runner. But
  `gcp-decisions.md:65-66` notes that budgets only alert. For a POC I accepted
  an alert plus the instruction-level search limit, and a real
  `max_llm_calls` only in `run_gold.py`. This is recorded in D6.
- **Genuinely helpful:**
  - The model lifecycle JSON
    (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`)
    caught that `gemini-3.6-flash` retires on Vertex on 2026-11-19. That falls
    inside the phase 2 horizon, so I chose `gemini-3.8-flash`.
  - The trifecta check (`design-decisions.md:182-190`) quickly justified
    leaving `adk-agent-security` out of phase 1, because the agent has no
    write or egress tools.
  - `check_schedule.py` cross-checking ticket front matter against the plan.
- **Mildly confusing:** the ticket template's front-matter key
  `review_and_verify` (`assets/ticket-template.md:13`) differs from the plan's
  `review` (`assets/implementation-plan-template.md:41`). The script maps one
  to the other, so it worked.

## 6. Next prompt the skills told the user to type

The ticket template (`assets/ticket-template.md:53-57`) gives this form, and I
used it in the design's closing section:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-policies.md.
```

The skill's own example is `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`
(`SKILL.md:279`). The full ticket form, as written in G01, is:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-policies.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
