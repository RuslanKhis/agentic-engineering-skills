# Working with Google's Agents CLI

*A shared project, with a clear job for each collection.*

Use **Agents CLI** for its project lifecycle, generated infrastructure, platform
commands and ADK reference implementations. Use **Agentic Engineering Skills**
to design and verify the particular application change. Add **Matt Pocock's
skills** when you want a development method such as test-first implementation
or code review.

Google's separate [skills collection](google-cloud-skills.md) covers the
products around the agent (Cloud Run, IAM, monitoring, databases); this guide
is about the ADK lifecycle skills.

There is overlap: Google's recipes already cover memory, approvals, credentials
and other engineering concerns. The useful combination is to adapt those
recipes using this toolkit's guidance on application boundaries and validation.
Neither collection requires the other. This is a proposed way to combine
instructions, not a tested integration or an endorsement by Google.
[Google's skills reference](https://google.github.io/agents-cli/reference/skills/),
[ADK code skill](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-adk-code/SKILL.md)

## Install them together

### Project skills for your coding client

From the application directory, install both collections for the same coding
agent. If one is already installed there, only add the missing collection:

```bash
npx skills@latest add google/agents-cli --skill '*' -a claude-code
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill '*' -a claude-code
```

For Codex, replace `-a claude-code` with `-a codex` on both commands. Keep the
quotes around `'*'`. The normal project installation makes seven Google skills
and the twenty-six skills of this toolkit available. Restart the coding-agent
session if they do not appear. Google's README offers the Skills CLI route as
`npx skills add google/agents-cli` (the same seven skills) and names both
Claude Code and Codex.
[Google's installation instructions](https://github.com/google/agents-cli#readme)

For Gemini CLI, use `-a gemini-cli` on both commands; for Antigravity, use
`-a antigravity` or `-a antigravity-cli`. These project targets share
`.agents/skills/`. Follow the [Google coding-agent setup guide](google-coding-agents.md)
for discovery and invocation. In Gemini CLI, start a combined request with
“Use the adk-engineer skill…” and name Google's relevant skill in the same request.

The skills installer needs the prerequisites in our
[getting-started guide](../../README.md#getting-started). Skill files alone do
not install the `agents-cli` executable, Google ADK or application dependencies.

### Add the CLI when you need its commands

With Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/)
available, Google's documented CLI installation is:

```bash
uv tool install google-agents-cli
agents-cli --help
```

This installs a user-level command-line tool. It is separate from the
project-scoped skill files and the application's Python environment. Configure
model access when you are ready for live runs; a local server or evaluation
can still call a paid remote model.
[Google workflow prerequisites](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-workflow/SKILL.md)

If you prefer Google's combined setup, use it **instead of** the Google
skills-only installation above:

```bash
uvx google-agents-cli setup --workspace --agent claude-code --skip-auth
```

Then install this toolkit with the second `npx` command. `--workspace` selects
project skills, `--agent` selects the coding agent, and `--skip-auth` skips the
authentication phase. Setup can still install the CLI as a user tool; it is
broader than copying skill files. Use `--agent codex` for Codex. Check your
version's `setup --help` before relying on these flags.
[Setup implementation](https://github.com/google/agents-cli/blob/main/src/google/agents/cli/setup/cmd_setup.py)

Choose one installation route for each collection. If you already use a native
plugin installation, use its command picker and namespace rather than adding
another copy.

## Decide which workflow leads

- **Architecture before implementation:** use `adk-system-designer` to work
  through requirements, trade-offs and application guarantees. Keep an existing
  Agents CLI specification as input and carry agreed decisions forward; design
  work does not itself initiate scaffolding or cloud commands.
- **New Agents CLI project:** begin with `google-agents-cli-workflow`. Use its
  scaffold and project conventions, then select an Agentic Engineering
  specialist for the feature being implemented.
- **Existing Agents CLI project:** start with `adk-engineer` or the relevant
  specialist for a focused feature, diagnosis or review. Name the relevant
  Google skills and retain the generated configuration and infrastructure.
- **Existing application without Agents CLI:** this toolkit remains usable as
  it is. Decide separately whether to adopt Agents CLI. Review a disposable
  scaffold or work on a separate copy before migrating the application's layout.

Google's workflow describes itself as always active and runs eight phases:
understand (a one-question-at-a-time dialogue that ends in
`.agents-cli-spec.md`, with a hard gate before any scaffold), study recipes,
scaffold, build, evaluate, deploy, publish and observe. It asks for
scaffolding before code changes and evaluation after implementation. Its
build phase also says not to write behavioural unit tests and to leave
behaviour to evaluation; this toolkit's scripted-model Runner tests of
forbidden effects (a refund issued twice, another user's record returned)
are deterministic application checks, not behaviour judgements, and stay.
Name that division in the request when both collections are installed.
The ADK code skill also points back to that workflow. Loading it is therefore
more than consulting an API cheatsheet. For a small change, explicitly tell the
coding agent which work is authorised and which existing conventions to keep.
The phrase “always active” is guidance in the skill; actual loading depends on
the coding agent.
[Google workflow](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-workflow/SKILL.md),
[ADK code prerequisites](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-adk-code/SKILL.md)

For example, append this scope to a request in an existing application:

```text
Keep this change within the existing application. Do not scaffold,
enhance or upgrade the project, change dependency pins or model selection,
or start live evaluation as part of this task. Implement and verify the
local change; report any platform work that would be needed separately.
```

Do not assume `scaffold enhance --dry-run` previews every migration: in the
reviewed source, that mode requires an existing Agents CLI manifest and a
requested enhancement; `scaffold upgrade` has `--dry-run` and `--force` since
1.8.0. Consult the installed command's help for your project.
[Enhancement implementation](https://github.com/google/agents-cli/blob/main/src/google/agents/cli/scaffold/commands/enhance.py)

## Three practical workflows

These are chat prompts, not terminal commands. The examples use Claude Code's
`/` prefix; in Codex replace the leading `/` with `$`. Name additional installed
skills in ordinary text rather than assuming several slash commands compose
automatically. Each example states its scope; expand it when you want live work.
In Gemini CLI and Antigravity IDE integrations, replace the first `/skill-name`
with “Use the skill-name skill to” and keep the remaining request. Antigravity
2.0 and its CLI also support the slash form.

### 1. Add memory to a generated support agent

```text
/adk-engineer In this existing Agents CLI project, remember each user's
preferred response language between conversations. Use the installed
google-agents-cli-adk-code skill to inspect relevant recipes and match
the installed ADK APIs. Use adk-memory-architecture to choose storage
and implement consent, user isolation, changing and forgetting a setting.
Keep the current scaffold, database, model and dependency pins. Add and
run offline tests, including persistence across process restarts. Report
what still needs a real-model evaluation; do not make live calls here.
```

**Expected result:** a feature integrated with the existing agent and storage,
with tests of the trusted user identity and saved effects. A persistent profile
record may fit an exact language setting better than semantic memory retrieval.
Google's memory recipe is a reference to assess, not a requirement to change
the application's backend.

### 2. Check a refund agent with both code tests and evaluation

```text
/adk-agent-evaluation Prepare a validation strategy for this Agents CLI
refund agent. Use google-agents-cli-eval for its dataset, metric and
result formats. Implement offline tests proving that a timed-out retry
cannot issue a second refund and that one user cannot refund another
user's order; use safe-api-tool-calls for the retry design. Prepare live
eval cases for tool choice and truthful refund confirmations, with
isolated test data, explicit budgets and holdout cases. Do not execute
live evaluations yet. Define how CI will reject failed or missing cases
even when the evaluation command exits successfully.
```

**Expected result:** deterministic checks of real application effects, plus a
separate evaluation plan for model-dependent decisions. A scripted model can
exercise an actual ADK Runner offline; passing those tests does not establish
real-model quality. Google's `eval run` generates and grades traces, while
acceptance still requires inspecting case coverage and scores. Its dataset
and result formats are distinct from the native ADK eval/CSV paths supported
by some of this toolkit's helpers; do not interchange them without validation.
[Google evaluation skill](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-eval/SKILL.md),
[our evaluation specialist](../../skills/adk-agent-evaluation/SKILL.md)

If Matt's `tdd` is installed, add “Use the installed tdd skill for the
deterministic tests.” That supplies the implementation method. Keep live judge
scores and local test results as separate evidence.

### 3. Prepare Cloud Run deployment and inspect telemetry

```text
/deploy-adk-on-google-cloud Review this Agents CLI project's Cloud Run
deployment. Use google-agents-cli-deploy for the generated infrastructure
and command conventions, and google-agents-cli-observability to map its
telemetry. Use protect-adk-sensitive-data to review where prompts,
responses and tool arguments can be stored. Preserve the existing
Terraform ownership, runtime identity and CI/CD setup. Prepare the
required file changes, validation steps and rollback plan. Identify
retention and access settings for each destination. Do not deploy or
change cloud resources in this task.
```

**Expected result:** a reviewable deployment change with a clear owner for
each resource and an inventory of exported data. Inspect traces, logs,
completion uploads and analytics independently. In the 1.11.0 observability
skill, as in 1.5.0, disabling message content in traces does **not** disable
the separate full-content GCS/BigQuery upload path. Since 1.10.0 a new project
deploys to Agent Runtime under Agent Identity by default, `deploy --dry-run`
makes read-only cloud calls and exits non-zero on a definite problem, and a
customer-managed key can only be set when the agent is created. Terraform and
the imperative `agents-cli deploy` must not own the same engine. Check the
actual generated files and installed version before applying any of this to
your project.
[Google observability skill](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-observability/SKILL.md)

For a latency investigation, use Google's tracing guidance to obtain evidence
and `optimise-adk-on-google-cloud` to choose and measure a change. For
registration in Gemini (formerly Gemini Enterprise) or the Agent Registry,
`adk-agent-interoperability` owns the agent card, the registration mode and
the contracts, and `google-agents-cli-publish` runs `agents-cli publish gemini`
and the registry commands.

## Keep versions and evidence visible

The comparison was first made on 15 September 2026 against version 1.5.0 and
re-checked on 22 October 2026 against a 1.11.0 snapshot (release notes dated
20 October 2026), whose seven skill files all declare 1.11.0. Online copies
can differ. Confirm the installed CLI, scaffold and SDK versions before
applying a recipe or interpreting an evaluation file.

Changes between those versions that affect how the collections combine:
new projects scaffold on `google-adk>=2.12.0` and set
`GOOGLE_GENAI_USE_ENTERPRISE=true` (this toolkit's recipes were checked
against 2.8.0, so a feature named in a recipe may need the newer pin); the
`adk@<name>` recipe shortcut is gone and recipes are addressed by URL in the
renamed `google/adk-recipes` repository; Agent Identity is the default for
new Agent Runtime projects; `deploy --dry-run` makes read-only cloud calls;
`--ingress`, `--key` and label flags were added; Live (voice) agents run and
evaluate through `--mode adk_live`; extensions can ship skills into
`.agents/skills/`; and usage telemetry is on by default since 1.9.0 (opt out
with `AGENTS_CLI_TELEMETRY=0` or `DO_NOT_TRACK=1`). The dated
[comparison note](../research/agents-cli-comparison-2026-10-22.md) lists what
this toolkit imported, routed and left out at 1.11.0.

In the reviewed implementation, `agents-cli update` upgrades the CLI and calls
the Skills CLI update command without filtering to Google's collection. It
can therefore affect other installed skills in the selected scope. For a
Google-skills-only refresh, rerun the explicit Google `skills add` command for
the same agent and scope after preserving any local edits.
[Update implementation](https://github.com/google/agents-cli/blob/main/src/google/agents/cli/setup/cmd_update.py)

This guide was checked against documentation and source. No combined
installation, code-generation session, live evaluation or cloud deployment was
run for this comparison. Earlier tests of this toolkit alone are recorded
separately in [the CLI test report](../testing/codex-cli-smoke.md).

For the detailed overlap and proposed changes to this toolkit, read
[the comparison and enhancement recommendations](../research/agents-cli-comparison.md),
its [23 September refresh](../research/agents-cli-comparison-2026-09-23.md)
and the [22 October note against 1.11.0](../research/agents-cli-comparison-2026-10-22.md).
