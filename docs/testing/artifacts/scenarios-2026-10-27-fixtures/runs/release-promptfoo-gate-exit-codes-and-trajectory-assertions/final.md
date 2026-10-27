Nothing in the Promptfoo wiring has been run. I have no shell here, so I couldn't run the unit tests, install Promptfoo or call a model.

## What the job should read
The job should not use `promptfoo eval`'s exit code on its own. It saves the code, then `evals/gate.py` reads that code and `results/promptfoo.json` together and returns its own code:

| Gate exit | Meaning | Job |
|---|---|---|
| 0 PASS | Every expected row is present (5 cases × 3 repeats). There are no error rows, every required assertion type was graded and passed, and the baseline date is set. | green |
| 1 BLOCK | An assertion failed, or Promptfoo exited 100. | red |
| 2 NOT RUN | The JSON is missing or garbled, Promptfoo exited with something other than 0 or 100, the row count is wrong, there are error rows, or a required assertion type is missing. | red |
| 3 PROVISIONAL | Everything passed, but `baseline_measured_on` is still null. | green with a warning; recorded as provisional, never as a pass |

- **Exit codes:** a failed test exits 100, pass exits 0, and a harness error exits 1. This comes from the skill's notes on Promptfoo 0.124.1 and an `echo` provider run, not from anything I ran.
- **Empty suite:** it exits 0, so the exit code alone would report green for nothing run.
- **Error rows:** they count as failures, so the exit code alone can report red for a harness fault.
- **Precedence:** NOT RUN outranks BLOCK, because error rows make the counts meaningless.

## What I added
- `package.json`: Promptfoo pinned at 0.124.1.
- `evals/promptfooconfig.yaml`: five cases using `trajectory:tool-used`, `tool-args-match`, `tool-sequence`, `trace-span-count` and `trace-error-spans`.
- `evals/provider.py`: runs the ADK agent in process. It exports ADK's own spans to Promptfoo's OTLP receiver. Payments and mail use `tests/fakes.py`, so nothing reaches a real provider. It also sets `SUPPORT_DB_PATH=:memory:`, because `build_agent` would otherwise create `support.db`.
- `evals/gate.py`, `evals/expectations.json`, `tests/test_eval_gate.py`: the reader, its case list, and 11 tests for it on synthetic JSON.
- `.github/workflows/nightly.yml`: runs `npm install`, then Promptfoo with `--repeat 3`, then the gate, and uploads the results.
- `docs/platform/nightly-evals.md`: this exit-code table and the first-run checks.

## Assumptions (nobody could answer)
- **Refund order:** the refund case expects `lookup_order` before `issue_refund`, taken from the scripted-test docstring. Confirm that is the real requirement.
- **Refund confirmation:** the prompt has no confirmation step before `issue_refund`, although that test's docstring mentions one. I did not change the agent.
- **Span schema:** `ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN=1` is a guess. The first live trace should settle it.

## Left undone
- **Unrun:** the unit tests, the assertion YAML and `trace-span-count` syntax against 0.124.1, and the provider itself. The provider also needs `opentelemetry-exporter-otlp-proto-http` importable.
- **Baseline:** the thresholds are unmeasured. Run the suite five times, then set `baseline_measured_on`. Until then the verdict is PROVISIONAL.
- **Lockfile:** none exists, because generating one needs the network.
- **Wrong gate code:** if no JSON is written, the gate reports NOT RUN. A first-run schema mismatch is therefore a red job, not a silent pass.