# Snyk Agent Scan alignment — 23 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/agent-scan-comparison-2026-10-23.md).
In the repository: item 6 of the security skill's supply-chain reference
(install form, what the scan uploads, the local `inspect` mode, the CI exit
codes, the experimental-output caveat, the container-only rule) and an
optional maintainer scan in the testing guide. After the trial: the
invocation shape and configuration format read from the README with a CI
job sketch and the agent-command equality test, a checklist row for a
mandated scan, the heading no longer "optionally", one canonical pin format
named across the security and interoperability skills, the inspector's
below-3.11 exit documented, and the engineer's note that pytest collects
`unittest` classes. **One scenario case**
(`security-adopt-third-party-mcp-server-with-scan`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. No helper changed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or `mcp` installed, on a synthetic project, without the expected
answers; the scanner was not run and nothing was uploaded.

### Security: adopting a vendor's stdio MCP server with a mandated scan

The project: an ADK 2.12 agent with an unfiltered `McpToolset` over a
vendor's `npx` server, a container CI job, a Snyk token in secrets.

What the agent did: a nine-step adoption checklist with the scan as
evidence beside the allow-list, recorded definitions and hash pin; an
independent CI job pinned to `snyk-agent-scan@0.6.9` with `--ci`, the
container flag, exit codes mapped and a missing token as NOT RUN; a scanner
configuration holding exactly the agent's command with a test that parses
the agent module to keep them equal; eleven standard-library tests run on
the pin-meeting interpreter; the inspector run before and after (unchanged,
because the allow-list needs the vendor's tool list); a notes file saying
what the scan sends where and what is owed.

Ease rating: **4 of 5**. Routing and the facts were where the mode said;
the invocation shape and the CI gate shape had to be inferred.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The configuration argument and file format were not shown | Both stated from the README, labelled documented and confirmed on first run |
| No CI shape for a security scan; the one-server checklist had no scan row | A job sketch in item 6 and a checklist row |
| "Optionally" read wrong for a mandated scan | Heading reworded |
| Two pin formats for the same control across two skills | The inventory manifest named as the canonical form in both |
| A below-3.11 inspector run looked like evidence when redirected | The exit and stderr behaviour documented |
| Unittest-style advice versus a pytest CI job | One clause: pytest collects them |

## What this does not establish

The scanner was not run; the positional argument, the `uv` pin and the
vendor's tool list are confirmed on the first CI run.
