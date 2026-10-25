# Letting each host read the profile

The profile root sits outside every project, so each host needs one setting
before the flow skills can read it without a prompt per file, and another
before `remember` or `bind` can write. Give the user the lines for their host
(from `engineer.md`, or ask); apply nothing to their configuration yourself.
Checked against each host's documentation on 25 October 2026.

| Host | Read the root | Write the root | Notes |
| --- | --- | --- | --- |
| Claude Code | `"permissions": {"additionalDirectories": ["/Users/<you>/.agentic-engineering"]}` in `~/.claude/settings.json` (an absolute path), or `claude --add-dir ~/.agentic-engineering`, or `/add-dir` in a session | Edits follow the permission mode; approve each write, or add `Edit(~/.agentic-engineering/**)` to `allow` | Files in an added directory are readable without prompts; its CLAUDE.md is not loaded unless `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`, so keep that unset |
| Codex | `workspace-write`, the default mode, can read files; whether reads outside the workspace prompt was not stated | `[sandbox_workspace_write]` `writable_roots = ["/Users/<you>/.agentic-engineering"]` in `~/.codex/config.toml` (an absolute path) | Do not enable `[features] memories` for client facts |
| Gemini CLI | `gemini --include-directories ~/.agentic-engineering`, or `/directory add ~/.agentic-engineering` (disabled in restrictive sandbox profiles; use the flag) | Same directory once added; writes still ask for approval | Do not let the memory tool save client facts: it routes cross-project facts to `~/.gemini/GEMINI.md`, which loads everywhere |
| Antigravity | Untested; no documented setting for reading an arbitrary outside directory was found | Untested | Its global rules load in every workspace; do not put the profile there |

When `AGENTIC_ENGINEERING_HOME` points elsewhere, use that path in each
line. The environment variable must be visible to the coding agent's shell;
setting it in the shell profile that launches the agent is enough.

**A one-line pointer is the most that belongs in a host's global file**, for
example in `~/.claude/CLAUDE.md`: "Practice profile at
~/.agentic-engineering; read it only through the practice-profile rules."
Never copy profile content there: global files load in every project and
every session, for every client.

When the host refuses a read, the flow skills continue without the profile
and say so in one line; they never ask the user to paste the profile in.
