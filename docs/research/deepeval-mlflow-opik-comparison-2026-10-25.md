# deepeval, MLflow and Opik compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [confident-ai/deepeval](https://github.com/confident-ai/deepeval)
at commit `5410e38` (2026-10-23; PyPI 4.3.1), [mlflow/mlflow](https://github.com/mlflow/mlflow)
at commit `77f1aff` (2026-10-25) and [comet-ml/opik](https://github.com/comet-ml/opik)
at commit `763a2ec` (2026-10-23), cloned on 25 October 2026 into their own
directories and read. Only the published deepeval package was spiked, with
google-adk 2.12.0, offline and with no key; MLflow and Opik were read, not
run.

**Licence.** All Apache-2.0, no NOTICE files, no carved-out directories.

**Maintenance.** All three active.

**Conclusion.** All four memo claims hold with corrections. deepeval's ADK
hook is a SaaS exporter that refuses to run without a key; its metrics can
run offline with an explicit model. MLflow can store traces in-house but
its ADK scorers record errors as rows without a value, record ADK's "not
evaluated" as a fail, and read empty tool arguments when content capture
is off. Opik can be self-hosted once its cloud default, error reporting and
analytics are switched off. Separately, the spike found that the
OpenTelemetry SDK's `force_flush` returns `True` after a failed export,
which corrects the observability skill's advice to trust the boolean.

## Method

MLflow's score coercion and error path, ADK 2.12.0's `"{}"` tool-argument
attribute, deepeval's dotenv loading, Opik's CI switches and MLflow's
telemetry gates were confirmed in the snapshots and installed packages, and
`BatchSpanProcessor.force_flush` in opentelemetry-sdk 1.42.1, before
editing. One scenario case covers the journey; the fresh-agent trial is in
the [testing record](../testing/deepeval-mlflow-opik-alignment-2026-10-25.md).

## Drift corrected

- "Inspect the boolean result" of `force_flush`: the boolean means drained,
  not delivered.

## Imported, by specialist

- **adk-agent-evaluation.** In `provider-compatibility.md`: how MLflow's
  ADK scorers change what a result means, and deepeval's offline-only use.
- **adk-agent-observability.** In `export-paths.md`: keeping traces and
  telemetry in-house with MLflow and Opik, and the `force_flush` correction.

After the trial, which ran MLflow 3.17.2 locally, the MLflow paragraph was
rewritten from what it observed: tool names come from span names, so trace
trajectories never match; parallel calls produce a merged span that errors;
a judge failure inside ADK's evaluator arrives as "no", not as an error;
the `Hallucination` scorer sends neither tool names nor results; the scorer
needs an explicit threshold; and the server fetches LiteLLM's cost map
unless told not to. Three statements made earlier the same day from reading
alone were corrected by this. A routing row was added to the evaluation
skill.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- deepeval's key-gated ADK hook and the undocumented local-endpoint
  workaround.
- deepeval's loop-detection metric, which needs that hook's traces.
- Any metric adopted as a gate.

## Limits

MLflow and Opik were not run; the Opik callback-order effect is read, not
observed.
