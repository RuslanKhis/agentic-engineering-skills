# google/mcp and Google's managed MCP servers compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [google/mcp](https://github.com/google/mcp) at commit
`9ebafd6` (2026-08-17; Apache-2.0), cloned on 24 October 2026 into
its own directory and read, never run, checked against Google Cloud's
documentation: the MCP overview and supported-products pages (last updated
2026-10-22), "Control MCP use with IAM" (2026-10-22) and "Use the BigQuery
MCP server" (2026-10-21), each fetched and re-read on 24 October 2026.

**Maintenance.** Quiet: no commit for more than two months. The README calls
the repository demonstration material and lists 16 servers against the
official page's much longer list, so the skills cite the official page with
its date and not the repository.

**Conclusion.** The memo's "list of managed remote MCP servers" is right as a
pointer and wrong as a source; and the repository takes no position that
managed servers should be preferred over self-hosting, which the memo
implied. What changes decisions is in the official pages: Google runs two
kinds of remote MCP server and only the Google Cloud kind is governed by
IAM; IAM can make those servers read-only at the platform; and BigQuery's
server caps query time and result rows, which affects whether an answer is
complete. The interoperability and SQL skills now carry these, and the SQL
skill states when to choose the managed server and when Toolbox.

## Method

Every fact was taken from the official pages and re-read verbatim before
editing (the deny condition text, the `tools/list` behaviour under a deny,
the enforced permission, the limits and the "can't use IAM" sentence). One
scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/google-mcp-alignment-2026-10-24.md).

## Drift corrected

- The SQL skill's managed-server paragraph lacked the platform read-only
  control and the row and time caps.

## Imported, by specialist

- **adk-agent-interoperability.** "Google's managed remote MCP servers": the
  two kinds, IAM and `roles/mcp.toolUser` for the Google Cloud kind, no IAM
  control for the others (so `tool_filter` and egress policy are the only
  gates), endpoint forms, and the instruction to take the list from the
  official page.
- **adk-sql-agent-engineering.** The IAM deny on
  `mcp.googleapis.com/tools.call` with the read-only condition, paired with a
  `tool_filter` because `tools/list` still returns write tools; the
  three-minute and 3,000-row caps and the truncation check; the separate
  agent identity; and the managed-versus-Toolbox decision.

## Routed, not copied

None; Google's product skills for these services are already routed from
the skills.

## Vendored assets

None.

## Left out, with reasons

- The repository's example ADK code: it mints a token once and sends it as
  a static header (which expires), sends a Maps key in a header where
  platform identity is offered, and pins google-adk 1.28.0.
- `gcloud beta services mcp enable` from its setup scripts, which the
  current documentation does not mention.
- The list of open-source servers: a directory, not a decision; adoption
  review belongs to `adk-agent-security`.

## Limits

No Google endpoint was called; the IAM behaviour is documented, not
observed.
