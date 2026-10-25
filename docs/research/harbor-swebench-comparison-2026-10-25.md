# Harbor and SWE-bench compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [harbor-framework/harbor](https://github.com/harbor-framework/harbor)
at commit `6099b8c` (release v0.24.0 of 2026-10-05) and
[SWE-bench/SWE-bench](https://github.com/SWE-bench/SWE-bench) at commit
`02e7a74` (2026-09-02; PyPI 5.0.2), cloned on 25 October 2026 into their own
directories and read, never run.

**Licence.** Harbor Apache-2.0 (no NOTICE); SWE-bench MIT. Methods are
restated; nothing is copied. The Hugging Face dataset licences were not
checked and no data is used.

**Maintenance.** Harbor active; SWE-bench quiet. Terminal-bench now points
new users to Harbor, as the memo said.

**Conclusion.** Yes, narrowly. SWE-bench's two lists and its grading rule,
and Harbor's oracle and do-nothing runs, turn "failing before, passing
after" into a checkable contract for a regression case and for a ticket.
Harbor's directory format, Docker images and reward files are not needed:
ADK already has eval sets, case metadata and scripted-model fixtures.

## Method

`test_failed`, `compute_fail_to_pass` and `get_resolution_status` in
SWE-bench's grading module, and Harbor's oracle and do-nothing agents, were
confirmed in the snapshots before editing. One scenario case covers the
journey; the fresh-agent trial is in the
[testing record](../testing/harbor-swebench-alignment-2026-10-25.md).

## Drift corrected

None.

## Imported, by specialist

- **adk-agent-evaluation.** In `deterministic-tests.md`: `fail_to_pass` and
  `pass_to_pass` and the grading rule, stricter than SWE-bench on a skipped
  neighbour and an empty list. In `evaluation-design.md`: a base-commit run
  and a reference-fix run before a case is accepted, and four metadata
  fields.
- **adk-system-designer.** A `pass_to_pass` field in the ticket template,
  base-commit exit codes in the evidence, and one clause in the
  implementation hand-off. After the trial: one meaning for `pass_to_pass`
  across both skills, the base commit for an incident, what to do when the
  merged fix fails its neighbours (a reference fix to prove the test, the
  case left red, a ticket for the follow-up), a routing row for incidents,
  replay through the Runner instead of a faked tool context, and a
  network-guard recipe.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- From SWE-bench: a skipped `pass_to_pass` test counted as kept, XFAIL as a
  pass, the PARTIAL result, an empty `fail_to_pass` scored as 1, and
  prefix-matching of truncated test ids.
- From Harbor: the task directory, Docker and reward-file format, passing
  API keys to the verifier, and installing packages at grade time.

## Limits

Nothing was run; SWE-bench's collection pipeline was not read.
