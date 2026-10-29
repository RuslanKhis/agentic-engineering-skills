# "Eval-Driven System Design" alignment — 29 October 2026

Source note: [comparison](../research/wimberly-eval-driven-system-design-comparison-2026-10-29.md).

## Changed journeys

- **adk-agent-evaluation.**
  - Grading each stage of a pipeline on the input it actually received, and
    attributing a wrong outcome to the stage that was wrong on its own
    input (`evaluation-design.md`, "Grade each stage on the input it
    received"; `result-auditing.md`; `quality-iteration.md` step 3).
  - Pricing each error type at the brief's volume, and gating on the priced
    total against today's process (`evaluation-design.md`, "Price each
    error type").
  - Ranking error categories by what they cost, and leaving out defects
    that change nothing downstream ("not all evals matter").
- **adk-discovery.** The brief records the price of each error type, the
  share of cases that need the action, and today's rates and cost per case
  (`opportunity-portfolio.md`, the brief template, `technology-fit.md` step
  5, `handoff-to-design.md`).
- **adk-presenter.** The value report's cost per outcome gains a
  cost-of-errors line, beside today's process priced at the same volume
  (`value-report.md` and its template).

**New scenario cases.**

| Case | Status in `evals/scenario-fixtures.json` |
| --- | --- |
| `evaluation-priced-errors-and-stage-attribution` | repo-fixture: overlay under `evals/fixtures/`, judge-only material under `evals/graders/` |
| `discovery-price-each-error` | runnable |
| `presenter-value-report-error-cost` | runnable |

## Fresh-agent trial

**Set-up.** One trial, run on 29 October 2026.

- **Agent.** A general-purpose subagent with a fresh context, on the same
  model as the coordinator (Claude Opus 5.5). It was told to work only
  inside the workspace and to read the installed skills' `SKILL.md` first.
  It did not see the scenario assertions or the judge material.
- **Workspace.** In the session scratchpad: the
  `evaluation-priced-errors-and-stage-attribution` overlay, plus copies of
  adk-agent-evaluation, adk-agent-instructions, adk-discovery and
  adk-presenter under `.claude/skills/` (without `tests/`). The copies were
  taken before the post-trial fixes below.
- **Data.** Synthetic run records generated with a seeded script (seed 3):
  - 40 labelled development cases of a two-stage invoice-hold agent, 10 of
    which should be held;
  - a team dashboard claiming 90% accuracy against an 88% target, which
    blames all four wrong decisions on the decision stage;
  - a brief extract with the volume, today's clerk-check rates and cost,
    and the price of each error.
- **Prompt.** The scenario's prompt and context. It was asked to write
  `docs/plan-review.md` and report frictions.
- **Limits.** Shell for reading and standard-library arithmetic only; no
  model, network or ADK. About 12 tool calls in about 2.5 minutes.

**What it did.**

- **Skills read.**
  - all of the evaluation `SKILL.md`;
  - all of `quality-iteration.md` and `result-auditing.md`;
  - the whole of "Shape the rubric before writing it" in
    `evaluation-design.md`, including both new paragraphs;
  - adk-agent-instructions' `instruction-vs-code.md`;
  - discovery's "Price of each error" paragraph, found by grep.
- **Answer.**
  - The plan is wrong on all three steps.
  - Supplier names: 18 of 40 wrong, no decision changed, no rule reads
    the field, so they are not a gate.
  - dev-011 and dev-027 are extraction errors: invoice numbers read with a
    letter O, so the duplicate lookup failed. `decide_hold` was right for
    its input, and these are the two £180 misses, so they are the first fix.
  - dev-014 and dev-036 are decision-stage errors: holds inside the 2%
    tolerance. Move that check into code rather than rewrite the prompt.
  - Priced at the brief's volume: today £398,592 a year; this run £495,840,
    about £97k more. Miss rate 2 of 10 against a break-even of about 14%.
  - Indicative because there are only 10 hold cases. Do not ask for the
    switch-off; collect a holdout with at least 30 should-hold invoices,
    and make the switch-off conditional on its priced total beating today's.
- **Ease.** 5 of 5 for finding the method, 4 of 5 for applying it.

**Against the scenario assertions** (graded by the coordinator from the
report and `docs/plan-review.md`):

| Assertion | Result |
| --- | --- |
| Priced totals for today (about £399k) and the agent (about £496k); 90% against 88% not the gate | Pass (£398,592 and £495,840) |
| dev-011 and dev-027 re-attributed to extraction; only dev-014 and dev-036 are decision-stage errors | Pass |
| Supplier names not a gate; invoice-number extraction first | Pass |
| Indicative with 10 hold cases; counts given; more hold cases before go-live; no switch-off | Pass |
| Works from the records; no model run | Pass |

The discovery and presenter journeys were not trialled. Their scenario
cases are runnable from the context, but no session ran them.

## Frictions and fixes (same day)

1. **The break-even rate had no formula.** The trial agent did not know
   which false-flag rate to hold fixed, and reported three values (14% to
   20%).
   - **Fix.** `evaluation-design.md` now gives the formula, with the
     false-flag rate held at its measured value. It was checked against
     the fixture (14.2%) and the article's cheaper configuration (8.5%).
2. **An enriched development set.** The set had 25% holds against the
   brief's 4%, and nothing said which share to use or whether accuracy on
   such a set compares with a target.
   - **Fix.** The pricing paragraph now says to take N and p from the
     brief, never the sample. Rates within each class do not depend on how
     the sample was drawn. Overall accuracy on an enriched set is not
     compared with today's or with a target.
3. **Is a correct hold manual work?** Entry 1's rule ("count an escalated
   case as manual work") left it unclear whether a correct flag, which
   goes to a person by design, counts against the agent.
   - **Fix.** A correct flag is the action working, priced at its
     handling. An escalation in place of a decision the agent should have
     made is priced as manual work.
4. **No interval for one version against a fixed target** ("does 36 of 40
   clear 88%?"). Not changed. A general interval on a single rate is the
   item entry 2 left for later. This article does not supply one, and the
   new text no longer treats accuracy against a target as a gate.
5. **Rare-class holdouts.** Stratified sampling of the rare class with
   reweighting is not described. Partly answered by fix 2: per-class rates
   price correctly whatever the mix. Holdout sizing for the rare class
   stays with "Tell a change from noise" and the per-class minimum.
6. **Numeric tolerance checks in adk-agent-instructions.** That skill's
   instruction-versus-code table has no row for "a numeric threshold or
   tolerance". Not changed: that skill is outside this article's scope,
   and the verifiability axis in `evaluation-design.md` covers it. Recorded
   for adk-agent-instructions' owner.

The fixes were not re-trialled with a fresh session.

## Scenario run (after review)

After the review, the user approved a paid scenario run. The three new
scenarios ran through `scripts/run_scenarios.py run` on 2026-10-29. Agent
and judge were `claude-sonnet-5-5` through `claude-cli`, with three judge
repeats (majority verdict), `--max-budget-usd 3` per agent run, a project
skill install and no shell. The first run cost $0.77 ($0.54 for the agents
and $0.23 for the judges), and the presenter re-run $0.33.

| Scenario | Passed | Primary skill loaded | Notes |
| --- | --- | --- | --- |
| evaluation-priced-errors-and-stage-attribution | 5/5 | yes | It priced today's process at about £399k and the agent at about £496k, moved dev-011 and dev-027 to extraction, ruled out the supplier name as a gate, and called the sample indicative. |
| discovery-price-each-error | 3/3 | no | Two assertions passed on split votes. It answered in two turns without loading the skill, and its monthly figure for today's process left out the handling of correct holds (£28.7k against £33k). |
| presenter-value-report-error-cost | 2/3, then 3/3 | yes | First run: it priced only the needless holds (£3,840, not £8,400 for all 1,400 handled), so both totals left out correct holds. |

**Follow-up.** The value report said to price "the period's misses and
false flags". That contradicted the evaluation formula, which charges every
flag its handling cost, needed or not, and the agent followed the wording.
`value-report.md` and `value-report-template.md` now price every handled
flag plus the misses, with today's process priced the same way. On the
re-run the presenter scenario passed 3 of 3, with split votes on A1 and A2.
The discovery skill was again not loaded for a direct sizing or pricing
question, the same activation miss as Miller's discovery scenario. It is
left open as an activation item.

## Checks

- **`.venv/bin/python scripts/check_repo.py`: passed.**
  - 28 offline suites, 1,232 tests (unchanged; no helper was added).
  - 26 skill packages, with 0 errors and the 3 existing warnings.
- **`git diff --check`:** clean.
- **`.venv/bin/python scripts/check_source_freshness.py --validate-only`:**
  "Register valid: 98 sources; nothing was fetched."
- **`.venv/bin/python scripts/run_scenarios.py list`.** It classifies the
  two context-only cases as runnable and the evaluation case as
  repo-fixture.
- **Value-report checker.** `check_value_report.py` was run on three
  versions of the new cost-of-errors line:
  - a line citing records and the brief: exit 0;
  - a line in the Estimate voice: exit 0;
  - a line writing "£30 a miss": exit 1, cost per outcome without both
    records. The guidance tells authors to cite the brief for rates.
- **Figures checked numerically** with the standard library:
  - the article's $380,000, $443,333 (the article's "+$63,000") and
    $261,333;
  - its $75,000 and "almost $400,000";
  - the fixture's £398,592 and £495,840, and the break-even at 14.2%;
  - the 2-in-10 interval (2.5% to 55.6%).

## Limits

- **One trial.** One trial on one synthetic fixture. It is not a paired
  comparison with the skills before this change.
- **Same model family.** The trial agent used the same model family as the
  author of the change.
- **Single scenario runs.** Each scenario ran once (presenter twice), so
  one run cannot separate a skill defect from run variance. No ADK Runner
  or `adk eval` run.
- **Untested content.** The discovery reference's content went untested,
  because the skill was not loaded. The trial's own fixes were not
  re-trialled.
