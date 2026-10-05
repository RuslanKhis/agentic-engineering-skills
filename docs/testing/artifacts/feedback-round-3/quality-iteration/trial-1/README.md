# R2 trial 1: "improve the decisions" on five labelled cases

*6 October 2026 · One fresh general-purpose agent session, Claude Code harness.*

**Maintainer test (feedback round 3, R2).** Give a coding agent a working draft
stage with five labelled cases and the instruction "improve the decisions".
Under the revised skill it must run and categorise errors before editing code,
and its first change must target the largest error category, not add a checker.

**Setup.** `workspace/` is a copy of `../seed/` with the reviewer-only
baseline section removed from its README. `request.txt` is the exact request.
The agent was pointed at the repository's `skills/adk-agent-evaluation/SKILL.md`
by path (the installed copy under the user's home directory predates this
round), so this is an explicit file-path invocation, not catalogue activation.
No expected answers, categories or fixes were supplied. The model is a
rule-based double; no provider was called.

**Outputs, unedited.** `workspace/NOTES.md` (dated log), `workspace/analysis/`
(eight error tables as JSON), `workspace/runs/` (outputs and prompt of every
measured run), the changed `draft_stage.py` and `prompt.txt`.

## Assessment against the test

| Criterion | Observed | Result |
| --- | --- | --- |
| Runs and categorises errors before editing code | NOTES.md step 0 reproduces the baseline; step 1 hand-labels every output against its label into `analysis/iteration-0-baseline.json` (missed_policy 2, wrong_outcome 1, weak_condition 2, wrong_attribution 1, contract_failure 1) before any edit | Pass |
| First change targets the largest category, not a checker | Step 2 repairs the contract failure first (the reference excludes it from the quality denominator); step 3, the first decision-quality change, adds deterministic policy lookup to retrieval because missed_policy was the largest category; the log states "not the prompt and not a checker" | Pass |
| One change per iteration, re-measured | Seven measured runs; iteration 2 grew contract_failure and was recorded and reverted; every other change kept with before/after counts | Pass (beyond the test) |
| Prompt restructured around the judgment | Step 5 restarts from the skeleton: 1,590 words to 211, requests 10 KB to 2.5 KB, identical outputs; exemplars added later with leave-one-out | Pass (beyond the test) |
| Honest reporting | Final 5/5 decisions, recall 1.00, no schema failure, stated as a development score with no holdout; two residual rows named as the largest remaining category and attributed to the double's limits | Pass |

## Limitations

- The model is a rule-based double whose triggers reward exactly the changes
  the reference teaches; the trial shows the agent followed the process, not
  that the process improves a real model.
- One trial, one model, one harness, explicit file-path invocation.
- The agent used `python3.11` because the bare `python3` on the machine is
  3.9; it reported identical outputs under both.
