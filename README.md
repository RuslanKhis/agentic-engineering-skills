<p align="center">
  <img src="docs/editorial/cover.svg" alt="Agentic Engineering Skills — The skills companion. An architectural ink drawing of connected agents, on warm paper." width="100%">
</p>

<p align="center">
  <a href="#where-to-start">Where to start</a> ·
  <a href="#getting-started">Getting started</a> ·
  <a href="#the-skills">The skills</a> ·
  <a href="#using-skills-together">Using skills together</a> ·
  <a href="#compatibility--checks">What has been tested</a> ·
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

Let's connect on [LinkedIn](https://www.linkedin.com/in/ruslan-k-b6a48a1a6/).
Questions, feedback or ideas about the skills or the book? Feel free to write
to me at [khissamiyev@proton.me](mailto:khissamiyev@proton.me).

A **skill** is a folder of instructions, references and, where useful, helper
scripts that your coding agent can read while working on your project. These
skills help it apply the book's engineering practices to your own application:
handle failed tool calls, add memory, connect a browser interface, test agent
behaviour, or prepare a deployment.

## Where to start

| You are… | Start with | What you get back |
| --- | --- | --- |
| **Not sure where AI fits, or which use case comes first** | `/adk-discovery` | A short discovery conversation, a ranked list of opportunities with the technology each needs (agent, LLM, classical ML, rules or a process change), the first use case with its outcome measure and baseline, and the exact prompt for the designer |
| **Starting a new ADK application** | `/adk-system-designer` | A short design conversation, then an architecture document, a goal plan, and the exact prompt for the first goal |
| **Changing an application you already have** | `/adk-engineer` | It names the specialist it is using, makes the change with local tests, and says what is still unverified |
| **Answering a client's legal, privacy or security reviewers** | `/adk-governance-pack` | A screen of which Australian (including NSW and Commonwealth government), US, EU, UK, New Zealand, Singapore and Canadian privacy and AI laws apply, then draft papers built from the design and plan: a regulatory memo (with the EU AI Act classification where the EU applies), privacy impact inputs serving as PIA, DPIA or US risk assessment, transfer facts, an impact assessment, a system card, processing records, security questionnaire answers and, for a government agency, draft answers to the DTA or NSW AIAF forms, each statement citing its evidence or flagged for counsel; drafts that support the client's lawyer, never replace one |
| **Presenting the work to decide the next step** | `/adk-presenter` | A slide outline with evidence under every claim, what to say, the questions to expect and a one-page decision memo, for a business or a technical audience, at proof-of-concept approval, production approval, results review, or as a public case study |

Discovery, design, engineering and presentation all lead to the same nineteen specialists; the governance pack drafts from what they record, and the optional portability planner assesses an accepted design for lock-in without changing it. You never need to remember which
one fits: the designer writes the specialist into every goal, and
`adk-engineer` picks one for any ticket or request. You can also call a
specialist directly when you already know the topic.
[Journey A](#journey-a-build-a-new-application),
[Journey B](#journey-b-maintain-an-application) and
[Journey C](#journey-c-win-the-decision) below show the prompts.

You do not need the book or its example repository to use the skills. Install
them in the project you want to work on. They guide your **coding agent**;
your application's ADK agents do not load them automatically.

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## Watch the Walkthrough

*Install. Ask. Review. · 2 minutes 20 seconds.*

Already have an ADK agent? See how to install the skills, ask for a streaming
frontend, and add a remembered language preference. This animated worked example
is backed by [runnable local code and checks](docs/video/skills-walkthrough/demo/README.md).

[![Watch the walkthrough: use adk-frontend-integration to connect an existing React chat to an ADK agent.](docs/video/skills-walkthrough/assets/preview.png)](docs/video/skills-walkthrough/assets/walkthrough.mp4)

**[Watch or download the video — 2:20, MP4](docs/video/skills-walkthrough/assets/walkthrough.mp4)**

Music: “just turn it on and make something.” by
[hijaq.](https://hijaqmusic.bandcamp.com/track/just-turn-it-on-and-make-something),
used under the artist's published free-use permission.
[Full music credits](docs/video/skills-walkthrough/publishing.md#music-credits).

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

Choose your coding agent when prompted. This installs **all twenty-six skills**
for the current project: `adk-discovery`, `adk-system-designer`,
`adk-engineer`, `adk-presenter`, `adk-governance-pack`, the optional
`adk-portability-planning`, the eleven chapter specialists,
the web backend specialist, the seven cross-framework specialists and the optional
`practice-profile`.
Keep the quotes around `'*'` so your shell passes it unchanged.

<details>
<summary>Choose a client explicitly, install globally, or select one specialist</summary>

**Choosing a Google client?** Use Antigravity for Google consumer accounts.
Since 18 June 2026, Gemini CLI no longer serves Code Assist for individuals,
Google AI Pro or Google AI Ultra through Google sign-in. Gemini CLI remains
available through Code Assist Standard/Enterprise and supported paid API-key
routes. See the [Google setup guide](docs/integrations/google-coding-agents.md),
[Google's account guidance](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals)
and [supported Gemini CLI access](https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/).

To select a particular coding agent, use one of these project commands:

```bash
# Claude Code
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a claude-code

# Codex
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a codex

# Google Antigravity app or IDE
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a antigravity

# Google Antigravity CLI (agy)
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a antigravity-cli

# Gemini CLI with supported Standard/Enterprise or paid API-key access
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a gemini-cli
```

For Claude Code, Codex or Gemini CLI, add `-g` to install for your user account
across projects. For example:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a codex -g
```

Antigravity's app, IDE and CLI document different global directories. Use the
project commands above or follow the [global directory guidance](docs/integrations/google-coding-agents.md#installation-scope)
for your client; the tested Skills CLI's `-g` destination differs from those paths.

To install a specific release rather than the latest commit, add its tag
(listed in the [changelog](CHANGELOG.md)) after the repository name:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills#v2026.10.25 --skill '*'
```

**Prefer updates that arrive on their own?** Claude Code and Gemini CLI can
install the collection as a plugin that follows tagged releases instead (see
[updating](docs/troubleshooting.md)). Use one route per coding agent,
not both, or every skill appears twice.

If you already know the topic, install that specialist on its own:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill adk-memory-architecture
```

Each specialist includes its own references and helpers. Installing only
`adk-engineer` does not give you the specialists it needs to carry out the work.

To see the available skills without installing them:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --list
```

Leave out `--skill` for interactive skill selection. Other supported coding
agents can be selected in the installer; their invocation interface may differ.

</details>

### 2. Open your coding agent

Open your project after installation. If the coding agent was already running
and the new skills do not appear, restart its session. Type skill requests
**in the coding agent's chat**:

| Coding agent | New application | Existing application | A specialist directly |
| --- | --- | --- | --- |
| Claude Code | `/adk-system-designer` | `/adk-engineer` | `/adk-memory-architecture` |
| Codex | `$adk-system-designer` | `$adk-engineer` | `$adk-memory-architecture` |
| Antigravity app / IDE / CLI | `Use the adk-system-designer skill to…` | `Use the adk-engineer skill to…` | `Use the adk-memory-architecture skill to…` |
| Gemini CLI, with supported access | `Use the adk-system-designer skill to…` | `Use the adk-engineer skill to…` | `Use the adk-memory-architecture skill to…` |

The prompts in this README use Claude Code's `/` form. In Codex replace the
leading `/` with `$`; in Gemini CLI or Antigravity say "Use the <skill> skill
to…" and keep the rest of the request.

Clients activate skills slightly differently; no separate setup command is
needed. See [how skill activation differs between clients](docs/troubleshooting.md#how-skill-activation-differs-between-clients).
Optionally, `/practice-profile` keeps your employer's and clients' context
outside your repositories so later projects start from it; without it,
nothing changes.

### 3. Ask for a first change

In an application you already have, hand `adk-engineer` a symptom or a change:

```text
/adk-engineer Our agent picks the wrong tool for order lookups and passes the
customer's name where the order ID goes. Fix it and add a regression test.
```

It names the specialist it is using and why, makes the change, runs the local
checks and says what remains unverified. Nothing is deployed or paid for
without your approval. For a new application, start with
[Journey A](#journey-a-build-a-new-application) instead.

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## The Skills

*The contents · Twenty-six skills: five entry points, eleven chapter specialists, a web backend specialist, seven cross-framework specialists and two optional skills.*

Choose a skill by the problem you need to solve, or let `adk-engineer` choose.
Each name links to its [full entry](docs/skills.md), with when it helps, what
to ask for and three example prompts; the package itself is under
`skills/<name>/`.

**Entry points** · start a piece of work here.

| Skill | Purpose | Use it for |
| --- | --- | --- |
| [adk-discovery](docs/skills.md#adk-discovery) | Find where AI pays off and pick the first use case | Where AI fits, which use case first, what to measure, and whether an agent, classical ML, rules or a process change is the right tool |
| [adk-system-designer](docs/skills.md#adk-system-designer) | Work out what the application must guarantee | A design conversation, architecture and phased goal plan before implementation |
| [adk-engineer](docs/skills.md#adk-engineer) | Choose the right specialist | Any change to an existing application, or a request that spans several concerns |
| [adk-presenter](docs/skills.md#adk-presenter) | Show the value, with evidence under every claim | Proof-of-concept approval, production decision, results review or a public case study |
| [adk-governance-pack](docs/skills.md#adk-governance-pack) | Draft what the client's reviewers sign | Which privacy and AI laws apply, and draft papers for counsel, DPO or CISO, each statement citing its evidence |

**Chapter specialists** · Chapters 0–10 of the book; no chapter reading is required.

| Skill | Purpose | Use it for |
| --- | --- | --- |
| [adk-workflow-design](docs/skills.md#adk-workflow-design) | 00 · Arrange the work and make sure it finishes | Sequential steps, parallel work or bounded loops |
| [safe-api-tool-calls](docs/skills.md#safe-api-tool-calls) | 01 · Handle unreliable APIs without repeating an action | Reliable API calls and protection against duplicate actions |
| [adk-operational-guardrails](docs/skills.md#adk-operational-guardrails) | 02 · Put limits and approval checks around agent actions | Usage limits, repeated-tool protection or human approval |
| [deploy-adk-on-google-cloud](docs/skills.md#deploy-adk-on-google-cloud) | 03 · Choose a host and prepare the files to run there | A hosting choice or deployment preparation |
| [optimise-adk-on-google-cloud](docs/skills.md#optimise-adk-on-google-cloud) | 04 · Find where time and model usage go | Faster replies and lower model usage |
| [adk-frontend-integration](docs/skills.md#adk-frontend-integration) | 05 · Connect the agent to the person using it | A browser interface, streaming or tool progress, its design system and agent UI states |
| [adk-memory-architecture](docs/skills.md#adk-memory-architecture) | 06 · Remember the right information for the right person | Conversation history, memory or document retrieval |
| [adk-agent-evaluation](docs/skills.md#adk-agent-evaluation) | 07 · Test what the agent does as well as what it says | Repeatable tests and trustworthy evaluation results |
| [protect-adk-sensitive-data](docs/skills.md#protect-adk-sensitive-data) | 08 · Control what sensitive information reaches each part | Sensitive-data controls across prompts, tools and replies |
| [adk-tool-auth-and-secrets](docs/skills.md#adk-tool-auth-and-secrets) | 09 · Give each tool the right identity | Tool identity, credentials or per-user OAuth |
| [adk-sql-agent-engineering](docs/skills.md#adk-sql-agent-engineering) | 10 · Turn business questions into read-only analytics | Controlled natural-language analytics and SQL execution |

**Web backend**

| Skill | Purpose | Use it for |
| --- | --- | --- |
| [adk-fastapi-backend](docs/skills.md#adk-fastapi-backend) | Build the ordinary web backend around the agent, safely | Sign-in check, own-record routes, migrations beside ADK's tables, API contract and typed client |

**Cross-framework specialists** · practices from across the field, implemented for ADK.

| Skill | Purpose | Use it for |
| --- | --- | --- |
| [adk-agent-instructions](docs/skills.md#adk-agent-instructions) | Write the instruction that carries the judgment | Agent instructions, state templating and sub-agent descriptions |
| [adk-tool-interface-design](docs/skills.md#adk-tool-interface-design) | Design the tool the way the model will see it | Tool docstrings, parameter schemas, tool count and result shape |
| [adk-model-and-output-contracts](docs/skills.md#adk-model-and-output-contracts) | Decide what the model emits and which model emits it | Structured output, model choice, thinking settings and failover |
| [adk-agent-security](docs/skills.md#adk-agent-security) | Assume the injection succeeds, and make sure it cannot do harm | Prompt-injection resilience, MCP vetting, sandboxing and red-teaming |
| [adk-agent-observability](docs/skills.md#adk-agent-observability) | See what the agent did, what it cost, and where the time went | Tracing, metrics, SLOs, alerts and production-to-evaluation hand-off |
| [adk-release-engineering](docs/skills.md#adk-release-engineering) | Ship prompt, model and tools as one release, and undo it | Version pinning, CI eval gates, model migration, canary and rollback |
| [adk-agent-interoperability](docs/skills.md#adk-agent-interoperability) | Cross a process or protocol boundary without losing the contract | MCP servers, remote A2A agents, agent cards and registration |

**Optional** · nothing changes if you never call them.

| Skill | Purpose | Use it for |
| --- | --- | --- |
| [adk-portability-planning](docs/skills.md#adk-portability-planning) | Answer a lock-in question without changing the build | A separate portability plan for an accepted GCP and ADK design: AWS and Azure alternatives, other frameworks, migration risks |
| [practice-profile](docs/skills.md#practice-profile) | Stop retyping each client's context | Your employer's and clients' context and lessons, kept outside every repository and offered as defaults |

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## Using Skills Together

*Three journeys through the same specialists.*

Each journey below is one paragraph and a first prompt. The
[journeys guide](docs/journeys.md) has every prompt for every stage, and how
to combine these skills with
[Google's Agents CLI](docs/journeys.md#using-these-with-googles-agents-cli),
[Google's Cloud skills](docs/journeys.md#using-these-with-googles-cloud-skills)
and [Matt Pocock's skills](docs/journeys.md#using-these-with-matt-pococks-skills),
including a [design-to-tickets walkthrough](docs/journeys.md#from-design-to-working-tickets).

### Journey A: build a new application

Find the use case with `adk-discovery` if nobody has chosen one, then design
in conversation with `adk-system-designer`. It asks about time, people,
budget, users and data, then saves an architecture and a phased goal plan
under `docs/architecture/` and `docs/plans/`, each goal naming its specialist
and an estimate of human hours. `adk-engineer` then builds one goal or ticket
at a time, checks the plan's health between tickets, and ends each run with
the prompt for the next. [Full walkthrough](docs/journeys.md#journey-a-build-a-new-application).

```text
/adk-system-designer I want to build <one-sentence product> with ADK on GCP.
I have <time and budget>; <who> will judge it as an <exploration, assignment,
pilot or production service>. Design only.
```

### Journey B: maintain an application

Hand `adk-engineer` a ticket, a symptom or a change. It reads the project,
tells you which specialist it is using and why, then does the work and reports
the checks that actually ran. [More examples](docs/journeys.md#journey-b-maintain-an-application).

```text
/adk-engineer Google says our Gemini model retires next month. Plan and make
the upgrade without silently dropping quality.
```

### Journey C: win the decision

A project is presented at proof-of-concept approval, at the production
decision, at the final results review and, when shareable, as a public case
study. `adk-presenter` builds each outline, speaker notes, decision memo and
expected questions from the evidence the goals recorded, never from a number
it made up. [All four prompts](docs/journeys.md#journey-c-win-the-decision).

```text
/adk-presenter Prepare the proof-of-concept approval presentation for a
business audience from docs/discovery/<topic>.md, docs/architecture/<topic>.md
and docs/plans/<topic>.md. Fifteen minutes. Then a technical version for the
platform team.
```

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## Updating and Troubleshooting

*Keep the installed skills current.*

The collection is released as dated versions, each tagged `v<version>` and
listed in the [changelog](CHANGELOG.md); the `stable` branch points at the
latest release. `adk-engineer` tells you in one line when your installed
skills are out of date, and never updates anything itself. Update with the
scope you installed into:

```bash
# Update skills installed in the current project.
npx skills@latest update -p

# Or update skills installed for your user account.
npx skills@latest update -g
```

If you ever installed globally (`-g`), update that copy too: in Claude Code a
user-level skill takes precedence over a project copy with the same name.
Restart the session afterwards. The
[updating and troubleshooting guide](docs/troubleshooting.md) covers plugin
installs that follow releases (Claude Code, Gemini CLI, Antigravity), trying
local edits before publishing them, and
[reporting a skill that is wrong in your project](docs/troubleshooting.md#when-a-skill-is-wrong-in-your-project).

<p align="center">
  <img src="docs/editorial/section-break.svg" alt="" width="240">
</p>

## Compatibility & Checks

*What has been tested, and what has not.*

- **Offline, on every change.** GitHub Actions validates all twenty-six
  packages against the [Agent Skills format](https://agentskills.io/specification)
  and runs their offline helper suites on Python 3.11 and 3.12. These checks
  do not establish model or cloud behaviour.
- **With models, in bounded trials.** Fresh coding-agent sessions in Claude
  Code and Codex, and one Antigravity IDE session with Gemini, used the skills
  on small local projects; the generated code was reviewed and passed
  independent acceptance checks. Skill selection from descriptions was
  measured over the activation corpus on 8 October 2026 (55 of 56 cases).
  Each trial is a sample on a given date, model and client version.
- **Not established.** That every skill, model, SDK version or client has
  been exercised. The log records no cloud deployment made through the
  skills. Gemini CLI generation was blocked by an account restriction, and
  the standalone Antigravity app and CLI were not used for generation.

The [testing log](docs/testing/index.md) has every dated entry, newest first,
with links to the prompts, versions and raw results.

## Improving and Contributing

*Make the instructions easier to select, then verify the work they produce.*

The [maintainer guide](CONTRIBUTING.md) provides a local check command and the
conventions for changing a skill. The
[quality evaluation guide](docs/testing/skill-quality.md) separates natural
skill selection, explicit invocation, composition and implementation results,
with positive and near-miss cases for every skill and a procedure for
comparing a change against a baseline. See
[the research behind these practices](docs/research/skill-quality-practices.md)
for sources and the limits of the available evidence.

## About the Book

These skills turn the engineering lessons in **Agentic Engineering: Building
Production-Grade Multi-Agent Systems with Google ADK on GCP** into workflows
you can apply to an existing project.

The [book's code companion](https://github.com/RuslanKhis/agentic-engineering-adk-gcp)
contains runnable chapter examples and their setup instructions. Start there
if you want to learn an idea through a small application. Start here when you
want your coding agent to help apply that idea to your own code.

**[Preorder the book on Amazon](https://www.amazon.com/dp/B0HK78328V?spcref=PUBLISHED_PREORDER_LIVE).**

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
