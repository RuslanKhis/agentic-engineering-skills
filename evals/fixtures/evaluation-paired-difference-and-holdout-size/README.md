# Claims triage agent: prompt comparison

A Python ADK 2.12 agent that reads a motor claim's intake documents and
decides `fast_track`, `standard` or `refer_to_investigator`. The prompt lives
in `triage/prompts/` under a version number; v3 is in production and v4 is
the candidate.

## Files

- `runs/baseline-prompt-v3.csv`, `runs/candidate-prompt-v4.csv`: the trial
  records of both prompt versions on the 20 labelled development cases
  (`dev-001` to `dev-020`), three runs each, written by the evaluation runner.
  One row per trial: `trial_id`, `run_id`, `case_id`, `scenario`,
  `prompt_version`, `started_at`, `outcome` (`pass`, `fail` or
  `infra_error`), `reward` and `scorer_version`. A trial passes when the
  decision matches the reviewed label and every required reason is present.
  `scenario` is the claim type a case was written from; cases with the same
  scenario are variants of one claim type with different documents.
- `runs/dashboard-2026-10-23.md`: the summary the team posted after the runs.
- `docs/discovery-brief.md`: the outcome measure and what the sponsor would
  act on.
- `cases/holdout/`: the current holdout, twelve unlabelled cases.

No model or cloud access is available in this workspace.
