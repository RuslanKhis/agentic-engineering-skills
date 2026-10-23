# Promptfoo compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)
at commit `15bcb0d` (2026-10-22; MIT), sparse-cloned on 22 October 2026
into its own directory and read, of the
[promptfoo-action](https://github.com/promptfoo/promptfoo-action) README
fetched raw, and of the published package `promptfoo` 0.124.1 (npm) run once
outside the repository with its `echo` provider to observe exit codes. Files
read: `site/docs/guides/evaluate-google-adk.md` and
`site/docs/usage/command-line.md`. The memo's note on the project's
ownership was not checked and is not repeated.

**Conclusion.** The memo's claim holds: Promptfoo's ADK 2.x guide is an
in-process Python provider that asserts on ADK's native spans and drained
session state, with no span translator. That makes it a usable
model-dependent tier for teams standardised on it, so the evaluation skill
records the provider shape and the assertion types, the release skill maps
its exit codes onto the gate vocabulary, and the observability skill notes
that the guide keys on ADK-owned span attributes. The exit codes were not
taken from the docs: a two-test suite on the `echo` provider exited 100 with
one failure, 0 with the same failure under a pass-rate threshold of 40, and
0 with both passing.

## Method and spike

Docs read for the provider shape and assertion names; `command-line.md` for
the exit-code statement; the action README for `repeat`, `repeat-min-pass`,
`fail-on-threshold` and sharing. The spike used `npx -y promptfoo@0.124.1
eval` with telemetry and sharing off, no model, no network beyond the
package download. Facts placed with the commit, the package version and the
spike date. One scenario case covers the journey; the fresh-agent trial is
in the [testing record](../testing/promptfoo-alignment-2026-10-23.md).

## Drift corrected

- Exit code 100 was a documentation claim in the memo; now observed, with
  the threshold path and the all-pass path.
- The memo's "ADK provider on native spans" is specifically the guide's
  example provider exporting to Promptfoo's OTLP receiver; the trajectory
  assertions work on those spans, and `trace-span-count` and
  `trace-error-spans` are separate.

## Imported, by specialist

- **adk-agent-evaluation.** Provider shape, assertion types, tier
  placement, exit codes and the action's options in provider compatibility.
- **adk-release-engineering.** Exit-code mapping and the at-least-m-of-n
  note in the CI gates reference.
- **adk-agent-observability.** The native-key dependency in trace to
  evaluation.

## Routed, not copied

Nothing; a harness invoked by name.

## Vendored assets

None.

## Left out, with reasons

- Promptfoo's red-team plugins and model-graded assertions: the security
  skill's adversarial suite and the evaluation skill's judge calibration
  already own those decisions; a later pass may compare them.
- `promptfoo optimize`: prompt optimisation belongs with the instructions
  skill's GEPA material.
- The bundled example's code: read for shape, not imported.

## Limits

The spike exercised exit codes only; the ADK provider and the trace
assertions were read, not run, and need a model.
