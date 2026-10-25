# AppWorld and MCPMark compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [StonyBrookNLP/appworld](https://github.com/StonyBrookNLP/appworld)
at commit `42b5bcf` (2026-09-03) and [eval-sys/mcpmark](https://github.com/eval-sys/mcpmark)
at commit `cd45b7f` (2026-06-12), cloned on 25 October 2026 into their own
directories and read, never run. AppWorld's encrypted bundles are stored in
git-lfs and were never fetched, unpacked or decrypted.

**Licence.** MCPMark is Apache-2.0. AppWorld's public code is Apache-2.0;
its encrypted bundles carry an extra rule that redistribution must stay
encrypted, so they are link only. Methods are restated; nothing is copied.

**Maintenance.** Both quiet. MCPMark's last release (v1.2.0, 2025-09-20)
predates its server pins, so pin a commit, not the release.

**Conclusion.** The memo's "collateral-damage state tests" is right, and it
exposed a gap: the evaluation skill hashed "the relevant tables", so a
mutation in any other table passed. AppWorld also labels each assertion by
whether a do-nothing run passes it, which gives a cheap check against
vacuous cases. MCPMark's per-task verifiers and pass^k are already covered;
its lesson is version pinning of MCP servers, with one entry still on
`@dev`.

## Method

The diff functions, the ignore defaults, the `no_op_fail`/`no_op_pass`
labels, `scenario_goal_completion`, the MCPMark server pins and its README's
comparability statement were confirmed in the snapshots before editing. One
scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/appworld-mcpmark-alignment-2026-10-25.md).

## Drift corrected

- The end-state check hashed "the relevant tables"; it now diffs the whole
  fixture with a named ignore list.
- The tau2-bench note's claim that the hash "already fails an extra
  mutation", corrected in that note.

## Imported, by specialist

- **adk-agent-evaluation.** In `evaluation-design.md`: a whole-fixture diff
  at table, record and field level with named ignores, beside the
  effective-mutations rule; a do-nothing control through every case's
  graders. In `live-evaluations.md`: exact MCP server versions per entry, a
  server change as a new baseline. In `result-auditing.md`: the scenario
  score across variants beside the case score. After the trial: the
  end-state section rewritten as four numbered steps (replay, whole-fixture
  diff from the raw changes, effective mutations defined for ADK with the
  diff as the backstop for unlisted tools, and the gates, with ADK's
  abnormal endings and grading of what the agent had to communicate); a
  routing link to the do-nothing control; resolving and hashing server
  versions; a pinned example in the interoperability skill; and two
  version and log notes.

## Routed, not copied

- MCPMark changed 55 verifiers together with task text in one commit, which
  argues for hashing custom grader code with the eval set in
  `adk-release-engineering`; left for that skill's next review.

## Vendored assets

None.

## Left out, with reasons

- MCPMark running its verifier after an agent failure (a crashed run that
  reached the target state passes), its substring-matched retries that
  delete earlier output, and its silent skip of tasks without a verifier.
- Tag pins, weaker than this repository's exact-version and digest rule.
- AppWorld's state save and restore, and anything in its bundles.

## Limits

The code that assigns AppWorld's no-op labels is inside the encrypted
bundles; the procedure is inferred from the public evaluator and README.
