# Strands steering and chaos testing compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk)
at commit `beae278` (2026-10-24, steering) and [strands-agents/evals](https://github.com/strands-agents/evals)
at commit `f6b894f` (2026-10-23, chaos testing; the memo placed it in
harness-sdk), cloned on 25 October 2026 into their own directories and read,
never run.

**Licence.** Both Apache-2.0 with a one-line NOTICE (harness-sdk keeps its
licence in `LICENSE.APACHE`). Only designs are restated; no code is copied,
so the NOTICE duty does not arise.

**Maintenance.** Both active.

**Conclusion.** Steering adds nothing the skills lack: cancel-with-guidance,
the ledger, interrupts and after-model retry are each already covered, and
the one new idea, an LLM judge inside the before-tool seam, fails open as
shipped. Chaos testing is worth two additions to the evaluation skill: a
single-fault matrix with a no-fault twin built from ADK's own Environment
Simulation fields, and resilience scored by checks, because Strands' judges
pass a trace in which the fault never fired.

## Method

ADK 2.12.0's `InjectionConfig` fields, validator, latency path, real-tool
fall-through and per-call reseeding were read in the installed package;
Strands' one-effect rule, baseline twin and judges' 0.5 scores in the
snapshot. One scenario case covers the journey; the fresh-agent trial is in
the [testing record](../testing/strands-alignment-2026-10-25.md).

## Drift corrected

None.

## Imported, by specialist

- **adk-agent-evaluation.** In `execution-evidence.md`: the fault matrix
  (error, slow, empty, corrupted), the no-fault twin and the check that each
  fault fired, with the feature's experimental status. In
  `evaluation-design.md`: failure honesty, partial completion and recovery
  discipline as checks, usage against the twin, and NOT RUN for a fault that
  never fired. After the trial: where the injected delay runs and how to
  avoid waiting offline, a cut-off slow call as fired, the injected error's
  shape and warning, an exact-match sentinel, retry storms counted by error
  class against the bound, designed stops kept apart from abnormal ends,
  and a routing pointer.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- LLM steering as a gate: it lets the tool run when the judge errors, its
  judge is unpinned, and it sends every tool's arguments and results to a
  second model; its ledger is unbounded and shared across sessions.
- "You MUST follow this guidance immediately" as cancel text.
- After-model discard-and-retry, which ADK cannot express.
- Unseeded corruption effects, Strands' "Timeout" (a message, not a
  delay), model-output chaos (the scripted model already covers it), the
  three judges as gates, and any Strands code.

## Limits

Nothing was run; the rejection of `{}` is read from the validator. The
TypeScript steering code was not read.
