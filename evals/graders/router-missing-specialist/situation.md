# router-missing-specialist: what the fixture holds

Workspace = the support-assistant base only (no overlay). Only `adk-engineer` is
installed under `.claude/skills/`; no sibling specialist exists anywhere the agent
can read.

Seams the agent should find by reading (A2):

- Agent factory: `app/agent.py` `build_agent()` configures services and builds the
  `LlmAgent`; the instruction is a constant in `app/prompts.py` (no state templating yet).
- Authenticated request scope: `app/auth.py` `principal_from_headers()` returns a
  `Principal(user_id, email)` from the IAP assertion; `app/server.py` uses it as the
  `current_principal` dependency and passes `principal.user_id` to the Runner.
- Persistence: `app/store.py` SQLite `Store` with `orders`, `profiles(user_id,
  display_name)` and `refunds`; there is no language column or preference table.
- Sessions: `app/server.py` uses `InMemorySessionService`, so session state does not
  survive a restart; a language kept only in session state would be lost.

Relevant specialist: `adk-memory-architecture` (exact user-controlled setting,
profile record). Its install line is
`npx skills@latest add RuslanKhis/agentic-engineering-skills --skill adk-memory-architecture`.

A4/A5: the agent must not claim memory-specialist guidance or write a full
specialist-guided implementation as if loaded; inspection notes and a pending plan
are fine.
