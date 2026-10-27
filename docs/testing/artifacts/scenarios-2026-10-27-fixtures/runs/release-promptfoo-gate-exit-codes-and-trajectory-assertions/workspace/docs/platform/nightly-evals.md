# Nightly agent evals (Promptfoo)

Files: `package.json` (promptfoo pinned to 0.124.1), `evals/promptfooconfig.yaml`,
`evals/provider.py` (runs the ADK agent in process against `tests/fakes.py`; no real payments or
mail), `evals/expectations.json` (cases, repeat, required assertion types, baseline date),
`evals/gate.py` (the reader), `.github/workflows/nightly.yml`.

## How the job reads the result

Never use `promptfoo eval`'s exit code alone. The job records it, then `evals/gate.py` reads it
together with `results/promptfoo.json` and returns its own code:

| Gate exit | Meaning | Job |
| --- | --- | --- |
| 0 PASS | Every expected row present (cases x repeat), no error rows, every required assertion type graded and passed, baseline measured | green |
| 1 BLOCK | A graded assertion failed, or promptfoo exited 100 | red |
| 2 NOT RUN | No/garbled JSON, promptfoo exit other than 0 or 100 (1 = harness error), wrong row count, error rows, a required assertion type missing | red |
| 3 PROVISIONAL | All passed, but `baseline_measured_on` is null so thresholds are unmeasured | green with a warning; record as provisional, never as a pass |

Why: promptfoo exits 100 on a failed test, 0 on pass, 1 on other errors (observed on 0.124.1 with
the echo provider, 2026-10-22, per the adk-agent-evaluation reference). An empty suite exits 0,
and errored rows count as failures, so the exit code alone can report green for nothing run or
red for a harness fault. NOT RUN outranks BLOCK because error rows make the counts meaningless.
`PROMPTFOO_PASS_RATE_THRESHOLD=100` keeps the exit code strict; the gate also checks rows itself.

## Assertions

Tool trajectory: `trajectory:tool-used`, `tool-args-match` (partial), `tool-sequence`, read from
ADK's native spans (`execute_tool <tool>`, `gen_ai.tool.name`). Spans: `trace-span-count` and
`trace-error-spans`. Tool arguments exist on spans only with
`ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=true`; the job sets it, and `redactAttributes` keeps the model
request and response out of Promptfoo. Side effects are checked on the fakes
(`payments_requests`).

## Before the thresholds count

1. First live run: confirm the assertion shapes, the span names under
   `ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN=1` (assumed; model span is `call_llm` or
   `generate_content <model>`), and that `opentelemetry-exporter-otlp-proto-http` is importable.
2. Run the suite five times, set `baseline_measured_on` in `evals/expectations.json`. Until then
   the verdict is PROVISIONAL. `--repeat 3` is a rule over rows (all must pass), not an estimator.
