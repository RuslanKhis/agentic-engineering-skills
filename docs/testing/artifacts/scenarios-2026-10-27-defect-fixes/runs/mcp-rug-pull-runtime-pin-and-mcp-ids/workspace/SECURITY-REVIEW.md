# MCP security review: filings research agent

Scope: `app/agent.py`, `app/inventory.py`, `scripts/check_mcp_inventory.py`, `.github/workflows/ci.yml`, `Dockerfile`, `pyproject.toml`.
Framework: OWASP MCP Top 10 (beta, ids MCP01:2025 to MCP10:2025; ids cited, text not copied), with LLM03/ASI04 beside MCP03.
Evidence: everything here is `offline (source read)`. Nothing was executed (see "Not run").

## Answer to security: what if Ledgerline quietly changes a tool description after deploy?

**Before this change: the changed text reached the model with no check.**

- `tool_filter=["search_filings", "get_filing"]` matches on name only.
- `tool_list_cache_ttl_seconds=None` means `tools/list` runs on every `get_tools()`, so the new description is read live on the next model request. ADK does not subscribe to `notifications/tools/list_changed`, but with no cache it does not need to.
- CI (`mcp-inventory`) runs only on pull requests and a weekly cron (Monday 05:00). A change between runs is live for up to a week. A change on a quiet repo is not seen until the next PR or cron run, and the failed job blocks nothing that is already deployed.
- The CI check is also a test of the vendor's server from the CI runner. It does not test what the running agent was told.

**After this change: a changed tool is withheld at run time.**

- `tool_filter` is now `pinned_tool_filter(...)` (`app/inventory.py`). It admits a tool only if the name is allowlisted and the hash of its live `name`, `description` and `inputSchema` equals the committed manifest.
- The predicate runs on every `get_tools()`, cache hits included. ADK caches the filtered list for the rest of an invocation, so a change is seen at the next invocation.
- A mismatched tool is dropped and logged as a warning. This is fail-closed per tool.
- Cost: a legitimate vendor change takes that tool away from analysts until someone re-approves it by updating `mcp/ledgerline.tools.json`. That is intended.
- Limit: a matching hash proves the definition, not the server's behaviour. Ledgerline can still change what `get_filing` returns (see MCP06).
- Scope of the hash: `name`, `description` and `inputSchema` (parameter descriptions are inside the schema). `outputSchema`, `annotations` and `_meta` are not hashed. Annotations are hints, so this is acceptable. Revisit if you rely on `outputSchema`.

## Findings (OWASP MCP Top 10)

| # | Sev | MCP id | Finding | Where | Status |
|---|-----|--------|---------|-------|--------|
| 1 | High | MCP03 (LLM03, ASI04) | Rug pull: name-only filter, so a post-deploy description change reached the model; CI is periodic and off the runtime path | `app/agent.py:15`, `ci.yml:3-6` | Fixed in code; test written, not run |
| 2 | High | MCP02, MCP04 | The PDF server runs as a stdio child inside the agent container. It shares the container's filesystem, network and service-account identity, and plausibly the metadata server that mints the agent's token (an inference, not tested). It parses untrusted PDFs. | `app/agent.py:19-23`, `Dockerfile:6` | Open, needs an owner decision |
| 3 | Med | MCP03, MCP09 | `pdf_tools` has no `tool_filter`, so every tool that server lists is declared to the model. It has no definition pin either, so a `pdf-extract-mcp` upgrade can change tool text unreviewed. | `app/agent.py:19-23` | Open: tool names unknown here |
| 4 | Med | MCP04 | `pdf-extract-mcp==0.9.2` is version-pinned but not hash-pinned, and the image runs `pip install .` without `--require-hashes`. `mcp==1.18.0` is also pinned. | `pyproject.toml:9`, `Dockerfile:5` | Open |
| 5 | Med | MCP01, MCP07 | Static `Authorization` header is read from the environment at import and shared by all users and sessions; it is not issued per user. Whether Ledgerline scopes it to this agent is unknown. | `app/agent.py:13` | Open; use `header_provider` |
| 6 | Med | MCP06 | `get_filing` returns third-party filing text and PDFs return extracted text, both unfenced (ADK does not fence tool results). With the token, retrieval and an agent that can call two servers, this is the injection route. The agent has no write or egress tool today, which limits impact. | `app/agent.py` | Accepted for now; re-check before adding any write tool |
| 7 | Low | MCP08 | No audit record of tool calls. The new filter logs withheld tools only. | n/a | Open |
| 8 | Low | MCP09 | No server registry. The manifest covers Ledgerline only; the PDF server is an unrecorded dependency. | `mcp/` | Open |
| 9 | Low | MCP10 | Queries and filing ids go to a third party. Analysts' questions may be sensitive for Corrib Capital. | `app/agent.py` | Needs owner decision |
| 10 | Info | n/a | `Dockerfile` ran `COPY app` only, so the manifest was not in the image. Fixed with `COPY mcp ./mcp`. `CMD` references `app.server:app` but no `app/server.py` exists in this tree. | `Dockerfile:4,8` | Fix applied to COPY only; confirm where `server.py` lives |

## The local PDF server in the same Cloud Run container

- It is not a separate trust boundary: a compromise of the PDF parser (MCP02/MCP04) runs with the agent's identity and filesystem. The agent's own env vars do not reach it by default, because the `mcp` SDK passes only a small default environment to stdio children, but the metadata server is reachable.
- Preferred fix: run it as its own Cloud Run service with its own minimal service account, private ingress and Streamable HTTP, and call it with an ID token minted through `header_provider`. Alternative: keep it in the container, record it as holding the agent's identity, drop capabilities, use a read-only filesystem, and restrict egress. Owner: `deploy-adk-on-google-cloud`.
- Interim: add a `tool_filter` and a manifest for it once its tool names are known. Generate that manifest offline-safe from a trusted environment with `mcp_tool_inventory.py --command "pdf-extract-mcp --stdio" --out ...`. This executes the server, so do it in a throwaway container.

## Changes made

- `app/inventory.py`: added `pinned_tool_filter(recorded, allowed, log)`.
- `app/agent.py`: Ledgerline `tool_filter` is now that predicate, built from `mcp/ledgerline.tools.json`. It raises at import if the manifest is missing, so startup fails closed.
- `Dockerfile`: `COPY mcp ./mcp` so the manifest ships in the image.
- `tests/test_inventory.py`: 5 tests using fake tools (unchanged admitted, changed description withheld, changed parameter description withheld, unlisted-but-pinned withheld, new unpinned tool withheld).

## Assumptions (questions nobody could answer)

1. Q: Is `LEDGERLINE_TOKEN` scoped to this agent only? Assumed unknown and recorded as finding 5.
2. Q: What tools does `pdf-extract-mcp` 0.9.2 expose? Unknown; no filter invented.
3. Q: Is a withheld tool acceptable as an outage until re-approval? Assumed yes (fail closed).
4. Q: Where is `app/server.py`? Assumed it exists outside this checkout.
5. Assumed `McpTool.raw_mcp_tool` and `McpToolset` calling the predicate on each `get_tools()` behave as the vendored skill notes describe for google-adk 2.12.0 (source read by the skill author, 2026-10-24). I did not read the installed package, since it is not installed.

## Not run

- No tests, no inventory script, no `inspect_security_surface.py`: this session had no command-execution tool and no network. The new tests are unexecuted (`not run`). Run `python -m unittest discover -s tests -t .`.
- A parity check is still needed: confirm the runtime hash of `raw_mcp_tool.model_dump(by_alias=True, mode="json", exclude_none=True)` equals what `scripts/check_mcp_inventory.py` hashes (it uses `model_dump(exclude_none=True)`) for the same live tool, once the SDK is installed. A mismatch would withhold both tools.
- CI was not changed. Consider adding a nightly schedule or keeping the weekly one, as the runtime pin now carries the protection.
