# REPORT — T-102 Connect the GitHub and Jira MCP servers

## 1. Skills invoked and reference files opened, in order

1. `adk-engineer` (invoked via `/adk-engineer`): `.claude/skills/adk-engineer/SKILL.md`
2. `.claude/skills/adk-agent-interoperability/SKILL.md` (primary specialist)
3. `.claude/skills/adk-agent-interoperability/references/mcp-consumption.md`
4. `.claude/skills/adk-agent-interoperability/references/compatibility.md` (first 70 lines)
5. `.claude/skills/adk-agent-interoperability/references/validation.md`
6. `.claude/skills/adk-tool-auth-and-secrets/SKILL.md` (supporting)
7. `.claude/skills/adk-agent-security/SKILL.md` (grep only) and `references/tool-supply-chain.md` (MCP rows, via grep)
8. Script: `.claude/skills/adk-agent-security/scripts/inspect_security_surface.py` (`--help`, then run)

Project files read: `tickets/T-102.md`, `README.md`, `pyproject.toml`,
`.github_workflows_ci.yml`, `support_agent/{__init__,agent,tools}.py`,
`tests/test_tools.py`, `tickets/T-101.md`, `tickets/T-103.md`.

## 2. Specialist chosen and why

**Primary: `adk-agent-interoperability`.** The ticket asks the agent to
consume two remote MCP servers. That skill's mode (b) covers the
`McpToolset` contract: connection params, `tool_filter`, `tool_name_prefix`,
`header_provider` and caching. The ticket names no `Primary skill`, so I
chose from the routing table row "Consuming or exposing MCP servers".

**Supporting:**
- `adk-tool-auth-and-secrets`, because the tokens are per user ("Keep tokens per user").
- `adk-agent-security`, because the agent already reads untrusted email and
  can send email and issue refunds. Adding more attacker-reachable text needs
  an allowlist and a lethal-trifecta check.

## 3. Files changed, and what is not finished

| File | Change |
| --- | --- |
| `support_agent/mcp_config.py` (new) | Has no google.adk import. Holds the URLs (env-overridable, defaults as given), the read-only allowlists `GITHUB_READ_TOOLS` / `JIRA_READ_TOOLS`, connect and read timeouts (10 s / 30 s) and the tool-list cache TTL (300 s). `bearer_header_provider(state_key)` reads `user:github_token` / `user:jira_token` from the session on every call. It raises `MissingUserToken` when the token is absent, so the request fails instead of going out without credentials |
| `support_agent/agent.py` | Adds module-level `github_toolset` and `jira_toolset`: `McpToolset` + `StreamableHTTPConnectionParams`, `tool_filter`, prefixes `github`/`jira`, `header_provider`, and no static auth headers. Adds `issue_tracker_agent`, a read-only sub-agent holding only those two toolsets. Registers it in `root_agent.sub_agents` with one routing sentence in the root instruction |
| `support_agent/__init__.py` | `root_agent` is now loaded lazily (PEP 562 `__getattr__`), so tests can import `support_agent.*` without google.adk, as `adk-engineer` asks. `support_agent.root_agent` still resolves |
| `tests/test_mcp_config.py` (new) | Checks that the allowlists contain only read tools and that endpoints use https. Checks that the header provider sends each user their own token, never sends one service's token to the other, and fails when the token is missing |
| `tests/test_agent_mcp.py` (new) | Needs the SDK (`importorskip("google.adk")`). Checks the toolset wiring, that no static Authorization header is set, and that write tools are filtered out |
| `README.md` | Documents the MCP boundary and recommends `GOOGLE_API_USE_CLIENT_CERTIFICATE=false` on 2.8.0 |
| `tickets/T-102.md` | Evidence section added |

**Not finished**
- The allowlisted tool names are assumptions based on the public GitHub and
  Atlassian MCP servers. They have not been checked against the internal
  servers' `tools/list`. No `mcp-manifest.json` is committed and there is no
  manifest-diff test.
- No fake-MCP-server tests yet for a normal result, `isError`, server down,
  server restart or a slow tool past `sse_read_timeout`.
- No adversarial cases (poisoned tool description or poisoned issue body).
- Pre-existing trifecta findings on `root_agent`, `triage_agent`,
  `billing_agent` and `refunds_agent` are untouched. They are out of scope
  for this ticket and belong to `adk-agent-security`.
- Residual risk: issue and ticket text returned by `issue_tracker_agent` can
  pass back into `root_agent`'s conversation after a transfer, and
  `root_agent` holds `send_email`.
- `close()` of the toolsets: `adk web` / `api_server` handle it. How the
  Cloud Run service starts its Runner is not in the repo, so this is not
  verified.
- Pins unchanged (`google-adk==2.8.0`). The specialist lists 2.10.0+ fixes
  that would help here, such as fenced MCP descriptions and rebuilding stale
  sessions. That upgrade is a decision for the owner, not something done here.

**Questions I would have asked (and the assumption I made)**
1. What are the exact tool names on the internal GitHub and Jira MCP servers? *Assumed public-server names; listed as placeholders to confirm.*
2. Were `user:github_token` / `user:jira_token` issued for these MCP servers' audience, or are they the users' upstream GitHub/Jira tokens? Forwarding an upstream token would be token passthrough. *Assumed they were minted for the MCP servers.*
3. If a user has not connected Jira (token missing), should the turn fail or should the agent explain? *Assumed fail closed, raising `MissingUserToken`. I did not verify how ADK 2.8.0 surfaces an exception raised from `header_provider` during `get_tools`. It may break the whole turn, including for users who only want GitHub.*
4. Should the lookups live on a separate sub-agent, or as tools on `root_agent`? *Chose a separate read-only sub-agent, so no write or send tools share a context with the new untrusted text.*
5. What are the measured latencies of the slowest tools? *Assumed 30 s read timeout.*
6. Who operates the servers, and may I list their tools with `--allow-remote`? *Not done: network is forbidden this session.*
7. The tokens sit in ordinary `user:` session state, which `adk-tool-auth-and-secrets/SKILL.md:39` advises against. Is moving them to a credential store in scope? *Assumed out of scope, because the ticket states that is where the tokens live.*

## 4. Checks run, and checks not run

**Run**
- `/opt/homebrew/bin/python3.11 /tmp/run_t102.py` calls each `tests/test_mcp_config.py` test function directly. Python 3.11 has no pytest, so the script substitutes a tiny stand-in for `pytest.raises`; it does not replace ADK. Result: **5 passed, exit 0**.
- `python3 -m pytest -q tests` on anaconda Python 3.9.13. Below the project's `>=3.11`, so this is indicative only. Result: **6 passed, 1 skipped** (`test_agent_mcp.py`, no google.adk).
- Syntax parse of `agent.py`, `__init__.py` and `test_agent_mcp.py` on 3.11: ok.
- `import support_agent` without google.adk on 3.11: ok (the lazy init works).
- `inspect_security_surface.py --project .` on 3.11: exit 1 (`partial`). The partial result comes from a malformed file inside `.claude/skills/...`, not from the project. `issue_tracker_agent` is flagged only as `untrusted_content_source` (MCP, expected) and **not** as `trifecta_present`. The trifecta findings at `agent.py` lines 18, 26, 37 and 87 are on agents that already existed.

**Not run**
- `tests/test_agent_mcp.py`: needs google-adk 2.8.0, which is not installed.
- `mcp_tool_inventory.py` against either server: remote, needs `--allow-remote` and owner approval, and network is forbidden this session.
- Fake-server Runner tests, a live `tools/list` and a read-only `tools/call`.
- CI (`pip install -e . pytest && pytest`): package install is not allowed.

## 5. Friction log

1. **Helpful:** the routing table at `.claude/skills/adk-engineer/SKILL.md:53-74` mapped the ticket to one row immediately. The "Specialist: <name>, because" line at `adk-engineer/SKILL.md:51` gave a clear first output.
2. **Unsure:** the ticket has no `Primary skill` (`adk-engineer/SKILL.md:34`), and two rows also apply: auth ("delegated OAuth") and security ("MCP supply-chain vetting"). The skill gives no tie-break rule for picking which supporting skills to load. I picked one primary and two supporting skills by judgement.
3. **Reference needed before useful work:** `adk-agent-interoperability/references/mcp-consumption.md` (213 lines). The constructor, header-merging and filter sections were essential. Reading it took two calls because tool output truncated the middle section.
4. **Assumed something I could not provide:** `adk-agent-interoperability/SKILL.md:45-60` and `references/validation.md:8-22` make the live inventory and a committed manifest the backbone of validation. No network was allowed, so there is no fallback path for "servers unreachable, tool names unknown". I had to invent the allowlist names.
5. **Did not fit:** `adk-agent-interoperability/SKILL.md:88-90` and `references/mcp-consumption.md:85` say to choose stdio locally and Streamable HTTP on Cloud Run via `K_SERVICE`. These servers are remote HTTP in every environment, so that rule did not apply. Not harmful, but it made me pause.
6. **Unsure:** the import paths for `McpToolset` / `StreamableHTTPConnectionParams` on 2.8.0 are not stated. The reference names file paths (`mcp-consumption.md:3-5`) but not the import line, so I inferred `google.adk.tools.mcp_tool.mcp_toolset` / `.mcp_session_manager`. A one-line import snippet would remove this guess.
7. **Unsure:** `tool_name_prefix` produces `github_<name>`, but the separator is not stated in `mcp-consumption.md:96-99` (only the example `pg_query`).
8. **Unsure:** `header_provider` behaviour when it raises is undocumented (`mcp-consumption.md:138-142`). That determines whether "fail closed" breaks every turn.
9. **Instruction assumed something absent:** `adk-engineer/SKILL.md:102` asks for Python 3.11+ for helpers. 3.11 exists here but has no pytest. The rule at `adk-engineer/SKILL.md:122` ("never imitate the SDK") made me careful to label my `pytest.raises` stand-in as not an SDK stand-in.
10. **Helpful but heavier than needed:** `adk-engineer/SKILL.md:119` (keep `google.adk` out of `__init__`). The repo's `__init__.py` violated this, and fixing it was necessary for any test to import.
11. **Friction:** `adk-agent-security/scripts/inspect_security_surface.py` takes `--project` (`adk-agent-security/SKILL.md:41`). My first call without it exited 2. The scan also walks `.claude/skills/**`, which adds about 10 irrelevant findings and marks the result `partial` because of a skill file. An exclude for `.claude/` would help.
12. **Contradiction to resolve by judgement:** `adk-tool-auth-and-secrets/SKILL.md:39` says to keep credentials out of ordinary ADK state, but the ticket and user put the tokens in `user:` state. I recorded this as a question instead of changing it.
13. **Unsure:** `adk-engineer/SKILL.md:40` says to "end with the run prompt for the next ready goal or ticket", but gives no template, and the tickets have no status or prerequisite fields to say which one is "ready".
14. **Helpful:** the evidence labels (`references/validation.md:63-71`) made the report structure obvious.
15. **Helpful:** the 2.8.0 mTLS/ADC note (`mcp-consumption.md:150-156`) was a real catch I would have missed. It led to the README recommendation.

## 6. Rating

**3 / 5.** Routing was fast and the MCP reference was precise. Most of the
friction came from validation steps that assume network access and live
servers, plus small missing API facts.

Three changes that would help most:
1. Add an **offline path** in `adk-agent-interoperability` validation for when the servers can't be reached: placeholder allowlist with a TODO, then a manifest-diff test that is skipped until a manifest exists, and a fake Streamable HTTP server fixture to copy.
2. Add **exact import lines and a minimal per-user `McpToolset` snippet** (prefix separator, `header_provider` error behaviour) to `mcp-consumption.md`.
3. Make `inspect_security_surface.py` **exclude `.claude/`** by default, and give the next-ticket prompt in `adk-engineer` a literal template.

## 7. Next prompt the skills told the user to type

None given. `adk-engineer/SKILL.md:40` says to end with "the run prompt for
the next ready goal or ticket" but supplies no wording. My suggestion, which
does not come from the skills, is:
"Please take ticket tickets/T-101.md and carry it out."
