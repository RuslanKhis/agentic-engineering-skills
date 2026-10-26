# spec-kit, OpenSpec, Conductor and HumanLayer compared with this toolkit — 26 October 2026

## Scope and snapshot

A review of [github/spec-kit](https://github.com/github/spec-kit) at commit
`67e0f72` (2026-10-23; v1.2.3), [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
at `6d04a1b` (2026-10-24; v1.15.0), [gemini-cli-extensions/conductor](https://github.com/gemini-cli-extensions/conductor)
at `6e8f9a8` (2026-09-01) and the HumanLayer command files in
[humanlayer/humanlayer](https://github.com/humanlayer/humanlayer), cloned on
26 October 2026 and read, never run. HumanLayer removed `.claude/commands`
from main on 2026-10-22 (`d8197ba`); the files were read at their last
version, commit `77c7fe9` (2025-11-12), which is the commit cited.

**Licence.** spec-kit and OpenSpec MIT; Conductor and HumanLayer
Apache-2.0. Only methods are restated.

**Maintenance.** spec-kit and OpenSpec active; Conductor quiet (its release
tag v0.4.1 disagrees with its `VERSION` file, 0.3.0); HumanLayer active, but
the commands the memo linked are gone from main.

**Conclusion.** Most of the memo's proposal is already in the system
designer: `parallel_safe`, `touches`, contract deltas, the automated and
manual verification split, per-ticket commit evidence and status rules were
adopted earlier from the memo without citing these sources. One real gap
remained: nothing in the designer re-read the code before a phase gate,
which only read the tickets. Both spec-kit's `converge` and OpenSpec's
`verify` re-inspect the code because "completion claims are not evidence".
Two smaller gaps: a withdrawn contract was recorded but not proved gone, and
nothing stopped an agent ticking a manual check for the person.

## Method

`converge.md`'s gap categories, `verify-change.ts`'s severities, its
"not verified" rule and its removed-requirement check, Conductor's phase
base commit and HumanLayer's manual confirmation were confirmed in the
snapshots before editing. One scenario case covers the journey; the
fresh-agent trial is in the
[testing record](../testing/spec-tools-alignment-2026-10-26.md).

## Drift corrected

None.

## Imported, by specialist

- **adk-system-designer.** In `checkpoint.md`: the phase gate reads the
  code in two halves (a base-commit diff checked against every ticket's
  `touches`, and a fresh-context read-only review graded CRITICAL, WARNING
  or SUGGESTION), and a withdrawn contract proved absent by a `SHALL NOT`
  item. In `plan_status.py`: `--gate --base <commit>`, with a test. In the
  ticket template: `withdraws` in `contract_deltas` and the manual-item
  evidence line.
- **adk-engineer.** In `ticket-lifecycle.md`: a manual item is recorded only
  on the named person's confirmation.

After the trial: a shipped `assets/code-review-prompt.md` for the
judgement half; the gate now checks that a withdrawn contract has its
`SHALL NOT` item and that manual checks name a person and date, and no
longer requires the presentation goal it precedes (a contradiction in the
existing gate); the checkpoint steps written as a numbered list; and the
"nothing ready" prompt points to the gate and the review.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- Conductor's automatic commit per task and its `git notes`: the person
  commits in this toolkit.
- Anything that writes to tasks (spec-kit's `converge` appends to
  `tasks.md`), spec-kit's four-level severity scale, OpenSpec's RENAMED
  delta, and installing any of the tools.
- New top-level spec documents.

## Limits

Nothing was run; the read-only review's grading is a prompt pattern, not a
measured check.
