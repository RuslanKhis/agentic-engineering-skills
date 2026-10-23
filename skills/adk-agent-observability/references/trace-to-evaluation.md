# From production traces to evaluation cases

Read when a bad trace, a low monitor score or negative feedback should become a regression case. This skill owns selection, redaction and export into the ADK `EvalSet` shape; adk-agent-evaluation owns what to measure, judge calibration, holdouts and the two-stage escalation. Field names below were read in google-adk 2.8.0 `evaluation/eval_set.py` and `evaluation/eval_case.py`.

## Where cases come from

| Source | Join key | Note |
| --- | --- | --- |
| Alert or dashboard outlier | `gen_ai.conversation.id` (session id) on spans, `gcp.vertex.agent.invocation_id` | Spans do not contain the stored events; fetch the session from the session service |
| Online Monitor low score | the graded trace id; the incident links to it (vendor) | Sampled; judge error applies |
| BigQuery row | `session_id`, `invocation_id`, `trace_id` | Cohorts and joins to feedback |
| Feedback record | `session_id`, `invocation_id` ([feedback capture](feedback-capture.md)) | Free text is PII until redacted |
| `adk web` | the web UI can save the current session into an eval set (adk-docs `evaluate/index.md`, fetched 2026-10-07) | Development path; it writes the same `EvalSet` model |
| AQuA insight (`agents-cli aqua list-insights`, `get-insight`) | the failing conversation traces the insight lists; it reads the BigQuery plugin table, the `_AllSpans` linked dataset or agents-cli logging | A deduplicated, recurring defect with its occurrence history (google/adk-recipes be63596, `core/python/ambient-quality-agent/README.md`, read 2026-10-22; vendor sample); adk-release-engineering decides whether it gates a release |

No Google tool converts Cloud Trace spans into `EvalSet` files, and spans are not the record anyway: the session's events are. `events_to_eval_set.py` fills that gap from a saved session export. Agent Platform evaluations can grade existing sessions directly (vendor); use that when the question is "how good was production" rather than "keep this from regressing".

## Sampling rule

Write the rule down before exporting: every tool-error invocation, every invocation with negative feedback, every monitor score below the threshold, plus a small uniform sample of ordinary invocations so the regression set does not consist only of failures. Record the rule, the window and the counts in the eval set description. Sampling limits volume, not sensitivity; redaction still applies to every case.

## The `EvalSet` shape (2.8.0)

```json
{
  "eval_set_id": "regressions_2026_10",
  "name": "...", "description": "...", "creation_timestamp": 0.0,
  "eval_cases": [{
    "eval_id": "regressions_2026_10_inv_abc",
    "conversation": [{
      "invocation_id": "...",
      "user_content": {"role": "user", "parts": [{"text": "..."}]},
      "final_response": {"role": "model", "parts": [{"text": "..."}]},
      "intermediate_data": {
        "tool_uses": [{"id": "c1", "name": "get_order", "args": {"id": 42}}],
        "tool_responses": [{"id": "c1", "name": "get_order", "response": {"status": "success"}}],
        "intermediate_responses": [["sub_agent_name", [{"text": "..."}]]]
      },
      "creation_timestamp": 0.0
    }],
    "session_input": {"app_name": "demo_app", "user_id": "eval_user", "state": {}},
    "creation_timestamp": 0.0
  }]
}
```

- `EvalBaseModel` uses a camelCase alias generator with `populate_by_name=True`, so snake_case keys (as above, and as in ADK's own shipped `*.evalset.json` samples) and camelCase keys both load. `extra="forbid"` applies to `Invocation`, `IntermediateData` and `SessionInput` fields other than `EvalCase` (which allows extras).
- Exactly one of `conversation` and `conversation_scenario` must be set per case (model validator).
- Ids must match `^[a-zA-Z0-9_]+$` when the local eval sets manager stores them; files are named `{eval_set_id}.evalset.json` under the app directory.
- `final_response` in a converted case is the observed output, not a reference answer. Review it before treating it as expected behaviour; for a failing trace the reference is usually what the agent should have said, which a human writes.

## Running the converter

```bash
python "$SKILL_DIR/scripts/events_to_eval_set.py" --session ./session.json --out ./agent_dir/regressions.evalset.json --select tool_error
python "$SKILL_DIR/scripts/events_to_eval_set.py" --session ./session.json --out ./all.evalset.json --select all --redact-hook myproject.redaction:scrub_case
python "$SKILL_DIR/scripts/events_to_eval_set.py" --session ./session.json --out ./check.json --dry-run --validate-with-sdk
```

- `--select all` writes one case holding the whole conversation, named `<eval_set_id>_<invocation_id>` (or `case_<n>` when that is not a valid id); rename the case in review. Keep the observed output of the release that failed beside the case, in the ownership metadata (for example `observed_final_response`), not in `final_response`, which holds the human-written reference; that pair is the offline form of "the old release fails the case". `--select tool_error` writes one case per invocation that contains a tool error (dict response with truthy `error`, `isError` or `is_error`, or an error status), each holding the conversation up to that invocation so context survives.
- Default redaction replaces text parts and tool-data strings longer than `--max-text-chars` (2000) or containing an email or URL, and every string under `error` / `error_message` keys, with `[REDACTED]`; binary, file and thought parts are dropped; session state is never copied; `session_input.user_id` is `eval_user` unless overridden. `--allow-content` disables the default scan; `--redact-hook MODULE:FUNC` runs your function over each case dict after it. Use the hook to apply the project's protect-adk-sensitive-data policy (for example its SDP de-identification helper) rather than widening the default.
- The report lists counts, the redaction tallies, structural problems and `sdk_validation`. Without `--validate-with-sdk` it says `not run`; with it, `validated with ...EvalSet.model_validate` or `not validated against SDK: google-adk not importable`. A structural pass is not proof that a particular ADK release loads the file; run `adk eval` on the target's interpreter as the live check.
- The output is reviewed data, not a test yet. Hand it to adk-agent-evaluation to choose metrics (tool trajectory, response match, rubric judges), to decide what is holdout, and to decide whether a case needs a human-written reference. The mapping from an ADK `Session` to an evaluation dataset (one turn per user event, the event author kept, `state_delta` carried) is recorded in adk-agent-evaluation's evaluation-design reference; the converter here follows it and does not redefine it.

Promptfoo's ADK guide asserts on the native spans directly (`execute_tool <tool>` names, `gen_ai.tool.name`, `gcp.vertex.agent.tool_call_args`) through its own OTLP receiver, which is one reason to keep those ADK-owned keys stable even where the GenAI conventions say otherwise; the assertion shapes are in adk-agent-evaluation's provider-compatibility reference (promptfoo commit 15bcb0d, read 2026-10-22).

The shape of an online evaluator that runs in the serving process is also documented outside ADK: evaluators attached to a function run in the background on every call or a sampled fraction, cheap checks on everything and model judges on a sample for cost, and emit one `gen_ai.evaluation.result` event per result pydantic/pydantic-ai commit eb0bd08, MIT, read 2026-10-23; another framework's documentation, restated, `docs/evals/online-evaluation.md`). On ADK the attachment point is an `after_model_callback` or a plugin that schedules the check off the request path, with the sample rate and the judge id recorded with the event.

## Judges on sampled observations (vendor)

Langfuse and Arize document LLM-as-a-judge over sampled traces with scores written back to the trace; Google's Online Monitors do the same with Cloud Monitoring as the sink. When the application emits its own scores, emit them as the conventions' `gen_ai.evaluation.result` event parented to the span that was evaluated (`gen_ai.evaluation.name` required; `gen_ai.evaluation.score.value` and `score.label` when applicable; `gen_ai.evaluation.explanation` and `gen_ai.response.id` recommended; `error.type` when the judge failed; all Development status; open-telemetry/semantic-conventions-genai commit 9ffc7e0, `docs/gen-ai/gen-ai-events.md`, read 2026-10-22), so a score joins the trace in any OTel backend and not only in BigQuery; the judge and its version stay in the event's attributes so a re-baseline can filter by them. Concretely, for a nightly job scoring yesterday's traces: spans are immutable once exported, so "parented to the span" means a log record with `event.name` `gen_ai.evaluation.result` whose trace context carries the evaluated span's `trace_id` and `span_id`; that requires the sessions store the job reads to keep `trace_id`, `span_id` and `invocation_id` per invocation, which is the usual missing column. The conventions define no attribute for the judge itself, so record the judge model id and rubric version under your own namespace (for example `<app>.judge.model`, `<app>.judge.rubric_version`) and keep that pair stable across re-baselines. Any of them can select candidates; none of them replaces the deterministic checks in adk-agent-evaluation's `execution-evidence.md`. When a judge flags a trace, export the session, redact, review, then decide whether the case documents a model error, a tool error or a judge error.

Independent community project; not affiliated with or endorsed by Google.
