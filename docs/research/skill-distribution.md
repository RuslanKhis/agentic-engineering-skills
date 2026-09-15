# Skill distribution research

Checked against primary sources on 15 September 2026. This records the evidence behind the installation and usage guidance; upstream skill names and CLI requirements can change.

## Conclusion

The existing `skills/<name>/SKILL.md` layout already supports distribution through the Vercel Skills CLI. Keep the ADK specialists independently installable, add one `adk-engineer` entry point for people who do not know which specialist to choose, and document installation and invocation separately. Matt Pocock's collection can provide general engineering practices alongside the ADK expertise.

The repository's configured Git remote is `https://github.com/RuslanKhis/agentic-engineering-skills.git`. At the start of this investigation it contained 11 specialist skills and a short README without installation or invocation instructions. These are observations from this checkout, not claims about what has already been published on GitHub.

## Installation: what the CLI supports

The CLI accepts GitHub `owner/repo` sources and local paths. It discovers `skills/<name>/SKILL.md` and category layouts beneath `skills/`; a valid skill needs `name` and `description`. Installation defaults to the current project. `-g` selects the user's global location; `-a` selects agents; `--list` lists the source without installing; `--skill '*'` selects every skill. `--all` also selects every supported agent, so it is unnecessarily broad for the quickstart. [Vercel Skills CLI](https://github.com/vercel-labs/skills#readme)

```bash
# Discover the published collection.
npx skills@latest add RuslanKhis/agentic-engineering-skills --list

# Install the collection for Claude Code in the current project.
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a claude-code

# Install the collection for Codex in the current project.
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a codex

# Select two specialists for both agents.
npx skills@latest add RuslanKhis/agentic-engineering-skills \
  --skill adk-memory-architecture adk-agent-evaluation \
  -a claude-code codex
```

Multiple names after one `--skill` or `-a` are supported, as are repeated flags. `-y` bypasses interactive confirmations. These forms are implemented by `parseAddOptions`. [CLI argument parser](https://github.com/vercel-labs/skills/blob/main/src/add.ts)

The current upstream package, version `1.5.26`, declares Node.js `>=22.20.0`. Its package provides the `skills` executable; this repository does not need an npm package to be installed as a skill source. [Package manifest](https://github.com/vercel-labs/skills/blob/main/package.json)

In the default symlink mode, the installer copies each complete skill directory to `.agents/skills/<name>` and links agent-specific locations to that copy. Thus references and assets should stay inside their own skill directory. Project-level Claude Code uses `.claude/skills`; Codex uses `.agents/skills`. `--copy` instead creates separate copies. [Installer](https://github.com/vercel-labs/skills/blob/main/src/installer.ts), [agent locations](https://github.com/vercel-labs/skills/blob/main/src/agents.ts)

### Updating: do not treat `check` as read-only

The current CLI routes `check`, `update`, and `upgrade` to the same `runUpdate` function. Thus `npx skills check` is a legacy alias for the update flow, not a separate read-only check. Document `update` with an explicit scope so readers understand that it changes their installed files. [CLI dispatch](https://github.com/vercel-labs/skills/blob/main/src/cli.ts), [upstream README](https://github.com/vercel-labs/skills#skills-update)

Use `npx skills@latest update -p` for project skills or `npx skills@latest update -g` for global skills. With no names or scope flag, an interactive run asks for project, global, or both; with `-y` or no terminal, it selects project when project skills are detected, otherwise global. Supplying skill names without a scope flag searches both scopes. These scopes include other installed collections; they do not filter by this repository. [Scope resolver and option parser](https://github.com/vercel-labs/skills/blob/main/src/update.ts)

## Invocation is specific to the coding agent

| Host | Explicit use | Project discovery location |
| --- | --- | --- |
| Claude Code | `/adk-engineer Add memory to this agent` | `.claude/skills/<name>/SKILL.md` |
| Codex CLI / IDE | `$adk-engineer Add memory to this agent`, or select it through `/skills` | `.agents/skills/<name>/SKILL.md` |

Claude Code exposes local skills as slash commands and can also select them from their descriptions. A plugin introduces a namespace, such as `/plugin-name:skill-name`; ordinary skill installation preserves the short command. Keep directory names and frontmatter names consistent. [Claude Code skills documentation](https://code.claude.com/docs/en/skills)

Codex supports explicit skill mentions and implicit matching against descriptions. It follows symlinked skill folders and scans project and user `.agents/skills` locations. Restart if a new skill does not appear. OpenAI currently recommends plugins for reusable distribution, while standalone local skills remain supported. The cross-agent CLI is therefore a supported local installation route, with native plugin packaging a possible later distribution channel. [Official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills)

The examples above assume the proposed `adk-engineer` skill has been published and installed. They are prompts typed into the coding agent, not terminal commands. Installing these instructions does not install Google ADK, provision Google Cloud resources, or give the agent cloud credentials.

## What Matt Pocock does well

Matt's current repository offers a Claude Code marketplace plugin and editable installations through `npx skills@latest add mattpocock/skills`. Its README now asks users to install and run `setup-matt-pocock-skills` once per repository. The live collection differs from older README copies: it includes `ask-matt`, `grill-with-docs`, `to-spec`, `to-tickets`, and `implement`, alongside `tdd`, `diagnosing-bugs`, and `code-review`. [Matt Pocock's current README](https://github.com/mattpocock/skills#readme)

Three useful patterns:

- **An entry point:** `ask-matt` maps a user's situation to a workflow, so people need not memorize the catalog. Its routing instructions distinguish planning, implementation, debugging, and standalone tasks. [ask-matt](https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md)
- **Small, composable practices:** `tdd` defines behavior-oriented tests and incremental implementation, and calls `codebase-design` when interface design needs vocabulary. Its current workflow asks the user to agree test boundaries before writing tests. [tdd](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md)
- **Setup only where needed:** `setup-matt-pocock-skills` records tracker and document conventions that its engineering workflows use. That configuration belongs to Matt's collection; the ADK collection need not inherit it as a mandatory prerequisite. [setup skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md)

### Suggested composition for an ADK memory feature

This is a proposed combination, not an existing integration or an endorsement from Matt:

1. Use `grill-with-docs` to clarify the feature, retention expectations, and acceptance criteria.
2. Use `adk-engineer` or `adk-memory-architecture` for the ADK memory design and implementation constraints.
3. Use `tdd` for deterministic behavior such as user isolation, consent, and deletion, with `codebase-design` available if needed.
4. Use `adk-agent-evaluation` for retrieval quality and agent behavior, then `code-review` for the implementation diff.

Install Matt's collection separately and follow its setup guidance. Refer to installed skills by name in a normal prompt when combining them; avoid presenting multiple slash commands in one message as a portable command language. The ADK entry point should remain useful without Matt's collection.

For Matt's Claude Code plugin, the manifest name is `mattpocock-skills`, so the unambiguous command is `/mattpocock-skills:tdd` or `/mattpocock-skills:setup-matt-pocock-skills`. Current Claude Code also accepts the short name when it has no collision. Skills installed through the CLI use the ordinary `/tdd` and `/setup-matt-pocock-skills` commands. Choose one installation method for Matt's collection to avoid duplicates. [Matt's plugin manifest](https://github.com/mattpocock/skills/blob/main/.claude-plugin/plugin.json), [Claude Code command naming](https://code.claude.com/docs/en/skills#how-a-skill-gets-its-command-name)

## Local smoke-test procedure

Use a temporary project, an absolute path to this checkout, and explicit agent flags. The CLI's global state file supports `XDG_STATE_HOME`, which prevents the experiment from updating the real `~/.agents/.skill-lock.json`. [State-file implementation](https://github.com/vercel-labs/skills/blob/main/src/skill-lock.ts)

Run this with Node.js meeting the CLI's requirement, from this repository's root:

```bash
skills_source_dir="$PWD"
skills_test_dir="$(mktemp -d)"
mkdir -p "$skills_test_dir/project" "$skills_test_dir/state" "$skills_test_dir/npm-cache"
cd "$skills_test_dir/project"

XDG_STATE_HOME="$skills_test_dir/state" npm_config_cache="$skills_test_dir/npm-cache" \
  npx --yes skills@latest add "$skills_source_dir" --list

XDG_STATE_HOME="$skills_test_dir/state" npm_config_cache="$skills_test_dir/npm-cache" \
  npx --yes skills@latest add "$skills_source_dir" \
  --skill '*' -a claude-code codex -y
```

Check that all intended skills are listed, their files match the source, and the Claude Code links resolve to the temporary canonical copies. Repeat with a fresh temporary project and `--copy` if that mode is documented. This verifies packaging and installation; it does not establish that a model routes correctly or produces a working ADK feature. Those behaviors need separate realistic prompts in a fresh coding-agent session.

### Results from this checkout

The equivalent local-path checks were executed after `adk-engineer` was added, using the already cached Skills CLI **1.5.24** with the already installed **Node.js 24.15.0**. Fetching `skills@latest` into a temporary npm cache failed because the execution environment could not resolve `registry.npmjs.org` (`ENOTFOUND`); therefore the newer upstream version was inspected but was not the executable used in these tests.

| Check | Result |
| --- | --- |
| `add <local-repo> --list` | Passed; all 12 skills discovered |
| `add <local-repo> --skill '*' -a claude-code codex -y` | Passed; 12 installed skills, 166 source files identical, 12 valid Claude Code symlinks |
| `add <local-repo> --skill adk-memory-architecture -a claude-code codex -y` | Passed; only the selected skill installed, all 13 files identical |
| Same single-skill install with `--copy` | Passed; 13 identical files in each agent's separate directory |
| Run the installed memory inspector from outside its skill directory | Passed with Python 3.12.14 and `--dry-run`; zero project files read |

Each install used a new temporary project, temporary CLI state, and no global installation flag. File comparisons included the memory skill's references, inspector script, tests, license, and agent metadata. The tests establish distribution portability, not ADK runtime compatibility or model behavior.

### Entry-point and documentation checks

- The skill validator passed for `adk-engineer` and the updated `safe-api-tool-calls` package. All 12 Codex metadata files passed display-description and explicit-prompt checks.
- An independent agent walked through three bounded routing scenarios: a memory request with all specialists, the same request with only the entry skill, and memory implementation with Matt's `tdd` already active. It selected the memory specialist, handled the missing dependency explicitly, and preserved the chosen development process. These were routing walkthroughs, not full feature implementations or fresh client sessions.
- Temporary copied and symlinked layouts resolved the selected specialist's own references correctly. A router-only copy had no accidental dependency on the source checkout.
- New Markdown file links and editorial SVG paths resolve. The SVGs parse and render. A local HTML rendering of the README was visually inspected; images loaded and the page had no horizontal overflow at the checked desktop viewport. This was a local approximation of GitHub's Markdown presentation.
- `git diff --check` passed. Existing ADK runtime suites were not rerun because their implementation files were unchanged.

Remote installation can only pick up committed changes available on the selected GitHub ref. The local tests do not claim these edits are published.

Subsequent [Codex CLI generation checks](../testing/codex-cli-smoke.md) went
beyond installation and routing walkthroughs: three fresh coding sessions
generated and tested memory, refund-tool and ADK workflow implementations.
That report includes the prompts, generated code and independent acceptance results.
