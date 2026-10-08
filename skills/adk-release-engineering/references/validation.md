# Validate the release contract

Use the target's existing test runner and interpreter. Keep doubles at the model boundary so the real `LlmAgent`, flow processors and `AgentEvaluator` run. Label every result **local** (no network, no model), **mocked** (scripted model or replay), **live** (real model or platform) or **not run**.

## Manifest and changelog (local)

- Run `scripts/inventory_release_refs.py --project . --dry-run` and confirm exit 0 (a partial scan is exit 1 and must be explained). Every `manifest.components` entry has a `version`, `sha256` or `digest`, or an `unknown` with an owner recorded in the changelog row.
- `model=` resolves a string constant bound in the same module or a module-level constant reached by import or module attribute (`from .config import AGENT_MODEL`, `config.AGENT_MODEL`) to `model_reference_resolved` plus `model_pinned`/`model_alias`; a reference it cannot resolve is `model_reference_unresolved`, and only subscripts, function calls and other expressions are `model_dynamic`. Zero-byte JSON files are listed in `skipped` as `skipped_empty`, not as `malformed_file`; write the report outside the scanned tree anyway (the CI template uses `$RUNNER_TEMP`).
- Assert in a unit test that the production configuration contains no alias model ID (`-latest`, `-preview`, `-exp`) and that every `LlmAgent` sets `model=` explicitly, so the ADK default cannot change the release silently.
- Assert that every judge-metric criterion in `test_config.json` or `EvalConfig` literals carries `judge_model_options.judge_model` and `num_samples`. Parse the JSON with the pinned ADK `EvalConfig` model in a test (`EvalConfig.model_validate`) to catch schema drift at upgrade time.
- Diff the changelog: the newest row has date, prompt hash, model ID, judge ID, eval-set hash, category delta, holdout field (score or "not run") and rollback target.

## Tool schema hash (mocked)

Capture `llm_request.config.tools` in a `before_model_callback` with a scripted model, serialise with sorted keys, hash, and compare with the manifest value. The test fails when a dependency upgrade changes the generated declarations without a manifest update.

## Gate behaviour (local and mocked)

- Feed `check_eval_results.py` a CSV with one row fewer than `cases x runs_per_case x criteria` and assert exit 1; feed an empty file and assert exit 2; both are NOT RUN in the workflow and must block.
- Run the workflow job locally (`act`, or a shell replica of the steps) with the CSV step removed and confirm the checker step fails rather than skips.
- With a scripted model that returns a wrong tool call on one repeat of three, run `AgentEvaluator.evaluate(num_runs=3, output_file=...)` and confirm the CSV has three rows for that case and metric with one `FAILED`, the evaluator raises `AssertionError`, and the checker exits 1. This proves the repeat policy end to end without a live model.

## Migration evidence (live, approved)

- The side-by-side ran on the frozen development set with the judge pinned; the report shows category counts before and after, token and latency deltas, and the judge agreement rate when the judge changed.
- The holdout ran once with the frozen winner; its score and date are in the changelog.
- Load test ran or the record states why it was not required.

## Rollout and rollback (live, approved, non-production first)

- Cloud Run: the candidate revision served at 0% under a tag; the tier-2 eval ran against the tagged URL; traffic stepped as recorded; `update-traffic --to-revisions PREVIOUS=100` rehearsed and the previous revision confirmed by digest in the service description.
- Agent Runtime (Pre-GA): a manual traffic split exists before the first update; the candidate revision answered a direct revision query; the rollback split rehearsed in a non-production project.
- After rollback, confirm the prompt hash in the startup log, the model ID in one recorded `LlmResponse.model_version`, the tool schema hash and the secret version numbers all match the previous changelog row.

## Production feedback (local)

- Every case file carries `freshness_expires` and `drift_mode` metadata; a test lists expired cases and the release record names them.
- The holdout size and replenishment history are in the record; cases moved from holdout to development in this release are counted.

## Report

List files changed, commands with exit codes, which tier produced each piece of evidence, actual `google-adk` version, what used real providers, what used doubles, what remains unverified and any approval that is pending. Distinguish designing a gate from running it, and running it from passing it.
