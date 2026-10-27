I wrote the upgrade plan and a CI eval gate, but nothing has been run. This session had no shell, so the unit tests, the new tests and the workflow are all untested.

## What I did
- **Plan:** `docs/release/model-upgrade-2026-11.md` is a dated schedule to the 2026-11-17 deadline. It covers a baseline, a side-by-side of `gemini-3.8-flash` against `gemini-3.5-flash`, a holdout, a 0%-traffic tagged Cloud Run deploy, a stepped rollout and a rollback rule. It also holds the assumptions and the questions nobody could answer.
- **Model ID:** `app/triage.py` now reads the model from `Settings`, so `app/settings.py` and `deploy/cloudrun.sh` are the only two places to change. I did not switch the model.
- **Gate config:** `eval/test_config.json` grades tool trajectory only. `eval/ci-expectations.json` lists all 40 cases at 3 runs each.
- **Tier 1, every PR:** `tests/test_release_gate.py` checks that the expectations match the eval set and that no model ID is hardcoded outside `settings.py`. A dry run of the results checker is added to `ci.yml`.
- **Tier 2, live:** it runs on the `run-live-eval` label, on merge to main, or by hand. `evals_live/test_ci_gate.py` runs the eval set and writes a results file. A strict per-run check then fails on a missing file, a dropped case or any single failed run. The case ceiling fails the run instead of skipping.
- **Flakiness controls:** no judge model, a deterministic criterion, 3 repeats and a strict per-run rule.
- I updated `eval/README.md` to match.

## Findings that limit the gate
- The 40 cases are 10 scenarios repeated 4 times.
- Every reference reply is a placeholder, so I left reply-wording scoring out.
- Every expected tool call has empty arguments. I couldn't verify how 2.8.0 matches those, so expect the first live run to fail on cases that expect a call. That means fixing the case data, not a model regression.
- Only 4 cases expect a refund, and none checks the refund amount or outcome. That is the risk you named, so refund end-state cases come before this gate is trusted for refunds.
- The judge model is unset, so it would default to `gemini-2.5-flash`. I left the judge-based nightly tier out for that reason.

## Assumptions
- The forwarded notice gives 2026-11-17. The repo's own model-lifecycle data says `gemini-2.5-pro` already retired on Vertex on 2026-10-20. I assumed 11-17 but listed "check production health today" as step 0.
- Vertex AI is the provider, and Sam approves go/no-go.
- Thresholds are provisional, so the live job should stay a non-required check until a baseline is recorded.

## Left undone
- No model change, no eval runs and no deploy.
- The GitHub `eval` environment (Workload Identity Federation, project, location) doesn't exist and needs an owner.
- Case-data fixes, refund end-state cases and a holdout set are not written.
- The live test file's use of `AgentEvaluator` and the `ci.yml` workflow are unverified against ADK 2.8.0 and GitHub.
- No dollar cost estimate; I only gave run counts.