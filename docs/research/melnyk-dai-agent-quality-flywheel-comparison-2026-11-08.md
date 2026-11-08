# "Driving the Agent Quality Flywheel from Your Coding Agent" compared with this toolkit — 8 November 2026

Entry 4 of the [engineering-articles reading plan](engineering-articles-reading-plan-2026-10-28.md).

## The article

- **Article.** Dima Melnyk and Jason Dai, "Driving the Agent Quality
  Flywheel from Your Coding Agent", Google Developers Blog, 30 June 2026,
  https://developers.googleblog.com/en/driving-the-agent-quality-flywheel-from-your-coding-agent/.
- **Reading.** The user pasted the full text on 8 November 2026. It was
  saved verbatim to the session scratchpad, not to this repository, and
  read in full from the title to the credits. A web search confirmed the
  URL, the date and the byline. The two result tables appear in the paste
  only as image names (`table1_first_pass`, `table2_before_after`), so
  their cells were not read. Every figure used here comes from the prose.

The article introduces a skill that a coding agent runs to improve an
agent's quality. It has five stages: prepare data, run inference, grade,
analyse failures, and optimise. Two worked cycles use ADK samples from
google/adk-samples.

- **travel-concierge.** The aim was to check that the agent honours
  changes the user makes mid-conversation. The skill added a custom
  categorical rubric, `revision_honored`, beside two adaptive built-in
  metrics and set an action threshold of more than 20% IGNORED. It then
  synthesised 25 scenarios across five revision types. 21% came back
  IGNORED. A three-sentence instruction fix brought that to 5%.
- **software-bug-assistant.** The agent never named the tools it had
  used, in 14 of 15 cases. A one-paragraph instruction fix brought
  compliance from 0% to 96%.

## Authorship evidence

- **Official company publication.** The Google Developers Blog is
  Google's own developer blog.
- **Bylines.** The bylines read "Dima Melnyk, Product Manager, Cloud AI"
  and "Jason Dai, Software Engineer". The credits name the Cloud AI Agent
  Platform team.
- **Criterion met.** Google authors at the time of writing, on an official
  Google publication.

## Method

1. Saved the pasted article to the scratchpad and read it in full.
2. Re-read the files the plan names, as entries 1 to 3 left them:
   - adk-agent-instructions: `prompt-as-code.md` "Optimisers";
   - adk-agent-evaluation: `live-evaluations.md` (managed simulation, the
     managed scorer's contract, Agents CLI limits) and
     `evaluation-design.md` ("Shape the rubric", "Calibrate the judge",
     "Grade the end state").

   Also re-read `quality-iteration.md` "Run the loop" and `expert-review.md`
   "Calibrate one judge per failure mode".
3. Searched `skills/` for "flywheel", "autorater", "user simulator", "loss
   analysis", the multi-turn metric names, "categorical", "not applicable",
   "adaptive", "independent", "proposes", "tool schema" and "revision".
   Results:
   - Google's agent-quality-flywheel sample is already cited in
     `live-evaluations.md`. That covers the pairing of a judge with a
     deterministic count, the single instruction change, and "trust the
     delta between runs more than any single absolute number".
   - Clustering above ten failures, the server-side scenario generation
     and the Agents CLI `synthesize`, `grade` and `analyze` commands are
     already covered.
   - Nothing said that the proposer of a change must not grade it.
   - Nothing said that adaptive metrics cannot track one behaviour.
   - Nothing covered the trajectory rater needing the agent's tool
     declarations.
4. Worked out the size of the 21% to 5% move from the article's own
   statement that there were four IGNORED cases: 4 of 19 applicable cases
   is 21%, and one case afterwards is about 5%. The article does not state
   the denominator, so the skill says "about four cases to one".

## Imported

**adk-agent-evaluation.**

- **`evaluation-design.md`, new paragraph "Give the behaviour a change
  targets its own fixed, categorical metric"** in "Calibrate the judge on
  fixed evidence":
  - Adaptive multi-turn metrics regenerate their criteria for each case
    and blend them into one score, so they detect a miss without isolating
    it. The 0.80 task-success example is given.
  - The fix is one fixed judge with categorical verdicts and a
    not-applicable class. Its rate is taken over the cases where the
    behaviour arose. A code check replaces it where code can decide.
  - The action rule is set before the run. Judge, version and cases stay
    fixed across cycles.
  - The new judge is calibrated like any other. The article reports no
    calibration, and its move from 21% to 5% is about four cases to one,
    so it is read with the paired interval.
  - The adaptive metrics stay as the broad-health signal.
  - The state-right, reply-wrong failure: in three of four IGNORED cases
    the state held the revised value while the reply repeated the old one.
    A revision case checks the reply against the latest state. This points
    to "Grade the end state", step 4, which already requires that no claim
    contradicts the end state.
  - In an Agents CLI project the judge is a local `custom_function` judge,
    and the class is kept per case.
- **`quality-iteration.md`, step 4.** Whoever proposed the change never
  grades it:
  - The keep-or-revert verdict comes from the evaluation fixed before the
    change.
  - A coding agent that wrote the change does not edit the cases, rubric,
    judge or thresholds in the same iteration, and its reading does not
    replace the evaluator's labels.
  - The article's warning is quoted: an optimiser that grades itself
    "learns to game the metric instead of improving the agent".
  - When the author of the change is the only labeller, it labels both
    versions without knowing which version produced which output. This is
    the toolkit's addition, marked as such.
- **`live-evaluations.md`, the managed scorer's contract, new bullet.**
  `multi_turn_trajectory_quality` marked legitimate calls as "tools not
  permitted" when the agent's tool declarations did not reach the rater.
  Before a trajectory score counts:
  - confirm the declarations are in the dataset;
  - read one failing verdict's reasoning.

  A "not permitted" call to a declared tool is a configuration fault, and
  the run is incomplete. The article's claim is marked as reported by the
  source, not verified here. The field that carries the declarations is
  left to Google's installed skills, because this run could not check it.
- **`SKILL.md`.** One sentence added to the rubric routing bullet, with
  links to both changes. The description is unchanged.

**adk-agent-instructions.**

- **`prompt-as-code.md`, "Optimisers".** A paragraph after the outcome
  measure rule says the following, and points to quality iteration's
  step 4:
  - whatever proposes a candidate (an optimiser, a coding agent or a
    person) never grades it;
  - the eval config, cases, judge and thresholds are fixed before the loop;
  - a coding agent reports the evaluator's verdicts rather than its own
    reading.

**Scenario case.** `evaluation-fixed-categorical-metric-and-independent-grader`
in `evals/scenarios.json`, runnable from its context and listed in
`evals/scenario-fixtures.json`. It covers:

- a blended score rising on fresh synthesized scenarios;
- a "not permitted" verdict on a declared tool;
- a request from the session that wrote the fix to adjust the eval so the
  fix passes.

## Linked only

None.

## Not imported, with reasons

- **The five-stage loop (prepare, infer, grade, analyse, optimise).**
  Already covered. Quality iteration's loop runs a baseline, error
  analysis and one change per iteration. Live evaluations covers
  assembling assets and managed simulation.
- **Reading verdicts directly below about ten failures and clustering
  above.** Already covered: `live-evaluations.md` routes more than ten
  failures on one metric to `generate_loss_clusters`.
- **"Trust the deltas between runs more than any single number".**
  Already covered: it is quoted from Google's flywheel sample in
  `live-evaluations.md`. Entry 2's paired interval says when a delta is
  real.
- **The User Simulator as a cold-start bootstrap, with production traces
  as the better input.** Already covered:
  - `evaluation-design.md` treats generated scenarios as a reviewed
    cold-start source, with hand-written turns as the regression form;
  - adk-agent-observability covers traces into evaluation cases and
    Online Monitors.
- **Grading production traces in place, skipping inference, and Online
  Monitors writing to Cloud Monitoring.** Already covered by
  adk-agent-observability (`trace-to-evaluation.md`, Online Monitors in
  `SKILL.md` and `operations-handover.md`).
- **The bug-assistant tool footer (0% to 96%).** Already covered by the
  same sample: an instruction that asks for something the model treats as
  optional, made countable with a deterministic check. The new
  categorical-metric paragraph names "a required footer" as a case for a
  code check.
- **"It proposes; you approve."** Generic human-in-the-loop advice. The
  skills already require approval before paid live work.
- **The install commands for `google-agents-cli-eval` and
  `agent-platform-eval-flywheel`.** Already referenced wherever this skill
  hands commands to Google's skills; adk-engineer explains how to get them.
- **Partitioning synthesized scenarios across five revision types, five
  each.** Too narrow to need its own rule. The categorical-metric
  paragraph's not-applicable class and per-class rate serve the same need.
- **The direction of letting the skill watch monitors and propose fixes on
  its own.** A product roadmap, not a mechanism.

## Conflicts

- **Omitting `judge_model` (Google's flywheel sample) against pinning it
  (this toolkit).** The article does not raise it. The toolkit keeps its
  rule in `live-evaluations.md`: pass the full resource name, because an
  unnamed default judge is a release artefact nobody pinned. The new
  categorical judge is pinned in the same way ("the judge, its version and
  the cases stay the same").
- **Uncalibrated custom rubric.** The article gates on its custom rubric
  without reporting calibration against human labels. The toolkit keeps
  expert review's rule that a judge used as a gate is calibrated first, and
  says so in the new paragraph.
- **Entry 3's `not evaluated` stage verdict versus the new not-applicable
  class.** These are different things. `not evaluated` means no reference
  has decided the stage yet, and it is never a pass. A not-applicable
  verdict means the behaviour did not arise in the case, and the case
  leaves the denominator. Entry 3's note had anticipated this entry.

## Limits

- **Tables not read.** The before-and-after tables came through as image
  names only. The figures used (0.80, 0.67, 21%, 5%, four IGNORED cases,
  14 of 15, 0% to 96%) are from the prose.
- **Nothing run.** No managed evaluation, Agents CLI or model call was made.
  Both rater behaviours (blended adaptive criteria, and trajectory
  false-flags without the tool declarations) are marked as reported by the
  source.
- **Trial.** One scenario ran twice, with user approval. The first run
  passed 4 of 5. It missed the trajectory rule because nothing it read
  linked to it. After links were added and the rule was made explicit, the
  second run passed 5 of 5. See the
  [testing record](../testing/melnyk-dai-agent-quality-flywheel-alignment-2026-11-08.md).
