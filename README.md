<p align="center">
  <img src="docs/editorial/cover.svg" alt="Agentic Engineering Skills — The skills companion. An architectural ink drawing of connected agents, on warm paper." width="100%">
</p>

<p align="center">
  <a href="#getting-started">Getting started</a> ·
  <a href="#the-skills">The skills</a> ·
  <a href="#using-these-with-matt-pococks-skills">Working with Matt's skills</a> ·
  <a href="#about-the-book">About the book</a>
</p>

# Agentic Engineering Skills

<p>
  <sub>
    <a href="https://github.com/google/adk-python">Google ADK</a> ·
    <a href="https://cloud.google.com/">Google Cloud</a> ·
    <a href="https://agentskills.io/">Agent Skills</a> ·
    <a href="LICENSE">MIT licensed</a>
  </sub>
</p>

Practical skills for building agent applications with Google's **Agent
Development Kit (ADK)** and **Google Cloud Platform (GCP)**. They accompany
**Agentic Engineering: Building Production-Grade Multi-Agent Systems with
Google ADK on GCP** by Ruslan Khissamiyev.

A **skill** is a folder of instructions, references and, where useful, helper
scripts that your coding agent can read while working on your project. These
skills help it apply the book's engineering practices to your own application:
handle failed tool calls, add memory, connect a browser interface, test agent
behaviour, or prepare a deployment.

Start with one command and describe the change you need:

```text
/adk-engineer I need to add memory to my Google ADK agent.
```

That is the Claude Code form. In Codex, use `$adk-engineer` with the same request.
The entry skill selects the relevant specialist and follows its workflow through
the requested work. You can also call a specialist directly.

You do not need the book or its example repository to use the skills. Install
them in the project you want to work on. They guide your **coding agent**;
your application's ADK agents do not load them automatically.

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## Getting Started

*Install the toolkit, open your project, and ask for a useful change.*

### 1. Install the skills

You need a coding agent that supports skills, Git, and Node.js **22.20 or later**
with npm, which provides `npx`. This is the current requirement of the
[Skills CLI](https://github.com/vercel-labs/skills/blob/main/package.json).
The installer downloads the skill files; it does not require Google Cloud
credentials or install ADK into your application.

From your application's project directory, run:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*'
```

This selects **all twelve skills**: `adk-engineer` and the eleven chapter
specialists. Choose your coding agent when prompted. The default installation
belongs to the current project. Keep the quotes around `'*'` so your shell
passes it to the installer unchanged.

To select a particular coding agent explicitly, use one of these commands:

```bash
# Claude Code
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a claude-code

# Codex
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a codex
```

The existing `skills/<name>/SKILL.md` layout is supported by the
[Skills CLI](https://github.com/vercel-labs/skills#readme). Each specialist brings
its own references and helpers. The entry skill relies on those installed
specialists, so installing only `adk-engineer` does not give you the whole toolkit.

<details>
<summary>Install one specialist, install for all projects, or inspect the list</summary>

If you already know the topic, install that specialist on its own:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill adk-memory-architecture
```

Add `-g` to install for your user account across projects:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -g
```

To see the available skills without installing them:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --list
```

Leave out `--skill` for interactive skill selection. Other supported coding
agents can be selected in the installer; their invocation interface may differ.

</details>

### 2. Ask your coding agent

Open your project in the coding agent after installation. If it was already
running and the new skills do not appear, restart the session.

| Coding agent | Entry command | Direct memory command |
| --- | --- | --- |
| Claude Code | `/adk-engineer` | `/adk-memory-architecture` |
| Codex | `$adk-engineer` | `$adk-memory-architecture` |

These are **chat commands**, typed into your coding agent, rather than terminal
commands. Claude Code supports `/name` for installed skills; Codex supports
explicit skill mentions using `$name`. See the respective
[Claude Code](https://code.claude.com/docs/en/skills) and
[Codex](https://developers.openai.com/codex/skills/) documentation for details.

No separate setup command is needed for this toolkit. The skills inspect the
project's existing code and configuration when they run. Their descriptions also
allow a supporting coding agent to select them from a natural-language request;
an explicit command makes your intended skill clear.

### 3. Try a concrete request

For example, in Claude Code:

```text
/adk-engineer Add memory so this support agent can remember a user's
preferred language between sessions. Keep our existing database and
include a way for the user to forget the preference.
```

In Codex:

```text
$adk-engineer Add memory so this support agent can remember a user's
preferred language between sessions. Keep our existing database and
include a way for the user to forget the preference.
```

The entry skill starts with `adk-memory-architecture`. It asks the coding agent
to inspect how your application identifies users and stores state, then choose
an appropriate design. An exact preference may belong in a profile record;
conversation history, facts across sessions and document retrieval have
different requirements. “Add memory” is enough to start that investigation.

For implementation work, the intended result is a change to your project with
relevant checks and a clear account of what remains unverified. For a design
question, ask for a design. You stay in control of the scope.

Here are a few other starting points; use `$` in place of `/` in Codex:

```text
/adk-engineer Our agent sometimes repeats a refund after a timeout.
Inspect the tool and fix the retry behaviour.

/adk-engineer Help me choose where to host this agent on Google Cloud.
Start with a deployment plan.

/adk-engineer Connect this ADK agent to our existing React interface
and show tool progress while a response streams.

/adk-engineer Add repeatable tests for tool selection and verify that
one user's session cannot read another user's history.
```

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## The Skills

*The contents · One entry point and eleven independently usable specialists.*

**[adk-engineer](skills/adk-engineer/SKILL.md)** is the starting point when you
know the outcome but have not chosen a specialist. It loads the relevant
instructions as needed. Installing the full set does not mean reading every
skill for every request.

The specialists below follow Chapters 0–10 of the book. Each linked name is
also its command name, with `/` in Claude Code or `$` in Codex.

### I. Foundations & safeguards

*Give the system a structure, then give it boundaries.*

**00** &nbsp; **[adk-workflow-design](skills/adk-workflow-design/SKILL.md)**

Choose how work moves through an agent: in sequence, in parallel, through a
bounded loop, or under ordinary Python control. Check handoffs and results.

**01** &nbsp; **[safe-api-tool-calls](skills/safe-api-tool-calls/SKILL.md)**

Handle temporary failures, deadlines and uncertain replies. Make repeated
requests safe when a tool changes something outside the application.

**02** &nbsp; **[adk-operational-guardrails](skills/adk-operational-guardrails/SKILL.md)**

Bound agent work, track usage, stop repeated tool calls and give consequential
actions a human approval path.

### II. From runtime to interface

*Find a home for the agent, refine its performance, and open the conversation.*

**03** &nbsp; **[deploy-adk-on-google-cloud](skills/deploy-adk-on-google-cloud/SKILL.md)**

Choose and prepare hosting on Cloud Run, Agent Runtime or GKE, including
identity, packaging, validation and resource lifecycle.

**04** &nbsp; **[optimise-adk-on-google-cloud](skills/optimise-adk-on-google-cloud/SKILL.md)**

Find where time and model usage go. Improve measured bottlenecks in agent work,
streaming, sessions, startup, concurrency and scaling.

**05** &nbsp; **[adk-frontend-integration](skills/adk-frontend-integration/SKILL.md)**

Connect an ADK agent to a browser through a custom JSON API or AG-UI with
CopilotKit. Handle session ownership, streamed text and tool progress.

### III. Memory, evidence & care

*Decide what the system knows, how to test it, and what it must protect.*

**06** &nbsp; **[adk-memory-architecture](skills/adk-memory-architecture/SKILL.md)**

Separate conversation state, facts across sessions, document retrieval and
structured history. Apply identity, consent, retention and erasure boundaries.

**07** &nbsp; **[adk-agent-evaluation](skills/adk-agent-evaluation/SKILL.md)**

Test agent behaviour with deterministic checks, live evaluation sets,
conversation simulation and strict inspection of the results.

**08** &nbsp; **[protect-adk-sensitive-data](skills/protect-adk-sensitive-data/SKILL.md)**

Control personal information in prompts, tools, stored history and public
responses, including Sensitive Data Protection and Model Armor integrations.

### IV. Trust in practice

*Secure the boundaries and work through a case study.*

**09** &nbsp; **[adk-tool-auth-and-secrets](skills/adk-tool-auth-and-secrets/SKILL.md)**

Verify who is calling a tool and what they may access. Work with keyless cloud
credentials, Secret Manager and delegated OAuth lifecycles.

**10** &nbsp; **[adk-sql-agent-engineering](skills/adk-sql-agent-engineering/SKILL.md)**

Build natural-language analytics agents with reviewed query templates,
selective schema retrieval and application-controlled query execution.

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## Using These with Matt Pocock's Skills

*Bring a development method and the ADK guidance to the same task.*

[Matt Pocock's skills](https://github.com/mattpocock/skills) cover general
engineering workflows. This toolkit contributes the ADK-specific decisions.
They can be installed alongside each other; neither collection is required
to use the other.

Some useful combinations:

| When you need to… | Matt's skill | ADK companion |
| --- | --- | --- |
| Clarify a feature and record its terminology | `grill-with-docs` | `adk-engineer` to carry out the resulting ADK work |
| Build a change through failing tests and small fixes | `tdd` | The relevant specialist, such as `adk-memory-architecture` |
| Investigate a slow agent | `diagnosing-bugs` | `optimise-adk-on-google-cloud` |
| Review the resulting change | `code-review` | The specialist's acceptance and validation guidance |

To add Matt's collection through the same installer:

```bash
npx skills@latest add mattpocock/skills --skill '*'
```

Choose the same coding agent and installation scope. Follow
[Matt's setup instructions](https://github.com/mattpocock/skills#installation-30-second-setup)
and run `setup-matt-pocock-skills` once per project: use
`/setup-matt-pocock-skills` in Claude Code or `$setup-matt-pocock-skills` in Codex.
That setup configures his workflow preferences. If you already use his Claude
Code plugin, keep that installation and use its command picker instead of
installing another copy through the CLI.

Then you can combine the installed skills in a request. In Claude Code:

```text
/adk-engineer Use the installed tdd skill to add cross-session memory
to this agent. Test user isolation and forgetting through our existing
storage interface.
```

In Codex:

```text
$adk-engineer Use $tdd to add cross-session memory to this agent.
Test user isolation and forgetting through our existing storage interface.
```

The development method supplies the test-first loop; the memory specialist
supplies the ADK and data-lifecycle guidance. This is composition through the
coding agent's instructions, with no special integration service to configure.
The result still depends on the coding agent following both sets of guidance.

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## Compatibility & Checks

The packages use the [Agent Skills format](https://agentskills.io/specification).
Each specialist contains a `SKILL.md`, supporting resources and its own licence.
The `agents/openai.yaml` files provide optional Codex display and invocation
metadata.

The specialists inspect your project's installed versions before applying an
SDK recipe. Their `references/` directories record compatibility, validation
evidence and practical limits; some helpers use only Python's standard library,
while optional checks require the listed ADK or cloud dependencies. There is
no single application environment to install at this repository's root.

Support for the file format and installer does not establish that every coding
agent, model or ADK version has been tested. Offline checks, live model calls
and deployed cloud behaviour are different kinds of evidence. The skills ask
the coding agent to report which checks actually ran. Cloud operations follow
the selected skill's scope and approval requirements.

For the packaging investigation, installation checks and design rationale, see
[the distribution notes](docs/research/skill-distribution.md).

### Updating and troubleshooting

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
and selected the correct coding agent, then restart its session. If the entry
skill reports a missing specialist, rerun the full-toolkit installation or
install the named specialist. If `npx` fails before showing the installer,
check `node --version` against the prerequisite above.

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

## About the Book

These skills turn the engineering lessons in **Agentic Engineering: Building
Production-Grade Multi-Agent Systems with Google ADK on GCP** into workflows
you can apply to an existing project.

The [book's code companion](https://github.com/RuslanKhis/agentic-engineering-adk-gcp)
contains runnable chapter examples and their setup instructions. Start there
if you want to learn an idea through a small application. Start here when you
want your coding agent to help apply that idea to your own code.

The book publication link will be added when it is available.

## License

This project is licensed under the [MIT License](LICENSE). You can adapt the
skills to your projects. Each installable package includes its own licence.

An independent community project, not affiliated with or endorsed by Google
or Matt Pocock. Contributions and reproducible issue reports are welcome.

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

<p align="center">
  <img src="docs/editorial/colophon.svg" alt="Agentic Engineering · The skills companion" width="240">
</p>

<p align="center">
  <a href="#getting-started">Install the skills</a> ·
  <a href="#the-skills">Return to the contents</a>
</p>
