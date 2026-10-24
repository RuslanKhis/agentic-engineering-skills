# OWASP MCP Top 10 and CoSAI Workstream 4 compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [OWASP/www-project-mcp-top-10](https://github.com/OWASP/www-project-mcp-top-10)
at commit `165fe0f` (2026-07-29; beta, 2025 ids) and
[cosai-oasis/ws4-secure-design-agentic-systems](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems)
at `855cb05` (2026-10-15), cloned on 24 October 2026 into their own
directories and read.

**Licence.** OWASP's licence files disagree (CC BY-SA in `LICENSE.md`,
CC BY-NC-SA linked from the index), so the skills cite its ids with a link
and copy no text. CoSAI's documents are CC BY 4.0, approved papers also
under an OASIS notice, so they are paraphrased with attribution.

**Maintenance.** OWASP quiet (three months), still beta; CoSAI active.

**Conclusion.** The OWASP list gives reviewers ids to cite for MCP
boundaries; one id (MCP06) has a different title in the repository and on
owasp.org, so the skills cite ids, not titles. CoSAI's runbooks changed
three decisions: the tool-definition pin is checked only in CI or at
startup, so a remote server can change a description after deploy; ADK's
`tool_filter` runs on every listing, cache hits included, and receives the
live description, which makes a run-time pin practical. A bundled stdio
server shares the agent's container. And credentials should follow tool
tiers within one runtime.

## Method

The ADK behaviour behind the run-time pin was confirmed in google-adk
2.12.0's source (the original finding was on 2.8.0). One scenario case
covers the journey; the fresh-agent trial is in the
[testing record](../testing/owasp-mcp-cosai-ws4-alignment-2026-10-24.md).

## Drift corrected

None; the skills lacked the MCP ids and the run-time pin.

## Imported, by specialist

- **adk-agent-security.** The run-time pin as a hashing `tool_filter`
  predicate; stdio isolation; the ten MCP ids beside LLM, ASI and ATLAS ids
  in the checklist; the licence and MCP06 caution in the threat model; dated
  source entries. After the trial: the pin is checked once per invocation;
  the predicate admits a tool only when allowlisted and matching the
  manifest, with the field mapping to the inventory's `describe_tool`; a
  table, in this skill's own words, from finding to MCP id; a loopback fake
  server when the control lives in the toolset; and two new inspector rows
  (`mcp_filter_predicate_review`, `mcp_toolsets_without_prefix`).
- **adk-agent-interoperability.** `mcp_tool_inventory.py --fail-on-diff`
  (exit 3 on a rug-pull signal), and the manifest now pins `ui_resource_uri`
  and `ui_visibility` when a tool declares them (the diff compared them, but
  the manifest never wrote them).
- **adk-tool-auth-and-secrets.** Credentials chosen by tool tier in trusted
  code.

## Routed, not copied

The hidden-text checks (bidirectional controls and HTML comments in tool
descriptions) for the interoperability inventory are left as a helper
change of their own.

## Vendored assets

None.

## Left out, with reasons

- OWASP descriptions and checklists (licence).
- Response and message signing (no verification hook in `McpToolset`, no
  standard), the runbook's credential-reference tool parameter (weaker than
  keeping selectors out of model-visible arguments), trusted execution
  environments, the autonomy-rate example, the assurance-level table, the
  draft containment paper and the sanitisation notebooks.

## Limits

The stdio server's reach to the metadata server is an inference, not
tested.
