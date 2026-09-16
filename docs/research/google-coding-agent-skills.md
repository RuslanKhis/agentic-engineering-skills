# Google coding agents: skill compatibility

**Checked:** 16 September 2026. **Method:** current official documentation and Google-maintained source. Commands below are documented recipes; this research did not authenticate a client, activate a model or generate code.

## Recommendation

Keep the existing `skills/<name>/SKILL.md` packages and their supporting directories. Google clients support this format. For a project used by several clients, install each complete package under `.agents/skills/<name>/`; avoid an extra enclosing repository directory. Document invocation separately for each client. No Google-specific rewrite of the engineering instructions is needed for discovery. This is a packaging recommendation based on the documented loaders, not evidence of equivalent generated-code quality. [Gemini skills](https://geminicli.com/docs/cli/skills/), [Google's Antigravity CLI codelab](https://codelabs.developers.google.com/antigravity/how-to-create-agent-skills-for-antigravity-cli).

## Discovery paths

Paths below contain individual `<name>/SKILL.md` packages, including their assets and references.

| Client | Project directory | User directory |
| --- | --- | --- |
| Gemini CLI | `.agents/skills/` or `.gemini/skills/` | `~/.agents/skills/` or `~/.gemini/skills/` |
| Antigravity 2.0 app | `.agents/skills/` | `~/.gemini/config/skills/` |
| Antigravity for IDEs | `.agents/skills/` | `~/.gemini/antigravity/skills/` |
| Antigravity CLI (`agy`) | `.agents/skills/` | `~/.gemini/antigravity-cli/skills/` |

Gemini gives project skills precedence over user skills; within a scope, `.agents/skills` takes precedence over `.gemini/skills`. Updating a lower-precedence duplicate can therefore leave the active copy unchanged. [Gemini discovery rules](https://geminicli.com/docs/cli/skills/).

Antigravity's app, IDE and CLI documentation specifies different global directories. The app and IDE also retain the older project `.agent/skills/` path. Prefer the shared project path in the quick start. The CLI plugins page uses a flat Markdown example, but Google's codelab explicitly demonstrates the standard nested `SKILL.md` layout. [App skills](https://www.antigravity.google/docs/skills/), [IDE skills](https://www.antigravity.google/docs/ide/skills/), [CLI skills](https://www.antigravity.google/docs/cli/plugins/), [CLI codelab](https://codelabs.developers.google.com/antigravity/how-to-create-agent-skills-for-antigravity-cli).

## Gemini CLI

The native installer accepts a repository subdirectory containing several skills. The implementation discovers that directory's skills and copies each complete package. Run this from the agent project:

```bash
gemini skills install https://github.com/RuslanKhis/agentic-engineering-skills.git --path skills --scope workspace
gemini skills list
```

For a local checkout, supply its `skills/` directory directly:

```bash
gemini skills install /path/to/agentic-engineering-skills/skills --scope workspace
```

Native installs target `.gemini/skills/` at project scope; omitting `--scope workspace` selects user scope. Installation replaces an existing same-name destination. Use one installation method per scope to avoid competing copies. [Installer command](https://github.com/google-gemini/gemini-cli/blob/main/packages/cli/src/commands/skills/install.ts), [installation implementation](https://github.com/google-gemini/gemini-cli/blob/main/packages/cli/src/utils/skillUtils.ts).

Inside Gemini CLI:

```text
/skills list
/skills reload
Use the adk-engineer skill to add memory to this ADK agent. Implement it locally and include offline tests.
```

`/skills refresh` aliases reload. `/skills enable <name>` and `/skills disable <name>` control availability. The model selects a matching skill and calls `activate_skill`; the documented user flow is a relevant request followed by activation consent. Installing a skill does not create a documented `/<skill-name>` command in Gemini CLI. [Managing skills](https://geminicli.com/docs/cli/using-agent-skills/).

If discovery fails, check the exact `SKILL.md` filename, leading YAML frontmatter with `name` and `description`, and one package-directory level below the discovery root. Workspace skills require a trusted workspace; `/trust` and a restart address that condition. Installation consent and activation consent are separate. [Getting started and troubleshooting](https://geminicli.com/docs/cli/tutorials/skills-getting-started/), [consent model](https://geminicli.com/docs/cli/using-agent-skills/).

## Antigravity

Copy or install complete packages into the project's `.agents/skills/`, then open that project in the desired client. Google's CLI tutorial starts `agy`, verifies discovery with `/skills`, and asks a relevant question. Its published permission prompt must be handled when shown. [Official CLI tutorial](https://codelabs.developers.google.com/antigravity/how-to-create-agent-skills-for-antigravity-cli).

The CLI and Antigravity 2.0 app document direct `/<skill-name>` invocation, so `/adk-engineer` is appropriate there. The IDE skill page explicitly documents mentioning the skill by name; the natural-language Gemini example above therefore also works as the documented IDE interaction pattern. [CLI invocation](https://www.antigravity.google/docs/cli/plugins/), [app invocation](https://www.antigravity.google/docs/migration/workflows-to-skills/), [IDE activation](https://www.antigravity.google/docs/ide/skills/).

In `agy`, `/skills` lists loaded skills. Version **1.2.4** adds `/skills reload`; restart earlier clients after installation. Version **1.1.12** added optional `disable-slash-command: true` frontmatter, which hides a skill from `/name` invocation while retaining model discovery. This repository does not need that flag. [CLI command reference](https://www.antigravity.google/docs/cli/reference/), [1.2.4 release](https://github.com/google-antigravity/antigravity-cli/releases/tag/1.2.4), [official changelog](https://github.com/google-antigravity/antigravity-cli/blob/main/CHANGELOG.md).

The reviewed Antigravity pages document copying standalone skills and installing **plugins** with `agy plugin install`; they do not establish a standalone `agy skills install` command. This repository is a skill collection, so a plugin installation example would require separate packaging. [CLI extensibility](https://www.antigravity.google/docs/cli/plugins/).

## Evidence boundary

Documentation supports format and command compatibility. A successful installer or `skills list` check establishes placement and discovery; it does not establish correct activation, reference loading or generated implementation. The earlier [laptop validation](../testing/updated-skills-laptop.md) records Claude Code and Codex runs. Google-client runtime claims require their own recorded versions and results. No minimum Gemini release supporting every feature above was established; check an installed client's version and help before applying current documentation to an older release.
