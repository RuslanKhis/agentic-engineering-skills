# agents-shipgate compared with this toolkit — 26 October 2026

## Scope and snapshot

A review of [ThreeMoonsLab/agents-shipgate](https://github.com/ThreeMoonsLab/agents-shipgate)
at commit `b980d4a` (2026-10-18), cloned on 26 October 2026 and read. The
published `agents-shipgate` 1.2.0 (PyPI, released 2026-10-01) was installed
in a throwaway Python 3.12 environment and run offline on two scratch git
repositories of ADK 2.12 agents written for the test, one change per
commit; nothing was pointed at this repository or a network target.

**Licence.** Apache-2.0, no NOTICE file.

**Maintenance.** Active, but 48 of the last 50 commits are by one
maintainer and its own maintainers file lists security intake, signing
custody and independent review as outstanding.

**Conclusion.** The memo's "cheap merge gate that diffs tool bindings" is
wrong as stated. `diff --application` is fast and compares function
bindings per agent from git objects, but it exits 0 whatever it finds and
says it "supplies no release verdict or merge permission". On the fixtures
it reported no change when `require_confirmation` or a
`before_tool_callback` was removed or an `McpToolset` filter widened, and
any `McpToolset` made the comparison partial. Its one addition is a digest
of each tool body with the hosts it calls. The toolkit's own security
inspector caught every change shipgate missed, so the gate the memo wanted
is now that inspector's `--compare` mode. Neither tool read an ADK 2.x
`Workflow` graph, where a function node that shells out was invisible to
both; the inspector now says so.

## Method

The spike recorded commands, version, outputs and exit codes for eleven
comparisons; the inspector was run on `git archive` trees of each base and
head. The inspector changes were then made and tested. One scenario case
covers the journey; the fresh-agent trial is in the
[testing record](../testing/agents-shipgate-alignment-2026-10-26.md).

## Drift corrected

- `inspect_security_surface.py` reported a project with a `Workflow` root
  as complete while a function node shelled out; it now names the graph's
  nodes (`workflow_graph_unread`) and marks the run partial.

## Imported, by specialist

- **adk-agent-security.** `inspect_security_surface.py --compare BASE_JSON`
  lists per-agent capability changes and exits 3, with tests; the
  validation reference describes the pull-request gate; `SKILL.md` names
  the `Workflow` limit.
- **adk-release-engineering.** In `ci-eval-gates.md`: the capability gate,
  and agents-shipgate as an optional advisory step with its exit codes and
  JSON fields.

After the trial: exit 3 now takes precedence over a partial run and the
output lists `unread_paths`, so a project with a `Workflow` does not fail
every pull request; the validation reference gives the CI steps (inspector
and gate run from the base commit, the skill vendored where the inspector
skips it, a code-owner label, NOT RUN on the bootstrap pull request); the
release reference adds shipgate's `verify` behaviour; and the release skill
routes to the capability gate.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- agents-shipgate as a gate, its `scan` manifest mode and `SHIP-ADK-*`
  checks, its host-config diff, and features not in a release.

## Limits

The unreleased object-binding reading, the `scan` mode and the GitHub
Action were not tested; the inspector still does not read what a
`Workflow` function node does.
