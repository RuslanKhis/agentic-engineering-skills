---
name: adk-engineer
description: >-
  Help build, change or review a Python Google ADK agent by selecting the
  relevant Agentic Engineering specialist skills. Use as the starting point
  for an ADK engineering request when the user has not chosen a specialist,
  or when a change spans several ADK concerns. For a focused task already
  covered by an active specialist, continue with that skill directly.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
---

# ADK engineer

Turn the user's request into a focused ADK engineering task and carry it out
with the relevant installed specialist. This is the entry point to the toolkit;
the implementation guidance lives in the specialist packages. The book and its
companion repository are optional reading.

## Understand the request

Read the project's instructions and the code, dependency pins and tests relevant
to the request. Establish whether the user wants an explanation, a design,
implementation or a review, and what observable result would satisfy it.
Preserve the project's domain and working conventions. Resolve routine choices
from the repository; ask only for missing decisions that affect the result.

If the project has `agents-cli-manifest.yaml`, the user asks to use Agents CLI,
or another collection already supplies the development workflow, read
[working with other skill collections](references/composition.md). It explains
how to preserve that workflow while selecting the ADK guidance for this task.

## Select and load the specialist

Choose one primary skill from the table. Add another only when the requested
change crosses its boundary. Say briefly which skill you are applying and why.

| Request concerns | Specialist skill |
| --- | --- |
| Workflow structure, handoffs, parallel work, loops, events or callbacks | `adk-workflow-design` |
| External API retries, deadlines, duplicate writes or uncertain outcomes | `safe-api-tool-calls` |
| Runaway invocations, usage budgets or human approval of agent actions | `adk-operational-guardrails` |
| Hosting choice, packaging or deployment on Google Cloud | `deploy-adk-on-google-cloud` |
| Measured latency, cost, concurrency, startup or scaling problems | `optimise-adk-on-google-cloud` |
| Browser interfaces, JSON APIs, AG-UI, CopilotKit or streaming contracts | `adk-frontend-integration` |
| Conversation state, cross-session memory, document retrieval or history | `adk-memory-architecture` |
| Agent behaviour tests, evaluation datasets, replay or result auditing | `adk-agent-evaluation` |
| Personal data in prompts, tools, storage, logs or streamed answers | `protect-adk-sensitive-data` |
| Tool identity, credentials, Secret Manager or delegated OAuth | `adk-tool-auth-and-secrets` |
| Natural-language SQL agents, schema retrieval or controlled query execution | `adk-sql-agent-engineering` |

Locate the selected skill through the coding agent's available-skills catalogue
and read its `SKILL.md`. When using a filesystem installation without a catalogue
entry, check the sibling directory `../<specialist-name>/SKILL.md` relative to
this installed skill directory. Resolve the specialist's references, scripts
and assets relative to its own directory, even when the installer uses symlinks.
Load only the references needed for the selected mode.

The installer does not automatically install dependencies for this entry skill.
If a selected specialist is unavailable, name the missing skill and show:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill <specialist-name>
```

Replace the placeholder with the actual skill name. Have the user reload the
coding agent after installation if needed. Continue independent inspection or
explanation, but distinguish it from work guided by the missing specialist;
resume specialist-dependent implementation after its instructions are available.

## Apply the guidance

Follow the selected specialist's inspection, implementation and validation path.
Its compatibility references determine which SDK recipes fit the target.
Preserve the user's requested scope and existing authorisation. Complete local
work and make any proposed external operation concrete before requesting a
missing approval for that operation.

For example, “add memory” starts with `adk-memory-architecture`. Determine
whether the need is conversation state, an exact profile setting, facts across
sessions or document retrieval before selecting a store. Add data-protection
guidance when the requested data flow needs that work. Add evaluation guidance
when the task calls for an agent evaluation strategy; ordinary regression tests
remain part of the memory implementation itself.

Finish with the requested explanation or the change made, validation actually
performed, and any unresolved decision or unverified behaviour. Naming a
specialist is the start of the work, not its completion.
