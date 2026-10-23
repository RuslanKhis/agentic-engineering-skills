# Pydantic AI documentation compared with this toolkit — 23 October 2026

## Scope and snapshot

A review of [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)
docs at commit `eb0bd08` (2026-10-21; MIT), sparse-cloned on 22 October
2026 and read on 23 October, never run: `docs/durable_execution/overview.md`,
`docs/deferred-tools.md`, `docs/evals/evaluators/span-based.md`,
`docs/evals/online-evaluation.md`.

**Conclusion.** Three shapes, no dependencies. The "durability is not
storage" framing was already carried into the workflow and designer skills
by the durable-execution review and is cited there; the deferred-tool
taxonomy (approval-required versus externally executed, both keyed by call
id, resolved inline or bubbled up) gives the tool-interface skill a clean
statement of what ADK's `require_confirmation` and `LongRunningFunctionTool`
are instances of; span-based trajectory grading and the online-evaluator
shape (background, sampled, one `gen_ai.evaluation.result` event per result)
land in the evaluation and observability skills beside the OpenTelemetry
review's event definition.

## Method

Four pages read; each shape restated for ADK with the commit and the
"another framework's documentation" label; no API names imported except as
citations. The journeys are covered by the existing observability and
tool-interface scenario cases; no separate trial, because the change adds
vocabulary and attachment points rather than a new mechanism.

## Drift corrected

- The memo listed pydantic-ai under the durability fork; that fork's facts
  came from Google's resume page and the two engines, so this note credits
  the framing only.

## Imported, by specialist

- **adk-tool-interface-design.** The two kinds of deferred call.
- **adk-agent-evaluation.** Span-based trajectory grading under the
  end-state rule.
- **adk-agent-observability.** The online-evaluator shape.

## Routed, not copied

Nothing.

## Vendored assets

None.

## Left out, with reasons

- Pydantic Evals as a harness for ADK: it needs the logfire SDK to capture
  spans; not spiked.
- The backends pages (Temporal, DBOS, Prefect, Restate, Airflow): covered
  for ADK by the engines' own integrations.

## Limits

Read, not run.
