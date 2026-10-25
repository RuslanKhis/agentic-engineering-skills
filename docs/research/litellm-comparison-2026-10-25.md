# LiteLLM ADK spend fixtures compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [BerriAI/litellm](https://github.com/BerriAI/litellm) at commit
`5603724` (2026-10-24; release v1.106.3) and of the fixtures' upstream,
[BerriAI/lens](https://github.com/BerriAI/lens) at commit `e320cab`
(2026-10-16), cloned blobless and sparse on 25 October 2026 into their own
directories and read, never run. Nothing under litellm's `enterprise/` was
opened.

**Licence.** MIT outside litellm's `enterprise/`, which has its own
licence; lens is MIT. The fixtures are real redacted proxy traffic, so they
are linked, not copied.

**Maintenance.** Both active.

**Conclusion.** The memo's "ADK spend fixtures" exist in litellm, but only
as seed data for a local dev stack; the tests that use them are in lens and
are framework-neutral. What they show, checked against google-adk 2.12.0,
matters: ADK counts reasoning twice on `LiteLlm` routes whose completion
count already includes it, an `AgentTool` child's usage is missing from the
saved parent session, and `retry_options.attempts` becomes LiteLLM's
`num_retries`, which does not mean the same thing. Retried and
failed-but-billed calls are invisible to ADK and need reconciliation against
gateway or billing rows. The main target is the observability skill, not
optimisation.

## Method

The `LiteLlm` usage mapping and token-usage sum, `AgentTool`'s sub-Runner
and session, and the `num_retries` mapping were read in google-adk 2.12.0;
LiteLLM's two uses of `num_retries` in its `main.py`. One scenario case
covers the journey; the fresh-agent trial is in the
[testing record](../testing/litellm-alignment-2026-10-25.md).

## Drift corrected

None.

## Imported, by specialist

- **adk-agent-observability.** In `signals-and-schema.md`: the reasoning
  double count on `LiteLlm` and the `AgentTool` session gap, with
  aggregation by trace. In `validation.md`: four offline cost cases and the
  "unknown, not partial" reconciliation rule. In `SKILL.md`: one clause on
  `AgentTool`. In `invocation_summary.py`: a
  `reasoning_counted_twice_on_N_calls` flag from the token arithmetic, with
  a test. After the trial: the helper prices a flagged call's output from
  candidates alone; the `call_llm` span repeats `generate_content`'s usage on
  2.12; how this skill's "ignore the reported total" and the guardrails
  skill's "prefer provider totals" fit; price-table keys on `LiteLlm`; a
  failed `AgentTool` child recorded as result text; gateway joins; running
  the `LiteLlm` path offline; and the session dump call.
- **adk-model-and-output-contracts.** In `failover-and-providers.md`:
  `attempts` as LiteLLM `num_retries`.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- The fixtures and their spend figures: real redacted traffic, ADK version
  not recorded, prices from LiteLLM's own price map.
- The Lens and ClickHouse stack.
- Streaming usage, already covered.

## Limits

The lens Rust tests were not run. The reasoning double count was confirmed
on one captured provider route; other providers may report differently.
