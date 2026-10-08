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

Give every case a `freshness_expires` date and a `drift_mode` in its ownership metadata (the schema adk-agent-evaluation's evaluation-design reference uses beside the ADK asset). Expired cases still run; they are listed in the release record as expired evidence, and the release owner decides whether to refresh or retire each.

## Sample production into candidates

Hamel Husain's evals FAQ (2025, practitioner) gives the loop: production uses sampled, asynchronous, reference-free judges; new production failures become CI cases; evaluators are written for errors discovered, not imagined. Apply it as:

1. **Sampling** (adk-agent-observability): a fixed fraction of invocations plus every invocation flagged by a user, a safety filter, a tool error or a budget stop. Capture allowlisted metadata by default and content only under the project's retention and access policy; `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` stays the default.
2. **Triage**: an asynchronous reference-free judge (rubric or hallucination metric with the pinned judge) scores the sample; humans read the lowest-scoring and the flagged traces first.
3. **Conversion**: a failing trace becomes a case by replacing sensitive values while preserving the failing state and sequence, recording the incident ID, the drift mode it reveals and a reviewer. The old release must fail the case when it can still be run; otherwise record "not reproduced".
4. **Placement**: a case that guided a fix joins the development set; a reviewed case that no change has looked at joins the holdout. A case that passes on the current release and covers a new traffic pattern joins the CI set as a regression guard.

Review synthetic or sampled cases for impossible setup, invented expected answers and duplicates before they count (adk-agent-evaluation's curation steps).

On Agent Runtime, Agent Platform Evaluations (GA 2026-07-31; documentation reviewed by the research pass on 2026-10-07, vendor, not exercised here) runs offline evaluation over stored traces and sessions filtered by agent version or time period with results written to GCS, and online monitors that sample a percentage of traffic on a schedule of roughly ten minutes with a maximum sample count per run; scores are exported as the Cloud Monitoring metric `aiplatform.googleapis.com/online_evaluator/scores` labelled by metric name, which an alert policy can threshold. There is no "add this trace to a dataset" call; the export path is the GCS artefacts, which the conversion step above reads. Filtering by agent version is why the revision ID belongs in the release manifest and the startup log.

## Replenish the holdout

The holdout is spent when a failure guides a fix. Each release records how many holdout cases moved to development; when the holdout falls below the agreed size, replenish it from reviewed production samples that no engineer has used for a fix. A holdout that has been reused for three releases without replenishment is a development set with a misleading name; say so in the release record.

## Retire and archive

Retire a case when its drift mode makes it meaningless (a tool that no longer exists, a policy that changed) and the replacement exists. Keep the retired case in git history with the retirement reason; a retired incident regression is a candidate for a conformance recording instead, so the behaviour stays observable without a live model.

## Completion

Every case carries a freshness date and drift mode; expired cases are listed in the release record; the sampling and triage path is documented with its data-handling policy; the holdout size and replenishment history are recorded; new production failures from the last release period appear as cases or as explicit "not reproduced" entries.
