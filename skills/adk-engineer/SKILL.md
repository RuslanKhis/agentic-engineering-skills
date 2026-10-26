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
  version: "2026.10.26"
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

When given a ticket, a plan goal or a pasted issue, read it first. If it names
a `Primary skill` (or `primary_skill`) and supporting skills, use them;
otherwise choose from the table below. If it names companion skills, load
each at the pin recorded in the project's `AGENTS.md` (or the plan's companion
table before the first goal has written it); report a missing companion as
setup, with its install line, and continue without claiming its guidance.
Follow its design system for UI work. Treat its security rule IDs (`SB03`)
like contracts. Read its linked design and plan,
dependencies, acceptance cases and execution scope, and preserve settled
choices; restart discovery only for a material new gap. For "the next ready
goal", pick the first goal whose prerequisites are complete. On finishing, write
actual evidence and status into the ticket's Evidence section or the plan's goal
entry, one line for each design contract the goal cites (its ID, the tier
reached (offline: no SDK, policy and tool functions on duck-typed inputs;
local: the real Runner with a scripted model or a local backend; live: an
authorised call; release: the promoted build), and the acceptance cases that
showed it), one line for each security rule it cites (ID, tier reached,
acceptance cases), the companion skills loaded with their pins, with a
numbered measurement record (`M<n>`: value, baseline, window, sample,
method, owner, build) for every figure a pilot or production
run produced and an incident record (`I<n>`) for every incident, so that
`adk-presenter` can cite them, an `actual:` line with the human hours the
person reports (or `not reported`), set the ticket's status with the template's
vocabulary (`verified_local` when every acceptance case that can run offline
has run here; `in_progress` with the owed run named in Evidence when the
SDK-tier cases are written but the SDK is absent in this session; `verified_live`
after the authorised run; `done` when the owner accepts; `blocked` only for a
decision or dependency outside the ticket), and end with the run prompt for the next
ready goal or ticket. For a plan with tickets, read
[the ticket lifecycle](references/ticket-lifecycle.md) before starting and
before finishing: it covers resuming from a `Progress:` block, updating the
design's Evidence cells, running the designer's `plan_status.py`, and ending
with the designer's checkpoint prompt instead of the next ticket when a
contract delta, an open ruling, an overrun, a blocked ticket or an orphaned
contract needs a decision. When the session must stop before the acceptance
cases pass, write the `Progress:` block first.
When there is none, end instead with the prompt for the most useful follow-up: the
verification still owed (for example the SDK tests marked not run) or the new
ticket the change uncovered, written so the user can paste it.

When a specialist's instruction failed on the installed versions, the user
overrode it, or its routing had to be redirected, record a generalised field
note as [field feedback](references/field-feedback.md) describes; nothing is
sent. At the end of the session, if this session recorded a pending note and
`AES_FIELD_NOTES` is not `quiet` or `off`, offer once to share it through a
prefilled issue form that the user reviews and submits.

If the project has `agents-cli-manifest.yaml`, the user asks to use Agents CLI,
another collection already supplies the development workflow, or a ticket
names companion skills, read
[working with other skill collections](references/composition.md). It explains
how to preserve that workflow while selecting the ADK guidance for this task.

## Select and load the specialist

Choose one primary skill from the table. Add another only when the requested
change crosses its boundary. Before any edit, tell the user in one line:
"Specialist: <name>, because <reason>", plus any supporting skills.
If the engineer keeps a practice profile, read
[practice profile](references/practice-profile.md) next and apply the org's
lessons tagged with that specialist and its stack conventions.

| Request concerns | Specialist skill |
| --- | --- |
| Where AI should be introduced at all, which workflow or use case to improve first, what business outcome to measure, or whether an agent, classical ML, rules or a process change is the right tool | `adk-discovery` |
| Whole-application architecture, requirements and trade-offs before coding, or a cross-cutting system review | `adk-system-designer` |
| Workflow structure, handoffs, parallel work, loops, events or callbacks; resume versus a durable-execution engine (Temporal, DBOS) when a run must survive a worker restart or wait days for a person | `adk-workflow-design` |
| External API retries, deadlines, duplicate writes, uncertain outcomes, or writes that must be tamper-evident (signed payloads, a ledger that detects an edited row) | `safe-api-tool-calls` |
| Runaway invocations, usage budgets or human approval of agent actions | `adk-operational-guardrails` |
| Hosting choice, packaging or deployment on Google Cloud | `deploy-adk-on-google-cloud` |
| Measured latency, cost, concurrency, startup or scaling problems; long sessions, context growth per turn or cache misses; a history trimming or summariser plugin, or a request rejected for a dangling function call | `optimise-adk-on-google-cloud` |
| Browser interfaces and the agent's run and stream API: JSON or SSE contracts, AG-UI, CopilotKit, agent UI states and the interface's design system, or interface widgets that tools render beside the reply (A2UI cards, tables, charts) | `adk-frontend-integration` |
| HTTP routes beyond the agent's run and stream API: domain data and migrations, the API contract or generated client, errors, CORS or headers in an ADK web application | `adk-fastapi-backend` |
| Conversation state, cross-session memory, document retrieval or history | `adk-memory-architecture` |
| Agent behaviour tests, evaluation datasets, replay or result auditing | `adk-agent-evaluation` |
| Decisions or answers are wrong on a labelled set; error analysis, one change per iteration, model comparison | `adk-agent-evaluation` (quality iteration) |
| Instruction text: prompt structure, state templating, tool-use guidance, sub-agent descriptions for routing, prompt versioning | `adk-agent-instructions` |
| Wrong tool or wrong arguments chosen, tool docstrings and parameter schemas, tool count, result size, AgentTool versus sub-agents | `adk-tool-interface-design` |
| Structured output arrives as prose or invalid JSON, response-schema design, model selection, thinking or temperature settings, model failover | `adk-model-and-output-contracts` |
| Prompt-injection resilience, MCP or tool supply-chain vetting, excessive agency, code-execution sandboxing (the executor and its policy; the GKE cluster side of Agent Sandbox is `deploy-adk-on-google-cloud`) or a pre-release security review | `adk-agent-security` |
| Missing or duplicated telemetry, token and cost attribution, SLOs and alerts, dashboards, production incidents, production traces into eval cases | `adk-agent-observability` |
| Model deprecation notices, prompt and model version pinning, eval gates in CI, canary or rollback of a release | `adk-release-engineering` |
| Consuming or exposing MCP servers, remote A2A agents and agent cards, the in-process versus remote topology choice, Gemini Enterprise or Agent Registry registration | `adk-agent-interoperability` |
| Personal data in prompts, tools, storage, logs or streamed answers; where a response screen (Model Armor or another) sits relative to tool dispatch and release | `protect-adk-sensitive-data` |
| Tool identity, credentials, Secret Manager or delegated OAuth | `adk-tool-auth-and-secrets` |
| Natural-language SQL agents, schema retrieval or controlled query execution | `adk-sql-agent-engineering` |
| A presentation, deck, narrative, questions to expect or decision memo for a proof-of-concept approval, a production decision, a results review, or a public case study | `adk-presenter` |
| Setting up, binding, updating or reviewing the engineer's own practice profile: employer or client context and lessons carried across projects, kept outside the repository (not an agent's memory) | `practice-profile` |
| A client proposal, statement of work, change request or data-and-access request letter built from the design and plan | `adk-system-designer` (engagement scoping) |
| A go-live rollout pack: user guide, quick-reference card, training plan, rollout messages, AI disclosure text, adoption metrics, hypercare exit test | `adk-presenter` (rollout pack) |
| Handing an agent's operation to a client's IT team (support tiers, RACI, alert ownership, access transfer) or a blameless postmortem for an agent incident | `adk-agent-observability` (handover) |
| Papers for a client's legal, privacy or security reviewers: which of Australian, US, EU and UK privacy and AI law applies, a regulatory memo (EU AI Act classification where the EU applies), AI impact assessment, privacy impact inputs (PIA, DPIA or US risk assessment), transfer facts, system card, records of processing, security questionnaire answers | `adk-governance-pack` |

Use `adk-system-designer` for the system-design conversation. `adk-discovery`
comes before it when the use case is not yet chosen or the business outcome is
unnamed; it ends with the designer's prompt. `adk-presenter` turns a plan's
recorded evidence into stakeholder material and never implements; a goal whose
primary skill is `adk-presenter` produces documents under `docs/presentations/`,
not code, and completes when its outline passes the deck check (a rollout pack:
when it passes the rollout check). A focused feature
design or code fix stays with its topic specialist; it does not need a new
architecture interview. Preserve the user's requested design-only scope and
already agreed architecture when handing work between skills.

Locate the selected skill through the coding agent's available-skills catalogue
and read its `SKILL.md`. When using a filesystem installation without a catalogue
entry, check the sibling directory `../<specialist-name>/SKILL.md` relative to
this installed skill directory. Resolve the specialist's references, scripts
and assets relative to its own directory, even when the installer uses symlinks.
Load only the references needed for the selected mode.

Once per session, compare this skill's `metadata.version` with the loaded
specialist's. If they differ, say in one line that an older copy is shadowing
part of the installation and give the update command from
[keeping the skills current](references/updates.md). The same reference says how to tell
the user, in one line, that a newer release is published. Never run an update
yourself, and never let this check delay or block the work.

The installer does not automatically install dependencies for this entry skill.
If a selected specialist is unavailable, name the missing skill and show:

```bash
npx skills@latest add RuslanKhis/agentic-engineering-skills --skill <specialist-name>
```

Replace the placeholder with the actual skill name and have the user restart
the coding agent; an already running session keeps the skill list it started
with. Continue independent inspection, and resume specialist-dependent work
once its instructions are available.

A goal or ticket may also list a Google product skill as
`google/skills:<name>` among its supporting skills (for provisioning,
querying or administering the Google Cloud product a route needs). That skill
operates the product; the specialist still decides what the application
needs. If it is not installed, show the equivalent
`npx skills@latest add google/skills --skill <name>` command or use Google's
`finding-google-skills` router when present, continue the local work, and
record the product step as an execution-scope prerequisite in the Evidence
section.
[Working with other skill collections](references/composition.md) has the
mapping and the rules that stay ours.

Specialists refer to `$SKILL_DIR` when running their helper scripts; it means
the directory that contains that specialist's `SKILL.md`. Helper output kept as
evidence goes in `.adk-evidence/` at the project root (create it and add it to
`.gitignore`); the helpers never scan it, nor the installed skill folders. The helpers need
Python 3.11 or later; if the project's interpreter is older, use any available
3.11+ interpreter for the helper only, without changing the project. When no
interpreter at hand meets the project's `requires-python`, run the project's
tests with the newest one available, say which one ran and that it is below
the pin, and install nothing; the tests the pin matters for are reported as
not run. When the only interpreter that meets the pin lacks the project's
test runner, run what the standard library runner can collect there, the
rest on the older interpreter, and report both runs by interpreter; write
new tests so the standard library runner can collect them (`unittest`-style
classes, which pytest collects as well, so a project's pytest job is
unaffected) when that is the runner that will see them; the command for a
`tests/` directory without `__init__.py` is
`PYTHONPATH=. python -m unittest discover -s tests`, since `discover -t .`
refuses a start directory that is not a package.

## Apply the guidance

Follow the selected specialist's inspection, implementation and validation path.
Its compatibility references determine which SDK recipes fit the target.
Preserve the user's requested scope and existing authorisation. Complete local
work and make any proposed external operation concrete before requesting a
missing approval for that operation.

Build at the depth the work is for. A goal or ticket may state its phase,
delivery profile (proof of concept, internal tool, MVP, production) and depth;
otherwise infer them from the request ("demo next Tuesday", "3 hours") and say
which you assumed. Specialists describe the complete mechanism for production.
At a lighter profile, build what the acceptance cases and the floor need: no
secrets in code, a spend stop (a quota on the model project when the host's
Runner is not yours; a budget alert only warns), a pinned model, and a human
before any irreversible or outside-visible effect on real people or money. Name the
specialist controls you deliberately left out in the Evidence section, with
the later goal or trigger that would add them, instead of building them or
dropping them silently.

When a ticket creates a resource that charges while provisioned (a database
instance, a deployed vector index, a managed RAG database, minimum instances,
a reservation, a load balancer), write the deletion script beside the script
that creates it, in the same change: it deletes only what this ticket owns,
dependants before owners, refuses to run without the approved scope, and is
tested at least by a dry run. Record each such resource in the Evidence
section as one line, `<resource>: <absent | retained: reason | unknown>;
cleanup: <command>; verified: <how, when>`. When the ticket asks for a price
and the pricing page cannot be read in this session, leave the placeholder,
say so in Evidence and keep that acceptance item open; never fill it from
memory. A teardown goal or ticket completes only when the
resource list and, once it has caught up, the billing report show the
resources gone; a delete command returning successfully is where
verification starts.

A ticket's estimate is human hours with a coding agent: hands-on plus review
and verify. Before editing, compare the work the acceptance cases need with
that estimate. If it is clearly larger (for example the high end would at least
double, or a calendar wait such as provider verification appears), say so
first. Build the largest useful slice that fits, and propose the remainder as
a new ticket with its own estimate instead of silently expanding the scope.
Write the human effort still owed for this change into the ticket's Evidence
and repeat it in the final message: hours to review and verify it, what to
check, and any step only a person can do (credentials, console setup,
approvals).

When the request asks for a document a person will read (a review, a migration
plan, a changelog entry), write that deliverable first, then make the code
changes it recommends; a long change can be interrupted, and the document is
what the requester acts on.

Keep tests runnable without the ADK SDK where possible: test tool functions,
schemas and policy modules directly, and keep `google.adk` imports out of
package `__init__.py` files and out of the module that defines the tool
functions so those tests can import them; when a project keeps its tools
inside the agent module, moving them out is in scope for any testing or
security request, because the suite cannot import them otherwise. `adk web` discovers
`<package>/agent.py:root_agent` without any export from `__init__.py`; only
when the package must also export `root_agent` does a module-level
`__getattr__` that imports on first access keep both working (confirm
discovery once on the target). Tests that need the
SDK or a live model are written but reported as **not run** when the SDK is
absent (a duck-typed stand-in passed to your own callback or policy function
proves that function, and is labelled so; the rule below is about faking
the Runner, the flow or the confirmation protocol); never imitate the SDK
with hand-built stand-ins and call the result a
pass.

For example, “add memory” starts with `adk-memory-architecture`. Determine
whether the need is conversation state, an exact profile setting, facts across
sessions or document retrieval before selecting a store. Add data-protection
guidance when the requested data flow needs that work. Add evaluation guidance
when the task calls for an agent evaluation strategy; ordinary regression tests
remain part of the memory implementation itself.

Seven cross-framework specialists sit outside the chapter sequence. Three own
what the model sees and emits (`adk-agent-instructions`,
`adk-tool-interface-design`, `adk-model-and-output-contracts`); three own the
production lifecycle (`adk-agent-security`, `adk-agent-observability`,
`adk-release-engineering`); one owns the process boundary
(`adk-agent-interoperability`, for MCP and A2A).
A misrouted request often needs two of them; name the primary, keep one change
set and one measurement, and hand the measured comparison to
`adk-agent-evaluation`.

Finish with the requested explanation or the change made, validation actually
performed, and any unresolved decision or unverified behaviour. Naming a
specialist is the start of the work, not its completion.
With a practice profile, offer its harvest ([practice profile](references/practice-profile.md), step 5).
