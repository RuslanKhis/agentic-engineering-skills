# Refresh evaluation sets from production

Read this when the eval set has not changed for months, production failures do not appear in CI, or the holdout has been spent on fixes. adk-agent-evaluation owns case construction and review; adk-agent-observability owns sampling, trace capture and the data-handling policy around them. This reference decides what is sampled, how cases expire, and how the holdout is replenished.

## Why eval sets age

An eval set is a simulator of production at the moment it was written. Drift modes that make it a worse simulator (practitioner analysis, tianpan.co, 2026-04-27, and Eugene Yan's evaluation process notes, 2025-04; practitioner evidence, not reproduced here):

| Drift mode | Symptom in CI | What expires |
| --- | --- | --- |
| Dataset drift | Cases still pass while users report new failure types | Cases whose inputs no longer resemble traffic |
| Tool-API drift | Trajectory cases fail after a tool or API version change | Expected tool calls and recorded tool responses |
| Prompt drift | Reference responses encode the old prompt's phrasing | `response_match_score` references |
| Retrieval-corpus drift | Grounded answers change because the corpus changed | Reference answers and rubrics that cite corpus content |
| User-distribution drift | The set over-represents launch-time users | The case mix, not individual cases |
| Step compounding | Multi-turn cases diverge at turn three because turn two changed | Later turns of scripted conversations |

Dataset drift has a measurable form when sessions land in BigQuery: Google's Agent Analytics SDK compares a golden-question table with production questions by case-insensitive, deduplicated keyword overlap (`Client.drift_detection(golden_dataset=<one table name>, filters=...)`, reporting coverage, uncovered golden questions and questions new in production, with raw and unique counts in `details`) and clusters production questions semantically (`deep_analysis` with `auto_group_using_semantics`); its `EvalSuite` keeps capability and regression categories, graduates a task to regression after it passed all of the last N runs (`auto_graduate(threshold_runs=)`), flags saturation at a 100 percent pass rate over recent runs and a positive-to-negative imbalance in `check_health`, and `EvalValidator` runs static checks for ambiguous tasks, class imbalance and suspicious thresholds (BigQuery-Agent-Analytics-SDK v0.6.1, `SDK.md` sections 7 to 9, read 2026-10-22; vendor library, not executed). Use the coverage number as the trigger for the dataset-drift row, and the saturation flag as the trigger to retire or harden a case; the retirement decision and the holdout rule stay as written here. The constructor, filter and result names are in adk-agent-observability's BigQuery reference; `EvalSuite` takes the pass history you give it, so the project persists its own run records.

Give every case a `freshness_expires` date and a `drift_mode` in its ownership metadata (the schema adk-agent-evaluation's evaluation-design reference uses beside the ADK asset). Expired cases still run; they are listed in the release record as expired evidence, and the release owner decides whether to refresh or retire each.

## Sample production into candidates

Hamel Husain's evals FAQ (2025, practitioner) gives the loop: production uses sampled, asynchronous, reference-free judges; new production failures become CI cases; evaluators are written for errors discovered, not imagined. Apply it as:

1. **Sampling** (adk-agent-observability): a fixed fraction of invocations plus every invocation flagged by a user, a safety filter, a tool error or a budget stop. Capture allowlisted metadata by default and content only under the project's retention and access policy; `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` stays the default.
2. **Triage**: an asynchronous reference-free judge (rubric or hallucination metric with the pinned judge) scores the sample; humans read the lowest-scoring and the flagged traces first.
3. **Conversion**: a failing trace becomes a case by replacing sensitive values while preserving the failing state and sequence, recording the incident ID, the drift mode it reveals and a reviewer. The old release must fail the case when it can still be run; otherwise record "not reproduced".
4. **Placement**: a case that guided a fix joins the development set; a reviewed case that no change has looked at joins the holdout. A case that passes on the current release and covers a new traffic pattern joins the CI set as a regression guard.

Review synthetic or sampled cases for impossible setup, invented expected answers and duplicates before they count (adk-agent-evaluation's curation steps).

On Agent Runtime, Agent Platform Evaluations (GA 2026-07-31; documentation reviewed by the research pass on 2026-10-07, vendor, not exercised here) runs offline evaluation over stored traces and sessions filtered by agent version or time period with results written to GCS, and online monitors that sample a percentage of traffic on a schedule of roughly ten minutes with a maximum sample count per run; scores are exported as the Cloud Monitoring metric `aiplatform.googleapis.com/online_evaluator/scores` labelled by metric name, which an alert policy can threshold. There is no "add this trace to a dataset" call; the export path is the GCS artefacts, which the conversion step above reads. Filtering by agent version is why the revision ID belongs in the release manifest and the startup log.

## A scheduled evaluator beside the agent

Google's Ambient Quality Agent (AQuA, `core/python/ambient-quality-agent` in google/adk-recipes, tag `ambient-quality-agent/v0.1.0`; README read 2026-10-22 at commit be63596; vendor sample, "not production use" per the repository README) is an ADK agent that runs beside the one it observes. It reads conversations from the BigQuery Agent Analytics plugin table, a Cloud Telemetry linked `_AllSpans` dataset or agents-cli default logging; runs investigations on a schedule, after each deployment of the observed agent or on demand (`agents-cli aqua schedule-investigation --wait`); reviews each conversation with an LLM against the agent's configuration and an evaluation goal, runs deterministic Python checks you publish (`agents-cli aqua metrics publish`) or Gemini-platform evaluation metrics; deduplicates failures into insights with status `NEW`, `RECURRING` or `RESOLVED` and occurrence history (`agents-cli aqua list-insights --status NEW`); and diagnoses an insight against a published snapshot of the agent's source. It installs as an agents-cli extension (`agents-cli extension add google/adk-recipes#core/python/ambient-quality-agent --ref ambient-quality-agent/v0.1.0`, then `--apply-aqua` on `infra single-project` and `--deploy-aqua` on `deploy`, or `agents-cli aqua attach` for an existing agent), needs agents-cli 1.6 or later, Terraform and a project in an organisation (its Cloud Run dashboard sits behind IAP), and ships an `agents-cli-aqua` skill for the commands.

Do not rebuild it. This reference owns two decisions about it:

- **Whether insights gate.** The release record says which AQuA insight statuses on which slice block a promotion (for example a `NEW` insight on the critical slice after the canary step) and which only open a case in the sampling loop above. Absent that sentence, an insight is a candidate case, not a gate.
- **Missing evidence is incomplete, never a pass.** An investigation that did not run for the release window, failed, or read a telemetry source the release does not write counts as NOT RUN in the release record, the same rule the CI gate applies to an empty CSV.

The insights it finds flow into the sampling loop above: a failing conversation trace becomes a case through adk-agent-observability's converter, and `RESOLVED` is checked against the case that fixed it, not against AQuA's status alone. The query subcommands print JSON; this reference did not read the field names, so the release record keeps its own insight row (a fingerprint such as `check:contract`, status, first and last seen, occurrence count, the failing session ids, the check that found it) and maps the installed version's output onto it once the extension runs. Its Resources created line names what the extension deploys (the AQuA engine on Agent Runtime, the Cloud Run dashboard behind IAP, its own dataset), with the idle cost of each taken from the pricing rows adk-system-designer's resource ledger already carries for Agent Runtime, Cloud Run and BigQuery, the cleanup being the same `infra` command with `--destroy --apply`; a price that cannot be read in the session stays a placeholder. For the commands, consult the installed `agents-cli-aqua` skill; if it is not installed, adk-engineer explains how to get it. This skill decides the gate and the evidence rule; Google's skill operates the extension.

## Replenish the holdout

The holdout is spent when a failure guides a fix. Each release records how many holdout cases moved to development; when the holdout falls below the agreed size, replenish it from reviewed production samples that no engineer has used for a fix. A holdout that has been reused for three releases without replenishment is a development set with a misleading name; say so in the release record.

## Retire and archive

Retire a case when its drift mode makes it meaningless (a tool that no longer exists, a policy that changed) and the replacement exists. Keep the retired case in git history with the retirement reason; a retired incident regression is a candidate for a conformance recording instead, so the behaviour stays observable without a live model.

## Completion

Every case carries a freshness date and drift mode; expired cases are listed in the release record; the sampling and triage path is documented with its data-handling policy; the holdout size and replenishment history are recorded; new production failures from the last release period appear as cases or as explicit "not reproduced" entries.
