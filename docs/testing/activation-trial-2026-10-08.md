# Activation trial with twenty skills · 8 October 2026

This records a description-based skill-selection trial over the whole
[activation corpus](../../evals/activation.json) after the seven
cross-framework specialists were added. It measures **selection from
descriptions**, which is the step a host performs before loading a skill. It
does not measure execution quality, and it was not run inside a real coding
agent session; read the method and its limits before quoting the counts.

## Method

- **Catalogue.** The twenty installed skills' `name` and `description`
  fields, extracted from the `SKILL.md` frontmatter at commit `f776114`
  ([catalogue.json](artifacts/activation-2026-10-08/catalogue.json),
  SHA-256 prefix `de33cfff3fc4a943`).
- **Corpus.** All 56 cases in `evals/activation.json` (SHA-256 prefix
  `7f49ab3a1a59be55`): one or two positives and one near-miss negative per
  skill, including the 21 cases written for the new specialists and the
  context-window case for the optimise skill.
- **Selectors.** Five fresh subagent sessions, each given only the catalogue
  and a shuffled batch of prompts, with no access to the repository, the
  labels or the rationale. Each returned a primary skill (or `none`), up to two
  supporting skills and a one-sentence reason. The main run used four batches
  of 14 cases on the session's default model. A repeat run on a different
  model (Sonnet) judged the 22 new-specialist and context-window cases again.
- **Grading.** For a positive case, PASS when the target skill is primary,
  PARTIAL when it is supporting only. For a near-miss negative, PASS when the
  target skill is neither primary nor supporting, PARTIAL when it is loaded as
  supporting behind another primary, FAIL when it is primary. Graded rows with
  reasons are in [graded.json](artifacts/activation-2026-10-08/graded.json).

## Results

| Run | Cases | PASS | PARTIAL | FAIL |
| --- | --- | --- | --- | --- |
| Main, all cases | 56 | 55 | 1 | 0 |
| Main, new-specialist cases only | 21 | 20 | 1 | 0 |
| Main, pre-existing cases only | 35 | 35 | 0 | 0 |
| Repeat on Sonnet, new-specialist batch | 22 | 21 | 1 | 0 |

Primary selections agreed between the two runs on all 22 repeated cases.

The single PARTIAL is the same case in both runs: `instructions-near-miss`
("answers are wrong on 30% of the labelled set; run the error analysis by
category, change one thing per iteration and report the holdout"). Both
selectors chose `adk-agent-evaluation` as primary, which the label expects,
and added `adk-agent-instructions` as a supporting skill. The description of
the instructions skill already excludes the measured loop, and the evaluation
skill's quality-iteration reference hands prompt changes back to it, so loading
it as a supporter is defensible rather than a misroute. No description change
was made for this; the case stays in the corpus as the one to watch.

## What this establishes and what it does not

It establishes that, from descriptions alone, two different models pick the
intended primary specialist for every positive case and avoid the intended
specialist for every near-miss, across twenty skills, with one soft
over-loading. The new specialists did not degrade selection for the thirteen
pre-existing skills in this trial.

It does not establish host behaviour: a real coding agent sees the catalogue
through its own loader, may apply its own ranking, and reads the project
before choosing. It does not establish execution quality, scope preservation
or improvement over any baseline. Samples are small, the prompts are the
corpus's own wording rather than held-out paraphrases, and the selectors were
asked to judge rather than to work. Follow the
[quality evaluation guide](skill-quality.md) for the host-session procedure
before publishing a stronger claim.
