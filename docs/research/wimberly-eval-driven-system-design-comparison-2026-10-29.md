# "Eval-Driven System Design" compared with this toolkit — 29 October 2026

Entry 3 of the [engineering-articles reading plan](engineering-articles-reading-plan-2026-10-28.md).

## The article

- **Article.** Hugh Wimberly, Joshua Marker, Eddie Siegel and Shikhar
  Kwatra, "Eval-Driven System Design: From Prototype to Production", OpenAI
  cookbook, https://developers.openai.com/cookbook/examples/partners/eval_driven_system_design/receipt_inspection.
- **Status.** The page calls itself "a joint collaboration effort between
  OpenAI and Fractional". It shows no date and carries the notice "This
  recipe is archived and may reference outdated models or APIs".
- **Date.** The cookbook's `registry.yaml` (openai/openai-cookbook, main,
  read 2026-10-29) dates it 2025-06-02, marks it `archived: true`, and lists
  the authors as `shikhar-cyber`, Hugh Wimberly, Joshua Marker and Eddie
  Siegel. It is inside the programme's preferred window.
- **Reading.** Read in full on 29 October 2026 with a web-fetch tool, from
  the overview to the contributors list. The page reached its end. The tool
  renders the page through a model, so the figures were taken from four
  targeted reads and then re-derived (Method, step 4) rather than copied.
  The notebook's raw JSON on GitHub was read the same way, to confirm the
  grader definitions and `calculate_costs`. Nothing was cloned or run.

The article builds a receipt-inspection service in two stages. The first
extracts the receipt's fields from the image. The second decides from those
fields, without the image, whether the expense needs an audit. Domain
experts correct the system's draft output to make labels. The service is
then measured three ways: extraction, the audit decision given the
extracted data, and end to end. It does this with 18 graders: exact-match
string checks, fuzzy text similarity and model judges.

The eval results are tied to money through a small cost model,
`calculate_costs(fp_rate, fn_rate, per_receipt_cost)`. It assumes 1 million
receipts a year, 5% needing an audit, $2 an audit and $30 for each missed
audit. It compares the candidate with today's manual process, which catches
97% of needed audits, wrongly flags 2% and costs $0.20 a receipt. Error
analysis follows ("not all evals matter"), then a prompt change, a cheaper
model, an ordered list of further improvements ending in fine-tuning, and
production monitoring.

## Authorship evidence

- **Official company publication.** The OpenAI cookbook is OpenAI's own
  developer site. The page states the joint collaboration "between OpenAI
  and Fractional".
- **Shikhar Kwatra.** He is listed in the cookbook's `authors.yaml` as
  `shikhar-cyber`. Bain & Company's team page lists him as "Partner Solution
  Architect, OpenAI". A profile built from LinkedIn data dates the OpenAI
  role from December 2024, before the article's June 2025 date. His LinkedIn
  page itself (login wall) was not read.
- **The other three authors.** Wimberly, Marker and Siegel are not in the
  cookbook's author registry, and the page links the partner to
  fractional.ai. They are taken to be Fractional's, as the plan says. This
  was not checked further.
- **Criterion met.** An OpenAI author at the time of writing, on an
  official OpenAI publication.

## Method

1. Read the article in full (see above). Then four targeted reads:
   - the "Initial Evals" and "Graders" sections, for which input each stage
     is graded on;
   - "Connecting Evals to Business Metrics", for every figure;
   - "System Improvements" and "Model Choice", for the error attribution
     and the cheaper-model figures;
   - the contributors and archive notice.
2. Re-read every file the plan names, as entries 1 and 2 left them:
   - adk-agent-evaluation: `result-auditing.md`, `quality-iteration.md`
     (including "Tell a change from noise"), `evaluation-design.md`
     ("Shape the rubric before writing it" and the sections after it) and
     `expert-review.md` ("Re-check where the costly error lands");
   - adk-discovery: `discovery-brief-template.md`, `technology-fit.md`,
     `opportunity-portfolio.md`;
   - adk-presenter: `value-report.md` and its template, and the value-report
     checker.
3. Searched `skills/` for "cost of a wrong", "cost of errors", "error
   cost", "price each", "priced", "per error", "not all evals",
   "conditioned on", "ignore its input", "gold upstream" and "upstream
   error". Results:
   - no skill turns an error rate into money;
   - error cost appears only in words (`discovery-brief-template.md` "Cost
     of a wrong answer", `technology-fit.md` step 5, `handoff-to-design.md`,
     the governance pack's impact assessment);
   - no skill says which input a stage's grader is fed.
4. Re-derived every figure with the Python standard library before it went
   into a skill:
   - the current process: $135,000 in audits, $45,000 in misses and
     $200,000 in processing, $380,000 in all;
   - the first o4-mini configuration (1/12 false flags, 1/8 misses, $0.01 a
     receipt): $443,333. This matches the article's "increase our overall
     costs by $63,000 per year";
   - the article's own cheaper configuration: $261,333, with a break-even
     miss rate of 8.5%;
   - the handwritten-mark figure: $75,000 is 1% prevalence × 50% missed ×
     50% leading to no audit × $30;
   - the math-error figure: 20% of 950,000 receipts × $2 is $380,000 ("almost
     $400,000");
   - 2 points of miss rate at the example's volume is $28,000 (1,000 misses at $30, net of the $2 audit each would have had; corrected in review from $30,000).
5. Checked ADK for the isolated stage run: `EvalCase.session_input.state`
   seeds the session state in google-adk 2.8.0 and 2.12.0
   (`evaluation/eval_case.py`, `SessionInput.state`;
   `evaluation_generator.py` creates the session with it).
6. Ran the value-report checker on three trial lines for the new "cost of
   errors" line, to word the presenter guidance so that a correct line
   passes (see Imported).

## Imported

**adk-agent-evaluation.**

- **`evaluation-design.md`, new paragraph "Grade each stage on the input it
  received".** It extends entry 1's horizon bullet, which said only to grade
  each stage's saved output and keep the verdicts.
  - A stage's grader reads the stage's actual input from this run, not the
    gold version, and asks whether the output is right for that input.
  - Graded against the end-to-end reference, a stage is pushed to ignore
    its input. This is the article's warning, restated.
  - There are three ways to get a reference that fits the actual input:
    code (the verifiability axis), an unchanged input, or a judge or
    reviewer. Until one decides, the verdict is `not evaluated`.
  - Each stage keeps three results: end to end, the stage on its actual
    input, and the stage run alone on the gold upstream record. In ADK the
    last is an eval set for the stage's agent alone, with
    `session_input.state` seeding the key it reads.
  - A case that fails end to end while every stage passed on its own input
    lost something at a hand-off. The article says splitting a process
    lets stages "play telephone".
  - The horizon bullet gained one sentence pointing to the paragraph.
- **`evaluation-design.md`, new paragraph "Price each error type, and gate
  on the priced total against today's process".**
  - The cost formula, restated from `calculate_costs` in plain terms
    (volume, share needing the action, miss rate, false-flag rate, running
    cost, handling cost of a flag, cost of a miss).
  - An escalated case is priced as manual work, following entry 1's rule.
  - The gate: the candidate's total below today's, not a rate above a round
    number. The article's example is given with its arithmetic, with a
    note of what the total leaves out.
  - "Not all evals matter": a field error that changes no decision is
    reported, not gated.
  - A small sample prices indicatively. It reuses expert review's
    per-class minimum of 30, quotes counts, and adds the rule of three and
    a break-even miss rate (this repository's additions; see Conflicts).
  - Between two versions, the paired interval (entry 2) says whether a
    rate moved, and the price says what the move is worth. This closes
    entry 2's "Left for later entries" note.
  - A price never buys a hard rule.
  - The stakes bullet gained one sentence pointing to the paragraph.
- **`quality-iteration.md`, the loop's step 3.**
  - Only defects that change something downstream count towards the first
    change.
  - Categories are ranked by cost when the brief prices errors.
  - In a staged pipeline, `stage` names the stage that was wrong on its own
    input.
- **`result-auditing.md`.** The "first violated boundary" sentence says
  that a stage right on its input has not violated its boundary.
- **`SKILL.md`.** Two routing sentences are extended (quality iteration;
  the rubric bullet). The description is unchanged.

**adk-discovery.**

- **`opportunity-portfolio.md`, new bullet "Price of each error"** in
  "Define the measure before the build":
  - the two errors of a decide-or-flag use case;
  - the price of a miss and the handling cost of a flag, with sources (every
    flag costs its handling; a false flag is the part that buys nothing);
  - the share that needs the action, and today's rates and cost per case;
  - "unknown: ask <role>" when nobody can give a price.
  The article's receipt figures are the example.
- **`discovery-brief-template.md`.** A "Price of each error" field after
  "Cost of a wrong answer".
- **`technology-fit.md`, step 5.** "High" error cost is judged against
  today's process, which has error costs of its own.
- **`handoff-to-design.md` and `SKILL.md`.** One clause each, so that the
  designer receives the prices and the brief asks for them.

**adk-presenter.**

- **`value-report.md`, cost per outcome.**
  - When the brief prices errors, a cost-of-errors line sits beside today's
    process priced at the period's volume.
  - Counts scaled from a sample or from evaluation rates take the Estimate
    voice.
  - Unit prices are cited from the brief rather than written on a measured
    line. The checker reads "£30 a miss" as a cost per outcome and asks for
    a cost record and a count record; this was confirmed by running
    `check_value_report.py` on three versions of the line.
- **`value-report-template.md`.** The matching optional bullet.

**Scenario cases.** Three new cases in `evals/scenarios.json`:

| Case | Fixture |
| --- | --- |
| `evaluation-priced-errors-and-stage-attribution` | `evals/fixtures/` overlay: a two-stage invoice-hold agent, 40 synthetic run records (seed 3), a dashboard, hold rules and a brief extract; judge-only material under `evals/graders/` with the priced figures and the stage re-attribution |
| `discovery-price-each-error` | runnable from the context |
| `presenter-value-report-error-cost` | runnable from the context |

All three are listed in `evals/scenario-fixtures.json`.
`run_scenarios.py list` classifies the first as repo-fixture and the other
two as runnable.

**After the trial (same day).** Three changes to the pricing paragraph in
`evaluation-design.md`:

- **Break-even formula.** It holds the false-flag rate at its measured
  value. It was checked at 14.2% on the fixture and 8.5% on the article's
  cheaper configuration.
- **Where N and p come from.** Both come from the brief, never the
  labelled sample. Rates within each class price correctly from an
  enriched development set; overall accuracy on that set does not.
- **A correct flag.** It is priced at its handling. Only an escalation in
  place of a decision the agent should have made counts as manual work.

## Linked only

None.

## Not imported, with reasons

- **The grader types (string check, text similarity with BLEU or fuzzy
  match, score model) and the Evals API run shape.** These are OpenAI Evals
  API facts. The method behind them, code checks before judges and one
  judge per failure mode, is already covered (`evaluation-design.md`
  verifiability axis and "Calibrate the judge on fixed evidence";
  `expert-review.md` "Calibrate one judge per failure mode").
- **Model names and prices (o4-mini, o3, gpt-4.1-mini, $0.01 and $0.003 a
  receipt).** Another vendor's models. Only the dollar figures of the cost
  example are quoted, as the authors' assumptions.
- **Draft labels corrected by experts.** The article builds its ground
  truth by having experts correct the model's draft. `expert-review.md`
  has experts label traces whole, from open coding. Correcting drafts is
  cheaper, but it risks anchoring the labeller on the draft, and the
  article does not measure that. Not imported. It belongs in expert review's
  session design if a later source measures it.
- **Labelling first the inputs where models disagree** ("if a dumb model
  agrees with a smart model then it's probably not a hard problem"). A
  heuristic with no measurement, and outside the plan entry. Expert
  review's sampling step already includes "the hard cases the experts
  name, and recent failures". Recorded here for a later change.
- **The ordered list of improvements (model, prompt, examples, tools,
  accessory models, fine-tuning) and graders as reinforcement fine-tuning
  rewards.** Fine-tuning needs a training run, not an application change,
  which the programme excludes. The order of cheaper changes is close to
  quality iteration's one-change loop.
- **Start with a capable model, then try cheaper ones.** Already covered:
  adk-model-and-output-contracts `SKILL.md` ("Choose models by measured
  quality on the project's development set, then cost, then lifecycle. A
  cheaper model is a hypothesis …"). The new pricing paragraph adds only
  that such a change is compared on the priced total.
- **Production monitoring, sampling real traffic for review, and deploying
  a new version only when it beats the current one.** Already covered:
  adk-agent-observability (traces into evaluation cases),
  adk-release-engineering (production feedback, CI gates).
- **Escalating low-confidence cases to QA.** The article lists QA volume
  as a cost driver but leaves it out of `calculate_costs`. The skills price
  an escalated case as manual work (entry 1's rule), and the guardrails
  skill owns escalation. Nothing else changes.
- **Choosing a judge's TPR or TNR threshold from the prices.** A natural
  extension of the stakes axis, but the article does not discuss judge
  thresholds. `expert-review.md` keeps its rule ("favour TPR when a missed
  failure is costly …").
- **The workflow-side re-check (`content-safeguards.md`).** Nothing in the
  article changes the runtime rule. Prices can say which verdict's error
  costs most, and the stakes bullet now points to them.

## Conflicts

- **Ranking error categories by size versus by cost.** `quality-iteration.md`
  said "The largest category names the first change", and `SKILL.md` said
  "the first change targets the largest category". The article's "not all
  evals matter" refines this rather than contradicting it. A defect that
  changes nothing downstream does not count, and a priced brief ranks by
  cost. The worked example in `SKILL.md` (retrieval first, because it
  causes missed policies) still holds. Both sentences were extended, not
  replaced.
- **The article's reference for the audit stage.** The article says to
  judge each step "conditioned on the output of the prior step". Its code
  compares the audit decision with the stored ground-truth decision, which
  was made on the correct receipt, not recomputed from the extracted
  fields. Its reasoning judge sees the extracted fields beside that
  decision, and the attribution in "System Improvements" was done by hand.
  The toolkit follows the stated principle and says how to get a reference
  that fits the actual input. It records the code's behaviour here.
- **Small-sample pricing.** The article prices a configuration whose sample
  had 0 misses in 8 and notes only that "our real false negative rate will
  be more than the 0 we see here". The toolkit keeps its own rule: below
  the per-class minimum a rate is indicative (`expert-review.md`,
  `label_agreement.py --min-per-class`). It adds the rule of three and a
  break-even miss rate, so the price cannot be read as a verdict. These two
  are this repository's additions, not the article's. Entry 2 left
  intervals on rates for later. The rule of three is the one-sided bound
  for zero events only; a general interval on a rate is still left for a
  later change.
- **Entry 1's outcome measure.** Entry 1 made the headline the outcome
  measure ("share of cases decided correctly with no manual intervention"
  for act-or-escalate). The priced total is that measure expressed in
  money, with the errors weighted. The two are reported together, and the
  priced total is the go or no-go gate when the brief prices errors. No
  text of entry 1 was changed.

## Left for later entries

- **Entry 23 (GDPval).** Review-adjusted savings: agent time + review time
  + (1 − acceptance) × manual time. The value report's new line prices
  errors and holds, but not the redo time of accepted-then-revised work.
- **Entry 44 ("Deploying AI from pilot to production").** Error cost at
  full volume before scaling, in the value report's call table, and
  checkpoint audits (catch rate, change rate, cost). This entry changed
  only section 4 (cost per outcome), not the call table.
- **Entry 4 (agent quality flywheel).** A categorical rubric with a
  not-applicable class. The stage verdict's `not evaluated` used here is
  ADK's status, not that rubric class.

## Limits

- **Reading.** Read through a fetch tool that renders the page through a
  model. Every figure used was re-derived. The handwritten-mark ($75,000)
  and math-error ("almost $400,000") estimates rest on the authors'
  assumed prevalence and are marked "reported by the source, not verified
  here" in the skill.
- **Archived recipe.** The page warns that its models and APIs may be
  outdated. Nothing from them was imported.
- **Synthetic data only.** The scenario's invoice records are synthetic,
  generated with a seeded script. No model was called.
- **Trial.** See the
  [testing record](../testing/wimberly-eval-driven-system-design-alignment-2026-10-29.md).
