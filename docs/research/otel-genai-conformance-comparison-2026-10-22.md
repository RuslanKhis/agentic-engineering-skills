# OpenTelemetry GenAI conventions and conformance compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [open-telemetry/semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai)
at commit `9ffc7e0` (2026-10-21) and
[open-telemetry/semantic-conventions-conformance](https://github.com/open-telemetry/semantic-conventions-conformance)
at commit `3a5dd62` (2026-10-21), both Apache-2.0 with no NOTICE, cloned on
22 October 2026 into their own directories and read, never run. Files read:
the google-adk reference scenario (`reference/scenarios/google-adk/README.md`,
`conformance.yaml`, `scenario.py`, `pyproject.toml`), `docs/gen-ai/gen-ai-events.md`
and `gen-ai-agent-spans.md`; the conformance repository's `README.md` and
the `tools/gen-ai/` runner and mock-server layout with their `pyproject.toml`
names. Related Phase B facts (the OpenInference 2.10 floor, the new home of
the GenAI instrumentation) were already applied.

**Conclusion.** The conventions now publish, for google-adk specifically, a
list of what is implemented and a list of expected violations. That list is
the baseline the observability skill lacked: a run on the pinned version that
shows a violation beyond it is drift. Two cautions were found in the source
and carried into the skill: the scenario is pinned to ADK 2.11.0, and it
patches ADK's native tool-span functions out in favour of the conventions'
reference instrumentation, so it describes ADK's operations and attributes
rather than ADK's native tool spans. The runner is not published, so the
check is written as planned until a team installs it from the repository.

## Method

Facts were read from `conformance.yaml` and `scenario.py` rather than the
README where they could differ; each is cited with the commit; the skill's
rules on content capture, token arithmetic and one provider owner are
untouched. One scenario case covers the journey; the fresh-agent trial is
recorded in the [testing record](../testing/otel-genai-conformance-alignment-2026-10-23.md).

## Drift corrected

- The memo's "Weaver live-check with the conformance runner's mock LLM
  server" is right about the shape; the runner packages
  (`opentelemetry-conformance`, `genai-conformance`, both `0.1.0.dev0`) are
  installed from the repository and are on no index, which the memo did not
  say.
- The memo did not note that the scenario patches ADK's native tool-call
  tracing; the skill does.

## Imported, by specialist

- **adk-agent-observability.** The reference scenario's implemented
  operations and its expected violations with the two cautions, the rule to
  key dashboards on `gen_ai.provider.name`, `gen_ai.operation.name` and
  `gen_ai.agent.name` rather than the removed `gen_ai.system`, the planned
  Weaver check with what to record, and `gen_ai.evaluation.result` with its
  required and recommended attributes as the way to put scores on traces.

## Routed, not copied

Nothing: a convention and a runner, not skills.

## Vendored assets

None.

## Left out, with reasons

- Running the scenario: the runner is not published and the rules forbid
  executing the downloaded repository; written as planned verification.
- The other scenarios (`adk_a2a`, other frameworks): no decision here
  depends on them.
- The conventions' metrics and inference pages beyond what the skill already
  cites.

## Limits

Read, not run; every convention is at Development status and the scenario
is pinned to 2.11.0, so the violation list is a dated baseline rather than a
contract.
