# The Skills

This is the full catalogue: for every skill, when it helps, what to ask
for, and example prompts. The [README](../README.md#the-skills) has the
one-line summary of each.

*The contents · A discovery skill, a system designer, one entry point, a presenter, a governance pack, a portability planner, eleven chapter specialists, a web backend specialist, seven cross-framework specialists and an optional practice profile.*

Choose a skill by the problem you need to solve. Each entry below explains
when it helps, what to ask for, and the command that selects it. The numbered
specialists follow Chapters 0–10 of the book; no chapter reading is required.

| What you need | Skill |
| --- | --- |
| Where AI fits, which use case first, what to measure, whether an agent, classical ML, rules or a process change is the right tool, and the countermeasures for the reasons AI projects stall | [adk-discovery](#adk-discovery) |
| A system-design conversation and architecture before implementation | [adk-system-designer](#adk-system-designer) |
| Help choosing an approach or combining concerns | [adk-engineer](#adk-engineer) |
| A presentation for a proof-of-concept approval, a production decision, a results review or a public case study | [adk-presenter](#adk-presenter) |
| Your employer's and clients' context and lessons, kept outside every repository and offered as defaults in the next project | [practice-profile](#practice-profile) |
| Draft papers for a client's counsel, DPO or CISO: which of Australian, US, EU, UK, New Zealand, Singapore and Canadian law applies, regulatory memo with the EU AI Act classification, impact assessment, PIA or DPIA inputs, transfer facts, system card, processing records, security questionnaire, and draft answers to DTA or NSW AIAF forms for a government agency | [adk-governance-pack](#adk-governance-pack) |
| A separate lock-in and portability plan for an accepted GCP and ADK design: AWS and Azure alternatives, other agent frameworks, replacement boundaries, migration risks | [adk-portability-planning](#adk-portability-planning) |
| Sequential steps, parallel work or bounded loops | [adk-workflow-design](#adk-workflow-design) |
| Reliable API calls and protection against duplicate actions | [safe-api-tool-calls](#safe-api-tool-calls) |
| Usage limits, repeated-tool protection or human approval | [adk-operational-guardrails](#adk-operational-guardrails) |
| A hosting choice or deployment preparation | [deploy-adk-on-google-cloud](#deploy-adk-on-google-cloud) |
| Faster replies and lower model usage | [optimise-adk-on-google-cloud](#optimise-adk-on-google-cloud) |
| A browser interface, streaming or tool progress, its design system and agent UI states | [adk-frontend-integration](#adk-frontend-integration) |
| The web backend around the agent: sign-in check, own-record routes, migrations beside ADK's tables, API contract and typed client | [adk-fastapi-backend](#adk-fastapi-backend) |
| Conversation history, memory or document retrieval | [adk-memory-architecture](#adk-memory-architecture) |
| Repeatable tests and trustworthy evaluation results | [adk-agent-evaluation](#adk-agent-evaluation) |
| Sensitive-data controls across prompts, tools and replies | [protect-adk-sensitive-data](#protect-adk-sensitive-data) |
| Tool identity, credentials or per-user OAuth | [adk-tool-auth-and-secrets](#adk-tool-auth-and-secrets) |
| Controlled natural-language analytics and SQL execution | [adk-sql-agent-engineering](#adk-sql-agent-engineering) |
| Agent instructions, state templating and sub-agent descriptions | [adk-agent-instructions](#adk-agent-instructions) |
| Tool docstrings, parameter schemas, tool count and result shape | [adk-tool-interface-design](#adk-tool-interface-design) |
| Structured output, model choice, thinking settings and failover | [adk-model-and-output-contracts](#adk-model-and-output-contracts) |
| Prompt-injection resilience, MCP vetting, sandboxing and red-teaming | [adk-agent-security](#adk-agent-security) |
| Tracing, metrics, SLOs, alerts and production-to-evaluation hand-off | [adk-agent-observability](#adk-agent-observability) |
| Version pinning, CI eval gates, model migration, canary and rollback | [adk-release-engineering](#adk-release-engineering) |
| MCP servers, remote A2A agents, agent cards and registration | [adk-agent-interoperability](#adk-agent-interoperability) |

**Copy any example into your coding agent's chat.** Examples use Claude Code's
`/` prefix. In Codex, replace only the leading `/` with `$`; keep the skill name
and request the same. In Gemini CLI or an Antigravity IDE integration, replace
`/skill-name` with “Use the skill-name skill to” and keep the request.
Antigravity 2.0 and its CLI also support the slash form. Adapt the scenario to your project.

## [adk-discovery](../skills/adk-discovery/SKILL.md)

*Before design · Find where AI pays off and pick the first use case.*

Use this when a company wants "AI" but has not said where, or has only a rough
area in mind. It works in two entry modes. With a rough area, it finds where
the current journey breaks (which step people abandon, re-key or wait on),
picks the first workflow to improve and the business outcome to measure, with
its baseline. With no use case at all, it asks what the business does, which
KPIs matter and which processes drive them, then proposes where AI, ordinary
automation or a process change would make a difference. Every opportunity gets
a technology fit: an agent, a single LLM call, classical machine learning,
rules or scripting, or no software at all, with the reason in a sentence a
stakeholder can repeat. It records the hypothesis chain and a counter-metric,
ranks the portfolio with a small helper so the arithmetic is not done in the
model's head, and checks the brief against the thirteen reasons AI projects
stall for reasons other than the model (a misframed problem, no baseline, an
unchanged workflow, no senior owner, no human-validation point, inaccessible
data, unmodelled cost, missing risk controls, ignored training, no feedback
loop, a pilot never embedded, build-or-buy on pride, model churn), each with
the field that answers it. It saves `docs/discovery/<topic>.md`, ends with
the exact `adk-system-designer` prompt, and offers to draft the
proof-of-concept approval presentation from the brief. It does not write contracts, architecture or
goals; that is the designer's job, and the designer does not reopen the
choice.

**Invoke:** Claude Code `/adk-discovery` · Codex `$adk-discovery`

Gemini CLI / Antigravity: "Use the adk-discovery skill to…"

<details>
<summary>Three practical examples</summary>

```text
/adk-discovery We sell advertising to small businesses and leadership wants
to use AI to sell more easily, but nobody has said where. Ask me about the
buying journey, find where advertisers drop out, and tell me which workflow
to improve first and what we would measure.
```

```text
/adk-discovery I run a regional logistics firm and do not know how AI agents
work or where they would help. Ask me about the business, its numbers and
its processes, then tell me where AI, plain automation or a process change
would pay off, and what to try first.
```

```text
/adk-discovery Here are five ideas our teams proposed for AI. Score them on
value, feasibility, data readiness and risk, say which need an agent and
which are really classical ML or a script, and write the brief for the one
we should start with.
```

</details>

## [adk-engineer](../skills/adk-engineer/SKILL.md)

*Start here · Choose the right specialist.*

Use this when you can describe the outcome but are unsure which skill fits.
It inspects your project, selects the relevant installed specialist, and follows
that skill through the requested explanation, design, code change or review.
It can combine specialists when a change crosses several concerns, and loads
their instructions as needed.

**Invoke:** Claude Code `/adk-engineer` · Codex `$adk-engineer`

Gemini CLI / Antigravity: “Use the adk-engineer skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-engineer Add memory so our support agent remembers a user's preferred
language between conversations. Use our existing database and let users
change or forget the preference.
```

```text
/adk-engineer Our agent sometimes issues a refund twice after a timeout.
Trace the tool call, fix the cause and add a regression test.
```

```text
/adk-engineer We have a working Python ADK agent and an existing React app.
Plan how to connect them with streamed replies and private user sessions.
Identify the code and tests we will need.
```

</details>

## [adk-system-designer](../skills/adk-system-designer/SKILL.md)

*Design first · Work out what the application must guarantee.*

Use this to design a new ADK/GCP application, rethink an existing architecture,
or review decisions that span several parts of the system. It asks a few useful
questions at a time, explains trade-offs and helps choose the smallest architecture
that meets your requirements.

It sizes the design to the team: a proof of concept, an internal tool, an MVP
and a production service each get a different depth per concern, a capacity
check against the people and hours available, and a phased plan with a cut
line you confirm.

It works through **requirement → contract → design choice → reason →
tradeoff → verification → evidence**. A requirement is what you need
("advertisers can buy campaigns"). A contract is a precise, observable promise
derived from it ("one confirmed purchase creates at most one order"). One
requirement usually splits into several contracts: here a quote, a
confirmation bound to the exact order, the purchase operation and the status
shown from real receipts. Each contract is numbered and records its invariant,
scope, authoritative source, where it is enforced (and checked again before the
effect), the failure outcome and its evidence. Decisions cite the contracts
they enforce, goals cite the contracts they prove, and `adk-engineer` records
evidence against each one, so you can always answer "what proves C3?". A
read-only demo needs a handful of contracts; money, orders or publishing need
more. When your answers change a requirement, it revises the affected
contracts and the choices, goals and checks that depend on them.

The result is a system design with component and request-flow diagrams where
useful, data ownership, identity and tool permissions, failure recovery, latency
and cost assumptions, plus an implementation plan. Each important choice includes
an ADK or application component, its GCP responsibility and the skill that can
help implement it. Goals record dependencies, acceptance checks, blockers and a
prompt for continuing the work in another session. Decisions and open questions
stay explicit. A focused request such as “add memory” still belongs with the
memory specialist.

The usual artifacts are `docs/architecture/<topic>.md` and
`docs/plans/<topic>.md`, adapted to your project. A small plan can stay in the
design document. See the [copyable design-to-tickets walkthrough](journeys.md#from-design-to-working-tickets)
and [guide to continuing the work](integrations/design-to-implementation.md).

For agency and consultancy work it also turns the brief, design and plan
into a statement of work, a change request and the letter asking the client
for data and access: deliverables mapped to plan goals, acceptance criteria
written as measured rates on agreed cases (never "the agent answers
correctly"), dated client dependencies, fees from the schedule check's
hours at the rate you supply, run cost from the cost ledger, and an AI-terms
checklist built on the EU model contractual clauses for AI procurement. A
helper fails the SOW when its hours, goals, dates or thresholds disagree
with the plan.

**Invoke:** Claude Code `/adk-system-designer` · Codex `$adk-system-designer`

Gemini CLI / Antigravity: “Use the adk-system-designer skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-system-designer I want a customer-support agent using ADK and GCP.
It should explain case status and create escalations. Talk me through
the requirements and trade-offs, then write the architecture before we code.
```

```text
/adk-system-designer We already have React, OIDC login and PostgreSQL.
Help design an ADK assistant that can request refunds. Work through user
permissions, approval, duplicate requests, recovery and cost controls.
Keep our existing stack and capture the decisions in docs/architecture/.
```

```text
/adk-system-designer Review our proposed multi-agent architecture on GCP.
Trace a successful request, a denied user, a lost tool response and a worker
restart. Identify unnecessary components and gaps in our guarantees.
Give us a revised design and acceptance plan; do not implement it yet.
```

</details>

## [adk-presenter](../skills/adk-presenter/SKILL.md)

*At every decision · Show the value, with evidence under every claim.*

Use this when the work must be presented to the people who decide what
happens next: approval to build a proof of concept, a review of that proof of
concept with a production decision, a final results review, or a public case
study to share with Google or the wider world. For each stage it prepares two
versions, one for business decision-makers (the decision requested, results
against the criteria agreed in advance, cost, risk, options) and one for the
technical teams who will inherit the system (architecture, contracts,
evidence, operations, handover). It reads the discovery brief, the design and
the plan, takes every number from recorded evidence, labels anything
unmeasured as a hypothesis, and writes a slide outline with an action title
and an evidence citation per slide, the speech itself as speaker notes
(bottom line first, one real case, three reasons, what did not work and the
answer, options and the decider, with timings per stage), the questions to
expect with a protocol for answering them, and a one-page decision memo.
Its slide-craft reference turns the outline into assertion-evidence slides:
one claim, one visual, the baseline drawn, a caption with sample and method.
A helper checks the outline: a number without a source, a slide without
evidence, or a missing stage topic fails the check; hype words, over-long
titles or bodies, and notes that overrun the minutes are warned. The
designer plans these presentations as goals at each phase boundary. After
launch it writes the sponsor's monthly one-page value report: outcome
against the discovery baseline, counter-metric, adoption, cost per outcome
against the estimate, incidents and thresholds fired, ending in a stop,
continue or scale call; a second helper fails a figure that cites no
measurement or incident record, a missing baseline, a stale measurement
window, an assumption presented as measured, a cost per outcome without
both its parts, and an unreported incident.

At go-live it also writes the rollout pack for the people who will use the
agent and their managers: a user guide and quick-reference card whose every
"it will" and "it won't" cites the design contract behind it, a training
plan, rollout messages for the sponsor, middle managers and frontline
users, the AI disclosure text (EU AI Act Article 50, applying since 2
August 2026), adoption metrics with "active user" defined and a
counter-metric, a "report a problem" route mapped onto the observability
skill's feedback record, and a hypercare exit test with numeric
thresholds. A second helper checks the pack's structure and citations.

**Invoke:** Claude Code `/adk-presenter` · Codex `$adk-presenter`

Gemini CLI / Antigravity: "Use the adk-presenter skill to…"

<details>
<summary>Three practical examples</summary>

```text
/adk-presenter We need leadership's approval for a four-week proof of
concept. Build the business presentation from docs/discovery/ads.md and
docs/plans/ads.md: the problem, the hypothesis, the success criteria we
will be judged on, cost, risks and the decision we are asking for.
```

```text
/adk-presenter The proof of concept is finished and its evidence is in
docs/plans/ads.md. Prepare the production-approval presentation for
leadership and a separate technical one for the platform team, with the
questions each will ask. Two acceptance cases were never run; say so.
```

```text
/adk-presenter The agent has run in production for a quarter with measured
results in docs/plans/ads.md. Draft the final results presentation and a
public case study, and list the approvals and numbers we need before
sharing it with our Google Cloud account team.
```

</details>

## [practice-profile](../skills/practice-profile/SKILL.md)

*Across projects · Stop retyping each client's context.*

Use this when you build for an employer or several clients and keep
re-explaining the same things: what the business is judged on, its sector
and jurisdictions, who decides and who must sign, which data and systems are
involved, its AI policy and past AI attempts, procurement lead times and
consultation duties, how long a proof of concept usually gets, the region
and stack, the security floor, how decks should look, and what the last
project taught you. You fill it once, either through a short interview
(sixteen core questions, about fifteen minutes) or by naming Markdown or
text files you already have, such as a strategy or an AI policy. From those
files it proposes one line at a time, each shown with its quote and
`file:line`. Lines with secrets or personal data, and any text that tries
to instruct the assistant, are held back and reported, never offered. It keeps
them as short Markdown files outside every repository
(`~/.agentic-engineering`, or `$AGENTIC_ENGINEERING_HOME`), one directory per
org, and binds each repository to one org by its path, so one client's facts
never reach another client's project. Discovery and the designer then offer
the org's values as defaults you accept in a word, labelled with where they
came from; the presenter takes the audience and style, never numbers; and
`adk-engineer` applies the lessons tagged with the specialist it chose. It
writes only a diff you approve, built from what you said, what the project
recorded or document lines you accepted one by one, and refuses secrets and
personal data. A one-page company context brief can be exported for a
teammate or a proposal; whoever receives it brings it in through the same
line-by-line import. It deliberately avoids your coding agent's global
memory files, which load in every project. Without a profile, every skill
behaves as before.

**Invoke:** Claude Code `/practice-profile` · Codex `$practice-profile`

Gemini CLI / Antigravity: "Use the practice-profile skill to…"

<details>
<summary>Three practical examples</summary>

```text
/practice-profile Set up my practice profile. I work for clients; this repo
is for Acme Retail: europe-west2, Terraform, two-week proofs of concept with
one developer, and a human approves anything sent to a customer. Bind this
repo to Acme.
```

```text
/practice-profile Import docs/client/strategy-2026.md and
docs/client/ai-policy.md into Acme's profile, then ask me the core
questions they don't answer.
```

```text
/practice-profile Review Acme's profile: what is stale, and what should go?
```

</details>

## [adk-governance-pack](../skills/adk-governance-pack/SKILL.md)

*Before production · Draft what the client's reviewers sign.*

Use this when a client's counsel, data protection officer or security team
asks for papers before a pilot or production decision. It reads the
discovery brief, the design and the plan's evidence and first screens which
regimes apply, always in the order Australia, United States, EU, UK, New
Zealand, Singapore, Canada: where the client is, where the people whose data
it handles are (the Canadian province included), where the data is processed
(including the agency's own staff in Australia), the client type (a NSW or
Commonwealth agency among them), the sector and whether outputs feed
decisions about people. An unknown fact keeps a regime in scope. It then
drafts a regulatory memo: the full EU AI Act classification where the EU
applies (prohibited practices, Annex III high-risk areas such as hiring or
credit, Article 50 transparency, provider and deployer roles) and, for the
other six regimes, which have no AI Act, a screen of the laws that do apply
(the Privacy Act and APP 1.7 automated-decision transparency, and for NSW
agencies the PPIP and HRIP Acts, GIPA, State records, the NSW Cyber Security
Policy and ICTA contract AI clauses; California's CPPA rules, Colorado, NYC
Local Law 144, state privacy and sector laws; UK GDPR as amended by the Data
(Use and Access) Act 2025, the Equality Act and the FCA; New Zealand's
Privacy Act 2020 and IPP 3A; Singapore's PDPA and its data intermediaries;
PIPEDA and Quebec's Law 25 in Canada). Alongside it come an AI impact
assessment along ISO/IEC 42005 mapped to the NIST AI RMF, a privacy impact
input pack that serves as each regime's PIA, DPIA or risk assessment, a
transfer assessment annex for EU, UK, New Zealand, Singapore and Quebec data
the agency reaches from Australia, a system card with an automated-decision
disclosure block, records-of-processing rows under GDPR or UK GDPR, a
security questionnaire answer bank and, for a Commonwealth or NSW agency,
draft answers in the official form's order for the DTA AI impact assessment
or the NSW AIAF, from crosswalks that never copy the forms. Every statement
cites a contract, decision or evidence ID, or is marked as an assumption or a
question for counsel or the agency; every draft carries a drafting-aid
banner and a sign-off table only its reviewer fills. These are drafts that
support the client's lawyer, not legal advice. A proof of concept gets a
one-page note; a pilot or production service gets the full pack. A helper
fails a draft with no jurisdictions, a screen missing any of the seven
regimes, a section for a regime not in scope, an uncited statement, an
invented ID, a legal date without the day it was checked, form answers
without their form version and checked date, or a high-stakes fact (hiring,
credit, housing, insurance, health, children, biometrics, a government
client, an exclusively automated decision) without a counsel flag. The
designer plans it as a goal before the production decision.

**Invoke:** Claude Code `/adk-governance-pack` · Codex `$adk-governance-pack`

Gemini CLI / Antigravity: "Use the adk-governance-pack skill to…"

<details>
<summary>Three practical examples</summary>

```text
/adk-governance-pack The client's counsel and DPO want the governance papers
for the CV-screening assistant before the pilot decision. Draft them from
docs/discovery/hiring.md, docs/architecture/hiring.md and docs/plans/hiring.md.
```

```text
/adk-governance-pack Their CISO sent a vendor security questionnaire about
our policy assistant. Draft the answer bank and a system card from what the
design and plan record, and mark what is only planned.
```

```text
/adk-governance-pack We are about to start a two-week proof of concept on
real customer emails for a UK client, and our Sydney team will read the
traces. Write the one-page note and data-flow summary for the client's
privacy team.
```

</details>

## [adk-portability-planning](../skills/adk-portability-planning/SKILL.md)

*Optional · Answer a lock-in question without changing the build.*

Use this when stakeholders worry about vendor lock-in for an accepted design:
the parent company may standardise on AWS or Azure, a platform team wants an
exit plan, or someone asks what replacing ADK with another agent framework
would take. This toolkit builds production Google ADK applications on GCP,
and that stays the primary build; portability planning is optional, and the
designer plans it as a goal only when you say yes to its one lock-in
question. It reads the design and plan, then classifies each component as
shared logic, a replaceable adapter, provider-specific by choice or an
expensive dependency, citing the design's IDs. It assesses cloud, agent
framework, model, service and deployment portability separately, compares
the AWS and Azure equivalents and a small set of other agent frameworks with
official sources and the dates they were read, and names the boundaries
worth keeping, what each costs now, the feature differences and the
migration risks. It ends with a recommended strategy and a phased outline
whose relative effort (small to very large, or unknown) states its drivers rather
than inventing hours or prices. It writes one document,
`docs/portability/<topic>.md`, and a helper fails it for a missing section,
an invented ID, a source without a read date, an unsupported figure, a
promise such as "fully portable" or infrastructure code. It does not build a
second application, write Terraform, IAM policies or Kubernetes manifests,
change the GCP design or its goals, or recommend running on several clouds
by default; changes to the current build appear only as optional
recommendations for a designer checkpoint.

**Invoke:** Claude Code `/adk-portability-planning` · Codex `$adk-portability-planning`

Gemini CLI / Antigravity: "Use the adk-portability-planning skill to…"

<details>
<summary>Three practical examples</summary>

```text
/adk-portability-planning Our CTO worries we'll be locked into Google because
the parent company may standardise on AWS. Using docs/architecture/claims.md
and docs/plans/claims.md, write up what a move would involve. Don't change
the GCP build.
```

```text
/adk-portability-planning The platform team asks which parts of the support
assistant's design are Google-specific on purpose and which boundaries are
worth keeping now. Include what replacing ADK with LangGraph would take.
```

```text
/adk-portability-planning Procurement wants an exit plan for the policy
assistant before a three-year Google Cloud commitment, with Azure as the
alternative. The agent framework is not a concern; say why in the plan.
```

</details>

## I. Foundations & safeguards

*Give the system a structure, then give it boundaries.*

### [adk-workflow-design](../skills/adk-workflow-design/SKILL.md)

*00 · Arrange the work and make sure it finishes.*

Use this to decide which steps run in order, which can run together, and when
a refinement loop should stop. It helps implement or repair the handoffs
between agents, shared state and final results. It also covers carrying on
from saved stages after an input changed, a checkpoint too large for its
store, a run that waits days for approval across restarts (ADK resume or a
durable engine), consistency checks on drafts and warning-only corrections.
Ask for a workflow design, a focused code change, or tests that show each step
produces the required output.

**Invoke:** Claude Code `/adk-workflow-design` · Codex `$adk-workflow-design`

Gemini CLI / Antigravity: “Use the adk-workflow-design skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-workflow-design Build a workflow that researches a topic, drafts an
answer, then checks it. Pass each step's result to the next and test what
happens when the research step fails.
```

```text
/adk-workflow-design Our agent fetches a customer's orders and support
tickets one after the other. Run these independent lookups in parallel,
then combine both results without losing either one.
```

```text
/adk-workflow-design Our writer and reviewer keep revising forever.
Limit them to three revision rounds and return an explicit result when
the reviewer still rejects the draft.
```

</details>

### [safe-api-tool-calls](../skills/safe-api-tool-calls/SKILL.md)

*01 · Handle unreliable APIs without repeating an action by accident.*

Use this when a tool calls an external service that can fail, hang or return
an unclear result. It helps add selective retries, time limits and protection
against duplicate writes where the provider supports it. The result should
include tests for failures and an honest response when an action's outcome
cannot yet be confirmed.

**Invoke:** Claude Code `/safe-api-tool-calls` · Codex `$safe-api-tool-calls`

Gemini CLI / Antigravity: “Use the safe-api-tool-calls skill to…”

<details>
<summary>Three practical examples</summary>

```text
/safe-api-tool-calls Our order lookup fails on occasional 429 and 503
responses. Add retries for recoverable failures, respect Retry-After,
and keep the complete lookup within a five-second budget.
```

```text
/safe-api-tool-calls This refund tool retries after a timeout and can
refund twice. Inspect the provider's duplicate-request guarantees and
fix the tool to preserve one logical refund across supported retries.
```

```text
/safe-api-tool-calls The booking API may accept a reservation before our
connection drops. Add an uncertain-result path and a status check so
the agent does not blindly submit another booking.
```

</details>

### [adk-operational-guardrails](../skills/adk-operational-guardrails/SKILL.md)

*02 · Put limits and approval checks around agent actions.*

Use this when an agent repeats tools, consumes too much model usage, runs too
long, or needs a person to approve an action. It helps put enforcement in the
application code that actually runs the work, with tests showing that blocked
actions never execute. It also helps design usage accounting across turns
and application controls for reducing spend, including escalation rates and
review-queue load, and paid continuations after a lost response, admitted
against a shared attempt ledger.

**Invoke:** Claude Code `/adk-operational-guardrails` · Codex `$adk-operational-guardrails`

Gemini CLI / Antigravity: “Use the adk-operational-guardrails skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-operational-guardrails Our agent keeps calling the same failing tool.
Stop repeated calls with identical arguments, cap model calls at ten per
request, and test that blocked calls never reach the tool.
```

```text
/adk-operational-guardrails Add a token allowance that accumulates across
a user's conversation. Refuse further model work when it is exhausted
and return a clear message without another model call.
```

```text
/adk-operational-guardrails Require human approval before the agent
cancels an order. Bind approval to that specific cancellation and test
rejection, repeated approval and attempted execution before approval.
```

</details>

## II. From runtime to interface

*Find a home for the agent, refine its performance, and open the conversation.*

### [deploy-adk-on-google-cloud](../skills/deploy-adk-on-google-cloud/SKILL.md)

*03 · Choose a host and prepare the files needed to run there.*

Use this to compare Cloud Run, managed Agent Runtime and Google Kubernetes
Engine (GKE), or adapt an existing project for your chosen host. It helps
prepare packaging, runtime identity, configuration, health checks and
verification steps. You can request a recommendation or locally checked
deployment files before doing any cloud deployment.

**Invoke:** Claude Code `/deploy-adk-on-google-cloud` · Codex `$deploy-adk-on-google-cloud`

Gemini CLI / Antigravity: “Use the deploy-adk-on-google-cloud skill to…”

<details>
<summary>Three practical examples</summary>

```text
/deploy-adk-on-google-cloud We have an ADK agent behind a custom FastAPI
service and no Kubernetes platform. Compare Cloud Run and Agent Runtime
for our project and recommend a host with a concrete deployment plan.
```

```text
/deploy-adk-on-google-cloud Prepare this existing API for Cloud Run.
Add the container configuration, a health check and a deployment runbook.
Validate locally and leave cloud deployment for later.
```

```text
/deploy-adk-on-google-cloud Review our agent's GKE manifests. Check the
runtime identity, startup and readiness probes, configuration and session
storage. Report specific changes with verification steps.
```

</details>

### [optimise-adk-on-google-cloud](../skills/optimise-adk-on-google-cloud/SKILL.md)

*04 · Find where time and model usage go before changing the system.*

Use this for slow replies, growing token usage, startup delays or problems
under concurrent load. It traces the request through tools, model calls,
session storage and hosting, then targets a measured bottleneck. Expect a
focused improvement with a comparison plan, or instrumentation and hypotheses
when the project has no measurements yet.

**Invoke:** Claude Code `/optimise-adk-on-google-cloud` · Codex `$optimise-adk-on-google-cloud`

Gemini CLI / Antigravity: “Use the optimise-adk-on-google-cloud skill to…”

<details>
<summary>Three practical examples</summary>

```text
/optimise-adk-on-google-cloud Our replies take about twelve seconds.
Add timing around model calls, tools and session storage so we can locate
the delay, and show how to compare requests consistently.
```

```text
/optimise-adk-on-google-cloud Token usage grows on every turn because we
keep passing full tool results and conversation history. Inspect what
the model needs, reduce avoidable context and test answer completeness.
```

```text
/optimise-adk-on-google-cloud This Cloud Run service is slow on the first
request and under concurrent load. Review our startup path, configuration
and supplied traces, then propose changes with a measurement plan.
```

</details>

### [adk-frontend-integration](../skills/adk-frontend-integration/SKILL.md)

*05 · Connect the agent to the person using it.*

Use this to connect an existing browser interface to an ADK agent through a
JSON API or a streaming interface using AG-UI and CopilotKit. It helps define
requests and responses, connect conversations to authenticated users, and
display text, tool progress and failures correctly. It also sets up a new
interface's look from a house design system (a restrained enterprise theme in
Google's DESIGN.md format, never shadcn's default) and the agent's UI states:
tool timeline, approvals, citations and a turn that fails after a partial
answer. Ask for a working integration, an interface design, or a repair to the
conversation flow.

**Invoke:** Claude Code `/adk-frontend-integration` · Codex `$adk-frontend-integration`

Gemini CLI / Antigravity: “Use the adk-frontend-integration skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-frontend-integration Connect our existing React chat to this ADK
agent through a JSON API. Reuse our login system and ensure users can
only create and continue their own conversations.
```

```text
/adk-frontend-integration Add streaming replies and tool-progress cards
to our existing CopilotKit interface using AG-UI. Check our pinned
versions and test one complete request through the browser.
```

```text
/adk-frontend-integration Our chat shows duplicate text when a final
answer arrives, and errors after partial text look like success.
Fix both cases and add tests for the actual event sequence.
```

</details>

### [adk-fastapi-backend](../skills/adk-fastapi-backend/SKILL.md)

*Build the ordinary web backend around the agent, safely.*

Use this for the HTTP application around an ADK agent: where the Runner runs,
one sign-in check that every `/api` route shares and that refuses requests
when no verifier is configured, routes that only return the caller's own
records, application tables and migrations kept apart from ADK's session
tables, the public API contract and the typed client generated from it,
errors, CORS, security headers and the single-process Cloud Run shape. FastAPI
syntax comes from FastAPI's own skill; this one covers where ADK and Google
Cloud change the answer, such as ADK's own server having no authentication.

**Invoke:** Claude Code `/adk-fastapi-backend` · Codex `$adk-fastapi-backend`

Gemini CLI / Antigravity: “Use the adk-fastapi-backend skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-fastapi-backend Add endpoints so users can list and delete the
documents they uploaded to our ADK assistant, with two-user tests.
```

```text
/adk-fastapi-backend Set up Alembic migrations for our app tables; the
agent's sessions already live in the same Postgres.
```

```text
/adk-fastapi-backend Generate a typed TypeScript client for our React app
from this backend and fail make check when it drifts.
```

</details>

## III. Memory, evidence & care

*Decide what the system knows, how to test it, and what it must protect.*

### [adk-memory-architecture](../skills/adk-memory-architecture/SKILL.md)

*06 · Remember the right information for the right person.*

Use this when an agent needs to continue a conversation, remember facts across
sessions, answer from approved documents, or look up structured history. It
helps choose the right store and connect it to the agent, with explicit rules
for who can read the data, how long it stays and how it is forgotten. Exact
settings, such as a preferred language, may belong in an ordinary profile record.

**Invoke:** Claude Code `/adk-memory-architecture` · Codex `$adk-memory-architecture`

Gemini CLI / Antigravity: “Use the adk-memory-architecture skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-memory-architecture Let users resume a conversation after the
server restarts. Use our existing database, enforce conversation
ownership and test that one user cannot load another user's history.
```

```text
/adk-memory-architecture Help our agent answer questions from approved
company manuals. Design document retrieval with source references,
document-version controls and access checks for each user.
```

```text
/adk-memory-architecture Add opt-in memory for low-risk facts users
share across sessions. Include correction, expiry and a forget action,
with offline tests for consent denial and cross-user access.
```

</details>

### [adk-agent-evaluation](../skills/adk-agent-evaluation/SKILL.md)

*07 · Test what the agent does as well as what it says.*

Use this to catch regressions in tool selection, arguments, action order,
stored effects and final answers. It helps write repeatable tests with a
scripted model, prepare evaluation cases for a real model, or audit a report
whose passing scores may hide missing checks. When the labels must come
from subject-matter experts, it plans the labelling session, the failure
taxonomy and the versioned criteria, and its helper reports Cohen's kappa
between two experts, the disagreements to adjudicate, criteria drift, and a
judge's true-positive and true-negative rates on a held-out split. It also
covers quote and citation support checks, and repairing a failed stage from
saved paid outputs without re-running them. The output is a test strategy,
executable tests, evaluation assets or evidence-backed findings.

**Invoke:** Claude Code `/adk-agent-evaluation` · Codex `$adk-agent-evaluation`

Gemini CLI / Antigravity: “Use the adk-agent-evaluation skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-agent-evaluation Add deterministic tests through our ADK runner
that force an invalid refund request. Assert that the refund tool
rejects it and no money-changing operation reaches the backend.
```

```text
/adk-agent-evaluation Create evaluation cases for a support agent that
must look up an order before cancelling it. Cover missing details,
refusal and successful cancellation. Validate the files offline.
```

```text
/adk-agent-evaluation Our evaluation report says every case passed,
but some tool failures were ignored. Audit the result files for missing
cases, failed actions and answers that falsely claim success.
```

</details>

### [protect-adk-sensitive-data](../skills/protect-adk-sensitive-data/SKILL.md)

*08 · Control what sensitive information reaches each part of the system.*

Use this when personal information or credentials could enter prompts, tools,
conversation history, logs or public replies. It helps implement or review
screening and data-handling rules, including Google Sensitive Data Protection
and Model Armor integrations, where a screen runs relative to the agent and
its tools, and prompt text leaking through trace, completion-upload or
analytics exporters. Ask for a traced data flow, a focused code change and
tests showing what happens when screening rejects data or fails.

**Invoke:** Claude Code `/protect-adk-sensitive-data` · Codex `$protect-adk-sensitive-data`

Gemini CLI / Antigravity: “Use the protect-adk-sensitive-data skill to…”

<details>
<summary>Three practical examples</summary>

```text
/protect-adk-sensitive-data Add a Sensitive Data Protection boundary
that replaces email addresses and rejects credentials before text is
saved or sent to the model. Test failures with a fake screening client.
```

```text
/protect-adk-sensitive-data Review this agent for customer data leaking
through tool results, session history, logs or traces. Map each path
and recommend specific fixes with regression cases.
```

```text
/protect-adk-sensitive-data Our API streams answers before screening
finishes. Buffer the answer, apply the configured Model Armor checks,
and test that blocked or uninspectable content is never released.
```

</details>

## IV. Trust in practice

*Secure the boundaries and work through a case study.*

### [adk-tool-auth-and-secrets](../skills/adk-tool-auth-and-secrets/SKILL.md)

*09 · Give each tool the right identity and keep credentials out of the conversation.*

Use this when tools need private Google Cloud access, an application secret,
or permission to act through a user's connected account. It helps separate
the authenticated user from the service's credentials, enforce access in
trusted code, and handle OAuth connection, refresh and disconnect flows.
Expect an implementation or review with tests for user isolation and
credential exposure.

**Invoke:** Claude Code `/adk-tool-auth-and-secrets` · Codex `$adk-tool-auth-and-secrets`

Gemini CLI / Antigravity: “Use the adk-tool-auth-and-secrets skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-tool-auth-and-secrets Our tool loads a service-account key file.
Adapt it for keyless Google Cloud credentials and document the narrow
runtime permissions it needs. Keep IAM changes as a reviewable plan.
```

```text
/adk-tool-auth-and-secrets Move our third-party API key out of agent
state and load it from Secret Manager in trusted code. Test that tool
results, errors and session events do not expose the key.
```

```text
/adk-tool-auth-and-secrets Add a per-user OAuth connection for our
calendar tool, including refresh and disconnect. Test locally that
one user's session cannot select or use another user's credentials.
```

</details>

### [adk-sql-agent-engineering](../skills/adk-sql-agent-engineering/SKILL.md)

*10 · Turn business questions into controlled, read-only analytics.*

Use this to build or improve an agent that answers questions from a database.
It helps route familiar questions to reviewed SQL templates, give the model
only relevant authorised schema information, and check proposed queries in
application code before execution. Expect a small working query path, tests
for correct answers and rejected queries, or an architecture review.

**Invoke:** Claude Code `/adk-sql-agent-engineering` · Codex `$adk-sql-agent-engineering`

Gemini CLI / Antigravity: “Use the adk-sql-agent-engineering skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-sql-agent-engineering Add a path for "What were monthly sales last
quarter?" using our approved revenue definition and a parameterised SQL
template. Test the totals and reject unsupported filters.
```

```text
/adk-sql-agent-engineering Our agent sends all 500 table schemas to the
model for every question. Retrieve only relevant authorised schemas
and test that unrelated or forbidden tables never enter its context.
```

```text
/adk-sql-agent-engineering Review our generated-query execution path.
Enforce read-only queries, allowed tables and resource limits in code,
and add tests proving rejected queries never reach the database.
```

</details>

## V. Cross-framework practices

*What the model sees and emits · Practices from across the field, implemented for ADK.*

These seven specialists did not come from a book chapter. They came from a
review of current AI-engineering practice (vendor guidance from Google,
Anthropic and OpenAI, independent studies, the official ADK documentation,
Google's samples and the ADK issue tracker) against what the toolkit already
covered. The first three own what the model sees and emits: the instruction
text, the tool declarations and the output contract. The next three own the
production lifecycle: the agent's security posture, its telemetry, and its
releases. The last owns the process boundary: MCP servers and A2A peers. Their
mechanics were checked against the google-adk 2.8.0 source and
the later changelog; see the
[gap review](research/ai-engineering-practices-gap-review.md).

### [adk-agent-instructions](../skills/adk-agent-instructions/SKILL.md)

*Write the instruction that carries the judgment, and keep it owned and tested.*

Use this when an agent follows its prompt poorly, calls tools too eagerly or
not at all, routes requests to the wrong sub-agent, or raises a templating
error on a placeholder. It covers instruction structure and altitude, ADK
session-state templating, tool-use guidance inside the prompt, sub-agent
descriptions as routing contracts, few-shot exemplars, the division between
prompt and code, model-generation notes and a prompt-as-code layout with a
contract test. A read-only linter reports unresolved placeholders, literal
braces, shouting modifiers, mandated tool calls and near-duplicate sibling
descriptions. The measured improvement loop stays with
[adk-agent-evaluation](#adk-agent-evaluation).

**Invoke:** Claude Code `/adk-agent-instructions` · Codex `$adk-agent-instructions`

Gemini CLI / Antigravity: “Use the adk-agent-instructions skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-agent-instructions Our coordinator keeps sending refund questions to
the billing agent instead of the refunds agent. Fix the sub-agent
descriptions and the root instruction, and show me the request the
model actually receives.
```

```text
/adk-agent-instructions Rewrite the system instruction for our Gemini 3
support agent. It is 1,800 words of MUST and NEVER rules, calls search on
every turn and nobody can review changes to it.
```

```text
/adk-agent-instructions Add a {customer_tier} placeholder and a JSON
output example to this agent's instruction without breaking state
templating on our pinned ADK, and give me a test that catches regressions.
```

</details>

### [adk-tool-interface-design](../skills/adk-tool-interface-design/SKILL.md)

*Design the tool the way the model will see it.*

Use this when the model picks the wrong tool or fills parameters wrongly, when
tool results flood the context, or when a new tool, toolset or MCP server needs
a model-facing schema. It covers FunctionTool docstrings and parameter rules
for the pinned ADK, naming and consolidation, tool-count budgets and dynamic
toolsets, result shaping and size, actionable error returns, and the choice
between AgentTool, sub-agents and single-turn mode. A read-only linter checks
declarations and a second helper measures tool-result sizes from recorded
events. Retries and idempotency of the external call stay with
[safe-api-tool-calls](#safe-api-tool-calls).

**Invoke:** Claude Code `/adk-tool-interface-design` · Codex `$adk-tool-interface-design`

Gemini CLI / Antigravity: “Use the adk-tool-interface-design skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-tool-interface-design Our agent keeps calling search_orders when it
should call get_order, and sometimes passes the customer name where the
order ID goes. Review the tool declarations and fix what the model sees.
```

```text
/adk-tool-interface-design We are adding a 40-tool MCP server. Help us
decide which tools to expose, how to name and filter them, and whether to
load them dynamically.
```

```text
/adk-tool-interface-design Write the docstrings, return shapes and error
messages for three new BigQuery lookup tools so Gemini uses them
reliably, and tell me how to check it.
```

</details>

### [adk-model-and-output-contracts](../skills/adk-model-and-output-contracts/SKILL.md)

*Decide what the model emits, which model emits it, and how code proves it.*

Use this when structured output arrives as prose, fenced JSON or invalid data,
when a response schema needs designing within Gemini's limits, when a model
must be chosen or escalated, or when thinking, temperature or failover settings
need to change. It covers output_schema contracts and their validation path on
the pinned ADK, repair loops with an attempt budget, output_schema together
with tools on each backend, current Gemini model IDs and lifecycle dates,
thinking_level and sampling rules for Gemini 3, and FallbackModel. Two helpers
check a response schema against the documented Gemini subset and audit a
project's model configuration. Measuring quality on a labelled set stays with
[adk-agent-evaluation](#adk-agent-evaluation).

**Invoke:** Claude Code `/adk-model-and-output-contracts` · Codex `$adk-model-and-output-contracts`

Gemini CLI / Antigravity: “Use the adk-model-and-output-contracts skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-model-and-output-contracts Our extraction agent returns fenced JSON
and sometimes plain prose instead of the Pydantic schema, and it has two
tools. Make the structured output reliable without breaking tool use.
```

```text
/adk-model-and-output-contracts Everything runs on gemini-2.5-pro with
temperature 0.2 and thinking_budget 2048. Move the right agents to a
current Flash model, set thinking per agent and add a fallback for 429s.
```

```text
/adk-model-and-output-contracts Design the response schema for our
classification agent: 40 enum values, a nested evidence list and a
nullable refusal. Keep it within Gemini's limits and tell me what the
code should validate versus what the model should decide.
```

</details>

### [adk-agent-security](../skills/adk-agent-security/SKILL.md)

*Assume the injection succeeds, and make sure it cannot do harm.*

Use this when an agent reads content it did not write (emails, documents,
search results, tool output, other agents' replies) and can also act, before
exposing MCP servers or code execution, or for a security review before
release. It threat-models the agent as a system (what it can read, what it can
change, where data can leave), maps prompt-injection design patterns onto ADK
structure, vets and pins tool and MCP supply chains, tiers tools with
confirmation, selects a sandboxed code executor, and seeds an adversarial suite
whose assertions are deterministic: a forbidden tool is never called and data
never leaves. A read-only inspector reports each agent's exposure. Findings map
to OWASP identifiers. Data screening and Model Armor stay with
[protect-adk-sensitive-data](#protect-adk-sensitive-data).

**Invoke:** Claude Code `/adk-agent-security` · Codex `$adk-agent-security`

Gemini CLI / Antigravity: “Use the adk-agent-security skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-agent-security Our support agent reads customer emails and can issue
refunds and send replies. Review it before launch and tell me what an
attacker could make it do through a poisoned email or tool result.
```

```text
/adk-agent-security We are adding three third-party MCP servers. Help us
vet, filter and pin their tools, and write tests proving a poisoned tool
description cannot make the agent leak data.
```

```text
/adk-agent-security Write adversarial test cases for indirect injection
through RAG chunks and tool results, asserting the agent never calls
delete_record or send_email without confirmation.
```

</details>

### [adk-agent-observability](../skills/adk-agent-observability/SKILL.md)

*See what the agent did, what it cost, and where the time went.*

Use this when telemetry is missing or duplicated, when token or cost
attribution is unclear, when you need SLOs, alerts or dashboards, or during a
production incident. It covers the spans, metrics and logs ADK emits and the
environment gates that control them, the exporter for each host (Cloud Run,
GKE, Agent Runtime, OTLP third parties), BigQuery Agent Analytics, feedback
capture, debugging from an alert to a trace to a session, and turning
production traces into redacted evaluation cases. Two helpers summarise
invocations from a saved session and convert sessions into an ADK eval set.
When the agent passes to a client's IT team it writes the operations
handover (support tiers with a one-accountable RACI, alert ownership,
access transfer, runbook entries, owners for model retirement, evaluation
refresh and cost review) and a blameless postmortem template that adds
affected users, harm, the client's notification decision and the
regression case to the incident note.
Content-redaction policy stays with
[protect-adk-sensitive-data](#protect-adk-sensitive-data).

**Invoke:** Claude Code `/adk-agent-observability` · Codex `$adk-agent-observability`

Gemini CLI / Antigravity: “Use the adk-agent-observability skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-agent-observability p95 latency on our Agent Runtime agent doubled
this week. Add tracing and metrics so we can tell model time from tool
time from session loading, and set an alert on it.
```

```text
/adk-agent-observability Define SLOs for the support agent: task success,
tool error rate and cost per resolved conversation, wired to Cloud
Monitoring dashboards and alerts. Keep prompts out of the traces.
```

```text
/adk-agent-observability Pull the thumbs-down conversations from BigQuery
Agent Analytics into an ADK eval set for regression, with personal data
removed, and show me what was redacted.
```

</details>

### [adk-release-engineering](../skills/adk-release-engineering/SKILL.md)

*Ship the prompt, the model and the tools as one release, and be able to undo it.*

Use this when a release, a CI gate, a model deprecation notice, a canary, a
rollback or a stale eval set is the concern. It covers prompt and configuration
versioning, pinned model and judge IDs, evaluation gates in CI with threshold,
repeat and cost policy, model-version migration with re-baselining, staged
promotion on Cloud Run and Agent Runtime, joint rollback of prompt, model,
tool schema and secrets, and refreshing eval sets from production. It records
that `adk eval` exits successfully even when cases fail on every release
through 2.12.0 (a main commit changes this), so the gate uses pytest or
conformance replay and the exit code is checked on the pinned version. A
helper inventories every model, judge, prompt
hash, eval set and deploy artefact into a release manifest. Writing the eval
cases stays with [adk-agent-evaluation](#adk-agent-evaluation).

**Invoke:** Claude Code `/adk-release-engineering` · Codex `$adk-release-engineering`

Gemini CLI / Antigravity: “Use the adk-release-engineering skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-release-engineering Google emailed that our Gemini model is retiring
next month. Plan the upgrade so our eval scores do not silently drop,
including the judge model our CI uses.
```

```text
/adk-release-engineering Add an eval gate to GitHub Actions so pull
requests that change the agent instruction are blocked on regressions,
without being flaky or expensive.
```

```text
/adk-release-engineering Canary the new system prompt to 10% of traffic
on Cloud Run and tell me how we roll back the prompt, model and tool
schema together if it misbehaves.
```

</details>

### [adk-agent-interoperability](../skills/adk-agent-interoperability/SKILL.md)

*Cross a process, team or protocol boundary without losing the contract.*

Use this when an agent must consume or offer capabilities across a boundary:
connecting to MCP servers, exposing an ADK agent as an MCP server, deciding
between in-process sub-agents and a remote A2A agent, consuming a remote agent
through its agent card, exposing an agent over A2A, or registering it with
Agent Runtime, Agent Registry or Gemini Enterprise. It covers tool-source
selection, McpToolset lifecycle and session pooling, filters and per-user
headers, SDK version contracts for both protocols, agent-card contents, task
states and failure handling, and how to test a remote peer with a fake server.
Two helpers inventory an MCP server's tools into a pinned manifest and validate
an agent card in both the 0.3 and 1.0 shapes. The MCP threat model stays with
[adk-agent-security](#adk-agent-security); in-process orchestration stays with
[adk-workflow-design](#adk-workflow-design).

**Invoke:** Claude Code `/adk-agent-interoperability` · Codex `$adk-agent-interoperability`

Gemini CLI / Antigravity: “Use the adk-agent-interoperability skill to…”

<details>
<summary>Three practical examples</summary>

```text
/adk-agent-interoperability Connect our agent to the company's GitHub and
Postgres MCP servers on Cloud Run, exposing only read tools with per-user
tokens, and pin the tool lists so we notice when a server changes them.
```

```text
/adk-agent-interoperability The billing team's agent runs in Java. Should
our ADK agent delegate refund questions to it over A2A or call their API,
and what must the agent card and failure handling look like?
```

```text
/adk-agent-interoperability Expose our research agent so Gemini Enterprise
users can invoke it, with an agent card and authentication, and validate
the card before we register it.
```

</details>
