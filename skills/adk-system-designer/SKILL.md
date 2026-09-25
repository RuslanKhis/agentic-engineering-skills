---
name: adk-system-designer
description: >-
  Work through requirements and trade-offs with the user to design or review
  the system architecture of a Python Google ADK application on GCP, before
  implementation. Use for a new application design, a substantial redesign,
  or a cross-cutting architecture review. For a focused memory, workflow,
  frontend or deployment change, use that specialist directly.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
---

# ADK system designer

Turn a product idea or an existing architecture into a reviewable system design
through a conversation. Establish the application's guarantees, explore the
decisions that change them, and connect each important claim to an enforcement
point and a validation plan. Scale the design to the requested problem.

The deliverable is an architecture and a resumable implementation plan. This skill
does not require other skills, the book, a starter repository or cloud access.
When the user also requests implementation, finish the relevant design decisions
and continue within that existing authorization using available specialist guidance.

## Establish what is known

Read the request, supplied material and relevant project instructions. For an
existing application, inspect its architecture notes, manifests, entrypoints,
interfaces and tests without importing application code or exposing secrets.
Preserve agreed requirements, the product's domain, working infrastructure and
dependency pins. A service already present is a constraint to evaluate, not an
automatic choice for every new responsibility.

Summarize one concrete user journey, its current friction, intended outcome and
fixed constraints in a few sentences. Keep that journey as the running example
when explaining components and failures. Distinguish observed facts, user
decisions, proposals and unknowns.
For a supplied design, begin with its consequential gaps instead of repeating
an introductory interview. For a narrowly scoped design question, resolve that
question without producing a whole-application document.

## Conduct the design conversation

Ask the next question that could change the architecture, explaining which
decision depends on the answer. Usually ask one to three related questions per
turn, with concrete options when useful. Use the host's question interface if
available; ordinary chat works too.
Let the user answer before treating a material product choice as settled.

Work from the journey towards the constraints, as needed:

- What may the system read, decide and change, and for whom?
- What would a correct completed result be? Which outcomes are unacceptable?
- What should improve over the current journey, and how will we measure it?
- What already exists: login, authoritative records, frontend, storage, platform?
- What traffic, latency, cost, retention, availability and recovery targets matter?

Avoid turning these into an upfront questionnaire. Infer repository facts by
inspection. Offer a reasoned default for reversible choices. When the user does
not know a target, show how it affects the design and propose a labelled assumption
or a measurement task. Never invent a numeric requirement, provider guarantee or
user approval. If asked for a one-pass draft, proceed with explicit assumptions
and open decisions instead of requiring an interview.

Explain each consequential recommendation through:

**Requirement → design choice → reason → tradeoff → verification.**

- **Requirement:** the user need or constraint, with its confirmed or assumed status.
- **Design choice:** a specific component responsibility or interaction to adopt.
- **Reason:** how that choice satisfies the requirement under the known contracts.
- **Tradeoff:** the cost, limitation or capability forgone compared with a credible alternative.
- **Verification:** an observable check and expected result; name unresolved evidence.

Use a few sentences or a compact row; the chain guides the explanation, not five
mandatory headings on every turn. Keep the rationale visible while asking useful
questions. Read the opening example in [design decisions](references/design-decisions.md)
when a concrete illustration would help.

After an answer, summarize what changed in the requirement, choice and verification,
then address the next unresolved decision. Maintain the cumulative decision record
without repeating the whole design. A user correction can supersede an earlier
proposal; update its dependent contracts and checks as well. Compare only credible
alternatives, including ordinary code or one agent when sufficient. Additional
agents need a distinct responsibility, context, tool set or evaluation reason;
names alone do not create security boundaries.

## Turn requirements into contracts

Write observable invariants: for example, an authenticated customer sees only
their cases, and one confirmed escalation produces at most one external ticket
under a verified provider replay contract. For each critical invariant identify
the trusted enforcing component, authoritative data, failure outcome and test.
Distinguish desired guarantees from mechanisms that actually support them.

Read [design decisions](references/design-decisions.md) when translating the
journey into component, data, identity, operation and cost contracts. Select its
relevant topics; account briefly for omitted concerns instead of adding unused
memory stores, agents or infrastructure. Capture the cross-boundary consequences:

- Session, invocation and business-operation identities have different lifetimes.
- Model proposals, user confirmation and backend authorization are separate.
- Partial output, persisted conversation state and external effects have separate
  completion rules. A timeout or cancellation can leave a write uncertain.
- A stored conversation does not by itself recover interrupted work.
- Screening after storage, tool execution or streaming cannot undo that exposure.
- Model/tool fan-out and nested retries consume the same application allowance.

Read [runtime and delivery](references/runtime-and-delivery.md) when requirements
depend on context limits, result downloads, browser streams, concurrent sessions,
capacity or continuity during a release. It adds the contracts between storage,
execution and the user's visible result.

## Select ADK and GCP components for those responsibilities

Use [GCP decisions](references/gcp-decisions.md) when selecting services or
estimating capacity and cost. Separate application hosting from model inference,
conversation storage, business records, artifacts and identity. Record which
component owns retries, authorization, shared state and recovery.

Check version-dependent ADK interfaces against the target's installed/deployed
versions and current official documentation. Check service availability, regions,
limits and prices before relying on them; cite sources and dates in the design.
If lookup or credentials are unavailable, keep those decisions provisional and
name the exact verification needed. Architecture planning can proceed without
provisioning or installing an SDK. Examples from the source material are teaching
evidence, not a guarantee for this application's versions or deployment.

## Make the recommendation implementable

For each consequential choice, add a short implementation route: the ADK building
block or ordinary application component, its concrete integration point, the GCP
responsibility if needed, and the primary specialist that can implement it. Read
[implementation handoff](references/implementation-handoff.md) for the mapping
and plan contract. Distinguish inspected paths and supported APIs from proposed
modules and version checks still needed. Explain where enforcement lives; a
service name or list of skills alone is not an implementation route.

Bring this detail into the conversation as choices become clear. Use a small
interface sketch or pseudocode only when it resolves an integration question;
keep unverified code labelled and preserve a design-only request. A feasibility
gap becomes a bounded investigation with an expected decision, not a fictional
working integration.

## Review the design through requests and failures

Read [failure review](references/failure-review.md) before calling a cross-cutting
design ready for implementation. Trace a successful request and applicable failure
paths across the actual components. Explain the visible result, retained state,
possible external effects, permitted next action and recovery owner.

Revise mechanisms that cannot enforce an invariant. Record unresolved decisions
with their impact and who or what can settle them. A significant unknown can
block a particular implementation step while independent work remains possible.
Present the trade-offs to the user; a diagram or an unanswered proposal does not
mean the architecture has been agreed.

## Deliver and hand off

Keep the design and build plan in the project's existing document convention.
When none exists, use `docs/architecture/<topic>.md` and, for a multi-goal effort,
`docs/plans/<topic>.md`. A small effort can keep its plan in the design. Use chat
if requested. Adapt the [design template](assets/system-design-template.md) and
[implementation plan](assets/implementation-plan-template.md); link decisions
instead of duplicating them, and split ADRs only where useful.

Include the recommendation, meaningful alternatives, component/sequence diagrams
when useful, critical contracts, workload and budget assumptions, recovery and
verification plans, and unresolved decisions. Mark the document **draft** while
material assumptions remain unsettled; distinguish user-accepted decisions from
your recommendations. Design review is complete when each critical invariant has
an owner/mechanism/test or an explicit unresolved gap, and the user can assess the
next step. It is not evidence that the system has been implemented or tested.

Finish with dependency-ordered goals for useful end-to-end behavior. Each needs
a stable ID, linked requirement/decision, bounded changes and integration points,
primary and supporting skills, prerequisites, acceptance evidence, status and
unresolved blockers. Separate discovery questions from ready implementation;
an unknown cloud contract need not block independent local work. Give the next
ready goal and a copyable continuation prompt naming the artifacts and scope.
Record what actually ran when a goal is later completed.

The handoff reference explains optional Wayfinder and other planning workflows.
Discover and read the selected installed workflow before using it; preserve
accepted decisions and one authoritative plan. Missing optional skills do not
block creating the artifact. `adk-engineer` can continue a requested goal with
the relevant specialist instead of restarting architecture discovery.

Preserve any workflow already chosen, including Agents CLI or another design
method. Do not scaffold applications, change dependencies, implement code or run
cloud commands merely because an architecture names them. Local design work does
not authorize deployments, IAM changes, paid tests, migrations or deletion.
For separately requested external work, make targets and effects concrete and
reuse authorization already given for that scope.

Independent community project; not affiliated with or endorsed by Google.
