# Using Google coding agents

*The same engineering skills, in Google's coding tools.*

**Gemini CLI** is Google's terminal coding agent. **Antigravity** provides a
coding app, IDE integrations and the `agy` CLI. They can read this collection's
existing `SKILL.md` packages and supporting resources.
[Gemini skills](https://geminicli.com/docs/cli/skills/),
[Antigravity skills](https://www.antigravity.google/docs/skills/).

These clients are where you ask for a code change. **Google's Agents CLI** is a
separate tool for scaffolding, evaluating and operating agent projects. You can
combine its skills with this collection inside a coding client; see the
[Agents CLI integration guide](agents-cli.md).

## Gemini CLI

### Install and discover

Install Gemini CLI and follow Google's sign-in instructions if you do not
already use it. The skills installer also needs the Node/Git prerequisites in
our [getting-started guide](../../README.md#getting-started).
[Official Gemini installation](https://geminicli.com/docs/get-started/installation/),
[authentication](https://geminicli.com/docs/get-started/authentication/).

From your application's project directory:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a gemini-cli
gemini skills list
gemini
```

The Skills CLI places the twelve complete packages in `.agents/skills/`.
Gemini discovers that shared directory. If this is a new project, use Gemini's
workspace-trust flow for a project you trust; untrusted project skills are not
loaded. Check `/skills list` in the session. After installing or changing skills,
use `/skills reload` or start a fresh session.
[Discovery](https://geminicli.com/docs/cli/skills/),
[workspace trust](https://geminicli.com/docs/cli/tutorials/skills-getting-started/).

<details>
<summary>Alternative: use Gemini's own installer</summary>

Choose this instead of the Skills CLI route for that scope:

```bash
gemini skills install https://github.com/RuslanKhis/agentic-engineering-skills.git --path skills --scope workspace
gemini skills list
```

For a local checkout:

```bash
gemini skills install /path/to/agentic-engineering-skills/skills --scope workspace
```

The native installer accepts the multi-skill directory and installs each package
under `.gemini/skills/`. Keep `--scope workspace` for a project installation;
user scope is the default. Complete its installation confirmation when shown.
[Native install command](https://github.com/google-gemini/gemini-cli/blob/main/packages/cli/src/commands/skills/install.ts),
[multi-skill installation](https://github.com/google-gemini/gemini-cli/blob/main/packages/cli/src/utils/skillUtils.ts).

Within a scope, Gemini gives `.agents/skills` precedence over `.gemini/skills`.
Use one installation route for a named skill so an older copy does not override
the one you just updated. [Precedence rules](https://geminicli.com/docs/cli/skills/).

</details>

### Ask for implementation

Type this in Gemini's chat:

```text
Use the adk-engineer skill to add memory so our support agent remembers a
user's preferred language across sessions. Keep our existing database and
dependency pins. Let the user change or forget the preference, and add
local tests that prove users cannot read each other's preferences.
```

Gemini selects the skill through its `activate_skill` tool. Follow the activation
prompt it shows. The router then selects `adk-memory-architecture` for the work.
`/skills` manages discovery and availability; installing this collection does
not create `/adk-engineer` as a Gemini command.
[Activation](https://geminicli.com/docs/tools/activate-skill/),
[skill usage](https://geminicli.com/docs/cli/using-agent-skills/).

Two direct specialist examples:

```text
Use the safe-api-tool-calls skill to repair this refund adapter. A timeout
may happen after the provider applies the refund. Preserve the public API
and add offline tests proving an uncertain result cannot trigger a second refund.
```

```text
Use the adk-agent-evaluation skill to test this ADK agent's tool choices and
results. Start with deterministic local tests and prepare a separate plan
for model-based evaluation.
```

## Antigravity app, IDE and CLI

Install your preferred Antigravity client using Google's
[app setup](https://www.antigravity.google/docs/getting-started/),
[IDE setup](https://www.antigravity.google/docs/ide/getting-started/), or
[CLI setup](https://www.antigravity.google/docs/cli/getting-started/).
From the application project, choose the corresponding installer target:

```bash
# Antigravity app or IDE integration
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a antigravity

# Antigravity CLI
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a antigravity-cli
```

Both project routes use `.agents/skills/`. If the collection is already installed
there for Codex, Gemini CLI or another Antigravity client, the project already
contains the shared packages. Open that same project and start a fresh session.
The natural-language requests above work as the documented way to request a
skill by name. [App discovery](https://www.antigravity.google/docs/skills/),
[IDE discovery](https://www.antigravity.google/docs/ide/skills/).

Antigravity 2.0 and its CLI also document named slash commands:

```text
/adk-engineer Add memory to this ADK agent. Keep our existing database and
include user-isolation and forget-preference tests.
```

In the CLI, run `agy` from the project and inspect `/skills`. Version 1.2.4 adds
`/skills reload`; restart earlier versions after changing files. IDE integrations
can use the by-name request above without assuming identical slash support.
[Google CLI walkthrough](https://codelabs.developers.google.com/antigravity/how-to-create-agent-skills-for-antigravity-cli),
[app slash commands](https://www.antigravity.google/docs/migration/workflows-to-skills/),
[CLI release notes](https://github.com/google-antigravity/antigravity-cli/releases/tag/1.2.4).

## Installation scope

Project installation is the tested common route. For Gemini CLI, add `-g` to
the Skills CLI command for all projects, or use `--scope user` with its native
installer. The existing Codex installation at `~/.agents/skills` is also a
Gemini discovery location; reinstalling it solely to create a second copy is
unnecessary. [Gemini directories](https://geminicli.com/docs/cli/skills/).

Antigravity documentation specifies these global directories for complete skills:

| Client | Documented global directory |
| --- | --- |
| Antigravity 2.0 app | `~/.gemini/config/skills/<name>/` |
| Antigravity for IDEs | `~/.gemini/antigravity/skills/<name>/` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/<name>/` |

[App](https://www.antigravity.google/docs/skills/),
[IDE](https://www.antigravity.google/docs/ide/skills/),
[CLI](https://www.antigravity.google/docs/cli/plugins/).

The tested Skills CLI 1.5.24 routes these targets' global installs to
`~/.agents/skills` through its shared-agent logic. We have not established that
all Antigravity clients read that user directory. Use the project commands above;
for a manual global installation, place each complete skill directory, including
its references and assets, in the directory documented for your actual client.
Do not flatten the files into one folder. See the
[installer evidence](../testing/google-coding-agents.md).

## Verification

The [Google compatibility check](../testing/google-coding-agents.md) records the
installer versions, source-file comparisons and native Gemini discovery results.
A subsequent [Antigravity IDE trial](../testing/google-client-generation.md) used
Gemini 3.8 Flash to load `safe-api-tool-calls`, repair a local adapter and pass
21 project tests plus nine independent checks. This is one specialist exercise;
the separate Antigravity app and CLI still need their own generation trials.
Gemini CLI generation was attempted but awaits sign-in. The earlier
[Claude Code and Codex trials](../testing/updated-skills-laptop.md) remain evidence
for those clients only.
