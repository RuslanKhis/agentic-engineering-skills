# Promptfoo alignment — 23 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/promptfoo-comparison-2026-10-22.md).
In the repository (22 October): the ADK 2.x provider shape, assertion types,
tier placement and spiked exit codes in the evaluation skill's provider
compatibility; the exit-code mapping in the release skill's CI gates; the
native-key dependency in observability. After the trial (23 October): the
provider contract and the tracing configuration keys from the docs, the
content-gate dependency and `redactAttributes`, the args matcher's fallback,
the 2.12.0 span names with the schema opt-in, the two gate traps (an empty
suite exits 0; errors count as failures) with the project reader's rules,
and the `find_spec` skip trap. **One scenario case**
(`release-promptfoo-gate-exit-codes-and-trajectory-assertions`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. No helper changed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no model, no
ADK installed, on a synthetic project, without the expected answers; the
agent was allowed to run the pinned promptfoo with the `echo` provider
only, telemetry and sharing off.

### Release and evaluation: a nightly Promptfoo gate on trajectories and native spans

The project: an ADK 2.12 trip planner, Node and Python on the runner, a
model key only in the nightly job.

What the agent did: an in-process Python provider owning one tracer
provider per worker, parenting ADK's spans under the test's trace and
draining one JSON payload; a nightly configuration with the OTLP receiver,
redaction of the request and response attributes, three cases asserting
trajectories, span counts and effects; a results reader with four outcomes
that counts rows, refuses error rows and checks assertion types, validated
against real echo-provider runs (exit 0, 100, threshold 0, missing config
1); a two-tier workflow; 29 tests run on the pin-meeting interpreter with
the SDK and OTel tiers reported as not run; the tools split out of the
agent module; a notes file with the result-reading procedure.

Ease rating: **3 of 5**. The routing was immediate; the Promptfoo route was
one paragraph with no artefact, and the span and attribute facts were spread
over three skills and verified against the bundle.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| No provider skeleton: traceparent, receiver, tracing keys, return shape | Stated from the docs: the provider contract, the tracing block, the receiver address, `redactAttributes`, the JSON-string output |
| The zero-tests exit-0 trap and errors counting as failures | Both stated in the evaluation and release references with the reader's rules |
| The args assertion relied on a fallback and on ADK's content gate | Both stated, with the gate to set and the redaction to keep prompts out |
| No Promptfoo variant of the workflow asset; the CSV checker cannot read its JSON | The reader's rules stated; the asset left as the ADK-native shape |
| Which model span 2.12.0 emits | `generate_content <model>` beside the legacy `call_llm`, with the schema opt-in, from the installed package |
| `find_spec` raises when the parent package is absent | The guard stated in deterministic tests |
| The heading says "proven on Inspect" while Promptfoo is vendor guidance; the engineer's ticket paragraphs | Left: the heading is accurate about what was proven; the paragraphs' placement is recorded under Phase D |

## What this does not establish

The ADK provider never ran; the span-smoke configuration and the nightly
suite were not executed; the exporter pin and the model-span choice wait
for the first live trace.
