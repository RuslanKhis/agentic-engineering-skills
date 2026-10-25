# Claude and OpenAI cookbooks compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of selected notebooks in [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks)
at commit `bfe50e5` (2026-10-24) and [openai/openai-cookbook](https://github.com/openai/openai-cookbook)
at commit `8495326` (2026-10-23), sparse-cloned on 25 October 2026 into their
own directories and read as data, never executed. These are another
vendor's patterns: only framework-neutral ideas are restated, mapped to ADK
2.12 mechanisms.

**Licence.** Both MIT, no NOTICE. Nothing is copied.

**Maintenance.** Both active; no releases, so pinned by commit.

**Conclusion.** Two of the memo's ideas hold in a narrower form. Escalation
is worth evaluating, but as a pair (missed and over-escalation on cases
with a reviewed expected lane), not as a raw rate; the notebook prints lane
counts and proposes no metric. Clearing and compaction advice changes ADK
practice in three places, all checked in ADK's source: the built-in sliding
context filter moves the prompt prefix every turn, so an explicit cache
never forms under it; the summariser cuts each tool payload at 2,000
characters and a custom template replaces its defaults; and summaries are
seeded from the previous one, so what survives two compactions is worth
probing.

## Method

`ContextFilterPlugin`'s cut condition and exception path, the cache
fingerprint, the summariser's truncation and template, and the rolling
summary seed were read in google-adk 2.12.0 before editing. One scenario
case covers the escalation journey; trials for both changed journeys are in
the [testing record](../testing/cookbooks-alignment-2026-10-25.md).

## Drift corrected

None.

## Imported, by specialist

- **optimise-adk-on-google-cloud.** In `context-window.md`: the sliding
  filter against the explicit cache, the summariser's 2,000-character cut
  and template replacement, and a two-compaction survival probe.
- **adk-agent-evaluation.** In `evaluation-design.md`: missed- and
  over-escalation rates on cases with a reviewed expected lane.
- **adk-operational-guardrails.** In `human-review.md`: deterministic
  escalation rules in code; the model may escalate more, never less.

After the two trials: a pre-model route so a forced case reaches review
even when the model does nothing, the floor share and an unreachable
target as the policy owner's decision, Tool Confirmation kept apart from a
review queue, a routing row for escalation targets, and
`before_agent_callback` in the guardrails inspector; on the context side,
`LoadArtifactsTool`'s list landing in the system instruction and breaking
the explicit cache, the corrected placement check for tool continuations,
how to test the cache offline, the compaction threshold against cached
tokens, a locator kept in state, the 2.12 file and import paths, the
bounded-result limit, and what the inspector's 2.8.0 gate means on 2.12.

## Routed, not copied

- "Store workflow lessons, not case facts" from the memory notebooks, for
  `adk-memory-architecture`'s next review.

## Vendored assets

None.

## Left out, with reasons

- The OpenAI improvement loop's gate: model-written evals, a judge on the
  same unpinned model alias as the agent, scoring of existing traces rather
  than a candidate run, and automatic merge and deploy.
- The gate notebook's simulated reviewer and its `always_allow` tools.
- Vendor model identifiers and prices; background "instant compaction";
  trace-to-eval mechanics already covered by the observability skill.

## Limits

Nothing was executed; the cache interaction is read from source, not
measured. Several notebooks were not read.
