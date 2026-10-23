# AG-UI 1.0, ag-ui-adk and the CopilotKit ADK example compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui)
at commit `85a427d` (2026-10-21; MIT) and
[CopilotKit/CopilotKit](https://github.com/CopilotKit/CopilotKit) at commit
`54dddf7` (2026-10-21; MIT), sparse-cloned on 22 October 2026 into their own
directories and read, never run, plus the archived `CopilotKit/with-adk`
README fetched raw. Files read: the ADK middleware's
`integrations/adk-middleware/python/CHANGELOG.md` (0.7.1 to 0.11.0 and the
unreleased section) and `README.md`; `docs/spec/1.0/changelog.mdx` and
`basic/patterns/interrupt-resume.mdx`; the TypeScript client's
`src/verify/` exports; the example's `agent/pyproject.toml` and
`package.json`. The version facts (ag-ui-adk 0.11.0, the 0.8.0 floor, the
0.11.0 security fix, AG-UI 1.0's normative changes) were applied in Phase B;
this note covers the approval contracts and the example.

**Conclusion.** The memo's main finding holds: 1.0 makes human approval two
incompatible client contracts, and `ag-ui-adk` implements both behind one
flag that is off by default for a stated reason. The frontend skill now
makes the ticket declare the contract, carries the middleware's enforcement
codes and the tests that prove each, and routes the paused position through
`from_app()` with resumability as the middleware README recommends. The
CopilotKit example confirms the generation mix the memo described, with the
exact pins. `verifyEvents` exists and is named as the 1.0 stream check
beside the bundled 0.x checker.

## Method

Facts were read from the middleware changelog and README, and the 1.0
pattern page, and written at the approval decision in the frontend skill
with the versions; the guardrails skill gets one sentence on the frontend
counterpart; the sources record is in the skill's provenance file. One
scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/ag-ui-copilotkit-alignment-2026-10-22.md).

## Drift corrected

- Beyond Phase B's 0.10.0 to 0.11.0 correction: the `RunAgentInput.resume`
  acceptance regardless of the flag is in the changelog's unreleased
  section, so the skill cites only the released 0.7.1 and 0.8.0 behaviour
  for enforcement and names `resume` as the 1.0 answer path.
- The example's web app pins `@ag-ui/client` 1.0.2 and `@copilotkit/react-core`
  1.79.0, not the 1.69.0 line the recipe exercised; recorded in
  compatibility rather than changing the tested recipe.

## Imported, by specialist

- **adk-frontend-integration.** The approval-contract section (both
  contracts, `emit_interrupt_outcome`, the three `RUN_ERROR` codes, the
  reason the flag defaults off, the declaration rule and its tests,
  `from_app()` with resumability and the deprecated direct path,
  `protocolVersion`, the 0.11.0 state-key rule, `verifyEvents` versus the
  bundled checker's scope); the example's location and pins; a line in
  production's replay section and in the recipe's header.
- **adk-operational-guardrails.** The frontend counterpart of the approval
  gate, owned by the frontend skill.

## Routed, not copied

Nothing to route; `verifyEvents` is invoked from the client package.

## Vendored assets

None: the 1.0 `schema.json` (MIT) was considered and not bundled, because
the bundled checker validates the 0.x profile and a schema file would need
its own tests.

## Left out, with reasons

- Updating `check_agui_trace.py` to the 1.0 shape (`outcome`, reasoning and
  subagent events, `protocolVersion`): a helper change with tests, left for
  a change of its own; the reference says what the checker does not cover.
- The A2UI helper in the middleware (`protocolVersion` 0.8 or 0.9,
  `generate_a2ui`): belongs with the A2UI source if it is reached.
- The predictive-state `confirm_changes` flow beyond naming it.

## Limits

Read, not run; the middleware's enforcement codes and the client's refusal
behaviour were taken from its changelog and README on one day and were not
exercised against a browser.
