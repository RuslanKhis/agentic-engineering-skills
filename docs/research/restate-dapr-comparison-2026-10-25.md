# Restate and Dapr compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [restatedev/sdk-python](https://github.com/restatedev/sdk-python)
at commit `37953b6` (its `ext/adk` plugin), the server licence in
[restatedev/restate](https://github.com/restatedev/restate) at `4b2fb2c`, the
example [restatedev/restate-google-adk-example](https://github.com/restatedev/restate-google-adk-example)
at `b306b86`, and Dapr's ADK integration, the `diagrid` package in
[diagridio/python-ai](https://github.com/diagridio/python-ai) at `cbd4f90`,
cloned on 25 October 2026 into their own directories and read. The published
packages were installed in throwaway environments and probed against a
stand-in Restate context and a scripted model; no server or sidecar was
started. Restate's external-events page was read on the same day. This
builds on the [durable execution note](durable-execution-comparison-2026-10-23.md).

**Licence.** Restate SDK MIT; Restate server Business Source License 1.1
with a grant permitting production use running your own services;
`diagrid` a modified Business Source License whose free production use is
limited to organisations under 60 full-time staff and US$15 million revenue,
so its adoption is an owner decision. Nothing is copied.

**Maintenance.** All active except the example (last commit February 2026).

**Conclusion.** Neither engine can be added without conditions. Restate's
plugin journals model calls but makes tools durable only when their bodies
opt in, and because it answers the model step itself it silences the
agent's model callbacks, later plugins' model callbacks and `max_llm_calls`,
and it breaks ADK's confirmation resume. `diagrid` does not run ADK at all:
it re-implements the loop and drops callbacks, plugins, state and
confirmation. Restate's awakeable approval is a durable wait whose id acts as
a credential, not a review gate.

## Method

The plugin's `LlmAgent` check, `stream=False` call and `run_typed` step,
the session service's empty-session default, ADK 2.12.0's early-exit paths
for a plugin that answers `before_model_callback`, both licences,
`diagrid`'s analytics opt-outs and Restate's documented queuing and resolve
path were confirmed before editing. One scenario case covers the journey;
the fresh-agent trial is in the
[testing record](../testing/restate-dapr-alignment-2026-10-25.md).

## Drift corrected

None in the skills. adk.dev's Restate page says every tool execution is
journaled; the plugin source does not do that, and the skill says so.

## Imported, by specialist

- **adk-workflow-design.** In `runtime.md`: Restate and Dapr beside
  Temporal and DBOS, with what each makes durable, what breaks on ADK 2.12
  and their licences.
- **adk-operational-guardrails.** In `runtime-bounds.md`: a plugin that
  answers the model step silences later guards and the call limit. In
  `human-review.md`: an awakeable is a durable wait, not a review record.
- **adk-system-designer.** In `design-decisions.md`: the two engines as
  catalogue options with conditions and their licences.
- **safe-api-tool-calls.** In `writes-and-confirmation.md`: the
  kill-after-the-write test, named and defined (the workflow skill cited it
  but no skill defined it), with Restate beside Temporal and DBOS.

After the trial: the after-model skip corrected to cover every plugin, not
only those listed after the engine; usage accounted in `on_event_callback`
with fields assigned rather than mutated; admission-time budgets blocking
the crossing response's tools; the confirmation failure's cause and a
replacement pattern; package names and versions; the stand-in shape; and a
reason on the workflow inspector's exit 3.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- Either engine as a default recommendation.
- The example's pattern of handing the approval text to the model to act on.
- Restate Cloud and Diagrid Catalyst hosting, not evaluated.

## Limits

No server or sidecar ran, so replay, suspension and retry were not
observed; the licence reading is not legal advice.
