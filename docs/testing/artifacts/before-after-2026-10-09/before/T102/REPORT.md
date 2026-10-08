# REPORT — T-102 Connect the GitHub and Jira MCP servers

## 1. Skills invoked and reference files opened (in order)

1. Skill `adk-engineer` (invoked by the user via `/adk-engineer`) — `.claude/skills/adk-engineer/SKILL.md`
2. `.claude/skills/adk-agent-interoperability/SKILL.md` (primary specialist, read from the sibling directory)
3. `.claude/skills/adk-agent-interoperability/references/mcp-consumption.md` (mode b)
4. `.claude/skills/adk-agent-interoperability/references/compatibility.md` (SKILL.md:37 says read before quoting behaviour)
5. `.claude/skills/adk-agent-interoperability/references/validation.md`
6. Grep only (not full reads): `adk-tool-auth-and-secrets/SKILL.md` + `references/*.md` for header_provider / token audience; `adk-agent-interoperability/references/evaluation-across-boundaries.md` for the MCP fake-server table.

Not opened: `topology.md` (validation.md:49 points there for the contract-table format; I wrote the table below from SKILL.md:111-113), `selection.md`, `assets/interop-review-checklist.md`, `adk-agent-security` (its inventory script, SKILL.md:31-34).

## 2. Specialist chosen and why

**Primary: `adk-agent-interoperability`, mode (b) "Consume an MCP server".** The ticket is about consuming two remote MCP servers, which matches the router row at `adk-engineer/SKILL.md:67`. The interop skill covers `McpToolset`, `tool_filter`, `tool_name_prefix` and `header_provider`. That is the whole change: read-only means a filter, and per-user tokens mean a header provider.
Not chosen as primary:
- `adk-tool-auth-and-secrets`: the tokens already exist in state, so there was no OAuth lifecycle work (consent, refresh, disconnect) to do. That remains its deferred concern.
- `adk-agent-security`: the ticket asks for wiring, not a threat model. The security risk is flagged below for that skill to handle.

## 3. Files changed / not finished

| File | Change |
| --- | --- |
| `support_agent/mcp_servers.py` (new) | URLs (env-overridable), state keys, read-only allowlists, timeouts, cache TTL, per-user `Authorization` header providers, `tool_filter` predicates that allow only allowlisted tools **and** hide a server's tools when the user has no token for it. No google.adk import, so it is testable without the SDK. |
| `support_agent/agent.py` | Two `McpToolset`s built at module level with `StreamableHTTPConnectionParams` (timeout 10 s, read timeout 30 s), `tool_name_prefix` `github` / `jira`, `header_provider`, filter, `tool_list_cache_ttl_seconds=300`; added to `root_agent.tools`. The `google-adk==2.8.0` pin is unchanged. |
| `tests/test_mcp_servers.py` (new) | 6 tests: each server gets only its own user's token; different users get different headers (and so separate pooled sessions); missing, empty or `None` context sends no `Authorization`; write tools rejected; tools hidden without a token. |
| `README.md` | 5-line note on the new boundaries and env overrides. |

Boundary contract (SKILL.md:111-113):

| | GitHub MCP | Jira MCP |
| --- | --- | --- |
| Input | allowlisted read tools only: `get_issue`, `list_issues`, `search_issues`, `get_issue_comments` (model sees `github_*`) | `getJiraIssue`, `searchJiraIssuesUsingJql` (model sees `jira_*`) |
| Output | MCP `CallToolResult` as JSON (`content`, `structuredContent`, `isError`) | same |
| Identity | caller's `user:github_token`, Bearer, per request through `header_provider`; never shared via `connection_params.headers` | caller's `user:jira_token`, same |
| Timeout | connect 10 s; read 30 s | same |
| Failure | ADK 2.8.0 graceful handling returns `{"error": ...}` to the model; no retry of `tools/call` | same |
| Consumer | `support_root` (LLM) | same |
| Coverage | unit tests of header/filter logic (local); fake-server tests **not written** | same |

**Not finished:**
- **Tool-name manifest.** I did not run `mcp_tool_inventory.py --url ... --allow-remote --out` against either server: no network, and SKILL.md:55-57 requires owner approval. The allowlist names are assumptions, so a wrong name silently hides that tool.
- **Fake-server tests** (normal, `isError`, server down, restart between calls, slow tool) were not written. They need `google.adk` to drive `McpToolset`, which cannot run here.
- **Agent instruction.** `root_agent`'s instruction does not mention GitHub/Jira yet. I left it unchanged; that is deferred to `adk-agent-instructions`.
- **mTLS env var.** `GOOGLE_API_USE_CLIENT_CERTIFICATE=false` is not set. mcp-consumption.md:150-156 says ADK 2.8.0 may offer ADC to non-Google hosts when mTLS is configured. This is a deployment decision for `deploy-adk-on-google-cloud`; it is likely inert on Cloud Run without client certs.
- **SECURITY RISK, deferred to `adk-agent-security`.** `root_agent` now reads untrusted text (issues and tickets, on top of inbound emails), holds private data (orders) and can act externally (`send_email`). That combination is the lethal trifecta. A malicious issue body could steer the agent to email order data out. Recommend moving the MCP toolsets to a quarantined read-only sub-agent, or gating `send_email`.

**Questions I would have asked (assumed answers in brackets):**
1. What are the exact tool names on the internal servers? [github-mcp-server and Atlassian Rovo MCP naming]
2. Are the tokens in `user:github_token` / `user:jira_token` access-token strings minted for each MCP server's audience, or credential dicts? [strings with the correct audience; anything else is treated as absent]
3. Which agent should get the tools: root only, or triage too? [root only]
4. Should a user without a linked account be told to connect it, or just not see the tools? [just hidden]
5. Are there SLA/timeouts for the servers, and which tool is the slowest? [10 s connect / 30 s read, matching the httpx 10 s elsewhere]
6. Is a 5-minute tool-list cache acceptable given ADK ignores `list_changed`? [yes]
7. Do the servers also need a stdio/local variant for dev? [no, remote HTTP only; I deviated from the K_SERVICE pattern at SKILL.md:86-90]

## 4. Checks

| Check | Result | Evidence label |
| --- | --- | --- |
| `python3.13 -I` run of every `test_*` in `tests/test_mcp_servers.py` (pytest not installed for 3.11+) | 6/6 PASS, exit 0 | Local |
| `python3.11 -m py_compile` agent.py, mcp_servers.py, test file | OK | Local |
| `python3 -m pytest` (system 3.9) | collection error: `str \| None` needs 3.10+; project requires >=3.11, so not a real failure | Local (wrong interpreter) |
| `tests/test_tools.py` and anything importing `support_agent` package (imports google.adk) | **Not run**: google-adk not installed | Not run |
| Import/construct `McpToolset` objects on google-adk 2.8.0 | **Not run** | Not run; constructor kwargs are source-verified per mcp-consumption.md:11-25 |
| `mcp_tool_inventory.py` manifest/diff against both servers | **Not run** (network forbidden, needs approval) | Not run |
| Fake-server tests | **Not written / not run** | Not run |
| Live `tools/list` + one read-only `tools/call` | **Not run** (needs approval) | Not run |

Commands still needed (after approval):
```bash
python .claude/skills/adk-agent-interoperability/scripts/mcp_tool_inventory.py --url https://mcp-github.internal.example/mcp --header "Authorization=Bearer <reviewer's github token>" --allow-remote --out mcp-github-manifest.json
python .claude/skills/adk-agent-interoperability/scripts/mcp_tool_inventory.py --url https://mcp-jira.internal.example/mcp --header "Authorization=Bearer <reviewer's jira token>" --allow-remote --out mcp-jira-manifest.json
```
Then replace the assumed names in `GITHUB_READ_TOOLS` / `JIRA_READ_TOOLS` with the reviewed read-only names, and commit both manifests.

## 5. Friction log

- **Helpful:** the router table at `.claude/skills/adk-engineer/SKILL.md:67` mapped "consuming MCP servers" to one specialist without ambiguity.
- **Helpful:** `.claude/skills/adk-agent-interoperability/SKILL.md:95-99` and `references/mcp-consumption.md:126-142` say exactly where a per-user token goes (`header_provider`, not `connection_params.headers`) and why (pool key at mcp-consumption.md:50-56). This was the core design decision of the ticket, settled in two paragraphs.
- **Helpful:** the constructor sketch at `references/mcp-consumption.md:11-25` let me write the wiring without the SDK installed.
- **Unsure / assumed something I couldn't provide:**
  - `.claude/skills/adk-agent-interoperability/SKILL.md:45-60` and `references/validation.md:6-22` build validation around running the inventory script against the live server. With no network and no approval, there was no fallback path. That left the biggest open question unanswered: what to put in the `tool_filter` list (SKILL.md:91-94).
  - The example commands at SKILL.md:49-53 don't show the script's `--header K=V` flag (`scripts/mcp_tool_inventory.py:583`). Authenticated servers need it, and I only found it by grepping the script.
- **Didn't fit:** `.claude/skills/adk-agent-interoperability/SKILL.md:86-90` and `references/mcp-consumption.md:80-87` prescribe choosing stdio vs HTTP by `K_SERVICE`. That does not apply to company-hosted remote servers, and I had to decide on my own to deviate.
- **Reference I had to read before useful work:** `references/compatibility.md` (SKILL.md:37 says read it "before quoting any behaviour"). It is 64 lines, mostly A2A and later-version rows irrelevant to a pinned 2.8.0 MCP consumer; only the mTLS row mattered.
- **Heavier than needed:** `references/validation.md:39-51` wants fake-server tests per row plus a contract table in topology.md's format (another file) for a two-toolset read-only ticket. The "minimum per boundary" is clear, but it cannot be met without the SDK, and there's no guidance for splitting SDK-free logic so part of it is testable. I worked that out myself.
- **Gap:** the `adk-tool-auth-and-secrets` references (grep across them) never mention MCP `header_provider` or the case where tokens already sit in `user:` state. So "Keep tokens per user" is owned by two skills, and neither covers this case end-to-end.
- **Unsure:** `.claude/skills/adk-engineer/SKILL.md:47` says to add a second skill only when the change crosses its boundary. The ticket brushes three (interop, auth, security), and it was unclear whether to load the security skill for the trifecta risk. I flagged it rather than loading it.
- **Environment friction (not the skills):** the system `python3` is 3.9 without the `|` union syntax, and no 3.11+ interpreter has pytest. I ran the test functions with a small direct harness.

## 6. Rating

**3 / 5.** Routing and the core MCP-consumption guidance were quick and precise. Validation and inspection assume a live server and an installed SDK.

Three changes that would most help:
1. **Add an offline path to the interop SKILL.md (Inspect step 4 / Validate).** When the server can't be queried, it should say: write the allowlist from vendor documentation, mark it unverified, and make the manifest command a release blocker.
2. **Cover remote-only HTTP servers alongside the K_SERVICE stdio/HTTP pattern,** plus a short recipe for "per-user token already in `user:` state → `header_provider` + token-gated `tool_filter`" with an SDK-free unit test layout.
3. **Show `--header` for authenticated servers in the SKILL.md:49-53 examples,** and add a one-line trifecta check pointer for "read untrusted content + root agent has write tools" so the security hand-off is explicit.

## 7. Next prompt the skills told the user to type

None given. The only literal command the skills supply is the conditional install command at `.claude/skills/adk-engineer/SKILL.md:88` (`npx skills@latest add RuslanKhis/agentic-engineering-skills --skill <specialist-name>`). It applies only when a specialist is missing, and none was.
