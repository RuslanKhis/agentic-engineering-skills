# Migrate a model version

Read this when a deprecation notice arrives, an alias moved, a cheaper or stronger model is proposed, or the judge model must change. The comparison itself runs through adk-agent-evaluation (two-stage escalation on the plainest contract); model settings such as `thinking_level` and temperature belong to adk-model-and-output-contracts. This reference turns the result into a release.

## Check the calendar first

Dates below are a snapshot; verify them on the cited pages at use time.

| Fact | Source (page date) | Evidence |
| --- | --- | --- |
| Gemini 2.0 Flash and Flash-Lite shut down 2026-06-01 | https://ai.google.dev/gemini-api/docs/deprecations (2026-10-07, re-read 2026-10-08) | vendor |
| Gemini 2.5 models limited to users who have actively used them; "for any new projects, use 3.5 Flash-Lite or 3.8 Flash" | same | vendor |
| `gemini-3.1-flash-lite` earliest shutdown 2027-05-07, replacement `gemini-3.5-flash-lite` | same | vendor |
| Shutdown dates are the earliest possible dates | same | vendor |
| Vertex AI: models available at least 12 months after release; short-term models give at least 45 days to migrate; dates may be extended and are never moved earlier | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions (2026-10-07, re-read 2026-10-08) | vendor |
| `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` retired on Vertex on 2026-10-20 (a date now past); replacements listed as `gemini-3.8-flash` or `gemini-3.5-flash` for Pro and `gemini-3.8-flash` or `gemini-3.5-flash-lite` for Flash | same, page updated 2026-10-21, re-read 2026-10-22 | vendor |
| `gemini-3.5-flash` released 2026-05-19 (the ADK 2.8.0 default) | same | vendor |
| Short-term models: `gemini-3.6-flash` retires 2026-11-19 and `gemini-3.7-flash` 2027-01-28, replacement `gemini-3.8-flash`; `gemini-3.8-flash` has no retirement date announced | same | vendor |
| Vertex AI SDK releases after June 2026 do not support Gemini; use `google-genai` 2.0.0 or later (ADK 2.8.0 requires `google-genai>=2.19,<3`) | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate (fetched 2026-10-07) | vendor |

The two calendars differ: the Gemini API page lists 2.5 models as limited to prior users with no shutdown date, while the Vertex page gives 2026-10-20, now past. State both in the project's calendar, and for each pinned model and judge record the retirement date (or "none announced"), the replacement candidate, and the release in which the migration lands. A judge or user simulator on `gemini-2.5-flash` (the 2.8.0 default when `judge_model` is unset) is a migration due before 2026-10-20 on Vertex and a limited-access model on the Gemini API today; ADK 2.2.0 (2026-06-04) moved the agent default to `gemini-3-flash-preview` and later releases to `gemini-3.5-flash`, but the judge default did not move (CHANGELOG and main `eval_metrics.py`). A short-term model such as `gemini-3.6-flash` gives 45 days from the announcement, so a project on one needs the migration rehearsed before the notice arrives. The same calendar entry is due for Agents CLI projects: `agents-cli eval dataset synthesize` runs its simulated user on ADK's `LlmBackedUserSimulator` default, which Google's eval skill names as `gemini-2.5-flash`, with no flag to change it (Agents CLI 1.11.0, `google-agents-cli-eval` skill `references/user-simulation.md`, read 22 October 2026); the model-versions page re-read on 22 October 2026 (updated 2026-10-21) keeps the 2026-10-20 retirement, so on Vertex that is a blocker to confirm against the installed ADK's actual default before a paid synthesis, and the simulator model is a pinned dependency with its own calendar row.

## Follow Google's migration playbook

Google's model migration guide (https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate, fetched 2026-10-07, vendor) sets three regression types and four rules; the GoogleCloudPlatform/generative-ai repository carries a worked notebook for the side-by-side (`gemini/evaluation/model_migration_with_gen_ai_eval.ipynb`, commit 3a716a8, listed 2026-10-22, not read here). Apply them as the release plan:

1. **Code regression tests** (always required): the deterministic tier from [CI eval gates](ci-eval-gates.md), run against the candidate model ID, because a model change can alter tool-call formatting and finish reasons.
2. **Model-performance regression tests**: offline on the golden set (the frozen development set, same cases, same exemplars, same retrieval, same judge), then online on a traffic sample ([staged rollout](staged-rollout.md)). Repeat every evaluation done since launch, not only the latest suite.
3. **Load tests**: required when latency or throughput is a requirement; token counts and response lengths change between model generations, so a passing quality run can still miss a latency budget.
4. Evaluate RAG, tool and chain components independently where the application is composed; a component-level regression is invisible in an end-to-end score.
5. Expect token-count reporting to change between generations; compare cost per case, not tokens per case, and re-measure `max_output_tokens` headroom.
6. For tuned models, re-tune rather than reuse hyperparameters. Re-tuning assumes the candidate is tunable: the Gemini API offers no tunable model (https://ai.google.dev/gemini-api/docs/model-tuning, page dated 2026-04-28), and Vertex supervised tuning listed Gemini 3.5 Flash, 3.5 Flash-Lite and 3.1 Flash-Lite (Preview since 2026-06-22, `us-central1` and `europe-west4`) plus the 2.5 family on 2026-10-20 (https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/tuning/supervised-tuning/use); `gemini-3.8-flash` was not listed. A migration off a tuned 2.5 model therefore needs a tuning target decision before the side-by-side. For the tuning job itself, dataset preparation and cost, consult the installed Google skill `agent-platform-tuning`, and for job status or cancellation `agent-platform-tuning-management` (both from google/skills); if they are not installed, adk-engineer explains how to get them.
7. New versions "may require prompt adjustments"; the guide says these are hard to predict without testing, so the prompt change, if any, is its own changelog row after the side-by-side, never folded into the model swap.

## Run the side-by-side

- Freeze: development set hash, prompt hash, exemplars, retrieval snapshot, tool schema hash, judge ID and `num_samples`. Record them in the changelog row before the first run.
- Stage 1 (adk-agent-evaluation): old and new model on the plainest contract, same settings except the ones the new generation requires (`thinking_level` on Gemini 3, temperature left at 1.0). Report per category, successes and attempts separately.
- Stage 2: the winner through the full workflow. A gain lost here is a workflow defect, not a model result.
- Deltas to record per case and in aggregate: category counts, schema validity and wrong-valid-schema (adk-model-and-output-contracts' four metrics), `tool_trajectory_avg_score`, response length, prompt and output tokens, thought tokens, p50 and p95 latency, cost. On 2.10.0 and later the efficiency metrics (`token_usage_v1`, `invocation_duration_v1`, `inference_call_count_v1`, `tool_call_count_v1`; verified in main `eval_metrics.py` and the adk-docs criteria page) report these without a pass/fail; on 2.8.0 read them from the eval result JSON and the recorded `usage_metadata`.
- Report the aggregate quality delta as a paired difference per case with its interval and minimum detectable difference (adk-agent-evaluation's quality-iteration reference, "Tell a change from noise"). A migration forced by a retirement or chosen for cost asks "not worse by more than the agreed margin": the interval's lower end must sit above minus the margin. A delta inside the interval is no measured difference, not a small gain or loss.
- Holdout once, with the frozen winner. Record score and date. The holdout result is release evidence; it does not guide a fix.

## Migrate the judge separately

The judge is a pinned dependency with its own migration. Changing judge and agent model in one release makes a metric movement unattributable. Sequence:

1. Run the old and new judge on the same frozen candidate outputs (the agent does not run again). Record the per-case agreement rate and the cases that flipped.
2. Human-review the flipped cases (adk-agent-evaluation's judge calibration). Decide whether the new judge is stricter, looser or noisier, and adjust thresholds with the evidence written down.
3. Adopt the new judge as its own changelog row. Nightly comparisons restart their baseline from that row.

In an Agents CLI project the judge lives in three places, and only one is pinned by the project (Agents CLI 1.11.0, `google-agents-cli-eval` skill `references/metrics-guide.md` and the scaffolded `tests/eval/response_quality.py`, read 22 October 2026): the managed built-in metrics use a server-side autorater that `agents-cli` exposes no pin for; a custom `LLMMetric` pins `judge_model` and `judge_model_sampling_count` in `tests/eval/eval_config.yaml`; and the scaffolded default metric `custom_response_quality` calls the agent's own model (`{{cookiecutter.default_model}}`, with `temperature=0`), so a model swap in `.env` or the scaffold silently swaps the judge too. Before the side-by-side, move the scaffold judge to an explicit model string in that file, record it in the changelog row, and keep temperature at this toolkit's setting from adk-model-and-output-contracts rather than the scaffold's 0. Consult the installed `google-agents-cli-eval` skill for the config schema; if it is not installed, adk-engineer explains how to get it. This skill decides the judge pin and its migration order; Google's skill operates the metric configuration.

## Go/no-go record

Fill [assets/model-upgrade-checklist.md](../assets/model-upgrade-checklist.md). The record carries both model IDs, the judge ID, the frozen hashes, the category delta table, the holdout result, cost and latency deltas, load-test outcome (or "not required because ..."), the rollout plan and the rollback target. A no-go is a complete record too; it saves the next person from repeating the comparison.

## Completion

Calendar entries exist for every pinned model and judge; the comparison ran with the judge pinned and the development set frozen; the holdout ran once; the checklist is filled with evidence tiers (local, mocked, live, not run); the changelog has a row; the rollout follows [staged rollout](staged-rollout.md).
