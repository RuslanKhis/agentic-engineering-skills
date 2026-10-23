# OpenAI Agents SDK docs and Microsoft Agent Framework decisions compared with this toolkit — 23 October 2026

## Scope and snapshot

A review of [openai/openai-agents-python](https://github.com/openai/openai-agents-python)
at commit `841dfdd` (2026-10-22; MIT; `docs/guardrails.md`,
`docs/human_in_the_loop.md`, `docs/testing.md`) and of
[microsoft/agent-framework](https://github.com/microsoft/agent-framework) at
commit `0200599` (2026-10-21; MIT; `docs/decisions/0045-dotnet-unanswered-tool-approvals.md`,
status proposed, dated 2026-10-02, and `0019-python-context-compaction-strategy.md`,
status accepted), sparse-cloned on 22 October 2026 and read on 23 October,
never run. Nothing from either framework is imported as code or API; each
rule is restated for ADK's own callbacks and gates and labelled as another
framework's documented behaviour.

**Conclusion.** The memo's reading holds and four rules the toolkit lacked
or left implicit are now explicit: screening placement (first agent, last
agent, every guarded tool call; blocking when it must prevent an effect; a
rejected output keeps tool events and gets a static, data-free envelope; a
raising check is an unknown verdict); approval rules that fail closed on
unreadable arguments; an unanswered approval rejected on the next run with
a late answer unable to authorise it; and a strict scripted model that fails
on extra or missing model calls. From the compaction decision: atomic
call-and-result groups and the three compaction points, which name the
failure ADK's 2.12.0 orphaned-call fix repaired.

## Method

Docs read in full for the named passages; each rule placed at the decision
in the guardrails, security, evaluation and optimise skills with the commit,
date and the "restated" label. Two scenario cases cover the journeys; the
fresh-agent trial is recorded in the
[testing record](../testing/approval-and-screening-rules-alignment-2026-10-23.md).

## Drift corrected

- ADR-0045 is "proposed", not adopted; the skill says so.
- The OpenAI tripwire rule has a second half the memo omitted: when the
  rejected answer was a tool's own result, the payload is withheld from the
  session too, and a check that raises is an unknown verdict, not a
  rejection. Both are in the skill.

## Imported, by specialist

- **adk-operational-guardrails.** Unanswered approvals rejected on the next
  run; fail-closed approval rules.
- **adk-agent-security.** The four placement rules for any screening layer.
- **adk-agent-evaluation.** The strict scripted-model rule.
- **optimise-adk-on-google-cloud.** Atomic groups and the three compaction
  points.

## Routed, not copied

Nothing.

## Vendored assets

None.

## Left out, with reasons

- The other decision records, the SDK's sandbox, realtime and voice
  testing recipes, and its hosted-tool approval callbacks: other products.
- The `.NET` mechanics of ADR-0045 (where rejection messages are placed in
  history): implementation detail of that framework.

## Limits

Rules restated from documentation; their ADK translations (which callback,
which envelope) are this toolkit's, verified only by the scenario cases and
the trial.
