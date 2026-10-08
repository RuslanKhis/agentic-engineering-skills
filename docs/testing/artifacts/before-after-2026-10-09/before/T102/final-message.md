The agent now has read-only access to GitHub issues and Jira tickets through the two MCP servers, with each user's own token sent on every call. The tool names it allows are my guesses and haven't been checked against the real servers, and nothing that needs google-adk could run here.

**Specialist: `adk-agent-interoperability`, "Consume an MCP server" mode.** The ticket is about connecting to two remote MCP servers, which is exactly what that skill covers (`adk-engineer/SKILL.md:67`). It also covers the two requirements: "read-only" becomes a tool allowlist, and "tokens per user" becomes a per-request header built from session state. I didn't make `adk-tool-auth-and-secrets` the main skill because the tokens already exist and there was no sign-in or refresh work to do. I didn't load `adk-agent-security` because the ticket asks for the connection, not a threat review; there is one risk I've passed to it (below).

**What changed**
- **`support_agent/mcp_servers.py` (new):**
  - The server addresses, which can be overridden with environment variables.
  - The read-only tool lists.
  - Timeouts: 10 s to connect, 30 s to read.
  - A 5-minute cache of each server's tool list.
  - Code that adds `Authorization: Bearer` from `user:github_token` or `user:jira_token`.
  - A filter that offers only the listed tools, and hides a server's tools from users with no token for it. Each server only ever receives its own token.
- **`support_agent/agent.py`:** two MCP connections defined in the module itself, with tool names prefixed `github_` and `jira_`, added to `root_agent`. The `google-adk==2.8.0` pin is unchanged.
- **`tests/test_mcp_servers.py` (new):** 6 tests covering token isolation, different users, a missing token, write tools being blocked, and tools being hidden without a token.
- **`README.md`:** a short note on the new connections.
- **`REPORT.md`:** written with all seven sections you asked for.

**Checks**
- The 6 new tests pass. There's no pytest for Python 3.11+ on this machine, so I called the test functions directly on 3.13.
- The changed files compile under 3.11.
- **Not run:** `tests/test_tools.py` and anything else that imports google-adk, building the MCP connections for real, listing the servers' tools, and a live call. These need the package, network access or your approval.

**Still open**
1. **Tool names are guesses.** I used the public GitHub and Atlassian MCP naming. If the internal servers name them differently, those tools are silently hidden. `REPORT.md` has the commands (with `--header`) to list each server's real tools so you can fix the names before release; running them needs your OK.
2. **Security risk.** The root agent can now read untrusted issue and ticket text, it holds order data, and it can send email. A malicious issue could get it to email order data out. I recommend moving the GitHub and Jira tools into a separate read-only sub-agent, or adding a confirmation step before sending email.
3. **Not done:** tests against a fake MCP server, mentioning GitHub and Jira in the agent's instructions, and a possible deployment setting (`GOOGLE_API_USE_CLIENT_CERTIFICATE=false`).
4. **Assumptions in place of questions.** I recorded seven questions in `REPORT.md` with the answer I assumed for each. For example: tokens are plain strings minted for each server, and only the root agent gets the tools.

I rated the experience **3/5**. Picking the specialist and the core guidance were quick, but its checks assume a live server and an installed google-adk. The skills gave no next prompt for you to type.