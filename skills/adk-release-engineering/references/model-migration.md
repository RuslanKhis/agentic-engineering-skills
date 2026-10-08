# Migrate a model version

Read this when a deprecation notice arrives, an alias moved, a cheaper or stronger model is proposed, or the judge model must change. The comparison itself runs through adk-agent-evaluation (two-stage escalation on the plainest contract); model settings such as `thinking_level` and temperature belong to adk-model-and-output-contracts. This reference turns the result into a release.

## Check the calendar first

Dates below are a snapshot; verify them on the cited pages at use time.

| Fact | Source (page date) | Evidence |
| --- | --- | --- |
| Gemini 2.0 Flash and Flash-Lite shut down 2026-06-01 | https://ai.google.dev/gemini-api/docs/deprecations (2026-10-01) | vendor |
| Gemini 2.5 models limited to users who have actively used them; "for any new projects, use 3.5 Flash-Lite or 3.8 Flash" | same | vendor |
| `gemini-3.1-flash-lite` earliest shutdown 2027-05-07, replacement `gemini-3.5-flash-lite` | same | vendor |
| Shutdown dates are the earliest possible dates | same | vendor |
| Vertex AI: models available at least 12 months after release; short-term models give at least 45 days to migrate; dates may be extended and are never moved earlier | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions (2026-10-05) | vendor |
| `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` retire on Vertex 2026-10-20; `gemini-3.8-flash` listed as a replacement | same | vendor |
| `gemini-3.5-flash` released 2026-05-19 (the ADK 2.8.0 default) | same | vendor |
| Short-term models: `gemini-3.6-flash` retires 2026-11-19 and `gemini-3.7-flash` 2027-01-28, replacement `gemini-3.8-flash`; `gemini-3.8-flash` has no retirement date announced | same | vendor |
| Vertex AI SDK releases after June 2026 do not support Gemini; use `google-genai` 2.0.0 or later (ADK 2.8.0 requires `google-genai>=2.19,<3`) | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate (fetched 2026-10-07) | vendor |

The two calendars differ: the Gemini API page lists 2.5 models as limited to prior users with no shutdown date, while the Vertex page gives 2026-10-20. State both in the project's calendar, and for each pinned model and judge record the retirement date (or "none announced"), the replacement candidate, and the release in which the migration lands. A judge or user simulator on `gemini-2.5-flash` (the 2.8.0 default when `judge_model` is unset) is a migration due before 2026-10-20 on Vertex and a limited-access model on the Gemini API today; ADK 2.2.0 (2026-06-04) moved the agent default to `gemini-3-flash-preview` and later releases to `gemini-3.5-flash`, but the judge default did not move (CHANGELOG and main `eval_metrics.py`). A short-term model such as `gemini-3.6-flash` gives 45 days from the announcement, so a project on one needs the migration rehearsed before the notice arrives.

## Follow Google's migration playbook

Google's model migration guide (https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate, fetched 2026-10-07, vendor) sets three regression types and four rules. Apply them as the release plan:

1. **Code regression tests** (always required): the deterministic tier from [CI eval gates](ci-eval-gates.md), run against the candidate model ID, because a model change can alter tool-call formatting and finish reasons.
2. **Model-performance regression tests**: offline on the golden set (the frozen development set, same cases, same exemplars, same retrieval, same judge), then online on a traffic sample ([staged rollout](staged-rollout.md)). Repeat every evaluation done since launch, not only the latest suite.
3. **Load tests**: required when latency or throughput is a requirement; token counts and response lengths change between model generations, so a passing quality run can still miss a latency budget.
4. Evaluate RAG, tool and chain components independently where the application is composed; a component-level regression is invisible in an end-to-end score.
5. Expect token-count reporting to change between generations; compare cost per case, not tokens per case, and re-measure `max_output_tokens` headroom.
6. For tuned models, re-tune rather than reuse hyperparameters.
7. New versions "may require prompt adjustments"; the guide says these are hard to predict without testing, so the prompt change, if any, is its own changelog row after the side-by-side, never folded into the model swap.

## Run the side-by-side

- Freeze: development set hash, prompt hash, exemplars, retrieval snapshot, tool schema hash, judge ID and `num_samples`. Record them in the changelog row before the first run.
- Stage 1 (adk-agent-evaluation): old and new model on the plainest contract, same settings except the ones the new generation requires (`thinking_level` on Gemini 3, temperature left at 1.0). Report per category, successes and attempts separately.
- Stage 2: the winner through the full workflow. A gain lost here is a workflow defect, not a model result.
- Deltas to record per case and in aggregate: category counts, schema validity and wrong-valid-schema (adk-model-and-output-contracts' four metrics), `tool_trajectory_avg_score`, response length, prompt and output tokens, thought tokens, p50 and p95 latency, cost. On 2.10.0 and later the efficiency metrics (`token_usage_v1`, `invocation_duration_v1`, `inference_call_count_v1`, `tool_call_count_v1`; verified in main `eval_metrics.py` and the adk-docs criteria page) report these without a pass/fail; on 2.8.0 read them from the eval result JSON and the recorded `usage_metadata`.
- Holdout once, with the frozen winner. Record score and date. The holdout result is release evidence; it does not guide a fix.

## Migrate the judge separately

The judge is a pinned dependency with its own migration. Changing judge and agent model in one release makes a metric movement unattributable. Sequence:

1. Run the old and new judge on the same frozen candidate outputs (the agent does not run again). Record the per-case agreement rate and the cases that flipped.
2. Human-review the flipped cases (adk-agent-evaluation's judge calibration). Decide whether the new judge is stricter, looser or noisier, and adjust thresholds with the evidence written down.
3. Adopt the new judge as its own changelog row. Nightly comparisons restart their baseline from that row.

## Go/no-go record

Fill [assets/model-upgrade-checklist.md](../assets/model-upgrade-checklist.md). The record carries both model IDs, the judge ID, the frozen hashes, the category delta table, the holdout result, cost and latency deltas, load-test outcome (or "not required because ..."), the rollout plan and the rollback target. A no-go is a complete record too; it saves the next person from repeating the comparison.

## Completion

Calendar entries exist for every pinned model and judge; the comparison ran with the judge pinned and the development set frozen; the holdout ran once; the checklist is filled with evidence tiers (local, mocked, live, not run); the changelog has a row; the rollout follows [staged rollout](staged-rollout.md).
