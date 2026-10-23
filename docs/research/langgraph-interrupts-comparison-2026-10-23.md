# LangGraph's rules of interrupts compared with this toolkit — 23 October 2026

## Scope and snapshot

A review of [langchain-ai/docs](https://github.com/langchain-ai/docs)
`src/oss/langgraph/interrupts.mdx` at commit `23152b1` (2026-10-21; MIT),
sparse-cloned on 22 October 2026 (checkout repaired on 23 October) and
read, never run.

**Conclusion.** The page's "Rules of interrupts" are framework-independent
once restated: a node re-runs from its beginning on resume, so side effects
before the pause are idempotent or moved after it; a pause wrapped in a bare
exception handler never reaches the caller; pause points inside one node
are not reordered or made conditional, because resume values match pauses by
position; and loops around a pause must be deterministic across executions.
They now sit in the workflow skill's runtime reference under the
resume-versus-durable-execution section, with the ADK translation
(`rerun_on_resume=True` nodes and confirmation-requesting tools) and the
at-least-once statement they restate from the node's side.

## Method

The rules section read in full; restated with the commit and label; placed
beside the engine facts so a reader sees them at the resume decision. The
journey is covered by the durable-refund scenario case and its trial.

## Drift corrected

- The memo's four bullets match the page; the page adds that side effects
  before the pause must be idempotent as a named rule, which the skill
  keeps.

## Imported, by specialist

- **adk-workflow-design.** The four rules in the runtime reference.

## Routed, not copied

Nothing.

## Vendored assets

None.

## Left out, with reasons

- Time-travel re-execution (checkpoint forking): ADK's `rewind_async` is a
  different primitive and is covered by the ADK source review.
- Response schemas for interrupt values: a LangGraph feature.

## Limits

Read, not run; the ADK mapping is this toolkit's.
