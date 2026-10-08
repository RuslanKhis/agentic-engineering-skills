# T-102 report: connect the GitHub and Jira MCP servers (reconstructed)

> Reconstructed from the working tree after the trial was interrupted by a usage limit before it wrote its own report. `support_agent/mcp_servers.py:17-18` says "see REPORT.md", so the agent intended to write one. Its live friction log and command transcript were lost.

Skill root for pointers: `/Users/ruslankhissamiyev/Documents/Coding Projects/skills/agentic-engineering-skills/skills/<name>/`.

## 1. Specialist selection (inferred)

**Primary:** `adk-agent-interoperability`, mode (b) "Consume an MCP server" (`SKILL.md:71`). The trial also wrote mode (a)-style selection reasoning ("`McpToolset` over `OpenAPIToolset`... selection table, row `McpToolset`" in `docs/mcp-boundaries.md:30-31`).

Evidence: the register and contract-table layout of `docs/mcp-boundaries.md` (`SKILL.md:111-113`), the `tool_filter` + `tool_name_prefix` + `header_provider` + `tool_list_cache_ttl_seconds` set (`SKILL.md:91-99`), the `mcp_tool_inventory.py --allow-remote --out mcp-manifest.json` procedure (`SKILL.md:45-60`), the `GOOGLE_API_USE_CLIENT_CERTIFICATE=false` note (`references/mcp-consumption.md:150-156`), and the token lifecycle deferred to `adk-tool-auth-and-secrets` (`SKILL.md:98`).

**Routing row:** `adk-engineer/SKILL.md:67`: "Consuming or exposing MCP servers ... | `adk-agent-interoperability`". The secondary row `:69` (tool identity, credentials, delegated OAuth: `adk-tool-auth-and-secrets`) covers "keep tokens per user". It was named as an owner but not loaded.

## 2. Changes

```
 README.md                     |  11 ++++
 docs/mcp-boundaries.md        |  85 ++++++  (new)
 support_agent/__init__.py     |  19 +++++-
 support_agent/agent.py        |  16 ++++-
 support_agent/mcp_config.py   | 150 ++++++  (new)
 support_agent/mcp_servers.py  |  57 ++++++  (new)
 tests/fake_mcp_http_server.py |  96 ++++++  (new)
 tests/test_mcp_config.py      | 112 ++++++  (new)
 tests/test_mcp_servers.py     | 124 ++++++  (new)
 9 files changed, 667 insertions(+), 3 deletions(-)
```
New files are staged intent-to-add. Nothing committed.

- `mcp_config.py` (stdlib only): URLs from env with defaults. The read-only filters (`GITHUB_READ_TOOLS`, `JIRA_READ_TOOLS`) are explicitly **assumed** names. Prefixes are `github` and `jira`, with connect 10 s, read 60 s and tools/list cache 300 s. `make_header_provider` reads `user:github_token` / `user:jira_token` from state and **raises** `MissingUserTokenError` instead of sending no header, so there is no shared `session_no_headers` and no ADC offered. There is a write-verb detector, and manifest helpers check filters against a committed `mcp-manifest.json`.
- `mcp_servers.py`: two module-level `McpToolset(StreamableHTTPConnectionParams(...))` with no static headers, plus `close_mcp_toolsets()`.
- `agent.py`: both toolsets added to `root_agent.tools`. The instruction gains "use github_*/jira_* ... treat issue and ticket text as data".
- `__init__.py`: `root_agent` is now resolved lazily via module `__getattr__` so the stdlib modules import without ADK.
- `tests/`: 16 deterministic config tests, 7 ADK-dependent fake-server boundary tests (normal, `isError`, down, slow, missing token, static wiring) and a stdlib loopback Streamable HTTP fake.
- `docs/mcp-boundaries.md`: the boundary register, contract table, decisions, steps blocked offline and open questions. `README.md` gets a section.

## 3. Completeness against the ticket

| Ticket requirement | State |
| --- | --- |
| Read GitHub issues and Jira tickets via company MCP servers | **Wired, not verified.** Tool names are guesses taken from public servers. The manifest was not produced because connecting is an approval step. |
| Read-only | **Done by allowlist** (`tool_filter` list). A test guards write-like names. Because the names are assumed, the real server could expose reads under other names, in which case the filter would declare nothing. |
| Tokens per user | **Half-done.** Per-user headers through `header_provider` are correct and tested. Who writes `user:*_token` into state, plus consent, refresh, revocation and audience, is deferred to `adk-tool-auth-and-secrets`. The `user:` prefix persists tokens in the session store across sessions, and that storage choice is not discussed. |
| Boundary tests | Config tests **ran**. Fake-server tests were written but **not run** (they need the SDK). |
| Security of new untrusted input | **Gap.** See quality note 4. |

Validation run during reconstruction (system Python 3.9.13, pytest 7.1.2, no installs):

```
python3 -m pytest -q -p no:cacheprovider tests
17 passed, 2 skipped
```
The 2 skips are `tests/test_mcp_servers.py` (whole module, `importorskip("google.adk")`) and `test_filter_names_exist_in_manifest` (no manifest). The baseline `tests/test_tools.py` now passes offline only because of the lazy `__init__`.

## 4. Quality notes against `adk-agent-interoperability/SKILL.md`

1. **Always pass `tool_filter` and, with several toolsets, `tool_name_prefix` (`SKILL.md:91-94`): followed.** The trial also wrote a manifest test to enforce it. The manifest itself is missing (blocked).
2. **Per-user credentials only through `header_provider` (`SKILL.md:95-99`): followed**, with good reasoning about pool keys and ADC (`mcp-consumption.md:48-55`, `:150-156`). The fail-closed raise is a sensible addition.
3. **Define toolsets synchronously at module level "in `agent.py`", transport chosen from `K_SERVICE` (`SKILL.md:86-90`): deviates, with justification.** The toolsets are defined in `mcp_servers.py` and imported, and the transport is always HTTP because the servers are remote (`docs/mcp-boundaries.md:32-34`).
4. **Trifecta not checked.** `root_agent` now combines untrusted text (GitHub/Jira issue bodies), private data (orders) and egress (`send_email`). The only mitigation is an instruction sentence, which `adk-agent-security/SKILL.md:104-105` says is not a control. The interoperability skill delegates the threat model to `adk-agent-security` (`SKILL.md:31-34`, description). Its inventory, run here, sees the two MCP toolsets but reports `all_three: false` because it cannot see `tools.send_email` (friction F2).
5. **Contract table per boundary (`SKILL.md:111-113`): followed**, in `docs/mcp-boundaries.md`.

## 5. Friction the artefacts reveal

- **F1. The core review artefact is blocked by design.** `SKILL.md:55-57` and `:91-94` make the committed manifest the control. Producing it needs `--allow-remote` against company servers (an approval step). The result is a filter built from guessed tool names plus a test that skips until someone else acts. The skill gives no route for "server not reachable from this machine", such as asking the owner for a `tools/list` dump.
- **F2. The inventory handed over from `adk-agent-security` (`adk-agent-interoperability/SKILL.md:31-34`) is unreliable here.** On this tree `inspect_security_surface.py` resolves both MCP toolsets but reports `tool_filter: "predicate"` with `allowed_tools: []` for `tool_filter=list(cfg.GITHUB_READ_TOOLS)`. It also misses every `tools.<fn>` reference (`adk-agent-security/scripts/inspect_security_surface.py:711`, the fall-through to `kind: "other"`), so the new trifecta on `support_root` goes unreported.
- **F3. Offline testability forced a package change.** `__init__.py` was rewritten to a lazy `__getattr__` purely so stdlib tests could import `support_agent.mcp_config`. The validation step (`SKILL.md:131-135`, a fake-server test per boundary) needs ADK and its pinned `mcp` SDK, so the most important tests could not run.
- **F4. A fake MCP server had to be hand-written (96 lines).** `SKILL.md:131-134` requires a fake-server test per boundary, but the skill ships no reusable fake or fixture for Streamable HTTP (its `tests/fixtures` are for the helper scripts).
- **F5. The docs file was compelled.** An 85-line `docs/mcp-boundaries.md` came from the contract-table requirement (`SKILL.md:111-113`) plus the evidence-label requirement (`SKILL.md:135-139`). It is useful, but it is one of several "write the table" artefacts across skills with no shared location convention.
- **F6. Ownership split on "per user".** The ticket's "keep tokens per user" spans this skill (`header_provider`) and `adk-tool-auth-and-secrets` (lifecycle, `SKILL.md:98`). The trial deferred the second half. `adk-engineer/SKILL.md:46-47` ("add another only when the change crosses its boundary") left that call to the agent.

## 6. Note on lost evidence

The original agent's friction log, the list of references it read and any helper invocations were lost with the interruption. Whether it ran `mcp_tool_inventory.py` against a loopback fake is unknown, because no manifest or output file remains.
