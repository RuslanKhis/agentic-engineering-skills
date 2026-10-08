The agent can now read GitHub issues and Jira tickets through the two MCP servers, read-only and with each user's own token. Nothing has been tried against the real servers yet, and the ADK test hasn't run because google-adk isn't installed.

**Specialist: `adk-agent-interoperability`**, because the ticket is about connecting the agent to remote MCP servers. That skill covers the connection settings, the list of allowed tools and per-user credentials. I also used two supporting skills:
- **`adk-tool-auth-and-secrets`**, because tokens must stay per user.
- **`adk-agent-security`**, because the agent already reads untrusted email and can send email and issue refunds.

**What changed**
- **`support_agent/mcp_config.py` (new):** the two server URLs, a list of allowed read-only tools per server, timeouts and a 5-minute cache of the server's tool list. Each request reads that user's token from `user:github_token` or `user:jira_token`. If the token is missing, the call fails instead of going out without credentials. This file doesn't import google.adk, so it can be tested here.
- **`support_agent/agent.py`:** one tool connection per server (tool names get `github_` / `jira_` in front) on a new `issue_tracker_agent`. That agent has only these read tools, nothing that sends or refunds. It is added to `root_agent`, with one routing sentence in its instruction.
- **`support_agent/__init__.py`:** now loads `root_agent` only when it's first used, so tests can import the package without google.adk. `support_agent.root_agent` still works.
- **Tests:** `tests/test_mcp_config.py` (no ADK needed) and `tests/test_agent_mcp.py` (skipped without ADK).
- **Also updated:** a README note, an Evidence section in `tickets/T-102.md`, and `REPORT.md`.

**Checks**
- **Run:** the new config tests passed 5/5 on Python 3.11, called directly because 3.11 has no pytest here. `pytest tests` on Python 3.9 gave 6 passed, 1 skipped; 3.9 is below the project's 3.11 minimum, so treat that as a rough check.
- **Security scan:** the skill's scanner does not flag the new agent as able to both read untrusted text and send data out. It does flag that on four agents that already existed, including `root_agent`; I left those alone as outside this ticket.
- **Not run:** the ADK wiring test, listing the real servers' tools (needs network and the server owners' approval), fake-server tests, and any live call.

**Assumptions to confirm**
- **Tool names:** the allowed tool names are guesses taken from the public GitHub and Atlassian MCP servers. Check them against the internal servers' tool lists before release.
- **Token audience:** I assumed the stored tokens were issued for these MCP servers. If they are users' ordinary GitHub/Jira tokens, forwarding them breaks MCP security rules.
- **Missing token:** I don't know how ADK 2.8.0 handles the "token missing" failure. It may break the whole turn, even for a user who only wants GitHub.

The full list of questions, the remaining risks and the friction log (with pointers into `.claude/skills/...`) are in `REPORT.md`. I rated the experience 3/5. The skills gave no exact next prompt; my own suggestion is "Please take ticket tickets/T-101.md and carry it out."