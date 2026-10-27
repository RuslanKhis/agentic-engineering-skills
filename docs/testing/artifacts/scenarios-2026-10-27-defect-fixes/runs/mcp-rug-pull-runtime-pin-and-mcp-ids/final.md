If Ledgerline quietly changes a tool description after you deploy, the old setup passed the new text to the model unchecked. I've changed the agent so a changed tool is now dropped at run time. I couldn't run any tests or scripts, so none of this is verified.

**Why it was exposed.** The `tool_filter` list matched tools by name only. With `tool_list_cache_ttl_seconds=None`, the agent re-lists tools on every model request, so a changed description would reach the model on the next turn. The CI inventory check only runs on pull requests and a weekly cron. A change could therefore be live for up to a week before anything flagged it, and CI never blocks a deployment that already exists.

**What I changed.**
- **Runtime pin:** `app/inventory.py` has a new `pinned_tool_filter`, and `app/agent.py` now uses it for Ledgerline. It admits `search_filings` and `get_filing` only if the live name, description and input schema hash to the values in `mcp/ledgerline.tools.json`. A mismatched tool is withheld and logged.
- **Re-approval:** A legitimate vendor change means that tool is unavailable until someone updates the manifest. I assumed that outage is acceptable.
- **Image fix:** `Dockerfile` now copies `mcp/` into the image, because the manifest wasn't shipping.
- **Tests:** Five new tests in `tests/test_inventory.py` use fake tools. They cover unchanged tools, a changed description, a changed parameter description, a tool that isn't allowlisted, and a new unpinned tool.

**Findings.** `SECURITY-REVIEW.md` has the full write-up against the OWASP MCP Top 10. The main ones:
- **MCP03 (rug pull):** fixed in code, as above.
- **MCP02 and MCP04 (PDF server):** the PDF server runs inside the agent's container and parses untrusted PDFs. It shares the container's filesystem, network and identity. Moving it to its own Cloud Run service with its own service account is the better fix, and it needs your decision.
- **MCP03 and MCP09 (no PDF filter or pin):** the PDF toolset has no `tool_filter` and no definition pin. I don't know its tool names, so I didn't invent a filter.
- **MCP04 (dependency pins):** `pdf-extract-mcp` is version-pinned but not hash-pinned.
- **MCP01 and MCP07 (shared token):** the Ledgerline token is a static header shared by all users. A `header_provider` would fix that.
- **MCP06 (injected content):** filing and PDF text comes back unfenced. Impact is limited today because the agent has no write or egress tools.
- **Lower findings:** MCP08 (no audit log), MCP09 (no server registry) and MCP10 (queries going to a third party).

**Left undone.**
- I had no command-execution tool and no network, so I ran no tests, inventory script or inspector. Run `python -m unittest discover -s tests -t .` before merging.
- Once the SDK is installed, check that the runtime hash matches what `scripts/check_mcp_inventory.py` computes for the same live tool. A mismatch would withhold both tools.
- I assumed ADK 2.12 runs the filter on every `get_tools()` and exposes the live definition as `raw_mcp_tool`. That comes from the bundled skill notes, not from reading the installed package.
- I did not change CI, the PDF server's isolation, the token handling, or the hash pins.
- `Dockerfile` starts `app.server:app`, but there is no `app/server.py` in this checkout. I assumed it lives elsewhere.