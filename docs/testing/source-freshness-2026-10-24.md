# Source freshness report — 24 October 2026

## What changed

`scripts/check_source_freshness.py` reports whether each external repository
this toolkit cites is still maintained. It reads
`docs/research/source-register.json` (44 sources at the start: every
repository the dated comparison notes and the external-collections review
prompt cite, with the commit read where the note recorded one, the read date,
the licence GitHub reported on 24 October 2026, the note, and the skills whose
files mention the repository), asks the GitHub REST API read-only questions,
and prints a band per source. The external-collections review prompt now
starts from this report and adds a register row for every new source;
CONTRIBUTING asks for the row as evidence.

Bands use days since the last commit on the default branch: active up to 30,
quiet up to 365, stale beyond. Both numbers are placeholders for a maintainer's
judgement and are arguments, not policy.

## Offline evidence

`tests/test_check_source_freshness.py`, 14 tests with a fake GitHub keyed by
request path: active, quiet and stale bands and their boundaries; archived,
renamed and relicensed repositories; a pinned commit GitHub no longer has; a
missing repository; an unpinned source that skips the comparison; a rate limit
that marks the remaining sources unchecked without further calls (exit 3); a
server error reported as unchecked, not clean; JSON output and `--only`; seven
invalid registers and three invalid arguments that exit 2 without a fetch;
`--validate-only` without a fetch; and the repository's own register validated
on every run of `scripts/check_repo.py`.

## Live run

`GH_TOKEN=$(gh auth token) python3 scripts/check_source_freshness.py` on
24 October 2026 checked all 44 sources and exited 0: 38 active, 6 quiet
(agentdojo 144 days, dbos-google-adk 159, longmemeval 166, atlas-data 44,
agents.md 44, agentskills 76), none stale, archived, renamed, relicensed or
missing a pinned commit. Every abbreviated pinned commit resolved through the
compare endpoint. Sources with the most commits since our read: pydantic-ai
155, copilotkit 87, ag-ui 47, langchain-docs 47, ms-agent-framework 43,
docling 37, agent-sandbox 32, adk-python 31.

The run surfaced new releases since our reads that are candidates for the
review prompt and were not acted on in this change: google-adk v2.13.0
(23 October 2026; the skills cite 2.12.0), tau2-bench v2.0.0 (20 October),
promptfoo 0.125.0 (23 October; spiked on 0.124.1) and mcp-toolbox v1.15.0
(23 October; read at v1.14.0).

## Limits

The report measures activity, not quality or correctness: an active
repository can still change a fact we cite, which is what "since read" and the
review prompt are for. Sources that are not GitHub repositories (Google
documentation pages, the Kiro format, papers) are not in the register and stay
with the review prompt. An unauthenticated run is limited to 60 requests an
hour, enough for about 15 sources.
