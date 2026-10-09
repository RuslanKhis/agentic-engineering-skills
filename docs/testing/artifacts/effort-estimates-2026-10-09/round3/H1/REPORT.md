# REPORT: HR policy Q&A POC design session

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user via `/adk-system-designer`). No other skill was invoked.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (whole file)
3. `.claude/skills/adk-system-designer/references/design-decisions.md` (whole file)
4. `.claude/skills/adk-system-designer/references/failure-review.md` (whole file)
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md` (whole file)
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/assets/ticket-template.md`
8. `.claude/skills/adk-system-designer/scripts/check_schedule.py` (header and argument list only)
9. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (for the model pin, as SKILL.md:198 directs)
10. `.claude/skills/adk-memory-architecture/references/compatibility.md` (grep only, for the ADK pin `google-adk 2.8.0`)
11. `.claude/skills/adk-memory-architecture/references/local-document-coverage.md` (first 30 lines) and `retrieval-strategy.md` (headings only)

These were not opened because their triggers did not apply: `runtime-and-delivery.md`, `gcp-decisions.md`, `assets/system-design-template.md`. The compact form replaces the full design template.

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| 1 | Which Friday is the demo? Today, 2026-10-09, is a Friday. | Next Friday, 2026-10-16 |
| 2 | Is the POC thrown away or continued if the demo lands? | Probably continued, so phase 1 is written to be kept |
| 3 | How familiar are you with ADK and GCP? | Comfortable with Python, new to ADK, so ×1.5 on every estimate. A billed GCP project or Gemini API key is available |
| 4 | What can you spend on models? | Under US$20 for the POC |
| 5 | Will HR leaders use it themselves or watch you demo it? | You demo by screen share with `adk web`, and they suggest questions |
| 6 | Do the PDFs contain personal data, and are they text based or scanned? | No personal data, text based. G01's report verifies the second part |
| 7 | May internal HR policies be sent to Gemini on your project? (O1) | Yes, on a billed project or Vertex AI. You must confirm this before G02's live check |
| 8 | Do the policies vary by country, entity or employee group? | One jurisdiction |
| 9 | Should it interpret policies or only quote them? (O3) | Summarise with page citations, and refuse when the policies are silent |
| 10 | Language? | English |
| 11 | Is the hour split OK: 6 h × 0.8 focus, with a 25% reserve for demo preparation? | Yes, which leaves 3.6 h for goals |
| 12 | Confirm or move the cut line: G01–G03 ship and G04 onward waits? | Confirmed as proposed |

## 3. Files written or changed, and what was not finished

- `docs/architecture/hr-policy-qa.md`: the design and plan in the compact POC form, marked **draft**, with an assumed-answers table, decisions D1–D6, the floor and depth table, the phase 1 YAML schedule, phase 2 goals G04–G07, a "later" list and open decisions O1–O3.
- `docs/tickets/hr-policy-qa/G01-extract-corpus.md`, `G02-answer-with-citations.md`, `G03-gold-questions-and-dry-run.md`: one ticket per phase 1 goal.
- `REPORT.md`: this file.

Not finished or not done, by design:
- No implementation (the user said not to implement).
- Phase 2 goals have no tickets. They are coarse in the plan, as the skill specifies.
- The design is about 1,700 words by `wc -w`, including the YAML and table syntax. That is over the skill's target of about 1,200 words, and I did not trim it further.
- The design is still a draft because the 12 assumptions above are unconfirmed.
- The model and ADK pins come from the skills' bundled snapshots. They were not checked against live documentation, since no network was allowed.

## 4. Checks run, and checks not run

**Run:**
- `python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/architecture/hr-policy-qa.md --tickets docs/tickets/hr-policy-qa/ --capacity 3.6 --days 2 --person "Builder=1.8"`
  - First run: **exit 1**, for two reasons. The G02 wait text in the ticket differed from the plan. The calendar fitted only at the low end, because the 0–1 day O1 wait pushed the high end to 3 days.
  - Fix: O1 is now assumed to be requested before day 1 (`wait_days: 0`), the wait text matches in both files, and the plan states the risk.
  - Re-run: **exit 0**. Phase 1 is 2.3–3.6 h against 3.6 h of capacity, so it fits. The chain is G01→G02→G03, the finish range is 1.28–2 working days, and the calendar fits.
- `wc -w` on the design: 1,709 words.

**Not run:**
- No project tests exist. There is no code, and the design-only request means none was written.
- No test that imports `google.adk`: the dependencies are not installed, and no network or package installs were allowed.
- The skill's own `tests/test_check_schedule.py`: it was not needed for this task.
- No live model calls and no cloud checks, including the model lifecycle and pricing.

## 5. Friction log

- **Unsure about the default `python3`.** The script asks for Python 3.11 or later (`delivery-profiles.md:173`). The default `python3` here is 3.9.13. I found `/opt/homebrew/bin/python3.11` and used that. The line at `delivery-profiles.md:163` writes `python3 "$SKILL_DIR/..."`, which would have run 3.9. A version guard or a `python3.11` hint would help.
- **Unsure how to show the assumed answers.** SKILL.md:123 asks for an "Assumed answers table at the top, one row per question". `delivery-profiles.md:228-229` says to fold assumed answers into the scope-gate table, one line each. I folded the scope-gate assumptions into the design's table and put the full list of 12 questions in this report. The two instructions overlap but are not identical.
- **Unsure where the plan lives.** SKILL.md:247 says a small effort can keep its plan in the design. But the example prompt at SKILL.md:279, the plan template (`implementation-plan-template.md:93`) and the ticket front matter (`ticket-template.md:5`, `plan:`) all assume a separate `docs/plans/` file. I kept the plan in the design, and both `design:` and `plan:` point to the same file. That worked, but it looked odd.
- **Unsure where the ADK pin check belongs.** SKILL.md:197-198 puts "confirm against the chosen pin" on the first implementation goal. My G01 (PDF extraction) does not import ADK. I put the pin in G01's `pyproject.toml` and the API confirmation in G02.
- **Unsure which focus factor to use.** `delivery-profiles.md:181` gives 0.6 for part-time and 0.8 for a dedicated block. "6 hours over two days" fits either. I chose 0.8 and recorded it as assumption 11.
- **Heavier than needed:** `design-decisions.md` (343 lines) is mostly about writes, approvals, OAuth and shared budgets, and none of that applies to a read-only POC. SKILL.md requires reading it for "the sections its journey touches", but finding those sections meant reading all of it. `failure-review.md:4-5` ("do not invent write machinery for a read-only product") helped me keep the failure paths to four lines.
- **Heavier than needed:** the 1,200-word target (SKILL.md:84) is hard to meet once the required YAML schedule, per-goal run prompts and phase 2 entries are included. I ended at about 1,700 words.
- **Helpful:** `check_schedule.py` caught a real wait-text mismatch between the ticket and the plan. It also caught a calendar overrun I had written into the plan prose before running it (SKILL.md:93; `delivery-profiles.md:157-174`).
- **Helpful:** the estimation guidance (`delivery-profiles.md:128-146`, with the ×1.5 rule) and the reserve rule (`delivery-profiles.md:185`) forced the cut that removed a separate demo-preparation goal.
- **Helpful:** the dated model lifecycle snapshot (SKILL.md:198) kept me from pinning a "limited" 2.5 model from memory.

## 6. The next prompt the skills told the user to type

The skill's closing instruction (SKILL.md:273-279) gives this form: `/adk-engineer Carry out G01 from docs/plans/<topic>.md.` The ticket template's prompt (`ticket-template.md:53-57`), filled in for this plan, is:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-extract-corpus.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
