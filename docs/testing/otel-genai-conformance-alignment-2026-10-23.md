# OpenTelemetry GenAI conventions and conformance alignment — 23 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/otel-genai-conformance-comparison-2026-10-22.md).
In the repository (22 October): the reference scenario's implemented
operations and expected violations with two cautions, the dashboard keying
rule, the planned Weaver check and the `gen_ai.evaluation.result` event in
the observability skill. After the trial (23 October): the expected
violations as a data asset
(`assets/semconv-expected-violations.adk-2.11.0.json`), a drift-check
procedure that works without the unpublished runner, how to produce a saved
session offline for the helpers, the judge event spelled out as a log record
in the evaluated span's context with the ids the sessions store must keep
and a namespace for the judge identity, the collector's Prometheus naming
rule for third-party dashboards, and a version tag on the skill's span-count
assertion. **One scenario case** (`observability-semconv-drift-and-evaluation-events`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. No helper, test or `last-tested` date
changed; the new asset is data.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or OpenTelemetry SDK installed, on a synthetic project, without the
expected answers.

### Observability: dashboards on the conventions, a drift check, judge scores on traces

The project: an ADK 2.11 agent exporting to a Grafana stack through a
collector, dashboards keyed on `gen_ai.system`, a nightly judge writing to
BigQuery only.

What the agent did: rewrote the dashboards onto the registry keys with the
ADK-owned keys kept as joins; built a contract module from the skill's
prose, a drift-check command with exit codes that classifies deviations as
known or drift against a committed baseline, and a dashboard lint; gave the
telemetry module a meter provider (without which no metric panel could have
had data), content gates defaulted off for a third-party backend, and a
bounded shutdown; turned judge scores into `gen_ai.evaluation.result` log
records in the judged span's context and extended the sessions query to
carry the ids; 29 pure tests run, SDK tests reported as not run on the
project interpreter; a notes file listing the baseline capture, the runner
and the collector confirmations as planned.

Ease rating: **3 of 5**. Routing was immediate; the guidance existed but
was spread over five references with the key sentences inside long
paragraphs, and the drift check had no deliverable shape.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The drift check had no shape when the upstream runner is unavailable | A procedure from parts the skill has: the list as data, the in-memory exporter test as the export, a classifier, a committed baseline, exit codes |
| The expected-violation list was prose; which `gcp.vertex.agent.*` keys it covers was unclear | A data asset with the ten entries and the statement that only five keys are upstream's |
| "Parented to the span" for a nightly job needed spelling out; the judge identity had no attribute; the ids were not stored | Stated: a log record in the span's context, the three ids the store must keep, a namespaced judge pair |
| Prometheus naming for a collector-fed Grafana was unaddressed | The exporter's normalisation and suffix options from the collector README, with the rule to read `/metrics` once |
| The helpers assume a saved session exists | The scripted-Runner test dumps one |
| The skill's one-span assertion read as unconditional | Version-tagged |
| The token-usage metric name is hedged; the engineer's apply section is long | Left: the name must be observed on the installed package; the section's placement is a Phase D question |

## What this does not establish

No export was observed; the baseline fixture is hand-written in the 2.11.0
shape; the collector's names were not read.
