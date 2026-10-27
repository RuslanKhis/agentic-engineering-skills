# Journeys and Combinations

The full walkthroughs behind the README's
[using skills together](../README.md#using-skills-together) summary: the three
journeys with every prompt, then how to combine these skills with Google's
Agents CLI, Google's Cloud skills and Matt Pocock's skills.

## Journey A: build a new application

**0. Find the use case first, if nobody has chosen one.** Skip this when you
already know what to build. Otherwise the discovery skill asks what the
business does and where its journey breaks, ranks the opportunities, says
which need an agent and which need classical ML, rules or a process change,
and ends with the designer's prompt:

```text
/adk-discovery Leadership wants AI in <area> but has not said where. Help me
find where it would pay off, which workflow to improve first, what outcome we
would measure, and whether an agent is even the right tool. Save the brief.
```

It saves `docs/discovery/<topic>.md`. The designer reads that brief as
answered scope and does not reopen the choice.

**1. Design it in conversation.** The designer asks only what changes the
design, offers defaults you can accept in one word, turns each requirement
into contracts the system must keep, and explains each choice as the contract
it enforces, its tradeoff and how to check it.

```text
/adk-system-designer I want to build <one-sentence product> with ADK on GCP.
I have <time and budget>; <who> will judge it as an <exploration, assignment,
pilot or production service>. Design only.
```

It first asks how much time, how many people and how much money there are,
who will use or judge the result, and what data it touches. A five-hour demo,
an internal tool for colleagues and a regulated production service get
different designs: it says which concerns are built now, which stay minimal
and which wait, and keeps a small safety floor even in a proof of concept.
When the application has its own web interface, it also asks who can reach the
URL and whether other developers will continue it. It then applies its web
defaults (a Vite and React app served by one FastAPI service, styled from the
house design system), names the companion skills each goal loads (FastAPI's
own skill, shadcn, Vercel's React rules, Playwright) with their pins, and
assigns its web security baseline: rules tagged with OWASP identifiers,
recorded once in the design with what proves each one or what defers it.

It saves `docs/architecture/<topic>.md` and `docs/plans/<topic>.md`, and ends
with the prompt for the first goal. The plan is split into phases: phase 1
fits the hours you have, phase 2 hardens or graduates it, and a later list
keeps each deferred item with what would bring it forward, so you can ship
first and continue when there is time. Every goal names its primary and
supporting specialists, an estimate of the human hours it needs when working
with a coding agent (hands-on time plus reviewing and verifying the change,
with waits such as security reviews listed separately), and its own run prompt.

**If someone worries about lock-in.** Among its first questions the designer
asks once whether vendor lock-in or future portability is a concern. The
default is no, and answering no adds nothing. Suppose you answer:

```text
Yes. Our CTO worries about lock-in: the parent company may standardise on AWS.
```

The designer still designs on GCP with Google ADK. It records the concern in
the design's scope-gate table and adds one goal to the plan, for example G07
(type portability, `Primary skill: adk-portability-planning`), which depends
only on the design and blocks no build goal, with its ticket
`docs/tickets/<topic>/G07.md`. When you reach it:

```text
/adk-engineer Carry out docs/tickets/<topic>/G07.md.
```

That produces a separate document, `docs/portability/<topic>.md`, and no
code, while G01 onward build the GCP application unchanged.

**2. Optionally turn goals into tickets.** One file per goal, for a tracker or
for parallel sessions:

```text
/adk-system-designer Turn the ready goals in docs/plans/<topic>.md into
ticket files under docs/tickets/<topic>/.
```

**3. Build, one goal or ticket at a time.**

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

```text
/adk-engineer Continue the next ready goal in docs/plans/<topic>.md.
```

Each run names the specialist it applies, loads the goal's companion skills at
the pins in the project's `AGENTS.md` (or says how to install a missing one),
verifies the goal's acceptance cases locally, records the evidence in the plan
or ticket, one line per contract and security rule, and ends with the prompt
for the next one. Nothing is deployed or paid for without your approval.

**Keep the big picture between tickets.** After each ticket the engineer runs
the designer's plan check, which reads every ticket's evidence back into the
plan: which promises are proven, which no remaining ticket will prove, what a
ticket changed or left for a decision, and whether the phase still fits the
hours. When something needs a decision, the next prompt is a checkpoint rather
than the next ticket:

```text
/adk-system-designer Checkpoint docs/plans/<topic>.md.
```

A ticket interrupted part way leaves a `Progress:` block, and the next session
resumes from it. Tickets whose files do not overlap can run in parallel, each in
its own worktree. Before each review, a journey goal checks the whole path end
to end, and the plan check's phase gate must pass. For a weekly update to your
sponsor, ask the designer for a status update; it drafts one, with a risk and
issue log, from the same records.

## Journey C: win the decision

A project is presented four times: to get the go-ahead for the proof of
concept, to show what the proof of concept did and win the production
decision, to show what the production build delivered, and, when the result
is shareable, as a public case study. The designer asks which of these
reviews the project needs and writes each as a goal in the plan (and a
ticket, if you ask for tickets), one per audience. The presenter builds each
from the evidence the goals recorded, never from a number it made up:

```text
/adk-presenter Prepare the proof-of-concept approval presentation for a
business audience from docs/discovery/<topic>.md, docs/architecture/<topic>.md
and docs/plans/<topic>.md. Fifteen minutes. Then a technical version for the
platform team.
```

```text
/adk-presenter The proof of concept is done and its evidence is in
docs/plans/<topic>.md. Prepare the production-approval presentation for
leadership and the questions they will ask; label anything unmeasured as a
hypothesis.
```

```text
/adk-presenter All production goals in docs/plans/<topic>.md are complete
with evidence. Prepare the final results presentation for the sponsor and
the leadership team: outcome against the baseline, adoption, cost, incidents
and what comes next. Then the technical handover version for the platform
team that runs it.
```

```text
/adk-presenter Draft a public case study from the production results in
docs/plans/<topic>.md, with the approvals and numbers we must gather before
sharing it with our Google Cloud account team.
```

Expect one outline per audience under `docs/presentations/<topic>/`, with
the speech written out as speaker notes in the same file, a one-page
decision memo, and a deck check that fails when a slide carries a number
without a source. The discovery skill offers the first of these prompts
when it finishes, so the approval deck can be drafted from the brief before
the design exists.

## Journey B: maintain an application

Hand `adk-engineer` a ticket, a symptom or a change. It reads the project,
tells you which specialist it is using and why, then does the work.

```text
/adk-engineer Carry out tickets/T-101.md.
```

```text
/adk-engineer Our agent picks the wrong tool for order lookups and passes the
customer's name where the order ID goes. Fix it and add a regression test.
```

```text
/adk-engineer Google says our Gemini model retires next month. Plan and make
the upgrade without silently dropping quality.
```

```text
/adk-engineer Which specialist should handle this, and why? Do not change
code yet: <paste the issue>
```

For implementation work, expect a project change, the checks that actually ran
and a clear account of what remains unverified. Find **three examples for every
skill** in the [catalogue](skills.md), and installation fixes under
[updating and troubleshooting](troubleshooting.md).

## Using Skills Together

*Bring complementary instructions to the same task.*

The collections below are optional. Install them in the same project or user
scope, then name the skills you want your coding agent to combine.

For a web application, the designer also names **companion skills** that
install into the application project rather than this toolkit: FastAPI's
bundled skill, React Router's, Vercel's React rules, shadcn's, Anthropic's
`frontend-design` for a new visual direction, and `playwright-cli`, with
Impeccable, CopilotKit and aimock when a goal needs them. The first goal
writes them with install lines and pins into the project's `AGENTS.md`. These
skills decide identity, ownership, security rules and the stream contract; a
companion decides library syntax for its pinned version; the project's
DESIGN.md decides between UI companions. The
[designer's web defaults](../skills/adk-system-designer/references/web-app-defaults.md)
list them.

### Using These with Google's Agents CLI

*Bring the project tools and the application design to the same task.*

[Google's Agents CLI](https://github.com/google/agents-cli) supplies commands,
project templates and seven skills for scaffolding, writing ADK code, evaluating,
deploying, publishing and observing agents. Its recipes also cover capabilities
such as memory, frontends, tool approval and credentials. This toolkit adds detailed
guidance for adapting those capabilities to your application's data, tools,
identity boundaries and tests. Agents CLI runs alongside the coding client
you use to work on the application.

**How are these different from Google's skills?** This collection concentrates
on implementing and checking the application-specific details in an existing
Python ADK project, while preserving its authentication, storage and dependency
pins. It can be used without adopting the Agents CLI lifecycle:

- **[Memory](../skills/adk-memory-architecture/SKILL.md):** choose between session
  state, exact preferences, semantic memory and retrieval; test consent, user
  isolation and whether a retry can restore forgotten data.
- **[API tools](../skills/safe-api-tool-calls/SKILL.md):** preserve one logical
  operation across retries and reconcile a refund whose reply was lost after
  the provider accepted it.
- **[Frontends](../skills/adk-frontend-integration/SKILL.md):** connect JSON or
  AG-UI/CopilotKit interfaces with session ownership, cancellation and correct
  handling of errors after streamed text.
- **[Evaluation](../skills/adk-agent-evaluation/SKILL.md):** assert actual tool
  effects through deterministic Runner tests, audit missing results, and
  distinguish offline evidence from live-model evaluation.

This adds focused implementation and verification guidance on topics that
overlap with Google's recipes. See the
[source comparison](research/agents-cli-comparison-2026-09-23.md) and the
[22 October 2026 note against Agents CLI 1.11.0](research/agents-cli-comparison-2026-10-22.md),
which records what the specialists imported from its skills and where they
route to them.

Use Google's workflow when you want an Agents CLI project. Bring in an Agentic
Engineering specialist for the particular feature or engineering decision:

| Work you are doing | Agents CLI contributes | This toolkit contributes |
| --- | --- | --- |
| Add memory to a generated agent | Project conventions, ADK APIs and reference recipes | Choosing what to store, user isolation, consent and forgetting |
| Evaluate a tool that changes data | Dataset and metric formats, trace generation and grading commands | Deterministic checks of actual effects, coverage and result auditing |
| Prepare and operate a deployment | Generated infrastructure, deployment commands and telemetry integrations | Hosting and identity decisions, recovery, performance analysis and sensitive-data controls |
| Publish to Gemini (formerly Gemini Enterprise) or the Agent Registry | Registration commands and platform-specific guidance | The agent card, the registration mode and the authentication and data-boundary review |

To install Google's skills alongside these in a Claude Code project:

```bash
npx skills@latest add google/agents-cli --skill '*' -a claude-code
```

For Codex, use `-a codex`; for Google's coding agents, use `-a gemini-cli`,
`-a antigravity` or `-a antigravity-cli` in the same project scope.
This installs Google's skill files; using its platform
commands also requires the Agents CLI executable. See the
[combined setup guide](integrations/agents-cli.md#install-them-together)
for the CLI installation and scope choices. Reload your coding-agent session
after installation.

For an existing Agents CLI project, try:

```text
/adk-engineer Add a remembered response-language preference to this
Agents CLI project. Use the installed google-agents-cli-adk-code skill
for its APIs and recipes, and adk-memory-architecture for storage,
consent, user isolation and forgetting. Preserve the generated project
structure and dependency pins. Implement and run offline tests;
prepare a separate plan for live evaluation.
```

In Codex, start with `$adk-engineer`. Use one entry command and name the other
installed skills in the request. Installing both collections makes their
guidance available; it does not establish an automatic integration or a rule
for resolving competing workflows. For a focused change, state the requested
scope: Google's full workflow expects scaffolding and live evaluation, while
an existing application may only need a local code change.

Read the [three worked usage examples](integrations/agents-cli.md#three-practical-workflows)
for feature development, evaluation and deployment planning. That guide also
explains how Matt's `tdd` or `code-review` can supply the development method
alongside both collections.

### Using These with Google's Cloud Skills

*Our skills decide what the application needs; Google's skills operate the product.*

[Google's skills collection](https://github.com/google/skills) holds about
170 skills for Google products: gcloud recipes, IAM policies, Cloud Run and
GKE operations, Terraform alert policies, PromQL and trace queries, database
administration and the Agent Platform services. About ten are agent-specific
and none covers building an ADK application, so there is no overlap with this
toolkit's journey, only a division of labour. A specialist here chooses the
mechanism and its contracts (which identity, which ingress, which SLI, which
store); Google's product skill carries it out (the role binding, the deploy
flags, the alert policy, the instance).

The designer writes the product skill into a goal's supporting skills as
`google/skills:<name>` with its purpose, and `adk-engineer` treats that entry
like a missing specialist: it uses the skill when installed, shows the
install command or asks Google's `finding-google-skills` router when not,
continues the local work and records the product step as a prerequisite
until you authorise it. Each specialist also names the product skill to
consult at the decision it serves, for example
`iam-helper-for-policy-management` when a role binding must be written or
`cloud-run-alert-configuration` once the SLIs are decided.

```bash
npx skills@latest add google/skills --skill '*' -a claude-code
```

Install one skill with `--skill cloud-run-basics`, or only
`finding-google-skills`, which fetches the rest on demand. Then, for a goal
that needs a product step:

```text
/adk-engineer Carry out G04 from docs/plans/warranty.md. Use
deploy-adk-on-google-cloud for the packaging, identity and readback plan and
the installed cloud-run-basics skill for the service and ingress commands.
Deploy nothing until I approve the exact command.
```

Google's skills were written for an operator at a terminal; this toolkit's
floor (scoped flags, platform identity, private by default, approval per
scope) still governs the commands they propose. The
[combined setup guide](integrations/google-cloud-skills.md) has the
mapping from each specialist to the product skills it pulls in and the
[comparison note](research/google-skills-comparison-2026-10-21.md)
records what was imported from that collection, what is routed and what was
left out.

### Using These with Matt Pocock's Skills

*Bring a development method and the ADK guidance to the same task.*

[Matt Pocock's skills](https://github.com/mattpocock/skills) cover general
engineering workflows. This toolkit contributes the ADK-specific decisions.
They can be installed alongside each other; neither collection is required
to use the other.

Some useful combinations:

| When you need to… | Matt's skill | ADK companion |
| --- | --- | --- |
| Clarify a feature and record its terminology | `grill-with-docs` | `adk-system-designer` for ADK/GCP decisions when needed |
| Resolve a large set of open architecture decisions | `wayfinder` | The designer's accepted decisions, open questions and relevant specialists |
| Turn an agreed design into a multi-session build | `to-spec` → `to-tickets` → `implement` | The designer's goal plan and each goal's primary specialist |
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

#### From design to working tickets

*One example · A support assistant with saved preferences and streamed replies.*

Give the next skill the saved architecture and plan paths. You can continue
in the same conversation or start a new one in the **same application project**.
The documents carry the decisions between sessions.

These examples use **Claude Code chat commands**. In **Codex**, replace the
leading `/` with `$`: `/to-spec` becomes `$to-spec`. In Google clients, ask
“Use the to-spec skill to…” and keep the rest of the prompt. Name supporting
skills in the request; one skill leads each step. Plugin-installed commands may
have a prefix—select the matching command from your client's picker.

For this walkthrough, choose **local Markdown** during Matt's project setup:

```text
/setup-matt-pocock-skills Use local Markdown for this project's issue tracker.
```

Follow the setup questions and review its configuration. It stores specs and
tickets under `.scratch/`. If your team already uses a configured tracker,
keep it and use the issue links it returns in place of the example file paths.
[Matt's setup and local tracker conventions](https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md).

**1. Discuss the application and save the decisions**

```text
/adk-system-designer Help design a support assistant using our existing
React app, OIDC login, PostgreSQL and Google ADK on GCP. Users should save
and forget a preferred language and receive streamed replies.
Ask me about requirements and explain the choices and tradeoffs.
When we have agreed the design, save it to docs/architecture/support-assistant.md
and the goal plan to docs/plans/support-assistant.md. Include dependencies,
ADK/GCP implementation routes, relevant skills and acceptance checks.
Identify the first goal we can build locally. Design and planning only for now.
```

Answer its questions and review the proposals. For example: “Preferences belong
to individual users; save only when they click Save; forgetting takes effect on
the next conversation.” The designer translates those answers into storage,
identity, invocation and testing decisions. Its first questions are the scope
gate: how much time and money there is, who judges the result and what they
read, and whether this is an exploration, an assignment, a pilot or a production
service. Those answers size everything that follows; for work judged on output
quality under a time limit, use the [time-boxed build order](#build-order-for-time-boxed-quality-judged-work)
instead of the ticket sequence below. **If these documents already exist,
start at step 2.** Substitute your actual paths throughout.

**2. Turn the agreed design into a specification**

A specification describes what the finished feature must do and how to verify it.

```text
/to-spec Read docs/architecture/support-assistant.md and
docs/plans/support-assistant.md. Turn the agreed local implementation goals
into the support-assistant spec using our configured local Markdown tracker.
Preserve accepted decisions, scope and acceptance checks; link both documents.
Use adk-memory-architecture and adk-frontend-integration to check the relevant
contracts while writing the spec. If an open decision blocks these goals,
identify it so we can resolve it before making those goals ready to build.
Check the proposed test boundaries with me. Create the spec only.
```

Expect `.scratch/support-assistant/spec.md` with user stories, module/interface
decisions and testing decisions. The agent may ask where tests should observe
behaviour—for example, through the authenticated API and browser. Concrete
code-path notes stay in the linked plan. [How `to-spec` works](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md).

Resolve decisions blocking the selected goals with the designer or Wayfinder
before proceeding; unrelated future decisions can stay open.

**3. Break the specification into tickets**

```text
/to-tickets Read .scratch/support-assistant/spec.md and its linked design
and goal plan. Propose tickets that each deliver a small, testable user outcome.
Carry the relevant goal/decision references, dependencies, primary ADK skill,
supporting skills and observable acceptance checks into every ticket.
Use adk-memory-architecture for preference behaviour, adk-frontend-integration
for streaming, and adk-agent-evaluation for the verification plan.
Review the breakdown with me, then write one file per approved ticket under
.scratch/support-assistant/issues/. Print their paths and the first ready ticket.
Make docs/plans/support-assistant.md point to the spec and tickets for work status.
```

Review the proposed size and order before the skill writes tickets. A useful
ticket might deliver **save → new conversation uses the preference → forget**,
including the UI, API, storage and checks. Another might deliver streamed text
with visible completed, failed and interrupted states. Each ticket should name
its blockers and skills. These are build tickets; you only need a Wayfinder map
if substantial design decisions remain open. [How `to-tickets` works](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md).

**4. Implement one ready ticket with the relevant ADK skills**

Open a fresh session in the same project. Paste the **actual ticket path**
printed in step 3; the filename below illustrates a memory ticket.

```text
/implement Implement .scratch/support-assistant/issues/01-save-language.md.
Read its linked spec, architecture and goal plan; check that its blockers are done.
Use adk-memory-architecture for the preference lifecycle, adk-tool-auth-and-secrets
for user ownership, and adk-frontend-integration for the changed UI/API boundaries.
Keep the accepted design and implement only this ticket with local tests.
Review the ticket's full changes, including staged and unstaged edits, against
its spec and the state before this ticket. Resolve actionable review findings.
Record checks and results in the ticket, and mark it complete only when its
acceptance checks pass.
Report any blocked or unverified checks. Keep live services and deployment
for their own tickets. Leave the changes uncommitted for my review.
```

Matt's `implement` leads development, testing and code review; the ADK skills
supply guidance for the affected parts. It **normally commits to the current
branch**; this example explicitly leaves changes for your review. Review the
diff and evidence, commit the accepted changes, then repeat with the next
unblocked ticket. The prompt explicitly includes uncommitted edits in the review.
For a streaming ticket, name `adk-frontend-integration` as its primary ADK skill.
[How `implement` works](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md).

**5. Check the application across ticket boundaries**

```text
/adk-agent-evaluation Review the support-assistant spec and completed tickets
under .scratch/support-assistant/. Run the relevant local checks for the whole
journey: save a language, start a new conversation, stream the reply, forget the
preference, and start again. Include another user's denied access and a stream
that fails after showing partial text. Report actual results and remaining gaps.
Separate local evidence from live-model and hosted checks still to be run.
```

Passing individual tickets is one part of verification. The combined journey
needs its own evidence; live-model behaviour and a deployed GCP application need
the corresponding evaluation and deployment work.

<details>
<summary>Return to an ADK specialist during planning or implementation</summary>

You can ask for a focused review before starting a ticket:

```text
/adk-memory-architecture Review the saved-language ticket in
.scratch/support-assistant/issues/ against the linked design and existing code.
Check ownership, persistence between conversations and forgetting. Propose
specific corrections to its implementation approach and acceptance checks.
Keep this step to planning; return the ticket path to resume with implement.
```

If implementation uncovers a product decision, return to the designer with the
ticket and the new information:

```text
/adk-system-designer While working on our saved-language ticket, we discovered
that several people share an account. Read docs/architecture/support-assistant.md,
docs/plans/support-assistant.md and the ticket in .scratch/support-assistant/issues/.
Help us decide whether the preference belongs to a person or the shared account.
Explain the implementation and testing consequences. After we agree, update the
design and affected ticket requirements; preserve unrelated accepted decisions.
Then give me a prompt to resume that ticket with implement and the relevant ADK skills.
```

For several unresolved decisions, use Wayfinder as described below. Continue
ready, independent tickets while other decisions are being resolved.

</details>

<details>
<summary>Use Wayfinder when substantial design decisions remain open</summary>

A Wayfinder map organizes **questions to resolve** before the build. For example:
individual versus team preferences, or the recovery behaviour after a disconnect.
Start from the same saved documents:

```text
/wayfinder Read docs/architecture/support-assistant.md and
docs/plans/support-assistant.md. Map the substantial unresolved design decisions.
Use support-assistant-design as the effort name. Preserve and link accepted
decisions; put adk-system-designer and the relevant ADK specialists in the map's
Notes. Our destination is a design ready for the local implementation spec.
Keep ready implementation goals in the linked plan.
```

With the local tracker, expect `.scratch/support-assistant-design/map.md` and
decision tickets in that effort's `issues/` directory. On a later session, use
`/wayfinder Continue .scratch/support-assistant-design/map.md` to work through
the next ready decision. Use the actual path returned by the agent. Keeping the
design effort separate from `support-assistant` keeps decision and build tickets
in their own directories.

When the relevant decisions are resolved, update the architecture and plan,
then return to **step 2** and include the map path in the `to-spec` request.
See the [handoff guide](integrations/design-to-implementation.md) for artifact
ownership, session resumption and direct implementation without Matt's collection.
[How Wayfinder works](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md).

</details>

#### Build order for time-boxed, quality-judged work

*One example · Decisions over a document pack, judged on unseen cases in a few hours.*

The ticket sequence above builds every control before any decision has been
measured. That is the right order for a production service. It is the wrong
order for an assignment, a pilot or an exploration that an evaluator will judge
on output quality: there, the core judgment is measured first and every other
control is a deferred ticket. Use this sequence instead:

1. **Scope gate.** Time, evaluator, artifact type, and the controls deferred with
   their reasons, at the top of the design (`adk-system-designer`).
2. **Qualify the inputs, about an hour.** An ingestion report for the supplied
   documents (scans, tables, drawings routed to OCR or vision) and a retrieval
   recall measurement on a small gold set of operative sections
   (`adk-memory-architecture`).
3. **Core judgment end to end, the largest share of time.** Draft decisions on
   the labelled development cases with exemplars, categorise the errors, change
   one thing per iteration, re-measure (`adk-agent-evaluation`).
4. **Content safeguards in code.** Consistency checks on every fresh draft,
   warnings ranked by materiality, documents treated as data
   (`adk-workflow-design`).
5. **Deliverable run with the frozen method.** The predictions the evaluator
   reads come from the method the report describes; the reserved budget is
   spent here first (`adk-agent-evaluation`, `adk-operational-guardrails`).
6. **Report within a reader's budget.** One living evaluation summary, raw runs
   as data, at most three documents named for the reviewer.
7. **Only then:** interface, revisions, export flows, recovery, hosting roadmap,
   each as a separate deferred control with its own ticket.

The [time-boxed, quality-judged walkthrough](integrations/quality-judged-build.md)
runs this order on synthetic documents with real bytes, using the bundled
ingestion, retrieval, consistency and evaluation helpers, in under an hour of
agent time. When `to-tickets` is used under this order, the first ready ticket
is the core judgment path, and no interface ticket precedes the first quality
measurement.
