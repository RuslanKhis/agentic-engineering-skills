---
name: adk-engineer
description: >-
  Help design, build, change or review a Python Google ADK application by selecting the
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
Note the time budget, who judges the result and the artifact type (exploration,
assignment, pilot, production) before sizing the work; a time-boxed task judged
on output quality starts with the core judgment measured on real inputs.

When continuing a design or implementation plan, read its linked decisions,
requested goal, dependencies, acceptance cases and execution scope. Check the
current repository and skill availability, preserve settled choices, and work
on the next authorized goal. Record actual evidence and unresolved blockers in
the canonical plan or tracker; restart discovery only for a material new gap.

If the project has `agents-cli-manifest.yaml`, the user asks to use Agents CLI,
or another collection already supplies the development workflow, read
[working with other skill collections](references/composition.md). It explains
how to preserve that workflow while selecting the ADK guidance for this task.

## Select and load the specialist

Choose one primary skill from the table. Add another only when the requested
change crosses its boundary. Say briefly which skill you are applying and why.

| Request concerns | Specialist skill |
| --- | --- |
| Whole-application architecture, requirements and trade-offs before coding, or a cross-cutting system review | `adk-system-designer` |
| Workflow structure, handoffs, parallel work, loops, events or callbacks | `adk-workflow-design` |
| External API retries, deadlines, duplicate writes or uncertain outcomes | `safe-api-tool-calls` |
| Runaway invocations, usage budgets or human approval of agent actions | `adk-operational-guardrails` |
| Hosting choice, packaging or deployment on Google Cloud | `deploy-adk-on-google-cloud` |
| Measured latency, cost, concurrency, startup or scaling problems; long sessions, context growth per turn or cache misses | `optimise-adk-on-google-cloud` |
| Browser interfaces, JSON APIs, AG-UI, CopilotKit or streaming contracts | `adk-frontend-integration` |
| Conversation state, cross-session memory, document retrieval or history | `adk-memory-architecture` |
| Agent behaviour tests, evaluation datasets, replay or result auditing | `adk-agent-evaluation` |
| Decisions or answers are wrong on a labelled set; error analysis, one change per iteration, model comparison | `adk-agent-evaluation` (quality iteration) |
| Instruction text: prompt structure, state templating, tool-use guidance, sub-agent descriptions for routing, prompt versioning | `adk-agent-instructions` |
| Wrong tool or wrong arguments chosen, tool docstrings and parameter schemas, tool count, result size, AgentTool versus sub-agents | `adk-tool-interface-design` |
| Structured output arrives as prose or invalid JSON, response-schema design, model selection, thinking or temperature settings, model failover | `adk-model-and-output-contracts` |
| Prompt-injection resilience, MCP or tool supply-chain vetting, excessive agency, code-execution sandboxing or a pre-release security review | `adk-agent-security` |
| Missing or duplicated telemetry, token and cost attribution, SLOs and alerts, dashboards, production incidents, production traces into eval cases | `adk-agent-observability` |
| Model deprecation notices, prompt and model version pinning, eval gates in CI, canary or rollback of a release | `adk-release-engineering` |
| Personal data in prompts, tools, storage, logs or streamed answers | `protect-adk-sensitive-data` |
| Tool identity, credentials, Secret Manager or delegated OAuth | `adk-tool-auth-and-secrets` |
| Natural-language SQL agents, schema retrieval or controlled query execution | `adk-sql-agent-engineering` |

Use `adk-system-designer` for the system-design conversation. A focused feature
design or code fix stays with its topic specialist; it does not need a new
architecture interview. Preserve the user's requested design-only scope and
already agreed architecture when handing work between skills.

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

Six cross-framework specialists sit outside the chapter sequence. Three own
what the model sees and emits (`adk-agent-instructions`,
`adk-tool-interface-design`, `adk-model-and-output-contracts`); three own the
production lifecycle (`adk-agent-security`, `adk-agent-observability`,
`adk-release-engineering`).
A misrouted request often needs two of them; name the primary, keep one change
set and one measurement, and hand the measured comparison to
`adk-agent-evaluation`.

Finish with the requested explanation or the change made, validation actually
performed, and any unresolved decision or unverified behaviour. Naming a
specialist is the start of the work, not its completion.
