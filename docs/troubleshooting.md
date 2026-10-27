# Updating and Troubleshooting

*Keep the installed skills current and find them when you need them.*

The collection is released as dated versions (`2026.10.25`, or
`2026.10.25.1` for a second release that day). Every skill carries the
version in its `metadata.version`, each release is tagged `v<version>` and
listed in the [changelog](../CHANGELOG.md), and the `stable` branch always points
at the latest release. When you use `adk-engineer`, it tells you in one line if
your installed skills come from different releases, or if a newer one is
published, with the command to update. It never updates anything itself.

**Plugin installs that follow releases.** Plugin installs receive releases,
not every commit to `main`:

| Coding agent | Install | Updates |
| --- | --- | --- |
| Claude Code | `/plugin marketplace add RuslanKhis/agentic-engineering-skills#stable`, then `/plugin install agentic-engineering@agentic-engineering-skills` | Turn on **Enable auto-update** for the marketplace under `/plugin` → Marketplaces, or run `/plugin marketplace update agentic-engineering-skills`; restart the session afterwards |
| Gemini CLI | `gemini extensions install https://github.com/RuslanKhis/agentic-engineering-skills --ref stable --auto-update` | Automatic with `--auto-update`, or `gemini extensions update agentic-engineering` |
| Antigravity app | Install the plugin from `https://github.com/RuslanKhis/agentic-engineering-skills` | The app updates installed plugins itself |

In Claude Code a plugin's skills carry its name as a prefix:
`/agentic-engineering:adk-engineer` rather than `/adk-engineer`. The prompts in
the README work after you add that prefix. Codex and the Antigravity CLI have
no documented automatic update for plugins, so on those use the Skills CLI and
the commands below. Pin a release tag if you want to choose when to move.

The [Skills CLI](https://github.com/vercel-labs/skills/blob/main/src/cli.ts)
can update installed skills. Choose the scope you used for installation:

```bash
# Update skills installed in the current project.
npx skills@latest update -p

# Or update skills installed for your user account.
npx skills@latest update -g
```

Each command updates installed skills in that scope, including other collections.
Keep any personal skill edits in version control before updating.

If a command is missing, confirm that you installed into the project you opened
and selected the correct coding agent, then restart its session.

**If you ever installed globally (`-g`), update that copy too.** In Claude Code a
skill installed for your user account takes precedence over a project copy with
the same name. An older global install therefore keeps serving old instructions
even after a fresh project install, and skills added since then appear while
older ones stay stale. This was observed on 9 October 2026 with Claude Code
2.1.294. Run `npx skills@latest update -g`, or remove the global copies, then
restart; a running session keeps the skill list it started with. To check what
a session actually loaded, ask it to quote the first words of `adk-engineer`'s
description: the current version begins "Help design, build, change or review", and its
`metadata.version` names the release. If the entry
skill reports a missing specialist, rerun the full-toolkit installation or
install the named specialist. If `npx` fails before showing the installer,
check `node --version` against the
[prerequisite](../README.md#1-install-the-skills).

<details>
<summary>Try local edits before publishing them</summary>

Clone this repository, then run the installer from a separate project directory,
passing the path to your clone:

```bash
npx skills@latest add "/path/to/agentic-engineering-skills" --skill '*'
```

Replace the example path with the real directory. This lets you try a changed
skill before it is available through the GitHub install command.

</details>

## How skill activation differs between clients

Claude Code supports `/name` for installed skills; Codex supports explicit
skill mentions using `$name`. See the respective
[Claude Code](https://code.claude.com/docs/en/skills) and
[Codex](https://developers.openai.com/codex/skills/) documentation.

Gemini CLI activates skills in response to the request; use `/skills list` to
check discovery and `/skills reload` after changes. Installing these skills
does not create `/adk-engineer` as a Gemini CLI command. Antigravity 2.0 and its
CLI also support named skill commands such as `/adk-engineer`; mentioning the
skill by name works across its app, IDE and CLI interfaces. Follow any
activation prompt the client shows.
[Gemini skill usage](https://geminicli.com/docs/cli/using-agent-skills/),
[Antigravity invocation](https://www.antigravity.google/docs/migration/workflows-to-skills/).

No separate setup command is needed for this toolkit. The skills inspect the
project's existing code and configuration when they run. Their descriptions also
allow a supporting coding agent to select them from a natural-language request;
an explicit command makes your intended skill clear.

## When a skill is wrong in your project

If a skill's instruction fails on your installed versions or keeps steering
you somewhere you override, `adk-engineer` records a short, redacted field
note on your machine and, at the end of the session, may ask once whether to
share it. Sharing opens a prefilled
[field report](https://github.com/RuslanKhis/agentic-engineering-skills/issues/new?template=field-report.yml)
form that you read and submit yourself; nothing is sent automatically.
`AES_FIELD_NOTES=off` turns it off. [What is never sent](field-feedback-privacy.md).
