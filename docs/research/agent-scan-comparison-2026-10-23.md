# Snyk Agent Scan compared with this toolkit — 23 October 2026

## Scope and snapshot

A review of [snyk/agent-scan](https://github.com/snyk/agent-scan) (formerly
invariantlabs-ai/mcp-scan) at commit `73c0966` (2026-10-21), cloned on
22 October 2026 into its own directory and read on 23 October, never run.
Code licence Apache-2.0; use of the scanning service is under Snyk's terms
(`TERMS.md`). Files read: `README.md`, `docs/cli-reference.md`,
`docs/failure-codes.md`, the risk names in `README.md`. The published
package is `snyk-agent-scan` 0.6.9 on PyPI (2026-10-20); the README says no
npm package exists.

**Conclusion.** The memo's caveats are the facts that matter and they are now
beside the decision: the scanner uploads configurations, tool names and
descriptions and skill content to Snyk's API under Snyk's terms (secrets
redacted), it executes configured stdio server commands to read their tools,
its output schema is declared experimental, and `--ci` exits 1 when risks or
operational failures remain. So the security skill names it as optional,
pinned evidence beside the allow-list, recorded definitions and hash pin,
with `inspect` as the local no-upload mode and the container-only rule for
CI; the testing guide names an optional maintainer scan of the packages as a
choice, not a check. The programme's rule stood: the scan was documented,
not run, because running it uploads content.

## Method

README and CLI reference read for the commands, flags, exit codes and
data-handling statements; each placed at the adoption decision with the
commit, the version and "documented, not run". One scenario case covers the
journey; a fresh-agent trial is recorded in the
[testing record](../testing/agent-scan-alignment-2026-10-23.md).

## Drift corrected

- The memo's "14 risk types and a `--ci` flag" holds for v0.6; the v0.5 line
  (issue codes, planned for deprecation) is left out.
- The memo did not note `inspect`, the local mode without analysis, nor
  that `--ci` must be paired with `--dangerously-run-mcp-servers` in
  non-interactive use.

## Imported, by specialist

- **adk-agent-security.** Item 6 of the supply-chain reference.
- **Maintainer docs.** The optional scan in the testing guide.

## Routed, not copied

Nothing; a tool invoked by its pinned name.

## Vendored assets

None.

## Left out, with reasons

- The enterprise push-key and control-server paths: platform operation.
- The risk and failure code tables: experimental by the vendor's own
  statement; only names appear.
- Running the scan on the toolkit's own packages: uploads content;
  recorded as the maintainer's choice.

## Limits

Documented, not run; exit codes come from the vendor's CLI reference, not
from observation, and are labelled so.
