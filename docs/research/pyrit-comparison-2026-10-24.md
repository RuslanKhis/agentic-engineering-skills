# PyRIT compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [microsoft/PyRIT](https://github.com/microsoft/PyRIT) at commit
`bc5a8bc` (2026-10-23; MIT; `pyproject.toml` on main says 1.2.0.dev0),
cloned on 24 October 2026 into its own directory and read, never run. Files
read: `pyrit/prompt_target/a2a_target.py`, `pyrit/executor/workflow/xpia.py`
and its `__init__.py`, `doc/code/targets/0_prompt_targets.md` (A2A section),
`doc/code/executor/5_workflow.py`, `pyproject.toml`, `LICENSE`,
`NOTICE.txt`. The latest release, 1.1.0 (2026-09-04), was installed from
PyPI into a scratch environment and introspected only.

**Maintenance.** Active: commits daily, releases about monthly. The separate
`Azure/PyRIT` repository is archived.

**Conclusion.** The memo's headline, that PyRIT's `A2ATarget` lets you
red-team an ADK agent over A2A with no adapter, is true of the main branch
only: 1.1.0 raises `ImportError` for it and has no `a2a` extra, which PyPI's
metadata confirms. The cross-domain injection workflow is released and has a
model-free scoring route, which is what fits this toolkit: the security
skill now shows how to make PyRIT's poisoned-document workflow score the
executed tool calls with a substring scorer, so the deterministic
forbidden-call assertion stays the grader, and the interoperability skill
records the A2A target's seam settings for when a release carries it.

## Method

Facts were read from source and checked against the installed 1.1.0
(`ImportError` for `A2ATarget`; the XPIA classes, `XPIAContext` fields and
`SubStringScorer` signature present) and against PyPI's extras list. One
scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/pyrit-alignment-2026-10-24.md).

## Drift corrected

- The memo's "speaks A2A 0.3 and 1.0, discovers cards, continues
  `input-required` tasks" is right on main and absent from every release; the
  memo did not say so.
- "Discovers cards" is not the default: `protocol_version` defaults to
  `"0.3"`, and only `"auto"` reads the card.
- "A natural ASI07 tool": it tests the remote agent's behaviour; a peer
  injecting into our own agent stays a fake-peer test.
- Our skill's PyRIT line was right but named no class or workflow.

## Imported, by specialist

- **adk-agent-security.** In the live campaign: `XPIAWorkflow` with a
  callback that runs the `Runner` against fakes and returns executed calls,
  `SubStringScorer` on the forbidden target, `UNKNOWN` without a scorer, the
  memory initialisation, the manual workflow kept out of CI, and the
  `A2ATarget` release status with its dependency floor.
- **adk-agent-interoperability.** Under "Measuring, not just testing": the
  target's protocol default, the prefixed card path for ADK, one text part
  per turn, `input-required` and `auth-required` continuation, the token
  provider instead of a static key, and the no-blind-resubmit rule after a
  polling timeout.

- **From the trial.** The scoring rule (executed calls and recorded effects
  only), the offline A2A route through an ASGI transport, the custom setup
  target's shape, `google-adk[a2a]` and the task-history exposure for
  `to_a2a`, and a `complete` flag on the security inspector's trifecta
  summary so a factory-built tool list reads as unknown.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- Azure-specific targets and credentials, and the static `X-API-Key` option
  for the A2A target: platform identity first.
- LLM scorers such as `SelfAskTrueFalseScorer` as the pass or fail grader.
- `XPIAManualProcessingWorkflow`, which blocks on `input()`.
- Installing from git main; the frontend, GUI and Docker material.
- Preserved notebook outputs as evidence.

## Limits

`A2ATarget` was not run against a local ADK A2A server because no release
contains it; whether its 0.3 mode works against an ADK server on a2a-sdk 1.x
is unverified. No workflow or attack was executed.
